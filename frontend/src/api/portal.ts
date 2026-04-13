import axios from 'axios'

const PORTAL_TOKEN_KEY = 'dtlms-portal-access-token'

export type PortalStudentRecord = {
  id: number
  full_name: string
  phone_number: string
  email: string
  id_number: string
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
  signed_agreement?: boolean
  selected_plan_id?: number | null
  selected_team_name?: string | null
  selected_advisor_name?: string | null
  self_evaluation?: string | null
  submitted_at?: string | null
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
  current_stage: string
  target_quota: number
  interview_group_count: number
  brochure_image_url?: string | null
  summary?: string | null
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
}

export type PortalLoginRequest = {
  account: string
  password: string
}

export type PortalPasswordResetRequest = {
  account: string
  id_number: string
  new_password: string
}

export type PortalApplicationUpsert = {
  plan_id: number
  gender?: string | null
  birth_date?: string | null
  ethnic_group?: string | null
  native_place?: string | null
  marital_status?: string | null
  religious_belief?: string | null
  id_type?: string | null
  mailing_address?: string | null
  graduation_school: string
  highest_degree: string
  intended_field: string
  political_status?: string | null
  english_level?: string | null
  family_info?: string | null
  education_experience?: string | null
  practice_experience?: string | null
  personal_profile?: string | null
  recommendation_notes?: string | null
  personal_statement_text?: string | null
  signed_agreement: boolean
  selected_team_name: string
  selected_advisor_name?: string | null
  self_evaluation?: string | null
}

export type PortalApplicationSubmissionResponse = {
  student: PortalStudentRecord
  application_business_key: string
  application_status: string
}

const portalHttp = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1',
  timeout: 10000,
})

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

export function loginPortalStudent(payload: PortalLoginRequest) {
  return portalHttp.post<PortalSessionResponse>('/portal/login', payload)
}

export function resetPortalStudentPassword(payload: PortalPasswordResetRequest) {
  return portalHttp.post<{ message: string }>('/portal/forgot-password', payload)
}

export function getPortalProfile() {
  return portalHttp.get<PortalStudentRecord>('/portal/me')
}

export function listPortalPlans() {
  return portalHttp.get<{ items: PortalPlanRecord[] }>('/portal/plans')
}

export function listPortalTeams() {
  return portalHttp.get<{ items: PortalTeamRecord[] }>('/portal/teams')
}

export function submitPortalApplication(payload: PortalApplicationUpsert) {
  return portalHttp.post<PortalApplicationSubmissionResponse>('/portal/applications', payload)
}
