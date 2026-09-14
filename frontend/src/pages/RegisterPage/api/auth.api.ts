import { request } from '@/shared/api/http'

import type { ApiResponse, RegisterCredentials, RegisteredUser } from '../types'

export async function register(credentials: RegisterCredentials): Promise<RegisteredUser> {
  const formData = new FormData()
  formData.set('username', credentials.username)
  formData.set('password', credentials.password)

  const response = await request<ApiResponse<RegisteredUser>>('/auth/register', {
    method: 'POST',
    body: formData,
    credentials: 'include',
  })

  if (response.status !== 'success' || response.data === null) {
    throw new Error('The API returned an empty response')
  }

  return response.data
}
