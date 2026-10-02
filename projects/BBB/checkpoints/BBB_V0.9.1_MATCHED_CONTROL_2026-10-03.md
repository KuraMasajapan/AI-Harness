# BBB v0.9.1 Matched Control — Checkpoint
Date: 2026-10-03

## Trigger
v0.9.0 target result:
- Tier-A events: 62
- FOMC 16 / CPI 23 / Employment 23
- Overall 24h average absolute BTC/JPY move: 2.30%
- Need to know whether Event windows move more than normal BTC windows.

## Implemented
### Matched Control v1
For each imported Tier-A event:
- preserve source-specific official release clock
- candidate controls: same weekday at +/- 7 / 14 / 21 / 28 days
- exclude candidates within 24h of any imported Tier-A event
- use up to 4 valid controls

### Metrics
At 30m / 1h / 4h / 24h:
- Event Avg |Move|
- Control Avg |Move|
- Excess Avg |Move| = Event - Control
- Event / Control Ratio
- Event > Control Share
- Avg Controls per Event

### UI
Global Macro card now shows:
- 24H Control
- 24H Excess
- Event / Control
- Matched Control table by FOMC / CPI / Employment
- replay button renamed to Run Matched Replay

### Interpretation boundary
Matched controls reduce baseline/time-of-week/nearby-regime bias only.
They do not eliminate other news or market confounders and do not prove causality.

## Validation
- pytest: 79 passed
- compileall: PASS
- UI JavaScript syntax: PASS
- flat ZIP root: PASS
- extracted ZIP pytest: 79 passed
- package: BBB_v0.9.1_Global_Macro_Matched_Control.zip
- SHA-256: 892eb3db738299c1eb130e180de0c9ef9407586bcb3e06584016582091b78164

## Safety
Sandbox / read-only research only.
No Paper / Risk / Live behavior change.
