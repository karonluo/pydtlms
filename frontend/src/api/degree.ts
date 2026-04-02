import http from './http'
import type { SelectOption } from './students'


export type ThesisRecord = {
  id: number
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


export type ThesisUpsert = Omit<ThesisRecord, 'id'>


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


export function listTheses(params?: { keyword?: string; degree_status?: string }) {
  return http.get<{ items: ThesisRecord[]; total: number }>('/degree/theses', { params })
}


export function createThesis(payload: ThesisUpsert) {
  return http.post<ThesisRecord>('/degree/theses', payload)
}


export function updateThesis(id: number, payload: ThesisUpsert) {
  return http.put<ThesisRecord>(`/degree/theses/${id}`, payload)
}


export function listThesisReviews(params?: { thesis_id?: number }) {
  return http.get<{ items: ThesisReviewRecord[]; total: number }>('/degree/reviews', { params })
}


export function createThesisReview(payload: ThesisReviewUpsert) {
  return http.post<ThesisReviewRecord>('/degree/reviews', payload)
}


export function updateThesisReview(id: number, payload: ThesisReviewUpsert) {
  return http.put<ThesisReviewRecord>(`/degree/reviews/${id}`, payload)
}
