---
status: proposal
created: 2026-09-20
origin: Obsidian / generative UI compatibility discussion
---

# Obsidian Compatibility Graph for HARNESS Components

## Signal

A growing HARNESS component library will eventually face a selection problem:

- many possible UI components
- multiple agent roles
- different tools
- different projects
- framework and dependency compatibility
- task-specific combinations that work well together

Searching source code alone is too expensive, while fixed hard-coded mappings are too rigid.

## Proposal

Use an Obsidian-compatible metadata and linking layer as a **compatibility graph**.

Each reusable component, role, tool, or workflow pattern can have a small Markdown note describing:

- what it does
- required inputs
- outputs
- dependencies
- permissions
- compatible components
- incompatible components
- useful project contexts
- known successful combinations
- verification / trust status

Example:

```yaml
---
component_id: usage-monitor
type: ui-component
compatible_with:
  - agent-status-card
  - human-approval-card
  - trinity-run-view
incompatible_with:
  - legacy-dashboard-v1
projects:
  - AI-Harness
verified: true
---
```

Body links may add semantic context:

```text
Works especially well with [[Agent Status Card]]
Often used in [[TRINITY Dashboard]]
Requires [[Usage Telemetry]]
Avoid with [[Legacy Dashboard v1]]
```

## Retrieval model

Use two layers:

1. explicit structured links and metadata for deterministic compatibility
2. Smart Connections / semantic similarity for candidate discovery

Semantic similarity should not automatically decide compatibility.

The preferred flow is:

```text
Task
→ retrieve explicit compatible candidates
→ expand with semantic candidates
→ filter by permissions / dependencies / trust
→ rank by task fit
→ compose UI or workflow
```

## Learning from successful combinations

When a combination repeatedly succeeds, preserve that relationship.

Examples:

- component A + component B worked well for task type X
- reviewer role + adversarial tester was useful for high-risk design
- a certain layout was easier for child-facing use
- a tool pair caused dependency conflict

This allows the graph to improve through operation without giving any single Agent persistent personal memory.

## Important limits

- Obsidian links are evidence / hints, not automatic truth.
- Do not let semantic similarity bypass security or compatibility checks.
- Keep authoritative version, hash, and verification state outside free-form prose when they matter.
- Avoid turning the graph into a heavy ontology before real use requires it.

## Why preserve this proposal

The existing Obsidian + Smart Connections setup can become more than a note browser.

It may serve as a lightweight relationship layer for selecting compatible HARNESS components, roles, tools, and workflows with very low infrastructure cost.
