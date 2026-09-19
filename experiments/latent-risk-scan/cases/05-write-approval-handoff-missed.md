---
status: observation
created: 2026-09-20
origin: AI-Harness GitHub workflow
---

# GitHub Write Approval Handoff Was Missed

## What was observed

The next task had effectively become a GitHub write operation.

The AI correctly refrained from performing the write without approval.

However, it did not immediately ask for the required GitHub write approval in the same response.

The human had to point out that the approval request had not been issued.

## Why this case matters

Avoiding an unauthorized action did not complete the workflow.

The handoff from:

```text
next action identified
```

to:

```text
required approval requested
```

was missing.

## Current state

Observed in live AI-Harness operation.

No common root cause with other cases is assumed here.
