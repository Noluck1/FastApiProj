<script setup lang="ts">
import {
  BookOpen,
  ChevronRight,
  Compass,
  Home,
  Library,
  LogIn,
  LogOut,
  Menu,
  Search,
  UserRound,
  X,
} from '@lucide/vue'
import { computed, ref, type Component } from 'vue'
import { useI18n } from 'vue-i18n'

import { Button, Input, ThemeToggle } from '@/shared/ui'

import type { CatalogSection } from '../types'

const props = defineProps<{
  activeSection: CatalogSection
  canCreate: boolean
  isLoggingOut: boolean
  search: string
  username: string | null
}>()

const emit = defineEmits<{
  logout: []
  'update:search': [value: string]
}>()

const { t } = useI18n()
const mobileMenu = ref(false)

type NavigationItem = {
  icon: Component
  section: CatalogSection
  label: string
}

const navigation = computed<NavigationItem[]>(() => [
  { icon: Home, section: 'catalog', label: 'home.landing.navigation.home' },
  { icon: Compass, section: 'new', label: 'common.navigation.new' },
  { icon: Library, section: 'mine', label: 'common.navigation.mine' },
  ...(props.canCreate
    ? [{ icon: BookOpen, section: 'created' as const, label: 'common.navigation.created' }]
    : []),
])

function handleSearchInput(event: Event) {
  emit('update:search', (event.target as HTMLInputElement).value)
}

function closeMobileMenu() {
  mobileMenu.value = false
}
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-border/70 bg-background/85 backdrop-blur-xl">
    <div class="mx-auto flex h-[72px] max-w-[1440px] items-center gap-3 px-4 sm:px-7 lg:px-10">
      <RouterLink
        class="mr-1 flex shrink-0 items-center gap-2.5 text-foreground no-underline"
        :to="{ name: 'home' }"
        :aria-label="t('home.landing.navigation.home')"
      >
        <span class="logo-mark"><span /><span /><span /></span>
        <span class="font-serif text-xl font-semibold tracking-tight">{{
          t('common.appName')
        }}</span>
      </RouterLink>

      <nav
        class="ml-6 hidden items-center gap-1 lg:flex"
        :aria-label="t('common.navigation.label')"
      >
        <Button
          v-for="item in navigation"
          :key="item.section"
          as-child
          variant="ghost"
          class="h-10 rounded-full px-4 text-sm font-semibold"
          :class="
            props.activeSection === item.section
              ? 'bg-secondary text-foreground'
              : 'text-muted-foreground'
          "
        >
          <RouterLink
            :to="{
              name: 'home',
              query: item.section === 'catalog' ? {} : { section: item.section },
            }"
            :aria-current="props.activeSection === item.section ? 'page' : undefined"
          >
            {{ t(item.label) }}
          </RouterLink>
        </Button>
      </nav>

      <label class="group relative ml-auto hidden w-full max-w-[380px] sm:block">
        <Search
          class="pointer-events-none absolute top-1/2 left-4 size-[18px] -translate-y-1/2 text-muted-foreground transition-colors group-focus-within:text-primary"
          aria-hidden="true"
        />
        <Input
          class="h-11 w-full rounded-full border-transparent bg-secondary/80 pr-5 pl-11 text-sm shadow-none focus-visible:border-primary/30 focus-visible:bg-background focus-visible:ring-4 focus-visible:ring-primary/10"
          type="search"
          :value="props.search"
          :placeholder="t('home.landing.searchPlaceholder')"
          :aria-label="t('home.catalog.search.label')"
          @input="handleSearchInput"
        />
      </label>

      <ThemeToggle />

      <div class="hidden items-center gap-1 sm:flex">
        <template v-if="props.username">
          <Button
            class="hidden max-w-36 truncate rounded-full bg-secondary px-3 py-2 text-xs font-semibold text-foreground xl:block"
            as-child
            size="sm"
            variant="secondary"
          >
            <RouterLink :to="{ name: 'profile' }" :title="props.username">
              <UserRound aria-hidden="true" />
              <span class="truncate"></span>
            </RouterLink>
          </Button>
        </template>
        <Button v-else as-child variant="secondary" size="icon" class="size-9 rounded-full">
          <RouterLink :to="{ name: 'login' }" :aria-label="t('auth.login.title')">
            <UserRound aria-hidden="true" />
          </RouterLink>
        </Button>
      </div>

      <Button
        type="button"
        variant="ghost"
        size="icon"
        class="size-9 rounded-full lg:hidden"
        :aria-label="t('home.landing.navigation.openMenu')"
        @click="mobileMenu = true"
      >
        <Menu aria-hidden="true" class="size-5" />
      </Button>
    </div>

    <div class="border-t border-border/70 px-4 py-3 sm:hidden">
      <label class="relative block">
        <Search
          class="pointer-events-none absolute top-1/2 left-4 size-[17px] -translate-y-1/2 text-muted-foreground"
          aria-hidden="true"
        />
        <Input
          class="h-10 w-full rounded-full border-transparent bg-secondary/80 pr-4 pl-11 text-sm shadow-none focus-visible:bg-background"
          type="search"
          :value="props.search"
          :placeholder="t('home.catalog.search.placeholder')"
          :aria-label="t('home.catalog.search.label')"
          @input="handleSearchInput"
        />
      </label>
    </div>
  </header>

  <Transition name="drawer-fade">
    <div
      v-if="mobileMenu"
      class="fixed inset-0 z-50 bg-overlay backdrop-blur-sm lg:hidden"
      @click.self="closeMobileMenu"
    >
      <aside
        class="ml-auto flex h-full w-[82%] max-w-[24rem] flex-col bg-background p-5 shadow-2xl"
        role="dialog"
        aria-modal="true"
        :aria-label="t('home.landing.navigation.menu')"
      >
        <div class="flex items-center justify-between">
          <span class="flex items-center gap-2.5 font-serif text-xl font-semibold">
            <span class="logo-mark"><span /><span /><span /></span>
            {{ t('common.appName') }}
          </span>
          <Button
            type="button"
            variant="ghost"
            size="icon"
            class="rounded-full"
            :aria-label="t('home.landing.navigation.closeMenu')"
            @click="closeMobileMenu"
          >
            <X aria-hidden="true" class="size-5" />
          </Button>
        </div>

        <nav class="mt-10 grid gap-2" :aria-label="t('common.navigation.label')">
          <RouterLink
            v-for="item in navigation"
            :key="item.section"
            :to="{
              name: 'home',
              query: item.section === 'catalog' ? {} : { section: item.section },
            }"
            class="mobile-link"
            :class="props.activeSection === item.section && 'bg-secondary text-foreground'"
            @click="closeMobileMenu"
          >
            <component :is="item.icon" class="size-5" aria-hidden="true" />
            {{ t(item.label) }}
            <ChevronRight class="ml-auto size-4" aria-hidden="true" />
          </RouterLink>
        </nav>

        <div class="mt-auto rounded-2xl bg-secondary p-4">
          <template v-if="props.username">
            <RouterLink
              class="flex min-w-0 items-center gap-2 font-serif text-lg font-semibold text-foreground no-underline"
              :to="{ name: 'profile' }"
              :title="props.username"
              @click="closeMobileMenu"
            >
              <UserRound class="size-5 shrink-0" aria-hidden="true" />
              <span class="truncate">{{ props.username }}</span>
            </RouterLink>
            <p class="mt-1 text-sm text-muted-foreground">{{ t('home.landing.profileHint') }}</p>
            <Button
              type="button"
              variant="outline"
              class="mt-4 w-full rounded-full"
              :disabled="props.isLoggingOut"
              @click="emit('logout')"
            >
              <LogOut aria-hidden="true" />
              {{ t('auth.profile.logout') }}
            </Button>
          </template>
          <template v-else>
            <p class="font-serif text-lg font-semibold">{{ t('home.landing.saveBooks') }}</p>
            <p class="mt-1 text-sm text-muted-foreground">{{ t('home.landing.loginHint') }}</p>
            <Button as-child class="mt-4 w-full rounded-full">
              <RouterLink :to="{ name: 'login' }" @click="closeMobileMenu">
                <LogIn aria-hidden="true" />
                {{ t('auth.login.title') }}
              </RouterLink>
            </Button>
          </template>
        </div>
      </aside>
    </div>
  </Transition>
</template>

<style scoped>
.logo-mark {
  position: relative;
  display: flex;
  width: 2rem;
  height: 2rem;
  align-items: flex-end;
  justify-content: center;
  gap: 2px;
  border-radius: 9999px;
  background: var(--primary);
  padding: 7px;
  color: var(--primary-foreground);
}

.logo-mark span {
  display: block;
  width: 3px;
  border-radius: 9999px;
  background: currentColor;
}

.logo-mark span:nth-child(1) {
  height: 52%;
}
.logo-mark span:nth-child(2) {
  height: 90%;
}
.logo-mark span:nth-child(3) {
  height: 68%;
}

.mobile-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-radius: 1rem;
  padding: 0.875rem 1rem;
  color: var(--foreground);
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 180ms ease;
}

.mobile-link:hover {
  background: var(--secondary);
}
.drawer-fade-enter-active,
.drawer-fade-leave-active {
  transition: opacity 250ms ease;
}
.drawer-fade-enter-active > *,
.drawer-fade-leave-active > * {
  transition: transform 300ms ease;
}
.drawer-fade-enter-from,
.drawer-fade-leave-to {
  opacity: 0;
}
.drawer-fade-enter-from > *,
.drawer-fade-leave-to > * {
  transform: translateX(24px);
}
</style>
