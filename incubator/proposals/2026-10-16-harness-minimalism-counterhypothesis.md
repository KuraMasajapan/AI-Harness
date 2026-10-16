# Harness minimalism — counter-hypothesis and design principle

**Date:** 2026-10-16
**Status:** RESEARCH / DESIGN PHILOSOPHY ONLY; NOT ADOPTED POLICY
**Initial assessment:** A+ / CANDIDATE (counter-hypothesis)
**Human decision:** Preserve the idea as a potentially valid blind spot. Saving does **not** imply that the project must adopt it or schedule an immediate evaluation.

## Trigger

A user-shared social comment (author and original URL not supplied) argued, in essence:

> 「そう、私が過度なユーザーハーネス否定派であったり、よくAI性善説的なことをいうのはこの考え方に近い。人間の余計な所作がモデルの性能を阻害する、的な⋯」

This is a *viewpoint*, not experimental proof that harnesses are harmful or that models are reliably safe. The user's response: this might have been a blind spot; the philosophy is not necessarily wrong; archive it even if future retrieval is uncertain.

## Central counter-hypothesis

**An excessively prescriptive user-created harness can obstruct model capabilities, add unnecessary process overhead, and lower net quality or efficiency.** Stronger models may need less procedural scaffolding for some tasks. Conversely, a model's capabilities do not replace external authorization, memory integrity, or testable evidence.

The correct question is not “more harness or less harness?” but **which constraints demonstrably improve outcomes for which tasks, at what cost?**

## Tension with existing research

- Superpowers (https://github.com/obra/superpowers) emphasizes structured brainstorming, planning, subagents, TDD and review.
- Existing AI-Harness already uses RULES / WORKFLOW / ACCESS, Human decisions, checkpoints and Trinity comparisons.
- Adding every attractive workflow can duplicate checks, increase tokens and Human intervention, delay simple changes, and cause instruction conflicts.
- Removing all structure can expose authorization, reproducibility, specification drift, or forgotten decisions.

**Distinguish:** (1) optional procedural scaffolding, (2) task-dependent quality gates, and (3) non-negotiable safety/authorization boundaries. Minimalism should target unnecessary overhead, **not** silently relax Human approval or tool permissions.

## Possible falsifiable study — future only

Compare the same representative tasks under:
- A: Minimal task instructions, with the same mandatory security/authorization constraints;
- B: Current AI-Harness workflow;
- C: Additional Superpowers-style workflow.

Measure acceptance-criteria correctness, regressions, rework, elapsed time, token/API cost, Human interventions, and instruction conflicts. Stratify by task complexity and risk. Use independent outcome evaluation and avoid assuming any condition will win.

A favorable result for minimalism on simple tasks would **not** justify removing safeguards for high-impact tasks. Conversely, improvement under heavy structure on complex tasks would **not** justify imposing it everywhere.

## Candidate design principle

> **Harness should earn its complexity.** Preserve only constraints that demonstrably improve correctness, safety, continuity, or accountability relative to their cost; use the lightest effective workflow appropriate to task risk and complexity.

This is a **hypothesis for future evaluation**, not a new Core rule. It may eventually motivate adaptive workflow depth, but there is no decision to implement that.

## Links to prior archived research

- `incubator/proposals/2026-10-16-superpowers-vs-existing-skills-trinity.md` — comparison of structured workflow additions.
- `incubator/proposals/2026-10-16-grok-agent-permission-approval-hold.md` — independent permission enforcement and Human approval boundaries.

## Governance and next action

**No immediate action required.** Do not modify `core/RULES.md`, `core/WORKFLOW.md`, `core/ACCESS.md`, Trinity sealed boundaries, Skills, or implementation on the strength of this note. Revisit only when Human requests a review or a relevant evaluation opportunity arises.
