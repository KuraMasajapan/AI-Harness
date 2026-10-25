# Single-Agent Loop + Skills: Evaluation Candidate (2026-10-25)

Status: **CANDIDATE / HIGH; ABSORB as evaluation method, not a Core change**  
Origin: Grok daily report (2026-10-25), independently reviewed  
Primary: https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop

## Verified primary-source claim
Anthropic's Applied AI article reports that, in several enterprise cases, a single agent loop with progressive skill/tool disclosure often outperformed both large monolithic prompts and orchestrated specialist subagents on quality, latency and cost. It cites a customer seeing roughly 2x faster runtime. These are **reported cases**, not universal reproducible performance guarantees.

The article explicitly preserves subagents for independent verification, true parallelism, context-window isolation, and conflicting instructions/tool-selection problems. It recommends end-to-end evaluation, including a starter set of about ten golden tasks, and one-at-a-time migration.

## AI-Harness comparison
- `HARNESS.md` and `core/WORKFLOW.md` already specify progressive disclosure and task-scaled context loading; therefore **not a new principle**.
- `core/RULES.md` already cautions against unnecessary complexity.
- Trinity independent review / sealed boundaries are not automatically redundant: preserve them when they provide isolation or measurable reliability.
- The value is a measurable test method for avoiding unnecessary subagents, especially in future Hermes / orchestration work.

## Suggested independent evaluation (requires approval before execution)
1. Select 10 representative tasks including normal, failure, privacy/permission and multi-step cases.
2. Compare current design vs a minimal single-agent + progressively loaded skills/tools prototype; same data/model/budgets where possible.
3. Measure task success, rule compliance, missed tools, context cost, latency, regressions and recovery.
4. Keep the multi-agent boundary where it wins; simplify only demonstrated redundancy.
5. Treat model-version effects separately and do not modify Trinity/Core during experiment.

## Risk and alternatives
Premature merging may erase independent checks, permissions, fresh-context boundaries and auditability. A simple checklist or selective skills may yield most of the benefit without architectural change.

## Decision
**CANDIDATE (HIGH) / ABSORB-EXPERIMENT**. Preserve research and eval design; no auto-migration, installation, Core or Trinity change.