# Project Agents

This project uses a staged orchestration model for design and frontend work in Codex.

The team is tuned for information-heavy service interfaces: request creation, work queues, tables, filters, entity cards, dashboards, forms, summaries of large information, statuses, and operational workflows. It is not optimized for marketing landing pages or sales funnels by default.

Core agents:

- `ux_goal_agent` - resolves screen job, primary work action, information hierarchy, and state requirements
- `art_director` - explores and finalizes visual direction for operational service screens
- `layout_stress_agent` - validates structural survivability under real content, state, table, form, and responsive stress
- `frontend_implementer` - implements approved UX, visual, and layout decisions
- `browser_qa_agent` - inspects the rendered UI and reports observable defects

Service agents:

- `goal_research_agent` - gathers missing workflow context when the job/action contract is ambiguous
- `qa_triage_agent` - classifies findings and routes re-entry to the correct owner stage

Mini-team note:

- Small local UI tasks use the separate mini team in `../team_design_mini`.
- This folder remains the full staged design team for serious or ambiguous service UI work.

Required project skill:

- `service-information-ui-guard` must be used by every agent for service UI work.
- `service-layout-regression-guard` must be used by layout, implementation, and browser QA work to catch squeezed headers, broken segmented controls, and long-Russian-label failures.
- `service-dense-surface-guard` must be used by layout, implementation, and browser QA work for repeated cards, tables, pills, badges, progress indicators, metadata rows, and dense summaries.
- `shadcn-component-source` must be used when components, wrappers, or UI primitives are selected or reviewed.
- `shadcn-mcp-ui` must be used by implementation work touching `src/shared/ui`, `components.json`, or shadcn registry additions.

Global design constraints:

- Pull visual colors from `src/app/styles/tailwind.css` variables only.
- Use official `shadcn-vue` components through MCP shadcn, registry `@shadcn`, and `src/shared/ui` wrappers in app code.
- Do not invent base UI primitives.
- Do not force the screenshot-like top hero/summary block (`Сводка дня`, `Рабочие приоритеты без лишнего шума`, explanatory copy, one CTA) as the first block. Remove or demote it unless explicitly required.
- Do not replace that pattern with a lookalike huge first-screen intro/status/summary block. The first viewport should expose task-native service content and must not squeeze text into a vertical column.

Read [ORCHESTRATION.md](./ORCHESTRATION.md) for the full staged flow, loop policy, human checkpoints, and concurrency budgets.
Read [../team_design_mini/README.md](../team_design_mini/README.md) for the compact team used on small, local UI tasks.
Read [SKILLS_AND_AGENTS_OVERVIEW.md](./SKILLS_AND_AGENTS_OVERVIEW.md) for a compact map of all skills, agents, source rules, and ownership.

## Stage Summary

1. `Context Pack`
2. `Goal Resolution`
3. `Goal Freeze Checkpoint`
4. `Visual Exploration`
5. `Visual Freeze Checkpoint`
6. `Structural Stress Validation`
7. `Implementation`
8. `Rendered QA`
9. `QA Triage`
10. `QA Triage Checkpoint`
11. `Targeted Re-entry`

## Handoff Contracts

- `ux_goal_agent` defines the semantic contract:
  - `mode`
  - `screen_job`
  - `job_rationale`
  - `primary_work_action`
  - `primary_work_action_validation`
  - `goal_confidence`
  - `ambiguity_causes`
  - `candidate_jobs`
  - `candidate_primary_actions`
  - `evidence_used`
  - `recommended_resolution_path`
  - `questions_for_human_checkpoint`
  - `secondary_actions`
  - `information_priority`
  - `attention_flow`
  - `disclosure_plan`
  - `state_matrix`
  - `remove_or_demote`
  - `non_goals`
  - `success_criteria`
  - `failure_signs`
  - `risks`
- `goal_research_agent` defines the goal research contract:
  - `job_hypotheses`
  - `recommended_job`
  - `recommended_primary_work_action`
  - `supporting_signals`
  - `conflicting_signals`
  - `resolvable_unknowns`
  - `needs_human_confirmation`
- `art_director` defines the visual direction contract:
  - `mode`
  - `visual_options`
  - `recommended_option`
  - `selection_criteria`
  - `selected_visual_option`
  - `visual_thesis`
  - `distinctive_mechanism`
  - `product_character`
  - `reference_traits`
  - `palette_direction`
  - `ui_motifs`
  - `allowed_visual_devices`
  - `forbidden_shortcuts`
  - `anti_patterns`
  - `non_goals`
  - `typography_strategy`
  - `color_strategy`
  - `density_strategy`
  - `emphasis_strategy`
  - `motion_guidance`
  - `risk_profile`
  - `tradeoffs_and_risks`
  - `self_check`
- `layout_stress_agent` defines the structural survivability contract:
  - `phase`
  - `acceptance_status`
  - `layout_structure`
  - `section_order`
  - `block_roles`
  - `capacity_rules`
  - `stress_cases`
  - `responsive_rules`
  - `state_rules`
  - `overflow_risks`
  - `progressive_disclosure_rules`
  - `adaptation_strategies`
  - `growth_assumptions`
  - `breakpoints_of_failure`
  - `conditional_acceptance_rules`
  - `future_risk_zones`
  - `implementation_warnings`
  - `non_goals`
  - `failure_signs`
- `frontend_implementer` produces the implementation contract:
  - `summary_of_changes`
  - `files_changed`
  - `implementation_notes`
  - `assumptions_made`
  - `verification_performed`
  - `retest_scope_completed`
  - `residual_risks`
  - `blockers`
- `browser_qa_agent` produces the rendered QA contract:
  - `findings`
  - `residual_risks`
  - or the no-issue report with routes, viewports, workflow states, and stress areas checked
- `qa_triage_agent` produces the re-entry contract:
  - `triage_summary`
  - `grouped_findings`
  - `owner_assignment`
  - `return_stage`
  - `required_inputs`
  - `rework_scope`
  - `retest_plan`
  - `escalate_to_human`

## Flow Rules

- `ux_goal_agent` is allowed to return `mode = needs_resolution` instead of causing an immediate hard stop.
- If `goal_confidence = low`, the next step is `goal_research_agent`, not visual or implementation work.
- `art_director` may explore 2-3 controlled directions in `exploration_mode`, but only one selected option may proceed downstream after the visual freeze checkpoint.
- `layout_stress_agent` should prefer `pass_with_constraints` over rejection when the primary workflow survives with explicit structural constraints.
- `browser_qa_agent` must classify each finding by owner and return stage instead of routing all defects to `frontend_implementer`.
- `qa_triage_agent` is the only agent that may convert mixed findings into a targeted re-entry packet.
- Downstream agents must not compensate for unresolved upstream ambiguity.

## Human Checkpoints

Three human checkpoints are mandatory:

1. After goal resolution is stable enough to freeze the semantic contract.
2. After visual exploration when one direction must be selected.
3. After QA triage when a new re-entry loop is about to start.

## Writing Rule

- Only `frontend_implementer` should modify application code by default.
- Other agents are advisory unless explicitly tasked otherwise.
- Keep code edits owned by one writing agent at a time.

## Parallelism Rule

- `max_threads = 5` is available capacity, not a recommendation to run five agents on every task.
- Use parallelism only when outputs are advisory and independent inside the active stage budget.
- Do not parallelize agents whose outputs depend on unresolved upstream decisions.
- Goal stage budget: at most 2 concurrent tasks (`ux_goal_agent` plus `goal_research_agent` on fallback).
- Visual stage budget: at most 3 concurrent advisory tasks.
- QA stage budget: at most 2 concurrent tasks (`qa_triage_agent` plus owner preparation).
- Do not run `frontend_implementer` before the upstream contract is stable.
- Do not run `browser_qa_agent` before there is a real render to inspect.
- Do not let one finding fan out into multiple full rework loops at once.

## Loop Policy

- At most 2 automatic fallback loops are allowed per stage.
- A 3rd attempt at the same stage must escalate to the relevant human checkpoint.
- Full restart from the beginning of the pipeline is forbidden unless `qa_triage_agent` or the main session documents why the current contracts are invalid.

## Orchestration Note

- With `max_depth = 1`, orchestration is intentionally centralized in the main session.
- Agents should not assume they can delegate further work from inside their own runs.
- Service branches, fallback passes, and re-entry loops must all be launched by the main session.
