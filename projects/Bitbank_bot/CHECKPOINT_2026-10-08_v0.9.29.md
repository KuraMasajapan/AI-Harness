# Bitbank_bot Checkpoint v0.9.29

Date: 2026-10-08
Status: latest confirmed release

## Version
- BBB v0.9.29
- Release: Employment Historical Regime Replay
- Package inspected: BBB_v0.9.29_EMPLOYMENT_HISTORICAL_REGIME_RUNTIME_FIX_FULL(1).zip
- Uploaded package SHA-256: ab5487f23ffb27528f0a467d01146f8c02856266a15979aad389028f6a4fa41c
- Update method: Full ZIP

## Version verification
Confirmed directly from package:
- src/bbb/__init__.py: __version__ = "0.9.29"
- pyproject.toml: version = "0.9.29"
- v0.9.29 documentation and dedicated tests are included.

## Employment Historical Regime Replay
Purpose:
- Evaluate U.S. Employment Situation history expanded back to 2017.
- Keep retrospective history strictly separate from Employment Forward OOS.

Market data design:
- Ordinary Global Macro Replay remains operational-window oriented.
- Historical Employment Replay uses bitbank official Public API dated candlesticks.
- Only necessary historical market days are acquired and cached locally.
- 30min candles are used in the Historical lane.
- Primary historical horizon is 24h with Matched Control.

Regime buckets:
- 2017–2020
- 2021–2023
- 2024–Forward Freeze

Regime metrics:
- Event absolute move
- Control absolute move
- Excess
- Ratio
- Median Excess
- Bootstrap CI

## Forward OOS boundary
Employment Forward OOS from v0.9.28 remains separate.
- Baseline n=33 remains frozen.
- Historical backfill does not enter Forward n.
- Historical results do not change the Forward baseline.
- Historical results do not alter Trade Gate.

## Training Lab state carried forward
Research Champion:
- Mean Reversion
- lookback: 79
- entry_z: 2.0
- exit_z: 0.0

Benchmark:
- QUALIFIED · RISK EFFICIENT

Strategy Forward Gate:
- Freeze: 2026-10-08 17:20:00 JST
- Latest observed Forward candles: 20 / 288
- Status: WAITING at last observation
- Continuous learning remains OFF while the frozen champion is under forward validation.

## Historical Employment data state before v0.9.29 replay
- Employment records expanded: 35 -> 119
- Historical additions: 84
- Global Macro Stored expanded: 148 -> 232
- These additions are retrospective-only relative to the Forward freeze.

## Runtime
The v0.9.29 package includes paired Import / Replay runtime retention and explicit Replay error presentation.
Runtime is not considered an active blocking issue.

## Safety
- Public read-only market data
- No private API
- No live order execution
- Historical replay has no Paper / Live unlock side effect
- Human approval remains required for any later production transition

## Current development position
v0.9.29 is no longer a candidate design. The Historical Employment Regime Replay is implemented.
The next step is to run/inspect the v0.9.29 Historical Regime results on the user's local imported 119-event dataset and evaluate regime stability without modifying Forward OOS.
