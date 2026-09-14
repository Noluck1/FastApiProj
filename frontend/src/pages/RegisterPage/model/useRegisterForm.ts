import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { computed, shallowRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { z } from 'zod'

import { isApiError } from '@/shared/api/types'

import { register } from '../api/auth.api'

function getErrorTranslationKey(error: unknown): string {
  if (!isApiError(error)) {
    return 'auth.register.errors.generic'
  }

  if (error.status === 0) {
    return 'auth.register.errors.connection'
  }

  if (error.status === 409) {
    return 'auth.register.errors.usernameExists'
  }

  if (error.status === 422) {
    return 'auth.register.errors.invalidRequest'
  }

  if (error.status >= 500) {
    return 'auth.register.errors.service'
  }

  return 'auth.register.errors.generic'
}

export function useRegisterForm() {
  const { t } = useI18n()
  const router = useRouter()
  const submitError = shallowRef<string | null>(null)

  const validationSchema = computed(() =>
    toTypedSchema(
      z
        .object({
          username: z
            .string()
            .min(5, t('auth.register.validation.usernameMin'))
            .max(50, t('auth.register.validation.usernameMax')),
          password: z
            .string()
            .min(8, t('auth.register.validation.passwordMin'))
            .max(128, t('auth.register.validation.passwordMax')),
          confirmPassword: z.string(),
        })
        .refine((values) => values.password === values.confirmPassword, {
          message: t('auth.register.validation.passwordMismatch'),
          path: ['confirmPassword'],
        }),
    ),
  )

  const form = useForm({
    validationSchema,
    initialValues: {
      username: '',
      password: '',
      confirmPassword: '',
    },
  })

  const onSubmit = form.handleSubmit(async ({ username, password }) => {
    submitError.value = null

    try {
      await register({ username, password })
      await router.replace({ name: 'login' })
    } catch (error) {
      submitError.value = t(getErrorTranslationKey(error))
    }
  })

  return {
    isSubmitting: form.isSubmitting,
    onSubmit,
    submitError,
  }
}
