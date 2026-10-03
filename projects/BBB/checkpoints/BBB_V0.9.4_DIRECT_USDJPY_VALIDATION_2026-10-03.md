# BBB v0.9.4 Direct USD/JPY Validation — Checkpoint
Date: 2026-10-03

## Trigger
v0.9.3 target decomposition:
- 62 / 62 events
- 24h Global BTC |Move| 2.14%
- 24h Implied JPY Overlay |Move| 0.58%
- Global BTC dominant 89%
- Employment dominant 96%
- CPI dominant 87%
- FOMC dominant 81%

Need to validate how much of Implied JPY Overlay is actual USD/JPY versus exchange basis/residual.

## Implemented
### Direct FX source
- Dukascopy public historical USD/JPY tick data
- bid/ask midpoint
- hourly .bi5 event-local files
- JPY point scale 1,000
- local cache: data/fx_cache/dukascopy
- no API key / no private credential / no order methods

### Decomposition
For each Tier-A event and 30m / 1h / 4h / 24h:
- v0.9.3 Implied JPY Overlay
- Direct USD/JPY return
- Basis Residual = Overlay / Direct FX multiplicative residual
- Direct FX magnitude share
- Direct FX dominant share
- sign agreement helper metric

Identity:
(1 + BTCJPY return)
= (1 + BTCUSD return)
× (1 + Direct USDJPY return)
× (1 + Basis Residual return)

### UI
Direct USD/JPY Validation section:
- Validated / failed
- 24h Direct USD/JPY |Move|
- 24h Basis Residual |Move|
- FX magnitude share
- FX dominant share
- elapsed
- FOMC / CPI / Employment comparison table

## Validation
- pytest: 96 passed
- compileall: PASS
- UI JavaScript syntax: PASS
- BAT static check: PASS
- flat ZIP root: PASS
- extracted ZIP pytest: 96 passed
- package: BBB_v0.9.4_Direct_USDJPY_Validation.zip
- SHA-256: e73137679877b1a0541102dc2f9be3aa9e5dd8a6f3463948b4365d956eb4792d

## Safety
Public read-only research only.
No Paper / Risk / Champion / Live behavior change.
