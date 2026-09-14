# Архитектура проектов

## Тезис (основные цели архитектуры)

- Простая структура, понятная без FSD / Clean Architecture
- Быстро находить код: **всё, что относится к странице — рядом со страницей**
- Минимум “общих свалок” (components/services)
- Предсказуемые правила: где UI, где логика, где API, где состояние

---

## Верхнеуровневая архитектура (директории)

```text
src/
  pages/          # всё по страницам (роутам)
  shared/
    ui/           # базовые UI-компоненты
    api/          # http client + endpoints + общие типы/ошибки
    stores/       # глобальные stores (user/session)
    lib/          # утилиты/хелперы/типы
    i18n/         # локали, словари, i18n-хелперы
  app/            # bootstrap: router, pinia, i18n, plugins, global styles
```

### Правила импортов

- `pages` → может импортировать из `shared` и `app` (обычно router types)
- `shared` → **не импортирует** из `pages`
- `app` → может импортировать из `shared`, минимально из `pages` (например routes)

---

## 1) app/

### Responsibility

`app/` отвечает только за “склейку” приложения:

- `main.ts` (createApp)
- `router` (routes)
- `pinia` (createPinia)
- `i18n` (createI18n)
- глобальные стили

### Пример кода

```text
app/
  main.ts
  i18n.ts
  pinia.ts
  router/
    index.ts
    routes.ts
  styles/
    index.scss
    variables.scss
    mixins.scss
```

### Rules

- Никакой бизнес-логики и запросов.
- Глобальные стили подключаем в `main.ts` через `styles/index.scss`.

---

## 2) pages/

### Responsibility

`pages/` — роуты и всё, что относится к конкретному экрану.

### Typical page module

```text
pages/
  ProductsPage/
    index.vue
    components/
      ProductsTable.vue
      FiltersPanel.vue
    model/
      useProductsFilters.ts
      useProductsList.ts
      useQuerySync.ts
    api/
      products.page.api.ts
    types.ts
```

### Что должно быть внутри папки со страницей

- `index.vue`: сборка страницы, layout, подключение компонентов (минимум логики)
- `components/`: компоненты, используемые **только на этой странице**
- `model/`: composables и “логика страницы” (filters, pagination, query sync)
- `api/`: запросы, которые нужны **только** этой странице (специфичные endpoints/агрегации)
- `types.ts`: типы, специфичные для страницы

### Rules

1. Всё одноразовое держим рядом со страницей.
2. Если компонент/логика понадобились на 2+ страницах — переносим в `shared`.
3. В `index.vue` нельзя держать “портянки” логики: выносим в `model/`.

---

## 3) shared/ui/

### Использование

Базовые UI-компоненты без бизнес-логики: Button, Input, Select, Modal, Tabs.
Источником компонентов является официальный workflow `shadcn-vue`.

### Требования

- Не знают про домен (user/product/order)
- Не делают HTTP
- Принимают данные через `props`
- Отдают события через `emit`
- Максимум переиспользуемости, минимум “особых кейсов”
- Добавляются через `components.json` и MCP/CLI `shadcn-vue`
- Экспортируются для приложения через `@/shared/ui`

### Пример

```text
shared/ui/
  button/
    Button.vue
    button.variants.ts
    index.ts
  form/
    FormControl.vue
    FormItem.vue
    FormLabel.vue
    FormMessage.vue
    index.ts
  input/
    Input.vue
    index.ts
  label/
    Label.vue
    index.ts
  sonner/
    Sonner.vue
    index.ts
```

> Правило: если компонент начинает принимать `product`, `user`, `order` или имеет внутри “правила бизнеса” — это НЕ `shared/ui`.
> Правило: прежде чем добавлять новый base primitive вручную, используй MCP shadcn и registry `@shadcn`.
> Правило: page-level формы строятся через `shared/ui/form`, а схема и `useForm()` остаются в `pages/<Page>/model`.

---

## 4) shared/api/

### Использование

Единый сетевой слой:

- `http.ts`: клиент, базовые настройки, перехватчики, обработка ошибок
- `endpoints.ts`: константы путей
- `types.ts`: типы ответов и ошибок

### Пример

```text
shared/api/
  http.ts
  endpoints.ts
  types.ts
```

### Правила

- Компоненты и `index.vue` не вызывают fetch/axios напрямую.
- Запросы идут через:
  - `shared/api/*` для общих
  - `pages/<Page>/api/*` для уникальных

### Пример

```ts
// shared/api/types.ts
export type ApiError = {
  status: number
  message: string
  details?: unknown
}
```

```ts
// shared/api/http.ts (idea)
export async function request<T>(input: RequestInfo, init?: RequestInit): Promise<T> {
  const res = await fetch(input, init)
  if (!res.ok) {
    // convert to ApiError
    throw { status: res.status, message: await res.text() } as const
  }
  return (await res.json()) as T
}
```

(Реализация может быть на axios — принцип тот же.)

---

## 5) shared/stores/ (Pinia)

### Использование

Только глобальные состояния приложения:

- `session` (token/refresh/expiry)
- `user` (me/roles/permissions)

### Что не должно быть здесь

- Состояние конкретной страницы (filters, table sort, local list) — это `pages/<Page>/model`

### Пример

```text
shared/stores/
  session.store.ts
  user.store.ts
```

### Naming convention

- file: `*.store.ts`
- export: `useXxxStore`

---

## 6) shared/lib/

### Использование

Утилиты и хелперы, которые можно использовать в разных местах:

- форматирование дат/денег
- debounce/throttle
- сборка query params
- общие типы

### Пример

```text
shared/lib/
  format/
    date.ts
    money.ts
  helpers/
    debounce.ts
  query/
    buildQuery.ts
  types/
    common.ts
```

### Правила

По возможности `shared/lib` не зависит от Vue. Если нужна реактивность и это реально общее - можно сделать `shared/lib/composables/`, но по умолчанию composables держим ближе к месту использования (в `pages/<Page>/model`).

---

## 7) shared/i18n/

### Использование

Словари переводов, список локалей и общие i18n-хелперы.

### Пример

```text
shared/i18n/
  locales/
    en.ts
    ru.ts
  index.ts
```

### Правила

- Переводы лежат в `shared/i18n/locales`.
- Конфиг и подключение плагина выполняем в `app/i18n.ts`.
- В `shared/ui` не используем `$t`, прокидываем уже переведённые строки через `props`.

---

### Когда использовать

Используй composables, когда:

- логика локальная для страницы/виджета
- нужно переиспользовать внутри страницы между компонентами
- это UI-логика (modal, confirm, query sync, pagination)

### Для чего нужна Pinia

Pinia нужен, если:

- состояние нужно на многих страницах
- есть общая сессия/пользователь
- нужен общий кэш данных или доступ из разных частей приложения

---

## Где размещать компоненты в зависимости от кол-ва использование

- Используется 1 раз → остаётся в `pages/<Page>/...`
- Используется 2+ раза → выносим в `shared/ui` или `shared/lib` или `shared/api`

Исключение: базовые UI (Button/Input/Modal) сразу `shared/ui`.

---

## Наименования

### Страницы

- Folder: `ProductsPage`, `ProfilePage`
- Entry: `index.vue`

### Компоненты

- `PascalCase.vue`
- “локальные” — в `pages/<Page>/components`

### Композаблы

- `useXxx.ts`
- живут в `pages/<Page>/model`

### Сторы

- `*.store.ts`
- `useXxxStore`

### API

- `*.api.ts`
- общие endpoints в `shared/api/endpoints.ts`

---

## Пример на основе страницы продуктов

### Функционал страницы

- filters + pagination + list
- sync filters with URL query
- fetch list through api layer

### Рекомендации по файлам

- `index.vue`: layout + wiring
- `model/useProductsFilters.ts`: состояние фильтров + маппинг в query
- `model/useProductsList.ts`: загрузка списка + loading/error
- `api/products.page.api.ts`: функции запросов

---

## Чеклист

### Создать новую страницу

1. Create `pages/NewPage/index.vue`
2. Add local components to `pages/NewPage/components`
3. Add logic to `pages/NewPage/model`
4. If unique requests exist → `pages/NewPage/api`
5. Register route in `app/router/routes.ts`

### Добавить глбальный стейлт

Если будет что-то использоваться связанное со всем приложением кладем в → `shared/stores`

### Переиспользуемые UI компоненты

- Этот компонент будет использоваться не только на этой странице → `shared/ui`
- Этот компонент будет использоваться только на этой странице → `pages/<Page>/components`

---

## Стилизация (SCSS)

- Глобальные переменные: `app/styles/variables.scss`, `mixins.scss`
- Глобальные сущности: `app/styles/index.scss`
- Стили компонентов: `style scoped lang="scss"`
- Не добавляем “глобальные классы” под конкретную страницу — держим стили внутри страницы/компонентов.
