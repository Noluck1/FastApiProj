import { useDark, useToggle } from '@vueuse/core'
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', () => {
  const isDark = useDark({
    storageKey: 'book-service-theme',
    disableTransition: false,
  })
  const toggleDark = useToggle(isDark)
  let transitionTimer: number | undefined

  function toggleTheme() {
    const root = document.documentElement

    window.clearTimeout(transitionTimer)
    root.classList.add('theme-transition')
    root.getBoundingClientRect()
    toggleDark()

    transitionTimer = window.setTimeout(() => {
      root.classList.remove('theme-transition')
    }, 500)
  }

  return { isDark, toggleTheme }
})
