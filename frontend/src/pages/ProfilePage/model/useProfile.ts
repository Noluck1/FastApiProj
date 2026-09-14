import { computed, onMounted, ref, shallowRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

import { logoutUser } from '@/shared/api/session'
import { isApiError } from '@/shared/api/types'
import { toast } from '@/shared/lib/toast'
import { useSessionStore } from '@/shared/stores/session.store'
import { useUserStore } from '@/shared/stores/user.store'

import { updateMyFullName } from '../api/profile.api'
import type { ProfileFormValues } from '../types'

function getErrorKey(error: unknown): string {
  if (!isApiError(error)) return 'auth.profile.errors.generic'
  if (error.status === 0) return 'auth.profile.errors.connection'
  if (error.status === 401) return 'auth.profile.errors.unauthorized'
  if (error.status === 422) return 'auth.profile.errors.invalidRequest'
  if (error.status >= 500) return 'auth.profile.errors.service'
  return 'auth.profile.errors.generic'
}

export function useProfile() {
  const { t } = useI18n()
  const route = useRoute()
  const router = useRouter()
  const sessionStore = useSessionStore()
  const userStore = useUserStore()

  const isEditing = ref(false)
  const isLoggingOut = ref(false)
  const isSaving = ref(false)
  const submitError = shallowRef<string | null>(null)

  const user = computed(() => userStore.user)
  const canCreate = computed(() => {
    const role = user.value?.role
    return role === 'author' || role === 'admin'
  })
  const fullName = computed(
    () =>
      user.value?.full_name?.trim() ||
      [user.value?.last_name, user.value?.first_name, user.value?.middle_name]
        .filter(Boolean)
        .join(' ') ||
      t('auth.profile.fullNameMissing'),
  )
  const initials = computed(() => {
    const parts = [user.value?.first_name, user.value?.last_name].filter((part): part is string =>
      Boolean(part),
    )
    const source = parts.length ? parts : [user.value?.username ?? '']
    return source
      .map((part) => part.trim().charAt(0))
      .join('')
      .slice(0, 2)
      .toUpperCase()
  })

  function startEditing() {
    submitError.value = null
    isEditing.value = true
  }

  function cancelEditing() {
    if (isSaving.value) return
    submitError.value = null
    isEditing.value = false
  }

  async function saveFullName(values: ProfileFormValues) {
    const accessToken = sessionStore.token
    if (!accessToken) {
      await router.replace({ name: 'login', query: { redirect: route.fullPath } })
      return
    }

    submitError.value = null
    isSaving.value = true

    try {
      const updatedUser = await updateMyFullName(
        {
          first_name: values.firstName.trim(),
          last_name: values.lastName.trim(),
          middle_name: values.middleName.trim() || null,
        },
        accessToken,
      )
      userStore.setUser(updatedUser)
      isEditing.value = false
      toast.success(t('auth.profile.notifications.updated'))
    } catch (error) {
      if (isApiError(error) && error.status === 401) {
        sessionStore.clearSession()
        userStore.clearUser()
        await router.replace({ name: 'login', query: { redirect: route.fullPath } })
        return
      }

      submitError.value = t(getErrorKey(error))
    } finally {
      isSaving.value = false
    }
  }

  async function logout() {
    if (isLoggingOut.value) return
    isLoggingOut.value = true
    try {
      await logoutUser()
    } catch {
      toast.error(t('auth.profile.logoutError'))
    } finally {
      sessionStore.clearSession()
      userStore.clearUser()
      isLoggingOut.value = false
      await router.replace({ name: 'login' })
    }
  }

  onMounted(async () => {
    if (!sessionStore.token || !userStore.user) {
      await router.replace({ name: 'login', query: { redirect: route.fullPath } })
    }
  })

  return {
    cancelEditing,
    canCreate,
    fullName,
    initials,
    isEditing,
    isLoggingOut,
    isSaving,
    logout,
    saveFullName,
    startEditing,
    submitError,
    user,
  }
}
