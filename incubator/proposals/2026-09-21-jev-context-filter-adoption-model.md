---
status: proposal
created: 2026-09-21
origin: Jev context-filter review
tags:
  - jev
  - context-management
  - context-filter
  - cost-optimization
  - deferred-adoption
  - harness-router
trigger_topics:
  - context-bloat
  - token-cost
  - keep-drop
  - context-filter
  - trinity
  - duplicated-context
  - routing
  - memory-compression
---

# Jev Context Filter Adoption Model

## Purpose

Preserve a future operating model for using Jev as a lightweight Context Filter inside AI-Harness, while explicitly recording why adoption is deferred as of 2026-09-21.

This proposal does **not** adopt Jev now.
It keeps both the intended operating model and the current non-adoption reasons together so the decision can be revisited when conditions change.

---

## Operating model

Use Jev as a bounded classification layer rather than as the system of record.

Concept:

```text
Context
  ↓
[ Context Filter ]
  ↓
AI / Agent
```

The Context Filter interface should remain replaceable:

```text
Context Filter
  ├─ none
  ├─ deterministic rules
  ├─ local model
  └─ Jev
```

Jev is therefore treated as one implementation candidate, not as a hard dependency.

---

## Protected Context

The following classes of information must not be delegated to Jev for KEEP / DROP authority:

- RULES
- Source of Truth
- CURRENT decisions or state
- accepted decisions
- sealed artifacts
- explicit prohibitions
- validation evidence required for audit or reproducibility

These remain protected and are retained by rule.

---

## Disposable Context

Jev may be evaluated only on context that has already been classified as disposable or compressible, for example:

- duplicate tool output
- repeated reads of the same source
- failed exploratory attempts that are no longer needed
- temporary notes
- superseded intermediate search results
- duplicated context fragments
- large transient tool results after required evidence has been preserved

For this pool, Jev can perform lightweight KEEP / DROP classification without rewriting the retained text.

---

## Why KEEP / DROP is attractive

Traditional summarization can alter wording, omit constraints, or collapse distinctions that matter later.

The desired pattern is instead:

```text
candidate context
   ↓
KEEP / DROP classification
   ↓
KEEP → preserve original text
DROP → remove from active context
```

The goal is context reduction without transforming the surviving evidence.

---

## Possible future role in HarnessRouter

If evaluation is positive, Jev may also be considered for small routing or classification decisions such as:

- which context fragment is relevant
- whether a fragment is duplicate
- whether a lightweight task can remain local
- whether escalation to a stronger model is warranted
- coarse task classification before invoking a more expensive model

This should remain a bounded first-pass role.
Final authority for protected state, permission, safety, or irreversible decisions must stay outside Jev.

---

## Adapter requirement

Any future integration should be removable.

Recommended shape:

```text
Jev Adapter
  ├─ enabled = true / false
  └─ fallback = deterministic rules or existing Harness path
```

AI-Harness must continue functioning when Jev is unavailable, disabled, rate-limited, repriced, or discontinued.

---

## Current decision — defer adoption

As of 2026-09-21, do not integrate Jev into the active AI-Harness path.

Reasons:

1. The current ecosystem is still small enough that context volume is not yet a material operational bottleneck.
2. The expected token savings do not yet clearly exceed the engineering, monitoring, fallback, and maintenance cost of an additional external dependency.
3. Jev is still new enough that pricing, free-credit policy, API stability, service continuity, and long-term operating conditions are not yet sufficiently established.
4. The currently observed free usage appears promotional rather than a clearly established perpetual free tier.
5. Adding an external service now would increase architectural surface area before there is a demonstrated need.
6. The same Context Filter interface can be prepared without choosing Jev now, preserving future optionality.

This is a defer decision, not a rejection.

---

## Re-evaluation triggers

Recall this proposal when one or more of the following becomes true:

- active context regularly becomes large enough to degrade cost or usability
- TRINITY creates substantial duplicated context across A / B / C
- repeated MCP or tool outputs become a major share of context
- multiple models repeatedly receive the same large context payloads
- token cost becomes a measurable constraint
- current rule-based filtering becomes burdensome
- Jev pricing and free-tier policy become stable and clearly documented
- Jev demonstrates reliable uptime and API stability over time
- a comparable alternative offers the same KEEP / DROP role with better cost, privacy, or stability

---

## Adoption test before production use

If a trigger fires, evaluate Jev in isolation before connecting it to the main Harness path.

Minimum test set:

1. KEEP / DROP accuracy on disposable context
2. false-drop rate on important-but-non-protected information
3. duplicate-context classification
4. behavior on CURRENT vs SUPERSEDED examples
5. latency and cost under realistic Harness loads
6. service failure and fallback behavior
7. auditability of the final retained context

Only promote beyond experiment status if measured value is positive and the fallback path remains intact.

---

## Guiding principle

Do not build AI-Harness around Jev.

Build a replaceable Context Filter boundary, and let Jev earn a place behind that boundary only when the ecosystem becomes large enough that the measured benefit exceeds the dependency cost.
