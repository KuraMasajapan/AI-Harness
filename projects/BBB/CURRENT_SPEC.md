# BBB CURRENT SPEC

Updated: 2026-09-29
Status: CURRENT

## 1. Project identity
- Name: BITBANK-BOT
- Short name: BBB
- Exchange: bitbank
- Exchange interface: CCXT
- Primary pair: BTC/JPY

## 2. Project objective
暗号資産取引BotをいきなりAIエージェント化せず、古典的な決定論的Botを基礎として構築する。
過去相場とLive Paperで実績を構築し、改善ループの有効性を検証する。
将来AIを追加する場合も、AIなし基準機と比較できる構造を維持する。

## 3. Current architecture
bitbank Public Market Data
-> CCXT
-> OHLCV / Dataset
-> Snapshot Builder
-> EMA / RSI Strategy
-> Risk Manager
-> Paper Broker
-> Journal / Report / State

## 4. Implemented research capabilities
- Live Paper Trade
- Backtest
- Historical Replay
- fee / slippage modeling
- Buy & Hold comparison
- maximum drawdown
- win rate
- Profit Factor
- dataset SHA-256
- Agentless Learning Loop
- Research Champion保存
- time-series fold validation
- unseen holdout validation
- USD/JPYを用いたFX-aware signal normalization

## 5. Learning definition
現時点の「学習」はLLMやニューラルネットの再学習ではない。
EMA/RSI等の戦略パラメータ候補を過去データで評価し、未見Holdoutを含む時系列検証を通してResearch Championを更新する方式とする。

安全上、リスク上限は自動学習の対象から外す。

## 6. FX handling
BTC/JPYにはBTC価格変動とUSD/JPY変動が混在するため、判断用シグナルでは

BTC/JPY ÷ USD/JPY

を用いた為替中立化を利用可能とする。
一方、実際の約定・損益・資産評価はJPY建てのまま保持する。

将来は Global BTC/USD reference を追加し、
- 世界BTC価格
- USD/JPY
- bitbank固有乖離
の分離を検討する。

## 7. bitbank API Source of Truth
Official:
https://github.com/bitbankinc/bitbank-api-docs

確認済みの主要仕様:
- Public REST: ticker / depth / transactions / candlestick
- Public Stream: ticker / transactions / depth diff / depth whole
- Private REST: assets / spot orders / cancel / trades 等
- Private Stream: asset_update / spot_order_new / spot_order / spot_trade 等
- Private REST base: https://api.bitbank.cc/v1
- Public REST base: https://public.bitbank.cc
- REST基本レート制限: 取得系10回/秒、更新系6回/秒
- Private認証: HMAC-SHA256
- ACCESS-TIME-WINDOW方式をLive実装時の優先候補とする

## 8. Live trading boundary
CURRENTでは実注文機能を有効にしない。

Liveへ進む前に最低限:
- API credential secret handling
- 出金権限なし
- Kill Switch
- max order
- max position
- daily loss stop
- duplicate order prevention
- timeout ambiguity handling
- active order reconciliation
- Private Stream reconciliation
- rate-limit handling
- minimum size / precision validation
- circuit breaker / maintenance handling
- canary small-value live test
- independent audit

を満たす。

## 9. Credentials
API Key / API Secret はAI-Harnessへ保存しない。
秘密情報はローカル実行環境のSecretとしてのみ扱う。

## 10. Current test state
2026-09-29:
- local pytest: 26 passed
- live order path: NOT IMPLEMENTED
