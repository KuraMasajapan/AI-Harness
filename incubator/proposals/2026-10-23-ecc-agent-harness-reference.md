---
document_type: research_evaluation
date: 2026-10-23
title: "ECC — External Agent Harness Reference Candidate"
source_repository: "https://github.com/affaan-m/ECC"
decision: REFERENCE CANDIDATE
implementation: HOLD
stage_1_rank: A+
stage_2_rank: A
evidence_status: "OFFICIAL REPOSITORY / README CONFIRMED; LOCAL BENEFIT UNVERIFIED"
tags:
  - ecc
  - claude-code
  - codex
  - harness
  - skills
  - agents
  - memory
  - hooks
  - security
---

# ECC — External Agent Harness Reference Candidate

## Status

**Stage 1: A+**  
**Stage 2: A**  
**Decision: REFERENCE CANDIDATE**  
**Implementation: HOLD**

ECC is not best treated as a drop-in addition to AI-Harness.

Its current scope overlaps strongly with AI-Harness itself, so its highest value is as an external reference implementation and comparison target.

## 1. Officially confirmed scope

Official repository:

- https://github.com/affaan-m/ECC
- MIT license
- active project
- supports Claude Code most deeply and also provides Codex integration paths

Current official README describes a coordinated engineering harness built around:

```text
plan
→ test
→ implement
→ review
→ verify
→ remember
→ improve
```

The project currently advertises:

- 71 agents
- 311 skills
- 97 legacy command shims
- hooks
- rules
- memory
- continuous learning / instincts
- AgentShield security scanning
- guided setup for Claude Code and Codex

These counts are upstream-maintainer claims and should be rechecked at any future trial.

## 2. Relationship to AI-Harness

ECC overlaps heavily with:

- RULES / WORKFLOW
- Skills
- checkpoints / persistence
- memory
- review / verification
- coding workflow
- security checks
- agent specialization

Therefore:

```text
AI-Harness + full ECC
≈ two overlapping harness layers
```

That can create duplicated instructions, hooks, memory, review steps and authority ambiguity.

## 3. What is still useful

ECC is valuable as a mature external comparison target for questions such as:

- Which workflow constraints actually earn their complexity?
- Which hooks are useful versus noisy?
- How much memory should be persistent?
- How should Skills be packaged?
- How should Codex / Claude Code integration be installed and rolled back?
- How should a harness distinguish workflow guidance from security enforcement?

This fits the existing Harness minimalism counter-hypothesis:

> Harness complexity should be justified by measured value.

## 4. Relevant comparison targets

Compare selected ECC patterns against:

- `core/RULES.md`
- `core/WORKFLOW.md`
- `core/ACCESS.md`
- Trinity evaluation patterns
- existing Skills
- `incubator/proposals/2026-10-16-harness-minimalism-counterhypothesis.md`
- `incubator/proposals/2026-10-16-superpowers-vs-existing-skills-trinity.md`

Do not bulk-import ECC.

## 5. Risks

- duplicate rules and hooks
- conflicting memory systems
- installation into multiple coding environments
- additional MCP / script / package supply-chain surface
- excessive workflow overhead
- unclear provenance if ECC-generated Skills or memory are mixed into AI-Harness
- future hosted/pro features differ from the MIT OSS repository

## 6. Suggested future experiment

Only test one isolated ECC feature or workflow at a time.

Example:

```text
A: current AI-Harness coding workflow
B: current workflow + one selected ECC practice
```

Measure:

- correctness
- regressions
- elapsed time
- Human intervention
- token/context use
- instruction conflicts
- rollback ease

## Decision

**REFERENCE CANDIDATE / IMPLEMENTATION HOLD**

ECC is important enough to keep watching, but current evidence does not justify installing the full harness on top of AI-Harness.

No Core change, installation, plugin registration, or workflow replacement is authorized by this record.
