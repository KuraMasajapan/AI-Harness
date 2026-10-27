---
document_type: research_landscape
date: 2026-10-27
status: RESEARCH
decision: KEEP / COMPARE
evidence_status: CONFIRMED_UPSTREAM / CLAIMS_REQUIRE_LOCAL_VALIDATION
tags:
  - obsidian
  - second-brain
  - claude-code
  - codex
  - agent-skills
  - knowledge-graph
  - memory
---

# Obsidian + AI Second-Brain OSS Landscape

Trigger post:
https://x.com/obsidianstudio9/status/2114857106025464208

Original roundup:
https://x.com/Mr_Buzzoni/status/2114262687022510215

The post claims seven open-source repositories can be combined into an Obsidian + Claude Code / Codex "second brain".

The repositories are real. Their combined GitHub star count was above 250,000 at review time.

## Repositories reviewed

1. Graphify-Labs/graphify
2. Egonex-AI/Understand-Anything
3. AgriciDaniel/claude-obsidian
4. eugeniughelbur/obsidian-second-brain
5. MarkusPfundstein/mcp-obsidian
6. heyitsnoah/claudesidian
7. NicholasSpisak/second-brain

## Ranking for AI-Harness

| Rank | Project | Stage 1 | Stage 2 | Decision |
|---|---|---:|---:|---|
| 1 | claude-obsidian | A++ | A+ | CANDIDATE HIGH / DEEP COMPARE |
| 2 | Graphify | A+ | A | CANDIDATE HIGH / EXPERIMENT |
| 3 | obsidian-second-brain | A++ | A- | CANDIDATE / STUDY |
| 4 | Understand Anything | A | B+ | COMPARE WITH GRAPHIFY |
| 5 | second-brain | B+ | B+ | REFERENCE |
| 6 | claudesidian | B | B | STARTER REFERENCE |
| 7 | mcp-obsidian | B | B- | HOLD / BROAD AUTHORITY |

---

## 1. claude-obsidian — strongest fit

Repository:
https://github.com/AgriciDaniel/claude-obsidian

Key confirmed characteristics:

- plain Markdown vault
- existing Obsidian vault can be adopted
- source originals kept untouched
- source-linked / cited derived notes
- query path can be read-only
- helper agents are read-only
- one transaction core performs writes
- SHA-256 fingerprints detect concurrent human edits
- write conflicts stop instead of overwrite
- journal / recovery for interrupted writes
- remote/web research is a separate consented operation
- supports Claude Code and Agent Skills-compatible hosts including Codex
- supports Obsidian CLI / Bases-oriented workflows
- MIT license

### Why it matters

The strongest pattern is not "AI writes Obsidian".

It is:

```text
read-only workers
      ↓
draft / verification
      ↓
single transaction core
      ↓
hash check
      ↓
write
      ↓
rollback if interrupted
```

This closely matches AI-Harness concerns around Human authority, source locking, durable state, and controlled writes.

### Evaluation

**Stage 1: A++**
**Stage 2: A+**
**Decision: CANDIDATE HIGH / DEEP COMPARE**

A dedicated proposal exists separately.

---

## 2. Graphify — strongest Harness-side knowledge-graph candidate

Repository:
https://github.com/Graphify-Labs/graphify

Confirmed characteristics:

- maps code, docs, schemas and some media into a queryable graph
- code parsing uses deterministic tree-sitter AST analysis
- code analysis can remain local
- no vector store required for the core graph
- distinguishes `EXTRACTED` vs `INFERRED` edges
- persists graph output
- supports Claude Code, Codex, Gemini, Cursor, Hermes and other Agent Skills hosts
- Apache-2.0 license

Potential AI-Harness role:

```text
AI-Harness repository
      ↓
Graphify
      ↓
queryable dependency / concept graph
      ↓
Codex / Hermes / other agents
```

Useful if the repository becomes large enough that repeated file search / reconstruction is inefficient.

### Caveat

Claims such as major token-spend reduction and benchmark superiority are upstream claims and need local reproduction.

### Evaluation

**Stage 1: A+**
**Stage 2: A**
**Decision: CANDIDATE HIGH / EXPERIMENT**

---

## 3. obsidian-second-brain — high capability, higher trust risk

Repository:
https://github.com/eugeniughelbur/obsidian-second-brain

Confirmed current features include:

- persistent Markdown memory
- Claude Code / Codex / Cursor / Grok Bot shared "Crew" log
- lessons left by agents become rules only after a human `keep`
- X / web / YouTube / podcast research workflows
- scheduled agents
- synthesis
- contradiction reconciliation
- decision / project / task tracking
- vault health tooling
- multi-agent shared context

Important alignment:

```text
agent leaves lesson
      ↓
human keep decision
      ↓
rule promotion
```

This strongly resembles the AI-Harness LESSON lifecycle.

### Main concern

The project also explicitly promotes a self-maintaining vault:

> "the vault rewrites itself"

Ingest and scheduled workflows may rewrite multiple existing notes, reconcile contradictions, and evolve the knowledge base.

This is powerful but raises:
- provenance
- truth-maintenance
- silent overwrite
- blast-radius
- instruction-trust
- autonomous write-scope

questions.

### Evaluation

**Stage 1: A++**
**Stage 2: A-**
**Capability: A++**
**Trust / Safety fit: B**
**Decision: CANDIDATE / STUDY, NOT ADOPT**

The most attractive subcomponent is the **Crew** shared-log concept.

---

## 4. Understand Anything

Repository:
https://github.com/Egonex-AI/Understand-Anything

Confirmed:
- codebase knowledge graph
- multi-agent analysis
- interactive dashboard
- structural + semantic analysis
- incremental updates
- Codex / Claude / Hermes and other platform support
- MIT license

Strong project, but substantial overlap with Graphify.

Graphify is currently the preferred first comparison because:
- deterministic local structural parsing is clearer
- EXTRACTED / INFERRED distinction is explicit
- lower conceptual complexity for an initial AI-Harness experiment

**Decision: COMPARE WITH GRAPHIFY**

---

## 5. second-brain

Repository:
https://github.com/NicholasSpisak/second-brain

Simple Karpathy-style structure:

```text
raw/
  ↓
wiki/
  ↓
output/
```

Agent Skills provide ingest, query and lint workflows.

Strength:
- simple
- plain Markdown
- multi-agent compatible
- easy to inspect

Weakness:
- less mature safety / transaction architecture than claude-obsidian

**Decision: REFERENCE**

---

## 6. claudesidian

Repository:
https://github.com/heyitsnoah/claudesidian

Useful starter vault with:
- PARA structure
- thinking / writing modes
- skills
- helper scripts
- Git integration
- multi-agent skill compatibility

For AI-Harness, the project is more useful as a starter-design reference than a wholesale adoption target because AI-Harness already has its own durable project architecture.

**Decision: STARTER REFERENCE**

---

## 7. mcp-obsidian

Repository:
https://github.com/MarkusPfundstein/mcp-obsidian

Provides MCP tools for:
- list
- read
- search
- patch
- append
- delete

Requires the Obsidian Local REST API community plugin and an API key.

### Main concern

The MCP surface can hold broad vault-wide read/write/delete authority.

For AI-Harness this is currently less attractive than:

```text
plain Markdown
+ official Obsidian CLI
+ scoped write authority
```

because the latter is easier to reason about and constrain.

**Decision: HOLD / BROAD AUTHORITY**

---

# Architecture conclusion

The reviewed ecosystem does not invalidate the current AI-Harness direction.

Preferred structure remains:

```text
GitHub / Markdown
    = durable Source of Truth

Obsidian
    = human exploration / navigation layer

Agents
    = scoped readers / workers over the same Markdown assets
```

The main external patterns worth absorbing are:

- immutable source retention
- provenance
- read-only worker agents
- single controlled writer
- content-hash conflict detection
- transactional writes
- rollback / recovery
- vault lint / health checks
- shared agent work log
- optional knowledge graph over growing repositories

## Strategic principle

> Do not turn Obsidian into an autonomous source of truth merely because AI can write to it.

Prefer:

```text
trusted source
  ↓
scoped interpretation
  ↓
reviewable proposed change
  ↓
single controlled write path
  ↓
durable history
```

## Final decision

**KEEP / COMPARE**

The seven-project roundup is useful as an ecosystem map, but only a subset should advance to experiments.

Priority order:

1. claude-obsidian
2. Graphify
3. obsidian-second-brain Crew
