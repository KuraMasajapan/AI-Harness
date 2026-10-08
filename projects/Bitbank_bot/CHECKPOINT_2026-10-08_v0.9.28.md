# Bitbank_bot Checkpoint v0.9.28

Date: 2026-10-08
Status: active research / forward validation + historical expansion

## Version
- BBB v0.9.28
- Release: Employment Forward OOS
- Update method: Full ZIP
- Patch / Delta method: not used

## Training Lab

### Research Champion
- Strategy: Mean Reversion
- Parameters:
  - lookback: 79
  - entry_z: 2.0
  - exit_z: 0.0
- Research Champion promotion was valid versus the prior EMA + RSI champion.

### Benchmark Gate
Current champion is Benchmark Qualified as:
- QUALIFIED · RISK EFFICIENT

Observed benchmark snapshot:
- Strategy Return: +1.90%
- Buy & Hold Return: +6.80%
- Return Gap: -4.89 pp
- Strategy Max DD: 1.17%
- Buy & Hold Max DD: 8.96%
- Return/DD: 1.63 vs 0.76

Interpretation:
- Lower absolute return than Buy & Hold
- Much lower drawdown
- Positive risk-adjusted research value
- Not a Production Candidate yet

### Strategy Forward Gate
Introduced in v0.9.27.
- Champion is frozen at promotion point.
- Only post-freeze unused BTC/JPY 5m candles are evaluated.
- States: WAITING -> EARLY -> VALIDATING -> QUALIFIED / REVIEW
- 1 day = 288 candles
- 30 days required before final gate judgement.
- Forward update is manual and batch-based; continuous runtime is not required.
- Continuous learning remains OFF while current champion is under forward validation.
- Paper / Live are not automatically changed by this gate.

Latest observed state:
- Freeze: 2026-10-08 17:20:00 JST
- Forward candles observed: 20 / 288
- Status: WAITING
- Closed trades: 0

## Global Macro

### Employment Forward OOS
Introduced in v0.9.28.

Baseline:
- Freeze: 2026-10-08 21:21:48 JST
- Baseline n: 33
- Forward n: 0
- Status: WAITING
- Integrity: PASS

Stored Employment at baseline creation:
- Stored Employment: 35
- Event IDs: 35
- Pending: 2
- Latest baseline event: 2026-10-02 21:30 JST

Future scheduled events observed:
- 2026-11-06 Employment Situation for October 2026
- 2026-12-04 Employment Situation for November 2026
- These remain FORWARD_PENDING until release and observation maturity.

Rules:
- Baseline 33 is frozen and must not be retroactively expanded.
- New historical imports before the freeze must never enter Forward n.
- Employment events are treated as independent monthly events; no Regulation-style 24h episode merge.
- Forward n < 5 remains descriptive / reference only.
- Trade remains BLOCKED.

### Employment Historical Expansion
Historical import was expanded back to 2017-01-01 with Employment only.

Observed data state:
- Employment: 35 -> 119
- Added historical Employment events: 84
- Global Macro total Stored: 148 -> 232

Important:
- Import succeeded.
- The 84 added pre-freeze historical events are retrospective research data only.
- Employment Forward OOS Baseline remains 33 and must stay unchanged.

## Current Blocking Issue

The ordinary Global Macro Matched Replay path is not suitable for the 2017-2026 Employment expansion.

Observed symptom:
- Import shows Employment 119.
- Existing Replay result still shows Employment n=33.
- Therefore the extra 84 historical events have not yet been incorporated into historical replay analysis.

Current conclusion:
- Do not repeatedly run the ordinary Global Macro Replay for this long historical range.
- Forward OOS data is not considered corrupted.
- Historical Expansion needs a dedicated replay path.

## Runtime
Global Macro Runtime display is confirmed normal.
No Runtime UI fix is required.

## Next Development Target

Employment Historical Replay + Regime Stability.

Planned separation:

Employment Forward OOS
- Keep current Baseline n=33 frozen
- High-precision forward validation
- Future events only

Employment Historical Expansion
- 2017-2026 retrospective dataset
- Dedicated historical replay
- Long-range market-data cache
- Regime comparison

Target regime buckets:
- 2017-2020
- 2021-2023
- 2024-Freeze

Target metrics:
- event count
- matched count / control coverage
- 24h Excess
- Ratio
- Median Excess
- confidence interval
- stability / consistency signal

## Safety Boundary
- Historical results must never mutate the Forward OOS baseline.
- Historical results must never auto-promote a trading strategy.
- No Paper or Live trading unlock.
- Human approval remains required for any later Production Candidate transition.
