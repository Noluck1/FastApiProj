<script setup lang="ts">
import { useI18n } from 'vue-i18n'

import { Button } from '@/shared/ui'

const props = defineProps<{
  page: number
  pageSize: number
  total: number
  totalPages: number
  isFirstPage: boolean
  isLastPage: boolean
}>()

const emit = defineEmits<{
  previous: []
  next: []
  'update:page-size': [value: number]
}>()

const { t } = useI18n()

function handlePageSizeChange(event: Event) {
  emit('update:page-size', Number((event.target as HTMLSelectElement).value))
}
</script>

<template>
  <footer
    class="flex flex-col gap-4 border-t border-border px-1 pt-5 text-sm text-muted-foreground sm:flex-row sm:items-center sm:justify-between"
  >
    <div class="flex flex-wrap items-center gap-3">
      <span>{{ t('home.catalog.pagination.total', { count: props.total }) }}</span>
      <label class="flex items-center gap-2">
        <span>{{ t('home.catalog.pagination.pageSize') }}</span>
        <select
          class="h-9 rounded-xl border border-input bg-background px-3 text-sm text-foreground outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
          :value="props.pageSize"
          @change="handlePageSizeChange"
        >
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
        </select>
      </label>
    </div>

    <div class="flex items-center justify-between gap-3 sm:justify-end">
      <Button
        type="button"
        size="sm"
        variant="outline"
        :disabled="props.isFirstPage"
        @click="emit('previous')"
      >
        {{ t('home.catalog.pagination.previous') }}
      </Button>
      <span class="shrink-0 text-foreground">
        {{ t('home.catalog.pagination.page', { page: props.page, total: props.totalPages || 1 }) }}
      </span>
      <Button
        type="button"
        size="sm"
        variant="outline"
        :disabled="props.isLastPage"
        @click="emit('next')"
      >
        {{ t('home.catalog.pagination.next') }}
      </Button>
    </div>
  </footer>
</template>
