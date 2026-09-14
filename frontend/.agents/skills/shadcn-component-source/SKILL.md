---
name: shadcn-component-source
description: Enforce official shadcn-vue registry sourcing for Vue UI work. Use when creating, selecting, wrapping, or reviewing UI components.
---

# Shadcn Component Source

Use this skill whenever UI components are selected, created, wrapped, or reviewed.

## Source Of Truth

- Primary implementation source: official `shadcn-vue` registry/docs via MCP shadcn and `components.json`.
- Required registry namespace: `@shadcn`.
- Repository implementation path: `src/shared/ui`, which exposes shadcn-based components to pages and page-local components.

## Non-Negotiable Rules

- Do not invent base UI primitives.
- Do not create page-local replacements for existing shadcn components.
- Do not import raw generated registry components directly from `src/pages/**`; pages must import from `@/shared/ui`.
- Do not fork component APIs or styling patterns unless repository constraints clearly require a very small local adaptation.
- Do not bypass MCP shadcn/registry workflow when an official shadcn-vue component exists.
- Native semantic HTML is allowed for document structure and content, but not as a substitute for an available shadcn primitive such as Button, Input, Dialog, Card, Tabs, Select, Badge, Table, Accordion, Dropdown, Tooltip, Checkbox, RadioGroup, Switch, or Toast.

## Wrapper Workflow

1. Check `src/shared/ui` for an existing wrapper.
2. Check `components.json` and use MCP shadcn with registry `@shadcn` to locate the component.
3. After selecting an item, use MCP shadcn `get_add_command_for_items` for the exact add command; do not rely on search-result add-command text if it is incomplete.
4. Add or update the generated component in `src/shared/ui/<component>`.
5. Re-export from the component folder and `src/shared/ui/index.ts`.
6. Use the shared export from pages and page components.

## Missing Component Policy

- If `components.json` is missing or broken, stop and restore the shadcn-vue project setup first.
- If MCP shadcn cannot find the needed primitive in registry `@shadcn`, report the gap instead of designing an invented substitute.
- If the registry component exists but the repository export is missing, add only the minimal generated component and shared export needed by the app.

## Token Policy

- Component color usage must resolve to variables from `src/app/styles/tailwind.css`.
- Prefer semantic classes and CSS variables over arbitrary values.
- Do not add new color tokens inside component wrappers unless the user explicitly approves a token update.
