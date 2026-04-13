<script setup lang="ts">
import { nextTick, reactive, ref } from 'vue'
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

const presets = ['招生协同', '培养流程', '学位治理']

async function submit() {
  if (loading.value) {
    return
  }
  loading.value = true
  try {
    await authStore.login(form.username, form.password)
    ElMessage.success('登录成功')
    const queryRedirect = typeof route.query.redirect === 'string' ? route.query.redirect : ''
    const redirect = queryRedirect || authStore.consumeRedirectTarget() || '/dashboard'
    const target = redirect === '/login' ? '/dashboard' : redirect
    await router.replace(target)
    await router.isReady()
    await nextTick()

    if (router.currentRoute.value.fullPath !== target && router.currentRoute.value.path !== target) {
      const resolved = router.resolve(target)
      window.location.assign(resolved.href)
    }
  } catch {
    ElMessage.error(authStore.sessionError || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="login-page">
    <article class="login-shell">
      <section class="login-hero">
        <div class="login-badge">学位成长 · 研管业务 · 一体化系统</div>
        <h1>招生、培养、学位、审批统一在一个工作台里完成</h1>
        <p>覆盖学生主档、培养方案、科研报告、论文评审、审批留痕与系统治理等核心业务场景。</p>

        <div class="hero-tags">
          <span v-for="item in presets" :key="item">{{ item }}</span>
        </div>

        <div class="hero-metrics">
          <article>
            <strong>7</strong>
            <span>一级模块</span>
          </article>
          <article>
            <strong>3</strong>
            <span>核心审批流</span>
          </article>
          <article>
            <strong>24h</strong>
            <span>在线日志追踪</span>
          </article>
        </div>
      </section>

      <section class="login-panel">
        <div>
          <h2>系统登录</h2>
          <p class="login-panel__tip">请输入账号密码进入业务后台。</p>
        </div>

        <el-form label-position="top" class="login-form" @submit.prevent="submit">
          <el-form-item label="用户名">
            <el-input v-model="form.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码">
            <el-input v-model="form.password" type="password" show-password placeholder="请输入密码" />
          </el-form-item>
          <el-button type="primary" native-type="submit" size="large" class="login-button" :loading="loading">登录系统</el-button>
        </el-form>

        <div class="account-panel">
          <p>系统管理员：admin / Admin@123456</p>
          <p>导师账号：liu.ya / LiuYa@2026</p>
          <p>学位秘书：zhou.qing / ZhouQing@2026</p>
        </div>
      </section>
    </article>
  </section>
</template>

<style scoped>
.login-page {
  display: grid;
  place-items: center;
  min-height: 100vh;
  padding: 24px;
  background: linear-gradient(180deg, #edf5ff 0%, #e3eefb 100%);
}

.login-shell {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(360px, 0.9fr);
  gap: 18px;
  width: min(980px, 100%);
  padding: 20px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 24px 60px rgba(52, 93, 148, 0.14);
}

.login-hero {
  padding: 34px;
  border-radius: 24px;
  background: linear-gradient(160deg, #5b86c8, #4d79bf 55%, #446fb7 100%);
  color: #fff;
}

.login-badge,
.login-hero h1,
.login-hero p,
.account-panel p,
.login-panel h2,
.login-panel__tip {
  margin: 0;
}

.login-badge {
  display: inline-flex;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.16);
  font-size: 12px;
}

.login-hero h1 {
  margin-top: 26px;
  font-size: 30px;
  line-height: 1.18;
}

.login-hero p {
  margin-top: 18px;
  max-width: 520px;
  color: rgba(255, 255, 255, 0.88);
  font-size: 17px;
  line-height: 1.7;
}

.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 22px;
}

.hero-tags span {
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  font-size: 13px;
}

.hero-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 28px;
}

.hero-metrics article {
  padding: 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.1);
}

.hero-metrics strong {
  display: block;
  font-size: 26px;
}

.hero-metrics span {
  display: block;
  margin-top: 8px;
  color: rgba(255, 255, 255, 0.82);
  font-size: 13px;
}

.login-panel {
  display: grid;
  align-content: start;
  gap: 18px;
  padding: 28px 22px;
  border: 1px solid rgba(218, 229, 242, 0.98);
  border-radius: 24px;
  background: #ffffff;
}

.login-panel h2 {
  color: #18355d;
  font-size: 20px;
}

.login-panel__tip {
  margin-top: 10px;
  color: #7a8ea9;
}

.login-form {
  margin-top: 4px;
}

.login-button {
  width: 100%;
  margin-top: 6px;
}

.account-panel {
  color: #6f86a7;
  font-size: 13px;
  line-height: 1.8;
}

@media (max-width: 900px) {
  .login-shell {
    grid-template-columns: 1fr;
  }

  .hero-metrics {
    grid-template-columns: 1fr;
  }
}
</style>
