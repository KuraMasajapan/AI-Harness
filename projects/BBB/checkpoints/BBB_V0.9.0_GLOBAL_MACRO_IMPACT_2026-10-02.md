# BBB v0.9.0 Global Macro Impact Lab — Checkpoint
Date: 2026-10-02

## Trigger
- BOJ Human Review interim: 28/50
- Human Category Accuracy: 28.6%
- Risk Bias Agreement: 57.1%
- Human observation: many minor BOJ items and likely lower direct BTC relevance than Global/US drivers.

## Implemented
- Global Macro Impact Lab
- Tier A Relevance Gate
- Official historical sources:
  - Federal Reserve FOMC Statement
  - BLS Consumer Price Index
  - BLS Employment Situation
- Global Macro Schema v3:
  - rates_liquidity
  - inflation
  - employment
  - regulation_etf
  - crypto_native
  - geopolitical
  - jpy_japan_overlay
- English text is not sent to current Japanese-only Sokudan.
- Exact official release time is used where available.
- BTC/JPY impact windows: 30m / 1h / 4h / 24h.
- UI shows event-type average absolute move.
- Impact means post-release association, not causality.

## BOJ status
- Human Label Review paused at 28/50.
- Existing labels retained.
- BOJ reframed as Japan / JPY Overlay evidence.

## Validation
- pytest: 73 passed
- compileall: PASS
- UI JavaScript syntax: PASS
- flat ZIP root: PASS
- extracted ZIP pytest: 73 passed
- package: BBB_v0.9.0_Global_Macro_Impact_Lab.zip
- SHA-256: e0cdc829ff825eac2556da7f27ced607ae9accde7709551804216065c3b9d1b8

## Safety
Sandbox / read-only research only.
No Paper / Risk / Live behavior change.

## Windows startup hotfix
- Target symptom: native launch failed, browser fallback also exited before startup completed.
- Removed import-time dependency on Windows IANA timezone database for America/New_York.
- US Eastern offset now uses modern US DST calendar rules for Tier-A release timestamps.
- Browser fallback now exposes Global Macro status/import/replay methods.
- Validation: 75 pytest PASS / compileall PASS / startup regression PASS.
- Package: BBB_v0.9.0_Global_Macro_Impact_Lab_WINDOWS_HOTFIX.zip
- SHA-256: 3bb6708370b7332ab2ed95e13d9cdbda129870e7db7e70030c31fe7ecde36472

