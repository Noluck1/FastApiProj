import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

import { formatDate } from '@/shared/lib/format/date'

export function useWelcomeMessage() {
  const today = new Date()
  const { locale, t } = useI18n()

  const message = computed(() => t('home.welcome.title'))
  const subtitle = computed(() =>
    t('home.welcome.subtitle', {
      date: formatDate(today, locale.value),
    }),
  )

  return { message, subtitle }
}
