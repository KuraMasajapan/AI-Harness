---
status: proposal
created: 2026-10-11
origin: Human-provided OSS shortlist -> ChatGPT strict practical-use review
tags:
  - practical-tools
  - oss
  - voice
  - diagrams
  - presentations
  - reverse-engineering
  - orchestration
  - candidate
---

# Practical OSS Tool Candidates — 2026-10-11

## Purpose

Preserve only the OSS tools from the reviewed shortlist that have enough practical value to justify future use or comparison.

This note is intentionally selective.

It does **not** mean adoption, installation, or promotion into AI-Harness.

Current principle:

> Useful tools may be used even when they are not part of the Harness itself, but they should earn their place through real utility, low operational friction, and limited overlap with existing capabilities.

---

## Summary

| Tool | Current judgment | Candidate role |
|---|---|---|
| VoiceStudio | TRY | Local voice / transcription / dubbing tool |
| Diagram Design | TRY | Publication-quality diagrams and visual explanations |
| PPT Master | USE WHEN NEEDED | Editable PowerPoint generation |
| REA | USE WHEN NEEDED | Evidence-backed reverse engineering / inspection |
| Paperclip | COMPARE LATER | Agent orchestration / management reference |

The following reviewed tools were intentionally **not preserved as active candidates**:

- God's Eye View
- mattpocock/skills as a full bundle
- ECC
- andrej-karpathy-skills
- claude-mem

Reason: insufficient current need, overlap with existing Harness work, excessive operational surface, or risk of making behavior harder to attribute.

---

# 1. VoiceStudio

Repository:

- https://github.com/debpalash/VoiceStudio

Current judgment:

**TRY**

## Why it survives the filter

VoiceStudio is more than a voice-cloning demo.

The current project provides a local-first desktop workflow covering:

- voice cloning
- voice design
- video dubbing
- dictation
- transcription
- audiobook / batch generation
- local API
- MCP integration
- Windows / macOS / Linux support
- optional remote workers

It can run without a dedicated GPU, although CPU execution is slower.

This gives it direct practical value for future local-AI, speech, family-interface, media, and accessibility workflows.

## Important constraints

- CPU-only operation may be slow.
- Local speech models can consume substantial disk space.
- "646 languages" is coverage, not proof of equal quality across all languages.
- Japanese quality must be tested directly.
- The application is AGPL-3.0.
- Individual model weights, tokenizers, voices, and generated outputs can have separate licensing conditions.
- Voice cloning should only be used with proper permission.

## Suggested test

Use one clean Japanese voice sample and evaluate:

1. Japanese voice cloning quality
2. transcription accuracy
3. latency on the current PC
4. disk / RAM use
5. MCP / local API usability
6. whether the result is good enough to replace simpler STT/TTS pieces

No adoption decision before this real test.

---

# 2. Diagram Design

Repository:

- https://github.com/cathrynlavery/diagram-design

Current judgment:

**TRY**

## Why it survives the filter

This is an Agent Skill for generating polished diagrams as self-contained HTML + SVG.

The project currently supports 44 diagram types, including:

- architecture
- flowchart
- sequence
- state machine
- timeline
- swimlane
- quadrant
- loop
- tree
- data / system diagrams

It also supports brand profiles and PNG / SVG export.

This maps directly to practical needs around:

- AI-Harness architecture diagrams
- TRINITY flows
- Temporal Spine diagrams
- BBB architecture
- UIAPduino explanations
- Note article visuals
- comparison diagrams
- project documentation

## Important constraint

It is not a full interactive diagram editor.

The project itself notes that output quality depends on the model and layout can vary between runs.

For frequently changing Git-tracked technical diagrams, Mermaid or another deterministic text format may remain better.

Candidate split:

```text
Internal evolving technical spec
→ Mermaid / text-native diagram

Published explanation / presentation visual
→ Diagram Design
```

## Suggested test

Generate one existing AI-Harness architecture diagram from the current specification and compare against:

- Mermaid
- hand-built SVG
- image generation

Judge:

- correctness
- readability
- visual quality
- editability
- repeatability
- update effort

---

# 3. PPT Master

Repository:

- https://github.com/hugohe3/ppt-master

Current judgment:

**USE WHEN NEEDED**

## Why it survives the filter

PPT Master produces real editable PowerPoint files rather than flattened slide images.

Current project capabilities include:

- source documents -> PPTX
- native PowerPoint shapes
- native charts and tables
- slide masters / layouts
- transitions
- animations
- narration
- use of existing PPTX templates
- local workflow apart from model communication
- MIT license

This is potentially useful whenever an actual editable presentation is required.

## Why it should not be installed preemptively

The tool itself is free, but output quality still depends heavily on the AI model used.

The project explicitly states that a one-shot perfect deck should not be expected.

That means real cost can appear as:

- model usage
- agent quota
- image-generation calls
- Human polishing time

Therefore this should be invoked when a real presentation task exists, not kept as infrastructure by default.

## Suggested trigger

Evaluate only when there is an actual need for:

- an editable PPTX
- reuse of an existing corporate / project template
- a large deck that would otherwise take substantial manual work

---

# 4. REA

Repository:

- https://github.com/morluto/rea

Current judgment:

**USE WHEN NEEDED**

## Why it survives the filter

REA is a practical inspection / reverse-engineering toolkit rather than just an AI explanation layer.

It can support analysis of:

- JavaScript / Electron applications
- websites
- native binaries
- .NET assemblies
- Android APKs
- saved network captures
- process behavior
- firmware
- EVM bytecode

The agent receives evidence and limitations with findings rather than only a free-form explanation.

It supports multiple agents through MCP, including Codex and Claude Code.

## Why it should remain on-demand

Its useful scope is broad, but some targets require additional tooling such as:

- Ghidra
- Hopper
- IDA
- JADX
- JDK
- Binwalk
- other native tooling

Installing the whole analysis stack without a concrete target would add maintenance burden with no current payoff.

## Suggested trigger

Use REA when there is a specific question such as:

- "How does this Electron application implement this feature?"
- "Where does this website perform this network call?"
- "How is this APK structured?"
- "What evidence supports this compatibility assumption?"

Do not use it as a default dependency.

---

# 5. Paperclip

Repository:

- https://github.com/paperclipai/paperclip

Current judgment:

**COMPARE LATER — DO NOT INSTALL NOW**

## Why it survives the filter

Paperclip is not merely a convenience app.

It is a substantial multi-agent orchestration and management system covering:

- tasks
- goals
- agent roles
- permissions
- Human approvals
- budgets
- cost tracking
- schedules
- cron / webhook triggers
- secrets
- workspaces
- git worktrees
- runtime services
- durable activity / audit trails
- pause / resume / termination

It supports multiple agent types including Codex, Claude Code, Gemini, Pi, Hermes and others.

Because of that, it is relevant as an external architectural comparison target for AI-Harness.

## Why it should not be adopted now

Paperclip is a server-oriented orchestration system.

The current Human operating environment does not assume an always-on home server.

That conflicts with the more natural topology currently under consideration:

```text
Human
  = Authority

GitHub
  = Durable Knowledge

iPhone / durable mobile runtime
  = Continuity / Ground Station candidate

Cloud AI
  = Intelligence

Home PC
  = Intermittent worker
```

Installing Paperclip now would introduce a large parallel orchestration model before the simpler runtime question is settled.

## Future comparison value

Paperclip may still be useful to compare against AI-Harness on:

- task ownership
- approval gates
- budget control
- event scheduling
- durable execution records
- agent lifecycle
- secret handling
- auditability

Treat it as a reference implementation, not a migration target.

---

# Rejected / deferred items

## God's Eye View

Interesting and technically rich, but insufficient day-to-day utility for the current workload.

Large data-source and API surface, experimental OAuth paths, and unclear current licensing posture reduce practical value.

Decision: **do not preserve as an active candidate**.

## mattpocock/skills

High-quality engineering skills, but substantial overlap with current Harness work around planning, review, handoff, testing and research.

The full bundle would make behavioral attribution harder.

Individual skills may be inspected later if a specific gap appears.

Decision: **do not preserve the full bundle as an active candidate**.

## ECC

Very broad system: agents, hundreds of skills, memory, hooks, security tooling and multiple harness adapters.

Installing it would place another large Harness layer on top of the existing one and make behavior difficult to isolate.

AgentShield or another isolated component may be revisited independently.

Decision: **do not install or adopt now**.

## andrej-karpathy-skills

The four principles are useful:

- think before coding
- simplicity first
- surgical changes
- goal-driven execution

However, these ideas already substantially exist in the current Harness direction.

Installing another instruction file would add little value.

Decision: **read-only reference; no active candidate**.

## claude-mem

Technically capable persistent memory system, but its automatic capture / compression / reinjection model overlaps with unresolved AI-Harness memory-governance work.

Potential conflicts include:

- stale memory
- silent capture
- automatic context injection
- unclear authority
- memory drift
- difficulty separating tool behavior from Harness behavior

Current hosted / trial memory options also add another service boundary.

Decision: **do not install now**.

---

# Practical adoption rule

A candidate should move forward only when one of these becomes true:

1. A real task appears that clearly benefits from it.
2. Current tools fail repeatedly at that task.
3. The candidate measurably reduces Human work.
4. It does not obscure which layer caused a failure.
5. It can be removed without damaging project state.

Popularity alone is not sufficient.

```text
Stars
!= Reliability
!= Fit
!= Safety
!= Lower total operating cost
```

The preferred strategy remains:

> **Use the smallest tool that solves a real problem, and only introduce another layer when measured friction justifies it.**
