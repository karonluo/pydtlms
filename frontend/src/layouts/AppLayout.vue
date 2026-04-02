<script setup lang="ts">
import {
  DataAnalysis,
  DocumentChecked,
  Files,
  Histogram,
  Reading,
  Setting,
  SwitchButton,
  UserFilled,
} from '@element-plus/icons-vue'
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'

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
const openedGroups = ref<string[]>([])

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
    items: [{ path: '/students', label: '学生主档', icon: UserFilled, requiredPermission: 'students:read' }],
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
        key: 'audit',
        label: '审计日志',
        icon: Files,
        items: [
          { path: '/system/operation-logs', label: '操作日志', icon: Files, requiredPermission: 'audit:read' },
          { path: '/system/sync-logs', label: '同步日志', icon: Files, requiredPermission: 'audit:read' },
        ],
      },
    ],
  },
]

const currentTitle = computed(() => String(route.meta.title || '博士生生命周期管理系统'))
const visibleMenuGroups = computed(() => {
  const permissionSet = new Set(authStore.permissions)
  const hasPermission = (permission?: string) => !permission || permissionSet.has(permission)

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

watch(() => route.path, syncOpenedGroups, { immediate: true })
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
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.layout-shell {
  min-height: 100vh;
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
}
</style>
