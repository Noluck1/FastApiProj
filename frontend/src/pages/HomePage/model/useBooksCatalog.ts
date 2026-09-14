import { useDebounceFn } from '@vueuse/core'
import { computed, nextTick, onMounted, ref, shallowRef, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

import { isApiError } from '@/shared/api/types'
import { toast } from '@/shared/lib/toast'
import { useSessionStore } from '@/shared/stores/session.store'
import { useUserStore } from '@/shared/stores/user.store'

import {
  addFavorite,
  createBook,
  deleteBook,
  getBooks,
  getCreatedBooks,
  getFavoriteBooks,
  removeFavorite,
  updateBook,
} from '../api/books.api'
import { logoutUser } from '../api/session.api'
import type {
  Book,
  BookFormValues,
  BookSortBy,
  BookStatusFilter,
  CatalogSection,
  SortOrder,
} from '../types'

type EditorState =
  { mode: 'create'; book: null } | { mode: 'edit'; book: Book } | { mode: null; book: null }

function getErrorKey(error: unknown, action: 'list' | 'save' | 'delete'): string {
  if (!isApiError(error)) {
    return `home.catalog.errors.${action}`
  }

  if (error.status === 0) {
    return 'home.catalog.errors.connection'
  }

  if (error.status === 401) {
    return 'home.catalog.errors.unauthorized'
  }

  if (error.status === 403) {
    return 'home.catalog.errors.forbidden'
  }

  if (error.status === 404) {
    return 'home.catalog.errors.notFound'
  }

  if (error.status === 422) {
    return 'home.catalog.errors.invalidBook'
  }

  if (error.status >= 500) {
    return 'home.catalog.errors.service'
  }

  return `home.catalog.errors.${action}`
}

export function useBooksCatalog() {
  const { t } = useI18n()
  const route = useRoute()
  const router = useRouter()
  const sessionStore = useSessionStore()
  const userStore = useUserStore()

  const books = shallowRef<Book[]>([])
  const searchInput = ref('')
  const appliedSearch = ref('')
  const statusFilter = ref<BookStatusFilter>('active')
  const sortBy = ref<BookSortBy>('updated_at')
  const sortOrder = ref<SortOrder>('desc')
  const page = ref(1)
  const pageSize = ref(12)
  const total = ref(0)
  const totalPages = ref(0)

  const isLoading = ref(false)
  const isLoadingMore = ref(false)
  const isSaving = ref(false)
  const isLoggingOut = ref(false)
  const deletingBookId = ref<number | null>(null)
  const pendingDeleteBookId = ref<number | null>(null)
  const listError = shallowRef<string | null>(null)
  const actionError = shallowRef<string | null>(null)
  const editor = shallowRef<EditorState>({ mode: null, book: null })
  const favoriteBookIds = shallowRef<ReadonlySet<number>>(new Set())
  const favoriteSavingBookId = ref<number | null>(null)

  let latestRequest = 0

  const canCreate = computed(() => {
    const role = userStore.user?.role
    return role === 'author' || role === 'admin'
  })
  const username = computed(() => userStore.user?.username ?? null)

  const activeSection = computed<CatalogSection>(() => {
    const value = route.query.section
    if (value === 'new' || value === 'mine') return value
    if (value === 'created' && canCreate.value) return value
    return 'catalog'
  })
  const isAuthenticated = computed(() => sessionStore.isAuthenticated)
  const requiresLogin = computed(() => activeSection.value === 'mine' && !sessionStore.token)

  const isFirstPage = computed(() => page.value <= 1)
  const isLastPage = computed(() => totalPages.value === 0 || page.value >= totalPages.value)
  const hasMore = computed(() => page.value < totalPages.value)

  function canManageBook(book: Book): boolean {
    const user = userStore.user

    if (!user || book.is_deleted) {
      return false
    }

    return user.role === 'admin' || (user.role === 'author' && book.author_id === user.id)
  }

  async function loadBooks(options: { append?: boolean } = {}): Promise<boolean> {
    const append = options.append ?? false
    const requestId = ++latestRequest
    if (append) {
      isLoadingMore.value = true
    } else {
      isLoading.value = true
      listError.value = null
    }

    const accessToken = sessionStore.token

    if (activeSection.value === 'mine' && !accessToken) {
      books.value = []
      total.value = 0
      totalPages.value = 0
      isLoading.value = false
      isLoadingMore.value = false
      return true
    }

    const statusQuery =
      statusFilter.value === 'active'
        ? { include_deleted: false }
        : statusFilter.value === 'deleted'
          ? { include_deleted: true, is_deleted: true }
          : { include_deleted: true }

    try {
      const query = {
        page: page.value,
        page_size: pageSize.value,
        title_contains: appliedSearch.value || undefined,
        sort_by: sortBy.value,
        sort_order: sortOrder.value,
      }
      let result
      if (activeSection.value === 'mine' && accessToken) {
        result = await getFavoriteBooks(query, accessToken)
      } else if (activeSection.value === 'created' && accessToken) {
        result = await getCreatedBooks({ ...query, ...statusQuery }, accessToken)
      } else {
        result = await getBooks({ ...query, ...statusQuery })
      }

      if (requestId !== latestRequest) {
        return false
      }

      books.value = append
        ? [...new Map([...books.value, ...result.item].map((book) => [book.id, book])).values()]
        : result.item
      total.value = result.total
      totalPages.value = result.total_pages
      if (activeSection.value === 'mine') {
        favoriteBookIds.value = new Set(books.value.map((book) => book.id))
      }
      return true
    } catch (error) {
      if (requestId === latestRequest) {
        if (append) {
          actionError.value = t(getErrorKey(error, 'list'))
        } else {
          books.value = []
          total.value = 0
          totalPages.value = 0
          listError.value = t(getErrorKey(error, 'list'))
        }
      }
      return false
    } finally {
      if (requestId === latestRequest) {
        isLoading.value = false
        isLoadingMore.value = false
      }
    }
  }

  async function loadFavoriteIds() {
    const accessToken = sessionStore.token
    if (!accessToken) {
      favoriteBookIds.value = new Set()
      return
    }

    try {
      const result = await getFavoriteBooks(
        { page: 1, page_size: 100, sort_by: 'updated_at', sort_order: 'desc' },
        accessToken,
      )
      favoriteBookIds.value = new Set(result.item.map((book) => book.id))
    } catch {
      favoriteBookIds.value = new Set()
    }
  }

  async function loadMore() {
    if (!hasMore.value || isLoadingMore.value) return
    page.value += 1
    const loaded = await loadBooks({ append: true })
    if (!loaded) page.value -= 1
  }

  const applySearch = useDebounceFn(() => {
    appliedSearch.value = searchInput.value.trim()
    page.value = 1
    void loadBooks()
  }, 350)

  watch(searchInput, () => {
    void applySearch()
  })

  function setStatusFilter(value: BookStatusFilter) {
    statusFilter.value = value
    page.value = 1
    void loadBooks()
  }

  function applySectionDefaults(section: CatalogSection) {
    page.value = 1
    statusFilter.value = 'active'
    sortBy.value = section === 'new' ? 'created_at' : 'updated_at'
    sortOrder.value = 'desc'
    actionError.value = null
  }

  function setSortBy(value: BookSortBy) {
    sortBy.value = value
    page.value = 1
    void loadBooks()
  }

  function toggleSortOrder() {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
    page.value = 1
    void loadBooks()
  }

  function setPageSize(value: number) {
    pageSize.value = value
    page.value = 1
    void loadBooks()
  }

  function goToPreviousPage() {
    if (isFirstPage.value) {
      return
    }

    page.value -= 1
    void loadBooks()
  }

  function goToNextPage() {
    if (isLastPage.value) {
      return
    }

    page.value += 1
    void loadBooks()
  }

  function openCreateEditor() {
    actionError.value = null
    editor.value = { mode: 'create', book: null }
    void nextTick(() => {
      document.querySelector('#book-editor')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    })
  }

  function openEditEditor(book: Book) {
    if (!canManageBook(book)) {
      return
    }

    actionError.value = null
    editor.value = { mode: 'edit', book }
    void nextTick(() => {
      document.querySelector('#book-editor')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    })
  }

  function closeEditor() {
    if (!isSaving.value) {
      editor.value = { mode: null, book: null }
    }
  }

  async function saveBook(values: BookFormValues) {
    const accessToken = sessionStore.token

    if (!accessToken || !editor.value.mode) {
      actionError.value = t('home.catalog.errors.unauthorized')
      return
    }

    isSaving.value = true
    actionError.value = null
    const payload = {
      title: values.title.trim(),
      description: values.description.trim() || null,
    }

    try {
      if (editor.value.mode === 'create') {
        await createBook(payload, accessToken)
        toast.success(t('home.catalog.notifications.created'))
      } else {
        await updateBook(editor.value.book.id, payload, accessToken)
        toast.success(t('home.catalog.notifications.updated'))
      }

      editor.value = { mode: null, book: null }
      await loadBooks()
    } catch (error) {
      actionError.value = t(getErrorKey(error, 'save'))
    } finally {
      isSaving.value = false
    }
  }

  async function toggleFavorite(book: Book) {
    const accessToken = sessionStore.token
    if (!accessToken) {
      await router.push({ name: 'login', query: { redirect: route.fullPath } })
      return
    }

    if (favoriteSavingBookId.value !== null) return

    favoriteSavingBookId.value = book.id
    actionError.value = null
    const isFavorite = favoriteBookIds.value.has(book.id)

    try {
      if (isFavorite) {
        await removeFavorite(book.id, accessToken)
        const next = new Set(favoriteBookIds.value)
        next.delete(book.id)
        favoriteBookIds.value = next
        toast.success(t('home.catalog.notifications.favoriteRemoved'))

        if (activeSection.value === 'mine') {
          books.value = books.value.filter((item) => item.id !== book.id)
          total.value = Math.max(0, total.value - 1)
        }
      } else {
        await addFavorite(book.id, accessToken)
        favoriteBookIds.value = new Set([...favoriteBookIds.value, book.id])
        toast.success(t('home.catalog.notifications.favoriteAdded'))
      }
    } catch (error) {
      if (isApiError(error) && error.status === 401) {
        sessionStore.clearSession()
        userStore.clearUser()
        await router.push({ name: 'login', query: { redirect: route.fullPath } })
        return
      }

      actionError.value = t('home.catalog.errors.favorite')
    } finally {
      favoriteSavingBookId.value = null
    }
  }

  function requestDelete(book: Book) {
    if (canManageBook(book)) {
      pendingDeleteBookId.value = book.id
      actionError.value = null
    }
  }

  function cancelDelete() {
    pendingDeleteBookId.value = null
  }

  async function confirmDelete(book: Book) {
    const accessToken = sessionStore.token

    if (!accessToken || !canManageBook(book)) {
      actionError.value = t('home.catalog.errors.unauthorized')
      return
    }

    deletingBookId.value = book.id
    actionError.value = null

    try {
      await deleteBook(book.id, accessToken)
      pendingDeleteBookId.value = null
      toast.success(t('home.catalog.notifications.deleted'))

      if (books.value.length === 1 && page.value > 1) {
        page.value -= 1
      }

      await loadBooks()
    } catch (error) {
      actionError.value = t(getErrorKey(error, 'delete'))
    } finally {
      deletingBookId.value = null
    }
  }

  async function logout() {
    if (isLoggingOut.value) {
      return
    }

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

  watch(activeSection, (section) => {
    applySectionDefaults(section)
    void loadBooks()
  })

  onMounted(() => {
    applySectionDefaults(activeSection.value)
    void Promise.all([loadBooks(), loadFavoriteIds()])
  })

  return {
    actionError,
    activeSection,
    books,
    canCreate,
    canManageBook,
    cancelDelete,
    closeEditor,
    confirmDelete,
    deletingBookId,
    editor,
    favoriteBookIds,
    favoriteSavingBookId,
    goToNextPage,
    goToPreviousPage,
    isFirstPage,
    isLastPage,
    isLoading,
    isLoadingMore,
    isAuthenticated,
    isLoggingOut,
    isSaving,
    listError,
    hasMore,
    loadBooks,
    loadMore,
    logout,
    openCreateEditor,
    openEditEditor,
    page,
    pageSize,
    pendingDeleteBookId,
    requestDelete,
    requiresLogin,
    saveBook,
    searchInput,
    setPageSize,
    setSortBy,
    setStatusFilter,
    sortBy,
    sortOrder,
    statusFilter,
    toggleSortOrder,
    toggleFavorite,
    total,
    totalPages,
    username,
  }
}
