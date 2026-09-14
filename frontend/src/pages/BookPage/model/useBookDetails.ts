import { computed, onMounted, ref, shallowRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

import {
  addFavorite,
  getBooks,
  getFavoriteBooks,
  removeFavorite,
  type Book,
} from '@/shared/api/books'
import { logoutUser } from '@/shared/api/session'
import { isApiError } from '@/shared/api/types'
import { toast } from '@/shared/lib/toast'
import { useSessionStore } from '@/shared/stores/session.store'
import { useUserStore } from '@/shared/stores/user.store'
import type { NavigationSection } from '@/shared/ui'

export function useBookDetails() {
  const route = useRoute()
  const router = useRouter()
  const { t } = useI18n()
  const sessionStore = useSessionStore()
  const userStore = useUserStore()

  const book = shallowRef<Book | null>(null)
  const isLoading = ref(false)
  const isFavorite = ref(false)
  const isSavingFavorite = ref(false)
  const isLoggingOut = ref(false)
  const error = shallowRef<string | null>(null)

  const bookId = computed(() => Number(route.params.id))
  const canCreate = computed(() => {
    const role = userStore.user?.role
    return role === 'author' || role === 'admin'
  })
  const activeSection = computed<NavigationSection>(() => {
    const value = route.query.from
    if (value === 'new' || value === 'mine') return value
    if (value === 'created' && canCreate.value) return value
    return 'catalog'
  })
  const username = computed(() => userStore.user?.username ?? null)
  const isAuthenticated = computed(() => sessionStore.isAuthenticated)

  async function loadBook() {
    if (!Number.isInteger(bookId.value) || bookId.value < 1) {
      error.value = t('home.book.notFound')
      return
    }

    isLoading.value = true
    error.value = null
    try {
      const result = await getBooks({
        page: 1,
        page_size: 1,
        book_id: bookId.value,
        include_deleted: false,
        sort_by: 'id',
        sort_order: 'asc',
      })
      book.value = result.item[0] ?? null
      if (!book.value) error.value = t('home.book.notFound')
    } catch (caught) {
      error.value =
        isApiError(caught) && caught.status === 404 ? t('home.book.notFound') : t('home.book.error')
    } finally {
      isLoading.value = false
    }

    if (book.value && sessionStore.token) {
      try {
        const result = await getFavoriteBooks(
          { page: 1, page_size: 1, book_id: book.value.id, sort_by: 'id', sort_order: 'asc' },
          sessionStore.token,
        )
        isFavorite.value = result.item.length > 0
      } catch {
        isFavorite.value = false
      }
    }
  }

  async function toggleFavorite() {
    if (!book.value || !sessionStore.token || isSavingFavorite.value) return
    isSavingFavorite.value = true
    try {
      if (isFavorite.value) {
        await removeFavorite(book.value.id, sessionStore.token)
        isFavorite.value = false
        toast.success(t('home.catalog.notifications.favoriteRemoved'))
      } else {
        await addFavorite(book.value.id, sessionStore.token)
        isFavorite.value = true
        toast.success(t('home.catalog.notifications.favoriteAdded'))
      }
    } catch {
      toast.error(t('home.catalog.errors.favorite'))
    } finally {
      isSavingFavorite.value = false
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

  onMounted(() => void loadBook())

  return {
    activeSection,
    book,
    canCreate,
    error,
    isAuthenticated,
    isFavorite,
    isLoading,
    isLoggingOut,
    isSavingFavorite,
    loadBook,
    logout,
    toggleFavorite,
    username,
  }
}
