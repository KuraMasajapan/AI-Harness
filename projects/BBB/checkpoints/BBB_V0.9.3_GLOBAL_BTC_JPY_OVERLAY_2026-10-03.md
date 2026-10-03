# BBB v0.9.3 Global BTC / JPY Overlay Decomposition — Checkpoint
Date: 2026-10-03

## Trigger
v0.9.2 robustness showed:
- overall matched 24h excess remained positive after robust summaries
- Employment was the strongest current matched sample
- next question: is BTC/JPY reaction mostly Global BTC or JPY-side movement?

## Implemented
### Public references
- BTC/JPY: bitbank Public via existing CCXT adapter
- BTC/USD: CCXT public reference
  - preferred: Coinbase
  - fallback: Kraken
- no private API / no credentials

### Decomposition
For each Tier-A Global Macro event:
- common official release-time anchor
- timeframe: 30m
- horizons: 30m / 1h / 4h / 24h
- exact multiplicative identity:
  (1 + BTCJPY return) = (1 + BTCUSD return) * (1 + Implied JPY Overlay return)

### Important interpretation boundary
Implied JPY Overlay is not a direct USD/JPY feed.
It is the BTC/JPY ÷ BTC/USD cross-rate residual and can include:
- USD/JPY / JPY movement
- cross-exchange basis
- market microstructure differences

### Dashboard
- Decomposed event count / failure count
- 24h Global BTC |Move|
- 24h JPY Overlay |Move|
- Global-dominant share
- average Global magnitude share
- FOMC / CPI / Employment comparison at 30m / 1h / 4h / 24h
- job elapsed time

### Efficiency
Fetch only event-local ~24h windows instead of downloading a complete multi-year BTC/USD 30m dataset.

## Validation
- pytest: 90 passed
- compileall: PASS
- UI JavaScript syntax: PASS
- flat ZIP root: PASS
- extracted ZIP pytest: 90 passed
- package: BBB_v0.9.3_Global_BTC_JPY_Overlay_Decomposition.zip
- SHA-256: 39d62d1ad97a7a78bf56a6bcee96519ca4956d746b453d04f06fd1f5bb0506d5

## Safety
Public read-only research only.
No Paper / Risk / Champion / Live behavior change.
