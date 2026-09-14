import { request } from '@/shared/api/http'

export async function logoutUser(): Promise<void> {
  await request('/auth/logout', {
    method: 'POST',
    credentials: 'include',
  })
}
