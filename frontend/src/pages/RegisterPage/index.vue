<script setup lang="ts">
import RegisterForm from './components/RegisterForm.vue'
import { BookCarouselArt, ThemeToggle } from '@/shared/ui'
</script>

<template>
  <main
    class="relative mx-auto grid min-h-screen w-full min-w-0 max-w-[var(--container-5xl)] grid-cols-[minmax(0,1fr)] items-center justify-items-center gap-12 px-4 py-16 sm:px-6 lg:grid-cols-[minmax(0,30rem)_minmax(0,22rem)] lg:justify-center lg:px-8 lg:py-10"
  >
    <div class="absolute top-4 right-4 sm:top-6 sm:right-6"><ThemeToggle /></div>
    <RegisterForm />
    <BookCarouselArt />
  </main>
</template>
