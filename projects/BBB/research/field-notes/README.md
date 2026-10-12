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


## Two-Stage Evaluation Protocol

BBB external research is evaluated in two separate stages.

### Stage 1 — Grok Intake Triage

Input:
- Grok summary
- source link
- short description
- basic metadata such as date / views when available

ChatGPT assigns a **provisional rank** based only on that limited intake:

- **A++** — exceptionally relevant; read in full next
- **A+** — strong candidate; detailed review recommended
- **A** — useful; review when time permits
- **B** — background / secondary value
- **C** — generic, weak, duplicated, or not worth deeper review

Stage 1 is only a reading-priority decision.

A high Stage 1 rank does not imply adoption.

### Stage 2 — Detailed Review / Final Research Rank

After the original article, post, repository, paper, or other detailed source is read, ChatGPT performs a fresh evaluation without being bound by the Stage 1 rank.

The Stage 2 evaluation should record:

- **Stage 1 Rank**
- **Stage 2 Final Rank**
- **Source Claim**
- **ChatGPT Evaluation**
- **BBB Relevance**
- **Principles worth retaining**
- **Parts not to import directly**
- **Evidence Status**
- **Candidate follow-up / verification**

The Stage 2 rank may move up or down.

Only the **Stage 2 detailed evaluation** is the basis for what is preserved as a substantive BBB field note.

Stage 1 may remain as compact provenance so later readers can see how the first impression changed after detailed reading.

### Storage Rule

Do not promote Stage 2 findings directly into `CURRENT_SPEC.md`, `DECISION_LOG.md`, or implementation.

The promotion path remains:

```text
Stage 1 triage
      ↓
Stage 2 detailed review
      ↓
field-notes/
      ↓
verification / reproduction
      ↓
Human approval
      ↓
BBB Source of Truth / implementation
```

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
