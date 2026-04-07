import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '../stores/auth'

import AppLayout from '../layouts/AppLayout.vue'

const DashboardView = () => import('../views/dashboard/DashboardView.vue')
const RecruitmentWorkbenchView = () => import('../views/recruitment/RecruitmentWorkbenchView.vue')
const StudentsView = () => import('../views/students/StudentsView.vue')
const TrainingView = () => import('../views/training/TrainingView.vue')
const DegreeView = () => import('../views/degree/DegreeView.vue')
const SystemView = () => import('../views/system/SystemView.vue')
const DictView = () => import('../views/system/DictView.vue')
const WorkflowCenterView = () => import('../views/workflow/WorkflowCenterView.vue')
const LoginView = () => import('../views/auth/LoginView.vue')
const ProfileView = () => import('../views/profile/ProfileView.vue')

const APP_TITLE = '博士生生命周期管理系统'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: LoginView, meta: { public: true, title: '系统登录' } },
    {
      path: '/',
      component: AppLayout,
      children: [
        { path: '', redirect: '/dashboard' },
        { path: 'dashboard', component: DashboardView, meta: { title: '经营总览' } },
        { path: 'recruitment', component: RecruitmentWorkbenchView, meta: { title: '招生计划' } },
        { path: 'students', redirect: '/students/records' },
        { path: 'students/records', component: StudentsView, meta: { title: '学生主档', section: 'records' } },
        { path: 'students/teams', component: StudentsView, meta: { title: '团队管理', section: 'teams' } },
        { path: 'training', redirect: '/training/plans' },
        { path: 'training/plans', component: TrainingView, meta: { title: '培养方案管理', section: 'plans' } },
        { path: 'training/reports', component: TrainingView, meta: { title: '科研报告管理', section: 'reports' } },
        { path: 'training/outbound', component: TrainingView, meta: { title: '外出研修管理', section: 'outbound' } },
        { path: 'degree', redirect: '/degree/theses' },
        { path: 'degree/theses', component: DegreeView, meta: { title: '论文主档管理', section: 'theses' } },
        { path: 'degree/reviews', component: DegreeView, meta: { title: '盲审意见管理', section: 'reviews' } },
        { path: 'workflow/tasks', component: WorkflowCenterView, meta: { title: '审批中心' } },
        { path: 'system', redirect: '/system/users' },
        { path: 'system/users', component: SystemView, meta: { title: '系统用户管理', section: 'users' } },
        { path: 'system/roles', component: SystemView, meta: { title: '角色权限管理', section: 'roles' } },
        { path: 'system/dict-types', component: DictView, meta: { title: '字典类型管理', section: 'dict-types' } },
        { path: 'system/dict-data', component: DictView, meta: { title: '字典数据管理', section: 'dict-data' } },
        { path: 'system/audit', component: SystemView, meta: { title: '审计策略管理', section: 'audit' } },
        { path: 'system/integrations', component: SystemView, meta: { title: '集成链路管理', section: 'integrations' } },
        { path: 'system/operation-logs', component: SystemView, meta: { title: '操作日志查询', section: 'operation-logs' } },
        { path: 'system/sync-logs', component: SystemView, meta: { title: '同步日志查询', section: 'sync-logs' } },
        { path: 'profile', component: ProfileView, meta: { title: '个人空间' } },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  const hasAccessToken = Boolean(localStorage.getItem('dtlms-access-token'))

  if (to.path === '/login' && hasAccessToken && authStore.sessionState !== 'ready') {
    try {
      await authStore.hydrateSession()
    } catch {
      // Let unauthenticated users stay on login.
    }
  }

  if (!to.meta.public) {
    if (!authStore.isAuthenticated) {
      authStore.rememberRedirectTarget(to.fullPath)
      if (hasAccessToken && authStore.sessionState !== 'ready') {
        try {
          await authStore.hydrateSession()
        } catch {
          return { path: '/login', query: { redirect: to.fullPath } }
        }
      }
      if (!authStore.isAuthenticated) {
        return { path: '/login', query: { redirect: to.fullPath } }
      }
    }
  }

  if (to.path === '/login' && authStore.isAuthenticated) {
    const queryRedirect = typeof to.query.redirect === 'string' ? to.query.redirect : ''
    return authStore.consumeRedirectTarget() || queryRedirect || '/dashboard'
  }

  return true
})

router.afterEach((to) => {
  const moduleTitle = String(to.meta.title || '首页')
  document.title = `${APP_TITLE}-${moduleTitle}`
})

export default router
