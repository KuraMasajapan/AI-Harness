---
status: proposal
created: 2026-09-21
origin: AI-Harness structure synthesis / external-information ingestion discussion
tags:
  - harness
  - reference-architecture
  - distributed-memory
  - trinity
  - shield
  - context
  - proposal-incubator
trigger_topics:
  - harness-architecture
  - system-map
  - external-information
  - knowledge-ingestion
  - distributed-custody
  - trinity
  - shield
  - context-management
---

# AI-Harness Reference Architecture — Distributed Knowledge and Control

## Purpose

Preserve a provisional **whole-system map** for AI-Harness without making any single AI conversation, model, or assistant the authoritative holder of the design.

This proposal is intentionally a reference architecture, not a final Core specification.

Its purpose is to make future information easy to attach to the correct layer, compare against existing concepts, and review later with TRINITY before promotion.

---

## Primary design principle

> No single AI should have to remember the whole system.

Durable system knowledge belongs in external artifacts.

Agent working memory is temporary.

Preferred model:

```text
AI working memory = temporary
HARNESS artifacts / Source of Truth = persistent
```

Conversation memory may help continuity, but it must not become the only place where architecture, decisions, constraints, or unresolved proposals exist.

---

## Six-layer reference architecture

```text
Human
  │
  ▼
1. HARNESS CORE
  │
  ├─ authority / permission
  ├─ Source of Truth precedence
  ├─ CURRENT / SUPERSEDED distinction
  ├─ sealed boundaries
  ├─ audit / provenance
  └─ Human final authority
  │
  ▼
2. TASK / MODE CONTROL
  │
  ├─ task classification
  ├─ scope
  ├─ completion condition
  ├─ risk / cost / impact framing
  └─ TRINITY mode selection
  │
  ▼
3. CONTEXT PLANE
  │
  ├─ progressive disclosure
  ├─ triggered guidance
  ├─ Skills
  ├─ Project Source of Truth
  ├─ memory / knowledge retrieval
  └─ replaceable Context Filter
  │
  ▼
4. S.H.I.E.L.D. CONTROL PLANE
  │
  ├─ model routing
  ├─ role selection
  ├─ TRINITY orchestration
  ├─ MCP / Plugin routing
  ├─ fallback
  └─ cost / quota awareness
  │
  ├───────────────┬───────────────┐
  ▼               ▼               ▼
ChatGPT       external AI      local AI
  │               │               │
  └───────────────┴───────────────┘
                  │
                  ▼
5. EXECUTION PLANE
  │
  ├─ GitHub
  ├─ shell / filesystem
  ├─ build / test
  ├─ browser / computer use
  └─ external services
  │
  ▼
6. EVIDENCE / LEARNING LOOP
  │
  ├─ validation
  ├─ audit log
  ├─ receipts
  ├─ cost / usage
  ├─ failures / retries
  ├─ Proposal / Lesson
  └─ regression evidence
```

The layers are conceptual boundaries.
They should help organize responsibility, not force premature implementation.

---

## 1. HARNESS CORE

Core should hold durable system invariants rather than task-specific operating detail.

Candidate invariant classes:

- authority and permission boundaries
- Source of Truth rules
- CURRENT vs SUPERSEDED handling
- sealed artifact integrity
- destructive / irreversible action gates
- provenance and audit requirements
- Human final authority

A future structure audit should test which current rules truly belong here.

Do not move a rule out of Core merely because a stronger model can often infer the right behavior.

---

## 2. TASK / MODE CONTROL

Before choosing a model, define the work.

Candidate task definition:

```text
goal
scope
completion condition
risk
permission
required evidence
mode
```

This layer answers:

- What is the task?
- What counts as done?
- What may be changed?
- What requires Human approval?
- What kind of review is needed?

### TRINITY mode concept

Initial mode candidates:

- ANALYSIS
- VALIDATION
- IMPACT REVIEW

Mode changes what the run evaluates.

Mode is not permission.

The mode model remains provisional until operational TRINITY runs validate it.

---

## 3. CONTEXT PLANE

The system should not load all available knowledge into every task.

Preferred pattern:

```text
task
→ lightweight routing metadata
→ relevant guidance only
→ deeper material only when required
```

This is progressive disclosure.

Candidate context classes:

- invariant guidance
- triggered procedural guidance
- Skills
- Project Source of Truth
- active task evidence
- durable memory
- external reference material

### Context Filter boundary

Keep a replaceable interface:

```text
Context Filter
  ├─ none
  ├─ deterministic rules
  ├─ local model
  └─ external service such as Jev
```

A Context Filter must not become the authority over protected Core / Source-of-Truth material.

---

## 4. S.H.I.E.L.D. CONTROL PLANE

Working metaphor:

- individual models / executors = Avengers
- coordinating control plane = S.H.I.E.L.D.

S.H.I.E.L.D. owns coordination rather than model intelligence itself.

Candidate responsibilities:

- task-to-model routing
- role composition
- low-cost / free-tier selection
- TRINITY invocation
- MCP / Plugin access
- fallback when a provider is unavailable
- quota awareness
- model-specific operating profiles
- escalation to stronger or paid capability only when justified

The control plane should remain provider-optional.

The durable system value should not depend on one model vendor.

---

## 5. EXECUTION PLANE

Reasoning and execution are separate capabilities.

An AI model may propose or decide work without having the environment needed to execute it.

Execution may include:

- repository reads / writes
- shell
- build
- test
- browser operations
- filesystem changes
- external service actions
- local-machine tasks

Permissions for execution remain governed by Core and task boundaries.

Do not treat access to an API model or MCP server as equivalent to a full Codex-like execution environment.

---

## 6. EVIDENCE / LEARNING LOOP

The system should learn from operation without silently promoting every observation into Core.

Preferred path:

```text
operation
→ evidence
→ observation
→ Proposal / Lesson
→ review
→ Human decision
→ Core / Workflow if justified
→ regression test
```

Useful evidence may include:

- run outputs
- comparison results
- validation receipts
- model / role composition
- cost
- latency
- retries
- failures
- Human intervention
- affected components

TRINITY may later become a primary review mechanism for changes that can affect multiple layers.

---

## External information ingestion

The user expects to continue bringing in substantial outside information.

The system should therefore support continuous intake without forcing one assistant to retain or reconcile everything mentally.

Preferred flow:

```text
external article / post / paper / project
→ source capture or concise abstraction
→ identify useful mechanism / claim
→ place in Incubator or research note
→ link to related proposals
→ defer promotion
→ later synthesis / TRINITY review
→ Human decision
```

The objective is not to archive the internet.

The objective is to preserve useful signals in durable, discoverable form.

---

## Information custody model

### Durable custody

Use external artifacts for:

- accepted decisions
- architecture concepts
- unresolved proposals
- Source of Truth
- operating procedures
- evidence
- evaluation results

Preferred durable stores in the current architecture:

- GitHub for history and machine-readable durability
- Obsidian for Human-facing exploration and relationship discovery

### Temporary custody

Use AI conversation context for:

- current reasoning
- temporary synthesis
- task-local working state
- draft interpretation

Temporary context may disappear without damaging the system.

---

## Proposal relationship model

This reference architecture does not replace existing proposals.

It acts as a map that relates them.

Examples:

### Core / task / review

- TRINITY Operating Modes Concept
- Post-TRINITY Harness Structure Audit

### Context

- Jev Context Filter Adoption Model
- Temporal Context Layer
- Obsidian Compatibility Graph
- Beyond the Second Brain

### Control plane / models

- S.H.I.E.L.D. — Low-Cost Multi-AI Control Plane
- Dynamic Agent Team Composition
- Role Pattern Library
- Constraint-Driven AI Systems Research
- Accessible Zero-Cost Agent Infrastructure
- ASTRA Work Compression

### Learning / intake

- Conversation-to-Incubator Capture
- HARNESS Compounding Capability Flywheel
- HARNESS Content Flywheel
- Proposal Incubator

The reference architecture should help future proposals answer:

> Which layer does this idea belong to, and what other layers might it affect?

---

## Architectural review principle

Do not evaluate a local change only in the file where it is proposed.

When a change becomes significant, review possible effects across:

- Core
- Task / Mode
- Context
- Control Plane
- Model behavior
- Execution
- Evidence / Audit
- Human UX

This is a major candidate use for TRINITY IMPACT REVIEW.

---

## Model-specific guidance

Separate system invariants from model-specific operating advice.

Candidate pattern:

```text
HARNESS invariant
  +
model profile
  +
task-specific guidance
```

A model upgrade should not require rewriting the whole Harness.

A provider-specific optimization should remain replaceable.

---

## Cost principle

Use the cheapest adequate capability, not the cheapest model blindly.

Candidate escalation:

```text
deterministic
→ local / free-tier
→ primary paid subscription
→ low-cost external API
→ strongest / scarce executor
→ TRINITY when independent review is worth the cost
```

Measure completion quality, retries, Human effort, latency, and total task cost rather than token price alone.

---

## Current status

This document is a provisional architecture map.

It does **not**:

- modify Core
- redefine TRINITY protocol
- adopt S.H.I.E.L.D. as a mandatory product name
- enable Jev
- authorize new external services
- require Obsidian as runtime infrastructure
- lock a specific model roster

It exists so future information can be stored and related without depending on one assistant's memory.

---

## Guiding principle

> Keep intelligence replaceable, knowledge durable, authority explicit, context selective, execution bounded, and evidence reusable.

The Harness should become easier to extend as more information arrives, not more dependent on the current AI that happened to discuss it.
