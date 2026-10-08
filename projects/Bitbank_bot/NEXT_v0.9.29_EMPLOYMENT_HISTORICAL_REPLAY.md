# v0.9.29 Candidate — Employment Historical Replay / Regime Stability

Status: design ready, implementation pending source package access
Date: 2026-10-08

## Goal
Add a dedicated retrospective replay path for the imported Employment history (2017-2026) without changing the v0.9.28 Employment Forward OOS baseline.

## Non-goals
- Do not change Employment Forward OOS Baseline n=33.
- Do not reuse historical additions as Forward observations.
- Do not unlock Paper or Live trading.
- Do not alter Research Champion or Strategy Forward Gate.
- Do not change Global Macro Runtime UI; it is confirmed normal.

## Proposed UI
Global Macro Impact Lab:

Employment Historical / 雇用統計・長期検証
- Historical Stored
- Historical Matched
- Coverage
- Last Replay
- Cache coverage
- State
- Run Historical Replay

Regime Stability table:
| Regime | Events | Matched | 24h Excess | Ratio | Median | CI | Control Coverage |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| 2017-2020 | | | | | | | |
| 2021-2023 | | | | | | | |
| 2024-Freeze | | | | | | | |

## Data Boundary
Historical eligibility:
- source/category = Employment
- event timestamp < Employment Forward Freeze
- imported historical records are allowed
- forward pending and post-freeze events are excluded

Forward eligibility remains exactly as v0.9.28.

## Market Data Retrieval
Do not fetch one continuous 2017-now 5m range through the existing generic replay path.

Use event-window acquisition:
1. For each eligible Employment event, derive only the required market windows.
2. Fetch BTC/JPY candles for those windows.
3. Cache by date/window so repeated replay does not redownload the same data.
4. Reuse cached candles across events when windows overlap.
5. Record cache hit / miss / missing coverage explicitly.

This keeps historical replay bounded by event count rather than by ten continuous years of 5m candles.

## Suggested Cache Layout
data/global_macro/historical_market_cache/
- btc_jpy/
  - 2017/
  - 2018/
  - ...
- manifest.json

Manifest should record:
- provider
- symbol
- timeframe
- date/window
- first_ts
- last_ts
- candle_count
- fetched_at
- integrity status

## Replay Output
Write a separate historical report, not the existing Forward OOS state.

Suggested:
data/global_macro/employment_historical/
- employment_historical_replay.json
- employment_regime_stability.json

Each event record should keep:
- Event ID
- event timestamp
- regime
- source
- title
- treatment return(s)
- control match
- excess
- market-data coverage
- exclusion reason if unmatched

## Regime Rules
Initial fixed buckets:
- 2017-01-01 through 2020-12-31
- 2021-01-01 through 2023-12-31
- 2024-01-01 through Forward Freeze

Do not silently move the Freeze boundary when rerunning.

## Integrity Guards
Fail or mark incomplete rather than silently dropping data when:
- event window candles are missing
- control window cannot be constructed
- event is post-freeze
- duplicate Event ID is detected
- cache contains inconsistent timestamps
- historical report attempts to mutate Forward state

## Tests
Minimum new coverage:
- pre-freeze imported events enter Historical only
- post-freeze events never enter Historical regime output
- Baseline n=33 remains unchanged after Historical Replay
- cache hit path
- cache miss fetch path
- partial candle coverage
- duplicate event IDs
- all three regime buckets
- repeated replay is idempotent
- historical report and forward report remain separate
- no Paper / Live unlock side effect

## Acceptance Criteria
The implementation is acceptable when:
1. Employment Stored remains 119 (or later legitimate import count).
2. Historical Replay evaluates the imported pre-freeze events beyond the original 33.
3. Forward OOS Baseline remains exactly 33.
4. Regime table is populated separately.
5. Re-running Historical Replay does not change Forward state.
6. Missing market data is visible as missing/incomplete rather than silently excluded.
7. Existing test suite plus new tests pass.
