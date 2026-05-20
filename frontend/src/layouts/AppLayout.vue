<script setup lang="ts">
import {
  Bell,
  DataAnalysis,
  DocumentChecked,
  Files,
  Histogram,
  Loading,
  Reading,
  Setting,
  SwitchButton,
  UserFilled,
  WarningFilled,
  CircleCheckFilled,
} from '@element-plus/icons-vue'
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import type { RegisteredPortalStudentExportJobRecord } from '../api/students'
import { useAuthStore } from '../stores/auth'
import { useExportJobStore } from '../stores/exportJobs'

type MenuItem = {
  path: string
  label: string
  icon: unknown
  requiredPermission?: string
}

type MenuGroup = {
  key: string
  label: string
  icon: unknown
  items?: MenuItem[]
  sections?: Array<{
    key: string
    label: string
    icon: unknown
    items: MenuItem[]
  }>
}

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const exportJobStore = useExportJobStore()
const openedGroups = ref<string[]>([])
const exportJobDialogVisible = ref(false)

const menuGroups: MenuGroup[] = [
  {
    key: 'workspace',
    label: '工作台',
    icon: DataAnalysis,
    items: [
      { path: '/dashboard', label: '经营总览', icon: DataAnalysis, requiredPermission: 'dashboard:read' },
      { path: '/workflow/tasks', label: '流程待办', icon: Files, requiredPermission: 'workflow:read' },
    ],
  },
  {
    key: 'recruitment',
    label: '招生管理',
    icon: Histogram,
    items: [{ path: '/recruitment', label: '招生计划', icon: Histogram, requiredPermission: 'recruitment:read' }],
  },
  {
    key: 'students',
    label: '学生管理',
    icon: UserFilled,
    items: [
      { path: '/students/records', label: '学生主档', icon: UserFilled, requiredPermission: 'students:read' },
      { path: '/students/portal-registrations', label: '注册学生', icon: UserFilled, requiredPermission: 'students:read' },
      { path: '/students/centers', label: '研究中心', icon: UserFilled, requiredPermission: 'students:read' },
    ],
  },
  {
    key: 'training',
    label: '培养管理',
    icon: Reading,
    items: [
      { path: '/training/plans', label: '培养方案', icon: Reading, requiredPermission: 'training:read' },
      { path: '/training/reports', label: '科研报告', icon: Reading, requiredPermission: 'training:read' },
      { path: '/training/outbound', label: '外出研修', icon: Reading, requiredPermission: 'training:read' },
    ],
  },
  {
    key: 'degree',
    label: '学位管理',
    icon: DocumentChecked,
    items: [
      { path: '/degree/theses', label: '论文主档', icon: DocumentChecked, requiredPermission: 'degree:read' },
      { path: '/degree/reviews', label: '盲审意见', icon: DocumentChecked, requiredPermission: 'degree:read' },
    ],
  },
  {
    key: 'system',
    label: '系统管理',
    icon: Setting,
    items: [{ path: '/system/users', label: '用户管理', icon: Setting, requiredPermission: 'system:read' }],
    sections: [
      {
        key: 'authority',
        label: '权限配置',
        icon: Setting,
        items: [
          { path: '/system/roles', label: '角色管理', icon: Setting, requiredPermission: 'system:read' },
          { path: '/system/audit', label: '审计策略', icon: Setting, requiredPermission: 'audit:read' },
          { path: '/system/integrations', label: '接口管理', icon: Setting, requiredPermission: 'system:read' },
        ],
      },
      {
        key: 'dictionary',
        label: '字典管理',
        icon: Setting,
        items: [
          { path: '/system/dict-types', label: '字典类型', icon: Setting, requiredPermission: 'system:read' },
          { path: '/system/dict-data', label: '字典数据', icon: Setting, requiredPermission: 'system:read' },
        ],
      },
      {
        key: 'audit',
        label: '审计日志',
        icon: Files,
        items: [
          { path: '/system/operation-logs', label: '操作日志', icon: Files, requiredPermission: 'audit:read' },
          { path: '/system/notification-logs', label: '通知发送日志', icon: Files, requiredPermission: 'audit:read' },
          { path: '/system/sync-logs', label: '同步日志', icon: Files, requiredPermission: 'audit:read' },
        ],
      },
    ],
  },
]

const currentTitle = computed(() => String(route.meta.title || '博士生生命周期管理系统'))
const visibleMenuGroups = computed(() => {
  const permissionSet = new Set(authStore.permissions)
  const hasPermission = (permission?: string) => !permission || permissionSet.has('*') || permissionSet.has(permission)

  return menuGroups
    .map((group) => {
      const items = (group.items || []).filter((item) => hasPermission(item.requiredPermission))
      const sections = (group.sections || [])
        .map((section) => ({
          ...section,
          items: section.items.filter((item) => hasPermission(item.requiredPermission)),
        }))
        .filter((section) => section.items.length > 0)

      return {
        ...group,
        items,
        sections,
      }
    })
    .filter((group) => (group.items || []).length > 0 || (group.sections || []).length > 0)
})
const headerAvatarText = computed(() => {
  const displayText = String(authStore.fullName || authStore.username || '').trim()
  return displayText ? displayText.slice(0, 1).toUpperCase() : '博'
})

function isGroupActive(group: MenuGroup) {
  return (group.items || []).some((item) => route.path === item.path)
    || (group.sections || []).some((section) => section.items.some((item) => route.path === item.path))
}

function syncOpenedGroups() {
  const activeGroup = visibleMenuGroups.value.find((group) => isGroupActive(group))
  openedGroups.value = activeGroup ? [activeGroup.key] : []
}

async function goLogout() {
  await authStore.logout()
  router.push('/login')
}

function goProfile() {
  router.push('/profile')
}

function resolveExportJobStatusLabel(status: string) {
  if (status === 'completed') return '导出成功'
  if (status === 'failed') return '导出失败'
  if (status === 'running') return '导出中'
  return '等待处理'
}

function resolveExportJobTime(job: { completed_at?: string | null; failed_at?: string | null; started_at?: string | null; created_at: string }) {
  return job.completed_at || job.failed_at || job.started_at || job.created_at
}

async function openExportJobDialog() {
  exportJobDialogVisible.value = true
  await exportJobStore.fetchJobs()
  await exportJobStore.acknowledgeJobs()
}

async function handleDownloadExportJob(job: RegisteredPortalStudentExportJobRecord) {
  try {
    await exportJobStore.downloadJob(job)
    ElMessage.success('导出文件已开始下载')
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '下载失败')
  }
}

watch(() => route.path, syncOpenedGroups, { immediate: true })
watch(
  () => authStore.isAuthenticated,
  (isAuthenticated) => {
    if (isAuthenticated) {
      exportJobStore.startPolling()
      return
    }
    exportJobStore.clear()
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  exportJobStore.stopPolling()
})
</script>

<template>
  <el-container class="layout-shell">
    <el-aside class="layout-aside" width="252px">
      <div class="brand-block">
        <div class="brand-badge">DT</div>
        <div>
          <h1>博士生仪表</h1>
          <p>招生到归档全流程协同</p>
        </div>
      </div>

      <div class="menu-scroll-host">
        <el-scrollbar>
          <el-menu :default-active="route.path" :default-openeds="openedGroups" :unique-opened="true" router class="side-menu">
            <el-sub-menu v-for="group in visibleMenuGroups" :key="group.key" :index="group.key">
              <template #title>
                <el-icon><component :is="group.icon" /></el-icon>
                <span>{{ group.label }}</span>
              </template>

              <el-menu-item v-for="item in group.items || []" :key="item.path" :index="item.path">
                <el-icon><component :is="item.icon" /></el-icon>
                <span>{{ item.label }}</span>
              </el-menu-item>

              <el-sub-menu v-for="section in group.sections || []" :key="section.key" :index="`${group.key}:${section.key}`">
                <template #title>
                  <el-icon><component :is="section.icon" /></el-icon>
                  <span>{{ section.label }}</span>
                </template>

                <el-menu-item v-for="item in section.items" :key="item.path" :index="item.path">
                  <el-icon><component :is="item.icon" /></el-icon>
                  <span>{{ item.label }}</span>
                </el-menu-item>
              </el-sub-menu>
            </el-sub-menu>
          </el-menu>
        </el-scrollbar>
      </div>
    </el-aside>

    <el-container>
      <el-header class="layout-header">
        <div>
          <h2>{{ currentTitle }}</h2>
        </div>
        <div class="header-actions">
          <el-tag type="success" effect="light">登录成功</el-tag>

          <el-badge :value="exportJobStore.unreadCount || undefined" :hidden="!exportJobStore.unreadCount" class="export-job-badge">
            <el-button circle plain class="export-job-button" @click="openExportJobDialog">
              <el-icon v-if="exportJobStore.iconStatus === 'danger'" class="is-danger"><WarningFilled /></el-icon>
              <el-icon v-else-if="exportJobStore.iconStatus === 'success'" class="is-success"><CircleCheckFilled /></el-icon>
              <el-icon v-else-if="exportJobStore.hasActiveJobs" class="is-warning"><Loading /></el-icon>
              <el-icon v-else><Bell /></el-icon>
            </el-button>
          </el-badge>

          <button class="user-panel" type="button" @click="goProfile">
            <div class="user-panel__avatar">{{ headerAvatarText }}</div>
            <div class="user-panel__meta">
              <strong>{{ authStore.fullName }}</strong>
              <span>{{ authStore.username }}</span>
            </div>
          </button>

          <el-button plain @click="goLogout">
            <el-icon><SwitchButton /></el-icon>
            <span>退出登录</span>
          </el-button>
        </div>
      </el-header>

      <el-main class="layout-main">
        <div class="layout-view-host">
          <router-view />
        </div>
      </el-main>
    </el-container>

    <el-dialog v-model="exportJobDialogVisible" title="导出通知" width="680px" destroy-on-close>
      <div class="export-job-dialog">
        <div class="export-job-dialog__summary">
          <div>
            <span class="export-job-dialog__label">未读结果</span>
            <strong>{{ exportJobStore.unreadCount }}</strong>
          </div>
          <div>
            <span class="export-job-dialog__label">进行中任务</span>
            <strong>{{ exportJobStore.jobs.filter((job) => job.status === 'pending' || job.status === 'running').length }}</strong>
          </div>
          <div>
            <span class="export-job-dialog__label">最近记录</span>
            <strong>{{ exportJobStore.jobs.length }}</strong>
          </div>
        </div>

        <div v-if="!exportJobStore.jobs.length" class="export-job-panel__empty">暂无导出记录</div>
        <div v-else class="export-job-list">
          <div v-for="job in exportJobStore.jobs" :key="job.job_id" class="export-job-item">
            <div class="export-job-item__meta">
              <strong>{{ resolveExportJobStatusLabel(job.status) }}</strong>
              <span>{{ resolveExportJobTime(job) }}</span>
            </div>
            <p>{{ job.file_name }}</p>
            <div v-if="job.status === 'completed'" class="export-job-item__actions">
              <span class="export-job-link">{{ job.download_url || '下载地址生成中' }}</span>
              <el-button link type="primary" :loading="exportJobStore.downloadingJobId === job.job_id" @click="handleDownloadExportJob(job)">
                点击下载
              </el-button>
            </div>
            <div v-else-if="job.status === 'failed'" class="export-job-item__actions is-error">
              <span>{{ job.error_message || '导出失败，请重试' }}</span>
            </div>
            <div v-else class="export-job-item__actions">
              <span>开始导出等待完成</span>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button type="primary" @click="exportJobDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </el-container>
</template>

<style scoped>
.layout-shell {
  height: 100vh;
  overflow: hidden;
}

.layout-aside {
  background: var(--surface-dark);
  color: var(--text-main);
  padding: 18px 14px;
  box-shadow: inset -1px 0 0 var(--border);
  display: flex;
  flex-direction: column;
}

.brand-block {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 16px;
  padding: 12px;
  border-radius: 16px;
  background: var(--surface-strong);
  border: 1px solid var(--border);
  box-shadow: var(--panel-shadow-soft);
}

.brand-badge {
  width: 46px;
  height: 46px;
  border-radius: 14px;
  background: var(--brand-strong);
  display: grid;
  place-items: center;
  color: var(--brand-contrast);
  font-family: var(--title-font);
  font-weight: 700;
  box-shadow: var(--panel-shadow-strong);
}

.brand-block h1 {
  margin: 0;
  font-family: var(--title-font);
  font-size: 18px;
}

.brand-block p {
  margin: 4px 0 0;
  color: var(--text-subtle);
  font-size: 12px;
}

.menu-scroll-host {
  flex: 1;
  min-height: 0;
}

.menu-scroll-host :deep(.el-scrollbar) {
  height: 100%;
}

.menu-scroll-host :deep(.el-scrollbar__wrap) {
  overflow-x: hidden;
}

.side-menu {
  background: transparent;
}

.side-menu :deep(.el-sub-menu__title),
.side-menu :deep(.el-menu-item) {
  height: 40px;
  margin-bottom: 6px;
  border-radius: 12px;
  color: var(--text-subtle);
  font-weight: 600;
  font-size: 13px;
}

.side-menu :deep(.el-sub-menu .el-menu) {
  background: transparent;
}

.side-menu :deep(.el-sub-menu__title:hover),
.side-menu :deep(.el-menu-item:hover) {
  background: var(--hover-bg-strong);
  color: var(--brand-deep);
}

.side-menu :deep(.el-menu-item.is-active) {
  background: var(--brand-strong);
  color: var(--brand-contrast);
  box-shadow: var(--panel-shadow-strong);
}

.side-menu :deep(.el-sub-menu.is-opened > .el-sub-menu__title) {
  background: var(--brand);
  color: var(--brand-contrast);
}

.side-menu :deep(.el-sub-menu .el-menu-item),
.side-menu :deep(.el-sub-menu .el-sub-menu__title) {
  margin-left: 8px;
  min-width: unset;
}

.side-menu :deep(.el-sub-menu .el-sub-menu .el-menu-item) {
  margin-left: 16px;
}

.layout-header {
  height: auto;
  padding: 10px 18px 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  background: var(--surface-strong);
  border-bottom: 1px solid var(--border);
}

.layout-header h2 {
  margin: 0;
  font-family: var(--title-font);
  font-size: 24px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.export-job-badge {
  display: inline-flex;
}

.export-job-button {
  border-color: var(--border-strong);
}

.export-job-button :deep(.el-icon.is-danger) {
  color: var(--danger);
}

.export-job-button :deep(.el-icon.is-success) {
  color: var(--success);
}

.export-job-button :deep(.el-icon.is-warning) {
  color: var(--warning);
}

.export-job-panel {
  display: grid;
  gap: 12px;
}

.export-job-dialog {
  display: grid;
  gap: 16px;
}

.export-job-dialog__summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: #f8fafc;
}

.export-job-dialog__label {
  display: block;
  margin-bottom: 6px;
  color: var(--text-muted);
  font-size: 12px;
}

.export-job-dialog__summary strong {
  color: var(--text-main);
  font-size: 14px;
}

.export-job-panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.export-job-panel__header span,
.export-job-panel__empty,
.export-job-item__meta span,
.export-job-item__actions span,
.export-job-link {
  color: var(--text-muted);
  font-size: 12px;
}

.export-job-list {
  display: grid;
  gap: 10px;
  max-height: 320px;
  overflow: auto;
}

.export-job-item {
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--surface);
  display: grid;
  gap: 8px;
}

.export-job-item p {
  margin: 0;
  color: var(--text-main);
  word-break: break-all;
}

.export-job-item__meta,
.export-job-item__actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.export-job-item__actions.is-error {
  justify-content: flex-start;
}

.export-job-link {
  flex: 1;
  word-break: break-all;
}

.user-panel {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-subtle);
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 6px 8px;
  border-radius: 10px;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.user-panel:hover {
  background: var(--hover-bg);
  color: var(--text-main);
}

.user-panel__meta {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-panel strong,
.user-panel span {
  text-align: left;
}

.user-panel__avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: var(--surface-muted);
  color: var(--brand-deep);
  display: grid;
  place-items: center;
  font-weight: 700;
  flex: 0 0 auto;
}

.user-panel__meta strong {
  font-size: 13px;
}

.user-panel__meta span {
  font-size: 12px;
}

.layout-main {
  padding: 4px 18px 18px;
  min-width: 0;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
}

.layout-view-host {
  min-height: 100%;
  min-width: 0;
}

.layout-shell > .el-container {
  min-width: 0;
  min-height: 0;
}

@media (max-width: 960px) {
  .layout-shell {
    flex-direction: column;
  }

  .layout-aside {
    width: 100% !important;
  }

  .layout-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
  }

  .export-job-dialog__summary {
    grid-template-columns: minmax(0, 1fr);
  }
}
</style>
