import type { PagedResponse, PaginationParams, SelectOption } from './common'
import http from './http'


export type ThesisRecord = {
  id: number
  business_key: string
  student_no: string
  student_name: string
  advisor_name: string
  title: string
  plagiarism_rate?: number | null
  thesis_status: string
  blind_review_status: string
  defense_status: string
  degree_status: string
}


export type ThesisUpsert = Omit<ThesisRecord, 'id' | 'business_key'> & {
  business_key?: string | null
}


export type ThesisReviewRecord = {
  id: number
  thesis_id: number
  thesis_title: string
  expert_name: string
  review_score?: number | null
  review_status: string
  review_comment?: string | null
}


export type ThesisReviewUpsert = Omit<ThesisReviewRecord, 'id'>


export type DegreeStats = {
  thesis_total: number
  plagiarism_pending_total: number
  blind_review_pending_total: number
  defense_pending_total: number
  degree_granted_total: number
}


export type DegreeOptions = {
  student_options: SelectOption[]
  advisor_options: SelectOption[]
  thesis_options: SelectOption[]
  thesis_status_options: SelectOption[]
  blind_review_status_options: SelectOption[]
  defense_status_options: SelectOption[]
  degree_status_options: SelectOption[]
  expert_options: SelectOption[]
  review_status_options: SelectOption[]
}


export function getDegreeStats() {
  return http.get<DegreeStats>('/degree/stats')
}


export function getDegreeOptions() {
  return http.get<DegreeOptions>('/degree/options')
}


export function createThesis(payload: ThesisUpsert) {
  return http.post<ThesisRecord>('/degree/theses', payload)
}


export function updateThesis(id: number, payload: ThesisUpsert) {
  return http.put<ThesisRecord>(`/degree/theses/${id}`, payload)
}


export function listTheses(params?: PaginationParams & { keyword?: string; degree_status?: string; advisor_name?: string; thesis_status?: string }) {
  return http.get<PagedResponse<ThesisRecord>>('/degree/theses', { params })
}

export function listThesisReviews(params?: PaginationParams & { thesis_id?: number; keyword?: string; expert_name?: string; review_status?: string }) {
  return http.get<PagedResponse<ThesisReviewRecord>>('/degree/reviews', { params })
}


export function createThesisReview(payload: ThesisReviewUpsert) {
  return http.post<ThesisReviewRecord>('/degree/reviews', payload)
}


export function updateThesisReview(id: number, payload: ThesisReviewUpsert) {
  return http.put<ThesisReviewRecord>(`/degree/reviews/${id}`, payload)
}
