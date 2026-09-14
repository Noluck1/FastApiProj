# Skills And Agents Overview

This file is the short operating map for the repository skills and the design-agent team.

## Global Source Rules

- Colors come from `src/app/styles/tailwind.css`. Agents should use semantic variables such as `--background`, `--foreground`, `--card`, `--primary`, `--muted`, `--accent`, `--border`, `--destructive`, `--chart-*`, `--positive-foreground`, and `--negative-foreground`.
- Components come from the official `shadcn-vue` registry workflow through MCP shadcn, `components.json`, and registry `@shadcn`. Repository code must consume components through `src/shared/ui` wrappers.
- Pages must import shared UI from `@/shared/ui`, not raw generated component paths directly.
- The screenshot-like top block with `Сводка дня`, `Рабочие приоритеты без лишнего шума`, explanatory copy, and a single CTA is forbidden as a default first block. It can be used only when explicitly requested or required by the frozen UX contract.
- Lookalike oversized first-screen intro/status/summary blocks are also forbidden when they dominate the viewport, push task-native content below the fold, or force text into vertical columns.

## Repository Skills

- `project-default`: Always-on repository orchestrator. Applies architecture rules, activates Vue/UI/router/Vite/Pinia/design skills by intent, and now enforces service UI, shadcn source, and `tailwind.css` color-token rules.
- `service-information-ui-guard`: Service UI guard for operational screens. Prevents landing-page bias, unclear primary action, overloaded first screens, weak progressive disclosure, long Russian text failures, off-token colors, and invented base components.
- `service-layout-regression-guard`: Layout QA guard for service pages. Prevents squeezed flex headers, one-word-per-line copy, broken segmented controls, unstable status/action rows, and long Russian label failures across 320/768/1024/1440 px.
- `service-dense-surface-guard`: Dense-surface guard for repeated cards, tables, pills, badges, metadata rows, progress indicators, summaries, and long Russian status/value text.
- `shadcn-component-source`: Component-source guard. Requires MCP shadcn + registry `@shadcn`, routes implementation through `src/shared/ui`, and blocks invented UI primitives.
- `shadcn-mcp-ui`: Wrapper and registry workflow policy for shared UI. Keeps app imports inside `@/shared/ui` and uses `components.json` as project setup.
- `vue-best-practices`: Baseline for Vue SFC, Composition API, `<script setup>`, TypeScript, reactivity, lifecycle, rendering, and maintainability.
- `vue`: Vue 3 Composition API and macro details for `.vue` implementation work.
- `vueuse-functions`: Use before creating new utilities or composables; prefer VueUse where it already solves the problem.
- `pinia`: Use for `defineStore`, global stores, store composition, HMR, SSR/testing patterns.
- `vue-router-best-practices`: Use for routes, guards, params, query state, `RouterLink`, route tabs, and navigation lifecycle.
- `vite`: Use for Vite config, plugins, build, env, SSR, and tooling changes.
- `web-design-guidelines`: Use for explicit UI/UX/accessibility audits.

## Design Agents

- `ux_goal_agent`: Owns the semantic contract. It defines one screen job, one primary work action, information priority, attention flow, disclosure plan, required states, demotions, non-goals, and risks. It must remove or demote generic hero-summary blocks unless they directly support the primary job.
- `goal_research_agent`: Advisory fallback when the goal is ambiguous. It gathers route/domain/workflow evidence and narrows hypotheses for the next `ux_goal_agent` pass.
- `art_director`: Owns visual direction after the UX contract is stable. It must use `tailwind.css` token roles, avoid hardcoded palettes, avoid forced hero-first patterns, and avoid visual directions that require invented component primitives.
- `layout_stress_agent`: Owns structural survivability. It validates section order, block roles, capacity, long Russian text, responsive behavior, states, and whether the layout can be built with approved shadcn components.
- `frontend_implementer`: Only default writing agent. It implements frozen contracts in Vue, uses `@/shared/ui` wrappers, creates thin wrappers around approved shadcn exports when missing, uses `tailwind.css` variables, and stops instead of inventing missing primitives.
- `browser_qa_agent`: Reviews the rendered UI. It checks workflow clarity, long Russian text, dense surfaces, responsive behavior, forbidden hero-summary drift, visible token consistency, and shadcn component-system alignment.
- `qa_triage_agent`: Routes QA findings to the smallest correct owner stage. It now recognizes component-source drift, token drift, and forbidden hero-summary drift instead of sending every issue to implementation.

## Normal Flow

1. Main session prepares the context pack.
2. `ux_goal_agent` freezes the screen job and primary work action, or routes ambiguity to `goal_research_agent`.
3. Human goal freeze checkpoint approves the semantic contract.
4. `art_director` explores visual direction using `tailwind.css` token roles and shadcn component constraints.
5. Human visual freeze checkpoint selects one direction.
6. `layout_stress_agent` validates structure, capacity, states, and responsive behavior.
7. `frontend_implementer` writes code using `src/shared/ui` wrappers and approved tokens.
8. `browser_qa_agent` checks the rendered UI.
9. `qa_triage_agent` routes defects back to the smallest correct owner if needed.

## Mini Flow For Small Tasks

The mini team lives in `.agents/team_design_mini`. Use it when the task is local, the route purpose is already clear, and the change does not redefine the shell, navigation, primary workflow, visual direction, design tokens, or base UI primitives.

1. `mini_goal_layout_agent` checks one primary local action, P0/P1 visibility, dense-surface risks, long Russian text, and responsive survivability.
2. `mini_frontend_implementer` makes the narrow Vue/UI patch through `@/shared/ui`, approved shadcn sources, and `tailwind.css` tokens.
3. `mini_browser_qa_agent` verifies the changed route or surface at focused desktop and mobile widths.

Escalate to the full team when intent is ambiguous, visual direction is being invented, the change touches multiple workflow stages, or QA finds an upstream contract defect.

## Duplication Policy

- The shared skills hold cross-cutting rules; agents should reference them instead of duplicating full policy text.
- `service-information-ui-guard` owns service workflow, density, progressive disclosure, and forbidden hero-summary rules.
- `service-dense-surface-guard` owns repeated dense surface readability and scanability rules.
- `shadcn-component-source` owns component source rules.
- `shadcn-mcp-ui` owns local wrapper and registry mechanics.
- Agent prompts keep only role-specific consequences of those rules.
