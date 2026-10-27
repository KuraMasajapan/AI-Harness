---
status: proposal
created: 2026-10-27
decision: CANDIDATE HIGH / DEEP COMPARE
stage_1: A++
stage_2: A+
implementation: HOLD / NOT IMPLEMENTED
evidence_status: CONFIRMED_UPSTREAM / LOCAL_VALIDATION_UNVERIFIED
tags:
  - claude-obsidian
  - obsidian
  - agent-skills
  - provenance
  - transaction
  - read-only-agent
  - rollback
  - conflict-detection
---

# claude-obsidian — AI-Harness Candidate

Source:
https://github.com/AgriciDaniel/claude-obsidian

License:
MIT

## Why this candidate is important

claude-obsidian is notable not because it connects Claude to Obsidian, but because its write architecture is comparatively disciplined.

Confirmed upstream design includes:

- plain Markdown
- source originals retained
- source-linked derived notes
- read-only helper agents
- one write-capable transaction core
- SHA-256 fingerprint checks before write
- conflict stop if the human edits during planning
- journal-based recovery for interrupted writes
- explicit separation of read/query and write operations
- consent boundaries for external research / remote operations
- support for Claude Code and other Agent Skills hosts including Codex
- ability to adopt an existing vault

## Architectural pattern worth comparing

```text
Source
  ↓
read-only ingest / lint / verification
  ↓
drafts
  ↓
transaction plan
  ↓
hash / conflict check
  ↓
single writer
  ↓
journaled apply
  ↓
rollback if needed
```

This is highly relevant to AI-Harness.

## Potential AI-Harness mappings

| claude-obsidian concept | AI-Harness analogue |
|---|---|
| source originals | Source of Truth / evidence preservation |
| read-only helper agents | low-authority research / verification agents |
| transaction core | controlled action authority |
| SHA-256 fingerprints | Source-Locked Creation / stale-state detection |
| write conflict stop | Human edits win |
| journal recovery | durable state / reversibility |
| cited notes | evidence traceability |
| lint | evaluation / consistency check |

## Important boundary

This proposal does **not** recommend replacing GitHub with Obsidian.

Preferred AI-Harness interpretation remains:

```text
GitHub / Markdown
    = durable Source of Truth

Obsidian
    = exploration / visualization / human interaction

Agent skills
    = scoped operations

Controlled writer
    = approved durable changes
```

## Questions for future Stage 2 experiment

1. Can its transaction model work safely over an AI-Harness-style repository?
2. Are fingerprints checked for every write target and every relevant dependency?
3. What happens under multiple concurrent agents?
4. How does recovery behave after partial filesystem failure?
5. Are source citations mechanically preserved through rewrites?
6. Can all external fetch/research remain separately gated?
7. Can write-capable operations be reduced to a minimal authority surface?
8. Can the model be used without making Obsidian the authoritative state?
9. Does the multi-agent setup respect Instruction Trust Boundary principles?
10. What complexity does it add compared with Git + existing AI-Harness workflow?

## Evaluation

**Stage 1: A++**
**Stage 2: A+ provisional**
**AI-Harness relevance: A++**
**Safety architecture: A**
**Implementation confidence: upstream-confirmed, local-unverified**

## Decision

**CANDIDATE HIGH / DEEP COMPARE**

No installation, vault migration, automatic writer, Core change, or Source-of-Truth replacement is authorized by this note.

Recommended future action:
run a disposable-vault / disposable-repository experiment focused specifically on:
- read-only worker isolation
- transaction behavior
- hash conflict handling
- rollback
- provenance preservation
