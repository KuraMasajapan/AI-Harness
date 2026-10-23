---
document_type: research_evaluation
date: 2026-10-23
title: "Awareness Local — Local-first MCP Memory Candidate"
source_repository: "https://github.com/everest-an/Awareness-Market"
discovery_source: "Grok Observer"
decision: CANDIDATE
implementation: HOLD
stage_1_rank: A+
stage_2_rank: A
evidence_status: "OFFICIAL REPOSITORY VERIFIED; BENCHMARK CLAIMS PARTIALLY SELF-REPORTED"
tags:
  - memory
  - mcp
  - local-first
  - markdown
  - sqlite
  - retrieval
  - codex
  - claude-code
---

# Awareness Local — Local-first MCP Memory Candidate

## Status

**Stage 1: A+**  
**Stage 2: A**  
**Decision: CANDIDATE**  
**Implementation: HOLD**

Discovered by the Grok Observer on 2026-10-23 and independently verified against the official repository.

## 1. What it is

Awareness Local is a local-first persistent-memory layer for AI coding agents.

Its basic structure is:

```text
Claude Code / Codex / Cursor / other MCP clients
                     ↓
                MCP daemon
                     ↓
           Markdown + SQLite FTS5
                     ↓
          keyword + semantic retrieval
```

The project stores durable memory in human-readable Markdown and uses a local SQLite index for retrieval.

Cloud sync is optional rather than required.

## 2. Officially confirmed capabilities

The official repository documents:

- local-first operation,
- no account required for local use,
- Markdown storage under `.awareness/`,
- SQLite FTS5 keyword search,
- optional local embeddings,
- hybrid retrieval,
- MCP access,
- progressive disclosure,
- cross-session memory,
- Claude Code support,
- Codex CLI support,
- multiple other MCP-compatible clients,
- optional cloud sync,
- local dashboard.

A key strength is that the durable source material remains inspectable by the Human.

## 3. Benchmark caution

The project reports **96.0% Recall@5 on LongMemEval**.

This must not be interpreted as:

> "The agent answers correctly 96% of the time."

Recall@5 means the relevant evidence was retrieved within the top five results in the reported benchmark.

This is useful evidence for retrieval quality, but it is not equivalent to end-to-end answer accuracy, memory correctness, or autonomous task performance.

Treat the benchmark as an upstream reproducible claim until independently reproduced in our environment.

## 4. Why it matters to AI-Harness

Awareness matches several existing goals:

- local-first memory,
- readable storage,
- low cloud dependency,
- cross-session continuity,
- low-cost retrieval,
- selective context loading.

Its progressive-disclosure pattern is especially relevant:

```text
memory index
   ↓
small summaries
   ↓
agent selects useful entries
   ↓
full records loaded only when needed
```

This may reduce context waste compared with dumping full history into every session.

## 5. Relationship to existing Harness design

Potential complementary role:

```text
AI-Harness project truth / rules
            +
Awareness retrievable episodic memory
```

It should not replace authoritative project files, RULES, ACCESS, WORKFLOW, or Human-approved durable records.

Memory retrieved from Awareness should remain evidence/context, not automatically become policy.

## 6. Risks

- incorrect or stale memory can be retrieved confidently,
- semantic search quality depends on indexing and embeddings,
- local daemon adds another runtime dependency,
- automatic capture may store sensitive material,
- cloud sync changes the threat model,
- retrieval quality does not guarantee reasoning quality,
- memory accumulation can create noise or contradictory history.

## 7. Comparison target

Primary comparison candidate:

- Orrery

Useful conceptual distinction:

```text
Awareness
= searchable memory library

Orrery
= continuous agent identity/history
```

A future experiment should compare:

- setup complexity,
- local resource use,
- retrieval precision,
- Human inspectability,
- cross-tool portability,
- memory growth,
- stale-memory handling,
- security boundaries,
- token savings.

## Decision

**A+ / CANDIDATE / IMPLEMENTATION HOLD**

Preserve as a strong local-memory candidate and source of design patterns.

No installation, MCP registration, cloud sync, auto-capture, or Core integration is authorized by this record.