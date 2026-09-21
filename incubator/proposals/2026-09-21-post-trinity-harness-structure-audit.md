---
status: proposal
created: 2026-09-21
origin: GPT-6 Astra / Harness structure review
tags:
  - harness
  - instruction-architecture
  - progressive-disclosure
  - model-specific
  - trinity
  - audit
trigger_topics:
  - astra
  - agents-md
  - skills
  - rule-audit
  - progressive-disclosure
  - instruction-bloat
  - model-profile
---

# Post-TRINITY Harness Structure Audit

## Purpose

Preserve the proposed order for reviewing AI-Harness instructions and structure after TRINITY reaches an operationally useful state.

The goal is not to assume that the current Harness is over-constrained.

The current rule set was built during active development to make safety boundaries, auditability, Source of Truth handling, and workflow behavior explicit.

The question for later review is:

> Which instructions are true system invariants, which should load only when relevant, and which are model-specific operating guidance?

---

## Priority order

Do not perform a large structural cleanup before TRINITY is operational.

Preferred sequence:

```text
Current Harness
→ bring TRINITY into operational range
→ establish a usable TRINITY baseline
→ audit Harness with TRINITY
→ review proposed changes
→ apply only justified changes
→ re-validate with TRINITY
```

Reason:

If TRINITY and the underlying Harness are both changing heavily at the same time, it becomes harder to identify which change caused an improvement or regression.

TRINITY should first become a quality-assurance instrument for later Harness changes.

---

## Candidate instruction layers

A future audit should test whether instructions are clearer when separated into three layers.

### 1. Invariant

Always-applicable rules that define durable system boundaries.

Examples may include:

- authority / permission boundaries
- Source of Truth precedence
- CURRENT vs SUPERSEDED handling
- sealed artifact integrity
- destructive-action approval
- audit / provenance requirements

These should not be weakened merely because a newer model is more capable.

### 2. Triggered

Guidance that should load only when the task makes it relevant.

Examples may include:

- project-specific knowledge
- TRINITY procedures
- Proposal Incubator procedures
- GitHub workflows
- Obsidian workflows
- image-generation guidance
- specialized validation procedures

Preferred pattern:

```text
small routing description
→ task trigger matches
→ load the relevant detailed guidance
```

This is progressive disclosure rather than deletion of useful documentation.

### 3. Model-specific

Operating guidance that exists because a particular model has characteristic strengths or failure modes.

Examples to evaluate:

- how much initiative to allow
- when broad testing is excessive
- how aggressively to discover related files
- when to continue through fix / retest loops
- model-specific tool-use or instruction-following adjustments

Model-specific guidance should not automatically become a universal Core rule.

---

## Audit classifications

A later TRINITY audit may classify existing instructions as:

- KEEP
- SIMPLIFY
- CONDITIONAL
- MOVE TO SKILL / LOCAL GUIDANCE
- MODEL-SPECIFIC
- REMOVE CANDIDATE
- REVIEW / INSUFFICIENT EVIDENCE

The objective is not minimum line count.

The objective is:

- preserve safety
- preserve quality
- reduce irrelevant context
- reduce contradictory or redundant guidance
- increase appropriate model autonomy
- retain explicit Human authority where consequences are material

---

## Progressive disclosure hypothesis

A strong model should not necessarily receive every potentially relevant document at the start of every task.

Candidate pattern:

```text
Task
→ route to relevant guidance
→ load only required files
→ expand context only when the work requires it
```

This may improve efficiency and reduce interference from unrelated instructions.

Important exception:

Some sealed evaluation tasks intentionally define a complete fixed input package.
In those cases, reading the predetermined package is part of the task contract and should not be replaced by opportunistic retrieval.

---

## Completion and autonomy review

Later review should inspect broad instructions such as:

- always read every related file
- always run the full test suite
- always stop when something is unclear
- always request confirmation

These may be appropriate in some scopes and excessive in others.

The audit should convert blanket behavior into bounded decision rules only where evidence supports doing so.

Safety-critical approval boundaries remain separate from convenience-oriented confirmation reduction.

---

## Use TRINITY for the review

A future structure audit is a strong candidate for TRINITY because local changes can have system-wide effects.

Potential flow:

```text
proposed instruction change
→ independent A / B review
→ C comparison
→ impact analysis
→ Human decision
→ controlled change
→ regression validation
```

This is especially useful when removing or narrowing old instructions that may have been added to prevent earlier failures.

---

## Current decision

Do not begin broad instruction cleanup now.

First make TRINITY operational.

Then use TRINITY to evaluate whether the current Harness structure should be simplified, made conditional, or separated by model.

---

## Guiding principle

Do not optimize the Harness for a model by adding more instructions automatically.

Do not optimize it by deleting instructions automatically either.

Preserve true invariants, load detailed guidance when it is relevant, and isolate model-specific behavior from system-wide policy.
