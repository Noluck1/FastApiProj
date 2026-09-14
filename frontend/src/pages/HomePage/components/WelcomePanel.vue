<script setup lang="ts">
import { Button } from '@/shared/ui'
import { useWelcomeMessage } from '../model/useWelcomeMessage'

const { message, subtitle } = useWelcomeMessage()
</script>

<template>
  <div
    class="flex items-center justify-between gap-6 rounded-2xl border border-border bg-card p-6 text-card-foreground shadow-sm"
  >
    <div>
      <h1 class="m-0 text-heading-3 font-semibold">{{ message }}</h1>
      <p class="mt-2 mb-0 text-paragraph-regular text-muted-foreground">{{ subtitle }}</p>
    </div>
    <Button>Explore</Button>
  </div>
</template>
