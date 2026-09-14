import { createI18n } from 'vue-i18n'

import { defaultLocale, messages } from '@/shared/i18n'

export const i18n = createI18n({
  legacy: false,
  locale: defaultLocale,
  fallbackLocale: defaultLocale,
  messages,
  globalInjection: true,
})
