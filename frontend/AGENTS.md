# Agents Guide

Short rules for consistent structure. If unsure, keep things page-local first.

## Quick Map

```
src/
  app/            # bootstrap: main, router, pinia, i18n, global styles
  pages/          # routes + page UI + page logic
  shared/
    ui/           # base UI generated from shadcn-vue and re-exported for app code
    api/          # http client + endpoints + shared types
    stores/       # global pinia stores
    lib/          # helpers, formatters, shared types
    i18n/         # locales, messages, i18n helpers
```

## Entry Points

- App bootstrap: `src/app/main.ts`
- Router: `src/app/router/index.ts` + `src/app/router/routes.ts`
- I18n plugin: `src/app/i18n.ts`
- Global styles: `src/app/styles/index.scss`

## Import Rules (Must Follow)

- `pages` can import from `shared` and `app`.
- `shared` must NOT import from `pages`.
- `app` can import from `shared` and only minimal from `pages` (routes).
- Dependency flow is one-way: `app/pages` -> `shared`.

## UI Kit Usage

- Base components live in `src/shared/ui/*`.
- Use the official `shadcn-vue` workflow for base components.
- Keep generated primitives under `src/shared/ui`.
- Use `components.json` + MCP shadcn registry flow before adding or changing base primitives.
- Page-specific UI stays under `pages/<Page>/components`.

## Page Module Template

```
pages/
  ProductsPage/
    index.vue
    components/
    model/
    api/
    types.ts
```

- `index.vue`: layout + wiring only (keep logic minimal).
- `components/`: used only by this page.
- `model/`: composables + page logic (filters, pagination, URL sync).
- `api/`: page-only requests.
- `types.ts`: page-specific types.

## Shared Layers

- `shared/api`: network layer only (no page logic).
- `shared/i18n`: locales, message catalogs, i18n helpers.
- `shared/stores`: global state only (user/session).
- `shared/lib`: helpers/formatters/types; avoid Vue dependency if possible.

## I18n (vue-i18n)

- Dictionaries live in `src/shared/i18n/locales`.
- Configure and export the plugin from `src/app/i18n.ts`.
- Prefer translating in pages or page components; `shared/ui` should receive translated labels via props.

## Utilities (VueUse)

- Before creating a new utility/composable, check VueUse for an existing solution.
- If VueUse covers it, use that; create a custom utility only if it does not exist.
- For shared class composition, use `src/shared/lib/utils.ts` and its `cn()` helper.

## Naming Conventions

- Pages: `ProductsPage`, `ProfilePage` with `index.vue`.
- Components: `PascalCase.vue`.
- Composables: `useXxx.ts`.
- Stores: `*.store.ts` with `useXxxStore`.
- API files: `*.api.ts`.

## Forms and Validation

- Always build form validation through `shadcn-vue` form components from `@/shared/ui`.
- Use `vee-validate` `useForm` with `@vee-validate/zod` `toTypedSchema`.
- Use `zod` for schema definition.
- Keep schemas page-local in `pages/<Page>/model` unless reused on 2+ pages.
- Promote shared schemas to `shared/lib` and re-export if needed.
- Keep field markup in the `FormField` / `FormItem` / `FormLabel` / `FormControl` / `FormMessage` structure from `shadcn-vue`.

## Adding a New Page (Checklist)

1. Create `pages/NewPage/index.vue`.
2. Add local components to `pages/NewPage/components`.
3. Put logic in `pages/NewPage/model`.
4. Add unique requests in `pages/NewPage/api`.
5. Register route in `src/app/router/routes.ts`.

## When to Promote to Shared

- Used once: keep in `pages/<Page>/...`.
- Used on 2+ pages: move to `shared/ui`, `shared/lib`, or `shared/api`.
- Base UI (Button/Input/Modal) goes straight to `shared/ui`.

## Codex Usage Tips

- Keep changes aligned with `architecture.md`.
- Prefer minimal, focused edits.
- Avoid placing business logic in `shared/ui` or `app/`.
- Update routes only via `src/app/router/routes.ts`.
- For base UI work, prefer MCP shadcn + registry-driven additions over hand-written primitives.

## Skill Execution Policy

- Use `.agents/skills/project-default` for every task in this repository.
- `project-default` is the orchestrator and decides which local skills are active by intent and touched files.
- Apply `vue-best-practices` as a default baseline for all Vue tasks.
- Activate additional local skills based on this matrix:
  - `.vue` / Composition API / macros: `vue`
  - New utility/composable candidates: `vueuse-functions`
  - `defineStore` / `*.store.ts` / global state: `pinia`
  - `src/app/router/**` / guards / params: `vue-router-best-practices`
  - `vite.config.ts` / build and tooling: `vite`
  - `src/shared/ui/**` / wrappers / shadcn registry work: `shadcn-mcp-ui`
  - UI/UX/a11y audit requests: `web-design-guidelines`

## Shadcn Rules

- `components.json` is required infrastructure for this template.
- App/page code imports UI from `@/shared/ui`, not from raw registry paths.
- For new base UI primitives, first use MCP shadcn against registry `@shadcn`.

## Local Skills

- Skills root: `.agents/skills`
- Required orchestrator: `.agents/skills/project-default/SKILL.md`
