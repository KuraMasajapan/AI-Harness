---
status: research_candidate
created: 2026-10-20
origin: Human-shared OpenBot v0.44.0 / v0.44.1 release announcement
decision: CANDIDATE / UI_UX_REFERENCE_ONLY
implementation: HOLD / NOT IMPLEMENTED
installation: NONE
branch: development
stage_1: A+
stage_2: A
tags:
  - openbot
  - ui
  - ux
  - human-in-the-loop
  - agent-tasks
  - browser-handoff
  - mcp-security
  - research-reference
trigger_topics:
  - OpenBot
  - agent task dashboard
  - needs you
  - human approval UI
  - agent browser handoff
  - operator console
---

# OpenBot v0.44.x — Agent-management UI/UX reference

**Human decision (2026-10-20):** Save **one research/reference note** on the `development` branch. The preferred direction is to borrow useful **UI/UX patterns** rather than adopt OpenBot's agent runtime or reproduce its architecture. Human approved this exact new-file scope after the intended path and content categories were presented.

**Research status:** Stage 1 **A+**, Stage 2 **A** (provisional AI-Harness relevance); **CANDIDATE** as UI/UX reference, **HOLD** for implementation, installation, or integration. No acceptance test, security audit, or comparison trial has been performed.

## Source and verification boundary

- Official product changelog: https://openbot.run/changelog
- Official repository: https://github.com/nightly-labs/openbot
- Versions under review: https://github.com/nightly-labs/openbot/releases/tag/v0.44.0 and https://github.com/nightly-labs/openbot/releases/tag/v0.44.1
- Related upstream documentation: https://github.com/nightly-labs/openbot/blob/v0.44.1/README.md and https://github.com/nightly-labs/openbot/blob/v0.44.1/SECURITY.md
- License text: https://github.com/nightly-labs/openbot/blob/v0.44.1/LICENSE — **PolyForm Noncommercial 1.0.0**, not an unrestricted permissive license.

The release announcements, README, and security documentation establish the *documented product design and stated security model*, **not** independent verification of safety, absence of credential leaks, agent reliability, or effectiveness in an AI-Harness workflow. The UI interpretation and proposed adaptation below are AI-Harness design inferences, not an OpenBot guarantee.

## Primary UI/UX references

| OpenBot pattern | Observed/documented interaction | Potential AI-Harness adaptation | Decision |
| --- | --- | --- | --- |
| **Tasks page** | `Needs you`, `Working`, `Waiting`, `Closed` group tasks by what the person needs to do, not by the number of agents | Operator-facing work queue with explicit pending decisions, in-progress work, blockers, completed items | **UI REFERENCE / HIGH** |
| **Agent questions** | Buttons, quick replies, choice lists, forms | Small, unambiguous Human decision cards for Trinity comparator findings or project handoffs; keep reasoning/evidence inspectable before selection | **UI REFERENCE / HIGH** |
| **Browser takeover / hand-back** | Human can take over an agent browser tab and return control after manual intervention | Optional handoff for login, site interaction, and ambiguous actions; make current operator and handoff state clear | **UX REFERENCE / HIGH** |
| **Progress and activity display** | Consolidated tasks and activity recap/status surfaces | Compact summary of waiting, active, completed tasks without forcing users to inspect each chat | **UX REFERENCE / MEDIUM** |
| **MCP credential attachment** | OpenBot handles MCP sign-in tokens on tool requests rather than providing raw tokens directly to agents; refresh/sign-out handling is documented | Useful *security design reference* only; separate token secrecy from what actions a tool is authorized to perform | **ARCHITECTURE REFERENCE / CONDITIONAL** |

### Candidate operator-console principle

Prioritize **Human attention**, not agent count. A user should see *which action needs their decision now*, with a short summary, linked evidence, consequences, current owner, and an explicit option to defer.

Possible Human decision labels include `APPROVE`, `REJECT`, `HOLD`, `REQUEST CHANGE` as a **provisional UI vocabulary only**. Do not silently reinterpret these as existing Trinity protocol states, authorization grants, or persistent Core rules.

A friendly interface does **not** itself enforce permissions. The actual write/execute gates must remain controlled by independently enforceable tool or execution boundaries, under current Human authority.

## Overlap / no-duplicate design

- `incubator/proposals/2026-09-20-generative-ui-component-library.md` already proposes task/run cards, agent cards, Human approval cards, status widgets and a verified component registry. OpenBot is a **concrete interaction reference**, not a new component framework.
- `incubator/proposals/2026-10-15-ui-design-skill-component-comparison-prep.md` covers separate UI design Skills/component sourcing and possible later UI comparisons; do not treat OpenBot as an interchangeable design Skill.
- `incubator/proposals/2026-10-16-grok-agent-permission-approval-hold.md` remains **Human-deferred**. This UI note must **not** reopen the broader permissions-gap audit, modify Core/ACCESS, or approve a third-party tool-call approval layer.
- `incubator/proposals/2026-10-18-grokbot-local-agent-task-webhook.md` already considers durable state/handoff; OpenBot's task dashboard is a presentation reference, not evidence that an execution backend has been selected.
- Future local agent study: `projects/Hermes_Local_Agent/` (no change to its current implementation status).
- Existing `core/ACCESS.md`, `core/WORKFLOW.md` and Trinity Human approval boundaries remain authoritative.

## Security, licensing, and adoption constraints

1. **Critical security difference:** The OpenBot v0.44.1 README and SECURITY.md describe a development preview in which agents operate with `danger-full-access` and `approvalPolicy: never` after first-launch consent. Agents may reach host files, commands, network and browser without per-action confirmations. This **does not meet AI-Harness's intended narrow, independently enforceable Human approval boundaries** merely because the UI provides handoff or permission labels.
2. **Credential handling:** Interposing MCP authentication tokens is useful defense-in-depth, but it does **not** constrain a tool's effective permissions or guarantee non-disclosure through other channels. Remote-provider and connected-app permissions require separate review.
3. **License:** The upstream source carries PolyForm Noncommercial 1.0.0; do not assume unrestricted commercial use, relicensing, or wholesale component reuse. Refer to UI interaction *ideas* first; review license before copying any assets or code.
4. **Complexity:** Avoid installing a second agent orchestration layer or browser framework while existing ChatGPT/Codex/Hermes research covers adjacent capabilities. UI feature adoption requires a concrete user problem and a simpler-alternative comparison.
5. **Verification gap:** No local install, security analysis, UX study or task-efficiency benchmark was run. Product behavior is documented upstream; suitability for AI-Harness is provisional.

## Narrow future check — not authorized for implementation

Only if an AI-Harness dashboard becomes an active, Human-approved project:

- Choose one actual operator workflow, for example **Trinity Human decision handoff**.
- Compare its existing text workflow with a minimal *mock* card showing `Needs you`, linked evidence and an explicit decision action.
- Measure omitted decisions, misclicks, time to resolution, readability on phone, and whether deferred items remain discoverable.
- Ensure state labels correspond to real backend status and approvals cannot be inferred merely from a click without authorized execution.
- Keep UI prototypes/design research separate from deployment and API/credential access.

**Persistence boundary:** This file records an approved external UI/UX reference only. It authorizes **no** installation, testing, runtime integration, browser control, GitHub changes beyond this one note, Core/Skills/Trinity changes, or promotion to formal specification.
