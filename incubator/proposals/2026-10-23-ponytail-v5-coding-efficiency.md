---
document_type: research_evaluation
date: 2026-10-23
title: "Ponytail v5 — Minimal-Code Coding Harness Candidate"
source_repository: "https://github.com/DietrichGebert/ponytail"
decision: CANDIDATE
implementation: HOLD
stage_1_rank: A+
stage_2_rank: A+
evidence_status: "OFFICIAL REPOSITORY / README CONFIRMED; AUTHOR BENCHMARKS NOT INDEPENDENTLY REPRODUCED"
tags:
  - ponytail
  - claude-code
  - codex
  - minimalism
  - review
  - audit
  - coding-efficiency
  - token-efficiency
---

# Ponytail v5 — Minimal-Code Coding Harness Candidate

## Status

**Stage 1: A+**  
**Stage 2: A+**  
**Decision: CANDIDATE**  
**Implementation: HOLD**

This record closes a prior research-record gap: Ponytail had already been evaluated in conversation, but no dedicated proposal file existed on the development branch.

## 1. Officially confirmed scope

Official repository:

- https://github.com/DietrichGebert/ponytail
- MIT license
- supports Claude Code and Codex installation paths

Core design principle:

> Write only what the task needs, without cutting validation, error handling, security or accessibility.

Ponytail attempts to make coding agents prefer:

- reuse over rebuilding
- browser / platform primitives over unnecessary dependencies
- less code where less code is sufficient
- review of surrounding affected code, not just the diff
- explicit tests around risky logic

Current commands include:

- `/ponytail`
- `/ponytail-review`
- `/ponytail-audit`

## 2. Author benchmark claims

The project currently reports benchmark improvements such as reductions in:

- code written
- time
- cost
- token use

and claims higher rates of risky logic being covered by tests.

These are **author-controlled benchmarks**.

AI-Harness must treat them as upstream claims until reproduced on our own workloads.

## 3. Relationship to AI-Harness

Ponytail strongly aligns with:

- `incubator/proposals/2026-10-16-harness-minimalism-counterhypothesis.md`
- minimal change philosophy
- reuse before new dependencies
- measured value over process accumulation

Useful mental model:

```text
Ponytail
= coding-time anti-overengineering pressure
```

It is not a replacement for Access, Human approval, project truth, or security policy.

## 4. Why it remains distinct

Ponytail is smaller and more focused than ECC or Superpowers.

Its main question is not:

> How do we build a complete coding harness?

but:

> How do we stop the coding agent from doing more than necessary?

That makes it a useful counterweight to increasingly large agent stacks.

## 5. Risks

- "less code" can become underengineering if misapplied
- project benchmark may not generalize
- aggressive reduction may conflict with readability or maintainability
- another always-active Skill/hook layer may add instruction pressure
- hidden interaction with existing project Skills / Codex instructions

## 6. Best future experiment

Use a real bounded coding task:

```text
A: Codex with current AI-Harness instructions
B: same model + Ponytail
```

Compare:

- LOC changed
- new dependencies
- correctness
- tests
- security / accessibility regressions
- Human corrections
- time
- token/context use

A result of "less code" is not automatically a win.

## Decision

**A+ / CANDIDATE / IMPLEMENTATION HOLD**

Preserve for comparative testing.

Do not install globally or treat upstream benchmark numbers as established AI-Harness facts.
