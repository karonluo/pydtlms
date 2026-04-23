<script setup lang="ts">
import { computed, onBeforeUnmount, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

import { useAuthStore } from '../../stores/auth'
import { getEmailValidationMessage, getPhoneValidationMessage, normalizeEmail, normalizePhoneNumber } from '../../utils/contactValidation'

const authStore = useAuthStore()
const savingProfile = ref(false)
const savingPassword = ref(false)

const profileForm = reactive({
  full_name: '',
  phone_number: '',
  email: '',
  theme_color: '#409eff',
})

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const presets = ['#409eff', '#6c7a89', '#36a3f7', '#5470c6']

const previewStyle = computed(() => ({
  background: `linear-gradient(180deg, ${profileForm.theme_color}22, ${profileForm.theme_color}11)`,
  borderColor: `${profileForm.theme_color}55`,
}))

watch(
  () => authStore.profile,
  (profile) => {
    if (!profile) {
      return
    }
    profileForm.full_name = profile.full_name
    profileForm.phone_number = profile.phone_number || ''
    profileForm.email = profile.email || ''
    profileForm.theme_color = profile.theme_color
  },
  { immediate: true },
)

watch(
  () => profileForm.theme_color,
  (color) => {
    authStore.applyThemeColor(color)
  },
)

onBeforeUnmount(() => {
  authStore.applyThemeColor(authStore.themeColor)
})

async function saveProfile() {
  const phoneValidationMessage = getPhoneValidationMessage(profileForm.phone_number)
  if (phoneValidationMessage) {
    ElMessage.warning(phoneValidationMessage)
    return
  }
  const emailValidationMessage = getEmailValidationMessage(profileForm.email)
  if (emailValidationMessage) {
    ElMessage.warning(emailValidationMessage)
    return
  }

  profileForm.phone_number = normalizePhoneNumber(profileForm.phone_number)
  profileForm.email = normalizeEmail(profileForm.email)
  savingProfile.value = true
  try {
    await authStore.saveProfile(profileForm)
    ElMessage.success('个人资料已更新')
  } finally {
    savingProfile.value = false
  }
}

function applyPreset(color: string) {
  profileForm.theme_color = color
}

async function savePassword() {
  if (!passwordForm.currentPassword || !passwordForm.newPassword) {
    ElMessage.warning('请填写完整密码信息')
    return
  }
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.warning('两次输入的新密码不一致')
    return
  }

  savingPassword.value = true
  try {
    await authStore.changePassword(passwordForm.currentPassword, passwordForm.newPassword)
    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
    ElMessage.success('密码已更新')
  } finally {
    savingPassword.value = false
  }
}
</script>

<template>
  <section class="profile-grid">
    <article class="section-card">
      <div class="section-card__header compact">
        <div>
          <p class="section-tag">工作台 / 个人空间</p>
          <h2>个人资料</h2>
          <span class="section-desc">维护显示昵称、界面主题色与常用联系方式。</span>
        </div>
      </div>

      <el-form label-width="88px" class="profile-form">
        <el-form-item label="登录账号">
          <el-input :model-value="authStore.profile?.username" disabled />
        </el-form-item>
        <el-form-item label="显示昵称">
          <el-input v-model="profileForm.full_name" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="profileForm.phone_number" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="profileForm.email" />
        </el-form-item>
        <el-form-item label="主题预设" class="profile-form__full">
          <div class="preset-row">
            <button v-for="color in presets" :key="color" class="preset-chip" type="button" :style="{ background: color }" @click="applyPreset(color)"></button>
          </div>
        </el-form-item>
        <el-form-item label="主题颜色" class="profile-form__full">
          <div class="theme-row">
            <el-color-picker v-model="profileForm.theme_color" />
            <el-input v-model="profileForm.theme_color" />
          </div>
        </el-form-item>
        <el-form-item label="界面预览" class="profile-form__full">
          <div class="preview-card" :style="previewStyle">
            <div class="preview-card__avatar">{{ authStore.initials }}</div>
            <div>
              <strong>{{ profileForm.full_name || authStore.fullName }}</strong>
              <p>{{ profileForm.phone_number || '未设置手机号' }} · {{ profileForm.email || '未设置邮箱' }}</p>
              <span>当前主题色将应用到系统顶层视觉元素。</span>
            </div>
          </div>
        </el-form-item>
      </el-form>

      <div class="action-row">
        <el-button @click="applyPreset('#409eff')">恢复默认配色</el-button>
        <el-button type="primary" :loading="savingProfile" @click="saveProfile">保存资料</el-button>
      </div>
    </article>

    <article class="section-card">
      <div class="section-card__header compact">
        <div>
          <p class="section-tag">安全设置</p>
          <h2>更新密码</h2>
        </div>
      </div>

      <el-form label-width="92px" class="security-form">
        <el-form-item label="当前密码">
          <el-input v-model="passwordForm.currentPassword" type="password" show-password placeholder="请输入当前密码" />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="passwordForm.newPassword" type="password" show-password placeholder="至少 8 位" />
        </el-form-item>
        <el-form-item label="确认新密码">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password placeholder="请再次确认新密码" />
        </el-form-item>
      </el-form>

      <div class="action-row action-row--end">
        <el-button type="primary" :loading="savingPassword" @click="savePassword">更新密码</el-button>
      </div>
    </article>
  </section>
</template>

<style scoped>
.profile-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(360px, 1fr);
  gap: 14px;
}

.section-card {
  border: 1px solid rgba(203, 223, 244, 0.94);
  border-radius: 20px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 18px 40px rgba(67, 108, 159, 0.08);
}

.section-card__header.compact {
  margin-bottom: 10px;
}

.section-tag,
.section-card h2,
.section-desc,
.preview-card p,
.preview-card span {
  margin: 0;
}

.section-tag {
  color: #8298b1;
  font-size: 11px;
}

.section-card h2 {
  margin-top: 6px;
  color: #1f3e64;
  font-size: 22px;
}

.section-desc {
  display: block;
  margin-top: 6px;
  color: #7d91ad;
  font-size: 12px;
}

.profile-form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0 12px;
}

.profile-form__full {
  grid-column: 1 / -1;
}

.preset-row,
.theme-row,
.action-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.preset-chip {
  width: 30px;
  height: 30px;
  border: 2px solid rgba(255, 255, 255, 0.92);
  border-radius: 10px;
  box-shadow: 0 8px 18px rgba(67, 108, 159, 0.18);
  cursor: pointer;
}

.theme-row :deep(.el-input) {
  flex: 1;
}

.preview-card {
  display: grid;
  grid-template-columns: 48px minmax(0, 1fr);
  gap: 12px;
  align-items: start;
  padding: 14px;
  border: 1px solid;
  border-radius: 16px;
}

.preview-card__avatar {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: linear-gradient(160deg, #c20e18, #ef4733);
  color: #fff7da;
  font-weight: 800;
}

.preview-card strong {
  color: #234264;
  font-size: 15px;
}

.preview-card p,
.preview-card span {
  font-size: 12px;
  line-height: 1.6;
}

.action-row {
  margin-top: 4px;
}

.preview-card p {
  margin-top: 8px;
  color: #6f86a7;
}

.preview-card span {
  display: block;
  margin-top: 10px;
  color: #7389a8;
  font-size: 13px;
}

.action-row {
  justify-content: space-between;
  margin-top: 18px;
}

.action-row--end {
  justify-content: end;
}

@media (max-width: 1100px) {
  .profile-grid,
  .profile-form {
    grid-template-columns: 1fr;
  }
}
</style>
