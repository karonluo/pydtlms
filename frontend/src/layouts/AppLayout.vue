<script setup lang="ts">
import {
  ArrowDown,
  DataAnalysis,
  DocumentChecked,
  Files,
  Histogram,
  Reading,
  Setting,
  UserFilled,
} from '@element-plus/icons-vue'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const menuTree = [
  {
    key: 'dashboard',
    label: '工作台',
    icon: DataAnalysis,
    groups: [{ title: '全局视图', items: [{ path: '/dashboard', label: '数据驾驶舱', hint: '全局运行态' }] }],
  },
  {
    key: 'recruitment',
    label: '招生',
    icon: Histogram,
    groups: [{ title: '招生执行', items: [{ path: '/recruitment', label: '招生计划与报名', hint: '计划、报名与录取' }] }],
  },
  {
    key: 'students',
    label: '学生',
    icon: UserFilled,
    groups: [{ title: '学生主数据', items: [{ path: '/students', label: '学生主档', hint: '主数据、导师与状态' }] }],
  },
  {
    key: 'training',
    label: '培养',
    icon: Reading,
    groups: [
      {
        title: '培养执行',
        items: [
          { path: '/training/plans', label: '培养方案', hint: '版本、周期与目标' },
          { path: '/training/reports', label: '科研报告', hint: '提交、审阅与评分' },
          { path: '/training/outbound', label: '外出研修', hint: '联合培养与企业研修' },
        ],
      },
    ],
  },
  {
    key: 'degree',
    label: '学位',
    icon: DocumentChecked,
    groups: [
      {
        title: '学位通道',
        items: [
          { path: '/degree/theses', label: '论文主档', hint: '查重、盲审、答辩' },
          { path: '/degree/reviews', label: '盲审意见', hint: '专家回执与评分' },
        ],
      },
    ],
  },
  {
    key: 'workflow',
    label: '审批',
    icon: Files,
    groups: [{ title: '流程中心', items: [{ path: '/workflow/tasks', label: '审批中心', hint: '待办、在途与归档' }] }],
  },
  {
    key: 'system',
    label: '治理',
    icon: Setting,
    groups: [
      {
        title: '基础配置',
        items: [
          { path: '/system/users', label: '系统用户', hint: '账号、部门与状态' },
          { path: '/system/roles', label: '角色权限', hint: '职责分离与授权' },
          { path: '/system/audit', label: '审计策略', hint: '日志与留痕规则' },
          { path: '/system/integrations', label: '集成链路', hint: '外部系统同步' },
        ],
      },
      {
        title: '运行审计',
        items: [
          { path: '/system/operation-logs', label: '操作日志', hint: '关键动作追踪' },
          { path: '/system/sync-logs', label: '同步日志', hint: '外部同步回执' },
        ],
      },
    ],
  },
]

const activeMainMenu = computed(() => menuTree.find((item) => route.path.startsWith(`/${item.key}`))?.key || 'dashboard')
const activeMenu = computed(() => menuTree.find((item) => item.key === activeMainMenu.value) || menuTree[0])

function goProfile() {
  router.push('/profile')
}

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="shell">
    <aside class="shell-sidebar">
      <div class="main-rail">
        <div class="brand-mark">D</div>
        <button
          v-for="item in menuTree"
          :key="item.key"
          class="main-rail__item"
          :class="{ 'is-active': activeMainMenu === item.key }"
          type="button"
          @click="router.push(item.groups[0].items[0].path)"
        >
          <component :is="item.icon" class="main-rail__icon" />
          <span>{{ item.label }}</span>
        </button>
      </div>

      <div class="menu-panel">
        <div class="brand-block">
          <div>
            <strong>DTLMS</strong>
            <p>博士生生命周期管理系统</p>
          </div>
        </div>

        <section v-for="group in activeMenu.groups" :key="group.title" class="menu-group">
          <p class="menu-group__title">{{ group.title }}</p>
          <button
            v-for="item in group.items"
            :key="item.path"
            class="nav-item"
            :class="{ 'is-active': route.path === item.path }"
            type="button"
            @click="router.push(item.path)"
          >
            <span>
              <strong>{{ item.label }}</strong>
              <small>{{ item.hint }}</small>
            </span>
          </button>
        </section>

        <section class="sidebar-callout">
          <p>治理要点</p>
          <strong>CTDTLMS_</strong>
          <span>Redis Key 前缀统一管理，便于哨兵主从切换与缓存隔离。</span>
        </section>
      </div>
    </aside>

    <main class="shell-main">
      <header class="shell-header">
        <div>
          <p class="eyebrow">前后端分离 · Vue3 + FastAPI · PostgreSQL + Redis Sentinel</p>
          <h1>{{ route.meta.title || '博士生生命周期管理系统' }}</h1>
        </div>

        <el-dropdown trigger="click">
          <div class="user-panel">
            <div class="user-avatar">{{ authStore.initials }}</div>
            <div>
              <strong>{{ authStore.fullName }}</strong>
              <p>{{ authStore.roleName }}</p>
            </div>
            <el-icon><ArrowDown /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="goProfile">个人空间</el-dropdown-item>
              <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </header>

      <section class="hero-band">
        <div>
          <p class="hero-band__title">业务已落地</p>
          <strong>当前已接入招生计划、报名申请、学生主数据三类核心管理操作，支持直接维护与状态流转。</strong>
        </div>
        <el-space wrap>
          <el-tag type="success" effect="dark">RBAC</el-tag>
          <el-tag type="warning" effect="dark">JWT</el-tag>
          <el-tag type="info" effect="dark">审计日志</el-tag>
          <el-tag type="primary" effect="dark">管理页</el-tag>
        </el-space>
      </section>

      <router-view />
    </main>
  </div>
</template>

<style scoped>
.shell {
  display: grid;
  grid-template-columns: 360px minmax(0, 1fr);
  min-height: 100vh;
}

.shell-sidebar {
  position: sticky;
  top: 0;
  display: grid;
  grid-template-columns: 88px minmax(0, 1fr);
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(54, 130, 255, 0.18), transparent 32%),
    linear-gradient(180deg, #0c2f63 0%, #0d2145 45%, #09182f 100%);
  color: #f5f9ff;
}

.main-rail {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
  padding: 26px 14px;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.main-rail__item {
  display: grid;
  justify-items: center;
  gap: 6px;
  width: 100%;
  padding: 12px 8px;
  border: 0;
  border-radius: 18px;
  background: transparent;
  color: rgba(245, 249, 255, 0.8);
  cursor: pointer;
}

.main-rail__item.is-active {
  background: rgba(255, 255, 255, 0.14);
  color: #ffffff;
}

.main-rail__item span {
  font-size: 12px;
}

.main-rail__icon {
  font-size: 18px;
}

.menu-panel {
  display: flex;
  flex-direction: column;
  gap: 22px;
  padding: 28px 22px;
}

.brand-block {
  display: flex;
  align-items: center;
}

.brand-block p,
.sidebar-callout p,
.sidebar-callout span {
  margin: 0;
}

.brand-mark {
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 16px;
  background: linear-gradient(145deg, #f4fbff, #72aef8);
  color: #0d2a57;
  font-size: 24px;
  font-weight: 700;
}

.menu-group {
  display: grid;
  gap: 10px;
}

.menu-group__title {
  margin: 0;
  color: rgba(245, 249, 255, 0.56);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.nav-item {
  display: block;
  width: 100%;
  padding: 14px 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.06);
  color: inherit;
  text-align: left;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.2s ease;
}

.nav-item:hover {
  transform: translateX(4px);
  background: rgba(255, 255, 255, 0.12);
}

.nav-item strong,
.nav-item small {
  display: block;
}

.nav-item small {
  margin-top: 4px;
  color: rgba(245, 249, 255, 0.66);
}

.nav-item.is-active {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.22), rgba(124, 177, 255, 0.28));
  border-color: rgba(255, 255, 255, 0.28);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
}

.sidebar-callout {
  margin-top: auto;
  padding: 18px;
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.08);
}

.sidebar-callout p {
  color: rgba(245, 249, 255, 0.7);
  font-size: 13px;
}

.sidebar-callout strong {
  display: block;
  margin: 10px 0 8px;
  font-size: 24px;
}

.sidebar-callout span {
  display: block;
  color: rgba(245, 249, 255, 0.78);
  line-height: 1.6;
}

.shell-main {
  padding: 28px;
}

.shell-header {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: center;
}

.eyebrow,
.hero-band__title,
.user-panel p {
  margin: 0;
}

.shell-header h1 {
  margin: 8px 0 0;
  color: #12284d;
  font-size: 34px;
}

.eyebrow {
  color: #5f7396;
  font-size: 13px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.user-panel {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 12px 30px rgba(14, 40, 88, 0.06);
  cursor: pointer;
}

.user-avatar {
  display: grid;
  place-items: center;
  width: 42px;
  height: 42px;
  border-radius: 14px;
  background: linear-gradient(145deg, #ffefc2, #fbcc6a);
  color: #7c5412;
  font-size: 22px;
  font-weight: 700;
}

.hero-band {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  margin: 24px 0 28px;
  padding: 22px 24px;
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 24px;
  background:
    radial-gradient(circle at top right, rgba(251, 206, 107, 0.4), transparent 24%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(235, 245, 255, 0.94));
}

.hero-band__title {
  color: #6b7d97;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.hero-band strong {
  display: block;
  margin-top: 8px;
  color: #10284d;
  font-size: 20px;
  line-height: 1.5;
  max-width: 720px;
}

@media (max-width: 1180px) {
  .shell {
    grid-template-columns: 1fr;
  }

  .shell-sidebar {
    position: static;
    min-height: auto;
    grid-template-columns: 1fr;
  }

  .main-rail {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    border-right: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }
}

@media (max-width: 768px) {
  .shell-main {
    padding: 18px;
  }

  .shell-header,
  .hero-band {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
