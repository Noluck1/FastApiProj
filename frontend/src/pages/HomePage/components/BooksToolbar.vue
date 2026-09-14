<script setup lang="ts">
import { ArrowDownUp } from '@lucide/vue'
import { useI18n } from 'vue-i18n'

import { Button } from '@/shared/ui'

import type { BookSortBy, BookStatusFilter, SortOrder } from '../types'

const props = defineProps<{
  showStatusFilter: boolean
  statusFilter: BookStatusFilter
  sortBy: BookSortBy
  sortOrder: SortOrder
}>()

const emit = defineEmits<{
  'update:status-filter': [value: BookStatusFilter]
  'update:sort-by': [value: BookSortBy]
  'toggle:sort-order': []
}>()

const { t } = useI18n()

const statusFilters: BookStatusFilter[] = ['active', 'all', 'deleted']
const sortFields: BookSortBy[] = ['updated_at', 'created_at']
</script>

<template>
  <section class="mx-auto max-w-[1440px] px-4 py-5 sm:px-7 lg:px-10">
    <div class="scrollbar-none flex min-w-0 gap-2 overflow-x-auto pb-2">
      <Button
        v-for="filter in props.showStatusFilter ? statusFilters : []"
        :key="filter"
        type="button"
        variant="outline"
        class="genre-chip h-10 shrink-0 rounded-full px-5 text-sm font-semibold"
        :class="props.statusFilter === filter && 'genre-chip--active'"
        :aria-pressed="props.statusFilter === filter"
        @click="emit('update:status-filter', filter)"
      >
        {{ t(`home.catalog.filters.${filter}`) }}
      </Button>

      <span v-if="props.showStatusFilter" class="my-1 w-px shrink-0 bg-border" aria-hidden="true" />

      <Button
        v-for="field in sortFields"
        :key="field"
        type="button"
        variant="outline"
        class="genre-chip h-10 shrink-0 rounded-full px-5 text-sm font-semibold"
        :class="props.sortBy === field && 'genre-chip--active'"
        :aria-pressed="props.sortBy === field"
        @click="emit('update:sort-by', field)"
      >
        {{ t(`home.catalog.sort.${field}`) }}
      </Button>

      <Button
        type="button"
        variant="outline"
        class="genre-chip h-10 shrink-0 rounded-full px-5 text-sm font-semibold"
        @click="emit('toggle:sort-order')"
      >
        <ArrowDownUp aria-hidden="true" />
        {{
          props.sortOrder === 'asc'
            ? t('home.catalog.sort.ascending')
            : t('home.catalog.sort.descending')
        }}
      </Button>
    </div>
  </section>
</template>

<style scoped>
.genre-chip {
  border-color: var(--border);
  background: var(--card);
  color: var(--muted-foreground);
  box-shadow: var(--shadow-sm);
}

.genre-chip:hover {
  border-color: color-mix(in oklab, var(--primary) 30%, transparent);
  color: var(--foreground);
}

.genre-chip--active {
  border-color: var(--primary);
  background: var(--primary);
  color: var(--primary-foreground);
}

.scrollbar-none {
  scrollbar-width: none;
}
.scrollbar-none::-webkit-scrollbar {
  display: none;
}
</style>
