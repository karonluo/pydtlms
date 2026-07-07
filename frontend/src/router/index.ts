import { createRouter, createWebHistory } from 'vue-router'

import { clearPortalToken, getPortalProfile } from '../api/portal'
import { useAuthStore } from '../stores/auth'
import { hasGrantedPermission, resolveAccessibleRoutePath, resolveFirstAccessibleMenuPath } from './menuAccess'

import AppLayout from '../layouts/AppLayout.vue'

const DashboardView = () => import('../views/dashboard/DashboardView.vue')
const RecruitmentWorkbenchView = () => import('../views/recruitment/RecruitmentWorkbenchView.vue')
const NewsManagementView = () => import('../views/recruitment/NewsManagementView.vue')
const CampOfferListView = () => import('../views/recruitment/CampOfferListView.vue')
const StudentsView = () => import('../views/students/StudentsView.vue')
const ResearchCentersView = () => import('../views/students/ResearchCentersView.vue')
const RegisteredStudentsView = () => import('../views/students/RegisteredStudentsView.vue')
const TrainingView = () => import('../views/training/TrainingView.vue')
const DegreeView = () => import('../views/degree/DegreeView.vue')
const SystemView = () => import('../views/system/SystemView.vue')
const DictView = () => import('../views/system/DictView.vue')
const WorkflowCenterView = () => import('../views/workflow/WorkflowCenterView.vue')
const LoginView = () => import('../views/auth/LoginView.vue')
const ProfileView = () => import('../views/profile/ProfileView.vue')
const PortalHomeView = () => import('../views/home/PortalHomeView.vue')
// 2026-07-07: Offer 签署副本路由 (功能与 UI 暂与 PortalHomeView 一致, 后续改造)
const PortalHomeOfferView = () => import('../views/home/PortalHomeOfferView.vue')
const StudentPortalAuthView = () => import('../views/portal/StudentPortalAuthView.vue')
const StudentPortalApplicationV2View = () => import('../views/portal/StudentPortalApplicationV2View.vue')
const OfferConfirmView = () => import('../../offer_page/OfferConfirmView.vue')

const APP_TITLE = '上海人工智能实验室联培博士生申请系统'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: LoginView, meta: { public: true, title: '系统登录' } },
    { path: '/portal', component: StudentPortalAuthView, meta: { public: true, title: '博士生招生门户' } },
    { path: '/portal/home', component: PortalHomeView, meta: { public: true, portalProtected: true, title: '门户首页' } },
    { path: '/portal/home/offer', component: PortalHomeOfferView, meta: { public: true, portalProtected: true, title: 'Offer 签署 (待改造)' } },
    { path: '/portal/application', component: StudentPortalApplicationV2View, meta: { public: true, portalProtected: true, title: '博士研究生申请表' } },
    { path: '/offer/confirm', component: OfferConfirmView, meta: { public: true, title: '入营名单确认' } },
    { path: '/portal/applicationv2', redirect: '/portal/application', meta: { public: true, portalProtected: true } },
    {
      path: '/',
      component: AppLayout,
      children: [
        { path: '', redirect: '/portal' },
        { path: 'dashboard', component: DashboardView, meta: { title: '经营总览', requiredPermission: 'dashboard:read' } },
        { path: 'recruitment', component: RecruitmentWorkbenchView, meta: { title: '招生计划', section: 'plans', requiredPermission: 'recruitment_plan:read' } },
        { path: 'recruitment/registered-students', component: RegisteredStudentsView, meta: { title: '注册学生管理', section: 'portal-registrations', requiredPermission: 'recruitment_registered_students:read' } },
        { path: 'recruitment/news', component: NewsManagementView, meta: { title: '新闻管理', requiredPermission: 'news_management:read' } },
        { path: 'recruitment/advisor-screening', component: RecruitmentWorkbenchView, meta: { title: '导师初筛', section: 'advisor-screening', requiredPermission: 'recruitment_advisor_screening:read' } },
        { path: 'recruitment/initial-screening-confirmation', component: RecruitmentWorkbenchView, meta: { title: '初筛确认', section: 'initial-screening-confirmation', requiredPermission: 'recruitment_initial_screening_confirmation:read' } },
        { path: 'recruitment/camp-offers', component: CampOfferListView, meta: { title: '入营名单', requiredPermission: 'recruitment_camp_offer:read' } },
        { path: 'students', redirect: '/students/records' },
        { path: 'students/records', component: StudentsView, meta: { title: '学生主档', section: 'records', requiredPermission: 'students:read' } },
        { path: 'students/portal-registrations', redirect: '/recruitment/registered-students' },
        { path: 'students/centers', component: ResearchCentersView, meta: { title: '研究中心管理', requiredPermission: 'research_center:read' } },
        { path: 'training', redirect: '/training/plans' },
        { path: 'training/plans', component: TrainingView, meta: { title: '培养方案管理', section: 'plans', requiredPermission: 'training:read' } },
        { path: 'training/reports', component: TrainingView, meta: { title: '科研报告管理', section: 'reports', requiredPermission: 'training:read' } },
        { path: 'training/outbound', component: TrainingView, meta: { title: '外出研修管理', section: 'outbound', requiredPermission: 'training:read' } },
        { path: 'degree', redirect: '/degree/theses' },
        { path: 'degree/theses', component: DegreeView, meta: { title: '论文主档管理', section: 'theses', requiredPermission: 'degree:read' } },
        { path: 'degree/reviews', component: DegreeView, meta: { title: '盲审意见管理', section: 'reviews', requiredPermission: 'degree:read' } },
        { path: 'workflow/tasks', component: WorkflowCenterView, meta: { title: '审批中心', requiredPermission: 'workflow_center_menu:read' } },
        { path: 'system', redirect: '/system/users' },
        { path: 'system/users', component: SystemView, meta: { title: '系统用户管理', section: 'users', requiredPermission: 'system:read' } },
        { path: 'system/roles', component: SystemView, meta: { title: '角色权限管理', section: 'roles', requiredPermission: 'system:read' } },
        { path: 'system/dict-types', component: DictView, meta: { title: '字典类型管理', section: 'dict-types', requiredPermission: 'system:read' } },
        { path: 'system/dict-data', component: DictView, meta: { title: '字典数据管理', section: 'dict-data', requiredPermission: 'system:read' } },
        { path: 'system/audit', component: SystemView, meta: { title: '审计策略管理', section: 'audit', requiredPermission: 'audit:read' } },
        { path: 'system/integrations', component: SystemView, meta: { title: '集成链路管理', section: 'integrations', requiredPermission: 'system:read' } },
        { path: 'system/operation-logs', component: SystemView, meta: { title: '操作日志查询', section: 'operation-logs', requiredPermission: 'audit:read' } },
        { path: 'system/notification-logs', component: SystemView, meta: { title: '通知发送日志', section: 'notification-logs', requiredPermission: 'audit:read' } },
        { path: 'system/sync-logs', component: SystemView, meta: { title: '同步日志查询', section: 'sync-logs', requiredPermission: 'audit:read' } },
        { path: 'profile', component: ProfileView, meta: { title: '个人空间' } },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  if (to.path === '/') {
    return { path: '/portal' }
  }

  const authStore = useAuthStore()
  const hasAccessToken = Boolean(localStorage.getItem('dtlms-access-token'))
  const hasPortalToken = Boolean(localStorage.getItem('dtlms-portal-access-token'))
  const hasPortalImpersonationCode = typeof to.query.impersonation_code === 'string' && to.query.impersonation_code.trim().length > 0

  if (to.meta.portalProtected || to.path === '/portal') {
    if (!hasPortalToken) {
      if (to.meta.portalProtected) {
        return { path: '/portal' }
      }
    } else if (!hasPortalImpersonationCode) {
      try {
        await getPortalProfile()
        if (to.path === '/portal') {
          return '/portal/home'
        }
      } catch {
        clearPortalToken()
        if (to.meta.portalProtected) {
          return { path: '/portal' }
        }
      }
    }
  }

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
    return resolveAccessibleRoutePath(authStore.consumeRedirectTarget() || queryRedirect, authStore.permissions)
  }

  const requiredPermission = typeof to.meta.requiredPermission === 'string' ? to.meta.requiredPermission : ''
  if (requiredPermission && !hasGrantedPermission(authStore.permissions, requiredPermission)) {
    return { path: resolveFirstAccessibleMenuPath(authStore.permissions) }
  }

  return true
})

router.afterEach((to) => {
  const moduleTitle = String(to.meta.title || '首页')
  document.title = `${APP_TITLE}-${moduleTitle}`
})

export default router
