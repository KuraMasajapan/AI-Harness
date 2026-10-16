# Superpowers × existing Skills / Trinity — comparative research candidate

**Date:** 2026-10-16  
**Status:** RESEARCH ONLY / NOT IMPLEMENTED  
**Evaluation:** Stage 1 **A+**; Stage 2 **CANDIDATE / REINFORCE** (provisional).  
**Human decision:** Save as a *comparative study of existing Skills and Trinity*, **not** as a standalone installation proposal. No installation, workflow modification, or adoption authorized.

## Source and verification boundary

- User-provided Japanese social post recommended installing “Superpowers” for “Codex 6.1,” citing a brainstorming → planning → subagent implementation → TDD → review workflow and claiming substantial efficiency improvements.
- Official upstream: https://github.com/obra/superpowers
- Related earlier research: https://github.com/mattpocock/skills
- The project is not specific to a single Codex model version; supported hosts and install instructions should be rechecked against upstream docs at the time of any trial.
- Claimed dramatic productivity improvement is **not independently established**. Compatibility, subagent support, skill auto-triggering, token cost, and test quality are environment-dependent.
- This note is a comparative research intake, **not** a completed code audit or benchmark.

## Overlap / possible added value

| Superpowers component | Existing AI-Harness / Codex practice | Incremental value to investigate | Assessment |
|---|---|---|---|
| brainstorming | Human specification approval; core/RULES.md and core/WORKFLOW.md | Explicit pre-code requirement questions, design checkpoints, ambiguity reduction | REINFORCE |
| writing-plans | Existing development plans, checkpoint and handoff discipline | Smaller executable tasks with verifiable done conditions | REINFORCE |
| subagent-driven-development | Trinity parallel evaluation / Comparator and handoff | Independent task implementation and review; **not equivalent to Trinity** | CONDITIONAL |
| test-driven-development | Existing project tests, build gates, reviews | Systematic test-first behavior and prevention of untested changes | CANDIDATE |
| requesting-code-review | Codex review and Trinity validation | Separate **specification-compliance review** from **code-quality review** | PRIORITY GAP TO TEST |

## Research question

**Does Superpowers add reproducible value beyond existing AI-Harness Skills / Trinity / Codex workflows, without redundant prompts, approval fatigue, higher token cost, or unauthorized autonomous changes?**

Compare with `mattpocock/skills` and the existing project-scoped frontend-agent skills. Do not bulk-import either skill set.

## Suggested read-only secondary investigation

1. Read the current upstream README, skill files, Codex integration instructions, license, releases, and open issues. Distinguish actual mechanisms from promotional claims.
2. Inspect existing `core/RULES.md`, `core/WORKFLOW.md`, `core/ACCESS.md`, Trinity research, and installed Skills to identify genuine gaps.
3. Compare `obra/superpowers` with `mattpocock/skills` on pre-code specification gates, task granularity, TDD, review separation, failure handling, and cost.
4. Draft a minimal isolated evaluation: same small task with existing workflow versus selected Superpowers practices; record spec mismatches, regressions, test coverage, Human interventions, wall time, and token/cost usage. Do not run without separate authorization.
5. Classify outcomes as REINFORCE / NEW / DUPLICATE, then CANDIDATE / HOLD / REJECT.

## Risks and constraints

- Automatic skill invocation and subagent capabilities may vary by host/version.
- More process steps can increase cost and approval fatigue; extra agents are not necessarily independent.
- Tool permissions and Human approval remain controlled by AI-Harness, not delegated to a skill.
- Preserve Trinity sealed boundaries and existing Human final authority.
- No edits to existing rules, no Superpowers installation, no Codex execution, and no implementation are authorized by this research note.

## Related saved intake

`incubator/proposals/2026-10-16-github-ai-repositories-top10.md` — includes `mattpocock/skills` as a research candidate.
