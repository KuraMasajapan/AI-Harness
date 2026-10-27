---
status: research_update
created: 2026-10-27
decision: CANDIDATE / REFERENCE
implementation: HOLD
related_record: incubator/proposals/2026-10-20-openbot-ui-ux-reference.md
evidence_status: CONFIRMED_UPSTREAM
tags:
  - openbot
  - agent-workspace
  - multi-agent
  - skills
  - mobile
  - remote
  - computer-use
  - security
---

# OpenBot — Capability Update (2026-10-27)

Primary repository:
https://github.com/nightly-labs/openbot

Existing AI-Harness reference:
`incubator/proposals/2026-10-20-openbot-ui-ux-reference.md`

This note records **new capability observations** and does not replace the earlier UI/UX evaluation.

## Confirmed expanded capabilities

Current upstream documentation/code shows support for multiple agent/provider runtimes including:
- Codex
- Claude
- Grok
- Gemini
- Cursor
- Cline
- OpenCode

Additional capabilities now include or document:
- desktop and mobile clients
- self-hosted / remote server options
- Computer Use
- task / queue / team-style workflows
- agent-to-agent collaboration surfaces
- local Skill creation
- shared Skill library
- Skill revision/version handling
- import of Grok Bot agent settings, skills, routines and memories
- remote access patterns and hosted server infrastructure
- mobile approval interfaces

## Particularly relevant architecture pattern

OpenBot now has a clearer reusable-skill lifecycle:

```text
Agent discovers reusable workflow
   ↓
create_skill
   ↓
local shared skill library
   ↓
versioned revision
   ↓
install into other agents
```

This is relevant to AI-Harness / Hermes research around reusable skills and learned operating procedures.

## Security constraint remains critical

Upstream README / SECURITY.md still document the default agent runtime as:

```text
danger-full-access
approvalPolicy: never
```

Agents may access files, execute commands, use the network and control the embedded browser without per-action confirmation after initial consent.

Therefore:

- broad capability does not imply compatibility with AI-Harness authority boundaries
- mobile approval UI does not automatically mean all runtime actions are independently gated
- the runtime trust model remains materially broader than AI-Harness intends for consequential actions

## Updated assessment

Capabilities / UX: **A++ reference**
Reusable skill lifecycle: **A+ reference**
Security fit for direct adoption: **C / HOLD**
Full runtime adoption: **HOLD**

Prefer extracting:
- operator-console patterns
- task state presentation
- skill lifecycle ideas
- handoff UX
- agent collaboration concepts

Do not adopt the unrestricted runtime model without a separate enforcement-layer review.
