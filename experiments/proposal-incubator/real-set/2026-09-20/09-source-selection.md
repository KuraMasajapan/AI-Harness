---
status: proposal
created: 2026-09-20
origin: feather-trigger
---

# Source Selection

Reacquiring context is not enough if the AI chooses the wrong source.

When multiple files contain plausible state, the system should identify the actual Source of Truth rather than merely reading the most obvious or most recently mentioned document.

This proposal is about selecting the correct durable state under ambiguity.
