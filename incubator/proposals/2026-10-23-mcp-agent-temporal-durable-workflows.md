---
document_type: research_evaluation
date: 2026-10-23
title: "mcp-agent + Temporal — Durable Agent Workflow Candidate"
source_repository: "https://github.com/lastmile-ai/mcp-agent"
discovery_source: "Grok Observer"
decision: CANDIDATE
implementation: HOLD
stage_1_rank: A
stage_2_rank: A
evidence_status: "OFFICIAL REPOSITORY VERIFIED; LOCAL FIT UNTESTED"
tags:
  - mcp
  - temporal
  - durable-execution
  - orchestration
  - hitl
  - workflow
  - agent-runtime
---

# mcp-agent + Temporal — Durable Agent Workflow Candidate

## Status

**Stage 1: A**  
**Stage 2: A**  
**Decision: CANDIDATE**  
**Implementation: HOLD**

Discovered by the Grok Observer on 2026-10-23 and independently verified against the official `lastmile-ai/mcp-agent` repository.

## 1. What it is

mcp-agent is an MCP-native Python framework for composing agents and workflows.

The important feature for AI-Harness is its support for **durable execution through Temporal**.

Conceptually:

```text
agent task starts
      ↓
workflow state persists
      ↓
failure / pause / Human wait / restart
      ↓
workflow resumes
```

This is different from ordinary in-memory asyncio execution where a process crash may require restarting the task.

## 2. Officially confirmed capabilities

The project documents:

- MCP-native agents,
- routing,
- parallel/map-reduce,
- orchestrator-worker patterns,
- evaluator-optimizer patterns,
- full MCP client/server support,
- structured logging,
- token accounting,
- Temporal-backed durable execution,
- long-running workflows,
- retries,
- pause/resume patterns,
- signals and Human input,
- cloud deployment options.

The same application-level workflow can use different execution backends.

## 3. Why it matters to AI-Harness

This is relevant to future workloads such as:

- long-running research,
- scheduled jobs,
- multi-step agent tasks,
- Human approval pauses,
- recovery after restart,
- external-event-driven agents,
- persistent background workflows.

It is especially relevant to the architectural question:

> How should an agent continue safely when execution spans hours or days?

## 4. Relationship to existing research

This reinforces existing interest in:

- event-driven agents,
- Amazon Bedrock AgentCore-style ambient triggers,
- durable execution,
- Human-in-the-loop approvals,
- Notion's long-running agent architecture.

It also provides an OSS implementation reference for concepts that proprietary systems expose only indirectly.

## 5. Why not adopt now

Temporal is a substantial infrastructure dependency.

For current AI-Harness usage, many jobs can still be handled with:

- ordinary scripts,
- cron,
- queues,
- ChatGPT automations,
- simple local state,
- explicit restart checkpoints.

Adding Temporal too early could violate the Harness minimalism principle.

Therefore the current value is mainly architectural reference plus a future experiment candidate.

## 6. Risks and costs

- infrastructure and operational complexity,
- workflow determinism constraints,
- replay-related development complexity,
- additional services to maintain,
- distributed-system failure modes,
- harder debugging than a local sequential script,
- overengineering for small tasks.

## 7. Useful design patterns to absorb

Even without adopting Temporal, AI-Harness can learn from:

- explicit workflow state,
- resumable checkpoints,
- idempotent steps,
- retry policies,
- Human approval signals,
- clear separation between workflow definition and execution engine,
- durable audit logs.

This is likely more valuable near-term than installing the full stack.

## 8. Future experiment gate

Consider a pilot only when a real task exists that repeatedly fails because of:

- process restarts,
- waiting for Human approval,
- long-running execution,
- external-event timing,
- reliable retries.

Comparison:

```text
A: current simple workflow
B: mcp-agent asyncio
C: mcp-agent + Temporal
```

Measure:

- recovery,
- setup burden,
- runtime overhead,
- Human intervention,
- observability,
- correctness,
- maintainability.

## Decision

**A / CANDIDATE / IMPLEMENTATION HOLD**

Preserve the durable-execution patterns now.

Do not introduce Temporal infrastructure until an actual workflow justifies the added complexity.