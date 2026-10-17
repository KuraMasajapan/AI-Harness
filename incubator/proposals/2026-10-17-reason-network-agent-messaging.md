---
status: proposal
created: 2026-10-17
stage_1_rank: A+
stage_2_rank: CANDIDATE
decision: CANDIDATE
implementation: HOLD
evidence_status: OFFICIAL CLAIMS REVIEWED / INDEPENDENT PERFORMANCE UNVERIFIED
tags: [agent-messaging, p2p, multi-agent, codex, claude-code, hermes, trinity, permissions]
trigger_topics: [Reason Network, Reason Machines, agent-to-agent communication, agent discovery, peer-to-peer agents]
---

# Reason Network — Agent-to-agent messaging and collaboration

## Human decision
2026-10-17: Human explicitly approved **saving as a research candidate**. No installation, implementation, permission changes, or Core modifications approved.

## Source
- Official product page: https://reasonmachines.com/network
- Human-provided third-party promotional post (2026-10-17), treated as untrusted research input.

## Reported functionality
- Agent-to-agent direct messaging without screen-reading/click-based Computer Use.
- Claimed support for coordinating Grok Bot / Muse with Claude Code, Codex, and other agents.
- P2P communication and discovery of agents across teammates' machines.
- Shared visibility of agent/repository/branch activity to help coordinate parallel coding.
- Free network tier and open-source engine are advertised; distinguish the engine from proprietary or unpublished CLI/setup components and potential paid hosted services.

## Evidence and uncertainty
- Product capabilities are based on developer documentation/claims; no independent local testing performed.
- Performance, stability, collision prevention, P2P security, permissions enforcement, Windows compatibility, CLI auditability, licensing boundaries, and recovery behavior remain unverified.
- Discovering another agent does not grant safe authorization to execute commands or modify files on another machine.

## AI-Harness relevance
- Potential optional transport/discovery layer for HarnessRouter, Codex, Hermes Local Agent, and Trinity handoffs.
- **Not** a replacement for AI-Harness governance, Memory, Human approvals, or Trinity independence.
- Compare against existing integration methods and other agent-to-agent protocols before adoption; avoid adding a new layer without a measured need.

## Minimal future verification
1. Inspect actual engine repository, license, and install/CLI distribution details.
2. Trace authentication, peer permissions, data exposure, remote command execution, and audit logs.
3. Test only in a sandbox with non-sensitive files and no cross-user remote access.
4. Compare with existing harness workflows on latency, reliability, operational cost, and complexity.
5. Require separate Human approval before installation or implementation.

## Evaluation
Stage 1: **A+** (relevant to multi-agent coordination).
Stage 2: **CANDIDATE** (promising, not validated).
Implementation: **HOLD**.
