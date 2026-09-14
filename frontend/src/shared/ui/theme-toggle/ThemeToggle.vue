<script setup lang="ts">
import { useI18n } from 'vue-i18n'

import { useThemeStore } from '@/shared/stores/theme.store'
import { Button } from '@/shared/ui/button'

const themeStore = useThemeStore()
const { t } = useI18n()
</script>

<template>
  <Button
    type="button"
    size="icon"
    variant="ghost"
    class="theme-toggle"
    :class="{ 'theme-toggle--dark': themeStore.isDark }"
    :aria-pressed="themeStore.isDark"
    :aria-label="themeStore.isDark ? t('common.theme.light') : t('common.theme.dark')"
    :title="themeStore.isDark ? t('common.theme.light') : t('common.theme.dark')"
    @click="themeStore.toggleTheme()"
  >
    <span class="theme-toggle__handler" aria-hidden="true">
      <span class="theme-toggle__crater theme-toggle__crater--1"></span>
      <span class="theme-toggle__crater theme-toggle__crater--2"></span>
      <span class="theme-toggle__crater theme-toggle__crater--3"></span>
    </span>
    <span class="theme-toggle__star theme-toggle__star--1" aria-hidden="true"></span>
    <span class="theme-toggle__star theme-toggle__star--2" aria-hidden="true"></span>
    <span class="theme-toggle__star theme-toggle__star--3" aria-hidden="true"></span>
    <span class="theme-toggle__star theme-toggle__star--4" aria-hidden="true"></span>
    <span class="theme-toggle__star theme-toggle__star--5" aria-hidden="true"></span>
    <span class="theme-toggle__star theme-toggle__star--6" aria-hidden="true"></span>
  </Button>
</template>

<style scoped>
.theme-toggle {
  position: relative;
  display: inline-block;
  width: 64px;
  height: 36px;
  overflow: hidden;
  padding: 0;
  border: 0;
  border-radius: 60px;
  background-color: #83d8ff;
  transition: background-color 350ms cubic-bezier(0.445, 0.05, 0.55, 0.95);
}

.theme-toggle:hover {
  background-color: #83d8ff;
}

.theme-toggle--dark,
.theme-toggle--dark:hover {
  background-color: #749dd6;
}

.theme-toggle__handler {
  position: absolute;
  z-index: 1;
  top: 2px;
  left: 2px;
  display: block;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #ffcf96;
  box-shadow: 0 2px 5px rgb(0 0 0 / 30%);
  transform: rotate(-45deg);
  transition:
    transform 500ms cubic-bezier(0.68, -0.55, 0.265, 1.55),
    background-color 350ms ease-in-out;
}

.theme-toggle__crater {
  position: absolute;
  border-radius: 100%;
  background-color: #e8cda5;
  opacity: 0;
  transition: opacity 300ms ease-in-out;
}

.theme-toggle__crater--1 {
  top: 13px;
  left: 7px;
  width: 3px;
  height: 3px;
}

.theme-toggle__crater--2 {
  top: 20px;
  left: 16px;
  width: 4px;
  height: 4px;
}

.theme-toggle__crater--3 {
  top: 7px;
  left: 18px;
  width: 6px;
  height: 6px;
}

.theme-toggle__star {
  position: absolute;
  border-radius: 50%;
  background-color: #ffffff;
  transition: all 400ms cubic-bezier(0.445, 0.05, 0.55, 0.95);
}

.theme-toggle__star--1 {
  z-index: 0;
  top: 7px;
  left: 25px;
  width: 21px;
  height: 2px;
}

.theme-toggle__star--2 {
  z-index: 1;
  top: 13px;
  left: 20px;
  width: 21px;
  height: 2px;
}

.theme-toggle__star--3 {
  z-index: 0;
  top: 19px;
  left: 28px;
  width: 21px;
  height: 2px;
}

.theme-toggle__star--4,
.theme-toggle__star--5,
.theme-toggle__star--6 {
  opacity: 0;
  transform: translate3d(2px, 0, 0);
  transition-delay: 0ms;
}

.theme-toggle__star--4 {
  z-index: 0;
  top: 11px;
  left: 8px;
  width: 2px;
  height: 2px;
}

.theme-toggle__star--5 {
  z-index: 0;
  top: 23px;
  left: 12px;
  width: 2px;
  height: 2px;
}

.theme-toggle__star--6 {
  z-index: 0;
  top: 26px;
  left: 20px;
  width: 2px;
  height: 2px;
}

.theme-toggle--dark .theme-toggle__handler {
  background-color: #ffe5b5;
  transform: translate3d(28px, 0, 0) rotate(0deg);
}

.theme-toggle--dark .theme-toggle__crater {
  opacity: 1;
}

.theme-toggle--dark .theme-toggle__star--1 {
  width: 2px;
  height: 2px;
}

.theme-toggle--dark .theme-toggle__star--2 {
  width: 3px;
  height: 3px;
  transform: translate3d(-4px, 0, 0);
}

.theme-toggle--dark .theme-toggle__star--3 {
  width: 2px;
  height: 2px;
  transform: translate3d(-5px, 0, 0);
}

.theme-toggle--dark .theme-toggle__star--4,
.theme-toggle--dark .theme-toggle__star--5,
.theme-toggle--dark .theme-toggle__star--6 {
  opacity: 1;
  transform: translate3d(0, 0, 0);
}

.theme-toggle--dark .theme-toggle__star--4 {
  transition-delay: 200ms;
}

.theme-toggle--dark .theme-toggle__star--5 {
  transition-delay: 300ms;
}

.theme-toggle--dark .theme-toggle__star--6 {
  transition-delay: 400ms;
}
</style>
