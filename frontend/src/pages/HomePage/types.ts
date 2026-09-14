export type Book = {
  id: number
  title: string
  description: string | null
  author_id: number
  author_username: string | null
  author_full_name: string | null
  is_deleted: boolean
  created_at: string
  updated_at: string
  deleted_at: string | null
}

export type BookFormValues = {
  title: string
  description: string
}

export type BookPayload = {
  title: string
  description: string | null
}

export type BookSortBy = 'id' | 'created_at' | 'updated_at'
export type SortOrder = 'asc' | 'desc'
export type BookStatusFilter = 'active' | 'deleted' | 'all'
export type CatalogSection = 'catalog' | 'new' | 'mine' | 'created'

export type BookListQuery = {
  page: number
  page_size: number
  title_contains?: string
  is_deleted?: boolean
  include_deleted?: boolean
  sort_by: BookSortBy
  sort_order: SortOrder
}

export type PaginatedBooks = {
  item: Book[]
  page: number
  page_size: number
  total: number
  total_pages: number
}

export type ApiResponse<T> = {
  status: 'success' | 'error'
  message: string
  data: T | null
}
