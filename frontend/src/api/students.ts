import http from './http'


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


export type StudentManagementResponse = {
  items: StudentRecord[]
  total: number
}


export type StudentStats = {
  total_students: number
  active_students: number
  outbound_students: number
  thesis_students: number
  advisor_count: number
}


export function listStudents(params?: { keyword?: string; status?: string; advisor_name?: string }) {
  return http.get<StudentManagementResponse>('/students/management', { params })
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