const chinaMobilePhonePattern = /^1[3-9]\d{9}$/
const emailPattern = /^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$/

export function normalizePhoneNumber(value: string) {
  return String(value || '').trim()
}

export function normalizeEmail(value: string) {
  return String(value || '').trim()
}

export function getPhoneValidationMessage(value: string, required = false, label = '手机号') {
  const normalized = normalizePhoneNumber(value)
  if (!normalized) {
    return required ? `请输入${label}` : null
  }
  if (!chinaMobilePhonePattern.test(normalized)) {
    return `${label}格式不正确，请输入有效的中国大陆手机号`
  }
  return null
}

export function getEmailValidationMessage(value: string, required = false, label = '邮箱') {
  const normalized = normalizeEmail(value)
  if (!normalized) {
    return required ? `请输入${label}` : null
  }
  if (!emailPattern.test(normalized)) {
    return `${label}格式不正确，请输入有效的邮箱地址`
  }
  return null
}