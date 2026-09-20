---
status: proposal
created: 2026-09-21
origin: Obsidian / independent discovery discussion
---

# Affordance-First Discovery Loop

## Signal

A recurring AI-Harness design pattern is emerging:

The project does not begin by copying a popular workflow and optimizing it.

Instead, it asks:

> What is the underlying capability of this tool that other people may be underusing?

For Obsidian, the common framing is "second brain" / personal knowledge management.

The HARNESS-oriented question became different:

- What happens if rough, heterogeneous knowledge is preserved first?
- Can later linking expose relationships that were not obvious when the notes were created?
- Can explicit links, structured metadata, semantic similarity, and execution history create a machine-usable relationship graph?
- Can that graph help select agents, tools, UI components, and workflows?

## Proposal

Preserve an **Affordance-First Discovery Loop** as a general design method:

```text
observe a tool / feature
→ identify its unique affordances
→ ignore the default usage pattern temporarily
→ form an independent hypothesis
→ build the smallest experiment
→ measure what changed
→ keep / reject / refine
→ only then compare with existing practice
```

The aim is not novelty for novelty's sake.

The value is that independent reasoning may reveal a useful role for an ordinary component before established usage patterns constrain the design.

## Relation to human "insight"

A useful analogy is:

```text
rough memories
+ delayed association
+ new context
→ unexpected connection
```

This should be treated as an analogy, not as a claim that Obsidian reproduces human cognition.

The practical test is whether delayed linking and semantic retrieval produce useful, non-obvious combinations that improve real tasks.

## Why self-discovery matters

Even if a similar idea already exists elsewhere, independently deriving it can still be valuable because it:

- exposes the assumptions behind the idea
- makes adaptation easier
- produces a testable local model
- reduces blind copying
- clarifies which parts actually matter
- creates stronger ownership of the design rationale

Novelty and usefulness are separate questions.

A concept does not need to be globally unique to be valuable inside the system.

## Important limits

- independent discovery does not prove global novelty
- semantic association does not prove causality or compatibility
- unusual framing still requires controlled testing
- external prior art should be reviewed after the local hypothesis is clear
- reject ideas that do not measurably improve capability, reliability, efficiency, auditability, or usability

## Why preserve this proposal

The distinctive value of AI-Harness may come partly from repeatedly taking ordinary tools, isolating their overlooked affordances, and recombining only the mechanisms that survive testing.
