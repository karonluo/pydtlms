export type MenuAccessEntry = {
  path: string
  requiredPermission: string
}

export const MENU_ACCESS_ENTRIES: MenuAccessEntry[] = [
  { path: '/dashboard', requiredPermission: 'dashboard:read' },
  { path: '/workflow/tasks', requiredPermission: 'workflow_center_menu:read' },
  { path: '/recruitment', requiredPermission: 'recruitment_plan:read' },
  { path: '/recruitment/registered-students', requiredPermission: 'recruitment_registered_students:read' },
  { path: '/recruitment/advisor-screening', requiredPermission: 'recruitment_advisor_screening:read' },
  { path: '/recruitment/initial-screening-confirmation', requiredPermission: 'recruitment_initial_screening_confirmation:read' },
  { path: '/students/records', requiredPermission: 'students:read' },
  { path: '/students/centers', requiredPermission: 'students:read' },
  { path: '/training/plans', requiredPermission: 'training:read' },
  { path: '/training/reports', requiredPermission: 'training:read' },
  { path: '/training/outbound', requiredPermission: 'training:read' },
  { path: '/degree/theses', requiredPermission: 'degree:read' },
  { path: '/degree/reviews', requiredPermission: 'degree:read' },
  { path: '/system/users', requiredPermission: 'system:read' },
  { path: '/system/roles', requiredPermission: 'system:read' },
  { path: '/system/audit', requiredPermission: 'audit:read' },
  { path: '/system/integrations', requiredPermission: 'system:read' },
  { path: '/system/dict-types', requiredPermission: 'system:read' },
  { path: '/system/dict-data', requiredPermission: 'system:read' },
  { path: '/system/operation-logs', requiredPermission: 'audit:read' },
  { path: '/system/notification-logs', requiredPermission: 'audit:read' },
  { path: '/system/sync-logs', requiredPermission: 'audit:read' },
]

const MENU_ACCESS_BY_PATH = new Map(MENU_ACCESS_ENTRIES.map((item) => [item.path, item.requiredPermission]))

export function hasGrantedPermission(permissions: string[], requiredPermission?: string) {
  if (!requiredPermission) {
    return true
  }
  const grantedPermissions = new Set(permissions)
  return grantedPermissions.has('*') || grantedPermissions.has(requiredPermission)
}

export function resolveFirstAccessibleMenuPath(permissions: string[]) {
  return MENU_ACCESS_ENTRIES.find((item) => hasGrantedPermission(permissions, item.requiredPermission))?.path || '/profile'
}

export function resolveAccessibleRoutePath(target: string, permissions: string[]) {
  const normalizedTarget = String(target || '').trim()
  const targetPath = normalizedTarget.split('?')[0]?.split('#')[0] || ''
  const requiredPermission = MENU_ACCESS_BY_PATH.get(targetPath)
  if (!normalizedTarget || normalizedTarget === '/login' || normalizedTarget.startsWith('/portal')) {
    return resolveFirstAccessibleMenuPath(permissions)
  }
  if (requiredPermission && !hasGrantedPermission(permissions, requiredPermission)) {
    return resolveFirstAccessibleMenuPath(permissions)
  }
  return normalizedTarget
}