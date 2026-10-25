---
document_type: research_strategy_note
date: 2026-10-26
project: Hermes Local Agent
status: CANDIDATE
implementation: NOT IMPLEMENTED
phase: "Phase 0 — Project Definition"
relationship: REINFORCE_AND_REFINE
---

# Hermes Ecosystem — Development Acceleration Signal

## Summary

Recent community projects around Hermes Agent indicate that several capabilities previously considered possible custom-development areas are already emerging as reusable external implementations.

This does **not** justify immediate installation or migration.

It does suggest a strategic refinement:

> Prefer **discover → verify → compare → selectively adopt** over building equivalent capabilities from scratch.

Potential benefit: shorter development time, lower maintenance burden, and fewer self-inflicted design mistakes.

This is currently an **inference from ecosystem maturity**, not a measured project-schedule reduction.

## Primary-source candidates reviewed

### 1. oh-my-hermes
Repository:
https://github.com/rlaope/oh-my-hermes

Observed capabilities include:

- DAG-based parallel task execution
- per-lane model / reasoning routing
- 100+ installable expert skills
- evidence-based completion states
- independent goal verification
- bounded parallel write scopes
- long-term memory / recall packs
- cost and token telemetry
- guardrails and approval tiers

### 2. hermes-lcm
Repository:
https://github.com/stephenschoettler/hermes-lcm

Observed capabilities include:

- SQLite-backed preservation of raw messages
- DAG-based hierarchical summaries
- bounded active context
- exact-detail recovery after compaction
- source lineage
- recall / expand / inspect tools
- optional sensitive-pattern redaction
- backup-first diagnostics and repair

This directly overlaps with AI-Harness concerns about losing constraints or evidence during summarization, compaction, or handoff.

### 3. 42-evey/hermes-plugins
Repository:
https://github.com/42-evey/hermes-plugins

Potentially relevant individual components include:

- verify-before-done
- work-ledger
- delegation-brief
- session-guard
- validation
- cost-guard
- telemetry

The bundle should not be treated as one adoption unit. Individual skills/plugins should be evaluated selectively.

### 4. hermes-plugin-shodan
Repository:
https://github.com/Adolanium/hermes-plugin-shodan

Not currently needed as functionality, but useful as an Agent Tool safety-design reference because it demonstrates:

- local budget enforcement
- default-off active scanning
- explicit opt-in
- capability / plan checks
- doctor-style diagnostics
- machine-readable failure with next-step guidance

### 5. hermes-bot-kit
Repository:
https://github.com/thomasbek3/hermes-bot-kit

Potential later-phase value:

- conversational bot UI
- bot grouping
- task dock
- live computer view
- optional remote computer control

Remote interaction features have materially larger permission and safety implications, so they remain later-phase only.

## Current priority

Research priority:

1. **hermes-lcm**
2. **oh-my-hermes**
3. **selected 42-evey skills/plugins**
4. Shodan plugin as design reference
5. Bot Kit as later UI / remote-computer reference

## Strategic implication for Hermes Local Agent

Earlier project direction intentionally avoided building a large autonomous system during Phase 0.

The emerging ecosystem strengthens that decision.

The preferred direction is now:

```text
Hermes core
   ↓
observe existing ecosystem
   ↓
identify actual capability gap
   ↓
verify primary source + behavior
   ↓
compare with AI-Harness / ChatGPT / Codex
   ↓
adopt only the smallest useful component
   ↓
build custom code only for uncovered needs
```

This should reduce unnecessary duplication.

## Relationship to AI-Harness

The ecosystem already contains implementations related to:

- Memory
- context compaction
- DAG orchestration
- verification
- work ledgers
- session protection
- cost control
- model routing
- UI
- remote-computer control

Therefore future evaluation should ask:

1. Does AI-Harness already solve this?
2. Is the external implementation measurably better or more enforceable?
3. Can it be used without weakening Human authority?
4. Can it be integrated without creating duplicate state or governance?
5. Does the maintenance burden remain lower than building it ourselves?
6. Is the capability actually necessary now?

## Important boundary

This note does **not**:

- move Hermes Local Agent out of Phase 0
- approve installation of any plugin
- approve autonomous execution
- modify Core / Workflow / ACCESS / TRINITY
- replace ChatGPT Work or Codex
- claim a quantified development-time reduction

The only decision recorded here is:

**The Hermes ecosystem now appears mature enough that ecosystem-first evaluation may materially shorten future development.**

That hypothesis should be validated through concrete comparisons before implementation.
