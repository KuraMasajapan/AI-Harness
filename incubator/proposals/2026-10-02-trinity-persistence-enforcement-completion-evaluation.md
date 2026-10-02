---
status: proposal
created: 2026-10-02
origin: Human request / Claude Code harness review
tags:
  - trinity
  - harness
  - persistence
  - enforcement
  - completion
  - validation
trigger_topics:
  - persistence-class
  - context-loss
  - rule-access
  - definition-of-done
  - trinity-validation
  - harness-audit
---

# TRINITY Companion Evaluation — Persistence, Enforcement, Completion

## Purpose

Preserve a future evaluation plan for testing three candidate Harness principles alongside TRINITY without changing the active TRINITY protocol.

The three candidates are:

1. **Persistence Class** — classify information by how strongly it must survive context loss, summarization, restart, or selective loading.
2. **Rule / Access separation** — distinguish model guidance from mechanically enforced permission boundaries.
3. **Definition of Done** — define observable completion evidence instead of accepting the model's completion claim by itself.

This document is a **proposal and companion evaluation plan**, not a Core rule, protocol amendment, or permission change.

---

## Why pair this with TRINITY

These candidates can affect the whole Harness and are easy to overvalue from a single successful example.

TRINITY should be used to test them as controlled changes rather than adopting the ideas directly.

Preferred sequence:

```text
current Harness baseline
→ sealed TRINITY evaluation
→ candidate change applied in an isolated test scope
→ sealed TRINITY evaluation
→ compare evidence, failures, overhead and side effects
→ optional IMPACT REVIEW
→ Human adoption / rejection decision
```

Do not rewrite prior sealed runs.

Do not switch the evaluation objective inside a sealed run merely to accommodate this experiment.

---

## Candidate A — Persistence Class

### Hypothesis

Important information should be placed according to how damaging its loss would be, rather than only by document type.

### Provisional classes for testing

These labels are intentionally non-binding.

```text
P0 — must not depend on model memory alone
     Examples: authority boundaries, destructive-action limits,
     sealed-artifact integrity, Source of Truth precedence.

P1 — must remain available throughout the active workflow
     Examples: current task constraints, workflow invariants,
     current-state / CURRENT vs SUPERSEDED handling.

P2 — load when the task or project makes it relevant
     Examples: project-specific procedures, Skills,
     specialized validation guidance.

P3 — archival / historical context
     Examples: lessons, prior observations, old checkpoints,
     superseded rationale retained for provenance.
```

The experiment must test whether these classes are useful before they are added to Core terminology.

### Questions

- Does the classification reduce loss of critical instructions after context compression, restart, or selective loading?
- Does it reduce unnecessary always-loaded context?
- Are P0/P1/P2/P3 boundaries understandable to different models?
- Does the classification duplicate existing Invariant / Triggered / Model-specific layers?
- Can the same effect be achieved with simpler existing structures?

---

## Candidate B — Rule / Access separation

### Hypothesis

A rule that only instructs the model is weaker than a known prohibited action that is mechanically blocked.

Candidate distinction:

```text
Rule   = what the model should understand and follow
Access = what the execution environment actually permits
```

This should be tested, not assumed, because mechanical restrictions can also introduce operational friction or block legitimate work.

### Questions

- Does the model correctly explain the rule even when no mechanical boundary exists?
- When a prohibited action is attempted, is it actually blocked?
- Can the system recover safely after a block?
- Does the boundary block valid adjacent actions?
- Is the boundary observable in audit evidence?

This candidate overlaps with the existing Latent Risk Scan principle:

```text
AI judgment
+ observable verification
+ mechanical boundary for known prohibited actions
```

Avoid creating a duplicate safety subsystem if the existing mechanism already covers the requirement.

---

## Candidate C — Definition of Done

### Hypothesis

Completion should be accepted from observable evidence, not from a model statement such as "done" or "completed".

Candidate pattern:

```text
Task
→ explicit completion conditions
→ execution
→ observable evidence
→ independent validation
→ completion
```

### Questions

- Does explicit DoD reduce premature completion claims?
- Are the completion conditions objectively observable?
- Does the model expose the evidence needed by the validator?
- Can the validator distinguish functional completion from incomplete provenance?
- Does DoD become excessively rigid for exploratory tasks?

---

## TRINITY pairing method

### Phase 0 — Freeze the experiment

Before execution, record:

- exact task package
- repository commit / tree or equivalent snapshot
- active Harness inputs
- candidate change under test
- expected observations
- Human-approved scope

Use the existing TRINITY operations receipt where applicable.

### Phase 1 — Baseline run

Run the task using the current Harness without the candidate change.

Record normal TRINITY outputs plus companion observations.

### Phase 2 — Candidate run

Repeat the same task with only the targeted candidate change.

Avoid bundling Persistence Class, Rule / Access separation and Definition of Done into one first experiment.

One-variable changes are preferred when practical.

### Phase 3 — Compare

Compare at least:

| Dimension | Baseline | Candidate |
|---|---|---|
| Critical instruction retained | | |
| Critical instruction omitted | | |
| Prohibited action attempted | | |
| Prohibited action blocked | | |
| Premature completion claim | | |
| Completion evidence present | | |
| Unsupported / unverified claim | | |
| Irrelevant context loaded | | |
| Human intervention required | | |
| Operational friction / false block | | |
| Provenance complete | | |

Do not collapse these into one score unless a later experiment establishes a justified weighting method.

### Phase 4 — Impact review

If a candidate appears useful, run a separate TRINITY IMPACT REVIEW before Core adoption.

Inspect impact on:

- HARNESS.md
- core/RULES.md
- core/WORKFLOW.md
- core/ACCESS.md
- project-local guidance
- Proposal Incubator
- TRINITY operations
- Latent Risk Scan
- Human approval boundaries
- model-specific guidance
- context / token overhead

---

## Suggested first experiment

Start with **Persistence Class only** because it directly tests the Harness memory / context-loss problem without granting new execution permissions.

Candidate test shape:

```text
same task + same source package
        │
        ├─ Baseline: current placement rules
        │
        └─ Candidate: selected information labeled and placed by provisional P-class

Then compare:
- what survives restart / context reduction
- what must be reloaded
- what is omitted
- what irrelevant context remains loaded
- whether task output quality changes
```

After that, test Rule / Access separation and Definition of Done independently.

---

## Acceptance rule

Do not adopt a candidate because it sounds architecturally clean.

A candidate should advance only if evidence shows that it:

- prevents or exposes a real failure mode,
- does not weaken Human authority,
- does not damage sealed-run auditability,
- does not create unacceptable false blocks or overhead,
- and is meaningfully better than the current simpler mechanism.

Possible outcomes:

- ADOPT
- ADOPT WITH NARROWER SCOPE
- KEEP EXPERIMENTAL
- MERGE INTO EXISTING MECHANISM
- REJECT
- INSUFFICIENT EVIDENCE

These are proposal-level review outcomes, not automatic protocol states.

---

## Relationship to existing proposals

This experiment complements, rather than replaces:

- **Post-TRINITY Harness Structure Audit** — especially Invariant / Triggered / Model-specific placement.
- **TRINITY Operating Modes Concept** — use VALIDATION for requirement satisfaction and separate IMPACT REVIEW for system-wide effects.
- **Latent Risk Scan** — especially the distinction between model instruction and missing enforcement layers.

A key test is whether Persistence Class adds a genuinely useful axis or merely renames the existing Invariant / Triggered distinction.

---

## Current decision

- Preserve this as a future TRINITY companion evaluation.
- Do not modify active TRINITY protocol.
- Do not add P0–P3 to Core vocabulary yet.
- Do not add new permission restrictions yet.
- Do not change current completion gates yet.
- When the next suitable TRINITY evaluation is run, use this document to prepare an isolated baseline-versus-candidate test.

---

## Guiding principle

Use TRINITY to test Harness ideas before turning them into Harness rules.

Architecture should be promoted by evidence, not by elegance.
