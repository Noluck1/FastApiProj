<script setup lang="ts">
import { ArrowLeft, AtSign, BadgeCheck, Pencil, ShieldCheck, UserRound } from '@lucide/vue'
import { useI18n } from 'vue-i18n'

import { AppHeader, Button, Card, CardContent, CardHeader, CardTitle } from '@/shared/ui'

import ProfileEditor from './components/ProfileEditor.vue'
import { useProfile } from './model/useProfile'

const profile = useProfile()
const { t } = useI18n()
</script>

<template>
  <main
    class="mx-auto grid min-h-screen w-full max-w-6xl content-start gap-6 px-4 py-4 sm:px-6 sm:py-6"
  >
    <AppHeader
      :active-section="null"
      :can-create="profile.canCreate.value"
      :username="profile.user.value?.username ?? null"
      :is-logging-out="profile.isLoggingOut.value"
      @logout="profile.logout"
    />

    <Button as-child variant="ghost" class="h-11 w-fit rounded-full px-3">
      <RouterLink :to="{ name: 'home' }">
        <ArrowLeft aria-hidden="true" />
        {{ t('auth.profile.backToCatalog') }}
      </RouterLink>
    </Button>

    <section
      v-if="profile.user.value"
      class="grid min-w-0 gap-6 lg:grid-cols-[18rem_minmax(0,1fr)]"
    >
      <Card class="h-fit overflow-hidden rounded-3xl border-border/80 shadow-sm">
        <CardContent class="grid justify-items-center gap-4 px-6 py-8 text-center">
          <div
            class="flex size-24 items-center justify-center rounded-full bg-primary font-serif text-3xl font-semibold text-primary-foreground shadow-sm"
            aria-hidden="true"
          >
            {{ profile.initials.value }}
          </div>
          <div class="min-w-0">
            <h1 class="m-0 break-words font-serif text-2xl font-semibold leading-tight">
              {{ profile.fullName.value }}
            </h1>
            <p class="mt-2 mb-0 inline-flex items-center gap-2 text-sm text-muted-foreground">
              <AtSign class="size-4" aria-hidden="true" />
              {{ profile.user.value.username }}
            </p>
          </div>
          <div class="grid w-full gap-2 border-t border-border pt-5 text-left text-sm">
            <p class="m-0 flex items-center gap-2 rounded-xl bg-secondary px-3 py-2.5">
              <ShieldCheck class="size-4 shrink-0 text-primary" aria-hidden="true" />
              <span>{{ t(`auth.profile.roles.${profile.user.value.role}`) }}</span>
            </p>
            <p class="m-0 flex items-center gap-2 rounded-xl bg-secondary px-3 py-2.5">
              <BadgeCheck class="size-4 shrink-0 text-primary" aria-hidden="true" />
              <span>{{ t('auth.profile.accountActive') }}</span>
            </p>
          </div>
        </CardContent>
      </Card>

      <Card class="min-w-0 rounded-3xl border-border/80 shadow-sm">
        <CardHeader
          class="flex-row items-start justify-between gap-4 border-b border-border px-5 py-6 sm:px-7"
        >
          <div class="min-w-0 flex-1">
            <CardTitle class="font-serif text-2xl leading-tight">
              {{ t('auth.profile.personalData') }}
            </CardTitle>
            <p class="mt-2 mb-0 text-sm leading-relaxed text-muted-foreground">
              {{ t('auth.profile.personalDataHint') }}
            </p>
          </div>
        </CardHeader>

        <CardContent class="px-5 py-6 sm:px-7">
          <ProfileEditor
            v-if="profile.isEditing.value"
            :is-saving="profile.isSaving.value"
            :submit-error="profile.submitError.value"
            :user="profile.user.value"
            @cancel="profile.cancelEditing"
            @submit="profile.saveFullName"
          />

          <dl v-else class="m-0 grid min-w-0 gap-x-8 gap-y-6 sm:grid-cols-2">
            <div class="min-w-0">
              <dt class="text-sm text-muted-foreground">{{ t('auth.profile.fields.lastName') }}</dt>
              <dd class="m-0 mt-1.5 break-words font-medium">
                {{ profile.user.value.last_name || t('auth.profile.notSpecified') }}
              </dd>
            </div>
            <div class="min-w-0">
              <dt class="text-sm text-muted-foreground">
                {{ t('auth.profile.fields.firstName') }}
              </dt>
              <dd class="m-0 mt-1.5 break-words font-medium">
                {{ profile.user.value.first_name || t('auth.profile.notSpecified') }}
              </dd>
            </div>
            <div class="min-w-0">
              <dt class="text-sm text-muted-foreground">
                {{ t('auth.profile.fields.middleName') }}
              </dt>
              <dd class="m-0 mt-1.5 break-words font-medium">
                {{ profile.user.value.middle_name || t('auth.profile.notSpecified') }}
              </dd>
            </div>
            <div class="min-w-0">
              <dt class="text-sm text-muted-foreground">{{ t('auth.profile.fields.username') }}</dt>
              <dd class="m-0 mt-1.5 break-words font-medium">
                {{ profile.user.value.username }}
              </dd>
            </div>
          </dl>
        </CardContent>
        <CardHeader>
          <Button
            v-if="!profile.isEditing.value"
            type="button"
            size="sm"
            variant="outline"
            class="mr-5 mb-6 h-9 w-fit justify-self-end rounded-full px-3 sm:mr-7 sm:px-4"
            @click="profile.startEditing"
          >
            <Pencil aria-hidden="true" />
            <span class="hidden sm:inline">{{ t('auth.profile.edit') }}</span>
          </Button>
        </CardHeader>
      </Card>
    </section>

    <Card v-else class="rounded-3xl">
      <CardContent class="grid justify-items-center gap-3 py-12 text-center text-muted-foreground">
        <UserRound class="size-8" aria-hidden="true" />
        <p class="m-0">{{ t('auth.profile.loading') }}</p>
      </CardContent>
    </Card>
  </main>
</template>
