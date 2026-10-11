---
status: proposal
created: 2026-10-11
origin: Human-provided coding-stack shortlist -> ChatGPT practical-use review
tags:
  - coding
  - context
  - mcp
  - code-navigation
  - documentation
  - candidate
---

# Coding Context Tool Candidates — Serena / Context7

## Purpose

Preserve only the newly reviewed coding-context tools that add a meaningfully distinct capability beyond the current AI-Harness / ChatGPT / Codex workflow.

This note does **not** mean adoption or installation.

Current decision:

- Serena: EXPERIMENT candidate
- Context7: HOLD candidate
- Existing candidates Browser Use / E2B / Langfuse remain covered by the existing OSS landscape note
- Aider / GitHub MCP / Ruff / pytest are not added here

---

# 1. Serena

Repository:

- https://github.com/oraios/serena

Current judgment:

**EXPERIMENT CANDIDATE**

## Why it survives the filter

Serena adds symbol-aware code navigation and editing through MCP and language-server-backed semantic structure.

Relevant capabilities include:

- find symbol
- symbol overview
- find references
- cross-file relationship discovery
- symbol-aware rename
- symbol body replacement
- insert before / after symbol
- code exploration at semantic rather than raw-text level

This is meaningfully different from simply adding another coding agent.

The main expected benefit is reducing unnecessary context loading in larger repositories.

Candidate pattern:

```text
Large repository
    ↓
Need to understand one feature / symbol
    ↓
Serena resolves symbols + references
    ↓
Only affected files / relationships enter context
    ↓
Codex or another agent reasons and edits
```

## Potential value

- more precise code navigation
- fewer irrelevant files loaded into model context
- better cross-file impact analysis
- safer symbol-level refactoring than blind search/replace
- possible token savings on large repositories
- fits as a specialist tool beneath the coding agent rather than replacing it

## When it is likely unnecessary

For small repositories, ordinary Codex search / grep / file reading may already be sufficient.

Do not add Serena merely because it exists.

## Risks / open questions

- adds another MCP surface
- language-server setup may vary by language
- tool behavior and agent behavior may become harder to distinguish
- benefit must be demonstrated on a real large repository
- Serena application licensing is GPL-3.0-or-later; SolidLSP has a separate MIT component license

## Suggested experiment trigger

Test Serena only when one or more of these become true:

- a repository becomes large enough that Codex repeatedly opens too many files
- symbol/reference discovery becomes a recurring manual step
- cross-file refactors create avoidable mistakes
- context use grows because code relationships must be rediscovered repeatedly

Suggested evaluation:

```text
same task
A: Codex alone
B: Codex + Serena
```

Compare:

- files opened
- context consumed
- time to identify impact
- correctness of affected-file set
- edit quality
- Human correction required

No adoption until the difference is measurable.

---

# 2. Context7

Repository:

- https://github.com/upstash/context7

Current judgment:

**HOLD — USE WHEN VERSIONED DOC FRICTION APPEARS**

## Why it survives the filter

Context7 provides current, version-specific documentation and code examples to coding agents.

Its main value is avoiding implementation from stale model knowledge.

Candidate pattern:

```text
Implementation requires external library
        ↓
Model knowledge may be stale
        ↓
Context7 fetches current / version-specific docs
        ↓
Agent implements against actual API surface
```

This is particularly relevant for fast-moving frameworks and SDKs.

## Potential value

- reduces hallucinated or removed APIs
- reduces manual browser switching during implementation
- can supply version-specific documentation
- can integrate through CLI / Skill or MCP
- may help Codex stay within the implementation flow

## Why it is not a current priority

ChatGPT can already inspect current official documentation and GitHub sources directly when needed.

Therefore Context7 only earns a place if documentation lookup becomes a recurring coding bottleneck inside Codex or another agent environment.

## Risks / open questions

- adds another external context provider
- fetched documentation still needs source / version verification
- convenience can encourage blind trust in retrieved examples
- an additional MCP integration increases configuration surface
- API key / service dependency may be unnecessary for infrequent use

## Suggested trigger

Revisit when:

- Codex repeatedly generates code against stale SDK APIs
- external library documentation must be checked many times per task
- switching between agent and browser becomes measurable friction
- a project pins many fast-moving dependencies

Possible evaluation:

```text
same version-sensitive task
A: Codex + ordinary web/docs lookup
B: Codex + Context7
```

Compare:

- implementation accuracy
- number of stale / invalid API calls
- Human correction effort
- setup overhead
- token / context cost

---

# 3. Explicitly not added

## Aider

A mature terminal coding agent, but its primary role overlaps strongly with Codex.

Current decision:

**IGNORE unless Codex itself becomes the problem.**

---

## GitHub MCP Server

GitHub's official MCP server is capable and useful, but the present ChatGPT environment already has direct GitHub access.

Possible future relevance exists for an independent Codex / MCP environment.

Current decision:

**NO NEW CANDIDATE NOTE. Revisit only for standalone Codex GitHub operation.**

---

## Ruff

Ruff is an excellent deterministic Python linter / formatter.

It should be treated as ordinary project tooling, not as an AI-Harness architectural candidate.

Current decision:

**USE in Python projects when appropriate; do not add to Incubator.**

---

## pytest

pytest is a standard Python testing framework and fits the broader principle:

```text
AI reasoning
!=
deterministic verification
```

But pytest itself is normal development infrastructure rather than an AI-Harness candidate.

Current decision:

**USE in Python projects when appropriate; do not add to Incubator.**

---

# Architectural takeaway

The useful part of the reviewed stack is not the number of tools.

The more durable pattern is:

```text
AI model
= planning
  hard reasoning
  implementation
  debugging
  final review

Specialist deterministic tools
= code navigation
  versioned documentation
  lint
  tests
  sandboxing
  observability
```

For the current operating model, start small:

```text
ChatGPT / Astra
      ↓
Codex
      ↓
Serena            (only when repository scale justifies it)
      ↓
Ruff / pytest     (when Python)
      ↓
Git
      ↓
Human
```

Add other layers only when a measured problem appears.

---

# Decision

Preserve Serena and Context7 as future coding-context candidates.

Do not install either yet.

Adoption requires a concrete workload, comparative test, and measurable reduction in Human effort or failure rate.
