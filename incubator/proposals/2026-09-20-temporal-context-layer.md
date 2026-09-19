---
status: proposal
created: 2026-09-20
origin: Feather Trigger / temporal-context discussion
---

# Temporal Context Layer

## Signal

Several time-related mechanisms are beginning to appear across AI-Harness work:

- activity gaps between user messages
- current local time
- timezone
- scheduled automation triggers
- context freshness
- time-sensitive validity of information

These are currently handled as separate concerns.

## Proposal

Preserve the possibility of a lightweight **Temporal Context Layer** that gives AI access to the minimum time signals needed for better runtime judgment.

Possible inputs may include:

```text
activity_gap
current_time
timezone
scheduled_trigger
source_freshness
```

The layer should not exist merely to collect timestamps.

Its purpose would be to support judgments such as:

- Has enough time passed that earlier context may be stale?
- Is a request relative to the current day or local time?
- Did a scheduled event or automation create the current interaction?
- Is a source still fresh enough for the current decision?
- Should a previous assumption be revalidated because time has passed?

## Existing evidence

Feather Trigger already demonstrates that a simple browser-side timestamp can produce an `activity_gap` signal without requiring a separate time API.

This means the value is not in fetching the clock itself.

The potential value is in combining temporal signals with runtime decisions.

## Important limits

Do not implement a broad temporal framework yet.

Do not assume that all time-related behavior should be centralized.

Do not add infrastructure simply because the concept is neat.

This proposal should remain dormant unless repeated real cases show that multiple temporal problems are being solved separately and would benefit from one shared mechanism.

## Possible future relation

This proposal may later connect to:

- Context Freshness
- Feather Trigger
- Runtime Activation
- Memory Routing
- automation wake-up signals
- temporal knowledge / obsolete-state handling

These are candidate relationships only.

## Why preserve this proposal

The individual mechanisms are currently simple enough to handle separately.

However, if several of them converge later, preserving the shared idea now may prevent rediscovering the same structure from scratch.
