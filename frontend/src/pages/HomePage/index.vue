<script setup lang="ts">
import BookEditor from './components/BookEditor.vue'
import BooksList from './components/BooksList.vue'
import BooksToolbar from './components/BooksToolbar.vue'
import CatalogHeader from './components/CatalogHeader.vue'
import CatalogLoadMore from './components/CatalogLoadMore.vue'
import ContinueShelf from './components/ContinueShelf.vue'
import HomeFooter from './components/HomeFooter.vue'
import HomeHero from './components/HomeHero.vue'
import MembershipPromo from './components/MembershipPromo.vue'
import { useBooksCatalog } from './model/useBooksCatalog'

const catalog = useBooksCatalog()
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <CatalogHeader
      :active-section="catalog.activeSection.value"
      :can-create="catalog.canCreate.value"
      :is-logging-out="catalog.isLoggingOut.value"
      :search="catalog.searchInput.value"
      :username="catalog.username.value"
      @logout="catalog.logout"
      @update:search="catalog.searchInput.value = $event"
    />

    <main>
      <HomeHero
        :books="catalog.books.value"
        :section="catalog.activeSection.value"
        :total="catalog.total.value"
      />

      <BooksToolbar
        :show-status-filter="catalog.activeSection.value !== 'mine'"
        :status-filter="catalog.statusFilter.value"
        :sort-by="catalog.sortBy.value"
        :sort-order="catalog.sortOrder.value"
        @update:status-filter="catalog.setStatusFilter"
        @update:sort-by="catalog.setSortBy"
        @toggle:sort-order="catalog.toggleSortOrder"
      />

      <section
        v-if="catalog.editor.value.mode || catalog.actionError.value"
        class="mx-auto grid max-w-[1440px] gap-4 px-4 py-5 sm:px-7 lg:px-10"
      >
        <BookEditor
          v-if="catalog.editor.value.mode"
          :key="`${catalog.editor.value.mode}-${catalog.editor.value.book?.id ?? 'new'}`"
          :mode="catalog.editor.value.mode"
          :book="catalog.editor.value.book"
          :is-saving="catalog.isSaving.value"
          @cancel="catalog.closeEditor"
          @submit="catalog.saveBook"
        />

        <p
          v-if="catalog.actionError.value"
          role="alert"
          class="m-0 rounded-2xl border border-destructive/30 bg-destructive/5 p-4 text-sm text-destructive"
        >
          {{ catalog.actionError.value }}
        </p>
      </section>

      <ContinueShelf :books="catalog.books.value" :section="catalog.activeSection.value" />

      <BooksList
        :books="catalog.books.value"
        :is-loading="catalog.isLoading.value"
        :error="catalog.listError.value"
        :pending-delete-book-id="catalog.pendingDeleteBookId.value"
        :deleting-book-id="catalog.deletingBookId.value"
        :favorite-saving-book-id="catalog.favoriteSavingBookId.value"
        :favorite-book-ids="catalog.favoriteBookIds.value"
        :is-authenticated="catalog.isAuthenticated.value"
        :requires-login="catalog.requiresLogin.value"
        :search="catalog.searchInput.value"
        :section="catalog.activeSection.value"
        :total="catalog.total.value"
        :can-create="catalog.canCreate.value"
        :can-manage-book="catalog.canManageBook"
        @create="catalog.openCreateEditor"
        @retry="catalog.loadBooks"
        @edit="catalog.openEditEditor"
        @request-delete="catalog.requestDelete"
        @cancel-delete="catalog.cancelDelete"
        @confirm-delete="catalog.confirmDelete"
        @toggle-favorite="catalog.toggleFavorite"
      />

      <div class="mx-auto max-w-[1440px] px-4 sm:px-7 lg:px-10">
        <CatalogLoadMore
          v-if="!catalog.isLoading.value && !catalog.listError.value"
          :has-more="catalog.hasMore.value"
          :is-loading="catalog.isLoadingMore.value"
          :shown="catalog.books.value.length"
          :total="catalog.total.value"
          @load="catalog.loadMore"
        />
      </div>

      <MembershipPromo
        :favorite-count="catalog.favoriteBookIds.value.size"
        :is-authenticated="catalog.isAuthenticated.value"
        :shown="catalog.books.value.length"
        :total="catalog.total.value"
      />
    </main>

    <HomeFooter />
  </div>
</template>
