<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { z } from 'zod'

import {
  Button,
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  Input,
  Textarea,
} from '@/shared/ui'

import type { Book, BookFormValues } from '../types'

const props = defineProps<{
  mode: 'create' | 'edit'
  book: Book | null
  isSaving: boolean
}>()

const emit = defineEmits<{
  cancel: []
  submit: [values: BookFormValues]
}>()

const { t } = useI18n()

const validationSchema = computed(() =>
  toTypedSchema(
    z.object({
      title: z
        .string()
        .trim()
        .min(5, t('home.catalog.editor.validation.titleMin'))
        .max(100, t('home.catalog.editor.validation.titleMax')),
      description: z.string().max(255, t('home.catalog.editor.validation.descriptionMax')),
    }),
  ),
)

const form = useForm<BookFormValues>({
  validationSchema,
  initialValues: {
    title: props.book?.title ?? '',
    description: props.book?.description ?? '',
  },
})

const onSubmit = form.handleSubmit((values) => {
  emit('submit', values)
})
</script>

<template>
  <Card
    id="book-editor"
    class="scroll-mt-28 gap-5 rounded-3xl border-border bg-card/70 py-5 shadow-sm"
  >
    <CardHeader class="px-5 sm:px-6">
      <h2 class="m-0 font-serif text-2xl font-semibold tracking-tight text-foreground">
        {{
          props.mode === 'create'
            ? t('home.catalog.editor.createTitle')
            : t('home.catalog.editor.editTitle')
        }}
      </h2>
      <CardDescription>
        {{ t('home.catalog.editor.subtitle') }}
      </CardDescription>
    </CardHeader>

    <CardContent class="px-5 sm:px-6">
      <form id="book-editor-form" class="grid gap-4" @submit="onSubmit">
        <FormField v-slot="{ componentField }" name="title">
          <FormItem>
            <FormLabel>{{ t('home.catalog.editor.fields.title') }}</FormLabel>
            <FormControl>
              <Input
                class="h-11 rounded-xl bg-background px-4 shadow-none"
                :disabled="props.isSaving"
                :placeholder="t('home.catalog.editor.fields.titlePlaceholder')"
                v-bind="componentField"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="description">
          <FormItem>
            <FormLabel>{{ t('home.catalog.editor.fields.description') }}</FormLabel>
            <FormControl>
              <Textarea
                class="min-h-24 resize-y rounded-xl bg-background px-4 py-3 shadow-none"
                :disabled="props.isSaving"
                :placeholder="t('home.catalog.editor.fields.descriptionPlaceholder')"
                v-bind="componentField"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>
      </form>
    </CardContent>

    <CardFooter class="flex-col-reverse gap-2 px-5 sm:flex-row sm:justify-end sm:px-6">
      <Button
        type="button"
        variant="outline"
        class="w-full rounded-full sm:w-auto"
        :disabled="props.isSaving"
        @click="emit('cancel')"
      >
        {{ t('common.cancel') }}
      </Button>
      <Button
        type="submit"
        form="book-editor-form"
        class="w-full rounded-full sm:w-auto"
        :disabled="props.isSaving"
      >
        {{ props.isSaving ? t('home.catalog.editor.saving') : t('home.catalog.editor.save') }}
      </Button>
    </CardFooter>
  </Card>
</template>
