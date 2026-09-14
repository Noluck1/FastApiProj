import { API_BASE_URL } from './endpoints'
import type { ApiError } from './types'

type AccessTokenRefreshHandler = () => Promise<string | null>

type ErrorPayload = {
  message?: unknown
  detail?: unknown
  data?: unknown
}

let accessTokenRefreshHandler: AccessTokenRefreshHandler | null = null

export function configureAccessTokenRefresh(handler: AccessTokenRefreshHandler): void {
  accessTokenRefreshHandler = handler
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

async function readResponseBody(response: Response): Promise<unknown> {
  const body = await response.text()

  if (!body) {
    return undefined
  }

  try {
    return JSON.parse(body) as unknown
  } catch {
    return body
  }
}

function getErrorMessage(payload: unknown, fallback: string): string {
  if (typeof payload === 'string' && payload.trim()) {
    return payload
  }

  if (!isRecord(payload)) {
    return fallback
  }

  const { message, detail } = payload as ErrorPayload

  if (typeof message === 'string' && message.trim()) {
    return message
  }

  if (typeof detail === 'string' && detail.trim()) {
    return detail
  }

  if (Array.isArray(detail)) {
    const validationMessage = detail.find(
      (item): item is Record<string, unknown> => isRecord(item) && typeof item.msg === 'string',
    )?.msg

    if (typeof validationMessage === 'string') {
      return validationMessage
    }
  }

  return fallback
}

export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  const isFormData = typeof FormData !== 'undefined' && init.body instanceof FormData

  if (typeof init.body === 'string' && !isFormData && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }

  async function send(): Promise<Response> {
    try {
      return await fetch(`${API_BASE_URL}${path}`, {
        ...init,
        headers,
      })
    } catch (error) {
      throw {
        status: 0,
        message: 'Network request failed',
        details: error,
      } satisfies ApiError
    }
  }

  let response = await send()
  const authorization = headers.get('Authorization')

  if (
    response.status === 401 &&
    authorization?.startsWith('Bearer ') &&
    accessTokenRefreshHandler
  ) {
    const accessToken = await accessTokenRefreshHandler()

    if (accessToken) {
      headers.set('Authorization', `Bearer ${accessToken}`)
      response = await send()
    }
  }

  const payload = await readResponseBody(response)

  if (!response.ok) {
    throw {
      status: response.status,
      message: getErrorMessage(payload, response.statusText || 'Request failed'),
      details: isRecord(payload) ? (payload.data ?? payload.detail) : undefined,
    } satisfies ApiError
  }

  if (response.status === 204) {
    return undefined as T
  }

  return payload as T
}
