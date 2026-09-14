import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { z } from 'zod'

import { toast } from '@/shared/ui'

export function useWelcomeForm() {
  const { t } = useI18n()

  const formSchema = computed(() =>
    toTypedSchema(
      z.object({
        name: z
          .string()
          .min(2, t('home.form.validation.nameMin'))
          .max(50, t('home.form.validation.nameMax')),
        email: z.string().email(t('home.form.validation.emailInvalid')),
      }),
    ),
  )

  const form = useForm({
    validationSchema: formSchema,
    initialValues: {
      name: '',
      email: '',
    },
  })

  const onSubmit = form.handleSubmit((values) => {
    toast.success(t('home.form.success.title'), {
      description: t('home.form.success.description', values),
    })

    form.resetForm()
  })

  return {
    form,
    onSubmit,
  }
}
