<script setup lang="ts">
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import {
  clearPortalToken,
  getPortalProfile,
  getPortalToken,
  loginPortalStudent,
  registerPortalStudent,
  resetPortalStudentPassword,
  sendPortalRegistrationEmailCode,
  setPortalToken,
} from '../../api/portal'
import { getEmailValidationMessage, getPhoneValidationMessage, normalizeEmail, normalizePhoneNumber } from '../../utils/contactValidation'
import { getChinaResidentIdValidationMessage, normalizeChinaResidentIdNumber } from '../../utils/chinaResidentId'
import { resolveRequestError, showPortalAlert } from '../../utils/portalAlerts'

const router = useRouter()
const mode = ref<'login' | 'register' | 'reset'>('login')
const submitting = ref(false)
const agreed = ref(true)
const emailCodeSending = ref(false)
const emailCodeCooldownSeconds = ref(0)
const emailCodeTarget = ref('')

const loginForm = reactive({
  account: '',
  password: '',
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

let emailCodeCountdownTimer: number | null = null

function switchMode(nextMode: 'login' | 'register' | 'reset') {
  if (submitting.value) {
    return
  }
  mode.value = nextMode
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

function clearEmailCodeCountdown() {
  if (emailCodeCountdownTimer !== null) {
    window.clearInterval(emailCodeCountdownTimer)
    emailCodeCountdownTimer = null
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

async function submitLogin() {
  if (submitting.value) {
    return
  }
  if (!ensureAgreement() || !ensureCaptcha(loginForm.captcha)) {
    return
  }
  submitting.value = true
  try {
    const response = await loginPortalStudent(loginForm)
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
        <span>我同意并已仔细阅读使用条款和隐私政策。</span>
      </label>
    </section>
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
