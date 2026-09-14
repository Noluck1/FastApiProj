export function formatDate(value: Date, locale = 'en-US'): string {
  return value.toLocaleDateString(locale, {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
  })
}
