import axios from 'axios'

import type { SelectOption } from './common'

const PORTAL_TOKEN_KEY = 'dtlms-portal-access-token'
const PORTAL_LONG_RUNNING_TIMEOUT = 60000

export type PortalApplicantProfileData = {
  full_name_pinyin?: string | null
  profile_photo_url?: string | null
  id_card_collage_url?: string | null
  gender?: string | null
  birth_date?: string | null
  ethnic_group?: string | null
  native_place?: string | null
  political_status?: string | null
  marital_status?: string | null
  religious_belief?: string | null
  id_type?: string | null
  mailing_address?: string | null
  emergency_contact_name?: string | null
  emergency_contact_phone?: string | null
}

export type PortalApplicationPreferenceItem = {
  preference_order: number
  research_center_name: string
  advisor_name?: string | null
  is_optional: boolean
}

export type PortalEducationExperienceItem = {
  sort_order: number
  education_stage: string
  start_month?: string | null
  end_month?: string | null
  school_name: string
  major_name?: string | null
  average_score?: string | null
  gpa?: string | null
  ranking?: string | null
  verifier_name?: string | null
  verifier_phone?: string | null
  transcript_attachment_url?: string | null
  transcript_attachment_name?: string | null
  degree_certificate_attachment_url?: string | null
  degree_certificate_attachment_name?: string | null
}

export type PortalPracticeExperienceItem = {
  start_month?: string | null
  end_month?: string | null
  organization_name: string
  position_name?: string | null
  responsibility_text?: string | null
  verifier_name?: string | null
  verifier_phone?: string | null
}

export type PortalEnglishProficiencyItem = {
  exam_name: string
  score_text?: string | null
  certificate_attachment_url?: string | null
  certificate_attachment_name?: string | null
}

export type PortalFamilyMemberItem = {
  member_name: string
  relation_type: string
  employer_name?: string | null
  job_title?: string | null
  contact_phone?: string | null
}

export type PortalAchievementRecordItem = {
  achievement_type: string
  achievement_month?: string | null
  paper_title?: string | null
  author_order?: string | null
  journal_or_conference?: string | null
  publish_or_index_month?: string | null
  award_name?: string | null
  award_rank?: string | null
  award_certificate_attachment_url?: string | null
  award_certificate_attachment_name?: string | null
  awarding_organization?: string | null
  award_level?: string | null
  award_year?: string | null
  description_text?: string | null
  responsibility_text?: string | null
}

export type PortalPersonalStatementData = {
  personal_statement_text?: string | null
  ai_problem_statement?: string | null
  ai_industry_opinion?: string | null
  growth_experience_text?: string | null
  program_application_reason_text?: string | null
  career_plan_text?: string | null
  resume_attachment_url?: string | null
  resume_attachment_name?: string | null
  supporting_material_attachment_url?: string | null
  supporting_material_attachment_name?: string | null
}

export type PortalApplicationDeclarationData = {
  has_read_declaration: boolean
  declaration_text?: string | null
  progress_snapshot?: Record<string, unknown> | null
}

export type PortalApplicationDraftRecord = {
  selected_plan_id?: number | null
  source_channel?: string | null
  source_channel_other?: string | null
  preferences: PortalApplicationPreferenceItem[]
  education_experiences: PortalEducationExperienceItem[]
  practice_experiences: PortalPracticeExperienceItem[]
  english_proficiencies: PortalEnglishProficiencyItem[]
  family_members: PortalFamilyMemberItem[]
  achievement_records: PortalAchievementRecordItem[]
  personal_statement: PortalPersonalStatementData
  declaration: PortalApplicationDeclarationData
  submitted_at?: string | null
}

export type PortalStudentRecord = {
  id: number
  full_name: string
  phone_number: string
  email: string
  id_number: string
  business_key?: string | null
  candidate_no?: string | null
  account_status?: string | null
  gender?: string | null
  birth_date?: string | null
  ethnic_group?: string | null
  native_place?: string | null
  marital_status?: string | null
  religious_belief?: string | null
  id_type?: string | null
  mailing_address?: string | null
  graduation_school?: string | null
  highest_degree?: string | null
  intended_field?: string | null
  political_status?: string | null
  english_level?: string | null
  family_info?: string | null
  education_experience?: string | null
  practice_experience?: string | null
  personal_profile?: string | null
  recommendation_notes?: string | null
  personal_statement_text?: string | null
  material_list_attachment?: string | null
  material_list_attachment_name?: string | null
  signed_agreement?: boolean
  selected_plan_id?: number | null
  selected_team_name?: string | null
  selected_advisor_name?: string | null
  self_evaluation?: string | null
  submitted_at?: string | null
  profile?: PortalApplicantProfileData | null
  application_draft?: PortalApplicationDraftRecord | null
}

export type PortalRegistrationResponse = {
  message: string
  student: PortalStudentRecord
}

export type PortalSessionResponse = {
  access_token: string
  token_type: string
  student: PortalStudentRecord
}

export type PortalPlanRecord = {
  id: number
  plan_name: string
  academic_term: string
  brochure_image_url?: string | null
  summary?: string | null
}

export type PortalProfileOptionsResponse = {
  political_status_options: SelectOption[]
  ethnic_group_options: SelectOption[]
}

export type PortalPublicConfigResponse = {
  portal_admissions_info_url: string
  portal_application_v2_blocked: boolean
  portal_application_v2_block_message: string
}

export type PortalTeamRecord = {
  id: number
  team_name: string
  lead_advisor_name: string
  advisor_names: string[]
  department_name: string
  discipline_name: string
  research_directions: string[]
  description?: string | null
}

export type PortalRegistrationRequest = {
  phone_number: string
  email: string
  full_name: string
  id_number: string
  password: string
  email_verification_code: string
}

export type PortalRegistrationEmailCodeRequest = {
  email: string
}

export type PortalRegistrationEmailCodeResponse = {
  message: string
  expires_in_seconds: number
  cooldown_seconds: number
}

export type PortalLoginRequest = {
  account: string
  password: string
}

export type PortalLoginEmailCodeRequest = {
  email: string
}

export type PortalEmailCodeLoginRequest = {
  email: string
  email_verification_code: string
}

export type PortalPasswordResetRequest = {
  account: string
  id_number: string
  new_password: string
}

export type PortalPasswordChangeRequest = {
  current_password: string
  new_password: string
}

export type PortalApplicationUpsert = {
  plan_id: number
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
  gender?: string | null
  birth_date?: string | null
  ethnic_group?: string | null
  native_place?: string | null
  marital_status?: string | null
  religious_belief?: string | null
  id_type?: string | null
  mailing_address?: string | null
  graduation_school?: string | null
  highest_degree?: string | null
  intended_field?: string | null
  political_status?: string | null
  english_level?: string | null
  family_info?: string | null
  education_experience?: string | null
  practice_experience?: string | null
  personal_profile?: string | null
  material_list_attachment?: string | null
  recommendation_notes?: string | null
  personal_statement_text?: string | null
  signed_agreement?: boolean
  selected_team_name?: string | null
  selected_advisor_name?: string | null
  self_evaluation?: string | null
}

export type PortalApplicationSubmissionResponse = {
  student: PortalStudentRecord
  application_business_key: string
  application_status: string
}

export type PortalApplicationDraftSaveResponse = {
  message: string
  student: PortalStudentRecord
}

export type PortalAttachmentCategory =
  | 'education_transcript'
  | 'education_degree_certificate'
  | 'english_certificate'
  | 'achievement_award_certificate'
  | 'profile_photo'
  | 'id_card_collage'
  | 'resume'
  | 'supporting_material'

export type PortalAttachmentUploadResponse = {
  category: PortalAttachmentCategory
  file_name: string
  file_type?: string | null
  file_size: number
  url: string
}

const portalHttp = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 10000,
})

const PORTAL_EMAIL_REQUEST_TIMEOUT_MS = 60000

portalHttp.interceptors.request.use((config) => {
  const token = localStorage.getItem(PORTAL_TOKEN_KEY)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

portalHttp.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(PORTAL_TOKEN_KEY)
    }
    return Promise.reject(error)
  },
)

export function getPortalToken() {
  return localStorage.getItem(PORTAL_TOKEN_KEY) || ''
}

export function setPortalToken(token: string) {
  localStorage.setItem(PORTAL_TOKEN_KEY, token)
}

export function clearPortalToken() {
  localStorage.removeItem(PORTAL_TOKEN_KEY)
}

export function registerPortalStudent(payload: PortalRegistrationRequest) {
  return portalHttp.post<PortalRegistrationResponse>('/portal/register', payload)
}

export function sendPortalRegistrationEmailCode(payload: PortalRegistrationEmailCodeRequest) {
  return portalHttp.post<PortalRegistrationEmailCodeResponse>('/portal/register/email-code', payload, {
    timeout: PORTAL_EMAIL_REQUEST_TIMEOUT_MS,
  })
}

export function loginPortalStudent(payload: PortalLoginRequest) {
  return portalHttp.post<PortalSessionResponse>('/portal/login', payload)
}

export function sendPortalLoginEmailCode(payload: PortalLoginEmailCodeRequest) {
  return portalHttp.post<PortalRegistrationEmailCodeResponse>('/portal/login/email-code/send', payload, {
    timeout: PORTAL_EMAIL_REQUEST_TIMEOUT_MS,
  })
}

export function loginPortalStudentByEmailCode(payload: PortalEmailCodeLoginRequest) {
  return portalHttp.post<PortalSessionResponse>('/portal/login/email-code', payload)
}

export function resetPortalStudentPassword(payload: PortalPasswordResetRequest) {
  return portalHttp.post<{ message: string }>('/portal/forgot-password', payload)
}


export function changePortalStudentPassword(payload: PortalPasswordChangeRequest) {
  return portalHttp.post<{ message: string }>('/portal/change-password', payload)
}

export function getPortalProfile() {
  return portalHttp.get<PortalStudentRecord>('/portal/me')
}

export function getPortalProfileOptions() {
  return portalHttp.get<PortalProfileOptionsResponse>('/portal/profile-options')
}

export function getPortalPublicConfig() {
  return portalHttp.get<PortalPublicConfigResponse>('/portal/public-config')
}

export function listPortalPlans() {
  return portalHttp.get<{ items: PortalPlanRecord[] }>('/portal/plans')
}

export function listPortalTeams() {
  return portalHttp.get<{ items: PortalTeamRecord[] }>('/portal/teams')
}

export function submitPortalApplication(payload: PortalApplicationUpsert) {
  return portalHttp.post<PortalApplicationSubmissionResponse>('/portal/applications', payload, {
    timeout: PORTAL_LONG_RUNNING_TIMEOUT,
  })
}

export function savePortalApplicationDraft(payload: PortalApplicationUpsert) {
  return portalHttp.post<PortalApplicationDraftSaveResponse>('/portal/applications/draft', payload, {
    timeout: PORTAL_LONG_RUNNING_TIMEOUT,
  })
}

export function uploadPortalAttachment(file: File, category: PortalAttachmentCategory) {
  const formData = new FormData()
  formData.append('category', category)
  formData.append('file', file)
  return portalHttp.post<PortalAttachmentUploadResponse>('/portal/attachments/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}
