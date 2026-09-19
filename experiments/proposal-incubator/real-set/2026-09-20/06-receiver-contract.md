---
status: proposal
created: 2026-09-20
origin: feather-trigger
---

# Receiver Contract

A lightweight external signal is useless unless the receiving AI knows what the signal means.

For Feather Trigger, activity_gap should be interpreted as one clue that context may be stale, not as an automatic command to reacquire state. The receiver combines the signal with the current task and dependency on recent project state.

This proposal is about defining semantics for signals before judging whether a trigger works.
