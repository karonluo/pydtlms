import http from './http'


export type SelectOption = {
  label: string
  value: string
  color_type?: string | null
  css_class?: string | null
}


export type TrainingStudentOption = {
  student_no: string
  student_name: string
  advisor_name: string
  label: string
}


export type TrainingPlanRecord = {
  id: number
  student_no: string
  student_name: string
  advisor_name: string
  version_no: string
  report_cycle: string
  plan_status: string
  scientific_goal: string
  assessment_rule: string
}


export type TrainingPlanUpsert = Omit<TrainingPlanRecord, 'id'>


export type ScientificReportRecord = {
  id: number
  student_no: string
  student_name: string
  period_label: string
  report_status: string
  reviewer_name?: string | null
  review_score?: number | null
  summary: string
}


export type ScientificReportUpsert = Omit<ScientificReportRecord, 'id'>


export type OutboundStudyRecord = {
  id: number
  student_no: string
  student_name: string
  advisor_name: string
  study_type: string
  destination: string
  start_date: string
  end_date: string
  approval_status: string
  expected_outcome?: string | null
}


export type OutboundStudyUpsert = Omit<OutboundStudyRecord, 'id'>


export type TrainingOptions = {
  plan_status_options: SelectOption[]
  report_cycle_options: SelectOption[]
  report_status_options: SelectOption[]
  study_type_options: SelectOption[]
  approval_status_options: SelectOption[]
  advisor_options: SelectOption[]
  reviewer_options: SelectOption[]
  student_options: TrainingStudentOption[]
}


export type TrainingStats = {
  training_plan_total: number
  pending_confirmation_total: number
  report_pending_total: number
  outbound_active_total: number
}


export function getTrainingStats() {
  return http.get<TrainingStats>('/training/stats')
}


export function getTrainingOptions() {
  return http.get<TrainingOptions>('/training/options')
}


export function listTrainingPlans(params?: { keyword?: string; plan_status?: string; advisor_name?: string; report_cycle?: string }) {
  return http.get<{ items: TrainingPlanRecord[]; total: number }>('/training/plans', { params })
}


export function createTrainingPlan(payload: TrainingPlanUpsert) {
  return http.post<TrainingPlanRecord>('/training/plans', payload)
}


export function updateTrainingPlan(id: number, payload: TrainingPlanUpsert) {
  return http.put<TrainingPlanRecord>(`/training/plans/${id}`, payload)
}


export function deleteTrainingPlan(id: number) {
  return http.delete(`/training/plans/${id}`)
}


export function batchDeleteTrainingPlans(ids: number[]) {
  return http.post<{ success_count: number }>('/training/plans/batch-delete', { ids })
}


export function listScientificReports(params?: { keyword?: string; status?: string; reviewer_name?: string }) {
  return http.get<{ items: ScientificReportRecord[]; total: number }>('/training/reports', { params })
}


export function createScientificReport(payload: ScientificReportUpsert) {
  return http.post<ScientificReportRecord>('/training/reports', payload)
}


export function updateScientificReport(id: number, payload: ScientificReportUpsert) {
  return http.put<ScientificReportRecord>(`/training/reports/${id}`, payload)
}


export function deleteScientificReport(id: number) {
  return http.delete(`/training/reports/${id}`)
}


export function batchDeleteScientificReports(ids: number[]) {
  return http.post<{ success_count: number }>('/training/reports/batch-delete', { ids })
}


export function listOutboundStudies(params?: { keyword?: string; status?: string; study_type?: string; advisor_name?: string }) {
  return http.get<{ items: OutboundStudyRecord[]; total: number }>('/training/outbound-studies', { params })
}


export function createOutboundStudy(payload: OutboundStudyUpsert) {
  return http.post<OutboundStudyRecord>('/training/outbound-studies', payload)
}


export function updateOutboundStudy(id: number, payload: OutboundStudyUpsert) {
  return http.put<OutboundStudyRecord>(`/training/outbound-studies/${id}`, payload)
}


export function deleteOutboundStudy(id: number) {
  return http.delete(`/training/outbound-studies/${id}`)
}


export function batchDeleteOutboundStudies(ids: number[]) {
  return http.post<{ success_count: number }>('/training/outbound-studies/batch-delete', { ids })
}
