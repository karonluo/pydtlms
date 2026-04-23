const chinaResidentId18Pattern = /^\d{17}[\dXx]$/
const chinaResidentId15Pattern = /^\d{15}$/
const chinaResidentIdWeights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
const chinaResidentIdChecksumMap = '10X98765432'

export function normalizeChinaResidentIdNumber(value: string) {
  return String(value || '').trim().toUpperCase()
}

function isValidBirthDate(text: string, legacy = false) {
  const candidate = legacy ? `19${text}` : text
  if (!/^\d{8}$/.test(candidate)) {
    return false
  }
  const year = Number(candidate.slice(0, 4))
  const month = Number(candidate.slice(4, 6))
  const day = Number(candidate.slice(6, 8))
  const date = new Date(year, month - 1, day)
  return date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day
}

export function isValidChinaResidentIdNumber(value: string) {
  const normalized = normalizeChinaResidentIdNumber(value)
  if (chinaResidentId18Pattern.test(normalized)) {
    if (!isValidBirthDate(normalized.slice(6, 14))) {
      return false
    }
    const checksumIndex = chinaResidentIdWeights.reduce((total, weight, index) => total + Number(normalized[index]) * weight, 0) % 11
    return normalized[17] === chinaResidentIdChecksumMap[checksumIndex]
  }
  if (chinaResidentId15Pattern.test(normalized)) {
    return isValidBirthDate(normalized.slice(6, 12), true)
  }
  return false
}

export function getChinaResidentIdValidationMessage(value: string) {
  const normalized = normalizeChinaResidentIdNumber(value)
  if (!normalized) {
    return '请输入身份证号'
  }
  if (!isValidChinaResidentIdNumber(normalized)) {
    return '身份证号格式不正确，请输入有效的中国居民身份证号码'
  }
  return null
}