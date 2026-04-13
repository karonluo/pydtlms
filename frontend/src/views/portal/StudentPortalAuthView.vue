<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useRouter } from 'vue-router'

import { getPortalToken, loginPortalStudent, registerPortalStudent, resetPortalStudentPassword, setPortalToken } from '../../api/portal'

const router = useRouter()
const mode = ref<'login' | 'register' | 'reset'>('login')
const submitting = ref(false)
const agreed = ref(true)

const loginForm = reactive({
  account: '',
  password: '',
})

const registerForm = reactive({
  full_name: '',
  phone_number: '',
  email: '',
  id_number: '',
  password: '',
  confirm_password: '',
})

const resetForm = reactive({
  account: '',
  id_number: '',
  new_password: '',
  confirm_password: '',
})

const panelTitle = computed(() => {
  if (mode.value === 'register') {
    return '立即注册'
  }
  if (mode.value === 'reset') {
    return '找回密码'
  }
  return '账号登录'
})

function ensureAgreement() {
  if (!agreed.value) {
    ElMessage.warning('请先同意使用条款和隐私政策')
    return false
  }
  return true
}

async function submitLogin() {
  if (!ensureAgreement()) {
    return
  }
  submitting.value = true
  try {
    const response = await loginPortalStudent(loginForm)
    setPortalToken(response.data.access_token)
    ElMessage.success('登录成功')
    await router.replace('/portal/application')
  } catch (error) {
    const detail = axios.isAxiosError(error) ? String(error.response?.data?.detail || '登录失败') : '登录失败'
    ElMessage.error(detail)
  } finally {
    submitting.value = false
  }
}

async function submitRegister() {
  if (!ensureAgreement()) {
    return
  }
  if (registerForm.password !== registerForm.confirm_password) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  submitting.value = true
  try {
    const response = await registerPortalStudent({
      full_name: registerForm.full_name,
      phone_number: registerForm.phone_number,
      email: registerForm.email,
      id_number: registerForm.id_number,
      password: registerForm.password,
    })
    ElMessage.success(response.data.message)
    loginForm.account = registerForm.phone_number
    loginForm.password = registerForm.password
    mode.value = 'login'
  } catch (error) {
    const detail = axios.isAxiosError(error) ? String(error.response?.data?.detail || '注册失败') : '注册失败'
    ElMessage.error(detail)
  } finally {
    submitting.value = false
  }
}

async function submitReset() {
  if (!ensureAgreement()) {
    return
  }
  if (resetForm.new_password !== resetForm.confirm_password) {
    ElMessage.warning('两次输入的新密码不一致')
    return
  }
  submitting.value = true
  try {
    const response = await resetPortalStudentPassword({
      account: resetForm.account,
      id_number: resetForm.id_number,
      new_password: resetForm.new_password,
    })
    ElMessage.success(response.data.message)
    loginForm.account = resetForm.account
    loginForm.password = resetForm.new_password
    mode.value = 'login'
  } catch (error) {
    const detail = axios.isAxiosError(error) ? String(error.response?.data?.detail || '找回密码失败') : '找回密码失败'
    ElMessage.error(detail)
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  if (getPortalToken()) {
    await router.replace('/portal/application')
  }
})
</script>

<template>
  <div class="portal-auth-shell">
    <section class="auth-brand-panel">
      <div class="brand-mark">SAIL</div>
      <p class="brand-kicker">Shanghai Artificial Intelligence Laboratory</p>
      <h1>欢迎加入上海人工智能实验室</h1>
      <p class="brand-summary">
        面向博士研究生考生提供独立注册、账户登录、密码找回、招生计划选择与在线申请表填写能力。
      </p>
      <ul class="brand-points">
        <li>独立学生端入口，与管理后台完全分离</li>
        <li>登录后查看开放中的招生计划与对应招生简章</li>
        <li>在线填写个人档案、教育经历和导师团队志愿</li>
      </ul>
    </section>

    <section class="auth-card">
      <div class="auth-card__header">
        <div class="auth-tabs">
          <button type="button" :class="{ active: mode === 'login' }" @click="mode = 'login'">账号登录</button>
          <button type="button" :class="{ active: mode === 'register' }" @click="mode = 'register'">立即注册</button>
          <button type="button" :class="{ active: mode === 'reset' }" @click="mode = 'reset'">忘记密码</button>
        </div>
        <strong>{{ panelTitle }}</strong>
      </div>

      <div v-if="mode === 'login'" class="auth-form">
        <label>
          <span>账号</span>
          <input v-model="loginForm.account" placeholder="请输入手机号或邮箱" />
        </label>
        <label>
          <span>密码</span>
          <input v-model="loginForm.password" type="password" placeholder="请输入登录密码" />
        </label>
        <button class="auth-submit" type="button" :disabled="submitting" @click="submitLogin">立即登录</button>
      </div>

      <div v-else-if="mode === 'register'" class="auth-form auth-form--grid">
        <label>
          <span>姓名</span>
          <input v-model="registerForm.full_name" placeholder="请输入真实姓名" />
        </label>
        <label>
          <span>手机号</span>
          <input v-model="registerForm.phone_number" placeholder="请输入手机号" />
        </label>
        <label>
          <span>邮箱</span>
          <input v-model="registerForm.email" placeholder="请输入邮箱" />
        </label>
        <label>
          <span>身份证号</span>
          <input v-model="registerForm.id_number" placeholder="请输入身份证号" />
        </label>
        <label>
          <span>设置密码</span>
          <input v-model="registerForm.password" type="password" placeholder="请输入登录密码" />
        </label>
        <label>
          <span>确认密码</span>
          <input v-model="registerForm.confirm_password" type="password" placeholder="请再次输入密码" />
        </label>
        <button class="auth-submit auth-submit--full" type="button" :disabled="submitting" @click="submitRegister">立即注册</button>
      </div>

      <div v-else class="auth-form auth-form--grid">
        <label>
          <span>账号</span>
          <input v-model="resetForm.account" placeholder="请输入手机号或邮箱" />
        </label>
        <label>
          <span>身份证号</span>
          <input v-model="resetForm.id_number" placeholder="请输入注册身份证号" />
        </label>
        <label>
          <span>新密码</span>
          <input v-model="resetForm.new_password" type="password" placeholder="请输入新密码" />
        </label>
        <label>
          <span>确认新密码</span>
          <input v-model="resetForm.confirm_password" type="password" placeholder="请再次输入新密码" />
        </label>
        <button class="auth-submit auth-submit--full" type="button" :disabled="submitting" @click="submitReset">重置密码</button>
      </div>

      <label class="auth-agreement">
        <input v-model="agreed" type="checkbox" />
        <span>我同意并已仔细阅读使用条款和隐私政策。</span>
      </label>
    </section>
  </div>
</template>

<style scoped>
.portal-auth-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: minmax(360px, 1.05fr) minmax(360px, 520px);
  background: linear-gradient(135deg, #f3f5fb 0%, #eef1f7 45%, #f8fafc 100%);
}

.auth-brand-panel {
  padding: 56px 64px;
  color: #fff;
  background: linear-gradient(145deg, #0d1f73 0%, #2f12b8 38%, #3e2ad8 100%);
}

.brand-mark {
  width: 88px;
  height: 88px;
  display: grid;
  place-items: center;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.12);
  font-size: 26px;
  font-weight: 700;
  letter-spacing: 0.14em;
}

.brand-kicker {
  margin: 24px 0 12px;
  font-size: 12px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  opacity: 0.72;
}

.auth-brand-panel h1 {
  margin: 0;
  font-size: clamp(32px, 4vw, 48px);
  line-height: 1.1;
}

.brand-summary {
  max-width: 640px;
  margin: 20px 0 30px;
  line-height: 1.9;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.82);
}

.brand-points {
  display: grid;
  gap: 12px;
  padding: 0;
  margin: 0;
  list-style: none;
}

.brand-points li {
  padding: 16px 18px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.08);
}

.auth-card {
  align-self: center;
  margin: 32px;
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

.auth-tabs button.active {
  color: #1f2f96;
  font-weight: 700;
}

.auth-form {
  display: grid;
  gap: 16px;
}

.auth-form--grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
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

.auth-submit--full {
  grid-column: 1 / -1;
}

.auth-agreement {
  margin-top: 18px;
  grid-template-columns: 18px 1fr;
  align-items: start;
}

@media (max-width: 1080px) {
  .portal-auth-shell {
    grid-template-columns: 1fr;
  }

  .auth-brand-panel,
  .auth-card {
    margin: 0;
    border-radius: 0;
  }
}

@media (max-width: 720px) {
  .auth-brand-panel,
  .auth-card {
    padding: 24px 18px;
  }

  .auth-form--grid {
    grid-template-columns: 1fr;
  }
}
</style>