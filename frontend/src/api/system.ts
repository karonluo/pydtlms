import http from './http'


export type SelectOption = {
  label: string
  value: string
}


export type PermissionOption = {
  code: string
  name: string
  module_name: string
  description: string
}


export type RoleRecord = {
  id: number
  role_code: string
  role_name: string
  scope_name: string
  permissions: string[]
  user_count: number
}


export type RoleUpsert = {
  role_code: string
  role_name: string
  scope_name: string
  permissions: string[]
}


export type SystemUserRecord = {
  id: number
  username: string
  full_name: string
  role_code: string
  role_name: string
  department_name: string
  phone_number?: string | null
  account_status: string
  last_login_at?: string | null
}


export type SystemUserUpsert = {
  username: string
  full_name: string
  role_code: string
  department_name: string
  phone_number?: string | null
  account_status: string
  password?: string | null
}


export type AuditPolicyRecord = {
  id: number
  item: string
  policy: string
  status: string
}


export type AuditPolicyUpsert = {
  item: string
  policy: string
  status: string
}


export type IntegrationRecord = {
  id: number
  name: string
  direction: string
  cadence: string
  status: string
  owner: string
}


export type IntegrationUpsert = {
  name: string
  direction: string
  cadence: string
  status: string
  owner: string
}


export type OperationLogRecord = {
  id: number
  operated_at: string
  operator_username: string
  module_name: string
  entity_name: string
  entity_id: string
  action: string
  result: string
  summary: string
}


export type SyncLogRecord = {
  id: number
  source_system: string
  target_system: string
  sync_status: string
  record_count: number
  executed_at: string
  failure_reason?: string | null
}


export type SystemStats = {
  integration_total: number
  active_integration_total: number
  operation_log_total: number
  sync_failure_total: number
  user_total: number
  role_total: number
}


export type SystemOptions = {
  account_status_options: SelectOption[]
  role_scope_options: SelectOption[]
  integration_direction_options: SelectOption[]
  integration_cadence_options: SelectOption[]
  integration_status_options: SelectOption[]
  audit_status_options: SelectOption[]
  operation_result_options: SelectOption[]
  sync_status_options: SelectOption[]
}


export type BulkActionResponse = {
  success_count: number
}


export function getSystemStats() {
  return http.get<SystemStats>('/system/stats')
}


export function getSystemOptions() {
  return http.get<SystemOptions>('/system/options')
}


export function getPermissionCatalog() {
  return http.get<{ items: PermissionOption[] }>('/system/permissions')
}


export function listSystemUsers(params?: {
  keyword?: string
  role_code?: string
  account_status?: string
  department_name?: string
}) {
  return http.get<{ items: SystemUserRecord[]; total: number }>('/system/users', { params })
}


export function createSystemUser(payload: SystemUserUpsert) {
  return http.post<SystemUserRecord>('/system/users', payload)
}


export function updateSystemUser(id: number, payload: SystemUserUpsert) {
  return http.put<SystemUserRecord>(`/system/users/${id}`, payload)
}


export function deleteSystemUser(id: number) {
  return http.delete(`/system/users/${id}`)
}


export function batchDeleteSystemUsers(ids: number[]) {
  return http.post<BulkActionResponse>('/system/users/batch-delete', { ids })
}


export function listRoles(params?: {
  keyword?: string
  scope_name?: string
  permission?: string
}) {
  return http.get<{ items: RoleRecord[]; total: number }>('/system/roles', { params })
}


export function createRole(payload: RoleUpsert) {
  return http.post<RoleRecord>('/system/roles', payload)
}


export function updateRole(id: number, payload: RoleUpsert) {
  return http.put<RoleRecord>(`/system/roles/${id}`, payload)
}


export function deleteRole(id: number) {
  return http.delete(`/system/roles/${id}`)
}


export function batchDeleteRoles(ids: number[]) {
  return http.post<BulkActionResponse>('/system/roles/batch-delete', { ids })
}


export function listAuditPolicies(params?: {
  keyword?: string
  status?: string
}) {
  return http.get<{ items: AuditPolicyRecord[]; total: number }>('/system/audit-policies', { params })
}


export function createAuditPolicy(payload: AuditPolicyUpsert) {
  return http.post<AuditPolicyRecord>('/system/audit-policies', payload)
}


export function updateAuditPolicy(id: number, payload: AuditPolicyUpsert) {
  return http.put<AuditPolicyRecord>(`/system/audit-policies/${id}`, payload)
}


export function deleteAuditPolicy(id: number) {
  return http.delete(`/system/audit-policies/${id}`)
}


export function batchDeleteAuditPolicies(ids: number[]) {
  return http.post<BulkActionResponse>('/system/audit-policies/batch-delete', { ids })
}


export function listIntegrations(params?: {
  keyword?: string
  status?: string
  direction?: string
}) {
  return http.get<{ items: IntegrationRecord[]; total: number }>('/system/integrations', { params })
}


export function createIntegration(payload: IntegrationUpsert) {
  return http.post<IntegrationRecord>('/system/integrations', payload)
}


export function updateIntegration(id: number, payload: IntegrationUpsert) {
  return http.put<IntegrationRecord>(`/system/integrations/${id}`, payload)
}


export function deleteIntegration(id: number) {
  return http.delete(`/system/integrations/${id}`)
}


export function batchDeleteIntegrations(ids: number[]) {
  return http.post<BulkActionResponse>('/system/integrations/batch-delete', { ids })
}


export function listOperationLogs(params?: {
  keyword?: string
  module_name?: string
  result?: string
}) {
  return http.get<{ items: OperationLogRecord[]; total: number }>('/system/operation-logs', { params })
}


export function listSyncLogs(params?: {
  keyword?: string
  sync_status?: string
  source_system?: string
}) {
  return http.get<{ items: SyncLogRecord[]; total: number }>('/system/sync-logs', { params })
}
