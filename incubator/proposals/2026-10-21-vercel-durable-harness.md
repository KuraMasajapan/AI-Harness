---
document_type: research_evaluation
date: 2026-10-21
timezone: Asia/Tokyo
subject: Vercel durable-harness
stage_1_rank: A++
stage_2_rank: A++
decision: CANDIDATE
relationship: COMPARE / COMPLEMENT
implementation: NOT APPROVED
origin: Human-provided Vercel durable-harness announcement; Human approved this research-record write
branch: development
tags: [durable-execution, agents, workflow, event-log, recovery, idempotency, vercel, local-ai, trinity, hermes, human-approval]
---

# Vercel durable-harness — durable agent execution (research only)

## Research status and evidence

**A++ / CANDIDATE** means high-priority **research and controlled experimentation**, not adoption. The assessment is based on upstream documentation and repository metadata, **not** an independent runtime or security audit.

Primary sources consulted:
- Vercel announcement: https://vercel.com/blog/making-every-harness-durable
- Official repository: https://github.com/vercel-labs/durable-harness
- README: https://github.com/vercel-labs/durable-harness/blob/main/README.md
- License: https://github.com/vercel-labs/durable-harness/blob/main/LICENSE.md
- Agent harness docs: https://vercel.com/docs/agent-harnesses
- Workflow SDK: https://workflow-sdk.dev

The Human supplied an excerpt saying that Pi, OpenCode, Codex, Claude Code, eve, fx and custom harnesses can execute durably over long periods. The **current README inspected** explicitly lists Pi, OpenCode, fx, Claude Code and Codex; other harnesses/custom integrations must be checked against actual adapters and supported interfaces rather than inferred from the excerpt alone.

## Confirmed from upstream README / license (documented capability, not independently tested)

1. A session is a Workflow SDK run. Its conversation, in-flight turn, model calls and tool calls are represented in an event log, enabling restoration/replay after a crash.
2. The design distinguishes tool calls unsafe to repeat. A durable record is intended to avoid re-executing such operations twice. Real-world exactly-once external side effects still require testing and idempotency/reconciliation at system boundaries.
3. Documented integrations: Pi, OpenCode, fx, Claude Code and Codex. The README says Claude Code and Codex execute inside a session-specific **Vercel Sandbox**, not a shared function.
4. Tool-less by default; file and command tools run in a virtual workspace or a dedicated sandbox, not on the machine coordinating the session, per README.
5. Local development uses a local Workflow SDK World. Hosted deployment can use Vercel managed infrastructure; self-hosting may use Postgres World or another World implementation. Thus the concept is not inherently limited to the Vercel SaaS.
6. The repository labels the project **experimental**, at version **0.0.x**, with APIs subject to change. The repository license is **Apache-2.0**.

**Unverified**: reliability under months-long outages; precise cost; platform free-tier fit; recovery across every supported harness; secret management; external API side-effect correctness; support for Hermes; Windows/low-spec-PC deployment; compatibility with ChatGPT Plus/Codex subscription access.

## Mechanism and AI-Harness fit

Problem signal: coding/research agents may be interrupted by crashes, execution timeouts, resource limits, deployment restarts or lost sessions. Merely saving generated files does not reliably preserve **which step** of an in-flight model/tool sequence completed.

Candidate architecture:

- Agent/harness (e.g., supported coding agent)
- durable-harness + Workflow SDK run/event log
- model and tool execution in appropriately isolated workspaces
- external storage for logs and artifacts
- AI-Harness governance (Rules / Access / Human approvals / evaluation / provenance) **outside** the automatic retry mechanism.

Potential future value:
- Recover interrupted multi-stage research and coding jobs.
- Keep evidence of tool/model execution and resume boundaries for audit.
- Support long-lived delegated tasks without requiring a continuously running chat session.
- Make interrupted handoff/checkpoint behavior testable independently of any one model.
- Inform future Ground Station and Hermes experiments, without assuming Hermes integration exists today.

**Important distinction:** This is an application/runtime persistence mechanism. It does **not** bypass ChatGPT Work or Codex product usage caps, provide unlimited model tokens, or automatically resume a particular user's existing ChatGPT session.

## Compare and combine with existing concepts

| Component | Principal responsibility | Relationship |
| --- | --- | --- |
| Vercel Drives (prior research concept) | Persistent workspace files and artifacts | Complementary; file persistence is not an execution checkpoint. Verify product integration specifics before adoption. |
| durable-harness | Persisted agent turn/model/tool-call history and restart/replay semantics | Candidate execution durability layer. |
| Cloud Harness MCP (existing proposal) | Coding-workspace, shell/Git/tool surface exposed through MCP | Different problem; compare overlapping task/session functions, security, maintenance and costs. |
| AI-Harness checkpoints / Trinity | Evidence, independent evaluation, rule and approval boundaries | Preserve as separate authority; automatic retry cannot override Human approval. |
| Hermes Local Agent | Future local agent candidate | Integration **unverified**; do not change Phase 0 or install Hermes. |

Existing related proposal:
- `incubator/proposals/2026-10-20-cloud-harness-mcp.md`

## Safety and failure cases to evaluate

1. **Duplicate side effects**: interrupted Git writes, network calls, file mutations and especially financial transactions must not be blindly replayed. Check idempotency keys, external transaction IDs, confirmation and reconciliation.
2. **Authorization freshness**: Human approval must be checked before a sensitive action and remain bound to its exact scope; recovery should not silently expand permissions or reinterpret an old approval.
3. **Data and secrets**: inspect event-log content, prompt/tool-output retention, sensitive data redaction, storage encryption, access controls and deletion/retention policy.
4. **Untrusted outputs**: fetched pages, tool results and repository text are untrusted inputs; resumed agents remain exposed to prompt injection.
5. **Isolation**: virtual workspaces and sandboxes are not equivalent to a blanket security guarantee. Verify the selected adapter and its actual process/network/file access.
6. **Version drift**: a workflow resuming weeks later may encounter changed code, schemas, model behavior, credentials, dependencies or pricing.
7. **Cost**: open-source license does not make Vercel compute/storage, sandbox time, API usage or a self-hosted Postgres setup free.

BBB-specific consideration: financial order submission requires broker/exchange-side idempotency and order-state reconciliation, not just durable workflow logs. **No connection to live trading is authorized**.

## Minimal evaluation plan (proposal, not executed)

**Phase A — read-only technical review**
- Inspect adapter implementation and Workflow SDK persistence model.
- Trace what is logged, how recovery is triggered and how side-effect classification is implemented.
- Check license/dependencies, current pricing and free-tier limitations.

**Phase B — isolated reproducible trial, only after separate Human approval**
- Use a throwaway workspace and no secrets, personal files or production Git write access.
- Run a short, deterministic tool sequence; force termination mid-step; restart from saved state.
- Test repeat-safe vs repeat-unsafe dummy tool calls, including injected failures.
- Compare against a simple existing checkpoint/JSON-log alternative.
- Measure recovery accuracy, duplicate actions, elapsed time, CPU/RAM/storage and monetary cost.

**Acceptance gates**
- Demonstrated recovery with no unintended duplicate side effects.
- Traceable, Human-readable execution history.
- No approval bypass; no production access in tests.
- Quantified benefit relative to simpler checkpoints and current Work/Codex workflows.
- Reproducible setup compatible with intended resource budget.

## Decision and change boundary

- **2026-10-21 — Stage 1 A++; Stage 2 research rank A++ / CANDIDATE.** This ranking indicates unusually high architectural relevance; operational effectiveness remains **UNVERIFIED** until testing.
- Human explicitly approved saving this proposal.
- This commit is **research-record-only**. No package installation, Vercel account/deployment, agent integration, Core rule modification, Hermes Phase change, Trinity modification or BBB execution change is approved.
- Subsequent implementation or further GitHub modifications require a new scoped Human decision.
