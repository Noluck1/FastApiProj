<script setup lang="ts">
import { ArrowRight, Bookmark, BookmarkCheck, BookPlus, Search } from '@lucide/vue'
import { useI18n } from 'vue-i18n'

import { formatDate } from '@/shared/lib/format/date'
import { Button, Card, CardContent } from '@/shared/ui'

import type { Book, CatalogSection } from '../types'
import BookCover from './BookCover.vue'

const props = defineProps<{
  books: Book[]
  isLoading: boolean
  error: string | null
  pendingDeleteBookId: number | null
  deletingBookId: number | null
  favoriteSavingBookId: number | null
  favoriteBookIds: ReadonlySet<number>
  isAuthenticated: boolean
  requiresLogin: boolean
  search: string
  section: CatalogSection
  total: number
  canCreate: boolean
  canManageBook: (book: Book) => boolean
}>()

const emit = defineEmits<{
  create: []
  retry: []
  edit: [book: Book]
  'request-delete': [book: Book]
  'cancel-delete': []
  'confirm-delete': [book: Book]
  'toggle-favorite': [book: Book]
}>()

const { t, locale } = useI18n()

function displayDate(value: string): string {
  return formatDate(new Date(value), locale.value === 'ru' ? 'ru-RU' : 'en-US')
}

function scrollToStart() {
  document.querySelector('#popular')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
</script>

<template>
  <section
    id="popular"
    class="mx-auto max-w-[1440px] scroll-mt-24 px-4 py-10 sm:px-7 lg:px-10 lg:pb-20"
    aria-live="polite"
    :aria-busy="props.isLoading"
  >
    <div class="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-end">
      <div class="min-w-0 flex-1">
        <p class="m-0 text-[11px] font-bold tracking-[0.18em] text-primary uppercase">
          {{ t(`home.catalog.sections.${props.section}Subtitle`) }}
        </p>
        <h2
          class="mt-1 mb-0 font-serif text-[28px] leading-tight font-semibold tracking-[-0.025em] sm:text-3xl"
        >
          {{
            props.search
              ? t('home.landing.catalog.searchResults')
              : t(`home.catalog.sections.${props.section}Title`)
          }}
        </h2>
      </div>
      <Button
        v-if="props.section === 'created' && props.canCreate"
        type="button"
        variant="secondary"
        class="h-10 shrink-0 rounded-full px-4"
        @click="emit('create')"
      >
        <BookPlus aria-hidden="true" class="size-4" />
        {{ t('home.catalog.actions.create') }}
      </Button>
      <Button
        v-else
        type="button"
        variant="ghost"
        class="hidden h-9 rounded-full px-3 text-muted-foreground sm:inline-flex"
        @click="scrollToStart"
      >
        {{ t('home.landing.catalog.allCatalog', { count: props.total }) }}
        <ArrowRight aria-hidden="true" class="size-4" />
      </Button>
    </div>

    <Card v-if="props.isLoading" class="mt-7 rounded-[24px] border-dashed">
      <CardContent class="py-16 text-center text-sm text-muted-foreground">
        {{ t('home.catalog.states.loading') }}
      </CardContent>
    </Card>

    <Card v-else-if="props.error" class="mt-7 rounded-[24px] border-dashed">
      <CardContent class="grid justify-items-center gap-4 py-16 text-center">
        <p role="alert" class="m-0 text-sm text-destructive">{{ props.error }}</p>
        <Button type="button" variant="outline" class="rounded-full" @click="emit('retry')">
          {{ t('home.catalog.actions.retry') }}
        </Button>
      </CardContent>
    </Card>

    <Card v-else-if="props.books.length === 0" class="mt-7 rounded-[24px] border-dashed">
      <CardContent class="py-16 text-center">
        <Search class="mx-auto size-8 text-muted-foreground" aria-hidden="true" />
        <h3 class="mt-4 mb-0 font-serif text-xl font-semibold text-foreground">
          {{ t('home.catalog.states.emptyTitle') }}
        </h3>
        <p class="mt-1 mb-0 text-sm text-muted-foreground">
          {{
            props.requiresLogin
              ? t('home.catalog.states.mineRequiresLogin')
              : t('home.catalog.states.emptyDescription')
          }}
        </p>
        <Button v-if="props.requiresLogin" as-child class="mt-5 rounded-full">
          <RouterLink :to="{ name: 'login' }">{{ t('auth.login.title') }}</RouterLink>
        </Button>
      </CardContent>
    </Card>

    <TransitionGroup
      v-else
      name="books"
      tag="div"
      class="mt-7 grid grid-cols-2 gap-x-4 gap-y-9 sm:grid-cols-3 sm:gap-x-6 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6"
    >
      <article v-for="book in props.books" :key="book.id" class="book-card group min-w-0">
        <RouterLink
          class="relative block w-full rounded-[5px_13px_13px_5px] text-left focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-primary/20"
          :to="{ name: 'book', params: { id: book.id }, query: { from: props.section } }"
          :aria-label="`${t('home.catalog.actions.open')}: ${book.title}`"
        >
          <BookCover :book="book" />
          <span
            class="absolute inset-0 rounded-[5px_13px_13px_5px] ring-primary/0 transition group-hover:ring-4 group-hover:ring-primary/15"
          />
        </RouterLink>

        <div class="mt-4 flex min-w-0 items-start gap-2">
          <RouterLink
            class="min-w-0 flex-1 text-left text-foreground no-underline"
            :to="{ name: 'book', params: { id: book.id }, query: { from: props.section } }"
          >
            <h3
              class="m-0 line-clamp-2 break-words font-serif text-base leading-tight font-semibold transition-colors group-hover:text-primary sm:text-lg"
            >
              {{ book.title }}
            </h3>
            <p class="mt-1 mb-0 truncate text-sm text-muted-foreground">
              {{
                book.author_full_name ||
                book.author_username ||
                t('home.catalog.states.unknownAuthor')
              }}
            </p>
          </RouterLink>
          <Button
            v-if="!book.is_deleted"
            type="button"
            size="icon-sm"
            variant="ghost"
            class="mt-0.5 size-8 shrink-0 rounded-full text-muted-foreground"
            :class="
              props.favoriteBookIds.has(book.id)
                ? 'bg-secondary text-primary'
                : !props.isAuthenticated
                  ? 'text-muted-foreground/70'
                  : ''
            "
            :disabled="props.favoriteSavingBookId === book.id"
            :aria-label="
              !props.isAuthenticated
                ? t('auth.login.title')
                : props.favoriteBookIds.has(book.id)
                  ? t('home.catalog.actions.removeFavorite')
                  : t('home.catalog.actions.addFavorite')
            "
            @click="emit('toggle-favorite', book)"
          >
            <BookmarkCheck v-if="props.favoriteBookIds.has(book.id)" aria-hidden="true" />
            <Bookmark v-else aria-hidden="true" />
          </Button>
        </div>

        <div class="mt-2 flex min-w-0 items-center gap-2 text-xs text-muted-foreground">
          <span
            class="shrink-0 font-semibold"
            :class="book.is_deleted ? 'text-destructive' : 'text-positive-foreground'"
          >
            {{
              book.is_deleted ? t('home.catalog.states.deleted') : t('home.catalog.states.active')
            }}
          </span>
          <span aria-hidden="true">·</span>
          <span class="truncate">{{ displayDate(book.updated_at) }}</span>
        </div>

        <div v-if="props.canManageBook(book)" class="mt-3 border-t border-border pt-2">
          <template v-if="props.pendingDeleteBookId === book.id">
            <p class="m-0 text-xs leading-snug text-destructive">
              {{ t('home.catalog.deleteConfirm') }}
            </p>
            <div class="mt-2 flex gap-2">
              <Button
                type="button"
                size="sm"
                variant="outline"
                class="h-auto min-w-0 flex-1 px-2 py-2 text-xs whitespace-normal"
                :disabled="props.deletingBookId === book.id"
                @click="emit('cancel-delete')"
              >
                {{ t('common.cancel') }}
              </Button>
              <Button
                type="button"
                size="sm"
                variant="destructive"
                class="h-auto min-w-0 flex-1 px-2 py-2 text-xs whitespace-normal"
                :disabled="props.deletingBookId === book.id"
                @click="emit('confirm-delete', book)"
              >
                {{
                  props.deletingBookId === book.id
                    ? t('home.catalog.actions.deleting')
                    : t('home.catalog.actions.confirmDelete')
                }}
              </Button>
            </div>
          </template>
          <div v-else class="flex items-center gap-1">
            <Button
              type="button"
              size="sm"
              variant="ghost"
              class="h-8 min-w-0 flex-1 rounded-full px-2 text-xs"
              @click="emit('edit', book)"
            >
              {{ t('home.catalog.actions.edit') }}
            </Button>
            <Button
              type="button"
              size="sm"
              variant="ghost"
              class="h-8 min-w-0 flex-1 rounded-full px-2 text-xs text-destructive hover:text-destructive"
              @click="emit('request-delete', book)"
            >
              {{ t('home.catalog.actions.delete') }}
            </Button>
          </div>
        </div>
      </article>
    </TransitionGroup>
  </section>
</template>

<style scoped>
.books-enter-active,
.books-leave-active {
  transition: all 250ms ease;
}
.books-enter-from,
.books-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
