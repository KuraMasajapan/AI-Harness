---
document_type: research_proposal
created: 2026-11-04
scope: AI-Harness / Codex / project progress visualization
stage_1_rank: A+
stage_2_rank: A
decision: CANDIDATE
implementation: HOLD / NOT INSTALLED
source_status: UPSTREAM README VERIFIED; LOCAL RUNTIME NOT VERIFIED
authority: Human approval required for implementation and publication
---

# You-Are-Here — Reusable Single-HTML Project Progress Dashboard

## Origin and primary source
- X original (read with TinyFish): https://x.com/mylifcc/status/2117542548889596069
- Creator's follow-up: https://x.com/mylifcc/status/2117542549627802100
- GitHub: https://github.com/majiayu000/you-are-here
- Official README checked on 2026-11-04 JST; MIT license according to repository.
- Early-stage repository as observed: 2 GitHub stars, not evidence of robust real-world adoption. No local install or execution was performed.

## The user's specific objective
Maintain **one reusable HTML dashboard** for a coding project. Update that same logical dashboard at each task completion, planned stop, or handoff, including:
1. current stage and short headline;
2. changes since last verified checkpoint;
3. completed, in-progress, blocked, not-started milestones;
4. evidence links to commit/PR/CI/file;
5. open questions and Human decisions (without auto-approving them);
6. next action and responsible party;
7. dated history/replay, with stale-state warning.
The user wants low effort, low token cost, and the ability to check progress across Codex cloud tasks, possibly from a phone.

## Factual evaluation
The upstream README claims:
- Collect local Git state and optionally GitHub issue/PR/CI data using read-only commands; analyze dependencies and milestones through an agent.
- Produce a standalone offline HTML under `.project-map/index.html`; show diffs, historical replay, bottlenecks and Human decisions.
- Support Claude Code, Codex and Grok through plugins/skills/hooks.
- Keep automatic refresh off by default; optional background refresh uses a headless agent and its quota/cost.
- While it describes the repository as read-only, the plugin itself writes dashboard/state/log files to `.project-map/`, and automatic modes install/use hooks and can invoke agent CLIs.
These are documented project claims; cross-platform hooks, lifecycle behavior, cost and robustness have not been reproduced.

## Relationship to existing AI-Harness
- Existing GitHub checkpoints, BBB research records and TRINITY sealed events remain separate sources of evidence and authority.
- This is a **presentation and status-diff layer**, not another source of truth or a replacement for checkpoints.
- Overlap: prior user-requested HTML progress dashboards and handoff/checkpoint files. Incremental value: automatic facts collection, evidence links, same-file refresh, comparison to last snapshot and visual replay.
- Relevant existing principle: `incubator/proposals/2026-10-16-harness-minimalism-counterhypothesis.md` — new complexity must earn its cost.
- Relevant access: `core/ACCESS.md` — no silent Core changes or Human approval bypass.

## Storage decision
Do not rely on Codex Cloud's per-task filesystem as permanent shared storage. Official Codex Cloud guidance says each new task has an isolated workspace and uncommitted changes in another task are not recovered automatically; save important results to source control.
Provisional recommended design:
- A single tracked dashboard file, e.g. `dashboard/index.html`, plus minimal machine-readable history/state if needed.
- Update on explicit task-complete, task-pause or handoff events; do not assume OS shutdown, force termination or crash will fire a completion hook.
- Commit/push only through a separately authorized workflow; dashboard content must not silently mix development and main, nor mutate CURRENT_SPEC, TRINITY sealed records or release history.
- GitHub Pages is optional and requires a separate publication/privacy decision, as issue titles, commit references, internal plans and approval queues may be sensitive.

## Minimal implementation path — proposal only
**Phase 0 — Scope/consent:** Choose one project, private/public viewing, dashboard repo/path, branch strategy, retention and approval requirements. Review the plugin source, hook behavior, external processes and exact writes. Do not install yet.
**Phase 1 — Manual pilot:** Produce one offline HTML using read-only Git + approved checkpoints; label verified facts vs AI inference; save a snapshot/checksum. Exclude secrets and full conversation logs. No background refresh or hooks.
**Phase 2 — Repeatable update:** On deliberate pause/finish, regenerate identical path; compare to previous snapshot, make an evidence-linked change summary, preserve old snapshots in bounded machine-readable data only if needed. Atomic write and schema validation.
**Phase 3 — Codex integration:** If tests pass, introduce an opt-in end-of-task/handoff workflow with explicit failure handling; ensure no unapproved commit/push, no automatic Human decision, no lifecycle confusion. Measure update latency/token cost.
**Phase 4 — Optional multi-project viewing:** Expand to other projects and optionally GitHub Pages after access classification, publication approval and branch isolation. Preserve Human authority.
No permanent daemon, unattended auto-refresh or service is required for the pilot.

## Acceptance criteria
1. One dashboard URL/path is reused across three consecutive finish/pause cycles and shows accurate diffs and the latest snapshot.
2. Every status has a reference or is marked inferred/unverified; GitHub vs local timestamp and freshness are differentiated.
3. Missing CI/GitHub access, offline states and failed refreshes are visibly marked, not silently represented as green.
4. No secret, private context or unapproved project detail leaks into HTML or Pages.
5. No alteration of TRINITY seals, CURRENT_SPEC, production BBB, Human approvals, or other project logic.
6. Update cost is measured against the current manual checkpoint/HTML flow and retained only if worthwhile.
7. Fresh Codex cloud tasks recover dashboard via the repository, not an assumed shared ephemeral disk.

## Security and failure cases
- Plugin may execute hooks and background `codex exec`; test with auto off and least privilege first.
- A task crash cannot be relied upon to emit a stop event. Mark stale until next successful reconciliation.
- HTML must escape dynamic fields and resist XSS from untrusted issue titles/commit messages.
- Avoid a full git history and screenshots in a publicly hosted dashboard.
- Multi-task concurrent updates need version/branch conflict handling; do not let dashboard commits disturb working branches or TRINITY writer lock.
- No automatic acceptance/override of decisions; dashboard is read-only display for Human Authority.

## Status
RESEARCH CANDIDATE ONLY. This file is a recorded proposal, **not approval** to install the plugin, modify hooks, create `dashboard/index.html`, set up Pages, push development work or turn on background agents.
