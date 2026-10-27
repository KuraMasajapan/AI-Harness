---
status: proposal
created: 2026-10-27
decision: CANDIDATE
priority: A++
implementation: HOLD / NOT IMPLEMENTED
evidence_status: CONFIRMED_UPSTREAM / LOCAL_VALIDATION_UNVERIFIED
tags:
  - thinkrail
  - jetbrains
  - agentic-ide
  - living-specs
  - worktree
  - skills
  - mcp
  - human-review
---

# ThinkRail — Agentic IDE / Harness Reference

Source:
https://github.com/JetBrains/thinkrail

## Confirmed upstream capabilities

ThinkRail is a JetBrains incubator project built around the `pi` coding agent.

Confirmed features include:
- git worktree-based isolated workspaces
- multiple concurrent agent sessions
- Monaco editor / terminals / file tree / diffs
- reusable Agent Skills
- persistent project knowledge through connected `SPEC.md` files ("living specs")
- `spec_*` tools for reading/searching/maintaining specs
- GitHub PR / CI / review workflow support
- MCP server integration
- non-read-only MCP calls require chat confirmation unless explicitly trusted
- repository-defined MCP servers remain disabled until approved
- model/provider credentials remain user-controlled
- Apache-2.0 license

## AI-Harness relevance

ThinkRail materially overlaps with several AI-Harness design goals:

- Source of Truth / durable project context
- isolated agent workspaces
- reusable skills
- Human review before consequential actions
- reviewable diffs and PRs
- project-specific specification graphs
- separation of agent runtime from human-facing control surfaces

Conceptual structure:

```text
Project specification
   ↓
Agent reads durable context
   ↓
isolated worktree
   ↓
implementation
   ↓
diff / tests / PR
   ↓
Human review
   ↓
merge
```

This is a strong external implementation reference for the general AI-Harness direction.

## Important correction to social-media framing

ThinkRail does **not** currently demonstrate autonomous model self-training or unrestricted self-evolution.

Its "gets better every time you use it" framing is primarily supported by:
- living specs that evolve with the project
- reusable skills
- accumulated project context

The README says future extension support may let ThinkRail create tools it needs, but that is described as a next-stage capability rather than a currently verified autonomous self-modification loop.

## Comparison questions for AI-Harness

Future evaluation should compare:
- `SPEC.md` graph vs current AI-Harness Markdown / project Source of Truth
- worktree isolation vs current Codex/project workflow
- MCP approval enforcement vs AI-Harness ACCESS
- reusable Skills loading / scope / precedence
- spec drift prevention
- runtime evidence and Definition of Done
- Human authority under concurrent agents
- whether adopting ThinkRail would simplify or duplicate existing ChatGPT/Codex/Hermes capability

## Decision

**Stage 1: A++**
**Stage 2: A+ provisional**
**Decision: CANDIDATE HIGH / COMPARE**
**Implementation: HOLD**

No installation, Core modification, workflow replacement, or agent migration is authorized by this note.
