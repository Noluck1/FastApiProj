# Mini Design Team Flow

This folder contains the compact design team for small local UI tasks. Use `.agents/team_design` instead for serious, ambiguous, multi-surface, or visual-direction work.

Use this flow for small local UI tasks where the screen job is already clear and the work does not redefine navigation, shell structure, product workflow, design tokens, or base UI primitives.

The mini team is a compact version of the full design team. It keeps the same service UI guardrails, but removes visual freeze checkpoints and multi-stage fallback loops for routine patches.

## When To Use

- Fixing a local layout regression in one route or component.
- Tightening a form, filter row, status strip, repeated card, table, or summary block.
- Adding a small page-local UI state when the workflow is already known.
- Replacing a bulky action cluster with a clearer local pattern.
- Adjusting responsive behavior for a known surface.

## When To Escalate

- The primary workflow or route purpose is ambiguous.
- The task introduces a new visual direction.
- The work changes app shell, navigation, routing model, shared design tokens, or base UI primitives.
- A required shadcn primitive is missing or the registry/setup is broken.
- QA indicates the defect belongs to goal hierarchy, visual direction, or structural contract, not implementation.

## Mini Team

1. `mini_goal_layout_agent`
   - Read-only.
   - Combines the small-task parts of `ux_goal_agent` and `layout_stress_agent`.
   - Confirms the local job/action, P0/P1 visibility, dense-surface risks, long Russian text handling, and responsive constraints.

2. `mini_frontend_implementer`
   - Workspace-write.
   - Implements only the narrow approved patch.
   - Uses `@/shared/ui`, MCP shadcn registry `@shadcn`, `components.json`, and `src/app/styles/tailwind.css` tokens.

3. `mini_browser_qa_agent`
   - Read-only.
   - Reviews the rendered changed surface only.
   - Checks focused desktop/mobile widths, long Russian text, primary action clarity, dense-surface scanability, and observable shadcn/token drift.

## Fast Contract

- task_scope
- route_or_component
- local_screen_job
- primary_local_action
- affected_surface
- required_states
- dense_surface_risks
- responsive_checks
- shadcn_components_needed
- token_constraints
- verification_scope

## Flow

1. Main session prepares a short context pack.
2. `mini_goal_layout_agent` returns `pass`, `pass_with_constraints`, or `escalate_full_team`.
3. `mini_frontend_implementer` edits only the affected files.
4. `mini_browser_qa_agent` checks the changed route or surface.
5. If QA finds a local implementation defect, return once to `mini_frontend_implementer`.
6. If QA finds goal, visual, structural, token, or component-source drift, escalate to the full team.

## Limits

- At most one implementation loop before escalation.
- No separate visual exploration stage.
- No design-system rewrite.
- No invented base primitives.
- No off-token color additions.
- No broad refactors outside the affected surface.
