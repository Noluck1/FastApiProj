import { defineStore } from 'pinia'
import { ref } from 'vue'

import type { SessionUser } from '@/shared/api/session'

export type User = SessionUser

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)

  function setUser(nextUser: User) {
    user.value = nextUser
  }

  function clearUser() {
    user.value = null
  }

  return { user, setUser, clearUser }
})
