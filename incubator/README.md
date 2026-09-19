# Proposal Incubator

## Purpose

The Proposal Incubator stores weak ideas, partial ideas, early hypotheses, and low-confidence improvement proposals before they are mature enough to become Lessons, Workflow changes, or Core rules.

The guiding principle is:

> Do not force structure before enough evidence exists. Store first, discover structure later.

## What belongs here

Examples:

- weak improvement ideas
- recurring friction that is not yet understood
- possible future capabilities
- partial mechanisms that may combine with other proposals later
- low-confidence hypotheses worth preserving
- ideas that are useful to remember but not ready to implement

A proposal does **not** need to justify immediate action.

Many proposals may remain dormant indefinitely.

## What does not belong here

Do not use the Incubator as a shortcut for:

- approved specifications
- Core rules
- authoritative project state
- promoted Lessons
- implementation decisions already accepted elsewhere
- sensitive or private information unsuitable for a public repository

## Storage model

Use one Markdown file per proposal.

Recommended path:

```text
incubator/proposals/YYYY-MM-DD-<slug>.md
```

Do not require an upfront category unless a category is already obvious and useful.

Prefer preserving the original problem signal and rationale over forcing a taxonomy.

## Discovery model

The Incubator is designed to work with semantic discovery tools such as Obsidian Smart Connections.

Semantic similarity is used only as a **candidate-discovery signal**.

It does not prove:

- common root cause
- correctness
- priority
- implementation readiness
- that two proposals should be merged

AI may use semantic candidates to look for:

- deeper shared structure
- contradictions
- combinable mechanisms
- repeated hidden assumptions
- higher-level abstractions

Any resulting abstraction remains provisional until evidence supports it.

## Human attention

Human attention is treated as scarce.

The AI should avoid escalating every weak proposal for review.

The preferred pattern is:

```text
weak signal
→ preserve if useful
→ discover relationships later
→ AI filters and synthesizes
→ escalate only when meaningful
```

## Escalation path

When a proposal becomes important enough to formalize, the normal path is:

```text
Incubator
→ Lesson
→ Review
→ Human Decision
→ Core / Workflow
→ Regression Test
```

Formal system changes remain human-gated.

## GitHub and Obsidian roles

- GitHub is the durable source, history, and AI-readable storage.
- Obsidian is the human-facing exploration and semantic-discovery interface.
- Smart Connections helps surface candidate relationships.
- AI-Harness interprets, synthesizes, and prioritizes.
- Human approval remains required for consequential changes.

At the current stage, GitHub proposal writes are still performed only after explicit human approval.

## Operational rule

Keep the Incubator simple.

Do not add databases, scoring systems, elaborate status workflows, or mandatory metadata unless real use demonstrates that they are necessary.
