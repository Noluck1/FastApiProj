---
name: shadcn-mcp-ui
description: Use official shadcn-vue components through MCP shadcn and repository wrappers. Trigger when tasks involve shared UI, base primitives, components.json, or registry-driven component additions.
---

# Shadcn MCP UI

Use this skill for UI work in this repository that touches base components, shared wrappers, or registry-driven component additions.

## Core Rules

- Primary component source is the official `shadcn-vue` registry accessed through MCP shadcn.
- Use registry namespace `@shadcn` unless the task explicitly introduces another registry.
- `components.json` is required infrastructure and must stay valid.
- Use `@/shared/ui` as the default import entry point in pages and page components.
- Keep app/page code off raw generated registry paths; expose components through `src/shared/ui`.
- Keep shared UI presentational; do not place business logic in `shared/ui`.
- Component colors must resolve to variables from `src/app/styles/tailwind.css`.
- Keep global `body` layout-neutral when using shadcn/Reka overlay primitives such as Select, Dialog, Drawer, Popover, DropdownMenu, Tooltip, Command, or Sheet. These primitives can portal to `body` and temporarily apply scroll-lock or pointer-event compensation to it; page containers (`max-width`, `padding`, `margin: auto`, grid/flex layout) must live on `#app`, `.app-shell`, or route containers instead.
- Do not preserve generated table defaults that make dense service tables scroll internally by accident. If a generated Table wrapper uses `overflow-auto` and cells/heads use `whitespace-nowrap`, adapt the wrapper so scrolling is opt-in and table text can wrap/truncate through the page-specific column contract.
- Button text must have a stable line-height contract that is tall enough for Cyrillic glyphs. Do not use `leading-none` for text buttons; prefer a compact readable line-height such as `leading-tight` so labels are vertically centered without clipping descenders.

## Workflow

1. Check whether the required component already exists in `src/shared/ui`.
2. If missing, use MCP shadcn to inspect registry `@shadcn`.
3. Use MCP shadcn `get_add_command_for_items` for the exact install command after choosing registry items.
4. Add the generated component into `src/shared/ui/<component>` using the official shadcn-vue structure.
5. Re-export from the component folder and `src/shared/ui/index.ts`.
6. Use the shared export from pages via `@/shared/ui`.

## Wrapper Patterns

- Pass-through controls: use `defineOptions({ inheritAttrs: false })` and forward attrs with `v-bind="$attrs"`.
- Slot-based controls: forward attrs and keep the wrapper surface minimal.
- Reuse `src/shared/lib/utils.ts` and `cn()` for class composition.

## Failure Policy

- If `components.json` is missing or invalid, fix project setup before adding components.
- If MCP shadcn or registry `@shadcn` does not provide the needed primitive, report the gap instead of inventing a replacement.
- If the generated component conflicts with repository constraints, adapt via a thin wrapper instead of forking the generated API in page code.
