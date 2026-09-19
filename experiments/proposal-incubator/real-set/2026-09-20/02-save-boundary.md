---
status: proposal
created: 2026-09-20
origin: feather-trigger
---

# Save Boundary

The collaboration should keep planning, attempted modification, successful write, and durable save as distinct states.

A user should not need to ask repeatedly whether something was actually saved. The system should avoid saying “saved” when it only prepared content or initiated a write.

This proposal is about separating discussion from durable state.
