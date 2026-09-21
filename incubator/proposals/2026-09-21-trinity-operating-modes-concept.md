---
status: proposal
created: 2026-09-21
origin: TRINITY structure review
tags:
  - trinity
  - operating-mode
  - impact-review
  - validation
  - audit
trigger_topics:
  - trinity-mode
  - impact-review
  - validation-mode
  - analysis-mode
  - model-composition
  - run-metadata
---

# TRINITY Operating Modes Concept

## Purpose

Preserve a non-binding concept for operating TRINITY as one common protocol with task-specific modes.

This is **not yet a protocol change**.

The concept should be revisited when TRINITY reaches operational use and different model compositions are being tested.

---

## Core idea

Keep one TRINITY Core and switch only the purpose-specific operating mode.

Conceptual shape:

```text
TRINITY Core
  ├─ independent A / B work
  ├─ explicit Source of Truth
  ├─ no cross-feed before comparison
  ├─ sealed inputs / outputs where required
  ├─ third-party comparison by C
  ├─ provenance / auditability
  └─ Human final authority
          │
          ▼
       MODE
```

Mode changes what the run is trying to evaluate.
Mode should not redefine the Core guarantees.

---

## Initial mode candidates

### ANALYSIS

Purpose:
Compare independent analyses, interpretations, or solution approaches.

Typical question:

> How should this problem be understood or solved?

C should focus on:

- agreement
- disagreement
- unique findings
- evidence
- unresolved uncertainty

### VALIDATION

Purpose:
Check whether an existing answer, artifact, or implementation satisfies defined requirements.

Typical question:

> Does this satisfy the specified requirements and evidence standard?

C should focus on:

- requirement coverage
- accepted-item coverage
- evidence quality
- unsupported claims
- missing or ambiguous items

### IMPACT REVIEW

Purpose:
Evaluate how a local change may affect the broader system.

Typical question:

> If this change is made, what else may be affected?

A and B should both perform independent whole-system impact analysis rather than being assigned artificial "for" and "against" roles.

C should integrate the results into an Impact Map.

Candidate Impact Map fields:

- change target
- direct effects
- indirect effects
- dependencies
- Core impact
- Workflow impact
- Project impact
- Skill impact
- permission-boundary impact
- Validation / Audit impact
- Human UX impact
- A/B agreement
- A-only findings
- B-only findings
- disagreements
- unknown / unverified areas

---

## Mode-selection hint

Possible initial selection rule:

```text
Need independent ideas / interpretations
→ ANALYSIS

Need to judge compliance with known requirements
→ VALIDATION

Need to understand system-wide effects of a proposed change
→ IMPACT REVIEW
```

Prefer the narrowest mode that matches the primary task.

If a task genuinely contains different purposes, consider separate runs rather than a catch-all mode.

---

## Candidate run-boundary rule

A useful hypothesis to test:

> Select the mode before the run starts and do not switch modes inside the same run.

Example:

```text
Run #1: VALIDATION
→ seal result
→ Run #2: IMPACT REVIEW
```

This may preserve clearer audit semantics than changing the evaluation objective mid-run.

Do not formalize this rule until operational testing confirms its value.

---

## Mode is not permission

Keep these concepts separate:

```text
Mode       = what the run evaluates
Permission = what actions the system may execute
```

Choosing IMPACT REVIEW must not implicitly authorize repository writes, destructive actions, production changes, or other operations.

---

## Model-composition test

Before formalizing modes, test whether behavior changes materially under compositions such as:

- same model for A / B / C
- different models for A and B
- stronger comparator model
- strong + lightweight mixed composition
- low-cost / free-tier mixed composition

The mode model should be accepted only if it remains understandable and useful across realistic compositions.

---

## Current decision

Do not modify the active TRINITY protocol yet.

Preserve this as a design hint for the point when:

1. TRINITY becomes operationally usable
2. model compositions are tested
3. real runs reveal whether the three-mode structure is sufficient
4. the value of mode metadata and fixed-per-run behavior can be measured

---

## Guiding principle

TRINITY should remain one auditable mechanism.

Modes should provide different review purposes without turning TRINITY into several unrelated protocols.
