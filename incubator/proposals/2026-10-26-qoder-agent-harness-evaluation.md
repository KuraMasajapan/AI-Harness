---
status: proposal
created: 2026-10-26
origin: X post -> primary-source verification
tags:
  - qoder
  - agent-harness
  - coding-agent
  - skills
  - hooks
  - mcp
  - byok
  - free-tier
  - evaluation
---

# Qoder — Agent Harness Evaluation Candidate

## Status

**CANDIDATE — MEDIUM/HIGH**

- Adoption: NOT DECIDED
- Installation: NOT PERFORMED
- Existing-tool replacement: NOT RECOMMENDED YET
- Core change: NONE
- TRINITY change: NONE

## Trigger

X post:
https://x.com/yedabinbinah/status/2114160360433529217

The post claimed that Qoder currently offers DeepSeek-V4.1-Flash-1017 for free for a limited time and described very large effective daily usage, daily 100 Credits, and an additional 1,024 Credits campaign.

The social post is treated as a lead, not as authoritative evidence.

## Primary-source verification

### CONFIRMED

Official Qoder documentation confirms:

- `DeepSeek-V4.1-Flash-1017` is listed in the Qoder Lite Flash model lineup and is currently marked **free for a limited time**.
- Qoder International individual users, including Free users, can manually claim **100 Credits each day** in the Qoder desktop app.
  - The promotion began September 18, 2026.
  - End date: to be announced.
  - Each claimed reward is valid for 30 days.
- Qoder Community Boost offers a **1,024 SOTA Credits Welcome Pack** under separate eligibility rules.
  - Promotion period: October 22–30, 2026 (UTC+8).
  - The promotional Credits are for the **Sonus** model.
  - Free users require application approval.
  - Lite does not currently support Sonus.

Official sources:

- https://docs.qoder.com/events/100credits
- https://docs.qoder.com/release-notes/lite-launch-announcement
- https://docs.qoder.com/events/communityboost
- https://docs.qoder.com/release-notes/qoder-cli

### UNVERIFIED / DO NOT STORE AS FACT

The X post's claims that:

- DeepSeek-V4.1-Flash-1017 is free specifically until **2026-11-01**
- one account effectively receives about **100 million tokens per day**

were not confirmed in the official material reviewed.

Treat both as social-post / user-observed claims unless later verified by Qoder's product UI or official documentation.

## Why Qoder matters to AI-Harness

The important research value is **not primarily the temporary free-token promotion**.

Qoder is a potentially useful comparison target for AI-Harness because official documentation shows support for several harness-level capabilities:

- Skills
- Hooks
- MCP
- BYOK
- Agents / sub-agents
- plugins containing Skills, Agents, Connectors, Commands, Rules and Hooks
- session resume / branching
- checkpoints and rewind behavior
- model-call limits
- automatic context compaction
- permission / approval modes
- retry and failure handling
- Cloud Agents and local automation

This makes Qoder useful as a **second coding-agent / agent-harness implementation to compare against Codex, Claude Code, OpenCode and future Hermes work**, rather than simply as a source of a free DeepSeek model.

## Evidence especially relevant to current Harness research

Recent Qoder CLI release notes show concrete reliability behavior relevant to existing AI-Harness concerns:

- 2026-10-13: fixed unfinished responses being incorrectly reported as completed when the model hit its output limit.
- 2026-10-10 and earlier: improved recovery around compaction and session failures.
- 2026-10-08: ACP `session/load` reports success only after historical messages have actually been replayed.
- 2026-09-18: Auto mode falls back to user confirmation when auto-approval is unavailable.
- 2026-09-09: per-request model-call limits added.
- Session branching, checkpoint/rewind behavior, Hooks, MCP, Skills and permission handling are actively maintained.

These are relevant to the AI-Harness distinction between:

```text
Rule exists
!= Runtime activated
!= Correctly completed
!= Verified
```

and to the Runtime Enforcement Review questions around state durability, gate bypass, recovery and evidence of execution.

## Existing overlap

AI-Harness already has principles for:

- progressive disclosure
- minimal necessary context
- Human authority
- Read / Propose / Evaluate / Write / Promote / Approve separation
- runtime activation vs declarative rules
- checkpoint / state durability review
- verification after execution
- failure handling

Therefore Qoder should **not** be adopted merely because it has similar features.

The research question is whether any of Qoder's concrete runtime mechanisms are measurably better, simpler, or more enforceable than the current or planned AI-Harness mechanisms.

## Suggested comparison

Before any installation or migration:

1. Compare Qoder against the current Codex workflow on a small fixed task set.
2. Evaluate:
   - rule / instruction loading
   - Skill discovery
   - MCP tool selection
   - Hooks / deterministic trigger behavior
   - permission approval and fallback
   - session resume / branch fidelity
   - compaction recovery
   - unfinished-response detection
   - model-call budgeting
   - checkpoint / rewind behavior
3. Record:
   - task success
   - missed constraints
   - false completion
   - user intervention required
   - latency
   - cost / credits
   - recovery quality
4. Do not mix the evaluation with the temporary free-model promotion.

## Risks / limits

- Promotional free access can disappear or change at any time.
- Large-token claims from social media may describe effective use rather than a contractual quota.
- Similar feature names do not prove identical enforcement semantics.
- Cloud features may introduce privacy / data-transfer considerations.
- Installing a second coding-agent stack may add complexity without improving the current Codex workflow.
- Promotional Credits and free model access should not drive architecture decisions.

## Decision

**CANDIDATE — MEDIUM/HIGH**

Preserve Qoder as an **Agent Harness comparison candidate**.

Do not:
- replace Codex,
- migrate projects,
- install Qoder solely for the promotion,
- change Core / Workflow / TRINITY,
- or record the "100M tokens/day" claim as verified fact.

A future low-risk comparison is justified if a concrete AI-Harness question requires an independent implementation reference.
