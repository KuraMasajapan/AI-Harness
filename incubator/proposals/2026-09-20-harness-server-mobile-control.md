---
status: proposal
created: 2026-09-20
origin: mobile access / local server discussion
---

# HARNESS Server with Mobile Control UI

## Signal

Running the full Harness stack directly on a phone would make Git, files, local scripts, logs, and implementation tooling harder to manage.

The local PC is already the natural location for repository state and execution tools.

## Proposal

Use the PC as a **HARNESS Server** and the smartphone as a lightweight control terminal.

Conceptual architecture:

```text
Smartphone / browser
→ HARNESS Control UI
→ local PC / HARNESS Server
   → Orchestrator
   → temporary agents
   → ASTRA when needed
   → Git / repository
   → logs / metrics
   → local scripts
→ cloud AI services as required
```

Initial UI may be a local web application or PWA instead of a native mobile app.

## Mobile responsibilities

The phone should focus on high-value Human operations:

- submit task
- view current task / run
- see active roles
- review short summaries
- approve / reject Human gates
- inspect usage state
- open detailed reports when needed

## Security boundary

Remote access should not begin with direct public port exposure.

Authentication and a deliberately reviewed remote-access mechanism are required before external access is treated as safe.

## Possible relation

This may combine naturally with a Usage Monitor showing:

- current executor
- active agents
- remaining usage when observable
- reset horizon
- Human approval required
- estimated task cost
- current run state

## Why preserve this proposal

A single persistent Harness backend could let multiple personal devices act as control surfaces without duplicating repository or agent state.
