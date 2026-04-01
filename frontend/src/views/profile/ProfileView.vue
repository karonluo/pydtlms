<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const savingProfile = ref(false)
const savingPassword = ref(false)

const profileForm = reactive({
  full_name: '',
  phone_number: '',
  email: '',
  theme_color: '#0f4cbd',
})

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

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

async function saveProfile() {
  savingProfile.value = true
  try {
    await authStore.saveProfile(profileForm)
    ElMessage.success('个人资料已更新')
  } finally {
    savingProfile.value = false
  }
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
  <section class="page-grid">
    <article class="section-card">
      <div class="section-card__header compact">
        <div>
          <p class="section-tag">个人资料</p>
          <h2>基础信息与界面主题</h2>
        </div>
      </div>
      <el-form label-width="100px" class="form-grid">
        <el-form-item label="用户名">
          <el-input :model-value="authStore.profile?.username" disabled />
        </el-form-item>
        <el-form-item label="角色">
          <el-input :model-value="authStore.profile?.role_name" disabled />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="profileForm.full_name" />
        </el-form-item>
        <el-form-item label="部门">
          <el-input :model-value="authStore.profile?.department_name" disabled />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="profileForm.phone_number" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="profileForm.email" />
        </el-form-item>
        <el-form-item label="主题色">
          <el-color-picker v-model="profileForm.theme_color" />
        </el-form-item>
      </el-form>
      <el-button type="primary" :loading="savingProfile" @click="saveProfile">保存个人资料</el-button>
    </article>

    <article class="section-card">
      <div class="section-card__header compact">
        <div>
          <p class="section-tag">安全设置</p>
          <h2>修改 / 重置密码</h2>
        </div>
      </div>
      <el-form label-width="120px">
        <el-form-item label="当前密码">
          <el-input v-model="passwordForm.currentPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认新密码">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <el-button type="warning" :loading="savingPassword" @click="savePassword">更新密码</el-button>
    </article>
  </section>
</template>

<style scoped>
.page-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 22px;
}

.section-card {
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 26px;
  padding: 22px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(14, 40, 88, 0.07);
}

.section-card__header.compact {
  margin-bottom: 16px;
}

.section-tag,
.section-card h2 {
  margin: 0;
}

.section-tag {
  color: #7183a0;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.section-card h2 {
  margin-top: 6px;
  color: #12284d;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 2px 18px;
}

@media (max-width: 1080px) {
  .page-grid,
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
