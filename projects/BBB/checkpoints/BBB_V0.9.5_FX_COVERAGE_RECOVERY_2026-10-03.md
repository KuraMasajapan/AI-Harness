# BBB v0.9.5 FX Coverage Recovery — Checkpoint
Date: 2026-10-03

## Trigger
v0.9.4 target Direct USD/JPY Validation:
- elapsed: 15:41
- input: 62
- validated: 3
- failed: 59
- successful sample: FOMC 1 / CPI 1 / Employment 1

The n=3 aggregate is pipeline proof only and must not be used as evidence.

## Implemented
- Dukascopy retry for retryable HTTP/network errors
- controlled backoff
- anchor-first prefetch
- horizon prefetch second
- max 3 concurrent requests
- serial repair pass for failed hours
- run-level unavailable-hour memoization
- existing cache reuse
- source diagnostics and failure-reason summary
- coverage state:
  - COMPLETE >=95%
  - PARTIAL >=50%
  - LOW_COVERAGE <50%
- UI coverage/source diagnostics

## Validation
- pytest: 101 passed
- compileall: PASS
- UI JavaScript syntax: PASS
- flat ZIP root: PASS
- extracted ZIP pytest: 101 passed
- package: BBB_v0.9.5_FX_Coverage_Recovery.zip
- SHA-256: 0ec75e7c8dcec2895c6f7e29e97d344b86d1556df62106ba7ac06c5f434bcf21

## Safety
Public read-only research only.
No Paper / Risk / Champion / Live behavior change.
