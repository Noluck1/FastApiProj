import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useSessionStore = defineStore('session', () => {
  const token = ref<string | null>(null)
  const expiresAt = ref<number | null>(null)

  const isAuthenticated = computed(() => Boolean(token.value))

  function setSession(newToken: string, expiry: number | null) {
    token.value = newToken
    expiresAt.value = expiry
  }

  function clearSession() {
    token.value = null
    expiresAt.value = null
  }

  return { token, expiresAt, isAuthenticated, setSession, clearSession }
})
