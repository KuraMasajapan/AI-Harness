# BBB v0.8.3 Fundamental Data Collector

Date: 2026-10-01
Status: IMPLEMENTED IN DISTRIBUTABLE PACKAGE / SANDBOX ONLY

## Goal

Connect real public fundamental information to the already-running Sokudan Local AI without giving AI any trading authority.

## Implemented sources

### BOJ News RSS
- URL: https://www.boj.or.jp/rss/whatsnew.xml
- mode: CLASSIFY
- Japanese feed items are sent to Sokudan.

### BOJ Statistics RSS
- URL: https://www.boj.or.jp/rss/statistics.xml
- mode: CLASSIFY
- Japanese statistical announcements are sent to Sokudan.

### Federal Reserve Press RSS
- URL: https://www.federalreserve.gov/feeds/press_all.xml
- mode: COLLECT ONLY
- Current Sokudan path is treated as Japanese-only, so English items are stored but not forced through the classifier.

### FRED
- UI state: NOT_CONFIGURED / PLANNED
- Structured macro API integration deferred to a later step.

## Pipeline

```text
Official public RSS
        ↓
Fundamental Data Collector
        ↓
SHA-256 dedupe
        ↓
Japanese text?
  ├─ yes -> Sokudan typed classification
  └─ no  -> collect only
        ↓
Sandbox storage
        ↓
Data Sources Hub / Fundamental Feed
```

## Runtime

- automatic poll: 15 minutes by default
- manual refresh: Risk & System -> Data Sources Hub -> 今すぐ取得
- first-run flood protection: only latest 2 new items per source are processed; older current-feed items are marked seen
- if Local AI is not READY, eligible items are queued in `data/fundamental/pending_classification.json` and retried later

## Storage

- `data/fundamental/feed_events.jsonl`
- `data/fundamental/seen_ids.json`
- `data/fundamental/pending_classification.json`
- Local AI ledger remains `data/local_ai/fundamental_sandbox.jsonl`

## UI

Added to Risk & System:
- Data Sources Hub
- Fundamental Feed

Source state includes:
- connection/fetch state
- CLASSIFY vs COLLECT ONLY
- last fetch
- new item count
- classified count
- error state

## Safety

Unchanged:
- Sandbox only
- trade influence OFF
- no BUY / SELL from Local AI
- no Risk mutation
- no Live authority
- no Private API credentials

## Validation

- pytest: 38 passed
- Python compileall: PASS
- UI JavaScript syntax check: PASS
- BAT label/goto static check: PASS

## Package

`BBB_v0.8.3_Fundamental_Data_Collector.zip`

SHA-256:
`dad806066d591957732597795a4bcebf33c82cd4b31c820525f1d88c68f635d3`
