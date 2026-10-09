---
status: proposal
created: 2026-10-09
origin: Human discovery / PiDurableKit review
tags:
  - durable-runtime
  - iphone
  - temporal-spine
  - mobile-agent
  - checkpoint
  - resume
  - human-gate
  - runtime
  - ground-station
  - pidurablekit
trigger_topics:
  - pidurablekit
  - iphone-runtime
  - temporal-runtime
  - temporal-spine
  - durable-agent
  - checkpoint-resume
  - mobile-ground-station
  - human-gate
  - always-carried-device
---

# PiDurableKit — iPhone Durable Runtime / Temporal Spine Candidate

## Purpose

Preserve PiDurableKit as a serious future candidate for the **runtime / temporal / durable-state layer** of AI-Harness.

This is not an adoption decision.

The important discovery is not merely that an AI agent can run on iPhone. The more relevant architectural point is that PiDurableKit provides a durable agent runtime on Apple devices with persisted task state, checkpoints, restart recovery, transactions, hooks, tool execution, typed documents, and model-provider abstraction.

This maps closely to a long-standing AI-Harness question:

> **Where should the Harness hold time, task continuity, resumable state, and Human-gated execution when no always-on home server exists?**

A plausible answer is:

> **The always-carried iPhone can act as a durable runtime / temporal spine, while GitHub keeps durable knowledge, cloud models provide intelligence, and the Human retains authority.**

---

## Source

Repository:

- https://github.com/finnvoor/PiDurableKit

PiDurableKit describes itself as a durable AI-agent framework for iPhone, iPad, Mac, and Vision Pro, powered by `@earendil-works/pi-durable` running in JavaScriptCore.

The reviewed repository exposes a Swift API and includes:

- SQLite / JSONL persistence
- crash / restart recovery
- durable tasks
- phases / checkpoints
- child tasks and subagents
- atomic transactions
- typed documents and entries
- hooks and tool wrappers
- task graph / inspect / event streams
- sandboxed read / write / edit tools
- model-provider abstraction
- OAuth sign-in support for several providers
- a PiChat iPhone example
- background-processing support in the example app
- a Shortcuts bridge in the example app

---

## Key architectural observation

PiDurableKit does **not** rely on an iPhone app process staying alive forever.

Its durability model is more important:

```text
work starts
    ↓
conversation / tool / task state is persisted
    ↓
iOS may suspend or terminate the app
    ↓
state remains durable
    ↓
next launch / allowed runtime window
    ↓
unfinished work resumes
```

This is a better fit for iOS than trying to force a permanently running background process.

The design principle is:

> **Do not require uninterrupted execution. Require interruption-safe execution.**

That principle is highly relevant to AI-Harness.

---

## Why this matters for the current Human environment

Current operating assumption:

- the home PC is not intended to be an always-on server
- the PC is normally available only when the Human is at home and chooses to use it
- the iPhone is carried and powered nearly continuously in normal life

This changes the natural runtime placement.

Instead of:

```text
PC = always-on control server
iPhone = remote UI
```

a more natural candidate architecture is:

```text
iPhone = durable controller / runtime / Human interface
PC     = optional worker / compute node
Cloud AI = reasoning / model capability
GitHub = durable knowledge / Source of Truth
Human  = authority
```

The iPhone becomes the continuity anchor rather than merely a chat screen.

---

## Mapping to AI-Harness needs

| AI-Harness need | PiDurableKit mechanism |
|---|---|
| Durable task state | durable tasks |
| Resume after interruption | `harness.resume()` / reopen recovery |
| Checkpointed execution | task phases / checkpoints |
| Duplicate-submission protection | request IDs |
| Structured runtime state | typed Documents |
| Task-local state | task-scoped documents |
| Rewindable state history | document history |
| State migration | version / migrate |
| Child work | child tasks / subagents |
| Atomic state transitions | transactions |
| Human approval hooks | before-tool hooks / allow-block pattern |
| Runtime observability | task graph / inspect / event streams |
| Tool boundary | Tool / Hook / Wrap |
| Sandboxed files | directory execution environment |
| Model replaceability | multiple providers / custom providers |

This makes PiDurableKit unusually close to the runtime concerns already discovered through AI-Harness incidents and Lessons.

---

## Relation to the Harness temporal model

AI-Harness has already accumulated several time- and continuity-related concepts:

- Context Freshness
- Resume Boundary
- Task State
- Checkpoint / resume
- CURRENT / SUPERSEDED state
- Lesson lifecycle
- TRINITY pause / resume
- Temporal Context proposals
- runtime-enforcement concerns

These pieces exist, but they are not yet unified by one runtime that owns durable transitions.

Candidate temporal model:

```text
Schedule / Event / Human input / Tool result
                  ↓
           durable Task ID
                  ↓
            Current State
                  ↓
             Checkpoint
                  ↓
      next permitted transition
                  ↓
         execute / wait / stop
                  ↓
              Evidence
```

PiDurableKit may be useful as the Apple-device runtime underneath such a model.

---

## Candidate role: Temporal Spine

The iPhone runtime should not become the source of policy truth or final authority.

A narrow candidate role is:

```text
Temporal Spine responsibilities
- know which task exists
- know its current phase
- know what event can wake or advance it
- know whether it is waiting for Human input
- resume from a durable checkpoint
- preserve evidence of transitions
```

It should **not** independently redefine:

- Core policy
- Human authority
- Source of Truth
- approval requirements
- protected boundaries
- final semantic judgment

Those remain Harness responsibilities.

---

## Human Gate advantage

An iPhone runtime has a structural advantage because the Human is physically close to it.

Candidate pattern:

```text
Agent requests protected action
        ↓
runtime reaches Human Gate
        ↓
iPhone UI / notification presents:
- requested action
- relevant evidence
- requested decision
        ↓
Human approves / denies
        ↓
durable task resumes or stops
```

This is especially attractive for:

- GitHub writes
- Core / Harness changes
- irreversible actions
- sensitive tool use
- actions requiring explicit Human judgment

The Human should not have to visit a server dashboard just to release a blocked task.

---

## Optional PC worker model

The home PC should not be forced into the role of always-on coordinator.

Candidate model:

```text
PC offline
→ iPhone preserves task state and continuity

PC becomes available
→ runtime marks PC worker as available
→ heavy / local / GPU / filesystem work may be delegated
→ result returns to durable task state
→ task continues or returns to Human Gate
```

This keeps the runtime topology aligned with actual use rather than forcing infrastructure that does not fit the Human's daily environment.

A future local GPU machine could join the same pattern without becoming the authority layer.

---

## Ground Station interpretation

This suggests a refinement of the existing Ground Station idea.

Possible role split:

```text
Human
  = Authority

GitHub / Harness
  = Durable Knowledge / Policy / Source of Truth

iPhone + PiDurableKit-like runtime
  = Ground Station / Durable Runtime / Task Continuity

ChatGPT / Claude / other models
  = Replaceable Intelligence

Home PC / local GPU
  = Optional Compute / Execution Worker
```

This is more modular than treating the local PC itself as the permanent center of the system.

---

## Background execution caveat

Do not interpret PiDurableKit as proof that arbitrary agents can run continuously on iPhone 24/7.

The reviewed PiChat example uses Apple's background-processing facilities to keep a requested reply running after the user leaves the app, but the implementation explicitly treats the background allowance as temporary execution time.

If iOS ends the background task:

- committed work remains durable
- the current run can continue on a later foreground / relaunch
- durability comes from persistence and resume, not from guaranteed permanent execution

This distinction is essential.

---

## Shortcuts bridge

The PiChat example includes a Shortcuts bridge.

The agent can call only Shortcuts that the user explicitly allows.

Conceptually:

```text
Agent tool
    ↓
allowed shortcut check
    ↓
iOS Shortcuts
    ↓
device / app action
    ↓
result returned to agent
```

This makes the iPhone not only a runtime host but a potential bounded device-side tool executor.

This is potentially relevant to:

- personal automation
- Human-facing notifications
- local device actions
- family / Ground Station workflows

It requires separate safety and permission review before adoption.

---

## Provider and OAuth note

PiDurableKit supports multiple model providers and custom providers.

The repository also documents OAuth sign-in paths including ChatGPT and Claude subscriptions.

Do **not** infer from this that a consumer subscription can automatically be used as a free or unrestricted replacement for API billing.

The repository itself warns that third-party subscription use may have provider-specific permission or billing conditions.

Any real integration must verify:

- provider terms
- allowed third-party OAuth use
- billing behavior
- token handling
- production restrictions

Treat OAuth support as a technical capability, not as permission or cost proof.

---

## Why this is more relevant than a generic Agent OS candidate

PiDurableKit is notable because it fits several constraints simultaneously:

1. Apple-device native
2. durable state
3. interruption-safe resume
4. typed task state
5. checkpoints
6. tool hooks
7. Human-gate-compatible control points
8. replaceable model providers
9. optional local file sandbox
10. direct alignment with an always-carried device

For the current Human environment, this may be a more natural runtime substrate than introducing a server-first orchestrator merely because server frameworks are more common.

---

## Relationship to existing AI-Harness work

This proposal is strongly related to:

- LESSON-005 — Context / resume continuity
- LESSON-009 — Runtime Activation Is Distinct from Rule Existence
- LESSON-013 — Declarative Rules Need Runtime Enforcement Review
- Operationalization Gap candidate
- AI-Harness Reference Architecture
- TRINITY Orchestrator V0.1
- Agent OS OSS Landscape
- Temporal Context Layer
- Rule / Access separation
- Definition of Done
- Persistence Class evaluation
- Ground Station / local-agent direction

Especially relevant pattern:

```text
Rule exists
≠
runtime owns state
≠
transition is enforced
≠
execution is observable
```

PiDurableKit appears to address part of the missing runtime side rather than adding more declarative instructions.

---

## Evaluation priority

Do not immediately adopt PiDurableKit.

Treat it as a **high-value runtime candidate requiring focused evaluation**.

Recommended evaluation order:

1. Durable task / phase / checkpoint semantics
2. SQLite persistence and restart recovery
3. typed Document state model
4. transaction behavior
5. Hook / Human Gate suitability
6. task graph / inspect / events
7. multi-day interrupted-task behavior
8. iOS background limits in real use
9. Shortcuts bridge reliability and permission safety
10. GitHub / Harness synchronization design
11. provider / OAuth terms and billing behavior
12. PC-worker handoff feasibility
13. security of credentials / local state
14. migration / upgrade behavior for long-lived tasks

---

## Current interpretation

PiDurableKit should be treated as:

```text
Not:
"an iPhone AI app"

But potentially:
"a durable mobile agent runtime that can host the temporal/state layer of AI-Harness"
```

This is the most important part of the discovery.

---

## Current status

```text
Status: HIGH-VALUE CANDIDATE
Adoption: NOT DECIDED
Core change: NONE
TRINITY change: NONE
Permission change: NONE
Runtime implementation: NONE
```

The next step, when the Harness runtime architecture is revisited, is to compare PiDurableKit against the actual minimum runtime requirements rather than against generic agent-framework feature lists.

---

## Guiding principle

> **Do not require the machine to stay alive forever. Make the task survive when the machine stops.**

For the current Human environment, the always-carried iPhone may be the most natural continuity anchor for that principle.
