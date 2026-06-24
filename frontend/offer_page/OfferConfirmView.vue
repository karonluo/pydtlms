<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { AxiosError } from 'axios'

import http from '../src/api/http'

/**
 * 活动邀请确认页
 * 仿照 offer_page/index.html 的视觉效果，使用 Vue3 + Element Plus 设计语言
 * 适配 Vue 3 <script setup>，样式使用 scoped
 */

type ChoiceValue = 'accept' | 'reject'

interface ChoiceOption {
  value: ChoiceValue
  title: string
  desc: string
}

const choiceOptions: ChoiceOption[] = [
  { value: 'accept', title: '接受邀请', desc: '确认参加夏令营' },
  { value: 'reject', title: '拒绝邀请', desc: '放弃此次参营机会' },
]

const form = reactive({
  email: '',
  password: '',
  choice: 'accept' as ChoiceValue,
})

const submitted = ref(false)
const submitting = ref(false)

const selectedChoice = computed(() => form.choice)

function selectChoice(value: ChoiceValue) {
  form.choice = value
}

function resolveErrorMessage(error: unknown): string {
  const axiosError = error as AxiosError<{ detail?: string }>
  const detail = axiosError.response?.data?.detail
  if (typeof detail === 'string' && detail.trim()) {
    return detail.trim()
  }
  if (error instanceof Error && error.message.trim()) {
    return error.message.trim()
  }
  return '提交失败，请稍后重试'
}

async function handleSubmit() {
  if (submitting.value) return
  if (!form.email.trim() || !form.password.trim()) {
    ElMessage.warning('请先填写邮箱和密码')
    return
  }
  // 二次确认：明确告知用户当前的选择及提交后的不可逆性
  const choiceText = form.choice === 'accept' ? '接受邀请（确认入营）' : '拒绝邀请（放弃入营）'
  try {
    await ElMessageBox.confirm(
      `您当前选择的是：${choiceText}。\n\n提交后将无法修改，请确认信息无误。`,
      '提交确认',
      {
        type: 'warning',
        confirmButtonText: '确认提交',
        cancelButtonText: '再看看',
        dangerouslyUseHTMLString: false,
      },
    )
  } catch {
    return
  }
  submitting.value = true
  try {
    const payload = new FormData()
    payload.append('email', form.email.trim())
    payload.append('password', form.password)
    payload.append('choice', form.choice)
    await http.post('/recruitment/camp-offers/confirm', payload, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    submitted.value = true
    ElMessage.success('提交成功')
  } catch (error) {
    await ElMessageBox.alert(resolveErrorMessage(error), '提交失败', {
      type: 'error',
      confirmButtonText: '知道了',
      dangerouslyUseHTMLString: false,
    })
  } finally {
    submitting.value = false
  }
}

</script>

<template>
  <div class="offer-page">
    <div class="container">
      <!-- 邮件图标 -->
      <div class="icon-wrapper">
        <svg
          class="email-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="#6b7280"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
          <polyline points="22,6 12,13 2,6" />
        </svg>
      </div>

      <!-- 标题 -->
      <h1>夏令营活动邀请确认</h1>

      <!-- 重要事项卡片 -->
      <div class="important-box">
        <div class="section-title">
          <span class="info-icon">ⓘ</span>
          <span>重要事项</span>
        </div>

        <div class="sub-section">
          <p class="highlight-text">活动时间</p>
          <p>2026年7月3日（周五）- 7月6日（周一）</p>
        </div>

        <div class="sub-section">
          <p class="highlight-text">活动准备</p>
          <ul>
            <li>请自备笔记本电脑</li>
            <li>建议使用 Chrome 浏览器（82版本及以上）</li>
            <li>请提前做好设备检查并保持充足电量</li>
          </ul>
        </div>

        <div class="sub-section">
          <p class="highlight-text">食宿安排</p>
          <p>实验室将根据系统确认名单统一安排活动期间食宿。住宿时间为：2026年7月3日至7月5日，共3晚。</p>
        </div>
      </div>

      <!-- 选择区域 -->
      <div class="choice-section">
        <h2>您的选择</h2>
        <div class="radio-group">
          <label
            v-for="item in choiceOptions"
            :key="item.value"
            class="radio-item"
            :class="{ active: selectedChoice === item.value }"
            @click.prevent="selectChoice(item.value)"
          >
            <input
              v-model="form.choice"
              type="radio"
              name="choice"
              :value="item.value"
            >
            <span class="radio-custom" />
            <div class="radio-content">
              <p class="radio-title">{{ item.title }}</p>
              <p class="radio-desc">{{ item.desc }}</p>
            </div>
            <span class="check-icon">✔</span>
          </label>
        </div>
      </div>

      <!-- 邮箱和密码表单 -->
      <div class="form-section">
        <div class="form-group">
          <label for="offer-account">邮箱地址</label>
          <input id="offer-account" v-model="form.email" type="email" autocomplete="username">
        </div>
        <div class="form-group">
          <label for="offer-password">登录密码</label>
          <input id="offer-password" v-model="form.password" type="password" autocomplete="current-password">
        </div>
      </div>

      <!-- 提交按钮 -->
      <button
        class="submit-btn"
        :disabled="submitting"
        @click="handleSubmit"
      >
        {{ submitting ? '提交中...' : '提交确认' }}
      </button>

      <p v-if="submitted" class="success-tip">已提交，请留意后续邮件通知。</p>

      <!-- 底部提示 -->
      <p class="footer-tip">请在收到邮件后24小时内完成参营确认，逾期未确认者，将视为自动放弃参营资格。</p>
    </div>
  </div>
</template>

<style scoped>
/* ====================== 全局重置与基础样式 ====================== */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.offer-page {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  background-color: #f8fafc; /* 浅灰背景 */
  color: #1e293b; /* 深色文字 */
  line-height: 1.6;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.container {
  width: 100%;
  max-width: 700px; /* PC 端最大宽度，移动端自动收缩 */
  background: #ffffff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

/* ====================== 顶部图标与标题 ====================== */
.icon-wrapper {
  text-align: center;
  margin-bottom: 20px;
}

.email-icon {
  width: 48px;
  height: 48px;
  background: #f1f5f9;
  border-radius: 50%;
  padding: 12px;
}

h1 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 24px;
  color: #0f172a;
}

/* ====================== 重要事项卡片 ====================== */
.important-box {
  background: #fefce8; /* 浅黄色背景 */
  border: 1px solid #fef08a;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #ca8a04; /* 橙色强调 */
  margin-bottom: 16px;
}

.info-icon {
  color: #ca8a04;
  font-size: 18px;
}

.sub-section {
  margin-bottom: 16px;
}

.sub-section:last-child {
  margin-bottom: 0;
}

.highlight-text {
  color: #ea580c; /* 红色强调 */
  font-weight: 600;
  margin-bottom: 8px;
}

.sub-section ul {
  list-style: none;
  padding-left: 20px;
}

.sub-section li {
  position: relative;
  margin-bottom: 8px;
}

.sub-section li::before {
  content: "•";
  position: absolute;
  left: -16px;
  top: 0;
  color: #1e293b;
}

/* ====================== 选择区域（单选框组） ====================== */
.choice-section h2 {
  font-size: 18px;
  margin-bottom: 16px;
  color: #0f172a;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.radio-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.radio-item.active {
  border-color: #3b82f6; /* 蓝色边框（选中态） */
  background: #eff6ff; /* 浅蓝背景 */
}

.radio-item input[type="radio"] {
  display: none; /* 隐藏原生单选框 */
}

.radio-custom {
  width: 20px;
  height: 20px;
  border: 2px solid #cbd5e1;
  border-radius: 50%;
  margin-right: 12px;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.radio-item.active .radio-custom {
  border-color: #3b82f6;
  background: #3b82f6;
}

.radio-content {
  flex: 1;
}

.radio-title {
  font-weight: 600;
  margin-bottom: 4px;
}

.radio-desc {
  font-size: 14px;
  color: #64748b;
}

.check-icon {
  display: none;
  color: #3b82f6;
  font-size: 18px;
}

.radio-item.active .check-icon {
  display: block;
}

/* ====================== 表单区域 ====================== */
.form-section {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #475569;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s ease;
  color: #1e293b;
  background-color: #ffffff;
}

.form-group input:focus {
  outline: none;
  border-color: #3b82f6;
}

.form-group.error input {
  border-color: #ef4444; /* 错误态红色边框 */
}

.error-tip {
  color: #ef4444;
  font-size: 14px;
  margin-top: 8px;
}

.forgot-link {
  display: inline-block;
  margin-top: 8px;
  color: #3b82f6;
  text-decoration: none;
  font-size: 14px;
  text-align: right;
}

.forgot-link:hover {
  text-decoration: underline;
}

/* ====================== 提交按钮与底部提示 ====================== */
.submit-btn {
  width: 100%;
  padding: 14px;
  background: #3b82f6;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
  background: #2563eb;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.footer-tip {
  text-align: center;
  font-size: 14px;
  color: #64748b;
  margin-top: 24px;
}

/* ====================== 移动端适配（屏幕 ≤768px） ====================== */
@media (max-width: 768px) {
  .offer-page {
    padding: 10px;
  }

  .container {
    padding: 20px;
  }

  h1 {
    font-size: 20px;
  }

  .important-box {
    padding: 16px;
  }

  .radio-item {
    padding: 12px;
  }

  .submit-btn {
    padding: 12px;
    font-size: 14px;
  }
}
</style>
