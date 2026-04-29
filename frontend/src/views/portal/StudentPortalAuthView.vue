<script setup lang="ts">
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import {
  clearPortalToken,
  getPortalProfile,
  getPortalToken,
  loginPortalStudentByEmailCode,
  loginPortalStudent,
  registerPortalStudent,
  resetPortalStudentPassword,
  sendPortalLoginEmailCode,
  sendPortalRegistrationEmailCode,
  setPortalToken,
} from '../../api/portal'
import { getEmailValidationMessage, getPhoneValidationMessage, normalizeEmail, normalizePhoneNumber } from '../../utils/contactValidation'
import { getChinaResidentIdValidationMessage, normalizeChinaResidentIdNumber } from '../../utils/chinaResidentId'
import { resolveRequestError, showPortalAlert } from '../../utils/portalAlerts'

const router = useRouter()
const mode = ref<'login' | 'register' | 'reset'>('login')
const loginMethod = ref<'password' | 'email-code'>('password')
const submitting = ref(false)
const agreed = ref(true)
const emailCodeSending = ref(false)
const emailCodeCooldownSeconds = ref(0)
const emailCodeTarget = ref('')
const loginEmailCodeSending = ref(false)
const loginEmailCodeCooldownSeconds = ref(0)
const loginEmailCodeTarget = ref('')
const termsDialogVisible = ref(false)
const termsHeadingPrimary = ref('')
const termsHeadingSecondary = ref('')
const termsBodyHtml = ref('')

const TERMS_AND_PRIVACY_CONTENT = `上海人工智能实验室招生系统隐私条款

（面向学生）

上海人工智能实验室是我国人工智能领域的新型科研机构，开展战略性、原创性、前瞻性的科学研究与技术攻关，突破人工智能的重要基础理论和关键核心技术，打造“突破型、引领型、平台型”一体化的大型综合性研究基地，支撑我国人工智能产业实现跨越式发展，目标建成国际一流的人工智能实验室，成为享誉全球的人工智能原创理论和技术的策源地。（以下简称“SHLAB”或“我们”或“上海人工智能实验室”）一贯重视对于个人信息和隐私的保护。我们将按法律法规要求，采取相应安全保护措施，尽力保护您的个人信息安全可控。您在使用我们的产品或服务时，我们将按照相关法律法zh规及本《隐私政策》（以下简称“本政策”）收集、储存、使用及对外提供您的个人信息。

本政策适用于上海人工智能实验室服务，包括上海人工智能实验室官方网站（域名为https://shlab.org.cn ）和小程序。需要特别说明的是，本政策不适用于其他第三方通过前述网页或客户端向您提供的服务。例如您通过上海人工智能实验室开放平台下载使用的第三方应用或者第三方依托上海人工智能实验室产品向您提供服务时，您向第三方提供的信息不适用本政策，请另行查阅相应的政策规定。

在您使用我们的产品或服务前，请务必仔细阅读并理解本政策。我们会在官方平台上登载本政策。当您使用我们的产品或服务时，即视为您已经阅读、理解并同意本政策及其不时更新的版本，同意我们按照本政策的约定收集和使用您的个人信息。

1. 我们收集您个人信息的内容、目的

1.1 收集内容

我们向您提供产品和服务时，可能会收集、储存和使用您的下列“个人信息”：包括但不限于您的姓名、性别、身份证信息、个人图像、邮寄地址、电子邮件地址、其他联系方式、成绩信息、教育经历、实践经历、英语语言能力、家庭情况、个人简介、个人陈述、自我评价以及其他相关您个人的隐私信息等。

1.2 收集、储存和使用目的

我们承诺在下述目的范围内收集、储存和使用您的个人信息：

• 管理服务，向您提供我们的服务，并就您使用我们服务的情况进行及时沟通；

• 支持我们产品的运作和服务的履行，回应您的咨询及请求；

• 向您提供在校、非在校服务及支持，接受您的反馈并解决反馈的问题；

• 及时向您通知我们的最新课程、服务、衍生市场推广活动等；

• 用于数据分析和研究等内部处理，以改进我们的产品、服务质量；

• 便于与您之间的沟通，及时解决您的问题；

• 经您同意的其他用途。

2. 我们如何收集您的个人信息

2.1 您向我们提供的信息

包括但不限于：您报考注册时提供的信息，您下载或使用我们或我们指定的公司开发的应用时提供的信息、您访问我们的官网、参与我们组织的活动，或者使用我们提供的其他网上服务时提供的信息、您关注我们的社交媒体时提供的信息、您在校期间的相关个人信息等。

2.2 我们在提供产品或服务时，主动收集的信息

包括但不限于:

您的成绩、教育经历、实践经历、英语语言能力、家庭情况等信息。

2.3 Cookie

我们会通过 Cookies 和其他追踪技术了解您使用我们网站的情况。通过 Cookies 收集的信息属于不能单独使用的个人信息，您理解并同意我们将会把通过 Cookies 收集的信息与您的其他信息结合使用。大部分网页浏览器会自动打开 Cookies，您可以随时调整您的浏览器设置，选择关闭Cookies。然而，Cookies 能让您享受我们更优质、更个性化的服务，如果您关闭了 Cookies，可能无法完全体验我们网站上提供的所有服务，所以我们建议您将其设置为打开状态。

2.4 请注意，您向我们提供的或我们收集的您的个人信息中可能包含您的敏感个人信息，如生物识别、宗教信仰、特定身份、医疗健康、金融账户、行踪轨迹等，请您谨慎并留意敏感个人信息，您同意我们可以按本政策所述的目的和方式来处理您的敏感个人信息。

3. 我们如何共享、转让、公开披露您的个人信息

我们尊重您的个人隐私并遵守相关的法律和法规，我们承诺严格保密所收集的您的个人信息，并且不会将您的个人信息非法出售给他人。

3.1 共享

3.1.1 为促进合作，推出优质及更新的服务，我们可能会向第三方合作伙伴提供您必要的个人信息。我们的授权伙伴无权将共享的个人信息用于任何其他用途。

目前，我们的授权合作伙伴包括以下几大类型：

我们聘请的第三方服务提供者（如供应商、服务外包商等）为我们的客户提供相关服务。

3.1.2 根据法律法规规定，或按政府主管部门的强制性要求，对外共享您的个人信息，无需事先征得您的授权同意。

3.1.3只有在获得您的明确同意后,我们才会向前述 3.1.1、3.1.2 提及的主体之外的其他方共享或提供的个人信息。

3.2 转让

我们不会将您的个人信息转让给任何公司、组织和个人，但以下情况除外：

3.2.1 获得您的明确同意后；

3.2.2 在涉及合并、收购或破产清算时，如涉及到个人信息转让，我们会在要求新的持有您个人信息的公司、组织继续受本政策的约束，否则我们将要求该公司、组织重新向您征求授权同意。

3.3 公开披露

我们仅会在以下情况下，公开披露您的个人信息：

3.3.1 获得您的明确同意后；

3.3.2 基于法律的披露：在法律、法律程序、诉讼或政府主管部门强制性要求的情况下，我们会公开披露您的个人信息。

3.4 我们会在共享、转让、公开披露前，确认第三方的管理体制及传输风险。

4. 我们如何保护您的个人信息

4.1 我们使用符合业界标准的、合理可行的安全防护措施保护您提供的个人信息，防止数据被未经授权访问、公开披露、使用、修改、损坏或丢失。

4.2 我们会采取合理可行的措施，确保不会收集无关的个人信息。

4.3 除法律法规另有规定外，我们只会在达成本政策所述目的所需的最短期限内保存您的个人信息。

4.4 我们将定期更新本政策，并公开安全风险等报告的有关内容。您可通过以我们的官方网站进行查看。

4.5 在不幸发生个人信息安全事件后,我们将及时向您告知,难以逐一告知个人信息主体时, 我们会采取合理、有效的方式发布公告。同时,我们还将按照监管部门要求,主动上报个人信息安全事件的处置情况。

5. 您对个人信息享有的权利

您可以选择不提供您的个人信息，但我们将可能因此无法为您提供我们的产品或服务，也可能无法回应您在使用我们的产品或服务时所遇到的问题。对于您可能因此遭受的损失，我们将不承担责任。

如果您选择同意提供给我们您的个人信息，我们将按照相关法律法规，保障您对自己的个人信息行使以下权利：

5.1 访问您的个人信息：

您有权访问或编辑您账户中的个人信息资料、更改您的密码、添加安全信息或关闭您的账户等。

5.2 更新您的个人信息：

当您发现我们收集、储存、使用的您的个人信息有错漏时，您有权要求我们做出更正。

5.3 删除您的个人信息

您可以向我们提出删除个人信息的请求。若我们决定响应您的删除请求，我们还将同时通知从我们获得您的个人信息的第三方，要求其及时删除，除法律法规另有规定，或其已获得您的独立授权。

当您从我们的产品或服务中删除个人信息后，我们可能不会立即从备份系统中删除相应的信息，但会在备份更新时删除这些信息。

若部分信息因需留存备查等不能完全删除时，我们将对此部分信息进行匿名化处理，使之不能再特定指向到个人。

5.4 更改您授权同意的范围

您可以改变您授权我们收集、储存、使用个人信息的范围或撤回您的授权。

当您撤回授权同意后，我们将不再处理相应的个人信息。但您撤回授权同意的决定，不会影响此前基于您的授权而开展的个人信息处理活动。

5.5 响应您的上述请求

您可以通过以下途径向我们提交上述权利请求：拨打电话。为保障安全,您可能需要以书面方式提交上述请求，同时我们可能会先要求验证您的身份，然后再处理您的请求。对于您合理的请求，我们原则上不收取费用，但对多次重复、超出合理限度的请求，我们将视情收取一定成本费用。

6. 本政策如何更新

我们可以修改本政策，并会在上海人工智能实验室相关网站平台上发布对本政策做出的任何变更。如有对您的个人信息的收集、储存、使用产生重要影响的重大变更（例如，对应个人信息的联络方式及投诉渠道发生变化时），我们将以明示的方式通知您，说明具体变更内容等。

7. 如果您对本政策有任何疑问、意见或建议，与我们联系。`

const loginForm = reactive({
  account: '',
  password: '',
  captcha: '',
})

const loginEmailCodeForm = reactive({
  email: '',
  email_verification_code: '',
  captcha: '',
})

const registerForm = reactive({
  full_name: '',
  phone_number: '',
  email: '',
  id_number: '',
  password: '',
  confirm_password: '',
  email_verification_code: '',
  captcha: '',
})

const resetForm = reactive({
  account: '',
  id_number: '',
  new_password: '',
  confirm_password: '',
  captcha: '',
})

const captchaSeed = '23456789'
const captchaCode = ref('')
const captchaImage = ref('')

const panelTitle = computed(() => {
  if (mode.value === 'register') {
    return '立即注册'
  }
  if (mode.value === 'reset') {
    return '找回密码'
  }
  return '账号登录'
})

const registerButtonText = computed(() => (submitting.value ? '注册中...' : '立即注册'))
const loginButtonText = computed(() => (submitting.value ? '登录中...' : '立即登录'))
const resetButtonText = computed(() => (submitting.value ? '提交中...' : '重置密码'))
const emailCodeButtonText = computed(() => {
  if (emailCodeSending.value) {
    return '发送中...'
  }
  if (emailCodeCooldownSeconds.value > 0) {
    return `${emailCodeCooldownSeconds.value}s后重试`
  }
  return '获取验证码'
})

const loginEmailCodeButtonText = computed(() => {
  if (loginEmailCodeSending.value) {
    return '发送中...'
  }
  if (loginEmailCodeCooldownSeconds.value > 0) {
    return `${loginEmailCodeCooldownSeconds.value}s后重试`
  }
  return '获取验证码'
})

let emailCodeCountdownTimer: number | null = null
let loginEmailCodeCountdownTimer: number | null = null

function switchMode(nextMode: 'login' | 'register' | 'reset') {
  if (submitting.value) {
    return
  }
  mode.value = nextMode
  if (nextMode === 'login') {
    loginMethod.value = 'password'
  }
  refreshCaptcha()
}

function createCaptcha() {
  return Array.from({ length: 5 }, () => captchaSeed[Math.floor(Math.random() * captchaSeed.length)]).join('')
}

function createCaptchaImage(code: string) {
  const palette = ['#1c4e92', '#2b63b8', '#4c6fb2', '#32527d', '#596d8f']
  const linePalette = ['rgba(36, 98, 172, 0.35)', 'rgba(64, 143, 214, 0.3)', 'rgba(88, 108, 156, 0.28)']
  const noise = Array.from({ length: 28 }, () => {
    const cx = Math.floor(Math.random() * 150) + 5
    const cy = Math.floor(Math.random() * 42) + 6
    const r = (Math.random() * 1.6 + 0.6).toFixed(2)
    const fill = Math.random() > 0.5 ? '#8cb4ea' : '#d6e4fb'
    const opacity = (Math.random() * 0.5 + 0.2).toFixed(2)
    return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${fill}" opacity="${opacity}" />`
  }).join('')

  const lines = Array.from({ length: 4 }, (_, index) => {
    const y1 = Math.floor(Math.random() * 48) + 4
    const y2 = Math.floor(Math.random() * 48) + 4
    const midX = 30 + index * 28 + Math.floor(Math.random() * 16)
    const midY = Math.floor(Math.random() * 48) + 4
    const stroke = linePalette[index % linePalette.length]
    return `<path d="M 0 ${y1} Q ${midX} ${midY}, 160 ${y2}" stroke="${stroke}" stroke-width="1.4" fill="none" />`
  }).join('')

  const chars = code.split('').map((char, index) => {
    const x = 18 + index * 27
    const y = 34 + Math.floor(Math.random() * 8)
    const rotate = Math.floor(Math.random() * 26) - 13
    const fill = palette[index % palette.length]
    return `<text x="${x}" y="${y}" fill="${fill}" font-size="24" font-weight="700" font-family="Bahnschrift, Aptos Display, Microsoft YaHei UI, sans-serif" transform="rotate(${rotate} ${x} ${y})">${char}</text>`
  }).join('')

  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="160" height="54" viewBox="0 0 160 54">
      <defs>
        <linearGradient id="captchaBg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#f6faff" />
          <stop offset="100%" stop-color="#e1efff" />
        </linearGradient>
      </defs>
      <rect x="0.5" y="0.5" width="159" height="53" rx="15" fill="url(#captchaBg)" stroke="#bfd2ee" />
      ${noise}
      ${lines}
      ${chars}
    </svg>
  `.trim()

  return `url("data:image/svg+xml;utf8,${encodeURIComponent(svg)}")`
}

function refreshCaptcha() {
  captchaCode.value = createCaptcha()
  captchaImage.value = createCaptchaImage(captchaCode.value)
  loginForm.captcha = ''
  loginEmailCodeForm.captcha = ''
  registerForm.captcha = ''
  resetForm.captcha = ''
}

function ensureCaptcha(input: string) {
  if (!input.trim()) {
    void showPortalAlert('请先填写随机验证码', '提示', 'warning')
    return false
  }
  if (input.trim().toUpperCase() !== captchaCode.value) {
    void showPortalAlert('随机验证码不正确，请重新输入', '提示', 'warning')
    refreshCaptcha()
    return false
  }
  return true
}

function ensureAgreement() {
  if (!agreed.value) {
    void showPortalAlert('请先同意使用条款和隐私政策', '提示', 'warning')
    return false
  }
  return true
}

function escapeHtml(value: string) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function formatTermsMarkdown(content: string) {
  const normalized = content.replace(/\r\n/g, '\n')
  const lines = normalized.split('\n')
  const nonEmptyLines = lines.map((line, index) => ({ line: line.trim(), index })).filter((item) => item.line)

  termsHeadingPrimary.value = nonEmptyLines[0]?.line ?? '使用条款和隐私政策'
  termsHeadingSecondary.value = nonEmptyLines[1]?.line ?? ''

  const bodyStartIndex = nonEmptyLines[1]?.index ?? nonEmptyLines[0]?.index ?? -1
  const bodySource = lines.slice(bodyStartIndex + 1)
  const paragraphs = bodySource.join('\n').split(/\n\s*\n/)

  termsBodyHtml.value = paragraphs
    .map((paragraph) => paragraph.split('\n').map((line) => line.trim()).filter(Boolean))
    .filter((paragraphLines) => paragraphLines.length > 0)
    .map((paragraphLines) => {
      const isBulletList = paragraphLines.every((line) => line.startsWith('•'))
      if (isBulletList) {
        const items = paragraphLines
          .map((line) => line.replace(/^•\s*/, '').trim())
          .filter(Boolean)
          .map((line) => `<li>${escapeHtml(line)}</li>`)
          .join('')
        return `<ul class="terms-dialog__list">${items}</ul>`
      }

      return `<p class="terms-dialog__paragraph">${paragraphLines.map((line) => escapeHtml(line)).join('<br />')}</p>`
    })
    .join('')
}

function openTermsDialog() {
  formatTermsMarkdown(TERMS_AND_PRIVACY_CONTENT)
  termsDialogVisible.value = true
}

function clearEmailCodeCountdown() {
  if (emailCodeCountdownTimer !== null) {
    window.clearInterval(emailCodeCountdownTimer)
    emailCodeCountdownTimer = null
  }
}

function clearLoginEmailCodeCountdown() {
  if (loginEmailCodeCountdownTimer !== null) {
    window.clearInterval(loginEmailCodeCountdownTimer)
    loginEmailCodeCountdownTimer = null
  }
}

function startEmailCodeCountdown(seconds: number) {
  clearEmailCodeCountdown()
  emailCodeCooldownSeconds.value = Math.max(0, Math.floor(seconds))
  if (emailCodeCooldownSeconds.value <= 0) {
    return
  }
  emailCodeCountdownTimer = window.setInterval(() => {
    if (emailCodeCooldownSeconds.value <= 1) {
      emailCodeCooldownSeconds.value = 0
      clearEmailCodeCountdown()
      return
    }
    emailCodeCooldownSeconds.value -= 1
  }, 1000)
}

function startLoginEmailCodeCountdown(seconds: number) {
  clearLoginEmailCodeCountdown()
  loginEmailCodeCooldownSeconds.value = Math.max(0, Math.floor(seconds))
  if (loginEmailCodeCooldownSeconds.value <= 0) {
    return
  }
  loginEmailCodeCountdownTimer = window.setInterval(() => {
    if (loginEmailCodeCooldownSeconds.value <= 1) {
      loginEmailCodeCooldownSeconds.value = 0
      clearLoginEmailCodeCountdown()
      return
    }
    loginEmailCodeCooldownSeconds.value -= 1
  }, 1000)
}

async function sendRegisterEmailCode() {
  if (submitting.value || emailCodeSending.value || emailCodeCooldownSeconds.value > 0) {
    return
  }
  const emailValidationMessage = getEmailValidationMessage(registerForm.email, true)
  if (emailValidationMessage) {
    await showPortalAlert(emailValidationMessage, '提示', 'warning')
    return
  }
  emailCodeSending.value = true
  try {
    const normalizedEmail = normalizeEmail(registerForm.email)
    const response = await sendPortalRegistrationEmailCode({ email: normalizedEmail })
    emailCodeTarget.value = normalizedEmail
    startEmailCodeCountdown(response.data.cooldown_seconds)
    await showPortalAlert(response.data.message, '发送成功', 'success')
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '邮件验证码发送失败'), '发送失败', 'error')
  } finally {
    emailCodeSending.value = false
  }
}

async function sendLoginEmailCode() {
  if (submitting.value || loginEmailCodeSending.value || loginEmailCodeCooldownSeconds.value > 0) {
    return
  }
  const emailValidationMessage = getEmailValidationMessage(loginEmailCodeForm.email, true)
  if (emailValidationMessage) {
    await showPortalAlert(emailValidationMessage, '提示', 'warning')
    return
  }
  loginEmailCodeSending.value = true
  try {
    const normalizedEmail = normalizeEmail(loginEmailCodeForm.email)
    const response = await sendPortalLoginEmailCode({ email: normalizedEmail })
    loginEmailCodeTarget.value = normalizedEmail
    startLoginEmailCodeCountdown(response.data.cooldown_seconds)
    await showPortalAlert(response.data.message, '发送成功', 'success')
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '登录验证码发送失败'), '发送失败', 'error')
  } finally {
    loginEmailCodeSending.value = false
  }
}

async function submitLogin() {
  if (submitting.value) {
    return
  }
  if (!ensureAgreement()) {
    return
  }
  submitting.value = true
  try {
    let response
    if (loginMethod.value === 'password') {
      if (!ensureCaptcha(loginForm.captcha)) {
        submitting.value = false
        return
      }
      response = await loginPortalStudent(loginForm)
    } else {
      const loginEmailValidationMessage = getEmailValidationMessage(loginEmailCodeForm.email, true)
      if (loginEmailValidationMessage) {
        submitting.value = false
        await showPortalAlert(loginEmailValidationMessage, '提示', 'warning')
        return
      }
      const normalizedLoginEmail = normalizeEmail(loginEmailCodeForm.email)
      if (!loginEmailCodeForm.email_verification_code.trim()) {
        submitting.value = false
        await showPortalAlert('请先填写邮件验证码', '提示', 'warning')
        return
      }
      if (!loginEmailCodeTarget.value || loginEmailCodeTarget.value !== normalizedLoginEmail) {
        submitting.value = false
        await showPortalAlert('请先获取当前邮箱对应的登录验证码', '提示', 'warning')
        return
      }
      if (!ensureCaptcha(loginEmailCodeForm.captcha)) {
        submitting.value = false
        return
      }
      response = await loginPortalStudentByEmailCode({
        email: normalizedLoginEmail,
        email_verification_code: loginEmailCodeForm.email_verification_code.trim(),
      })
      loginEmailCodeForm.email_verification_code = ''
      loginEmailCodeTarget.value = ''
      clearLoginEmailCodeCountdown()
      loginEmailCodeCooldownSeconds.value = 0
    }
    setPortalToken(response.data.access_token)
    await router.replace('/portal/home')
  } catch (error) {
    refreshCaptcha()
    await showPortalAlert(resolveRequestError(error, '登录失败'), '登录失败', 'error')
  } finally {
    submitting.value = false
  }
}

async function submitRegister() {
  if (submitting.value) {
    return
  }
  if (!ensureAgreement()) {
    return
  }
  if (registerForm.password !== registerForm.confirm_password) {
    await showPortalAlert('两次输入的密码不一致', '提示', 'warning')
    return
  }
  const registerPhoneValidationMessage = getPhoneValidationMessage(registerForm.phone_number, true)
  if (registerPhoneValidationMessage) {
    await showPortalAlert(registerPhoneValidationMessage, '提示', 'warning')
    return
  }
  const registerEmailValidationMessage = getEmailValidationMessage(registerForm.email, true)
  if (registerEmailValidationMessage) {
    await showPortalAlert(registerEmailValidationMessage, '提示', 'warning')
    return
  }
  const normalizedRegisterEmail = normalizeEmail(registerForm.email)
  if (!registerForm.email_verification_code.trim()) {
    await showPortalAlert('请先填写邮件验证码', '提示', 'warning')
    return
  }
  if (!emailCodeTarget.value || emailCodeTarget.value !== normalizedRegisterEmail) {
    await showPortalAlert('请先获取当前邮箱对应的邮件验证码', '提示', 'warning')
    return
  }
  const registerIdValidationMessage = getChinaResidentIdValidationMessage(registerForm.id_number)
  if (registerIdValidationMessage) {
    await showPortalAlert(registerIdValidationMessage, '提示', 'warning')
    return
  }
  if (!ensureCaptcha(registerForm.captcha)) {
    return
  }
  submitting.value = true
  try {
    const response = await registerPortalStudent({
      full_name: registerForm.full_name,
      phone_number: normalizePhoneNumber(registerForm.phone_number),
      email: normalizedRegisterEmail,
      id_number: normalizeChinaResidentIdNumber(registerForm.id_number),
      password: registerForm.password,
      email_verification_code: registerForm.email_verification_code.trim(),
    })
    loginForm.account = registerForm.phone_number
    loginForm.password = registerForm.password
    registerForm.email_verification_code = ''
    emailCodeTarget.value = ''
    clearEmailCodeCountdown()
    emailCodeCooldownSeconds.value = 0
    await showPortalAlert(response.data.message, '完成注册', 'success')
    mode.value = 'login'
    refreshCaptcha()
  } catch (error) {
    refreshCaptcha()
    await showPortalAlert(resolveRequestError(error, '注册失败'), '注册失败', 'error')
  } finally {
    submitting.value = false
  }
}

async function submitReset() {
  if (submitting.value) {
    return
  }
  if (!ensureAgreement()) {
    return
  }
  if (resetForm.new_password !== resetForm.confirm_password) {
    await showPortalAlert('两次输入的新密码不一致', '提示', 'warning')
    return
  }
  const resetIdValidationMessage = getChinaResidentIdValidationMessage(resetForm.id_number)
  if (resetIdValidationMessage) {
    await showPortalAlert(resetIdValidationMessage, '提示', 'warning')
    return
  }
  if (!ensureCaptcha(resetForm.captcha)) {
    return
  }
  submitting.value = true
  try {
    const response = await resetPortalStudentPassword({
      account: resetForm.account,
      id_number: normalizeChinaResidentIdNumber(resetForm.id_number),
      new_password: resetForm.new_password,
    })
    await showPortalAlert(response.data.message, '操作成功', 'success')
    loginForm.account = resetForm.account
    loginForm.password = resetForm.new_password
    mode.value = 'login'
    refreshCaptcha()
  } catch (error) {
    refreshCaptcha()
    await showPortalAlert(resolveRequestError(error, '找回密码失败'), '找回密码失败', 'error')
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  refreshCaptcha()
  if (getPortalToken()) {
    try {
      await getPortalProfile()
      await router.replace('/portal/home')
    } catch {
      clearPortalToken()
    }
  }
})

onUnmounted(() => {
  clearEmailCodeCountdown()
  clearLoginEmailCodeCountdown()
})
</script>

<template>
  <div class="portal-auth-shell">
    <section class="portal-auth-copy" aria-label="门户欢迎说明">
      <p class="portal-auth-copy__eyebrow">同学你好，</p>
      <h1 class="portal-auth-copy__title">欢迎加入上海人工智能实验室</h1>
      <p class="portal-auth-copy__description">
        上海人工智能实验室自2022年启动博士生联合培养项目以来，已与国内十余所顶尖高校建立深度合作关系，致力于在通用人工智能（AGI）及相关前沿领域培养高水平科研人才。<br />
      </p>
    </section>
    <section class="auth-card">
      <div class="auth-card__header">
        <div class="auth-tabs">
          <button type="button" :class="{ active: mode === 'login' }" :disabled="submitting"
            @click="switchMode('login')">账号登录</button>
          <button type="button" :class="{ active: mode === 'register' }" :disabled="submitting"
            @click="switchMode('register')">立即注册</button>
          <button type="button" :class="{ active: mode === 'reset' }" :disabled="submitting"
            @click="switchMode('reset')">忘记密码</button>
        </div>
        <strong>{{ panelTitle }}</strong>
      </div>

      <div v-if="mode === 'login'" class="auth-form">
        <div class="login-method-tabs">
          <button type="button" :class="{ active: loginMethod === 'password' }" :disabled="submitting" @click="loginMethod = 'password'">账号登录</button>
          <button type="button" :class="{ active: loginMethod === 'email-code' }" :disabled="submitting" @click="loginMethod = 'email-code'">验证码登录（通过邮件）</button>
        </div>
        <template v-if="loginMethod === 'password'">
          <label>
            <span>账号</span>
            <input v-model="loginForm.account" :disabled="submitting" placeholder="请输入手机号或邮箱" />
          </label>
          <label>
            <span>密码</span>
            <input v-model="loginForm.password" :disabled="submitting" type="password" placeholder="请输入登录密码" />
          </label>
          <label>
            <span>随机验证码</span>
            <div class="captcha-row">
              <input v-model="loginForm.captcha" :disabled="submitting" placeholder="请输入右侧验证码" />
              <button type="button" class="captcha-chip" :style="{ backgroundImage: captchaImage }" :disabled="submitting"
                @click="refreshCaptcha">
                <span class="captcha-chip__sr">点击刷新验证码，当前验证码 {{ captchaCode }}</span>
              </button>
            </div>
          </label>
        </template>
        <template v-else>
          <label>
            <span>邮箱</span>
            <div class="inline-action-row">
              <input v-model="loginEmailCodeForm.email" :disabled="submitting || loginEmailCodeSending" placeholder="请输入注册邮箱" />
              <button type="button" class="inline-action-button" :disabled="submitting || loginEmailCodeSending || loginEmailCodeCooldownSeconds > 0" @click="sendLoginEmailCode">
                {{ loginEmailCodeButtonText }}
              </button>
            </div>
          </label>
          <label>
            <span>邮件验证码</span>
            <input v-model="loginEmailCodeForm.email_verification_code" :disabled="submitting" maxlength="6" placeholder="请输入邮件验证码" />
          </label>
          <label>
            <span>随机验证码</span>
            <div class="captcha-row">
              <input v-model="loginEmailCodeForm.captcha" :disabled="submitting" placeholder="请输入右侧验证码" />
              <button type="button" class="captcha-chip" :style="{ backgroundImage: captchaImage }" :disabled="submitting"
                @click="refreshCaptcha">
                <span class="captcha-chip__sr">点击刷新验证码，当前验证码 {{ captchaCode }}</span>
              </button>
            </div>
          </label>
        </template>
        <button class="auth-submit" type="button" :disabled="submitting" @click="submitLogin">{{ loginButtonText
          }}</button>
      </div>

      <div v-else-if="mode === 'register'" class="auth-form auth-form--grid auth-form--register">
        <label>
          <span>姓名</span>
          <input v-model="registerForm.full_name" :disabled="submitting" placeholder="请输入真实姓名" />
        </label>
        <label>
          <span>身份证号</span>
          <input v-model="registerForm.id_number" :disabled="submitting" placeholder="请输入身份证号" />
        </label>
        <label>
          <span>设置密码</span>
          <input v-model="registerForm.password" :disabled="submitting" type="password" placeholder="请输入登录密码" />
        </label>
        <label>
          <span>确认密码</span>
          <input v-model="registerForm.confirm_password" :disabled="submitting" type="password" placeholder="请再次输入密码" />
        </label>
        <label class="auth-form__full">
          <span>邮箱</span>
          <div class="inline-action-row">
            <input v-model="registerForm.email" :disabled="submitting || emailCodeSending" placeholder="请输入邮箱" />
            <button type="button" class="inline-action-button" :disabled="submitting || emailCodeSending || emailCodeCooldownSeconds > 0" @click="sendRegisterEmailCode">
              {{ emailCodeButtonText }}
            </button>
          </div>
        </label>
        <label class="auth-form__full">
          <span>邮件验证码</span>
          <input v-model="registerForm.email_verification_code" :disabled="submitting" maxlength="6" placeholder="请输入邮件验证码" />
        </label>
        <label class="auth-form__full">
          <span>手机号</span>
          <input v-model="registerForm.phone_number" :disabled="submitting" placeholder="请输入手机号" />
        </label>
        <label class="auth-form__full">
          <span>随机验证码</span>
          <div class="captcha-row">
            <input v-model="registerForm.captcha" :disabled="submitting" placeholder="请输入右侧验证码" />
            <button type="button" class="captcha-chip" :style="{ backgroundImage: captchaImage }" :disabled="submitting"
              @click="refreshCaptcha">
              <span class="captcha-chip__sr">点击刷新验证码，当前验证码 {{ captchaCode }}</span>
            </button>
          </div>
        </label>
        <button class="auth-submit auth-submit--full" type="button" :disabled="submitting" @click="submitRegister">{{
          registerButtonText }}</button>
      </div>

      <div v-else class="auth-form auth-form--grid">
        <label>
          <span>账号</span>
          <input v-model="resetForm.account" :disabled="submitting" placeholder="请输入手机号或邮箱" />
        </label>
        <label>
          <span>身份证号</span>
          <input v-model="resetForm.id_number" :disabled="submitting" placeholder="请输入注册身份证号" />
        </label>
        <label>
          <span>新密码</span>
          <input v-model="resetForm.new_password" :disabled="submitting" type="password" placeholder="请输入新密码" />
        </label>
        <label>
          <span>确认新密码</span>
          <input v-model="resetForm.confirm_password" :disabled="submitting" type="password" placeholder="请再次输入新密码" />
        </label>
        <label class="auth-form__full">
          <span>随机验证码</span>
          <div class="captcha-row">
            <input v-model="resetForm.captcha" :disabled="submitting" placeholder="请输入右侧验证码" />
            <button type="button" class="captcha-chip" :style="{ backgroundImage: captchaImage }" :disabled="submitting"
              @click="refreshCaptcha">
              <span class="captcha-chip__sr">点击刷新验证码，当前验证码 {{ captchaCode }}</span>
            </button>
          </div>
        </label>
        <button class="auth-submit auth-submit--full" type="button" :disabled="submitting" @click="submitReset">{{
          resetButtonText }}</button>
      </div>

      <label class="auth-agreement">
        <input v-model="agreed" :disabled="submitting" type="checkbox" />
        <span class="auth-agreement__text">
          我同意并已仔细阅读
          <button type="button" class="auth-agreement__link" :disabled="submitting" @click.prevent="openTermsDialog">使用条款和隐私政策</button>
          。
        </span>
      </label>
    </section>

    <el-dialog v-model="termsDialogVisible" title="使用条款和隐私政策" width="880px" class="terms-dialog">
      <div class="terms-dialog__content">
        <div class="terms-dialog__heading">
          <p class="terms-dialog__heading-line">{{ termsHeadingPrimary }}</p>
          <p v-if="termsHeadingSecondary" class="terms-dialog__heading-line">{{ termsHeadingSecondary }}</p>
        </div>
        <div class="terms-dialog__body" v-html="termsBodyHtml"></div>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
.portal-auth-shell {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 48px;
  padding: 32px 160px 32px 96px;
  background: url('/images/login_background.png') center center / cover no-repeat;
}

.portal-auth-copy {
  max-width: 680px;
  margin-top: 248px;
  color: #1f6fd7;
}

.portal-auth-copy__eyebrow {
  margin: 0 0 16px;
  font-size: clamp(26px, 2.7vw, 38px);
  line-height: 1.18;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.portal-auth-copy__title {
  margin: 0;
  font-size: clamp(26px, 2.7vw, 38px);
  line-height: 1.24;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.portal-auth-copy__description {
  margin: 30px 0 0;
  color: #67707d;
  font-size: clamp(14px, 0.98vw, 17px);
  line-height: 1.74;
  font-weight: 400;
}

.auth-card {
  width: min(100%, 520px);
  padding: 34px 32px;
  border-radius: 30px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 30px 80px rgba(37, 51, 92, 0.18);
}

.auth-card__header {
  display: grid;
  gap: 18px;
  margin-bottom: 28px;
}

.auth-tabs {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.auth-tabs button {
  border: none;
  background: transparent;
  color: #6a7392;
  font-size: 14px;
  cursor: pointer;
}

.auth-tabs button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.auth-tabs button.active {
  color: #1f2f96;
  font-weight: 700;
}

.auth-form {
  display: grid;
  gap: 13px;
}

.login-method-tabs {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.login-method-tabs button {
  min-height: 38px;
  padding: 0 14px;
  border: 1px solid #d8def0;
  border-radius: 999px;
  background: #f6f8ff;
  color: #5f6d90;
  font-size: 13px;
  cursor: pointer;
}

.login-method-tabs button.active {
  border-color: #2b58d6;
  background: rgba(43, 88, 214, 0.1);
  color: #1f2f96;
  font-weight: 700;
}

.login-method-tabs button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.auth-form--grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.auth-form--register {
  align-items: start;
}

.auth-form__full,
.auth-submit--full {
  grid-column: 1 / -1;
}

.auth-form label,
.auth-agreement {
  display: grid;
  gap: 8px;
}

.auth-form span,
.auth-agreement span {
  color: #46506f;
  font-size: 13px;
}

.auth-form input {
  width: 100%;
  min-height: 48px;
  padding: 12px 14px;
  border-radius: 14px;
  border: 1px solid #d8def0;
  background: #f8faff;
}

.auth-form input:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.inline-action-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 120px;
  gap: 10px;
  align-items: center;
}

.inline-action-button {
  min-height: 48px;
  border: 1px solid #cbd7f0;
  border-radius: 14px;
  background: #eef4ff;
  color: #2b58d6;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.inline-action-button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.captcha-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 160px;
  gap: 10px;
  align-items: center;
}

.captcha-chip {
  position: relative;
  min-height: 54px;
  border: 1px dashed rgba(52, 91, 149, 0.24);
  border-radius: 16px;
  background-color: #edf5ff;
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  cursor: pointer;
  overflow: hidden;
}

.captcha-chip:hover {
  border-color: rgba(52, 91, 149, 0.46);
}

.captcha-chip__sr {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.auth-submit {
  min-height: 48px;
  border: none;
  border-radius: 16px;
  background: linear-gradient(135deg, #2b58d6, #193ca8);
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
}

.auth-submit:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.auth-agreement {
  margin-top: 18px;
  grid-template-columns: 18px 1fr;
  align-items: start;
}

.auth-agreement__text {
  display: inline;
  line-height: 1.7;
}

.auth-agreement__link {
  display: inline;
  padding: 0;
  border: none;
  background: transparent;
  color: #1f58d6;
  font-size: 13px;
  text-decoration: underline;
  cursor: pointer;
}

.auth-agreement__link:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

:deep(.terms-dialog .el-dialog) {
  border-radius: 24px;
}

:deep(.terms-dialog .el-dialog__body) {
  padding-top: 8px;
}

.terms-dialog__content {
  max-height: min(70vh, 760px);
  overflow: auto;
  padding-right: 8px;
}

.terms-dialog__heading {
  display: grid;
  gap: 4px;
  margin-bottom: 20px;
}

.terms-dialog__heading-line {
  margin: 0;
  text-align: center;
  color: #173459;
  font-size: 20px;
  font-weight: 700;
  line-height: 1.5;
}

.terms-dialog__body {
  color: #455a78;
  font-size: 14px;
  line-height: 1.9;
}

.terms-dialog__paragraph {
  margin: 0 0 14px;
}

.terms-dialog__list {
  margin: 0 0 14px 0;
  padding-left: 20px;
}

.terms-dialog__list li {
  margin-bottom: 8px;
}

@media (max-width: 1080px) {
  .portal-auth-shell {
    padding: 24px;
  }

  .portal-auth-copy {
    margin-top: 0;
    max-width: 560px;
  }

  .auth-card {
    border-radius: 0;
  }
}

@media (max-width: 720px) {
  .portal-auth-shell {
    justify-content: center;
    flex-direction: column;
    gap: 24px;
    padding: 20px 16px;
  }

  .portal-auth-copy {
    max-width: none;
    margin-top: 0;
  }

  .portal-auth-copy__description {
    margin-top: 20px;
    line-height: 1.72;
  }

  .auth-card {
    padding: 24px 18px;
    border-radius: 28px;
  }

  .auth-form--grid,
  .inline-action-row,
  .captcha-row {
    grid-template-columns: 1fr;
  }
}
</style>
