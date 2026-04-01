import http from './http'


export type RoleRecord = {
  id: number
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
  department_name: string
  phone_number?: string | null
  account_status: string
}


export type AuditPolicyRecord = {
  id: number
  item: string
  policy: string
}


export type IntegrationRecord = {
  id: number
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


export function getSystemStats() {
  return http.get<SystemStats>('/system/stats')
}


export function listSystemUsers() {
  return http.get<{ items: SystemUserRecord[]; total: number }>('/system/users')
}


export function createSystemUser(payload: Omit<SystemUserRecord, 'id'>) {
  return http.post<SystemUserRecord>('/system/users', payload)
}


export function updateSystemUser(id: number, payload: Omit<SystemUserRecord, 'id'>) {
  return http.put<SystemUserRecord>(`/system/users/${id}`, payload)
}


export function listRoles() {
  return http.get<{ items: RoleRecord[]; total: number }>('/system/roles')
}


export function createRole(payload: Omit<RoleRecord, 'id'>) {
  return http.post<RoleRecord>('/system/roles', payload)
}


export function updateRole(id: number, payload: Omit<RoleRecord, 'id'>) {
  return http.put<RoleRecord>(`/system/roles/${id}`, payload)
}


export function listAuditPolicies() {
  return http.get<{ items: AuditPolicyRecord[]; total: number }>('/system/audit-policies')
}


export function createAuditPolicy(payload: Omit<AuditPolicyRecord, 'id'>) {
  return http.post<AuditPolicyRecord>('/system/audit-policies', payload)
}


export function updateAuditPolicy(id: number, payload: Omit<AuditPolicyRecord, 'id'>) {
  return http.put<AuditPolicyRecord>(`/system/audit-policies/${id}`, payload)
}


export function listIntegrations() {
  return http.get<{ items: IntegrationRecord[]; total: number }>('/system/integrations')
}


export function createIntegration(payload: Omit<IntegrationRecord, 'id'>) {
  return http.post<IntegrationRecord>('/system/integrations', payload)
}


export function updateIntegration(id: number, payload: Omit<IntegrationRecord, 'id'>) {
  return http.put<IntegrationRecord>(`/system/integrations/${id}`, payload)
}


export function listOperationLogs() {
  return http.get<{ items: OperationLogRecord[]; total: number }>('/system/operation-logs')
}


export function listSyncLogs() {
  return http.get<{ items: SyncLogRecord[]; total: number }>('/system/sync-logs')
}
