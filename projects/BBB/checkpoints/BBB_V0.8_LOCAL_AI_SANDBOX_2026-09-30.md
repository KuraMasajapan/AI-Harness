# BBB v0.8 Local AI Sandbox

Date: 2026-09-30
Status: IMPLEMENTED IN DISTRIBUTABLE PACKAGE / SANDBOX ONLY

## Summary

BBB v0.8 adds an optional Local AI Fundamental Sentinel Sandbox using Sokudan.

Target:
- Windows PC
- no GPU required
- CPU inference
- Local AI starts with BBB after one-time optional setup
- BBB continues to operate when Local AI is absent, loading, offline, or broken

Current Local AI has **zero trading authority**.

## Implementation

### Optional setup
Added:
- `BBB_LOCAL_AI_SETUP.bat`
- `BBB_LOCAL_AI_DIAGNOSTIC.bat`

Setup installs:
- `sokudan[serve]>=0.3,<0.4`

The model weights are downloaded by Sokudan on first Local AI start.

### Auto-start
`DesktopController` owns a `LocalAIManager`.

When Local AI is enabled and Sokudan is installed:
- BBB starts the official Sokudan server as a separate local child process
- endpoint: `127.0.0.1:8766`
- backend: torch
- device: cpu
- model: `GeneLab/sokudan-ja-310m`

If a compatible local server is already reachable, BBB reuses it.

BBB does not block waiting for Local AI model loading.

### Isolation / fallback
Local AI process is isolated from the Paper trading loop.

States:
- READY
- LOADING
- NOT_INSTALLED
- OFFLINE
- DISABLED

Local AI failure does not stop:
- market data
- Paper trading
- Strategy Lab
- journal
- desktop UI

### Sandbox classification
Implemented fixed financial-text schema:

- category
  - monetary_policy
  - inflation
  - employment
  - crypto_market
  - regulation
  - geopolitical
- importance: low / medium / high
- btc_relevance: low / medium / high
- fx_relevance: low / medium / high
- risk_bias: risk_on / risk_off / unclear

Current output is observation-only.

No method connects this output to:
- BUY / SELL
- order size
- Risk limits
- Research Champion
- Live Gate

### Sandbox ledger
Local AI observations are stored locally:

- `data/local_ai/fundamental_sandbox.jsonl`
- server log: `data/local_ai/sokudan_server.log`

No API credentials are stored or passed to Local AI.

### UI
Risk & System now includes:

`Local AI · Fundamental Sentinel`

Displays:
- state
- model
- Sokudan package version
- CPU device
- last inference latency/time
- SANDBOX ONLY
- Trade influence OFF

Added a Local AI self-test button and Ctrl+K command.

### Tests
Local test result:
- pytest: **33 passed**
- Python compileall: PASS
- UI JavaScript syntax check: PASS

New tests cover:
- Local AI config loading
- Sokudan response normalization
- fixed classification schema request
- safe behavior when Sokudan is not installed

## Package

Generated package:
`BBB_v0.8_Local_AI_Sandbox.zip`

SHA-256:
`a616f88fc6a2144cae50190151bcc15948054b836f875f5e12c0883b24ac016b`

## Safety boundary

Still true:
- PAPER / RESEARCH only
- Private API not used
- Live order path not implemented
- Local AI Sandbox does not influence trading
- Local AI cannot unlock Live
- Local AI cannot alter risk limits
- Research Champion cannot auto-promote to Live

## Next recommended work

1. Install Sokudan on target Windows PC.
2. Measure actual CPU load, RAM, model-load time, and latency.
3. Run BBB-specific financial text benchmark.
4. Start collecting Sandbox classifications.
5. Only after evidence, design Fundamental Policy Engine risk-only influence.
