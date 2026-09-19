---
status: proposal
created: 2026-09-20
origin: harness-permissions
---

# Permission Gate Reality Check

An external permission prompt can be useful as a second human-approval layer, but it should never be assumed to appear reliably on every write.

The system should distinguish “a permission gate exists in principle” from “this particular action actually presented one.” Repeated observation is needed before depending on it as part of the architecture.

This proposal is about verifying the real behavior of external approval boundaries.
