---
status: review-candidate
created: 2026-10-12
origin: Grok Codex orphan-process anomaly + Human observation about post-task disk growth
tags:
  - resource-hygiene
  - runtime
  - cleanup
  - observability
  - efficiency
  - reliability
  - candidate
---

# Resource Hygiene / Runtime Cleanup — Review Candidate

## Status

**REVIEW CANDIDATE / 要検討**

This is not yet a Core rule.

No automatic cleanup behavior is adopted by this proposal.

The purpose is to preserve the emerging cross-project concern that AI/agent work can complete functionally while leaving unnecessary runtime or disk resources behind.

---

## Core observation

```text
Task Complete != Runtime Clean
```

A task can produce the requested result and still leave behind:

- child processes
- browser sessions
- open ports
- temporary worktrees
- temporary files
- caches
- build artifacts
- generated intermediate files
- logs
- RAM allocations
- GPU / VRAM allocations
- local servers
- test databases
- background workers
- other disposable runtime state

These leftovers are often difficult for the Human to see directly.

They can therefore accumulate across repeated AI/agent runs even when each individual task appears successful.

---

## Why this matters

The current AI-Harness already considers several forms of waste:

- unnecessary token use
- avoidable API cost
- repeated Human work
- redundant context
- duplicate modules / agents
- unnecessary complexity

Resource Hygiene extends the same principle to runtime and storage waste.

Possible long-term failure pattern:

```text
task succeeds
→ disposable resources remain
→ leftovers accumulate
→ RAM / disk / ports / processes become polluted
→ next task starts in a dirtier environment
→ performance degrades or failures become harder to explain
```

This is both an efficiency problem and a reliability problem.

---

## Triggering observations

### Codex orphan-process signal

A Grok observer report surfaced multiple reports of processes such as git, browser, shell, or subagent-related processes remaining after Codex activity.

Current interpretation:

- this is an anomaly signal
- it is not yet treated as a universal Codex fact
- it is sufficient to justify measuring process lifecycle behavior in real use

### Human observation about Gemini-assisted app debugging

The Human reported a recurring impression that application folders can grow substantially while Gemini-assisted debugging proceeds.

This observation is preserved only as a **hypothesis / motivation**.

Do **not** treat it as evidence that Gemini itself has a confirmed cleanup defect.

Possible causes include:

- repeated builds
- caches
- generated bundles
- logs
- dependency downloads
- temporary files
- backup copies
- test artifacts
- agent/tool-specific behavior rather than the model itself

The useful question is not "Does Gemini leave junk?" but:

> What disposable resources are created by an AI-assisted task, and what remains after the task ends?

---

## Proposed rule direction

Potential future rule:

### Resource Hygiene — Medium Priority

AI and agent workflows should consider the environment left behind by a task, not only the task result.

Temporary resources created or started for task execution should not remain indefinitely when they are no longer required.

However, this should **not** initially mean automatic deletion of anything that appears unnecessary.

The safer initial requirement is:

> Observe and identify residual resources before introducing destructive cleanup.

---

## Priority position

Suggested relative priority:

```text
Safety / Access / Human Approval
        ↓
Correctness / Source / State integrity
        ↓
Resource Hygiene
        ↓
Performance / token / cosmetic optimization
```

Resource Hygiene should never override:

- Human approval
- source-of-truth requirements
- preserved evidence
- checkpoints
- required logs
- reproducibility artifacts
- project files whose status is uncertain

---

## Candidate lifecycle model

A future executor/runtime may track:

### Before Run

- baseline process list
- relevant RAM use
- relevant GPU / VRAM use
- active local ports
- relevant workspace size
- temporary worktrees
- browser / worker sessions

### During Run

Track resources created or owned by the task where practical:

- parent PID
- child PIDs
- ports
- local servers
- browser sessions
- temporary directories
- worktrees
- generated artifacts
- build/cache locations

### After Run

Verify:

- owned child processes terminated
- temporary ports released
- disposable browser / worker sessions closed
- temporary worktrees handled
- temporary artifacts identified
- relevant resource use returned near expected baseline
- unexpected residuals reported

A possible future completion chain:

```text
Result Produced
→ Verification PASS
→ Runtime Resource Check
→ Residuals Reported / Cleaned if explicitly safe
→ COMPLETE
```

---

## Important safety constraint

The first implementation should prefer **detection over deletion**.

Bad pattern:

```text
AI decides "probably unused"
→ deletes files automatically
```

Preferred early pattern:

```text
AI / runtime detects residual
→ classifies it
→ reports it
→ cleanup is automatic only for clearly owned disposable resources
→ ambiguous resources remain untouched
```

This preserves the existing fail-safe direction of the Harness.

---

## Possible resource classes

A future machine-readable classification could distinguish:

### OWNED_DISPOSABLE

Created by the current task and safe to remove/stop.

Examples:
- task-owned temporary server
- task-owned browser session
- temporary working directory with explicit ownership
- temporary worktree created solely for the run

### REQUIRED_OUTPUT

A requested deliverable or required build/test evidence.

Must be preserved.

### REUSABLE_CACHE

Not required for correctness but intentionally reusable.

Removal may save space while increasing future execution cost.

### UNKNOWN

Ownership or necessity cannot be established.

Do not delete automatically.

### PROTECTED

Explicitly preserved by project/Human policy.

Never delete through routine cleanup.

---

## Evaluation idea

Resource Hygiene should eventually be measurable rather than subjective.

Possible metrics:

- orphan process count after task
- task-owned process survival time
- unreleased port count
- RAM delta after task
- GPU / VRAM delta after task
- project/workspace disk delta
- temporary artifact count
- cache growth
- Human cleanup time
- repeated-run accumulation

This creates an additional model/agent evaluation axis:

```text
Task Success
+
Verification Quality
+
Residual Resource Cost
```

Two agents with equal task success may have very different long-term operating quality if one consistently leaves significant residual state.

---

## Failure modes of this proposal

### Over-cleaning

Useful caches, evidence, logs, or Human files are removed.

Mitigation:
- detect first
- explicit ownership
- UNKNOWN fails safe
- Human approval for ambiguous/destructive cleanup

### Cleanup itself becomes complex infrastructure

A large cleanup framework could cost more than the waste it prevents.

Mitigation:
- start with observation
- add deterministic checks only where recurring waste is measured

### False baseline assumptions

Memory, disk, or processes may legitimately remain because another application owns them.

Mitigation:
- track task ownership rather than simply comparing all system resources

### Optimizing insignificant waste

Minor temporary files may not justify additional engineering.

Mitigation:
- prioritize measured recurring resource cost

---

## Adoption trigger

Consider promotion only when one or more of the following are observed:

- repeated orphan processes
- measurable post-task RAM leakage
- repeated unreleased ports or servers
- substantial unexplained project/storage growth
- repeated manual cleanup by the Human
- stale worktrees or browser sessions affecting later tasks
- automation runs whose residual state causes downstream failures

---

## Suggested first experiment

Do not build a cleanup subsystem yet.

Pick one real AI-assisted workload and record:

```text
Before
- project directory size
- relevant process count
- relevant RAM usage
- relevant open ports

Run task

After
- same measurements
- newly created large directories/files
- surviving task-related processes
```

Repeat across several runs.

If a repeatable residual pattern appears, promote only that specific cleanup need into deterministic runtime behavior.

---

## Relationship to AI-Harness

Potential affected layers:

- Runtime
- Validation
- Observability
- Scheduler
- Execution
- Completion semantics

Possible future principle:

> A runtime should not rely solely on the executor's statement that work is finished. Completion may require independent verification that task-owned disposable resources have been released.

This aligns with the broader Harness direction of separating:

- execution
- evidence
- verification
- completion

without yet changing Core.

---

## Additional observation — Artifact handoff readability (2026-10-14)

- External X post contrasted an organized project folder with one containing many mixed intermediate files. **Single anecdote, not a controlled model comparison**: folder count does not prove output quality or that files are unnecessary.
- Human clarified that **AI-Harness operations have not produced a noticeable filing problem**. This is a prompt for reflection, **not an observed Harness defect**.
- If a concrete need arises, consider **human-readable handoff** alongside resource hygiene: distinguish final deliverables, reproducibility/audit evidence, and clearly task-owned disposable intermediates. Preserve required evidence and never infer deletion safety from appearance alone.
- **No new rule, implementation, cleanup automation, priority escalation, or proactive experiment** is justified by this observation alone.

---

## Decision

Preserve as a medium-priority review candidate.

Do not promote to Core yet.

Do not introduce automatic destructive cleanup yet.

First prove that residual resource waste is recurring and measurable in real workloads.
