import en from './locales/en'
import ru from './locales/ru'

export const messages = { en, ru } as const

export type Locale = keyof typeof messages

export const defaultLocale: Locale = 'ru'
export const supportedLocales = Object.keys(messages) as Locale[]
