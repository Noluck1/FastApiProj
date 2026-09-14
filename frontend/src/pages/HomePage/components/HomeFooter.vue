<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <footer class="border-t border-border">
    <div
      class="mx-auto flex max-w-[1440px] flex-col gap-4 px-4 py-8 text-sm text-muted-foreground sm:flex-row sm:items-center sm:px-7 lg:px-10"
    >
      <RouterLink
        class="flex items-center gap-2 font-serif text-base font-semibold text-foreground no-underline"
        :to="{ name: 'home' }"
      >
        <span class="logo-mark"><span /><span /><span /></span>
        {{ t('common.appName') }}
      </RouterLink>
      <p class="m-0 sm:ml-auto">{{ t('home.landing.footer') }}</p>
    </div>
  </footer>
</template>

<style scoped>
.logo-mark {
  display: flex;
  width: 1.5rem;
  height: 1.5rem;
  align-items: flex-end;
  justify-content: center;
  gap: 2px;
  border-radius: 9999px;
  background: var(--primary);
  padding: 5px;
  color: var(--primary-foreground);
}

.logo-mark span {
  display: block;
  width: 2px;
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
</style>
