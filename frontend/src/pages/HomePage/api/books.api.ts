import { request } from '@/shared/api/http'
import { buildQuery } from '@/shared/lib/query/buildQuery'

import type { ApiResponse, Book, BookListQuery, BookPayload, PaginatedBooks } from '../types'

export { addFavorite, getFavoriteBooks, removeFavorite } from '@/shared/api/books'

function getResponseData<T>(response: ApiResponse<T>): T {
  if (response.status !== 'success' || response.data === null) {
    throw new Error('The API returned an empty response')
  }

  return response.data
}

function getAuthorizationHeaders(accessToken: string): HeadersInit {
  return {
    Authorization: `Bearer ${accessToken}`,
  }
}

export async function getBooks(query: BookListQuery): Promise<PaginatedBooks> {
  const response = await request<ApiResponse<PaginatedBooks>>(`/books${buildQuery(query)}`)
  return getResponseData(response)
}

export async function getCreatedBooks(
  query: BookListQuery,
  accessToken: string,
): Promise<PaginatedBooks> {
  const response = await request<ApiResponse<PaginatedBooks>>(
    `/books/created-by-me${buildQuery(query)}`,
    {
      headers: getAuthorizationHeaders(accessToken),
    },
  )

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
