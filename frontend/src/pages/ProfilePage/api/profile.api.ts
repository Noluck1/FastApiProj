import { request } from '@/shared/api/http'
import type { SessionUser } from '@/shared/api/session'

import type { ApiResponse, UpdateFullNamePayload } from '../types'

function getResponseData<T>(response: ApiResponse<T>): T {
  if (response.status !== 'success' || response.data === null) {
    throw new Error('The API returned an empty response')
  }

  return response.data
}

export async function updateMyFullName(
  payload: UpdateFullNamePayload,
  accessToken: string,
): Promise<SessionUser> {
  const response = await request<ApiResponse<SessionUser>>('/auth/me/full-name', {
    method: 'PATCH',
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify(payload),
  })

  return getResponseData(response)
}
