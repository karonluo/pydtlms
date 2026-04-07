export type SelectOption = {
  label: string
  value: string
  color_type?: string | null
  css_class?: string | null
}


export type PaginationParams = {
  page?: number
  page_size?: number
}


export type PagedResponse<T> = {
  items: T[]
  total: number
  page: number
  page_size: number
}


export type BulkActionResponse = {
  success_count: number
}