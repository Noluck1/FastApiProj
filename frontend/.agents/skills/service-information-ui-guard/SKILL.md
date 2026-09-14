---
name: service-information-ui-guard
description: Guardrail for information-heavy service UI work. Use for service screens, dashboards, work queues, forms, tables, summaries, statuses, dense cards, operational actions, or design-team orchestration.
---

# Service Information UI Guard

Use this skill for every design-team task in this repository.

## Team Routing

- For small, local UI changes, use the mini design team in `.agents/team_design_mini`.
- For serious, ambiguous, or multi-stage service UI work, use the full design team in `.agents/team_design`.
- Keep mini work narrow: one route or component, known workflow, no new visual direction, no shell/navigation changes, no design-token changes, and no new base UI primitive decisions.
- Escalate to the full team when the local task reveals unclear intent, structural instability, visual-direction work, or component/token drift.

## Core Rules

- Treat the product as an operational service UI, not a marketing landing page or sales funnel.
- Freeze exactly one main screen job before visual design or implementation.
- Freeze exactly one primary work action per screen or action cluster unless the upstream contract explicitly says otherwise.
- Keep P0/P1 information visible; move P2/P3 details, history, audit data, secondary metrics, and rare controls into progressive disclosure.
- When a separate block would be overloaded by large button-like actions, prefer compact checklist rows for selectable tasks, requirements, or confirmations; reserve buttons for explicit commands.
- Long Russian labels and dense real data are default stress cases.
- Preserve scanability for tables, filters, forms, summaries, badges, statuses, action clusters, and repeated cards.
- Prevent visible layout regressions: header copy must not collapse into one-word lines, and segmented choices must not use fixed narrow columns for long Russian labels.
- Keep the first viewport work-native and compact. Do not create a huge main-screen block whose main contribution is introductory copy, status atmosphere, or a decorative summary wrapper.
- P0/P1 visibility does not mean putting every priority into one oversized top panel; distribute critical information into task-native controls, rows, tables, forms, or compact status strips.
- Do not let decoration, mood, or visual novelty weaken workflow clarity.

## Forbidden Default Pattern

Do not automatically add or keep a first-screen hero/summary block like:

- small eyebrow text such as `Сводка дня`
- oversized headline such as `Рабочие приоритеты без лишнего шума`
- explanatory paragraph about keeping blockers/actions/metrics on the first screen
- isolated large rounded hero card with one CTA such as `Открыть приоритет`

This block may exist only when the user explicitly asks for this exact top summary pattern or the frozen UX contract proves it is required for the primary work action. Otherwise remove it, demote it, or replace it with task-native service content.

Also reject lookalike variants of the same pattern even when the wording changes: oversized first-screen cards, tall intro panels, decorative status summaries, large empty visual blocks, or layouts that force headline/body text into narrow vertical columns.

## Design Token Rules

- Color decisions must come from `src/app/styles/tailwind.css`.
- Use semantic CSS variables and Tailwind theme variables from that file, for example `--background`, `--foreground`, `--card`, `--primary`, `--muted`, `--accent`, `--border`, `--destructive`, `--chart-*`, `--positive-foreground`, and `--negative-foreground`.
- Do not invent hardcoded palettes, arbitrary hex colors, decorative gradients, or off-token button colors.
- If the available tokens are insufficient, call out the token gap instead of silently adding a new palette.

## Component Source Rules

- Base UI controls must come from the official `shadcn-vue` workflow through MCP shadcn and registry `@shadcn`.
- `components.json` is required setup for component search/add flows.
- In this repository, implementation must consume shadcn-based controls through `src/shared/ui` wrappers.
- Do not invent custom Button/Input/Card/Dialog/Table/Badge/Select/Tabs/Accordion/Toast primitives when a shadcn-ready component exists.
- If a needed component is missing from the available source, report the missing component and create only a thin wrapper around an approved source export.

## Done Check

- One screen job and one primary work action remain clear.
- Long Russian text and dense states have explicit handling.
- Header, status strips, segmented choices, side rails, and action clusters survive 320/768/1024/1440 px without squeezed text.
- Top-of-page order is task-native and not forced into the forbidden hero/summary pattern.
- No first-screen block dominates the viewport unless it directly contains the primary workflow surface.
- No headline, paragraph, CTA, badge, or summary text is forced into a vertical strip or one-word-per-line stack.
- Colors are token-backed by `src/app/styles/tailwind.css`.
- Base components come from official shadcn-vue registry sources through repository wrappers.
