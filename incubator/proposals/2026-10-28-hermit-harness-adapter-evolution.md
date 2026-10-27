---
status: proposal
created: 2026-10-28
decision: CANDIDATE HIGH / EXPERIMENT
priority: HIGH
stage_1: A++
stage_2: A
implementation: HOLD / NOT IMPLEMENTED
evidence_status: CONFIRMED_UPSTREAM / INDEPENDENT_REPRODUCTION_UNVERIFIED
tags:
  - hermit
  - harness-adapter
  - continual-learning
  - self-evolution
  - skills
  - memory
  - evaluation
  - hermes
---

# Hermit — Harness Adapter Evolution Candidate

Primary source:
https://github.com/Infini-AI-Lab/hermit

Visual companion:
ChatGPT Library path:
`/AI-HARNESS/Research/Images/hermit-ai-harness-architecture-2026-10-28.png`

## Summary

Hermit is an Apache-2.0 framework from Infini-AI-Lab for continual learning and harness evolution through an external **Harness Adapter**.

The existing model and original harness remain unchanged.

The trainable behavior lives in an external adapter that can contain:
- instructions / prompts
- skills
- memory
- tools
- executable code
- sub-agents
- multi-agent coordination logic

The framework unifies:
- task execution
- feedback collection
- Evolver updates
- specification checks
- version history
- evaluation
- deployment

Supported evolution methods in v0.1.0 include:
- GEPA
- SkillOpt
- MetaWorld Model
- Harness²
- Continual Harness

## AI-Harness translation

Recommended Japanese interpretation:

- Harness Adapter → 外付け適応レイヤー / 学習可能な装備
- Acting Agent → 実行担当Agent
- Evolver → 改善ロジック / 改善器
- Judge → 評価器
- Trainer → 学習管理器
- learnable → 変更許可領域
- fixed → 変更禁止領域
- specification check → 仕様適合チェック

## Core architecture

```text
Existing Agent
Model + Original Harness
      │
      │ frozen
      ▼
Harness Adapter
      │
      ├─ Prompt
      ├─ Skills
      ├─ Memory
      ├─ Tools
      ├─ Sub-agents
      └─ Coordination
      │
      ▼
Task execution
      ↓
Trajectory / result
      ↓
Judge
      ↓
Evolver
      ↓
Candidate adapter
      ↓
Specification check
      ↓
Git/versioned adapter
      ↓
Evaluation
```

## Strong design point: learnable vs fixed

Hermit's adapter manifest explicitly separates what a learner may modify from what must remain fixed.

Example conceptual mapping for AI-Harness:

```text
FIXED / Human-controlled
- Core
- RULES
- ACCESS
- Human Authority
- security boundaries
- checker / enforcement

LEARNABLE / Experimental
- prompts
- selected skills
- selected memory
- agent workflow
- task-specific coordination
```

This offers a practical way to separate:

> AI can improve itself

from:

> AI can rewrite its governing rules.

## Specification checks

Hermit checks candidate adapters before accepting them.

The manifest can constrain:
- editable paths
- fixed paths
- file counts
- file sizes
- text/frontmatter rules
- custom checker logic

A custom checker can reject a candidate after the built-in structural checks.

Important limitation from the upstream security policy:

> Passing the specification check establishes structural validity, not that the adapter is safe or improves performance.

Therefore a Hermit-generated adapter must remain an **UNTRUSTED CANDIDATE** until independent security/evaluation/Human review passes.

## Versioning and traceability

Hermit stores adapter evolution as versioned history and run records.

Typical artifacts include:
- current adapter checkout
- per-step scores
- changes
- costs
- commit IDs
- learning material
- state snapshots
- reports
- eval summaries
- Git history of adapter versions

This maps well to AI-Harness:
- Promotion Evidence
- Regression Test
- LESSON traceability
- rollback / comparison

## OfficeQA evidence

Hermit's documentation reports OfficeQA results under a shared GLM 5.3 Flash + Codex 0.162 setting:

| Method | Accuracy |
|---|---:|
| no adapter | 0.541 |
| initial skill | 0.576 |
| GEPA | 0.580 |
| SkillOpt | 0.600 |
| Continual Harness | 0.634 |
| Harness² | 0.651 |

Important qualification:
- GEPA / SkillOpt use train-validation-test style evaluation.
- Continual Harness / Harness² are streaming protocols over the 172 questions.
- These are not directly identical evaluation protocols.
- Some confidence intervals cross zero.
- Independent reproduction has not been verified by this AI-Harness review.

Do not conclude that Harness² is universally superior from this table.

## Security relevance

Hermit adapters may contain executable code, tools and coordination logic.

Apply AI-Harness Instruction Trust Boundary:

```text
Hermit-generated Adapter
        ↓
UNTRUSTED CANDIDATE
        ↓
structural check
        ↓
security check
        ↓
evaluation
        ↓
Human approval
        ↓
TRUSTED / deployable
```

The upstream project also notes that isolation depends on host/sandbox configuration, and Linux program isolation uses bubblewrap.

## Relationship to OPST

Hermit and OPST operate at different layers.

```text
OPST
  → changes model parameters
  → model capability evolves

Hermit
  → keeps model frozen
  → evolves external harness behavior
```

For current AI-Harness work, Hermit is closer to the existing architecture.

OPST remains a future local-model post-training candidate.

## Relationship to Hermes Local Agent

Hermit can convert compatible adapters for:
- Codex
- Claude Code
- Pi
- Hermes

This makes it relevant to the future Hermes Local Agent project.

Potential future architecture:

```text
AI-HARNESS Core
     ↓
Hermit Experimental Adapter Layer
     ↓
Codex / Claude Code / Hermes Local
     ↓
task experience
     ↓
adapter improvement
     ↓
LESSON candidate
     ↓
Human Review
     ↓
selective promotion
```

## AI-Harness interpretation

Hermit should not replace AI-HARNESS.

The promising role is:

> **Hermit = automated improvement laboratory around a Human-controlled Core.**

Preferred future pattern:

```text
AI-HARNESS Core
= constitution / frozen / Human-controlled

        ↓

Hermit
= experimental trainable layer

        ↓

LESSON
= candidate record

        ↓

Human Review

        ↓

only verified improvements promoted
```

This could help combine:

- "the Harness improves with use"
- "the Harness does not autonomously rewrite its Core"

## Evaluation

**Stage 1: A++**

**Stage 2: A**

**Novelty: A+**

**AI-Harness relevance: A++**

**Design quality: A++**

**Current maturity: B+**

**Security fit: A- with independent gates**

**Evidence: CONFIRMED upstream implementation + benchmark recipes**

**Independent reproduction: UNVERIFIED**

## Decision

**CANDIDATE HIGH / EXPERIMENT**

Do not install Hermit into AI-Harness production workflow from this note alone.

Future experiment should be isolated and test:
1. learnable/fixed boundary enforcement
2. adapter versioning and rollback
3. custom checker behavior
4. security of tool/executable exports
5. compatibility with Instruction Trust Boundary
6. LESSON promotion integration
7. Codex/Hermes portability
8. drift and regression under continual learning
9. cost/benefit versus existing manual LESSON process

No Core change, automatic self-modification, or Hermes implementation is authorized by this proposal.
