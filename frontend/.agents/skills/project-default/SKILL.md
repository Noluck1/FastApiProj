---
name: project-default
description: Repository orchestration skill for vuetemplate. Use for every task in this repository to apply architecture rules and activate vue-best-practices, vue, vueuse-functions, pinia, vue-router-best-practices, vite, shadcn-mcp-ui, and web-design-guidelines based on task intent and touched files.
metadata:
  owner: vuetemplate
  version: "1.0.0"
---

# Project Default

Use this skill for every task in this repository.

## Always-On Rules

- Follow repository architecture from `AGENTS.md`.
- Apply `vue-best-practices` for all Vue-related work.
- Keep logic page-local first, then promote to `shared` only when reused on 2+ pages.
- Preserve dependency flow: `app/pages -> shared`; never `shared -> pages`.
- For service UI/design-team work, apply `service-information-ui-guard`.
- For service UI layout implementation/review, apply `service-layout-regression-guard`.
- For dense service surfaces, apply `service-dense-surface-guard`.
- For UI component selection or wrappers, apply `shadcn-component-source`, use MCP shadcn against registry `@shadcn` first, and route page usage through `src/shared/ui`.
- Pull visual colors from `src/app/styles/tailwind.css`; do not invent hardcoded palettes.
- Treat `components.json` as required project infrastructure for shared UI work.

## Design Team Routing

- Use `.agents/team_design_mini` for small, local UI requests: single route/component fixes, minor layout tightening, small form/filter/card/table/status changes, or focused responsive fixes where the workflow is already clear.
- Use `.agents/team_design` for serious or ambiguous design work: new screens, workflow definition, visual direction, multi-surface redesigns, shell/navigation changes, shared design tokens, base UI primitives, or issues that require goal/visual/layout freeze checkpoints.
- Escalate from mini to full when the primary job is unclear, a new visual direction is needed, the change touches multiple workflow stages, or QA finds a goal, visual, structural, token, or component-source defect.

## Activation Matrix

- `vue`: any `.vue` SFC, Composition API, `<script setup>`, or Vue macros.
- `vueuse-functions`: before writing a new utility/composable, check VueUse first.
- `pinia`: `defineStore`, `*.store.ts`, or global state changes.
- `vue-router-best-practices`: `src/app/router/**`, guards, params, and route lifecycle changes.
- `vite`: `vite.config.ts`, build setup, plugins, env/build/SSR config.
- `shadcn-mcp-ui`: UI-kit work (`src/shared/ui/**`, wrapper creation, shadcn registry additions, or MCP shadcn workflow in app/pages).
- `web-design-guidelines`: only when user asks for UI/UX/accessibility review or audit.
- `service-information-ui-guard`: design-team tasks, operational service screens, dense dashboards, work queues, tables, filters, forms, summaries, or status-heavy pages.
- `service-layout-regression-guard`: service UI pages with flex/grid headers, forms, segmented controls, badges, side rails, status strips, or long Russian labels.
- `service-dense-surface-guard`: repeated cards, data tables, pills, badges, progress indicators, metadata rows, summaries, dense cards, or long Russian status/value text.
- `shadcn-component-source`: choosing, creating, or reviewing UI components; any mention of shadcn, MCP shadcn, registries, `components.json`, or `src/shared/ui`.

## Conflict Resolution

1. Direct user instruction.
2. `AGENTS.md` repository rules.
3. This orchestrator policy.
4. Individual skill details.

## Execution Checklist

1. Detect user intent and touched files.
2. Activate the minimum matching skills from the matrix.
3. Mention activated skills briefly in the work log/response.
4. Keep edits focused and avoid moving business logic to `shared/ui` or `app`.
