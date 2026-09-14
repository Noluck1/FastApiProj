<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { Check, X } from '@lucide/vue'
import { useForm } from 'vee-validate'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { z } from 'zod'

import {
  Button,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  Input,
} from '@/shared/ui'
import type { User } from '@/shared/stores/user.store'

import type { ProfileFormValues } from '../types'

const props = defineProps<{
  isSaving: boolean
  submitError: string | null
  user: User
}>()

const emit = defineEmits<{
  cancel: []
  submit: [values: ProfileFormValues]
}>()

const { t } = useI18n()

const validationSchema = computed(() =>
  toTypedSchema(
    z.object({
      lastName: z
        .string()
        .trim()
        .min(1, t('auth.profile.validation.lastNameRequired'))
        .max(100, t('auth.profile.validation.nameMax')),
      firstName: z
        .string()
        .trim()
        .min(1, t('auth.profile.validation.firstNameRequired'))
        .max(100, t('auth.profile.validation.nameMax')),
      middleName: z.string().trim().max(100, t('auth.profile.validation.nameMax')),
    }),
  ),
)

const form = useForm<ProfileFormValues>({
  validationSchema,
  initialValues: {
    firstName: props.user.first_name ?? '',
    lastName: props.user.last_name ?? '',
    middleName: props.user.middle_name ?? '',
  },
})

const onSubmit = form.handleSubmit((values) => emit('submit', values))
</script>

<template>
  <form class="grid gap-5" :aria-busy="isSaving" @submit="onSubmit">
    <div class="grid min-w-0 gap-5 sm:grid-cols-2">
      <FormField v-slot="{ componentField }" name="lastName">
        <FormItem>
          <FormLabel>{{ t('auth.profile.fields.lastName') }}</FormLabel>
          <FormControl>
            <Input
              class="h-12 rounded-xl px-4"
              autocomplete="family-name"
              :disabled="isSaving"
              :placeholder="t('auth.profile.placeholders.lastName')"
              v-bind="componentField"
            />
          </FormControl>
          <FormMessage />
        </FormItem>
      </FormField>

      <FormField v-slot="{ componentField }" name="firstName">
        <FormItem>
          <FormLabel>{{ t('auth.profile.fields.firstName') }}</FormLabel>
          <FormControl>
            <Input
              class="h-12 rounded-xl px-4"
              autocomplete="given-name"
              :disabled="isSaving"
              :placeholder="t('auth.profile.placeholders.firstName')"
              v-bind="componentField"
            />
          </FormControl>
          <FormMessage />
        </FormItem>
      </FormField>
    </div>

    <FormField v-slot="{ componentField }" name="middleName">
      <FormItem>
        <FormLabel>{{ t('auth.profile.fields.middleName') }}</FormLabel>
        <FormControl>
          <Input
            class="h-12 rounded-xl px-4"
            autocomplete="additional-name"
            :disabled="isSaving"
            :placeholder="t('auth.profile.placeholders.middleName')"
            v-bind="componentField"
          />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <p v-if="submitError" role="alert" class="m-0 text-sm leading-relaxed text-destructive">
      {{ submitError }}
    </p>

    <div class="flex flex-col-reverse gap-3 border-t border-border pt-5 sm:flex-row sm:justify-end">
      <Button
        type="button"
        variant="ghost"
        class="h-11 rounded-full px-5"
        :disabled="isSaving"
        @click="emit('cancel')"
      >
        <X aria-hidden="true" />
        {{ t('common.cancel') }}
      </Button>
      <Button type="submit" class="h-11 rounded-full px-6" :disabled="isSaving">
        <Check aria-hidden="true" />
        {{ isSaving ? t('auth.profile.saving') : t('auth.profile.save') }}
      </Button>
    </div>
  </form>
</template>
