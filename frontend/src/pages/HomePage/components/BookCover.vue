<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

import type { Book } from '../types'

const props = withDefaults(
  defineProps<{
    book: Book
    compact?: boolean
  }>(),
  { compact: false },
)

const { t } = useI18n()

const coverTone = computed(
  () => `book-cover--${((Math.max(1, Math.abs(props.book.id)) - 1) % 6) + 1}`,
)
const author = computed(
  () =>
    props.book.author_full_name ||
    props.book.author_username ||
    t('home.catalog.states.unknownAuthor'),
)
const mark = computed(() => props.book.title.trim().charAt(0).toLocaleUpperCase() || '#')
</script>

<template>
  <div
    class="book-cover group/cover relative isolate aspect-[2/3] w-full overflow-hidden rounded-[5px_13px_13px_5px]"
    :class="coverTone"
  >
    <div
      class="absolute inset-y-0 left-0 z-20 w-[7%] border-r border-cover-highlight/15 bg-cover-shadow/10 shadow-[inset_-2px_0_4px_color-mix(in_oklab,var(--cover-shadow)_20%,transparent)]"
    />
    <div
      class="absolute -top-6 -right-10 size-36 rounded-full border-[22px] border-current opacity-15"
    />
    <div
      class="absolute -bottom-14 -left-10 size-36 rotate-45 border-[18px] border-current opacity-10"
    />
    <div class="relative z-10 flex h-full flex-col px-[14%] py-[12%]">
      <div
        class="line-clamp-2 text-[9px] font-bold tracking-[0.18em] uppercase opacity-80 sm:text-[10px]"
      >
        {{ author }}
      </div>
      <div
        class="my-auto line-clamp-4 break-words font-serif text-[clamp(1rem,1.8vw,1.55rem)] font-semibold leading-[1.05] tracking-tight"
      >
        {{ book.title }}
      </div>
      <div class="flex items-end justify-between border-t border-current/40 pt-3">
        <span class="font-serif text-xl font-bold opacity-90">{{ mark }}</span>
        <span
          v-if="!props.compact"
          class="text-[8px] font-bold tracking-widest uppercase opacity-60"
        >
          {{ t('common.appName') }}
        </span>
      </div>
    </div>
    <div
      class="absolute inset-0 bg-gradient-to-br from-cover-highlight/15 via-transparent to-cover-shadow/20 transition-opacity group-hover/cover:opacity-70"
    />
  </div>
</template>

<style scoped>
.book-cover {
  box-shadow:
    0 24px 35px -18px var(--cover-shadow-color),
    2px 4px 8px var(--cover-shadow-soft);
}

.book-cover--1 {
  background: var(--cover-1);
  color: var(--cover-1-ink);
}

.book-cover--2 {
  background: var(--cover-2);
  color: var(--cover-2-ink);
}

.book-cover--3 {
  background: var(--cover-3);
  color: var(--cover-3-ink);
}

.book-cover--4 {
  background: var(--cover-4);
  color: var(--cover-4-ink);
}

.book-cover--5 {
  background: var(--cover-5);
  color: var(--cover-5-ink);
}

.book-cover--6 {
  background: var(--cover-6);
  color: var(--cover-6-ink);
}
</style>
