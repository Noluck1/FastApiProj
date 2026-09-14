<script setup lang="ts">
import { useI18n } from 'vue-i18n'

interface CarouselBook {
  title: string
  author: string
  cover: string
  ink: string
}

const books: CarouselBook[] = [
  { title: 'Белые ночи', author: 'Ф. Достоевский', cover: '--cover-1', ink: '--cover-1-ink' },
  { title: 'Алые паруса', author: 'А. Грин', cover: '--cover-2', ink: '--cover-2-ink' },
  { title: 'Детство', author: 'Л. Толстой', cover: '--cover-3', ink: '--cover-3-ink' },
  { title: 'Отцы и дети', author: 'И. Тургенев', cover: '--cover-4', ink: '--cover-4-ink' },
  { title: 'Чайка', author: 'А. Чехов', cover: '--cover-5', ink: '--cover-5-ink' },
  { title: 'Обломов', author: 'И. Гончаров', cover: '--cover-6', ink: '--cover-6-ink' },
  { title: 'Мы', author: 'Е. Замятин', cover: '--cover-2', ink: '--cover-2-ink' },
  { title: 'Невский проспект', author: 'Н. Гоголь', cover: '--cover-1', ink: '--cover-1-ink' },
  { title: 'Гранатовый браслет', author: 'А. Куприн', cover: '--cover-4', ink: '--cover-4-ink' },
  {
    title: 'Герой нашего времени',
    author: 'М. Лермонтов',
    cover: '--cover-3',
    ink: '--cover-3-ink',
  },
]

const { t } = useI18n()
</script>

<template>
  <aside class="book-carousel" aria-hidden="true">
    <div class="book-carousel__intro">
      <span class="book-carousel__eyebrow">Bibliotheca</span>
      <p class="book-carousel__motto">{{ t('common.libraryMotto') }}</p>
    </div>

    <div class="book-carousel__scene">
      <div class="book-carousel__ring" :style="{ '--quantity': books.length }">
        <div
          v-for="(book, index) in books"
          :key="book.title"
          class="book-carousel__book"
          :style="{
            '--book-index': index,
            '--book-cover': `var(${book.cover})`,
            '--book-ink': `var(${book.ink})`,
          }"
        >
          <div class="book-carousel__cover book-carousel__cover--front">
            <span class="book-carousel__spine"></span>
            <span class="book-carousel__ornament">✦</span>
            <strong class="book-carousel__title">{{ book.title }}</strong>
            <span class="book-carousel__rule"></span>
            <span class="book-carousel__author">{{ book.author }}</span>
          </div>
          <div class="book-carousel__cover book-carousel__cover--back">
            <span class="book-carousel__back-mark">B</span>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.book-carousel {
  pointer-events: none;
  display: none;
  width: 100%;
  min-width: 0;
  height: 28rem;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}

.book-carousel__intro {
  display: grid;
  width: 100%;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.book-carousel__eyebrow {
  color: var(--muted-foreground);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.28em;
  text-transform: uppercase;
}

.book-carousel__motto {
  max-width: 22rem;
  margin: 0;
  color: var(--foreground);
  font-family: var(--font-serif);
  font-size: 1.875rem;
  line-height: 1.25;
}

.book-carousel__scene {
  display: grid;
  width: 100%;
  height: 17rem;
  place-items: center;
}

.book-carousel__ring {
  --book-width: 5.25rem;
  --book-height: 8rem;
  --carousel-radius: 9.5rem;

  position: relative;
  width: var(--book-width);
  height: var(--book-height);
  transform-style: preserve-3d;
  animation: book-carousel-rotation 36s linear infinite;
}

.book-carousel__book {
  position: absolute;
  inset: 0;
  transform: rotateY(calc((360deg / var(--quantity)) * var(--book-index)))
    translateZ(var(--carousel-radius));
  transform-style: preserve-3d;
}

.book-carousel__cover {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: 0.35rem 0.7rem 0.7rem 0.35rem;
  background: var(--book-cover);
  color: var(--book-ink);
  box-shadow:
    var(--shadow-lg),
    0 0.65rem 1.4rem var(--cover-shadow-soft);
  backface-visibility: hidden;
}

.book-carousel__cover--front {
  transform: translateZ(0.22rem);
  padding: 0.8rem 0.65rem 0.7rem 0.9rem;
}

.book-carousel__cover--back {
  justify-content: center;
  transform: rotateY(180deg) translateZ(0.22rem);
}

.book-carousel__spine {
  position: absolute;
  inset-block: 0;
  left: 0;
  width: 0.42rem;
  border-right: 1px solid var(--book-ink);
  background: var(--book-cover);
  box-shadow: 0.12rem 0 0 var(--cover-shadow-soft);
}

.book-carousel__ornament,
.book-carousel__back-mark {
  display: grid;
  width: 1.55rem;
  height: 1.55rem;
  place-items: center;
  border: 1px solid var(--book-ink);
  border-radius: 50%;
  font-family: var(--font-serif);
  font-size: 0.7rem;
}

.book-carousel__title {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  max-width: 100%;
  overflow-wrap: anywhere;
  text-align: center;
  font-family: var(--font-serif);
  font-size: 0.7rem;
  line-height: 1.15;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.book-carousel__rule {
  width: 72%;
  border-top: 1px solid var(--book-ink);
}

.book-carousel__author {
  margin-top: 0.42rem;
  max-width: 100%;
  text-align: center;
  font-family: var(--font-serif);
  font-size: 0.5rem;
  line-height: 1.2;
  letter-spacing: 0.03em;
}

@keyframes book-carousel-rotation {
  from {
    transform: perspective(52rem) rotateX(-12deg) rotateY(0);
  }
  to {
    transform: perspective(52rem) rotateX(-12deg) rotateY(1turn);
  }
}

@media (min-width: 1024px) and (min-height: 700px) {
  .book-carousel {
    display: flex;
  }
}

@media (prefers-reduced-motion: reduce) {
  .book-carousel__ring {
    animation-play-state: paused;
  }
}
</style>
