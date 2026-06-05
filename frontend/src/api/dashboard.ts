import http from './http'


export type DashboardMetricCard = {
  label: string
  value: string
  target?: string | null
  trend?: string | null
  status: string
}


export type DashboardAlert = {
  level: string
  title: string
  owner: string
  due_text: string
}


export type DashboardOverview = {
  lifecycle_coverage: DashboardMetricCard[]
  recruitment_metrics: DashboardMetricCard[]
  training_metrics: DashboardMetricCard[]
  degree_metrics: DashboardMetricCard[]
  alerts: DashboardAlert[]
  workflow_metrics: DashboardMetricCard[]
}


export type DashboardUndergraduateSchoolRankingItem = {
  school_name: string
  student_count: number
}


export type DashboardUndergraduateSchoolRankingResponse = {
  items: DashboardUndergraduateSchoolRankingItem[]
}


export type DashboardUndergraduateSchoolGroupItem = {
  school_name: string
  student_count: number
  percentage: number
}


export type DashboardUndergraduateSchoolGroupDistribution = {
  group_name: string
  dict_type: string
  total: number
  items: DashboardUndergraduateSchoolGroupItem[]
}


export type DashboardUndergraduateSchoolGroupDistributionResponse = {
  total_applications: number
  groups: DashboardUndergraduateSchoolGroupDistribution[]
}


export type DashboardRecruitmentAdvisorChoiceItem = {
  advisor_name: string
  student_count: number
  percentage: number
}


export type DashboardRecruitmentAdvisorChoiceDistribution = {
  choice_round: string
  choice_name: string
  total: number
  items: DashboardRecruitmentAdvisorChoiceItem[]
}


export type DashboardRecruitmentAdvisorChoiceDistributionResponse = {
  choices: DashboardRecruitmentAdvisorChoiceDistribution[]
}


export type DashboardUndergraduateSchoolStudentItem = {
  recruitment_application_id: number
  student_name: string
  school_name?: string | null
  candidate_no?: string | null
  registered_at?: string | null
  phone_number?: string | null
  email?: string | null
}


export type DashboardUndergraduateSchoolStudentListResponse = {
  school_name: string
  total: number
  items: DashboardUndergraduateSchoolStudentItem[]
}


export function getDashboardOverview() {
  return http.get<DashboardOverview>('/dashboard/overview')
}


export function getDashboardUndergraduateSchoolRankings(limit = 20) {
  return http.get<DashboardUndergraduateSchoolRankingResponse>('/dashboard/undergraduate-school-rankings', {
    params: { limit },
  })
}


export function getDashboardUndergraduateSchoolGroupDistribution() {
  return http.get<DashboardUndergraduateSchoolGroupDistributionResponse>('/dashboard/undergraduate-school-group-distribution')
}


export function getDashboardRecruitmentAdvisorChoiceDistribution() {
  return http.get<DashboardRecruitmentAdvisorChoiceDistributionResponse>('/dashboard/recruitment-advisor-choice-distribution')
}


export function getDashboardRecruitmentAdvisorChoiceStudents(params: { choice_round: string; advisor_name?: string; bucket?: string }) {
  return http.get<DashboardUndergraduateSchoolStudentListResponse>('/dashboard/recruitment-advisor-choice-distribution/students', {
    params,
  })
}


export function getDashboardUndergraduateSchoolGroupStudents(params: { dict_type: string; school_name?: string; bucket?: string }) {
  return http.get<DashboardUndergraduateSchoolStudentListResponse>('/dashboard/undergraduate-school-group-distribution/students', {
    params,
  })
}


export function getDashboardUndergraduateSchoolStudents(schoolName: string) {
  return http.get<DashboardUndergraduateSchoolStudentListResponse>('/dashboard/undergraduate-school-rankings/students', {
    params: { school_name: schoolName },
  })
}