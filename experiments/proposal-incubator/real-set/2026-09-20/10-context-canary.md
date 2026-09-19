---
status: proposal
created: 2026-09-20
origin: experiment-design
---

# Context Canary

A small, deliberately changeable marker can reveal whether an AI actually refreshed project state.

Instead of asking broad questions, a test can update a known value and then observe whether the model reports the new or stale version after a resume boundary.

This proposal is about making context freshness observable with a low-cost probe.
