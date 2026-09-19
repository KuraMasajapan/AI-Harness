---
status: proposal
created: 2026-09-20
origin: feather-trigger
---

# Visible vs Invisible Transport

A debug trigger can be injected directly into visible user text, but a mature implementation may need a transport channel that does not clutter the conversation history.

The visible version is easier to inspect and debug. An invisible version would require a separate metadata or gateway path and should only be pursued if the visible form becomes a practical problem.

This proposal is about separating debug-friendly transport from polished transport.
