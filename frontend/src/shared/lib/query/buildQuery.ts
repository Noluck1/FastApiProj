type QueryValue = string | number | boolean | null | undefined

export function buildQuery(params: Record<string, QueryValue>) {
  const entries = Object.entries(params).filter(
    ([, value]) => value !== undefined && value !== null,
  )

  if (entries.length === 0) {
    return ''
  }

  const searchParams = new URLSearchParams()
  for (const [key, value] of entries) {
    searchParams.set(key, String(value))
  }

  return `?${searchParams.toString()}`
}
