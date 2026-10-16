# BBB Checkpoint — v0.9.37 Holdout Evidence Boundary Audit

Date: 2026-10-16 (JST)
Status: Release packaged and test-verified; Windows user acceptance pending.
Repository branch: main.
Source-of-Truth caution: Code release is distributed as a Full ZIP, **not** committed to GitHub by this checkpoint.
Human intent: Progress without expanding nonessential features; assistant may save durable checkpoints at discretion. Live trading remains human-gated.

## Strategic direction reaffirmed

Project aim: a safe, low-maintenance bitbank BTC/JPY spot research bot that can determine whether a genuinely executable net-of-cost strategy exists before risking actual funds. Separate deterministic baseline, experimental Shadow, Forward evidence, account/exchange execution reality, and future AI news classification.

The scope was drifting toward breadth of validation features rather than provable economic advantage. New priority:
1. Phase A: evidence/data boundary correctness, reproducibility, reliable source-of-truth (this release addresses the holdout boundary only).
2. Phase B: small, controlled net-of-cost strategy experiments; no blind parameter/strategy proliferation.
3. Phase C: proven candidates get order-book, actual costs, Paper execution/reconciliation checks.
4. Phase D: real funds only after safety/execution/forward gates and explicit Human authorization.

## Current release

- v0.9.37 — **Historical Holdout Evidence Boundary Audit**
- Full ZIP: `BBB_v0.9.37_HOLDOUT_EVIDENCE_BOUNDARY_AUDIT_FULL.zip`
- SHA-256: `d040a5229741a3d28d3163286fd47188ef8d197c43ec06a4d05d8500c07ac883`
- Build check: 276/276 pytest PASS on source; extraction regression: 11 new/integration + 265 existing = 276/276 PASS; compileall PASS; inline UI JavaScript `node --check` PASS; ZIP archive integrity PASS.
- Windows target user acceptance has NOT been performed. This checkpoint is not proof of live functionality.
- Preserve `data`, `config.json`, and `.venv_local_ai` during Full ZIP overlay. No secrets attached or saved in GitHub.

### Implemented work

The v0.9.36 Shadow Cost-Aware Buffer Lab still evaluates the same five predeclared Mean Reversion conditions with next-open execution, 80% dev/20% historic holdout, and zero/assumed/stress cost. v0.9.37 adds evidence boundary diagnostics, not trading strategy changes:

- UTC time range and Unix ms of actual held-out evaluation.
- SHA-256 of stored market CSV, and a separate fingerprint of the non-secret research settings + frozen candidate.
- Prior history scan across `data/strategy_lab/shadow/cost_buffer_lab/runs/*/report.json`.
- Overlap detection for old v0.9.36 reports using the historical holdout simulation's real start timestamp.
- `FIRST_LOCAL_EVALUATION` = no overlaps found locally, **not** global untouched proof.
- `REPEATED_HOLDOUT_EXPOSURE` = the held-out interval was evaluated before; further gains must NOT be promoted as independent evidence.
- `REVIEW_PREVIOUS_REPORT_UNREADABLE` = unresolved historical provenance, not presumed valid.
- Prior overlap/unreadable state forces this research screen to `REVIEW`, keeping old results and blockers visible.
- UI now displays the evaluation interval and overlap count; `RESEARCH_SCREEN_ONLY` no longer gets a green qualified badge.
- Reports remain under `data/strategy_lab/shadow/cost_buffer_lab/`; no Active/Forward/Paper/Live files should be mutated.

**Critical scope limit:** v0.9.37 does NOT implement a truly new post-hypothesis prospective Shadow Forward evaluation. It prevents overclaiming the historical Holdout; it does not prove an edge.

## v0.9.36 local experiment observed on 2026-10-16

Historical Shadow data: 25,919 BTC/JPY 5-min candles / coverage 100% as reported by UI.
Dev selected `entry_buffer_06` (entry z=2.6, exit z=0).

| Scenario | Frozen reference | Dev-selected buffer |
| --- | ---: | ---: |
| Dev net | -8.94% | -4.19% |
| Historical Holdout gross | +0.38% | +1.21% |
| Historical Holdout net | -2.78% | -0.72% |
| Historical Holdout stress | -5.30% | -2.25% |
| Closed trades (displayed) | 232 | 143 |
| Max DD displayed | 3.94% | 1.88% |

Dev selection reduced modeled losses but did not create positive net returns in the historical holdout. Status REVIEW, blockers: net <= 0, stress <= 0, PF < 1.10. No champion promotion. The historical holdout in that earlier run has already been exposed to Human review; it must not be called untouched prospective validation.

## Active Forward target observation (2026-10-16 21:30 JST)

- Freeze: 2026-10-08 17:20 JST
- Stage: VALIDATING; forward candles 2,354
- Strategy return +0.53%, Buy & Hold -1.04%, UI return gap +1.58pp (rounding may differ)
- Strategy DD 1.55%, B&H DD 5.75%, PF 1.50, 109 closed trades.
- Benchmark QUALIFIED_OUTPERFORM — **gross/legacy research comparison only**, not net executable qualification.
- Execution Parity: next-open gross +0.53%, public Taker reference 0.1000% per side; public Taker reference + modeled slippage -0.89%, assumed-cost -1.08%, stress -2.03%, cost drag -1.61pp. Same-semantics trade count difference 0. Parity status REVIEW.
- These are model/simulation results, not verified realized net fills. Active freeze and its outputs must not be overwritten.

## What to do next

1. Human optionally updates to v0.9.37 and checks the new Holdout evidence line. Older v0.9.36 run's archived reports are expected to be recognized on a subsequent run; do not rerun solely to seek better metrics.
2. Preserve current Active Forward observation; continue once-daily observation without tuning its frozen parameters.
3. Phase A next: consolidate release/source provenance and standardize explicit evidence tiering across existing Shadow/Forward/Parity; distinguish benchmark qualification from executable economic/operational readiness.
4. Phase B once evidence boundaries are clear: bounded time-horizon / net cost comparison, selected only from DEVELOPMENT, locked new forward after selection, not repeatedly optimized against same exposed history.
5. Live remains BLOCKED. Order-state UNKNOWN reconciliation, fees/precisions/actual fill monitoring, recovery checks, risk controls and Human authorization required before live.

## Related evidence files

- `main/projects/Bitbank_bot/CHECKPOINT_2026-10-14_v0.9.35_RESEARCH_HANDOFF.md`
- `development/projects/BBB/research/field-notes/2026-10-14-hoheto-account-audit.md`
- `development/projects/BBB/research/field-notes/2026-10-14-hoheto-execution-cost-research.md`
- `development/projects/BBB/research/field-notes/2026-10-12-grok-live-trading-lessons.md`
- `development/projects/BBB/CURRENT_SPEC.md` is older and not yet reconciled to latest binary release. This checkpoint does **not** silently promote the field notes to canonical spec.

## Safety / explicit exclusions

No automatic Champion update, no private keys, no orders, no live trades, no change to freeze or capital, and no automatic promotion. No claim the author's published trading examples demonstrate BTC/JPY edge.
