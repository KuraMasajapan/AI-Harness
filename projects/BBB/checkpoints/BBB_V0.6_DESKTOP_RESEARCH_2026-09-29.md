# BBB v0.6 Desktop Research Checkpoint — 2026-09-29

Status: RESEARCH / PAPER
Version: v0.6

## Human direction
- すぐ使える形に仕上げて渡す。
- そこから継続的に学習させる。
- EMA+RSIだけでなく、他のトレード手法も継続して試す。
- UIはデスクトップから扱えるアプリ形式を目指す。

## Implemented
- Desktop Research Console
- Windows BBB_START.bat
- Desktop shortcut installer
- native pywebview shell
- localhost browser fallback
- Paper start/stop
- Paper Kill Switch
- recent decision log UI
- Research Champion UI
- manual Research Cycle
- continuous Research Loop
- Strategy Lab

## Strategy Lab families
- EMA + RSI
- EMA Cross
- Breakout
- Mean Reversion
- Momentum

## Learning / promotion controls
- time-series development folds
- unseen holdout
- dataset SHA-256 reuse block
- minimum new-market-data gate
- minimum closed-trade gate
- holdout score gate
- drawdown worsening gate
- risk limits excluded from optimization
- Research -> Live automatic promotion prohibited

## Paper reflection
- Paper Runner reloads a compatible Research Champion each new candle.
- FX/reference-based Champion is not silently applied without a matching live reference signal.

## Verification
- pytest: 28 passed
- all five strategy families simulation smoke tested
- Strategy Lab tournament smoke tested
- synthetic smoke test selected EMA Cross and completed report generation
- UI asset package presence verified
- synthetic champion files removed from distributable data directory

## Environment limitation
This ChatGPT container has no outbound pip/network access, so native pywebview/CCXT installation and live bitbank connectivity cannot be executed here. The Windows bootstrap installs runtime dependencies on the user's PC.

## Live boundary
- Real-money order path: NOT IMPLEMENTED
- Private bitbank API credentials: NOT REQUIRED
- API keys/secrets: NOT stored in Harness
