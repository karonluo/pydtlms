import type { BulkActionResponse, PagedResponse, PaginationParams, SelectOption } from './common'
import http from './http'

export type NewsArticleRecord = {
  id: number
  news_code: string
  news_title: string
  news_content: string
  news_type: string
  publisher_user_id?: number | null
  publisher_username?: string | null
  publisher_name?: string | null
  reviewer_user_id?: number | null
  reviewer_username?: string | null
  reviewer_name?: string | null
  published_at?: string | Date | null
  status: string
  is_pinned: boolean
  display_order: number
  created_at: string
  updated_at: string
}

export type NewsArticleUpsert = {
  news_title: string
  news_content: string
  news_type: string
  published_at?: string | Date | null
  status: string
  is_pinned: boolean
  display_order: number
}

export type NewsArticleListResponse = PagedResponse<NewsArticleRecord>
export type NewsImageUploadResponse = { url: string }

export const NEWS_STATUS_OPTIONS: SelectOption[] = [
  { label: '草稿', value: '草稿' },
  { label: '待发布', value: '待发布' },
  { label: '已发布', value: '已发布' },
  { label: '已下线', value: '已下线' },
]

export function listNewsArticles(params?: PaginationParams & {
  keyword?: string
  news_type?: string
  status?: string
}) {
  return http.get<NewsArticleListResponse>('/recruitment/news', { params })
}


export function getNewsTypeOptions() {
  return http.get<SelectOption[]>('/recruitment/news/options/news-types')
}

export function getNewsArticle(newsArticleId: number) {
  return http.get<NewsArticleRecord>(`/recruitment/news/${newsArticleId}`)
}

export function createNewsArticle(payload: NewsArticleUpsert) {
  return http.post<NewsArticleRecord>('/recruitment/news', payload)
}

export function updateNewsArticle(newsArticleId: number, payload: NewsArticleUpsert) {
  return http.put<NewsArticleRecord>(`/recruitment/news/${newsArticleId}`, payload)
}

export function publishNewsArticle(newsArticleId: number) {
  return http.post<NewsArticleRecord>(`/recruitment/news/${newsArticleId}/publish`)
}

export function deleteNewsArticle(newsArticleId: number) {
  return http.delete(`/recruitment/news/${newsArticleId}`)
}

export function offlineNewsArticle(newsArticleId: number) {
  return http.post<NewsArticleRecord>(`/recruitment/news/${newsArticleId}/offline`)
}

export function uploadNewsImage(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  return http.post<NewsImageUploadResponse>('/recruitment/news/image-upload', formData)
}

export function batchPublishNewsArticles(ids: number[]) {
  return http.post<BulkActionResponse>('/recruitment/news/batch-publish', { ids })
}

export function batchOfflineNewsArticles(ids: number[]) {
  return http.post<BulkActionResponse>('/recruitment/news/batch-offline', { ids })
}
