import { request } from './http'

type ApiResponse<T> = {
  status: 'success' | 'error'
  message: string
  data: T | null
}

export type SessionToken = {
  access_token: string
  token_type?: string
}

export type SessionUser = {
  id: number
  username: string
  role: 'user' | 'author' | 'admin'
  is_active: boolean
  first_name: string | null
  last_name: string | null
  middle_name: string | null
  full_name: string | null
}

function getResponseData<T>(response: ApiResponse<T>): T {
  if (response.status !== 'success' || response.data === null) {
    throw new Error('The API returned an empty response')
  }

  return response.data
}

export async function refreshSession(): Promise<SessionToken> {
  const response = await request<ApiResponse<SessionToken>>('/auth/refresh', {
    method: 'POST',
    credentials: 'include',
  })

  return getResponseData(response)
}

export async function getCurrentUser(accessToken: string): Promise<SessionUser> {
  const response = await request<ApiResponse<SessionUser>>('/auth/me', {
    credentials: 'include',
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })

  return getResponseData(response)
}

export async function logoutUser(): Promise<void> {
  await request('/auth/logout', { method: 'POST', credentials: 'include' })
}
