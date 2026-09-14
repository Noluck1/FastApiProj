<script setup lang="ts">
import { LogOut } from '@lucide/vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

import { Button } from '@/shared/ui/button'
import { ThemeToggle } from '@/shared/ui/theme-toggle'

export type NavigationSection = 'catalog' | 'new' | 'mine' | 'created'

const props = defineProps<{
  activeSection: NavigationSection | null
  canCreate: boolean
  username: string | null
  isLoggingOut: boolean
}>()

const emit = defineEmits<{ logout: [] }>()
const { t } = useI18n()

const navigation = computed<NavigationSection[]>(() => [
  'catalog',
  'new',
  'mine',
  ...(props.canCreate ? (['created'] as const) : []),
])
</script>

<template>
  <header
    class="sticky top-0 z-40 -mx-4 grid min-w-0 grid-cols-[minmax(0,1fr)_auto] items-center gap-x-3 gap-y-2 border-b border-border/80 bg-background/90 px-4 py-3 backdrop-blur-xl sm:-mx-6 sm:px-6 lg:grid-cols-[auto_minmax(0,1fr)_auto] lg:gap-5"
  >
    <RouterLink
      class="flex w-fit min-w-0 items-center gap-2.5 font-serif text-xl font-semibold tracking-tight text-foreground no-underline"
      :to="{ name: 'home' }"
    >
      <span
        aria-hidden="true"
        class="flex size-9 shrink-0 items-end justify-center gap-0.5 rounded-full bg-primary p-2 text-primary-foreground shadow-sm"
      >
        <span class="h-2.5 w-0.5 rounded-full bg-current"></span>
        <span class="h-4 w-0.5 rounded-full bg-current"></span>
        <span class="h-3 w-0.5 rounded-full bg-current"></span>
      </span>
      <span class="truncate">{{ t('common.appName') }}</span>
    </RouterLink>

    <nav
      class="order-3 col-span-2 flex min-w-0 gap-1 overflow-x-auto lg:order-none lg:col-span-1 lg:justify-center lg:overflow-visible"
      :aria-label="t('common.navigation.label')"
    >
      <Button
        v-for="item in navigation"
        :key="item"
        as-child
        size="sm"
        :variant="activeSection === item ? 'secondary' : 'ghost'"
        class="h-9 min-w-fit rounded-full px-4 leading-tight"
      >
        <RouterLink
          :aria-current="activeSection === item ? 'page' : undefined"
          :to="{ name: 'home', query: item === 'catalog' ? {} : { section: item } }"
        >
          {{ t(`common.navigation.${item}`) }}
        </RouterLink>
      </Button>
    </nav>

    <div class="flex min-w-0 items-center justify-end gap-1 sm:gap-2">
      <ThemeToggle />
      <Button
        v-if="username"
        type="button"
        size="icon"
        variant="outline"
        class="size-9 rounded-full"
        :disabled="isLoggingOut"
        :aria-label="t('auth.profile.logout')"
        :title="t('auth.profile.logout')"
        @click="emit('logout')"
      >
        <LogOut aria-hidden="true" />
      </Button>
      <template v-else>
        <Button as-child size="sm" variant="ghost" class="h-9 rounded-full px-2.5 sm:px-4">
          <RouterLink :to="{ name: 'login' }">{{ t('auth.login.title') }}</RouterLink>
        </Button>
        <Button as-child size="sm" variant="outline" class="h-9 rounded-full px-2.5 sm:px-4">
          <RouterLink :to="{ name: 'register' }">{{ t('auth.register.title') }}</RouterLink>
        </Button>
      </template>
    </div>
  </header>
</template>
