---
document_type: research_evaluation
date: 2026-10-16
subject: LCU (Local Computer Use)
stage_1_rank: A++
stage_2_rank: A++
decision: CANDIDATE
relationship: REINFORCE
related_project: Hermes Local Agent
implementation: NOT APPROVED
verification: "Upstream documentation claims require reproducible environment-specific validation"
---
# LCU — desktop-control candidate linked to Hermes Local Agent

## Signal
An X post describes LCU as a way to expose desktop computer-control capabilities to Claude Code through the ChatGPT desktop application's local environment, without Codex model inference. Treat assertions about login requirements, quota consumption, OpenAI endorsement and unrestricted compatibility as **claims needing separate confirmation**.

Upstream candidate: https://github.com/amontlabs/lcu

## Evaluation
- **Stage 1 A++**: relevant to local agent capabilities, computer use, and Human-controlled execution.
- **Stage 2 provisional A++ / CANDIDATE**: potential extension for the already-established Hermes Local Agent research; **REINFORCE** rather than NEW.
- Hermes adapter compatibility is described as experimental; actual end-to-end integration remains untested.
- **Environment dependency is a gating concern**: OS, CPU architecture, display server, desktop app version, access permissions, and upstream changes may determine viability. Prior research reported Apple Silicon macOS and selected Linux/X11 setups as supported, Windows x64 as a candidate and Intel Mac/native Wayland as unsupported. Recheck the current upstream compatibility matrix before any trial.
- Desktop interaction may expose files, credentials, browsers, and sensitive workflows. Use isolated read-only tests first, minimize permissions, explicitly gate consequential actions, and assess prompt-injection risks.
- Compare with native ChatGPT Work/Computer Use, Hermes Bot Screen, and existing Harness controls. Bot Screen (visibility/takeover) and LCU (desktop action transport) are not interchangeable.

## Relationship to Hermes
The [Hermes v0.22.2 reinforcement record](../../projects/Hermes_Local_Agent/research/2026-10-15-hermes-agent-reinforcement.md) already identifies local-first operation and Human takeover as priorities. LCU could add desktop control if the actual OS and integration permit it; this is **not evidence of an operational integration**.

## Deferred checks
1. Verify official upstream installation and support matrix for the actual target PC.
2. Confirm connector/adapter maintenance and dependency on ChatGPT desktop app versions.
3. Review license, permissions, authentication, privacy, security and applicable terms.
4. Only after separate Human approval, run an isolated pilot and measure real utility against existing tools.

## Boundary
Hermes remains Phase 0 / NOT IMPLEMENTED. This file authorizes neither installation nor workflow or policy changes.
