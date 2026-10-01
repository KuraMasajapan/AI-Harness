---
status: proposal
created: 2026-10-02
origin: ChatGPT / AI-Harness discussion
tags:
  - agent-os
  - autonomous-agents
  - runtime
  - orchestration
  - memory
  - sandbox
  - observability
  - evaluation
  - obsidian
trigger_topics:
  - agent-runtime
  - workflow-automation
  - repeated-codex-routine
  - long-running-agent
  - checkpoint-resume
  - sandboxed-execution
  - agent-observability
  - temporal-memory
---

# Agent OS OSS Landscape — Hold for Future Runtimeization

## Purpose

Preserve the current understanding of a group of open-source projects that can turn a strong model into a more autonomous agent system.

This is a knowledge note, not an implementation decision.

Current Human decision:

```text
Keep the present operating loop:
ChatGPT → Codex → Human
```

Do not add a new orchestration/runtime layer now.

Revisit only when repeated work becomes sufficiently routine that manual handoff and checkpoint management create real friction.

---

## Core architecture pattern

The observed ecosystem can be summarized as:

```text
model
→ context
→ planner
→ memory
→ tools
→ execution
→ evaluation
→ retry
```

For AI-Harness, this should be interpreted more conservatively as:

```text
model
→ context
→ planner
→ memory
→ tools
→ execution
→ evidence
→ evaluation
→ policy / gate
   ├─ accept
   ├─ retry
   └─ Human review
```

Reason:

A retry loop without an independent gate can amplify a wrong judgment instead of correcting it.

---

## OSS map

### 1. LangGraph
Repository:
https://github.com/langchain-ai/langgraph

Role:
- stateful orchestration
- checkpoints
- pause / resume
- long-running workflows
- Human-in-the-loop

Potential HARNESS fit:
Strongest future candidate when the current ChatGPT → Codex → Human loop becomes repetitive and runtime state needs to persist automatically.

Current status:
```text
HOLD — strongest future runtime candidate
```

Do not adopt while Git + Checkpoint + Human approval remain sufficient.

---

### 2. PydanticAI
Repository:
https://github.com/pydantic/pydantic-ai

Role:
- typed agents
- structured outputs
- tool schemas
- validation

Potential HARNESS fit:
Useful where agent-to-agent or task-to-validator handoffs require strict machine-readable contracts.

Current status:
```text
REFERENCE — no current need
```

---

### 3. Mastra
Repository:
https://github.com/mastra-ai/mastra

Role:
- agents
- workflows
- memory
- broader agent framework

Potential HARNESS fit:
Overlaps heavily with existing Harness concepts.

Current status:
```text
REFERENCE — avoid duplicate control layer for now
```

---

### 4. Agno
Repository:
https://github.com/agno-agi/agno

Role:
- agent systems
- teams
- workflows
- runtime / control plane

Potential HARNESS fit:
Possible future full-platform alternative, but likely too broad for the current simple-first direction.

Current status:
```text
REFERENCE — no current need
```

---

### 5. Cognee
Repository:
https://github.com/topoteretes/cognee

Role:
- transform documents, code, and conversations into persistent knowledge
- retrieval-oriented agent memory

Potential HARNESS fit:
Could become useful after the corpus becomes too large for direct Markdown-first recall and manual structure.

Current status:
```text
HOLD — only if knowledge volume becomes a real retrieval problem
```

---

### 6. Graphiti
Repository:
https://github.com/getzep/graphiti

Role:
- temporal knowledge graph
- knowledge that changes over time
- validity periods and changing facts

Potential HARNESS fit:
Especially relevant to:
- CURRENT / SUPERSEDED
- rule evolution
- changing project facts
- time-aware memory

Current status:
```text
HOLD — conceptually strong, but do not create a second Source of Truth yet
```

Git/Markdown remains preferable while it is still readable and sufficient.

---

### 7. Browser Use
Repository:
https://github.com/browser-use/browser-use

Role:
- browser control by AI agents

Potential HARNESS fit:
Low immediate value because browser-operation capability already exists elsewhere in the current tool stack.

Current status:
```text
REFERENCE — no current need
```

---

### 8. E2B
Repository:
https://github.com/e2b-dev/E2B

Role:
- isolated execution environments
- sandboxed code execution

Potential HARNESS fit:
Important if a future autonomous agent generates and executes code without direct Human oversight.

Current status:
```text
HOLD — adopt when autonomous execution risk becomes real
```

---

### 9. Langfuse
Repository:
https://github.com/langfuse/langfuse

Role:
- traces
- observability
- LLM/tool execution visibility
- evaluation support
- token / latency / failure analysis

Potential HARNESS fit:
Useful when task volume becomes large enough that Git history, checkpoints, and conversation records are no longer sufficient to understand agent behavior.

Current status:
```text
HOLD — adopt when agent execution volume becomes difficult to inspect manually
```

---

### 10. DeepEval
Repository:
https://github.com/confident-ai/deepeval

Role:
- agent evaluation
- end-to-end and trajectory testing

Potential HARNESS fit:
Conceptually overlaps with Trinity / validation work.

Current status:
```text
REFERENCE — do not duplicate current validation machinery without a measured gap
```

---

## Current shortlist

Only four projects should remain active future candidates:

```text
1. LangGraph
   Future state / checkpoint / Human-gate runtime

2. E2B
   Safe isolated execution

3. Langfuse
   Trace / audit / observability

4. Graphiti
   Temporal memory / CURRENT-SUPERSEDED evolution
```

The remaining six are reference technologies, not active adoption candidates.

---

## Current operating decision

Do not change the present workflow.

```text
Human owns the complete product intent
        ↓
ChatGPT helps structure / reason
        ↓
Codex implements
        ↓
Human reviews and decides
```

This is especially important for current game development because the complete specification still exists partly in the Human's head.

Automation should not infer missing intent merely to remove Human involvement.

Operating principle:

```text
Exploration stays Human-led.
Routine work becomes automation candidates.
```

---

## Adoption triggers

Revisit this note when one or more of these become true:

- the same ChatGPT → Codex → Human sequence repeats many times with little variation
- restarting from checkpoints becomes repetitive overhead
- a task should pause for hours or days and resume automatically
- autonomous code execution begins
- manual execution traces are no longer enough
- CURRENT / SUPERSEDED relations become difficult to manage in Markdown
- the Harness corpus becomes too large for practical recall
- Human approval remains required, but orchestration around it has become routine

Then:

```text
friction appears
→ identify the exact gap
→ match one candidate
→ run a minimal test
→ Human approval
→ adopt only if measured value is positive
```

---

## Safety gaps not solved by these ten projects alone

Even a combined agent stack still needs explicit treatment of:

- secrets management
- fine-grained permissions
- rate limits
- cost ceilings
- rollback
- kill switch
- identity
- tool risk classification
- independent evidence / validation boundaries

Therefore these projects should be treated as runtime components, not as a complete safe-agent operating system.

---

## Obsidian role

This note is intentionally stored in the AI-Harness Incubator so that the existing path can expose it to Obsidian:

```text
GitHub development
→ local AI-Harness clone
→ Obsidian Vault
→ Obsidian Git auto-pull
→ Smart Connections semantic discovery
```

The goal is not immediate adoption.

The goal is to make these technologies recallable when a future HARNESS problem matches one of their strengths.
