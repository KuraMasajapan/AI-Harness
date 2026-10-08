# v0.9.29 — Employment Historical Regime Replay

Status: IMPLEMENTED
Date: 2026-10-08

This file was originally created as a candidate design before the actual v0.9.29 package was available.
The uploaded v0.9.29 Full ZIP confirms this work is already implemented.

## Implemented scope
- Dedicated Employment Historical Regime Replay
- Employment Forward OOS remains separated from retrospective history
- Long-range historical BTC/JPY data uses bitbank Public API dated candlesticks
- Historical lane uses 30min candles and 24h matched-control horizon
- Local cache is reused on later runs
- Regime buckets:
  - 2017–2020
  - 2021–2023
  - 2024–Forward Freeze
- Regime output includes Event |Move|, Control |Move|, Excess, Ratio, Median Excess and Bootstrap CI
- Historical results do not mutate Forward n, Baseline n or Trade Gate
- Global Macro Runtime retains Import / Replay values and surfaces Replay errors

## Forward boundary
Employment Forward OOS from v0.9.28 remains the authoritative prospective lane.
Historical expansion is retrospective-only.

## Safety
- Public read-only data
- Sandbox/research use
- No private API
- No live orders
- Historical replay cannot unlock trade execution

## Source verification
Verified from uploaded package:
- src/bbb/__init__.py: 0.9.29
- pyproject.toml: 0.9.29
- docs/V0.9.29_EMPLOYMENT_HISTORICAL_REGIME_REPLAY_JA.md
- tests/test_global_macro_historical_v0929.py
- tests/test_ui_v0929.py
