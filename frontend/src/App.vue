<script setup lang="ts">
import { Toaster } from '@/shared/ui'
</script>

<template>
  <div class="app-shell w-full min-w-0 max-w-full">
    <Toaster />
    <RouterView />
  </div>
</template>
