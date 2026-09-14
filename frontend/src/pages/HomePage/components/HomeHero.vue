<script setup lang="ts">
import { ArrowRight, BookOpen, Sparkles } from '@lucide/vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

import { Button } from '@/shared/ui'

import type { Book, CatalogSection } from '../types'
import BookCover from './BookCover.vue'

const props = defineProps<{
  books: Book[]
  section: CatalogSection
  total: number
}>()

const { t } = useI18n()
const featuredBooks = computed(() => props.books.slice(0, 3))
const primaryBook = computed(() => featuredBooks.value[0] ?? null)

function scrollToCatalog() {
  document.querySelector('#popular')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
</script>

<template>
  <section
    id="catalog"
    class="mx-auto max-w-[1440px] px-4 pt-6 pb-8 sm:px-7 sm:pt-8 lg:px-10 lg:pb-12"
  >
    <div
      class="hero-grid relative overflow-hidden rounded-[28px] bg-hero px-6 py-8 text-hero-foreground sm:px-10 sm:py-10 lg:min-h-[430px] lg:px-14 lg:py-12"
    >
      <div class="hero-grain absolute inset-0 opacity-30" />
      <div class="relative z-10 max-w-[42rem]">
        <span
          class="mb-5 inline-flex items-center rounded-full bg-hero-badge px-3 py-1 text-xs font-semibold text-hero-badge-foreground backdrop-blur"
        >
          <Sparkles aria-hidden="true" class="mr-1.5 size-3.5" />
          {{ t('home.landing.hero.badge') }}
        </span>
        <h1
          class="m-0 text-balance font-serif text-[42px] leading-[0.98] font-semibold tracking-[-0.045em] sm:text-6xl lg:text-[72px]"
        >
          {{ t('home.landing.hero.titleFirst') }}<br class="hidden sm:block" />
          {{ t('home.landing.hero.titleSecond') }}
        </h1>
        <p class="mt-5 max-w-[32rem] text-base leading-relaxed text-hero-muted sm:text-lg">
          {{ t('home.landing.hero.description') }}
        </p>
        <div class="mt-7 flex flex-wrap gap-3">
          <Button v-if="primaryBook" as-child class="h-10 rounded-md px-4">
            <RouterLink
              :to="{
                name: 'book',
                params: { id: primaryBook.id },
                query: { from: props.section },
              }"
            >
              <BookOpen aria-hidden="true" class="size-[18px]" />
              {{ t('home.catalog.actions.open') }}
            </RouterLink>
          </Button>
          <Button
            type="button"
            variant="outline"
            class="h-10 border-hero-foreground/15 bg-hero-action px-4 text-hero-foreground hover:bg-hero-action-hover hover:text-hero-foreground"
            @click="scrollToCatalog"
          >
            {{ t('home.landing.hero.catalogAction') }}
            <ArrowRight aria-hidden="true" class="size-4" />
          </Button>
        </div>
        <div class="mt-9 flex min-w-0 items-center gap-4 text-sm text-hero-muted">
          <div class="flex shrink-0 -space-x-2" aria-hidden="true">
            <span class="reader-dot reader-dot--one" />
            <span class="reader-dot reader-dot--two" />
            <span class="reader-dot reader-dot--three" />
            <span
              class="flex size-8 items-center justify-center rounded-full border-2 border-hero bg-card text-[9px] font-bold text-hero-foreground"
            >
              {{ total > 99 ? '99+' : total }}
            </span>
          </div>
          <span class="min-w-0 leading-snug">
            <strong class="text-hero-foreground">{{ total }}</strong>
            {{ t('home.landing.hero.booksCount') }}
          </span>
        </div>
      </div>

      <div
        v-if="featuredBooks.length"
        class="hero-books pointer-events-none relative z-10 mt-12 hidden min-h-[320px] lg:block"
        aria-hidden="true"
      >
        <div
          v-for="(book, index) in featuredBooks"
          :key="book.id"
          class="hero-book"
          :class="`hero-book--${index + 1}`"
        >
          <BookCover :book="book" />
        </div>
        <div class="hero-shadow absolute right-[18%] bottom-3 h-5 w-[72%] rounded-[50%] blur-xl" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(400px, 0.8fr);
}

.hero-grain {
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.16'/%3E%3C/svg%3E");
}

.hero-book {
  position: absolute;
  width: 155px;
  filter: drop-shadow(0 25px 22px var(--cover-shadow-soft));
  transition: transform 220ms ease;
}

.hero-book--1 {
  bottom: 5%;
  left: 10%;
  z-index: 3;
  transform: rotate(-9deg);
}
.hero-book--2 {
  bottom: 8%;
  left: 39%;
  z-index: 4;
  transform: rotate(4deg);
}
.hero-book--3 {
  bottom: 6%;
  left: 66%;
  z-index: 2;
  transform: rotate(12deg);
}
.hero-shadow {
  background: color-mix(in oklab, var(--hero-foreground) 20%, transparent);
}
.reader-dot {
  display: block;
  width: 2rem;
  height: 2rem;
  border: 2px solid var(--hero);
  border-radius: 9999px;
}
.reader-dot--one {
  background: var(--cover-2);
}
.reader-dot--two {
  background: var(--cover-1);
}
.reader-dot--three {
  background: var(--cover-6);
}

@media (max-width: 1023px) {
  .hero-grid {
    display: block;
  }
}

@media (max-width: 639px) {
  .hero-grid {
    border-radius: 22px;
  }
}
</style>
