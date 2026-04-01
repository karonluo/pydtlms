<script setup lang="ts">
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const loading = ref(false)

const form = reactive({
  username: 'admin',
  password: 'Admin@123456',
})

async function submit() {
  loading.value = true
  try {
    await authStore.login(form.username, form.password)
    ElMessage.success('登录成功')
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/dashboard'
    router.push(redirect)
  } catch {
    ElMessage.error(authStore.sessionError || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="login-page">
    <article class="login-card">
      <p class="login-tag">博士生生命周期管理系统</p>
      <h1>系统登录</h1>
      <span class="login-tip">默认演示账号已预置，可直接进入完整业务系统。</span>

      <el-form label-position="top" class="login-form">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password placeholder="请输入密码" />
        </el-form-item>
        <el-button type="primary" size="large" class="login-button" :loading="loading" @click="submit">进入系统</el-button>
      </el-form>

      <div class="account-panel">
        <strong>演示账号</strong>
        <p>平台管理员：admin / Admin@123456</p>
        <p>导师账号：mentor.demo / Mentor@123456</p>
      </div>
    </article>
  </section>
</template>

<style scoped>
.login-page {
  display: grid;
  place-items: center;
  min-height: 100vh;
  padding: 24px;
  background:
    radial-gradient(circle at top left, rgba(15, 76, 189, 0.22), transparent 30%),
    linear-gradient(160deg, #f4f8ff 0%, #e8f0fb 55%, #f7fbff 100%);
}

.login-card {
  width: min(520px, 100%);
  padding: 34px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(18, 50, 95, 0.08);
  box-shadow: 0 24px 60px rgba(14, 40, 88, 0.1);
}

.login-tag,
.login-card h1,
.login-tip,
.account-panel p {
  margin: 0;
}

.login-tag {
  color: #5f7396;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.login-card h1 {
  margin-top: 10px;
  color: #10284d;
  font-size: 34px;
}

.login-tip {
  display: block;
  margin-top: 12px;
  color: #5c7091;
}

.login-form {
  margin-top: 26px;
}

.login-button {
  width: 100%;
  margin-top: 8px;
}

.account-panel {
  margin-top: 24px;
  padding: 18px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(241, 246, 255, 0.96), rgba(255, 246, 227, 0.96));
}

.account-panel strong {
  display: block;
  margin-bottom: 8px;
  color: #12315e;
}

.account-panel p + p {
  margin-top: 6px;
}
</style>
