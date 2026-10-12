# BBB Field Notes

## Purpose

This folder stores external operational lessons, failure reports, implementation anecdotes, and research signals that may be useful to BBB later.

These notes are intentionally separated from BBB's Source of Truth.

Content in this folder is **not automatically part of CURRENT_SPEC** and is **not an implementation decision**.

## Promotion Flow

```text
External signal / field report
        ↓
research/field-notes/
        ↓
Verification / reproduction / comparison
        ↓
Candidate design decision
        ↓
Human approval
        ↓
CURRENT_SPEC / DECISION_LOG / implementation
```

## Evidence Handling

Each note should distinguish:

- **Source claim** — what the external author/report says
- **BBB relevance** — why the claim may matter to BBB
- **Evidence status** — confirmed, partially verified, unverified, or anecdotal
- **Do not import directly** — article-specific thresholds, exchange-specific quirks, or code should not be copied into BBB without verification

## Current Focus

Priority topics include:

- Production / Replay / Forward parity
- execution quality and reality gap
- fees, spread, slippage, rounding
- state reconciliation
- pending orders and duplicate-order protection
- risk reject vs emergency stop
- portfolio / capital allocation
- position sizing
- promotion / demotion gates
- skip / no-trade reason logging
- market-data quality and timing granularity
- deterministic independent cross-checks
- live-trading failure catalogues

## Boundary

This folder may contain useful ideas that later prove wrong.

Do not treat presence here as endorsement.
