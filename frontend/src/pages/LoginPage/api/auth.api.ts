import { request } from '@/shared/api/http'
export { getCurrentUser } from '@/shared/api/session'

import type { ApiResponse, LoginFormValues, TokenResponse } from '../types'

function getResponseData<T>(response: ApiResponse<T>): T {
  if (response.status !== 'success' || response.data === null) {
    throw new Error('The API returned an empty response')
  }

  return response.data
}

export async function login(credentials: LoginFormValues): Promise<TokenResponse> {
  const formData = new FormData()
  formData.set('username', credentials.username)
  formData.set('password', credentials.password)

  const response = await request<ApiResponse<TokenResponse>>('/auth/login', {
    method: 'POST',
    body: formData,
    credentials: 'include',
  })

  return getResponseData(response)
}
