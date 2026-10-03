# BBB v0.9.7 FX Evidence Gate + Sidebar Contrast Fix — Checkpoint
Date: 2026-10-03

## Trigger
- FRED daily cross-check: 62/62, 100% COMPLETE, near-instant.
- Direct intraday FX remains low coverage.
- Human UI feedback: selected sidebar item could become a pale filled block with similarly pale text, reducing readability.

## Implemented
### FX Evidence Gate
Separate evidence layers:
- Daily Baseline: FRED DEXJPUS
- Intraday Precision: Dukascopy historical ticks

Coverage states:
- READY >=95%
- CAUTION >=50% and <95%
- BLOCKED <50%

Combined states include:
- FULL_READY
- DAILY_READY_INTRADAY_CAUTION
- DAILY_READY_INTRADAY_BLOCKED
- BLOCKED

If Daily is READY but Intraday is not READY:
- official daily baseline is usable
- 30m / 1h / 4h short-horizon conclusions remain blocked

### Fast FRED UX
- DONE label
- processed count (e.g. 62/62)
- sub-second duration shown as <1s or milliseconds instead of 00:00-only

### Sidebar selection contrast
- dark selected background
- Electric Blue left rail
- high-contrast main text
- readable Japanese sublabel
- blue icon accent
- high-specificity override prevents older theme rules from washing out selected items

## Validation
- pytest: 108 passed
- compileall: PASS
- UI JavaScript syntax: PASS
- BAT static check: PASS
- flat ZIP root: PASS
- extracted ZIP pytest: 108 passed
- package: BBB_v0.9.7_FX_Evidence_Gate_UI_Fix.zip
- SHA-256: 38084f885c75d9a473b53f8c9fad73c9931950c59569028b6fd4b6ecef53b38c

## Safety
Research / Sandbox only.
No Paper / Risk / Champion / Live behavior change.

## Evidence card overflow hotfix
- Symptom: long machine-state value overflowed the first FX Evidence Gate metric card.
- Display labels shortened; full machine state retained in title/hover.
- Metric values now defensively wrap and cards allow shrink with min-width:0.
- pytest: 109 passed
- compileall: PASS
- UI JS syntax: PASS
- package: BBB_v0.9.7_FX_Evidence_Gate_OVERFLOW_HOTFIX.zip
- SHA-256: d8ab3132db1263b13b59e9e3b0877359a48f3760b929307c6e5b720b91fa49e7

