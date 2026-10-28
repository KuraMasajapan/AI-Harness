---
status: proposal
created: 2026-10-28
source: https://github.com/github/spec-kit
social_source: https://x.com/josesilesdata/status/2115005711532912643
decision: ABSORB / COMPARE HIGH
priority: HIGH
stage_1: A++
stage_2: A+
novelty: B+
relevance: A++
implementation: HOLD / NOT IMPLEMENTED
evidence_status: CONFIRMED_UPSTREAM / AI_HARNESS_APPLICATIONS_PROPOSED
tags: [spec-kit, spec-driven-development, convergence, workflow, verification, artifact-inventory, overlay, hermit, instruction-trust-boundary]
---

# GitHub Spec Kit — Process Reference and AI-HARNESS Applications

## Scope and evidence

Reviewed 2026-10-28. GitHub's official `github/spec-kit` README, integration catalog, changelog, and security policy were inspected; existing AI-HARNESS `HARNESS.md`, `core/RULES.md`, `core/WORKFLOW.md`, `core/ACCESS.md`, Hermit proposal, and industry-convergence note were compared. This is a **research and application proposal**, not adoption.

- Upstream: https://github.com/github/spec-kit
- Docs: https://github.github.io/spec-kit/
- Social post: https://x.com/josesilesdata/status/2115005711532912643
- Verified release context: CHANGELOG 1.2.4 dated 2026-10-27; do not treat as permanently latest.
- MIT license per upstream README.
- Repository's current README describes SDD, independent bug-fixing and idea-assessment entry points, and customizable processes.
- `integrations/catalog.json` includes Codex, Claude Code, Copilot, Cursor, Gemini, Grok Build, Hermes Agent, generic bring-your-own-agent, and many others. The social post's “30+” is broadly supported, but the exact count is time-sensitive.

## What the post gets right, and what it omits

The post describes specification-first development and five commands, but the official README's current minimal SDD example includes a sixth: `/speckit-converge`. Official command spelling in that example is hyphenated (`/speckit-constitution` etc.), not the dotted spelling shown in the post. Agent-specific invocation syntax varies.

Current reference SDD:
```text
Constitution (once per project)
  -> Specify (what/why)
  -> Plan (architecture/how)
  -> Tasks (executable breakdown)
  -> Implement
  -> Converge (repeat implement/converge until 'Converged')
```

The project is no longer merely a five-command SDD template. It provides:
- Bug fixing: assess -> fix -> test; result `verified`, `partial`, or `failed`.
- Idea assessment: intake -> research -> define -> shape -> decide; `go`, `needs-clarification`, `kill`.
- Integration, Extension, runtime events/hooks, Preset, Workflow, Workflow Overlay, Workflow Step, Bundle, Catalog, authentication, project-local override, Artifact Inventory.

Upstream documentation claims these capabilities; **AI-HARNESS has not installed or independently runtime-tested them**.

## Overlap with existing AI-HARNESS

| Spec Kit concept | Existing AI-HARNESS counterpart | Assessment |
|---|---|---|
| Constitution | `HARNESS.md`, `core/RULES.md`, `core/ACCESS.md`, Human authority | STRONG OVERLAP; do not duplicate constitutional authority |
| Specify | Goal/context and project Source of Truth | OVERLAP; compare artifact clarity |
| Plan / Tasks | `core/WORKFLOW.md` Understand/Gather/Plan/Act | OVERLAP; potential project-scoped structure |
| Implement | Act + existing Codex/project tools | OVERLAP; no replacement justified |
| Converge | Verify/Correct, regression, Definition of Done | **PROMISING DELTA**: explicit, evidence-backed exit state |
| Bug assess/fix/test | Verify/Correct and project incident process | COMPARE; useful structured outcome vocabulary |
| Idea assessment | Research Stage 1/2, CANDIDATE/HOLD/REJECT | STRONG OVERLAP; preserve research-vs-implementation separation |
| Workflow overlay | Core vs Project-specific workflow | **PROMISING DELTA**: non-forked scoped customization |
| Artifact inventory | Source of Truth, provenance, instruction trust | **PROMISING DELTA**: trace exact origin/precedence of instructions |
| Catalog/bundle | Skills, proposals, approved reusable components | OPTIONAL; high supply-chain and complexity cost |

No claim is made that the existing AI-HARNESS runtime enforces all declared policies. `HARNESS.md` explicitly distinguishes declared files, activation, and observed behavior.

## Applications worth testing — proposals, not implemented

### A1. Convergence Gate / 仕様収束ゲート (HIGH)

Target: software projects such as BBB, GROWGLE, and game development.

Proposed small pilot:
```text
Approved requirement + acceptance criteria
 -> implementation
 -> tests + observable evidence
 -> compare actual result with spec
 -> CONVERGED / PARTIAL / FAILED / BLOCKED
 -> if nonconverged: scoped correction and retest
 -> Human review and delivery
```

Store a compact record: spec revision, code revision, test command/results, unresolved gaps, owner, and reason for verdict. **A model declaring “Converged” without test evidence is not a gate.** Do not confuse acceptance criteria with market performance or subjective design quality.

### A2. Project Workflow Overlay (HIGH)

Experiment with **declarative, reviewable project-specific additions** instead of cloning Core:
- BBB: replay/forward-OOS evidence and trading-risk review.
- GROWGLE: content provenance, implemented/unimplemented status, cross-category links.
- UIAPduino: hardware safety, source-locked dimensions and BOM constraints.
- Hermes Local Agent: GPU-less Phase 0 / no installation without approval.

Proposed resolution rule: Core + approved project overlay; an overlay **cannot weaken** Core, ACCESS, sandbox, Human gates, or safety restrictions. Detect conflicts and unknown precedence explicitly. Avoid a second workflow engine unless a concrete gap is demonstrated.

### A3. Instruction / Artifact Provenance Inventory (CRITICAL SECURITY COMPARISON)

Inspired by Spec Kit Artifact Inventory, and linked to the existing Instruction Trust Boundary research:
- Track artifact path, version/commit, producing layer (Core/Project/Extension/Preset/External), source/provenance, approval state, active runtime scope, and supersession.
- Distinguish **present on disk**, **loaded into agent context**, **trusted/approved**, and **technically enforced**.
- Untrusted Downloads, ZIP, external repositories, or community catalogs must not gain authority from filenames alone.
- Reject or require Human review for instruction-driven permission expansion, global agent config edits, MCP installation, sandbox bypass, or secret access.

An inventory is *visibility*, not a security sandbox. Enforce sensitive operations with permissions, sandbox, credential isolation, and independently reviewed gates.

### A4. Independent Bug-Fix Evidence Record (MEDIUM-HIGH)

For repeat regressions, standardize:
```text
symptom -> reproduction -> cause hypothesis -> scoped patch
 -> original-symptom test -> regression test -> VERIFIED / PARTIAL / FAILED
```
Use on one real bug before adding generic ceremony. If the current project already records equivalent evidence, keep existing format.

### A5. Idea Assessment Handoff (MEDIUM)

Compare Spec Kit `go / needs-clarification / kill` with AI-HARNESS `CANDIDATE / HOLD / REJECT`. They are not semantically identical: **CANDIDATE means research worth retaining, not approval to build**. Proposed handoff:
```text
Stage 1/2 research -> evidence-backed candidate
 -> explicit Human decision to experiment
 -> scoped spec and acceptance criteria
 -> implementation gate
```
Avoid automatically turning a research candidate into an executable plan.

### A6. Cross-Agent Portability (MEDIUM)

Spec Kit's integrations include Codex and Hermes Agent, relevant to the future Hermes Local Agent project. Evaluate whether a **small common specification artifact** can travel across agents without exporting credentials, expanding authority, or losing project-specific instructions. Phase 0 of Hermes remains NOT IMPLEMENTED.

### A7. Spec Kit × Hermit division of responsibilities (HIGH, CONCEPTUAL)

```text
AI-HARNESS Core (Human-controlled authority)
        |
        +-- Spec Kit patterns: define/process/verify work
        |
        +-- Hermit candidate: learn/evolve external adapter
        |
        +-- LESSON / independent evaluation / Human promotion
```

Spec Kit = **how to structure and converge tasks**; Hermit = **how to propose improving external adapter behavior**. Neither may automatically rewrite Core or approve its own privileges. Hermit-generated changes must pass fixed-path checks, independent security/evaluation, and Human review. This is an architectural analogy, not verified interoperability.

## Security and implementation cautions

- Upstream README explicitly warns community catalog listing is not an audit or endorsement. Treat catalog components as untrusted until reviewed.
- Hooks, scripts, workflow steps, extensions, and bundles can increase executable surface and dependency complexity.
- Presets are not proof of runtime enforcement. Verify the actual enforcement boundary.
- Avoid installing a complete Spec Kit workflow on top of AI-HARNESS without proving a need; risk: duplicated governance, conflicting command routing, and ambiguous Source of Truth.
- External version, integration count, commands, and behavior may change; pin and retest before any pilot.

## Smallest meaningful future experiment

1. Choose **one** software project and one bounded task.
2. Baseline existing AI-HARNESS Plan/Verify/Correct workflow.
3. Apply only a convergence-report template and provenance fields; **no Spec Kit installation initially**.
4. Compare missed acceptance criteria, rework loops, human review time, and record quality.
5. Independently verify security/authority boundaries.
6. Keep / reject the minimal pattern based on evidence; only then consider isolated Spec Kit CLI integration.

## Evaluation / Decision

- Stage 1: **A++**
- Stage 2: **A+** (upstream functionality verified from official sources; independent integration into AI-HARNESS NOT tested)
- Novelty to AI-HARNESS: **B+**
- AI-HARNESS relevance: **A++**
- Maturity of upstream: **A+** (active releases/docs; not an independent security audit)
- Security fit: **A- conditional on external enforcement**
- Decision: **ABSORB / COMPARE HIGH**
- Implementation: **HOLD / NOT IMPLEMENTED**

**Priority extraction:** Convergence Gate, Workflow Overlay, Artifact Provenance Inventory, then bug-fix verification. Research note only. No Core/TRINITY/ACCESS changes or automatic installation are authorized.

## Related AI-HARNESS notes

- `incubator/proposals/2026-10-28-hermit-harness-adapter-evolution.md`
- `research/2026-10-27-agent-harness-industry-convergence.md`
- Instruction Trust Boundary security research (locate exact current path before linking).
