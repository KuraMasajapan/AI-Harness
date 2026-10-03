# BBB v0.9.6 FX Source Cross-check — Checkpoint
Date: 2026-10-03

## Trigger
v0.9.5 target result:
- input 62
- validated 13
- failed 49
- coverage 21.0% / LOW_COVERAGE
- elapsed 24:20
- cache 27 / network OK 24 / retries 402 / failures 197

Retry tuning alone is not sufficient.

## Source decision
Official Dukascopy documentation describes the current daily bucket as a Requester Pays S3 source.
BBB does not make that path the default because it would require AWS credentials and may incur request/data-transfer cost.

## Implemented
### Dukascopy hourly resilience
- primary: https://datafeed.dukascopy.com/datafeed
- fallback: https://www.dukascopy.com/datafeed
- existing cache retained
- max concurrent public fetches remains restrained
- host fallback diagnostics added

### Analysis Gate
- READY: coverage >= 95%
- CAUTION: coverage >= 50% and <95%
- BLOCKED: coverage <50%
Low-coverage aggregate values are not promoted to research conclusions.

### Official daily cross-check
Source:
- FRED DEXJPUS
- Federal Reserve H.10
- Japanese Yen to One U.S. Dollar
- New York noon daily observation

Method:
- event before NY noon: prior available noon -> same-day noon
- event after NY noon: same-day noon -> next available noon
- this brackets the event with official daily observations
- this is not an exact event-time 24h return and not a 30m/1h/4h substitute

UI:
- Coverage
- Avg absolute bracket move
- sign agreement with Implied JPY Overlay 24h
- coarse FX magnitude share
- FOMC / CPI / Employment comparison
- elapsed time

## Validation
- pytest: 106 passed
- compileall: PASS
- UI JavaScript syntax: PASS
- BAT static check: PASS
- flat ZIP root: PASS
- extracted ZIP pytest: 106 passed
- package: BBB_v0.9.6_FX_Source_Crosscheck.zip
- SHA-256: 96ba959e0da96f19e4d59471071498b79ef853177330dc022bf14292060a8259

## Safety
Public read-only research only.
No Paper / Risk / Champion / Live behavior change.
