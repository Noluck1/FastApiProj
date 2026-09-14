# Service UI Staged Orchestration

This repository uses a staged orchestration model for information-heavy service interfaces. The model is tuned for request creation, work queues, tables, filters, entity cards, dashboards, forms, summaries of large information, and operational workflows. It is no longer optimized for marketing landing pages or sales funnels.

## Global Rules

- The main session owns orchestration.
- `max_depth = 1` remains in force. Agents do not spawn their own agents.
- At most 2 automatic fallback loops are allowed per stage.
- A 3rd attempt at the same stage requires escalation to the relevant human checkpoint.
- Full restart from the beginning of the pipeline is forbidden unless QA triage or the main session documents why the current contracts are invalid.
- Only `frontend_implementer` writes application code by default.
- The primary action is a service workflow action, not a sales CTA by default.
- The first screen must not default to a generic `Сводка дня` / `Рабочие приоритеты без лишнего шума` hero-summary block. Remove, demote, or replace that pattern unless the user explicitly requests it or the frozen UX contract requires it.
- The first screen must not use a lookalike oversized intro/status/summary block that dominates the viewport, pushes the real workflow below the fold, or forces copy into a vertical text column.
- Visual colors must come from `src/app/styles/tailwind.css` variables; agents must not invent hardcoded palettes.
- Base UI components must come from official `shadcn-vue` sources via MCP shadcn, `components.json`, and registry `@shadcn`. Implementation must consume them through `src/shared/ui` wrappers.
- Each screen must freeze one primary work action; competing primary-level actions must be demoted, grouped, or moved into a contextual flow.
- Dense service screens must use progressive disclosure: P0/P1 stays visible, while verbose details, history, audit data, secondary metrics, and rare controls move out of the default view.
- Long Russian text is a default stress case for tables, filters, forms, badges, row actions, and summaries.
- Mobile/tablet behavior must be explicit for tables, filters, forms, action bars, and summary panels.

## Required Skills For This Project

- `service-information-ui-guard`: mandatory for `ux_goal_agent`, `goal_research_agent`, `art_director`, `layout_stress_agent`, `frontend_implementer`, `browser_qa_agent`, and `qa_triage_agent`. Use it to prevent marketing/sales bias, weak workflow hierarchy, overloaded tables, cramped forms, unclear primary work actions, missing states, and layouts that break under long Russian content.
- `service-layout-regression-guard`: mandatory for `layout_stress_agent`, `frontend_implementer`, and `browser_qa_agent` on service UI pages with flex/grid headers, segmented controls, badges, status strips, side rails, repeated cards, or long Russian labels. Use it to prevent squeezed header copy, one-word-per-line paragraphs, and broken option groups.
- `shadcn-component-source`: mandatory for `art_director`, `layout_stress_agent`, `frontend_implementer`, `browser_qa_agent`, and `qa_triage_agent` whenever component source, wrappers, or UI primitives are involved. It must use MCP shadcn with registry `@shadcn` as the primary source flow.
- `service-dense-surface-guard`: mandatory for `layout_stress_agent`, `frontend_implementer`, and `browser_qa_agent` when working on repeated cards, pills, badges, progress indicators, and data tables. Use it to prevent glued inline text, wrapped pills, and unstable column widths.
- `shadcn-mcp-ui`: mandatory for `frontend_implementer` when touching `src/shared/ui`, wrappers, `components.json`, or registry-driven UI additions.
- `vue-best-practices`: mandatory for Vue SFC, TypeScript, template state, and build-safe implementation work.
- `vue-router-best-practices`: mandatory when route tabs, `RouterLink`, route meta, query params, workflow deep links, or navigation state are touched.
- `agent-browser`: mandatory for rendered QA through `browser_qa_agent`.

## Human Checkpoints

Three human checkpoints are mandatory:

1. `Goal Freeze Checkpoint`
2. `Visual Freeze Checkpoint`
3. `QA Triage Checkpoint`

Each checkpoint freezes one decision layer before the next loop proceeds.

## Stage 1: Context Pack

- Owner: main session
- Input contract:
  - route
  - screen type
  - user role
  - service workflow
  - required content
  - candidate work actions
  - known states
  - constraints
- Allowed outputs:
  - normalized task context
  - known unknowns
  - stage entry packet
- Proceed when:
  - the task has enough visible context for `ux_goal_agent` to begin
- Fallback when:
  - core identifiers, route purpose, workflow step, or user role are missing
- Automatic loop limit:
  - 2
- Allowed parallelism:
  - none beyond read-only context gathering

## Stage 2: Goal Resolution

- Primary owner: `ux_goal_agent`
- Optional service owner on fallback: `goal_research_agent`
- Input contract:
  - context pack
  - route defaults
  - service/workflow context
  - candidate work actions
- Allowed outputs:
  - `mode = final_contract`
  - `mode = needs_resolution`
- Proceed when:
  - `ux_goal_agent` returns `final_contract` with one screen job, one primary work action, and confidence sufficient for downstream use
- Fallback when:
  - `goal_confidence = low`
  - ambiguity still blocks a safe freeze
- Automatic loop limit:
  - 2 total passes across `ux_goal_agent` and `goal_research_agent`
- Allowed parallelism:
  - at most 2 concurrent tasks
  - normal case: `ux_goal_agent` first
  - fallback case: `goal_research_agent` may run before a second `ux_goal_agent` pass

## Stage 3: Goal Freeze Checkpoint

- Owner: human checkpoint
- Input contract:
  - latest `ux_goal_agent` contract
  - optional `goal_research_agent` packet
- Allowed outputs:
  - frozen semantic contract
  - explicit request for more context
- Proceed when:
  - one screen job and one primary work action are accepted for the screen
- Fallback when:
  - service intent remains ambiguous after 2 automatic loops
- Automatic loop limit:
  - none; checkpoint is mandatory once reached
- Allowed parallelism:
  - none

## Stage 4: Visual Exploration

- Primary owner: `art_director`
- Secondary advisory owner: `layout_stress_agent` in `baseline_structural_envelope`
- Input contract:
  - frozen semantic contract
  - surface type
  - information pressure
  - interaction mode
- Allowed outputs:
  - 2-3 controlled visual options
  - one recommended option
  - baseline structural envelope
- Proceed when:
  - visual exploration produces distinct service-appropriate options and one is recommended
- Fallback when:
  - options are not materially distinct
  - options contradict the semantic contract
  - options drift into marketing/landing-page presentation for a workspace screen
- Automatic loop limit:
  - 2
- Allowed parallelism:
  - at most 3 advisory tasks
  - `art_director` exploration plus baseline structural envelope may overlap after goal freeze

## Stage 5: Visual Freeze Checkpoint

- Owner: human checkpoint
- Input contract:
  - `art_director` exploration packet
  - baseline structural envelope notes
- Allowed outputs:
  - one selected visual option
  - final visual contract request
- Proceed when:
  - exactly one option is selected and frozen
- Fallback when:
  - none of the explored options is acceptable
- Automatic loop limit:
  - none; checkpoint is mandatory once reached
- Allowed parallelism:
  - none

## Stage 6: Structural Stress Validation

- Owner: `layout_stress_agent`
- Input contract:
  - frozen semantic contract
  - selected visual option
  - baseline structural envelope
- Allowed outputs:
  - `acceptance_status = pass`
  - `acceptance_status = pass_with_constraints`
  - `acceptance_status = fail`
- Proceed when:
  - status is `pass` or `pass_with_constraints`
- Fallback when:
  - the selected direction breaks the primary workflow
  - tables, forms, summaries, filters, or state handling remain structurally unstable
- Automatic loop limit:
  - 2
- Allowed parallelism:
  - advisory only; no implementation in parallel

## Stage 7: Implementation

- Owner: `frontend_implementer`
- Input contract:
  - frozen semantic contract
  - final visual contract
  - structural contract
  - optional QA re-entry packet
- Allowed outputs:
  - implementation contract
  - render-ready UI
- Proceed when:
  - code changes are complete and locally verified
- Fallback when:
  - implementation reveals an upstream contract contradiction
- Automatic loop limit:
  - 2 before human checkpoint escalation through QA triage
- Allowed parallelism:
  - implementation stays single-owner

## Stage 8: Rendered QA

- Owner: `browser_qa_agent`
- Input contract:
  - render-ready UI
  - frozen upstream contracts
  - implementation notes
- Allowed outputs:
  - findings with owner hints and return stages
  - no-issue report
  - residual risks
- Proceed when:
  - no blocking findings remain
- Fallback when:
  - observable defects are found
- Automatic loop limit:
  - 2 on the same re-entry packet before checkpoint escalation
- Allowed parallelism:
  - none before a stable render exists

## Stage 9: QA Triage

- Owner: `qa_triage_agent`
- Input contract:
  - rendered QA findings
  - latest upstream contracts
  - implementation notes
- Allowed outputs:
  - grouped findings
  - one primary owner per finding
  - re-entry stage
  - required inputs
  - rework scope
  - retest plan
  - escalate-to-human flag
- Proceed when:
  - targeted re-entry scope is clear
- Fallback when:
  - ownership remains mixed or low-confidence
- Automatic loop limit:
  - 2
- Allowed parallelism:
  - at most 2 concurrent tasks
  - `qa_triage_agent` plus owner preparation only

## Stage 10: QA Triage Checkpoint

- Owner: human checkpoint
- Input contract:
  - triage packet
  - grouped findings
  - loop count
- Allowed outputs:
  - approved re-entry plan
  - escalation to upstream redefinition
- Proceed when:
  - one re-entry path is chosen
- Fallback when:
  - ownership or scope remains disputed
- Automatic loop limit:
  - none; checkpoint is mandatory before a new loop starts
- Allowed parallelism:
  - none

## Stage 11: Targeted Re-entry

- Owner: stage-specific
- Possible owners:
  - `ux_goal_agent`
  - `art_director`
  - `layout_stress_agent`
  - `frontend_implementer`
- Input contract:
  - triage packet
  - required upstream contracts
  - minimal rework scope
- Allowed outputs:
  - revised contract or implementation at the selected stage
- Proceed when:
  - the targeted issue is fixed and ready for the next validation stage
- Fallback when:
  - the selected owner proves not to be sufficient
- Automatic loop limit:
  - 2 on the same stage, then escalate
- Allowed parallelism:
  - only within the budget of the selected stage

## Owner Mapping for Findings

- `goal_hierarchy` -> `Goal Resolution`
- `visual_emphasis` -> `Visual Exploration`
- `layout_density` -> `Structural Stress Validation`
- `responsive_overflow` -> `Structural Stress Validation`
- `implementation_bug` -> `Implementation`
- `interaction_regression` -> `Implementation`
- `component_source_drift` -> `Implementation`
- `token_drift` -> `Implementation` unless the visual contract explicitly requested off-token color, then `Visual Exploration`
- `forbidden_hero_summary` -> `Goal Resolution` if present in the frozen goal contract, otherwise `Implementation`
- `mixed_ownership` -> `QA Triage` decides the owner and may assign one observer

## Concurrency Budgets

- Goal stage: max 2 concurrent tasks
- Visual stage: max 3 concurrent advisory tasks
- QA stage: max 2 concurrent tasks
- No parallel implementation and upstream redefinition
- No parallel launch of `browser_qa_agent` before a stable render

## What This Model Prevents

- Marketing/sales CTA bias on service screens
- Hard-stop as the only response to uncertainty
- Blanket loop-back from QA straight to implementation
- Simultaneous full rework loops for one finding
- Hidden nested delegation inside agent runs
- Visual exploration proceeding without frozen semantic intent
- Decorative redesign that weakens tables, forms, summaries, or workflow states
