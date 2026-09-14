<script setup lang="ts">
import { ChevronDown } from '@lucide/vue'
import { useI18n } from 'vue-i18n'

import { Button } from '@/shared/ui'

const props = defineProps<{
  hasMore: boolean
  isLoading: boolean
  shown: number
  total: number
}>()

const emit = defineEmits<{ load: [] }>()
const { t } = useI18n()
</script>

<template>
  <footer class="grid justify-items-center gap-3 border-t border-border pt-7 pb-4 text-center">
    <p class="m-0 text-sm text-muted-foreground">
      {{ t('home.catalog.states.shown', { shown: props.shown, total: props.total }) }}
    </p>
    <Button
      v-if="props.hasMore"
      type="button"
      variant="outline"
      class="h-11 w-full rounded-full bg-card px-6 sm:w-auto"
      :disabled="props.isLoading"
      :aria-busy="props.isLoading"
      @click="emit('load')"
    >
      <ChevronDown aria-hidden="true" />
      {{
        props.isLoading ? t('home.catalog.actions.loadingMore') : t('home.catalog.actions.loadMore')
      }}
    </Button>
    <p v-else-if="props.total > 0" class="m-0 text-sm text-muted-foreground">
      {{ t('home.catalog.states.allShown') }}
    </p>
  </footer>
</template>
