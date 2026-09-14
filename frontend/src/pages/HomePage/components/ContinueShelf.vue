<script setup lang="ts">
import { ArrowRight, ChevronRight } from '@lucide/vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

import { formatDate } from '@/shared/lib/format/date'
import { Button } from '@/shared/ui'

import type { Book, CatalogSection } from '../types'
import BookCover from './BookCover.vue'

const props = defineProps<{
  books: Book[]
  section: CatalogSection
}>()

const { t, locale } = useI18n()
const shelfBooks = computed(() => props.books.slice(0, 3))
const shelfEyebrow = computed(() => {
  if (props.section === 'mine') return t('home.landing.shelf.mineEyebrow')
  if (props.section === 'created') return t('home.landing.shelf.createdEyebrow')
  return t('home.landing.shelf.eyebrow')
})
const shelfTitle = computed(() => {
  if (props.section === 'mine') return t('home.landing.shelf.mineTitle')
  if (props.section === 'created') return t('home.landing.shelf.createdTitle')
  return t('home.landing.shelf.title')
})

function displayDate(value: string): string {
  return formatDate(new Date(value), locale.value === 'ru' ? 'ru-RU' : 'en-US')
}

function scrollToCatalog() {
  document.querySelector('#popular')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
</script>

<template>
  <section
    v-if="shelfBooks.length"
    id="continue"
    class="mx-auto max-w-[1440px] px-4 py-10 sm:px-7 lg:px-10"
  >
    <div class="flex items-end justify-between gap-4">
      <div class="min-w-0">
        <p class="m-0 text-[11px] font-bold tracking-[0.18em] text-primary uppercase">
          {{ shelfEyebrow }}
        </p>
        <h2
          class="mt-1 mb-0 font-serif text-[28px] leading-tight font-semibold tracking-[-0.025em] sm:text-3xl"
        >
          {{ shelfTitle }}
        </h2>
      </div>
      <Button
        type="button"
        variant="ghost"
        class="hidden h-9 rounded-full px-3 text-muted-foreground sm:inline-flex"
        @click="scrollToCatalog"
      >
        {{ t('home.landing.shelf.allBooks') }}
        <ArrowRight aria-hidden="true" class="size-4" />
      </Button>
    </div>

    <div class="mt-6 grid gap-3 md:grid-cols-3">
      <RouterLink
        v-for="book in shelfBooks"
        :key="book.id"
        class="continue-card group relative flex min-w-0 items-center gap-4 overflow-hidden rounded-[20px] border border-border bg-card p-3 pr-9 text-foreground no-underline transition duration-300 hover:-translate-y-1 hover:border-primary/30"
        :to="{ name: 'book', params: { id: book.id }, query: { from: props.section } }"
      >
        <div class="w-[72px] shrink-0 sm:w-[82px]">
          <BookCover :book="book" compact />
        </div>
        <div class="min-w-0 flex-1 py-1">
          <p class="m-0 line-clamp-2 font-serif text-lg leading-snug font-semibold">
            {{ book.title }}
          </p>
          <p class="mt-1 mb-0 truncate text-xs text-muted-foreground">
            {{
              book.author_full_name ||
              book.author_username ||
              t('home.catalog.states.unknownAuthor')
            }}
          </p>
          <p class="mt-5 mb-0 text-[11px] text-muted-foreground">
            {{ t('home.catalog.details.updated') }}: {{ displayDate(book.updated_at) }}
          </p>
        </div>
        <span
          class="absolute top-1/2 right-3 flex size-7 -translate-y-1/2 items-center justify-center rounded-full bg-secondary text-muted-foreground opacity-0 transition group-hover:opacity-100 group-focus-visible:opacity-100"
        >
          <ChevronRight aria-hidden="true" class="size-4" />
        </span>
      </RouterLink>
    </div>
  </section>
</template>

<style scoped>
.continue-card {
  box-shadow: 0 12px 28px -22px color-mix(in oklab, var(--foreground) 35%, transparent);
}
</style>
