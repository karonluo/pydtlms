import type { PagedResponse, PaginationParams, SelectOption } from './common'
import type { RegisteredPortalStudentExportJobCreateResponse, RegisteredPortalStudentExportRequest } from './students'
import type {
  PortalAchievementRecordItem,
  PortalApplicantProfileData,
  PortalApplicationDeclarationData,
  PortalApplicationPreferenceItem,
  PortalEducationExperienceItem,
  PortalEnglishProficiencyItem,
  PortalFamilyMemberItem,
  PortalPersonalStatementData,
  PortalPracticeExperienceItem,
} from './portal'
import http from './http'


export type RecruitPlanRecord = {
  id: number
  plan_name: string
  academic_term: string
  academic_year: string
  semester: string
  application_count: number
  brochure_image_url?: string | null
  plan_description?: string | null
}


export type RecruitPlanUpsert = Omit<RecruitPlanRecord, 'id' | 'academic_term' | 'application_count'>


export type BackgroundAssessmentRecord = {
  evaluator_user_id?: number | null
  evaluator_username: string
  evaluator_name?: string | null
  evaluator_role_code: string
  assessment_result: string
  assessment_comment?: string | null
  assessed_at?: string | null
}

export type QualificationReviewHistoryRecord = {
  reviewer_username: string
  reviewer_name?: string | null
  reviewer_role_code?: string | null
  action: string
  action_label: string
  review_comment?: string | null
  reviewed_at?: string | null
}


export type RecruitApplicationRecord = {
  id: number
  plan_id: number
  business_key: string
  portal_student_id?: number | null
  candidate_no?: string | null
  review_round?: string | null
  student_name: string
  first_choice?: string | null
  second_choice?: string | null
  gender?: string | null
  political_status?: string | null
  marital_status?: string | null
  religious_belief?: string | null
  native_place?: string | null
  phone_number?: string | null
  email?: string | null
  mailing_address?: string | null
  id_type?: string | null
  id_number?: string | null
  graduation_school: string
  undergraduate_school?: string | null
  accept_adjustment?: string | null
  undergraduate_average_score?: string | null
  undergraduate_gpa?: string | null
  undergraduate_rank?: string | null
  undergraduate_major?: string | null
  graduate_average_score?: string | null
  graduate_gpa?: string | null
  graduate_rank?: string | null
  graduate_major?: string | null
  highest_degree: string
  intended_field: string
  intended_advisor_name?: string | null
  discovery_channel?: string | null
  source_channel?: string | null
  source_channel_other?: string | null
  graduate_school?: string | null
  overseas_university_name?: string | null
  overseas_master_university_name?: string | null
  self_evaluation?: string | null
  applied_at?: string | null
  research_problem?: string | null
  research_status_analysis?: string | null
  research_impact?: string | null
  ai_society_impact?: string | null
  dissenting_view?: string | null
  family_info?: string | null
  education_experience?: string | null
  practice_experience?: string | null
  personal_statement_text?: string | null
  student_activity_experience?: string | null
  personal_statement_attachment?: string | null
  material_list_attachment?: string | null
  material_list_attachment_name?: string | null
  supplementary_profile?: string | null
  material_status: string
  application_status: string
  advisor_screening_status?: string | null
  advisor_screening_round?: string | null
  first_choice_screening_batch_id?: number | null
  second_choice_screening_batch_id?: number | null
  first_choice_screening_submitted_at?: string | null
  second_choice_screening_submitted_at?: string | null
  first_choice_screening_score?: number | null
  second_choice_screening_score?: number | null
  initial_screening_status?: string | null
  initial_screening_result?: string | null
  initial_screening_confirmed_at?: string | null
  initial_screening_confirmer_username?: string | null
  initial_screening_confirmer_name?: string | null
  initial_screening_notification_status?: string | null
  initial_screening_notification_sent_at?: string | null
  next_stage_name?: string | null
  reviewer_name?: string | null
  final_score?: number | null
  background_assessments?: BackgroundAssessmentRecord[]
  profile?: PortalApplicantProfileData | null
  preferences?: PortalApplicationPreferenceItem[]
  education_experiences?: PortalEducationExperienceItem[]
  practice_experiences?: PortalPracticeExperienceItem[]
  english_proficiencies?: PortalEnglishProficiencyItem[]
  family_members?: PortalFamilyMemberItem[]
  achievement_records?: PortalAchievementRecordItem[]
  personal_statement?: PortalPersonalStatementData | null
  declaration?: PortalApplicationDeclarationData | null
}


export type RecruitApplicationUpsert = Omit<RecruitApplicationRecord, 'id' | 'business_key'> & {
  business_key?: string | null
}


export type RecruitPortalApplicationDetail = {
  application_id: number
  plan_id: number
  business_key: string
  candidate_no?: string | null
  student_name: string
  phone_number?: string | null
  email?: string | null
  id_number?: string | null
  application_status: string
  material_status: string
  advisor_screening_status?: string | null
  advisor_screening_round?: string | null
  advisor_screening_submitted_at?: string | null
  advisor_signature_base64?: string | null
  first_choice_screening_score?: number | null
  second_choice_screening_score?: number | null
  initial_screening_status?: string | null
  initial_screening_result?: string | null
  next_stage_name?: string | null
  reviewer_name?: string | null
  submitted_at?: string | null
  background_assessments?: BackgroundAssessmentRecord[]
  qualification_review_history?: QualificationReviewHistoryRecord[]
  profile?: PortalApplicantProfileData | null
  source_channel?: string | null
  source_channel_other?: string | null
  preferences?: PortalApplicationPreferenceItem[]
  education_experiences?: PortalEducationExperienceItem[]
  practice_experiences?: PortalPracticeExperienceItem[]
  english_proficiencies?: PortalEnglishProficiencyItem[]
  family_members?: PortalFamilyMemberItem[]
  achievement_records?: PortalAchievementRecordItem[]
  personal_statement?: PortalPersonalStatementData | null
  declaration?: PortalApplicationDeclarationData | null
}


export type RecruitPlanListResponse = PagedResponse<RecruitPlanRecord>


export type RecruitApplicationListResponse = PagedResponse<RecruitApplicationRecord>


export type RecruitApplicationImportIssue = {
  row_number: number
  student_name?: string | null
  reason: string
}


export type RecruitApplicationImportResult = {
  imported_count: number
  skipped_count: number
  plan_id: number
  imported_business_keys: string[]
  issues: RecruitApplicationImportIssue[]
}


export type AdvisorScreeningSubmitItem = {
  application_id: number
  advisor_score: number
}


export type AdvisorScreeningBatchSubmitRequest = {
  signature_base64: string
  items: AdvisorScreeningSubmitItem[]
}


export type AdvisorScreeningBatchSubmitResponse = {
  batch_id: number
  screening_round: string
  submitted_count: number
  applications: RecruitApplicationRecord[]
}


export type InitialScreeningConfirmationRequest = {
  result: 'passed' | 'rejected'
  comment?: string | null
}


export type RecruitmentBrochureUploadResponse = {
  url: string
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
    plan_description?: string | null
    application_count: number
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
  advisor_options: SelectOption[]
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


export function listRecruitmentPlans(params?: PaginationParams & { keyword?: string; semester?: string }) {
  return http.get<RecruitPlanListResponse>('/recruitment/plans', { params })
}


export function createRecruitmentPlan(payload: RecruitPlanUpsert) {
  return http.post<RecruitPlanRecord>('/recruitment/plans', payload)
}


export function updateRecruitmentPlan(id: number, payload: RecruitPlanUpsert) {
  return http.put<RecruitPlanRecord>(`/recruitment/plans/${id}`, payload)
}


export function deleteRecruitmentPlan(id: number) {
  return http.delete(`/recruitment/plans/${id}`)
}


export function listRecruitmentApplications(params?: PaginationParams & { keyword?: string; status?: string; plan_id?: number; portal_student_only?: boolean; advisor_names?: string }) {
  return http.get<RecruitApplicationListResponse>('/recruitment/applications', { params })
}


export function createRecruitmentApplication(payload: RecruitApplicationUpsert) {
  return http.post<RecruitApplicationRecord>('/recruitment/applications', payload)
}


export function getRecruitmentApplicationDetail(id: number) {
  return http.get<RecruitApplicationRecord>(`/recruitment/applications/${id}`)
}


export function getRecruitmentPortalApplicationDetail(id: number) {
  return http.get<RecruitPortalApplicationDetail>(`/recruitment/applications/${id}/portal-detail`)
}


export function updateRecruitmentApplication(id: number, payload: RecruitApplicationUpsert) {
  return http.put<RecruitApplicationRecord>(`/recruitment/applications/${id}`, payload)
}


export function deleteRecruitmentApplication(id: number) {
  return http.delete(`/recruitment/applications/${id}`)
}


export function submitAdvisorScreeningBatch(payload: AdvisorScreeningBatchSubmitRequest) {
  return http.post<AdvisorScreeningBatchSubmitResponse>('/recruitment/applications/advisor-screening:submit', payload)
}


export function confirmInitialScreening(applicationId: number, payload: InitialScreeningConfirmationRequest) {
  return http.post<RecruitApplicationRecord>(`/recruitment/applications/${applicationId}/initial-screening-confirmation`, payload)
}


export function importRecruitmentApplications(planId: number, file: File) {
  const formData = new FormData()
  formData.append('plan_id', String(planId))
  formData.append('file', file)
  return http.post<RecruitApplicationImportResult>('/recruitment/applications/import', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}


export function exportRecruitmentApplications(params?: { keyword?: string; status?: string; plan_id?: number; portal_student_only?: boolean; advisor_names?: string }) {
  return http.get<Blob>('/recruitment/applications/export', {
    params,
    responseType: 'blob',
  })
}


export function createAdvisorScreeningExportJob(payload: RegisteredPortalStudentExportRequest) {
  return http.post<RegisteredPortalStudentExportJobCreateResponse>('/recruitment/advisor-screening/export-jobs', payload)
}


export function downloadRecruitmentTemplate() {
  return http.get<Blob>('/recruitment/applications/template', {
    responseType: 'blob',
  })
}


export function uploadRecruitmentBrochureImage(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  return http.post<RecruitmentBrochureUploadResponse>('/recruitment/plans/brochure-upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}