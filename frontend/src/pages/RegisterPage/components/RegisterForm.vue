<script setup lang="ts">
import { useI18n } from 'vue-i18n'

import {
  AuthSubmitButton,
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  Input,
} from '@/shared/ui'

import { useRegisterForm } from '../model/useRegisterForm'

const { t } = useI18n()
const { isSubmitting, onSubmit, submitError } = useRegisterForm()
</script>

<template>
  <Card class="w-full min-w-0 max-w-[30rem] gap-6 rounded-3xl py-7 shadow-lg sm:py-8">
    <CardHeader class="min-w-0 gap-2 px-5 sm:px-8">
      <RouterLink
        class="mb-2 w-fit font-serif text-sm font-semibold text-foreground no-underline"
        :to="{ name: 'home' }"
      >
        {{ t('common.appName') }}
      </RouterLink>
      <h1 class="m-0 font-serif text-3xl font-semibold tracking-tight text-foreground">
        {{ t('auth.register.title') }}
      </h1>
      <CardDescription class="leading-relaxed">
        {{ t('auth.register.subtitle') }}
      </CardDescription>
    </CardHeader>

    <CardContent class="px-5 sm:px-8">
      <form class="grid gap-4" :aria-busy="isSubmitting" @submit="onSubmit">
        <FormField v-slot="{ componentField }" name="username">
          <FormItem>
            <FormLabel>{{ t('auth.register.fields.username.label') }}</FormLabel>
            <FormControl>
              <Input
                class="h-12 rounded-xl px-4"
                type="text"
                autocomplete="username"
                :placeholder="t('auth.register.fields.username.placeholder')"
                :disabled="isSubmitting"
                v-bind="componentField"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="password">
          <FormItem>
            <FormLabel>{{ t('auth.register.fields.password.label') }}</FormLabel>
            <FormControl>
              <Input
                class="h-12 rounded-xl px-4"
                type="password"
                autocomplete="new-password"
                :placeholder="t('auth.register.fields.password.placeholder')"
                :disabled="isSubmitting"
                v-bind="componentField"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="confirmPassword">
          <FormItem>
            <FormLabel>{{ t('auth.register.fields.confirmPassword.label') }}</FormLabel>
            <FormControl>
              <Input
                class="h-12 rounded-xl px-4"
                type="password"
                autocomplete="new-password"
                :placeholder="t('auth.register.fields.confirmPassword.placeholder')"
                :disabled="isSubmitting"
                v-bind="componentField"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="min-h-5">
          <p v-if="submitError" role="alert" class="m-0 text-sm leading-snug text-destructive">
            {{ submitError }}
          </p>
        </div>

        <AuthSubmitButton type="submit" :disabled="isSubmitting" :aria-busy="isSubmitting">
          {{ isSubmitting ? t('auth.register.submitting') : t('auth.register.submit') }}
        </AuthSubmitButton>

        <p class="m-0 text-center text-sm text-muted-foreground">
          {{ t('auth.register.hasAccount') }}
          <RouterLink
            class="font-medium text-primary underline-offset-4 hover:underline"
            :to="{ name: 'login' }"
          >
            {{ t('auth.register.loginLink') }}
          </RouterLink>
        </p>
      </form>
    </CardContent>
  </Card>
</template>
