# BBB Checkpoint — v0.9.39 Active & Shadow Forward Observations

Recorded: 2026-10-27, JST
Evidence: user-provided screenshots of the BBB Windows research dashboard, last observation 2026-10-27 18:25 JST.
Scope: Observational research only; no strategy promotion, source modification, or live order authorization.

## Known release and frozen strategies

- v0.9.39 (Shadow Prospective Forward) remains the latest **user-observed deployed** release in this thread.
- Active mean reversion freeze **2026-10-08 17:20 JST**, lookback 79, entry_z=2.0, exit_z=0.
- Shadow prospective candidate **entry_buffer_06**, frozen independently on **2026-10-20 20:32:52 JST**. Do not refreeze/reset.
- Shadow Historical Holdout was already viewed (EXPOSED); this Shadow Forward uses only postfreeze completed candles.
- All earnings and fills shown are hypothetical model results. Live remains LOCKED; execution functions are not proven live-ready.

## Active Forward, 2026-10-27 screenshot

| Metric | 2026-10-20 | 2026-10-27 |
| --- | ---: | ---: |
| Stage | VALIDATING | VALIDATING |
| Forward 5min bars | 3482 | 5485 |
| Legacy Strategy Return | +1.37% | +0.58% |
| Same-period Buy & Hold | -1.79% | -4.34% |
| Legacy gap Strategy - B&H | +3.16 pp | +4.92 pp |
| Max DD | 1.55% | 2.15% |
| Profit Factor | 2.20 | 1.19 |
| Closed trades | 174 | 278 |
| Benchmark label | QUALIFIED_OUTPERFORM | QUALIFIED_OUTPERFORM |

- Approximately 63.5% of the target 8,640 5min candles. Calendar target is 2026-11-07 17:20 JST.
- Legacy benchmark outperform is relative risk/buy-hold observation, not executable profitability.

## Execution Parity Audit, same Active window

| Metric | 2026-10-27 |
| --- | ---: |
| Next-open (same config) | +0.52% |
| Next-open no-cost | +0.52% |
| Next-open assumed-cost | **-3.67%** |
| Next-open stressed-cost | **-6.15%** |
| Public BTC/JPY Taker fee reference | 0.1000% per side |
| Public fee + modeled 5bps/slippage per side | **-3.17%** |
| Timing gap | -0.05 pp |
| Cost drag | -4.19 pp |
| Assumed-cost PF | 0.27 |
| Assumed-cost closed trades | 271 |
| Same-configuration Forward vs Audit count delta | 0; both 278 |
| Verdict | REVIEW |

The previous public-fee reference return had been -0.99% on 2026-10-20; negative impact grew with a longer accumulating sample. The assumed-cost 271 trades and same-configuration 278 counts are distinct scenarios/counters; do not claim contradiction or equivalence without per-trade reconciliation. Real fees, spread, fill quality and slippage are not authenticated/exchange-executed data.

## Shadow Prospective Forward, first substantive out-of-sample observation

- Status **EARLY**, postfreeze new 5min bars **1990** (~7 days).
- Candidate **entry_buffer_06** unchanged.
- Baseline net **-2.24%**, candidate net **-1.59%**, difference candidate-minus-baseline **+0.65 pp**.
- Candidate stressed net **-2.41%**.
- Panel displays `prospective_net_nonpositive / stress_net_nonpositive / net_pf_below_1_10`, not qualified.
- Candidate's improved relative PnL is potentially useful **negative-loss mitigation evidence**, not proof of positive, tradable returns.
- Do not directly subtract these Shadow figures from the Active 19-day net figures; the freeze boundaries and evaluated windows differ.

## Direction and next actions

1. Keep frozen Active and Shadow strategies and boundary timestamps unchanged. One daily refresh each as needed; no 24h process requirement.
2. Do NOT repeat/tune exposed historical cost-buffer Holdout or run new Shadow tournaments to exploit this one-week evidence.
3. Next engineering focus: independently auditable **cost-driver diagnostics** (trade frequency/turnover, break-even fee or slippage, average per-roundtrip gross edge, holding duration, net edge by market regime) to identify economic viability obstacles, with same-window paired baselines and no lookahead.
4. Consider controlled next time-horizon experiments only after cost-driver data and proper locked/prospective evaluation plans; keep external Kronos/Discord/Hoheto signals as separate, unpromoted research candidates.
5. Preserve 30-day forward observation until >=8,640 candles, then assess statistical and economic gates separately. 30 days is a review checkpoint, not automatic live permission.
6. Eventual live trading requires verified production order handling, reconciliation, limits, actual fills, fee truth, risk and explicit Human approval.

## Related
- main: `projects/Bitbank_bot/CHECKPOINT_2026-10-20_v0.9.39_SHADOW_PROSPECTIVE.md`
- development: `projects/BBB/CURRENT_SPEC.md`
- development: `projects/BBB/research/field-notes/2026-10-20-kronos-candlestick-model-evaluation.md`

No user secrets, API credentials or local dataset exported.
