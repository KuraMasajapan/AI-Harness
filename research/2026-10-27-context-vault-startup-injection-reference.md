---
document_type: research_reference
date: 2026-10-27
status: REFERENCE
decision: ABSORB_CONCEPT
stage_1: A
stage_2: B+
novelty: B
ai_harness_relevance: A+
implementation: UNVERIFIED
evidence_status: SINGLE_REPORT / IMPLEMENTATION_DETAILS_UNVERIFIED
tags:
  - context-vault
  - startup-context
  - multi-agent
  - notion
  - shared-context
  - context-injection
  - trust-boundary
---

# Context Vault / Startup Context Injection Reference

Source post:
https://x.com/Haruki_dev/status/2114889562669695318

Quoted original:
https://x.com/Haruki_dev/status/2114665842956980687

## Observed concept

The author reports using a Notion-based **Context Vault** for multiple personal AI agents such as Dots, Muse, and Grok bot.

The stated operating idea is:

> On agent startup, inject shared context from Notion through hooks or equivalent setup so multiple agents begin from the same perspective.

The visible Context Vault UI includes:
- Memories
- Documents
- Agents
- Sessions
- About / Context Vault navigation

No implementation code, hook configuration, data schema, permission model, or synchronization mechanism was visible in the reviewed post images.

## Why it is relevant

The useful idea is not "Notion" itself.

The more general pattern is:

```text
Shared durable context
        ↓
startup injection
        ↓
multiple agents
        ↓
common project / user perspective
```

This is strongly related to AI-Harness goals around:
- durable project context
- cross-agent continuity
- reusable operating context
- Source of Truth
- consistent agent behavior across local and remote environments

## Evaluation

### Stage 1 — A

The concept is practical and directly relevant.

### Stage 2 — B+

The score is intentionally below A because the public evidence does not show:
- exact hook implementation
- read/write authority
- synchronization semantics
- provenance controls
- conflict resolution
- context freshness strategy
- failure handling
- security boundaries
- whether all agents receive identical or filtered context

Therefore the implementation quality cannot yet be verified.

### Supporting sub-scores

- Concept / direction: **A–A+**
- AI-Harness relevance: **A+**
- Novelty: **B**
- Implementation verification: **B**
- Overall Stage 2: **B+**

## Main risk

A shared Context Vault can become a shared failure domain.

```text
shared context poisoned or stale
        ↓
all connected agents consume it
        ↓
blast radius expands across agents
```

This is especially important after the Instruction Trust Boundary research.

A shared context system should therefore distinguish between:
- trusted context
- untrusted / external context
- agent-specific context
- project-specific context
- task-specific context

## Preferred AI-Harness interpretation

Rather than injecting the same full context into every agent, a safer structure is:

```text
Trusted Source of Truth
        ↓
Context Compile
        ↓
Core Context
Project Context
Agent Context
Task Context
        ↓
Agent-specific injection
```

This preserves a shared perspective without forcing every agent to receive identical authority or unnecessary context.

## Candidate principle

> **Shared context should be compiled, scoped, and trust-aware before injection.**

Useful properties:
- startup continuity
- common perspective
- lower context reconstruction cost
- cross-agent consistency

Required protections:
- provenance checks
- read/write separation
- freshness controls
- agent-specific filtering
- independent authority boundaries
- protection against one shared vault becoming a single contamination point

## Decision

**REFERENCE / ABSORB CONCEPT**

Do not adopt Notion as a new Source of Truth from this post alone.

Do not add automatic startup injection to Core without a separate design and security review.

The value of this record is as an external implementation signal that multi-agent systems are converging on shared durable context, while also reinforcing the need for context trust and scoping.
