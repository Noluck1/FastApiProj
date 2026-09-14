<script setup lang="ts">
import { ArrowRight, BookMarked, Heart, Library } from '@lucide/vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

import { Button } from '@/shared/ui'

const props = defineProps<{
  favoriteCount: number
  isAuthenticated: boolean
  shown: number
  total: number
}>()

const { t } = useI18n()

const benefits = computed(() => [
  { icon: BookMarked, value: props.total, label: t('home.landing.promo.books') },
  { icon: Library, value: props.shown, label: t('home.landing.promo.available') },
  { icon: Heart, value: props.favoriteCount, label: t('home.landing.promo.saved') },
])
</script>

<template>
  <section class="mx-auto max-w-[1440px] px-4 pb-12 sm:px-7 lg:px-10 lg:pb-20">
    <div
      class="membership-card grid overflow-hidden rounded-[28px] bg-membership px-6 py-8 text-membership-foreground sm:px-10 sm:py-10 lg:grid-cols-[1.4fr_1fr] lg:items-center lg:gap-10 lg:px-14 lg:py-12"
    >
      <div class="min-w-0">
        <p class="m-0 text-[11px] font-bold tracking-[0.18em] text-membership-accent uppercase">
          {{ t('home.landing.promo.eyebrow') }}
        </p>
        <h2
          class="mt-2 mb-0 max-w-[42rem] font-serif text-3xl leading-tight font-semibold sm:text-4xl"
        >
          {{
            props.isAuthenticated
              ? t('home.landing.promo.authTitle')
              : t('home.landing.promo.guestTitle')
          }}
        </h2>
        <p
          class="mt-3 mb-0 max-w-[36rem] text-sm leading-relaxed text-membership-muted sm:text-base"
        >
          {{
            props.isAuthenticated
              ? t('home.landing.promo.authDescription')
              : t('home.landing.promo.guestDescription')
          }}
        </p>
        <Button
          as-child
          class="mt-6 bg-membership-action text-membership-action-foreground hover:bg-membership-action-hover"
        >
          <RouterLink
            :to="
              props.isAuthenticated
                ? { name: 'home', query: { section: 'mine' } }
                : { name: 'register' }
            "
          >
            {{
              props.isAuthenticated
                ? t('home.landing.promo.myBooksAction')
                : t('auth.register.title')
            }}
            <ArrowRight aria-hidden="true" class="size-4" />
          </RouterLink>
        </Button>
      </div>

      <div class="mt-8 grid grid-cols-3 gap-2 sm:gap-4 lg:mt-0">
        <div
          v-for="benefit in benefits"
          :key="benefit.label"
          class="flex min-w-0 flex-col rounded-2xl border border-membership-border bg-membership-surface p-3 sm:p-5"
        >
          <component :is="benefit.icon" class="size-5 text-membership-accent" aria-hidden="true" />
          <strong class="mt-5 truncate font-serif text-base sm:text-xl">{{ benefit.value }}</strong>
          <span
            class="mt-1 truncate text-[10px] text-membership-subtle sm:text-xs"
            :title="benefit.label"
          >
            {{ benefit.label }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.membership-card {
  background-image: radial-gradient(
    circle at 85% 20%,
    color-mix(in oklab, var(--membership-accent) 18%, transparent),
    transparent 30%
  );
  box-shadow: 0 22px 45px -34px color-mix(in oklab, var(--foreground) 50%, transparent);
}
</style>
