---
status: proposal
created: 2026-09-20
origin: feather-trigger
---

# Cross-Chat Leakage Control

A new-chat experiment can be contaminated by memory or continuity from other chats.

Tests that are meant to isolate a trigger should include controls that detect whether the model already knows the expected project state through another channel.

This proposal is about preventing hidden continuity from invalidating context-freshness experiments.
