---
status: proposal
created: 2026-10-28
decision: ABSORB / COMPARE HIGH
stage_1: A++
stage_2: A+
novelty: B+
ai_harness_relevance: A++
maturity: A+
implementation: HOLD / NOT IMPLEMENTED
evidence_status: CONFIRMED_UPSTREAM
tags:
  - spec-kit
  - spec-driven-development
  - workflow
  - convergence
  - artifact-inventory
  - workflow-overlay
  - bug-verification
  - idea-assessment
  - agent-integration
---

# GitHub Spec Kit — AI-Harness Comparison and Application Candidates

Primary source:
https://github.com/github/spec-kit

Trigger source:
https://x.com/josesilesdata/status/2115005711532912643

Reviewed version context:
- Spec Kit v1.2.4
- release date: 2026-10-27
- MIT license
- GitHub-maintained open-source project

## Summary

Spec Kit is no longer only a "write the spec before coding" tool.

Its current architecture provides reusable processes and infrastructure for:
- Spec-Driven Development
- Bug fixing
- Idea assessment
- custom processes
- multi-agent integrations
- extensions
- hooks
- presets
- workflows
- workflow overlays
- workflow steps
- bundles
- catalogs
- artifact inventory

The important AI-Harness value is therefore not adopting Spec Kit wholesale.

The useful role is:

> **Use Spec Kit as a mature external reference implementation for structured agent execution processes.**

AI-Harness already contains many of the same principles:
- Understand
- Gather
- Plan
- Act
- Verify
- Correct
- Human authority
- Project Source of Truth
- LESSON
- Promotion
- Regression
- evidence-based research

Spec Kit provides concrete mechanisms that can be compared against these existing concepts.

---

# 1. Current Spec-Driven Development flow

The simplified social-media description lists five stages, but current upstream documentation includes a sixth convergence stage:

```text
Constitution
    ↓
Specify
    ↓
Plan
    ↓
Tasks
    ↓
Implement
    ↓
Converge
    ↺
Implement / Converge until converged
```

Japanese interpretation:

```text
プロジェクト原則
    ↓
何を・なぜ作るか
    ↓
どう実現するか
    ↓
実行可能な作業へ分解
    ↓
実装
    ↓
仕様と実装の一致確認
    ↺
不一致なら修正
```

The most important concept for AI-Harness is **Converge**.

Completion is not defined by "code was written".

Completion is defined by the implementation converging on the specification.

This is closely aligned with:

```text
Act
 ↓
Verify
 ↓
Correct
 ↓
Verify again
```

in AI-Harness.

---

# 2. Current Spec Kit processes

## A. Spec-Driven Development

Purpose:
- feature / application development

Outcome:
- specification
- implementation plan
- task decomposition
- implementation
- convergence

## B. Bug fixing

Upstream flow:

```text
bug symptom
   ↓
assess cause
   ↓
scoped fix
   ↓
test original symptom
   ↓
verified / partial / failed
```

Important property:

Only `verified` represents confirmed success.

This maps strongly to AI-Harness's rule:

> Completion is not success unless the intended result has been verified.

## C. Idea assessment

Upstream flow:

```text
Intake
 ↓
Research
 ↓
Define
 ↓
Shape
 ↓
Decide
 ↓
go / needs-clarification / kill
```

This has strong conceptual overlap with the AI-Harness research process:

```text
incoming information
 ↓
Stage 1
 ↓
primary-source verification
 ↓
Stage 2
 ↓
CANDIDATE / HOLD / REJECT
```

## D. Custom process infrastructure

Spec Kit currently supports:
- Extension
- Extension runtime event
- Extension hook
- Preset
- Project-local override
- Workflow
- Workflow overlay
- Workflow step
- Bundle
- Catalog
- Authentication
- local / air-gapped sources
- Artifact Inventory

This is the area with the largest long-term comparison value.

---

# 3. Agent portability

The current upstream integration catalog includes many agent environments, including:
- Codex CLI
- Claude Code
- GitHub Copilot
- Cursor
- Gemini CLI
- Cline
- OpenCode
- Devin
- Pi
- Grok Build
- Hermes Agent
- Qwen Code
- Junie
- Kiro
- Kimi Code
- Mistral Vibe
- Antigravity
- others

A generic "bring your own agent" integration is also provided.

This supports an important architectural direction:

> Process logic should not be unnecessarily bound to one model or one agent host.

---

# 4. Direct comparison with AI-Harness

| Spec Kit | AI-Harness analogue |
|---|---|
| Constitution | RULES / Core principles / project constraints |
| Specify | Understand / requirements / project specification |
| Plan | Plan |
| Tasks | executable work decomposition |
| Implement | Act |
| Converge | Verify + Correct + Definition of Done |
| Bug assess | diagnosis / evidence gathering |
| Bug test | regression / real verification |
| Idea assessment | research Stage 1 / Stage 2 |
| Preset | reusable policy package |
| Project override | Project-specific behavior |
| Workflow | WORKFLOW |
| Workflow Overlay | Core + project-specific adaptation |
| Extension | Skill / capability extension |
| Artifact Inventory | provenance / instruction-source inspection |
| Catalog | reusable component registry |
| Integration | agent-host adapter |

The overlap is substantial.

Therefore **full adoption is not the default recommendation**.

A second full workflow layer could create duplicated governance, duplicated state, and unclear authority.

---

# 5. Application candidates for AI-Harness

## Candidate A — Convergence Gate

AI-Harness already verifies output, but software work could benefit from an explicit convergence state.

Candidate pattern:

```text
Specification
    ↓
Implementation
    ↓
Convergence Check
    ├─ requirements satisfied?
    ├─ tests pass?
    ├─ unresolved deviations?
    ├─ accepted provisional decisions?
    └─ regression clean?
          ↓
      NO → Correct
      YES → Deliver
```

Possible states:
- NOT_CONVERGED
- PARTIAL
- CONVERGED
- BLOCKED_BY_HUMAN

**Decision: ABSORB CONCEPT — HIGH VALUE**

---

## Candidate B — Workflow Overlay

Use deltas rather than copying whole workflows:

```text
Core Workflow
     ↓
Project Overlay
     ↓
Agent Overlay
     ↓
Task-specific constraints
```

Potential structure:

```text
core/WORKFLOW.md
      +
projects/<project>/WORKFLOW_OVERLAY.md
      +
agents/<agent>/OVERLAY.md
```

Benefits:
- less duplicated text
- easier upgrades
- clearer precedence
- lower drift risk

Caution:
- origin and authority must remain visible
- no silent instruction precedence

**Decision: CANDIDATE / DESIGN STUDY**

---

## Candidate C — Artifact Inventory

Instruction Trust Boundary research showed that recognized instruction files can become execution paths.

As AI-Harness gains Skills, Agent instructions, project overlays, external research, and generated configuration, it becomes increasingly important to know where active behavior came from.

Candidate inventory fields:

```text
Artifact
Source
Authority
Trust class
Scope
Persistence
Override priority
Last Human approval
```

Example:

| Artifact | Source | Trust | Scope |
|---|---|---|---|
| RULES.md | AI-Harness Core | TRUSTED | global |
| Project rule | project Source of Truth | TRUSTED | project |
| external AGENTS.md | downloaded repository | UNTRUSTED | local |
| Skill candidate | incubator | CANDIDATE | experimental |

**Decision: CANDIDATE HIGH**

---

## Candidate D — Explicit Bug Verification State

For important debugging tasks:

```text
FIX_PROPOSED
FIX_APPLIED
VERIFICATION_PENDING
VERIFIED
PARTIAL
FAILED
```

This prevents:
- patch applied = fixed
- code changed = success
- agent says done = verified

**Decision: ABSORB CONCEPT**

---

## Candidate E — Research / Idea Assessment Comparison

Spec Kit:

```text
Intake → Research → Define → Shape → Decide
```

AI-Harness:

```text
Input → Stage 1 → Verify → Stage 2 → CANDIDATE/HOLD/REJECT
```

Possible lessons:
- preserve an explicit intake artifact
- separate definition from shaping
- allow "stop with documented reason" as a valid successful outcome
- retain unresolved unknowns rather than forcing a decision

**Decision: REFERENCE / MINOR ABSORPTION**

---

## Candidate F — Process as a Portable Asset

Reusable operational processes can be modeled independently from a specific agent:

```text
Process
  ├─ inputs
  ├─ steps
  ├─ gates
  ├─ outputs
  ├─ evidence requirements
  └─ host adapters
```

Then the same process can target Codex, Claude Code, Hermes, or future local agents.

This becomes especially relevant alongside Hermit.

Spec Kit represents **how work should be executed**.

Hermit represents **how an external harness layer can improve from experience**.

Long-term conceptual combination:

```text
AI-HARNESS Core
       │
       ├── Process layer
       │      └─ Spec Kit-like structured workflow
       │
       └── Evolution layer
              └─ Hermit-like adapter learning
```

Human authority remains above both.

**Decision: LONG-TERM ARCHITECTURE CANDIDATE**

---

# 6. Spec Kit + Hermit conceptual relationship

These should not be treated as competitors.

## Spec Kit

Primary question:

> How should the agent perform work?

Focus:
- specification
- process
- task structure
- quality gates
- convergence
- workflow portability

## Hermit

Primary question:

> How should an external harness improve from experience?

Focus:
- trajectories
- feedback
- Evolver
- adapter updates
- versioning
- evaluation

Combined conceptual architecture:

```text
                Human Authority
                      │
               AI-HARNESS Core
                      │
        ┌─────────────┴─────────────┐
        │                           │
Process / Execution            Evolution Lab
        │                           │
Spec Kit-like                  Hermit-like
workflow                       adapter learning
        │                           │
        └─────────────┬─────────────┘
                      ↓
                    Agent
```

Neither process automation nor evolution automation receives authority to rewrite Core autonomously.

---

# 7. Security implications

Spec Kit explicitly warns that community catalog presence is not an audit or endorsement.

Therefore:

```text
Catalog entry
    ≠
Trusted component
```

This aligns with AI-Harness Instruction Trust Boundary:

```text
Instruction exists
    ≠
Instruction is trusted
```

Candidate rule:

> Catalogs improve discoverability, not trust.

External extensions, presets, workflows, bundles, and hooks should remain untrusted until reviewed.

Workflow overlays also require visible provenance to avoid hidden instruction precedence.

---

# 8. Evaluation

**Stage 1: A++**

**Stage 2: A+**

**AI-Harness relevance: A++**

**Novelty: B+**

The lower novelty score is intentional. Much of the philosophy already exists inside AI-Harness.

The value is in:
- mature implementation patterns
- process packaging
- convergence
- workflow overlay
- artifact inventory
- broad host portability
- external validation of the architectural direction

**Maturity: A+**

**Implementation quality: A**

**Security fit: A-**

## Decision

**ABSORB / COMPARE HIGH**

Do not install or merge Spec Kit into AI-Harness from this note alone.

Do not create a second authoritative workflow layer.

Use Spec Kit primarily as:
1. a reference architecture,
2. a comparison target,
3. a source of selected mechanisms.

---

# 9. Priority application order

1. **Artifact Inventory**
   - directly supports Instruction Trust Boundary
2. **Convergence Gate**
   - strengthens Definition of Done / Verify
3. **Workflow Overlay**
   - useful for Core → Project → Agent hierarchy
4. **Explicit Bug Verification States**
   - low-cost reliability gain
5. **Process portability**
   - useful for Codex / Hermes / future agents
6. **Idea Assessment comparison**
   - mostly confirms existing AI-Harness research design

---

# 10. Final architectural interpretation

Spec Kit should not replace AI-Harness.

```text
AI-HARNESS
  = governance / trust / Human authority / durable learning

Spec Kit
  = mature reference for structured execution processes

Hermit
  = candidate reference for controlled external harness evolution
```

Possible long-term stack:

```text
Human
  ↓
AI-HARNESS Core
  ↓
Trust / Access / Rules
  ↓
Structured Process Layer
(Spec Kit lessons)
  ↓
Agent
  ↓
Experience
  ↓
Experimental Evolution Layer
(Hermit lessons)
  ↓
Candidate improvement
  ↓
LESSON
  ↓
Human Review
  ↓
selected promotion
```

This preserves the central AI-HARNESS principle:

> The Harness may learn from experience, but Core authority remains Human-controlled.
