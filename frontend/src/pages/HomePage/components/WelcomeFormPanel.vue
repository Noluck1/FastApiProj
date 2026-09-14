<script setup lang="ts">
import { useI18n } from 'vue-i18n'

import {
  Button,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  Input,
} from '@/shared/ui'

import { useWelcomeForm } from '../model/useWelcomeForm'

const { t } = useI18n()
const { onSubmit } = useWelcomeForm()
</script>

<template>
  <div class="rounded-2xl border border-border bg-card p-6 text-card-foreground shadow-sm">
    <div class="mb-6">
      <h2 class="m-0 text-heading-4 font-semibold">{{ t('home.form.title') }}</h2>
      <p class="mt-2 mb-0 text-paragraph-regular text-muted-foreground">
        {{ t('home.form.subtitle') }}
      </p>
    </div>

    <form class="grid gap-5" @submit="onSubmit">
      <FormField v-slot="{ componentField }" name="name">
        <FormItem>
          <FormLabel>{{ t('home.form.fields.name.label') }}</FormLabel>
          <FormControl>
            <Input
              type="text"
              :placeholder="t('home.form.fields.name.placeholder')"
              v-bind="componentField"
            />
          </FormControl>
          <FormDescription>{{ t('home.form.fields.name.description') }}</FormDescription>
          <FormMessage />
        </FormItem>
      </FormField>

      <FormField v-slot="{ componentField }" name="email">
        <FormItem>
          <FormLabel>{{ t('home.form.fields.email.label') }}</FormLabel>
          <FormControl>
            <Input
              type="email"
              :placeholder="t('home.form.fields.email.placeholder')"
              v-bind="componentField"
            />
          </FormControl>
          <FormDescription>{{ t('home.form.fields.email.description') }}</FormDescription>
          <FormMessage />
        </FormItem>
      </FormField>

      <div class="flex items-center justify-between gap-4 border-t border-border pt-5">
        <p class="m-0 text-paragraph-small text-muted-foreground">
          {{ t('home.form.footer') }}
        </p>
        <Button type="submit">{{ t('home.form.submit') }}</Button>
      </div>
    </form>
  </div>
</template>
