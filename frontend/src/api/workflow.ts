import type { PagedResponse, PaginationParams, SelectOption } from './common'
import http from './http'


export type WorkflowActionOption = {
  action: string
  label: string
}


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
  available_actions: WorkflowActionOption[]
  process_definition_key?: string | null
  process_definition_id?: string | null
  process_instance_id?: string | null
  execution_id?: string | null
  task_definition_key?: string | null
}


export type WorkflowTaskUpsert = Omit<
  WorkflowTaskRecord,
  'id' | 'available_actions' | 'process_definition_key' | 'process_definition_id' | 'process_instance_id' | 'execution_id' | 'task_definition_key'
>


export type WorkflowStats = {
  todo_total: number
  in_progress_total: number
  approved_total: number
  rejected_total: number
  overdue_total: number
}


export type WorkflowOptions = {
  workflow_name_options: SelectOption[]
  business_module_options: SelectOption[]
  applicant_options: SelectOption[]
  handler_options: SelectOption[]
  current_node_options: SelectOption[]
  priority_options: SelectOption[]
  status_options: SelectOption[]
}


export type WorkflowTaskActionLog = {
  operated_at: string
  operator_username: string
  operator_full_name: string
  action: string
  action_label: string
  from_node: string
  to_node?: string | null
  result_status: string
  comment?: string | null
}


export type WorkflowTaskDetailResponse = {
  task: WorkflowTaskRecord
  history: WorkflowTaskActionLog[]
}


export type WorkflowTaskActionRequest = {
  action: string
  comment?: string | null
}


export function getWorkflowStats() {
  return http.get<WorkflowStats>('/workflow/stats')
}


export function getWorkflowOptions() {
  return http.get<WorkflowOptions>('/workflow/options')
}


export function listWorkflowTasks(params?: PaginationParams & { keyword?: string; status?: string; module?: string }) {
  return http.get<PagedResponse<WorkflowTaskRecord>>('/workflow/tasks', { params })
}


export function getWorkflowTaskDetail(id: number) {
  return http.get<WorkflowTaskDetailResponse>(`/workflow/tasks/${id}`)
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


export function executeWorkflowTaskAction(id: number, payload: WorkflowTaskActionRequest) {
  return http.post<WorkflowTaskDetailResponse>(`/workflow/tasks/${id}/actions`, payload)
}
