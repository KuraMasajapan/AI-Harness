---
status: proposal
created: 2026-09-20
origin: cost-constrained AI-HARNESS research discussion
---

# Constraint-Driven AI Systems Research

## Signal

AI-HARNESS is developing under an explicit cost constraint.

The goal is not to maximize spending on premium agents, local hardware, or subscriptions and then seek revenue to justify that spending.

The working question is closer to:

> How much useful AI-system capability can be extracted from inexpensive, free, or already-available components before additional spending is justified?

This changes cost from a limitation into an experimental variable.

## Proposal

Treat **constraint-driven optimization** as a first-class research direction for AI-HARNESS.

The system should repeatedly test whether capability can be improved through:

- better orchestration
- better context selection
- reusable roles
- verified component reuse
- local preprocessing
- memory / retrieval structure
- semantic discovery
- deterministic automation
- workload compression
- selective use of expensive executors
- open-source components
- Human-guided design

before buying more compute or subscriptions.

## Core principle

```text
minimum additional cost
+ measured quality
+ measured reliability
+ measured human effort
→ maximum useful capability
```

The objective is not "free at all costs."

The objective is to identify the point where spending actually produces more value than structural optimization.

## External idea absorption

Public work from other users, researchers, vendors, and open-source communities is treated as a discovery pool rather than something to copy wholesale.

Preferred flow:

```text
discover
→ isolate the useful mechanism
→ understand assumptions
→ adapt to HARNESS
→ controlled test
→ measure effect
→ keep / reject / defer
```

A feature is adopted because it measurably improves the system, not because it is fashionable or complete.

## Possible differentiation

A system built under real constraints may develop strengths that are less visible in high-budget environments:

- cost awareness
- graceful degradation
- selective use of strong models
- small-component reuse
- portability
- local-first fallbacks
- transparent operating costs
- suitability for individuals and small teams

This can become an important public positioning if supported by real measurements.

## Japan-specific opportunity hypothesis

There may be a useful audience in Japan for practical, low-cost, build-it-yourself AI systems.

This is currently a hypothesis and should not be treated as established market fact.

Potential audiences to investigate include:

- individual makers
- students
- educators
- small businesses
- hobby developers
- households
- technically curious non-specialists

A future content / market study should test actual demand rather than rely on cultural assumptions.

## Research outputs

Useful public outputs may include:

- cost-per-task comparisons
- ASTRA work-compression experiments
- baseline vs optimized workflows
- free / paid component comparisons
- local-first fallback tests
- "what actually improved performance" reports
- reusable implementation patterns

## Important limits

- low cost must not justify lower security or privacy
- "cheap" should not be confused with "efficient"
- public ideas require license / security / provenance review
- cultural or market claims require evidence
- performance claims should be tied to measured tasks and conditions

## Why preserve this proposal

A long-running constraint-driven research program can turn a limitation into an accumulated design advantage.

The durable value may come from knowing which inexpensive mechanisms reliably improve capability, and which popular techniques do not.
