---
document_type: research_evaluation
date: 2026-10-23
title: "Orrery — Persistent Agent Identity and Memory Candidate"
source_repository: "https://github.com/Tech0001/orrery"
discovery_source: "Grok Observer"
decision: CANDIDATE
implementation: HOLD
stage_1_rank: A+
stage_2_rank: A+
evidence_status: "OFFICIAL REPOSITORY VERIFIED; LONG-TERM LOCAL PERFORMANCE UNTESTED"
tags:
  - memory
  - persistent-agent
  - identity
  - codex
  - claude-code
  - local-first
  - hierarchical-summary
  - multi-tool
  - sync
---

# Orrery — Persistent Agent Identity and Memory Candidate

## Status

**Stage 1: A+**  
**Stage 2: A+**  
**Decision: CANDIDATE**  
**Implementation: HOLD**

Discovered by the Grok Observer on 2026-10-23.

The Observer initially had only an X report. Independent follow-up resolved the author's link to the public repository:

- https://github.com/Tech0001/orrery

## 1. What it is

Orrery gives a named coding agent a persistent memory that survives:

- sessions,
- model changes,
- coding tools,
- projects,
- machines.

The important conceptual shift is:

```text
session owns memory
```

becoming:

```text
agent owns memory
```

A named agent keeps one continuing history rather than being recreated from scratch in each tool.

## 2. Officially confirmed capabilities

The official repository documents support for:

- Claude Code,
- Codex,
- OpenCode,
- pi,
- OMP,
- OpenRouter Ori,
- named persistent agents,
- per-agent instructions,
- imported Claude Code / Codex chat history,
- SQLite memory,
- hierarchical summaries,
- retrieval back to original messages,
- configurable summary models,
- local OpenAI-compatible summary models,
- usage/cost tracking,
- encrypted cross-machine sync,
- backup and restore,
- controlled read access between agents,
- credential/file guards,
- Human-controlled instruction editing.

Windows currently uses WSL rather than native support.

## 3. Memory architecture

Each message is retained in the agent's SQLite database.

A summary model builds a hierarchy over older messages.

The agent receives:

- recent messages close to verbatim,
- progressively coarser summaries of older history,
- tools to zoom/search back to original messages.

Conceptually:

```text
all history
   ↓
summary tree
   ↓
compact persistent view
   ↓
agent context
   ↓
zoom to original when needed
```

This is a different approach from pure search-first retrieval.

## 4. Why it is important to AI-Harness

Orrery closely matches the long-term idea of AI as a continuing member rather than a disposable chat session.

Potential relevance:

- family AI members,
- Hermes Local Agent,
- long-lived specialist agents,
- cross-model continuity,
- switching between cloud and local models without losing identity,
- portable Human-owned memory.

The design idea is especially relevant to:

> persistent agent identity independent of the current model/provider.

## 5. Strong governance patterns

Several upstream safeguards are notable:

- agent instructions are Human-controlled,
- agents cannot freely rewrite their own identity instructions,
- one agent cannot read another agent's memory unless explicitly allowed,
- credential files are guarded,
- Orrery's own internal files are protected from agent writes,
- imported chats can be previewed before commitment,
- backup/rollback is supported.

These patterns align strongly with AI-Harness Human authority and Access separation.

## 6. Relationship to Awareness

Awareness and Orrery overlap but are not identical.

### Awareness

```text
memory as searchable knowledge library
```

Strengths:

- Markdown,
- transparency,
- hybrid retrieval,
- progressive disclosure,
- simpler local knowledge model.

### Orrery

```text
memory as continuity of a named agent
```

Strengths:

- persistent identity,
- hierarchical lifetime history,
- cross-tool continuity,
- model independence,
- agent-to-agent memory permissions,
- remote encrypted portability.

A future experiment should compare them directly rather than assuming one replaces the other.

## 7. Important risks

- summary drift over very long histories,
- incorrect old summaries becoming persistent context,
- memory poisoning,
- privacy of full conversation history,
- synchronization complexity,
- cost of summary generation,
- dependence on tool-specific hooks/mods,
- agent identity becoming too broad across unrelated projects.

The claim that a busy agent remains effective after approximately 17,000 messages is an author report, not independent evidence.

## 8. High-value patterns to absorb

Even if Orrery itself is never installed, several patterns are valuable:

- memory belongs to agent identity, not current model,
- Human owns identity instructions,
- hierarchical compaction with drill-down,
- explicit inter-agent read permissions,
- local original history,
- encrypted portable copies,
- backup/restore,
- separate conversational model and memory-compaction model.

## 9. Future experiment

A controlled comparison could use one bounded long-running project:

```text
A: current project Markdown / Harness only
B: Awareness
C: Orrery
```

Measure:

- continuity after new sessions,
- stale-memory rate,
- correction burden,
- token/context use,
- local resource use,
- cross-tool transfer,
- Human inspectability,
- security boundaries,
- recovery from bad memory.

## Decision

**A+ / CANDIDATE / IMPLEMENTATION HOLD**

Orrery is one of the strongest recent Memory candidates because it treats persistent memory as part of the agent's identity while retaining explicit Human authority.

Preserve both the implementation candidate and its design patterns.

No installation, login, chat import, memory migration, remote sync, hook modification, or Core integration is authorized by this record.