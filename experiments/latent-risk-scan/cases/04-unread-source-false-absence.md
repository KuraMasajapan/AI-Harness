---
status: observation
created: 2026-09-20
origin: exploratory Latent Risk Scan probe
---

# Unread Source Was Mistaken for Absence

## What was observed

A tested AI stated that controlled test results had not been stored in a durable source.

That statement was incorrect.

The results already existed in:

`experiments/latent-risk-scan/RESULTS.md`

The AI had not loaded that file.

## Why this case matters

A missing-layer search can produce a false finding when it treats:

```text
not present in current context
```

as equivalent to:

```text
verified absent from the relevant Source of Truth
```

## Current state

Observed during exploratory validation.

No common root cause with other cases is assumed here.
