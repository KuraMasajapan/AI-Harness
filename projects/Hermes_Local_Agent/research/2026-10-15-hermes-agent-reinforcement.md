---
document_type: research_evaluation
date: 2026-10-15
source: Grok daily report via Airtable Harness Inbox
project: Hermes Local Agent
stage_1_rank: A++
stage_2_rank: A++
decision: CANDIDATE
relationship: REINFORCE
implementation: NOT IMPLEMENTED
phase: "Phase 0 — Project Definition"
verification: "Official v0.22.2 GitHub release checked; actual local deployment and performance untested"
---

# Hermes Agent v0.22.2 — Existing Project Reinforcement

## Context and historical decision
Human previously decided to establish **Hermes Local Agent** as a staged research project, evaluating Nous Research Hermes Agent as a possible local AI / Ground Station. The aim is to begin on an existing PC without a dedicated GPU, test Memory / Skills / Shell / File functions incrementally, and avoid recreating features already served by ChatGPT Work or Codex. **This report reinforces that earlier project decision; it is not a newly discovered independent project or an approval to implement.**

At recording time, the `development` branch tree contained no Hermes Local Agent paths. This research record preserves the previously discussed project direction; it does **not** assert that a prior GitHub PROJECT.md or formal project specification exists.

## New signal — 2026-10-15
Grok's daily report, received in Airtable Harness Inbox, highlighted Hermes Agent v0.22.0–v0.22.2:
- Easier one-click local model onboarding (llama.cpp; no API key for local execution).
- Bot Screen as a potential Human observation/takeover interface.
- App Connectors and plugin ecosystem as possible substitutes for bespoke integration.
- v0.22.2 gateway startup/reboot reliability fixes and improvements for long local-model turns on laptops.

**Independent primary-source check:** [Official Hermes Agent v0.22.2 release](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.2), published 2026-10-15. The release notes explicitly describe gateway reboot fixes and local-model long-turn handling; the broader v0.22 line contains other features. Feature availability and usability on the user's target hardware are **not** established by the release notes alone.

**Known issue:** v0.22.1 was built from the wrong commit and included unreleased gateway changes; sessions run under its gateway cannot be deleted in v0.22.2. Do not treat this release as proof of production stability.

## Two-stage assessment
- **Stage 1: A++** — Directly relevant to the already-selected Hermes Local Agent research direction, local-first low-cost operation and Human-in-the-loop controls.
- **Stage 2 (provisional): A++ / CANDIDATE, relation REINFORCE** — Official release evidence increases the plausibility and priority of the existing project; **not** a verified operational benefit. Preserve the distinction between evidence, inferred benefits, and untested assumptions.
- **No new independent proposal needed.** This is a reinforcement of an existing project hypothesis, not a duplicate to reject.
- **No implementation approval.** Remain at Phase 0 / NOT IMPLEMENTED pending a separate Human decision.

## Benefits, overlaps and limitations
| Topic | Potential benefit | Unverified question |
| --- | --- | --- |
| Local model onboarding | Reduce setup work and API dependence | Does it run acceptably without GPU on the available PC? |
| Bot Screen | Human visibility and takeover | What operations and approval boundaries does it actually enforce? |
| App Connectors | Reduce custom Harness integration | Which integrations are safe, free and necessary versus existing ChatGPT/Codex tools? |
| Gateway and long-turn fixes | Better resilience on laptops | Can reboot, sleep/wake and long contexts be reproduced reliably? |

Potential overlap: existing Ollama + HarnessRouter; ChatGPT Work/Codex; Harness approval/access controls. Favor **best-fit over feature count**. Do not infer that Hermes replaces Harness governance or satisfies Human approval by default.

## Minimal next validation, only after Human approval
1. Verify supported OS, CPU/RAM and GPU-free model options, installation requirements and licensing against upstream documentation.
2. Define a read-only, isolated pilot and baseline against current Ollama/HarnessRouter; do not grant broad Shell/File permissions by default.
3. Test local response latency, memory consumption, long-turn recovery, reboot persistence, and failure handling.
4. Observe Bot Screen takeover and whether sensitive actions truly remain Human-gated.
5. Compare setup/maintenance cost and functional overlap before any adoption recommendation.

## Record boundary
This document is a **research record**, not a PROJECT.md, Core rule, workflow modification, runtime installation or implementation order. No existing project files, Airtable records, Core, or Workflow are changed by this entry. Further modifications require explicit Human approval.
