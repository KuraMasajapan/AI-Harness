# BBB v0.8.4 Cleanup + Fundamental Replay Lab α — Checkpoint
Date: 2026-10-01
Project: BITBANK-BOT (BBB)
Branch: development

## State
v0.8.3 target PC confirmed:
- bitbank Public API connected
- Sokudan Local AI READY on CPU
- BOJ News / Statistics RSS real-data collection working
- Fed Press RSS collect-only working
- deferred Local AI classification produced duplicate UI rows for the same event
- an orphan Sokudan/Python process previously kept an old BBB folder locked until manually terminated

## v0.8.4 implemented
### Feed Current View
- feed_events.jsonl remains append-only for audit
- UI/materialized current view merges records by event_id
- deferred classification update replaces the visible local_ai_not_ready state instead of adding a second visible news row

### Local AI lifecycle
- Desktop and browser shutdown paths call controller.shutdown()
- Fundamental collector loop is stopped
- owned Sokudan process is explicitly terminated
- Windows uses taskkill /T /F for the owned process tree
- BBB_STOP.bat added for emergency cleanup of BBB/Sokudan listener processes

### Classification Schema v2
- schema id: bbb-fundamental-v2
- added category: financial_markets
- crypto_market wording narrowed to crypto-specific material
- schema version and SHA-256 stored with new Local AI classification records
- accuracy improvement is NOT assumed; it must be measured by case study/replay

### Fundamental Replay Lab α
- source events: current de-duplicated classified Fundamental Feed
- knowledge-time boundary: recorded_at (time BBB actually observed the item)
- market source: bitbank Public BTC/JPY via existing CCXT read-only adapter
- horizons: 5m / 30m / 1h / 4h / 24h
- unavailable future horizon remains null
- outputs:
  - data/fundamental_replay/run_*/market.csv
  - data/fundamental_replay/run_*/confidence_ledger.jsonl
  - data/fundamental_replay/run_*/report.json
  - data/fundamental_replay/last_report.json
- Sandbox only / Trade influence OFF

## UI
Risk & System now contains Fundamental Replay Lab α:
- Observed events
- Classified events
- Last run
- 1h bias alignment
- Replay trial button

## Validation
- pytest: 43 passed
- Python compileall: PASS
- UI JavaScript syntax: PASS
- BAT goto/label static check: PASS
- packaged ZIP was extracted and the 43-test suite passed again

## Package
- filename: BBB_v0.8.4_Cleanup_Fundamental_Replay.zip
- SHA-256: 2fd48fb7a28914c7bb8ee567d6354c11f89f8ff415eebb45a65d34e3077feb3a

## Safety boundary
Unchanged:
- no private API
- no real-money order path
- no Local AI BUY/SELL authority
- no automatic Risk mutation
- no Research/Replay result auto-promotion to Live

## Next
1. Target PC overwrite upgrade while preserving data and .venv_local_ai.
2. Confirm duplicate Fundamental Feed rows are unified.
3. Close BBB and confirm Sokudan does not remain orphaned.
4. Run Fundamental Replay trial on current classified events.
5. Then expand historical event ingestion for larger case-study datasets.
