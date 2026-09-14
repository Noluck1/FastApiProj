import { request } from './http'
import { buildQuery } from '@/shared/lib/query/buildQuery'

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

export type BookPayload = {
  title: string
  description: string | null
}

export type BookSortBy = 'id' | 'created_at' | 'updated_at'
export type SortOrder = 'asc' | 'desc'

export type BookListQuery = {
  page: number
  page_size: number
  book_id?: number
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

type ApiResponse<T> = {
  status: 'success' | 'error'
  message: string
  data: T | null
}

type Favorite = { user_id: number; book_id: number }

function getResponseData<T>(response: ApiResponse<T>): T {
  if (response.status !== 'success' || response.data === null) {
    throw new Error('The API returned an empty response')
  }

  return response.data
}

function getAuthorizationHeaders(accessToken: string): HeadersInit {
  return { Authorization: `Bearer ${accessToken}` }
}

export async function getBooks(query: BookListQuery): Promise<PaginatedBooks> {
  const response = await request<ApiResponse<PaginatedBooks>>(`/books${buildQuery(query)}`)
  return getResponseData(response)
}

export async function getBook(bookId: number): Promise<Book> {
  const response = await request<ApiResponse<Book>>(`/books/${bookId}`)
  return getResponseData(response)
}

export async function getFavoriteBooks(
  query: Omit<BookListQuery, 'is_deleted' | 'include_deleted'>,
  accessToken: string,
): Promise<PaginatedBooks> {
  const response = await request<ApiResponse<PaginatedBooks>>(`/favorite${buildQuery(query)}`, {
    headers: getAuthorizationHeaders(accessToken),
  })
  return getResponseData(response)
}

export async function addFavorite(bookId: number, accessToken: string): Promise<Favorite> {
  const response = await request<ApiResponse<Favorite>>(`/favorite/${bookId}`, {
    method: 'POST',
    headers: getAuthorizationHeaders(accessToken),
  })
  return getResponseData(response)
}

export async function removeFavorite(bookId: number, accessToken: string): Promise<Favorite> {
  const response = await request<ApiResponse<Favorite>>(`/favorite/${bookId}`, {
    method: 'DELETE',
    headers: getAuthorizationHeaders(accessToken),
  })
  return getResponseData(response)
}

export async function createBook(payload: BookPayload, accessToken: string): Promise<Book> {
  const response = await request<ApiResponse<Book>>('/books', {
    method: 'POST',
    headers: getAuthorizationHeaders(accessToken),
    body: JSON.stringify(payload),
  })
  return getResponseData(response)
}

export async function updateBook(
  bookId: number,
  payload: BookPayload,
  accessToken: string,
): Promise<Book> {
  const response = await request<ApiResponse<Book>>(`/books/${bookId}`, {
    method: 'PATCH',
    headers: getAuthorizationHeaders(accessToken),
    body: JSON.stringify(payload),
  })
  return getResponseData(response)
}

export async function deleteBook(bookId: number, accessToken: string): Promise<Book> {
  const response = await request<ApiResponse<Book>>(`/books/${bookId}`, {
    method: 'DELETE',
    headers: getAuthorizationHeaders(accessToken),
  })
  return getResponseData(response)
}
