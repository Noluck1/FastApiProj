import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { computed, shallowRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { z } from 'zod'

import { isApiError } from '@/shared/api/types'
import { useSessionStore } from '@/shared/stores/session.store'
import { useUserStore } from '@/shared/stores/user.store'

import { getCurrentUser, login } from '../api/auth.api'

function getErrorTranslationKey(error: unknown): string {
  if (!isApiError(error)) {
    return 'auth.login.errors.generic'
  }

  if (error.status === 0) {
    return 'auth.login.errors.connection'
  }

  if (error.status === 401) {
    return 'auth.login.errors.invalidCredentials'
  }

  if (error.status === 403) {
    return 'auth.login.errors.inactiveUser'
  }

  if (error.status === 422) {
    return 'auth.login.errors.invalidRequest'
  }

  if (error.status >= 500) {
    return 'auth.login.errors.service'
  }

  return 'auth.login.errors.generic'
}

export function useLoginForm() {
  const { t } = useI18n()
  const route = useRoute()
  const router = useRouter()
  const sessionStore = useSessionStore()
  const userStore = useUserStore()
  const submitError = shallowRef<string | null>(null)

  const validationSchema = computed(() =>
    toTypedSchema(
      z.object({
        username: z
          .string()
          .min(5, t('auth.login.validation.usernameMin'))
          .max(50, t('auth.login.validation.usernameMax')),
        password: z
          .string()
          .min(8, t('auth.login.validation.passwordMin'))
          .max(128, t('auth.login.validation.passwordMax')),
      }),
    ),
  )

  const form = useForm({
    validationSchema,
    initialValues: {
      username: '',
      password: '',
    },
  })

  const onSubmit = form.handleSubmit(async (values) => {
    submitError.value = null

    try {
      const token = await login(values)
      sessionStore.setSession(token.access_token, null)

      const user = await getCurrentUser(token.access_token)
      userStore.setUser(user)

      const redirect = route.query.redirect
      await router.replace(
        typeof redirect === 'string' && redirect.startsWith('/') && !redirect.startsWith('//')
          ? redirect
          : { name: 'home' },
      )
    } catch (error) {
      sessionStore.clearSession()
      userStore.clearUser()
      submitError.value = t(getErrorTranslationKey(error))
    }
  })

  return {
    isSubmitting: form.isSubmitting,
    onSubmit,
    submitError,
  }
}
