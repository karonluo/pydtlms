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


export function getDashboardOverview() {
  return http.get<DashboardOverview>('/dashboard/overview')
}