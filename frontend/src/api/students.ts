import type { BulkActionResponse, PagedResponse, PaginationParams, SelectOption } from './common'
import http from './http'


export type { BulkActionResponse, PagedResponse, PaginationParams, SelectOption } from './common'


export type StudentRecord = {
  id: number
  student_no: string
  full_name: string
  status: string
  advisor_name: string
  team_name: string
  degree_type: string
  enrollment_year: number
  phone_number?: string | null
  political_status?: string | null
}


export type StudentUpsert = Omit<StudentRecord, 'id'>


export type StudentManagementResponse = PagedResponse<StudentRecord>


export type TeamRecord = {
  id: number
  team_code: string
  team_name: string
  department_name: string
  discipline_name: string
  lead_advisor_name: string
  advisor_names: string[]
  research_directions: string[]
  status: string
  established_on?: string | null
  description?: string | null
  member_student_count: number
  active_student_count: number
}


export type TeamUpsert = Omit<TeamRecord, 'id' | 'member_student_count' | 'active_student_count'>


export type TeamListResponse = PagedResponse<TeamRecord>


export type TeamAdvisorMapItem = {
  team_name: string
  advisors: SelectOption[]
}


export type StudentOptions = {
  status_options: SelectOption[]
  degree_options: SelectOption[]
  advisor_options: SelectOption[]
  team_options: SelectOption[]
  team_status_options: SelectOption[]
  political_status_options: SelectOption[]
  department_options: SelectOption[]
  discipline_options: SelectOption[]
  team_advisor_map: TeamAdvisorMapItem[]
}


export type StudentStats = {
  total_students: number
  active_students: number
  outbound_students: number
  thesis_students: number
  advisor_count: number
  team_total: number
  active_team_total: number
}


export function listStudents(params?: PaginationParams & { keyword?: string; status?: string; advisor_name?: string; team_name?: string }) {
  return http.get<StudentManagementResponse>('/students/management', { params })
}


export function getStudentOptions() {
  return http.get<StudentOptions>('/students/options')
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


export function listTeams(params?: PaginationParams & {
  keyword?: string
  status?: string
  department_name?: string
  lead_advisor_name?: string
}) {
  return http.get<TeamListResponse>('/students/teams', { params })
}


export function createTeam(payload: TeamUpsert) {
  return http.post<TeamRecord>('/students/teams', payload)
}


export function updateTeam(id: number, payload: TeamUpsert) {
  return http.put<TeamRecord>(`/students/teams/${id}`, payload)
}


export function deleteTeam(id: number) {
  return http.delete(`/students/teams/${id}`)
}


export function batchDeleteTeams(ids: number[]) {
  return http.post<BulkActionResponse>('/students/teams/batch-delete', { ids })
}