---
status: proposal
created: 2026-09-20
origin: generative UI / HARNESS UX discussion
---

# Generative UI Component Library

## Signal

Generating a complete task-specific interface from scratch each time would waste time, tokens, and implementation effort.

The more practical direction is to maintain a reusable library of verified UI components and layouts, then compose only the subset needed for the current task.

## Proposal

Create a HARNESS-side **UI Component Library / Template Registry**.

Possible reusable components:

- task / run status card
- agent status card
- Human approval card
- Git / sync status
- Usage Monitor
- test result panel
- timeline / event log
- file / artifact browser
- metrics chart
- alerts
- project-specific widgets
- child-friendly simplified views

A task would not ask an AI to invent a whole UI.

Instead:

```text
Task context
→ identify required functions
→ retrieve compatible verified components
→ compose layout
→ bind current data
→ render
```

## Component manifest

Each component may carry lightweight metadata such as:

- component ID
- purpose
- accepted input schema
- output / interaction contract
- required permissions
- dependencies
- compatibility version
- trust / verification status
- accessibility notes
- estimated runtime cost

This allows the composer to select components without reading all source files.

## External component discovery

GitHub and other open-source sources may provide candidate components, but they should not be imported directly into trusted runtime.

Preferred flow:

```text
discover
→ license / dependency / security check
→ adapt
→ test
→ pin version or hash
→ add to trusted local registry
```

External code is a candidate source, not a trusted component by default.

## Storage principle

Cloud storage capacity is unlikely to be the main bottleneck for ordinary UI components.

More likely constraints are:

- component discovery and curation
- dependency conflicts
- framework / version compatibility
- security and supply-chain risk
- duplicated components
- stale or abandoned dependencies
- context cost if too much code is given to an AI at once

Use lazy loading and manifests so only the relevant component metadata and code enter the active context.

## Local-first direction

Prefer storing the trusted registry locally or in the AI-Harness repository where practical.

Large external assets may remain referenced or cached separately.

The key optimization is not to store everything, but to know **what exists, what is trusted, and when to retrieve it**.

## Why preserve this proposal

A verified component registry could make generative UI fast and inexpensive while preserving consistency, safety, and a recognizable HARNESS identity.
