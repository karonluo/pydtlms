import http from './http'


export type WorkflowTaskRecord = {
  id: number
  workflow_name: string
  business_module: string
  business_key: string
  title: string
  applicant_name: string
  current_handler: string
  current_node: string
  priority: string
  status: string
  created_at: string
  due_at: string
  form_summary: string
  latest_comment?: string | null
}


export type WorkflowTaskUpsert = Omit<WorkflowTaskRecord, 'id'>


export type WorkflowStats = {
  todo_total: number
  in_progress_total: number
  approved_total: number
  rejected_total: number
  overdue_total: number
}


export function getWorkflowStats() {
  return http.get<WorkflowStats>('/workflow/stats')
}


export function listWorkflowTasks(params?: { status?: string; module?: string }) {
  return http.get<{ items: WorkflowTaskRecord[]; total: number }>('/workflow/tasks', { params })
}


export function createWorkflowTask(payload: WorkflowTaskUpsert) {
  return http.post<WorkflowTaskRecord>('/workflow/tasks', payload)
}


export function updateWorkflowTask(id: number, payload: WorkflowTaskUpsert) {
  return http.put<WorkflowTaskRecord>(`/workflow/tasks/${id}`, payload)
}


export function deleteWorkflowTask(id: number) {
  return http.delete(`/workflow/tasks/${id}`)
}
