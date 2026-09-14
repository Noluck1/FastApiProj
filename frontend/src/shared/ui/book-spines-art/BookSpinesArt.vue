<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <aside class="auth-library-art" aria-hidden="true">
    <div class="mb-5 grid gap-2">
      <span class="text-xs font-semibold tracking-[0.28em] text-muted-foreground uppercase"
        >Bibliotheca</span
      >
      <p class="m-0 max-w-[24rem] font-serif text-3xl leading-tight text-foreground">
        {{ t('common.libraryMotto') }}
      </p>
    </div>
    <div class="book-shelf">
      <div class="book-spine spine-muted h-48 w-12 -rotate-2">
        <span class="spine-rule"></span><span class="spine-title">ESSAYS</span
        ><span class="spine-mark">I</span>
      </div>
      <div class="book-spine spine-primary h-64 w-16">
        <span class="spine-rule"></span><span class="spine-ornament">✦</span
        ><span class="spine-title">LIBER</span><span class="spine-mark">MMXXVI</span>
      </div>
      <div class="book-spine spine-secondary h-56 w-14 rotate-1">
        <span class="spine-rule"></span><span class="spine-title">POETICA</span
        ><span class="spine-mark">VII</span>
      </div>
      <div class="book-spine spine-accent h-60 w-14 -rotate-1">
        <span class="spine-rule"></span><span class="spine-ornament">◇</span
        ><span class="spine-title">STORIES</span><span class="spine-mark">III</span>
      </div>
      <div class="book-spine spine-muted h-52 w-12 rotate-2">
        <span class="spine-rule"></span><span class="spine-title">PROSE</span
        ><span class="spine-mark">XII</span>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.auth-library-art {
  pointer-events: none;
  display: none;
  min-width: 0;
  flex-direction: column;
  justify-content: center;
}
.book-shelf {
  display: flex;
  height: 19rem;
  align-items: flex-end;
  gap: 0.65rem;
  border-bottom: 0.5rem solid var(--border);
  padding: 0 1rem;
}
.book-spine {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: 0.75rem 0.75rem 0.25rem 0.25rem;
  padding: 0.8rem 0.35rem;
  box-shadow: var(--shadow-md);
}
.book-spine::before,
.book-spine::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  height: 0.28rem;
  border-block: 1px solid currentColor;
  opacity: 0.3;
}
.book-spine::before {
  top: 1.4rem;
}
.book-spine::after {
  bottom: 1.4rem;
}
.spine-muted {
  background: var(--muted);
  color: var(--muted-foreground);
}
.spine-primary {
  background: var(--primary);
  color: var(--primary-foreground);
}
.spine-secondary {
  background: var(--secondary);
  color: var(--secondary-foreground);
}
.spine-accent {
  background: var(--accent);
  color: var(--accent-foreground);
}
.spine-rule {
  width: 55%;
  border-top: 1px solid currentColor;
  opacity: 0.5;
}
.spine-title {
  font-family: var(--font-serif);
  font-size: 0.65rem;
  letter-spacing: 0.18em;
  writing-mode: vertical-rl;
  transform: rotate(180deg);
}
.spine-mark,
.spine-ornament {
  font-family: var(--font-serif);
  font-size: 0.6rem;
  letter-spacing: 0.08em;
}
@media (min-width: 1024px) and (min-height: 700px) {
  .auth-library-art {
    display: flex;
  }
}
</style>
