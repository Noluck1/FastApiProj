export type ApiError = {
  status: number
  message: string
  details?: unknown
}

export function isApiError(error: unknown): error is ApiError {
  if (typeof error !== 'object' || error === null) {
    return false
  }

  const candidate = error as Partial<ApiError>

  return typeof candidate.status === 'number' && typeof candidate.message === 'string'
}
