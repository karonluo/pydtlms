import type { BulkActionResponse, PagedResponse, PaginationParams, SelectOption } from './common'
import http from './http'


const CENTER_MUTATION_TIMEOUT = 30000


export type { BulkActionResponse, PagedResponse, PaginationParams, SelectOption } from './common'


export type StudentRecord = {
  id: number
  student_no: string
  full_name: string
  status: string
  advisor_name: string
  advisor_id?: number | null
  center_name: string
  degree_type: string
  enrollment_year: number
  phone_number?: string | null
  political_status?: string | null
}


export type StudentUpsert = {
  student_no: string
  full_name: string
  status: string
  advisor_name?: string | null
  advisor_id?: string | number | null
  center_name: string
  degree_type: string
  enrollment_year: number
  phone_number?: string | null
  political_status?: string | null
}


export type StudentManagementResponse = PagedResponse<StudentRecord>


export type RegisteredPortalStudentRecord = {
  id: number
  full_name: string
  phone_number: string
  email: string
  id_number: string
  account_status: string
  application_form_status: string
  selected_plan_name?: string | null
  selected_center_name?: string | null
  selected_advisor_name?: string | null
  recruitment_application_id?: number | null
  recruitment_application_business_key?: string | null
  recruitment_application_status?: string | null
  registered_at?: string | null
  submitted_at?: string | null
}


export type RegisteredPortalStudentListResponse = PagedResponse<RegisteredPortalStudentRecord>


export type RegisteredPortalStudentActionResponse = {
  message: string
  account_status?: string | null
  email_sent?: boolean | null
  temporary_password?: string | null
}


export type RegisteredPortalStudentEmailRequest = {
  subject: string
  content: string
}


export type CenterRecord = {
  id: number
  center_name: string
  director_name: string
  director_id?: number | null
  advisor_names: string[]
  advisor_ids: number[]
  is_enabled: boolean
  created_date?: string | null
  member_student_count: number
  active_student_count: number
}


export type CenterUpsert = {
  center_name: string
  director_name?: string | null
  director_id?: string | number | null
  advisor_names?: string[]
  advisor_ids: Array<string | number>
  is_enabled: boolean
  created_date?: string | null
}


export type CenterListResponse = PagedResponse<CenterRecord>


export type CenterAdvisorMapItem = {
  center_name: string
  advisors: SelectOption[]
}


export type StudentOptions = {
  status_options: SelectOption[]
  degree_options: SelectOption[]
  advisor_options: SelectOption[]
  center_options: SelectOption[]
  political_status_options: SelectOption[]
  center_advisor_map: CenterAdvisorMapItem[]
}


export type StudentStats = {
  total_students: number
  active_students: number
  outbound_students: number
  thesis_students: number
  advisor_count: number
  center_total: number
  enabled_center_total: number
  registered_portal_total: number
  portal_submitted_total: number
  portal_unsubmitted_total: number
}


export function listStudents(params?: PaginationParams & { keyword?: string; status?: string; advisor_name?: string; center_name?: string }) {
  return http.get<StudentManagementResponse>('/students/management', { params })
}


export function getStudentOptions() {
  return http.get<StudentOptions>('/students/options')
}


export function listRegisteredPortalStudents(params?: PaginationParams & { keyword?: string; application_form_status?: string }) {
  return http.get<RegisteredPortalStudentListResponse>('/students/portal-registrations', { params })
}


export function deactivateRegisteredPortalStudent(id: number) {
  return http.post<RegisteredPortalStudentActionResponse>(`/students/portal-registrations/${id}/deactivate`)
}


export function activateRegisteredPortalStudent(id: number) {
  return http.post<RegisteredPortalStudentActionResponse>(`/students/portal-registrations/${id}/activate`)
}


export function resetRegisteredPortalStudentPassword(id: number) {
  return http.post<RegisteredPortalStudentActionResponse>(`/students/portal-registrations/${id}/reset-password`)
}


export function sendRegisteredPortalStudentEmail(id: number, payload: RegisteredPortalStudentEmailRequest) {
  return http.post<RegisteredPortalStudentActionResponse>(`/students/portal-registrations/${id}/send-email`, payload)
}


export function getStudentStats() {
  return http.get<StudentStats>('/students/management/stats')
}


export function createStudent(payload: StudentUpsert) {
  return http.post<StudentRecord>('/students/management', payload)
}


export function updateStudent(id: number, payload: StudentUpsert) {
  return http.put<StudentRecord>(`/students/management/${id}`, payload)
}


export function deleteStudent(id: number) {
  return http.delete(`/students/management/${id}`)
}


export function listCenters(params?: PaginationParams & {
  keyword?: string
  is_enabled?: boolean
  director_id?: string | number
}) {
  return http.get<CenterListResponse>('/students/centers', { params })
}


export function createCenter(payload: CenterUpsert) {
  return http.post<CenterRecord>('/students/centers', payload, { timeout: CENTER_MUTATION_TIMEOUT })
}


export function updateCenter(id: number, payload: CenterUpsert) {
  return http.put<CenterRecord>(`/students/centers/${id}`, payload, { timeout: CENTER_MUTATION_TIMEOUT })
}


export function deleteCenter(id: number) {
  return http.delete(`/students/centers/${id}`)
}


export function batchDeleteCenters(ids: number[]) {
  return http.post<BulkActionResponse>('/students/centers/batch-delete', { ids })
}