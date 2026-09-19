# Latent Risk Scan — V0.1

- Date: 2026-09-20
- Branch: development
- Status: Experiment
- Scope: Minimal pre-failure detection experiment

## Purpose

Test whether AI-Harness can notice a missing safety or verification layer **before** a failure occurs, without requiring the human to point out the missing layer first.

The target is not exhaustive risk analysis.

The target is a lightweight trigger that asks whether an important change contains a hidden dependency, an undetected failure mode, or a missing enforcement layer.

## V0.1 Trigger

Run the scan only when a task materially involves one or more of:

- permission expansion
- automation expansion
- external write/action capability
- Core / Workflow changes
- Source of Truth changes
- high-impact or difficult-to-reverse actions

Do not run it for ordinary conversation or low-risk edits.

## Minimal Scan

Before execution, ask:

1. What assumption is this change relying on?
2. If the AI is wrong about that assumption, what can break?
3. Is any required detection, verification, or enforcement layer missing?

The third question is intentionally different from normal risk analysis.

It looks for a **missing layer**, not only a known component that may fail.

## Design Principle

A rule that exists only in AI instructions is not equivalent to an external enforcement mechanism.

Where practical, prefer:

```text
AI judgment
    +
observable verification
    +
mechanical boundary for known prohibited actions
```

over relying only on:

```text
AI remembers the rule
```

## V0.1 Limits

This experiment does not:

- change Core rules
- grant new autonomous permissions
- implement a policy engine
- add Giskard, PyRIT, promptfoo, OPA, or other external frameworks
- claim complete threat modeling
- block normal work by default

External projects may inform later design, but V0.1 intentionally keeps only the smallest useful pattern.

## Evaluation

The first evaluation uses two test types:

```text
High-risk case
→ scan should trigger
→ scan should identify the missing enforcement layer

Low-risk case
→ scan should not overreact
→ normal work should continue
```

PASS requires both behaviors.

See `TEST_CASES.md`.
