---
name: service-layout-regression-guard
description: Prevent visible layout regressions in dense service UI: squeezed header copy, broken segmented controls, over-wrapped Russian labels, unstable action/status rows, and responsive width failures.
---

# Service Layout Regression Guard

Use this skill for service UI implementation and QA when a page contains forms, cards, status strips, segmented choices, side rails, or long Russian text.

## Mandatory Pre-Flight Checks

- Test the layout mentally and visually at 320, 768, 1024, and 1440 px.
- Header text blocks in flex rows must have an explicit `flex-1` or stable width contract; fixed/summary blocks must use `shrink-0` only when the main text still has enough room.
- Never let introductory copy wrap one word per line. If this happens, the flex/grid width contract is wrong.
- Never ship a first-screen block that becomes a tall decorative panel while the real workflow starts below the fold.
- If any first-screen text reads vertically, stacks one or two words per line, or is squeezed beside a summary/sidebar block, the layout fails.
- Segmented controls with Russian labels must use wrapping flex or `repeat(auto-fit, minmax(...))`, not fixed `grid-cols-3` inside a narrow parent.
- Pills, badges, and segmented options must have `min-w-0`, `leading-snug`, and sensible min widths; avoid mid-word wrapping.
- Do not put long labels beside inputs in a single row. Put labels above controls.
- Repeated cards/rows must keep action/status elements stable while descriptive text wraps.
- In dense standalone blocks, replace bulky stacked buttons with checklist-style rows when the items represent selectable steps, confirmations, or requirements rather than immediate commands.
- Keep `body` neutral: do not put page container rules such as `max-width`, `padding`, `margin: auto`, grid, or flex layout on `body`. Portalled shadcn/Reka overlays, selects, dialogs, drawers, and popovers can temporarily lock or compensate `body`; app layout constraints must live on `#app`, `.app-shell`, or route-level containers so opening an overlay cannot shift the whole interface.

## Forbidden Patterns

- `min-w-0` on the main header text without `flex-1` when a sibling summary card exists.
- Fixed 3-column option groups for labels like `Конечный потребитель`, `Военное представительство есть`, or long industry/status names.
- Narrow side summaries that force primary copy into a vertical text strip.
- Oversized top panels that consume the main viewport with intro copy, decorative metrics, or a generic summary instead of the primary workflow surface.
- Two-column hero/header layouts where a wide card or summary block leaves the heading/body copy in a narrow vertical column.
- Equal-width chips where one option is much longer than the others and no min width is defined.
- Global page layout attached directly to `body`, especially when the screen uses shadcn/Reka overlay primitives such as Select, Dialog, Drawer, Popover, DropdownMenu, Tooltip, or Command.

## Done Check

- Header paragraph reads as a paragraph on desktop and tablet.
- The main workflow or task-native content is visible in the first viewport; a large intro/summary block does not push it below the fold.
- Segmented choices are readable and clickable without awkward word stacks.
- Long Russian labels wrap only at sensible word boundaries.
- Primary CTA stays visible and does not compete with secondary actions.
- Checklist rows are used instead of oversized internal buttons when they reduce block weight without hiding available choices.
- No first-screen block visually resembles a placeholder hero or generic summary card.
- Opening and closing select/dropdown/dialog/popover overlays does not change the page container width, left offset, or scroll position.
