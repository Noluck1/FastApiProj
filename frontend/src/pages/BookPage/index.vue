<script setup lang="ts">
import { ArrowLeft, BookOpen, Bookmark, BookmarkCheck, CalendarDays, UserRound } from '@lucide/vue'
import { useI18n } from 'vue-i18n'

import { formatDate } from '@/shared/lib/format/date'
import { AppHeader, Button, Card, CardContent } from '@/shared/ui'

import { useBookDetails } from './model/useBookDetails'

const details = useBookDetails()
const { t, locale } = useI18n()

function displayDate(value: string): string {
  return formatDate(new Date(value), locale.value === 'ru' ? 'ru-RU' : 'en-US')
}
</script>

<template>
  <main class="mx-auto grid w-full max-w-6xl gap-6 px-4 py-4 sm:px-6 sm:py-6">
    <AppHeader
      :active-section="details.activeSection.value"
      :can-create="details.canCreate.value"
      :username="details.username.value"
      :is-logging-out="details.isLoggingOut.value"
      @logout="details.logout"
    />

    <Button as-child variant="ghost" class="h-11 w-fit rounded-full px-3">
      <RouterLink
        :to="{
          name: 'home',
          query:
            details.activeSection.value === 'catalog'
              ? {}
              : { section: details.activeSection.value },
        }"
      >
        <ArrowLeft aria-hidden="true" />
        {{ t('home.book.back') }}
      </RouterLink>
    </Button>

    <Card v-if="details.isLoading.value">
      <CardContent class="py-12 text-center text-sm text-muted-foreground">
        {{ t('home.book.loading') }}
      </CardContent>
    </Card>

    <Card v-else-if="details.error.value">
      <CardContent class="grid justify-items-center gap-4 py-12 text-center">
        <p role="alert" class="m-0 text-destructive">{{ details.error.value }}</p>
        <Button type="button" variant="outline" class="rounded-full" @click="details.loadBook">
          {{ t('home.book.retry') }}
        </Button>
      </CardContent>
    </Card>

    <article
      v-else-if="details.book.value"
      class="grid min-w-0 gap-6 md:grid-cols-[14rem_minmax(0,1fr)]"
    >
      <div
        aria-hidden="true"
        class="relative mx-auto flex aspect-[2/3] w-full max-w-56 flex-col justify-between overflow-hidden rounded-r-2xl rounded-l-md border border-border bg-secondary p-6 text-secondary-foreground shadow-xl before:absolute before:inset-y-0 before:left-3 before:w-px before:bg-current before:opacity-20 after:absolute after:inset-x-6 after:top-12 after:border-t after:border-current after:opacity-30 md:mx-0"
      >
        <span class="text-xs tracking-[0.2em] uppercase opacity-60">Bibliotheca</span>
        <span class="font-serif text-5xl font-semibold uppercase">{{
          details.book.value.title.charAt(0)
        }}</span>
        <span class="border-t border-current pt-3 text-xs tracking-widest opacity-70"
          >№ {{ details.book.value.id }}</span
        >
      </div>

      <div class="grid min-w-0 content-start gap-6">
        <header class="grid min-w-0 gap-4 border-b border-border pb-6">
          <div class="flex min-w-0 flex-wrap items-center gap-3 text-sm text-muted-foreground">
            <span class="inline-flex items-center gap-2"
              ><UserRound class="size-4" aria-hidden="true" />{{
                details.book.value.author_full_name ||
                details.book.value.author_username ||
                t('home.catalog.states.unknownAuthor')
              }}</span
            >
            <span class="inline-flex items-center gap-2"
              ><CalendarDays class="size-4" aria-hidden="true" />{{
                displayDate(details.book.value.created_at)
              }}</span
            >
          </div>
          <h1 class="m-0 break-words font-serif text-3xl leading-tight text-foreground sm:text-5xl">
            {{ details.book.value.title }}
          </h1>
          <div class="flex flex-wrap gap-2">
            <Button
              v-if="details.isAuthenticated.value"
              type="button"
              variant="outline"
              class="h-11 rounded-full"
              :disabled="details.isSavingFavorite.value"
              @click="details.toggleFavorite"
            >
              <BookmarkCheck v-if="details.isFavorite.value" aria-hidden="true" />
              <Bookmark v-else aria-hidden="true" />
              {{
                details.isFavorite.value
                  ? t('home.catalog.actions.removeFavorite')
                  : t('home.catalog.actions.addFavorite')
              }}
            </Button>
          </div>
        </header>

        <section class="grid gap-3">
          <h2 class="m-0 font-serif text-2xl text-foreground">{{ t('home.book.description') }}</h2>
          <p class="m-0 max-w-[48rem] break-words text-base leading-7 text-muted-foreground">
            {{ details.book.value.description || t('home.catalog.states.noDescription') }}
          </p>
        </section>

        <section class="grid gap-3 rounded-2xl border border-border bg-muted/50 p-5">
          <div class="flex items-center gap-2">
            <BookOpen class="size-5 text-primary" aria-hidden="true" />
            <h2 class="m-0 font-serif text-xl text-foreground">
              {{ t('home.book.contentTitle') }}
            </h2>
          </div>
          <p class="m-0 max-w-[42rem] text-sm leading-relaxed text-muted-foreground">
            {{ t('home.book.contentUnavailable') }}
          </p>
        </section>

        <section class="grid gap-3 border-t border-border pt-5">
          <h2 class="m-0 font-serif text-xl text-foreground">{{ t('home.book.details') }}</h2>
          <dl class="m-0 grid gap-3 text-sm sm:grid-cols-2">
            <div>
              <dt class="text-muted-foreground">{{ t('home.book.id') }}</dt>
              <dd class="m-0 mt-1 font-medium">{{ details.book.value.id }}</dd>
            </div>
            <div>
              <dt class="text-muted-foreground">{{ t('home.book.status') }}</dt>
              <dd class="m-0 mt-1 font-medium">
                {{
                  details.book.value.is_deleted
                    ? t('home.catalog.states.deleted')
                    : t('home.catalog.states.active')
                }}
              </dd>
            </div>
            <div>
              <dt class="text-muted-foreground">{{ t('home.catalog.details.created') }}</dt>
              <dd class="m-0 mt-1 font-medium">{{ displayDate(details.book.value.created_at) }}</dd>
            </div>
            <div>
              <dt class="text-muted-foreground">{{ t('home.catalog.details.updated') }}</dt>
              <dd class="m-0 mt-1 font-medium">{{ displayDate(details.book.value.updated_at) }}</dd>
            </div>
          </dl>
        </section>
      </div>
    </article>
  </main>
</template>
