import http from './http'
import type { SelectOption } from './students'


export type RecruitPlanRecord = {
  id: number
  plan_name: string
  academic_term: string
  academic_year: string
  semester: string
  current_stage: string
  target_quota: number
  application_count: number
  interview_group_count: number
  is_open: boolean
}


export type RecruitPlanUpsert = Omit<RecruitPlanRecord, 'id' | 'academic_term' | 'application_count'>


export type RecruitApplicationRecord = {
  id: number
  plan_id: number
  candidate_no: string
  student_name: string
  graduation_school: string
  highest_degree: string
  intended_field: string
  material_status: string
  application_status: string
  reviewer_name?: string | null
  final_score?: number | null
}


export type RecruitApplicationUpsert = Omit<RecruitApplicationRecord, 'id'>


export type RecruitPlanListResponse = {
  items: RecruitPlanRecord[]
  total: number
}


export type RecruitApplicationListResponse = {
  items: RecruitApplicationRecord[]
  total: number
}


export type RecruitStats = {
  plan_count: number
  open_plan_count: number
  application_total: number
  pending_review_total: number
  pre_admit_total: number
}


export type RecruitWorkbench = {
  plans: Array<{
    plan_name: string
    academic_term: string
    current_stage: string
    application_count: number
    interview_group_count: number
  }>
  pipeline: Array<{
    stage: string
    count: number
    status: string
  }>
  pending_tasks: Array<{
    title: string
    owner: string
    due_text: string
  }>
}


export type RecruitmentOptions = {
  semester_options: SelectOption[]
  plan_stage_options: SelectOption[]
  degree_options: SelectOption[]
  material_status_options: SelectOption[]
  application_status_options: SelectOption[]
  intended_field_options: SelectOption[]
  reviewer_options: SelectOption[]
  graduation_school_options: SelectOption[]
}


export function getRecruitmentStats() {
  return http.get<RecruitStats>('/recruitment/stats')
}


export function getRecruitmentOptions() {
  return http.get<RecruitmentOptions>('/recruitment/options')
}


export function getRecruitmentWorkbench() {
  return http.get<RecruitWorkbench>('/recruitment/workbench')
}


export function listRecruitmentPlans() {
  return http.get<RecruitPlanListResponse>('/recruitment/plans')
}


export function createRecruitmentPlan(payload: RecruitPlanUpsert) {
  return http.post<RecruitPlanRecord>('/recruitment/plans', payload)
}


export function updateRecruitmentPlan(id: number, payload: RecruitPlanUpsert) {
  return http.put<RecruitPlanRecord>(`/recruitment/plans/${id}`, payload)
}


export function listRecruitmentApplications(params?: { keyword?: string; status?: string; plan_id?: number }) {
  return http.get<RecruitApplicationListResponse>('/recruitment/applications', { params })
}


export function createRecruitmentApplication(payload: RecruitApplicationUpsert) {
  return http.post<RecruitApplicationRecord>('/recruitment/applications', payload)
}


export function updateRecruitmentApplication(id: number, payload: RecruitApplicationUpsert) {
  return http.put<RecruitApplicationRecord>(`/recruitment/applications/${id}`, payload)
}


export function deleteRecruitmentApplication(id: number) {
  return http.delete(`/recruitment/applications/${id}`)
}