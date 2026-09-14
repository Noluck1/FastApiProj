---
name: service-dense-surface-guard
description: Guardrail for dense service UI surfaces with repeated cards, tables, pills, badges, metadata rows, progress indicators, and long Russian text.
---

# Service Dense Surface Guard

Use this skill for dense service UI implementation and QA when a page contains repeated cards, data tables, badges, pills, progress indicators, metadata rows, summaries, or long Russian labels.

## Core Rules

- Treat dense surfaces as repeated systems, not isolated polished examples.
- Preserve scanability before adding visual weight.
- Keep labels, values, statuses, and actions visually separable; do not let inline text glue together.
- Long Russian labels are a default stress case for badges, table cells, card titles, row metadata, tabs, filters, and action labels.
- Pills and badges must not wrap into unreadable fragments. Prefer bounded widths, sensible wrapping, or truncation with access to the full value.
- Progress/status rows must keep the status, value, and next action stable while descriptions wrap.
- Tables need explicit column priority, overflow behavior, and a mobile fallback when the surface is user-facing.
- Do not make internal table scroll the default solution for dense service screens. Prefer column priority, wrapping/truncation, fixed layout contracts, and mobile row cards; use table-region horizontal scroll only as an explicit exception for truly wide comparison data.
- Repeated cards must avoid uncontrolled height explosions; secondary detail should move into disclosure when it breaks rhythm.
- Do not solve density with smaller text alone. Reduce simultaneous emphasis, group related data, or disclose lower-priority detail.

## Risk Patterns

- Multiple badges touching each other without spacing or clear priority.
- Metadata rows where label/value pairs read as one continuous sentence.
- Status pills that become two or three lines while neighboring content stays compact.
- Equal-width table columns with mixed long Russian labels and short numeric/status values.
- Shared table primitives that combine `overflow-auto` containers with default `whitespace-nowrap` cells, causing hidden horizontal scrollbars and clipped row actions.
- Repeated cards where one long item stretches the whole grid and breaks comparison.
- Progress indicators that lose their numeric value or state label on narrow screens.
- Action rows where secondary controls visually compete with the primary action.

## Done Check

- Repeated rows/cards remain scannable with long Russian content.
- Badges, pills, and status labels keep readable boundaries.
- Table columns have clear priority and responsive behavior.
- Tables do not show an internal horizontal scrollbar in normal desktop service layouts; mobile uses a readable fallback instead of forcing users to scroll inside the table.
- Metadata label/value pairs remain visually distinct.
- Progress/status surfaces keep state, value, and next action understandable.
- Dense blocks use progressive disclosure for verbose P2/P3 detail.
