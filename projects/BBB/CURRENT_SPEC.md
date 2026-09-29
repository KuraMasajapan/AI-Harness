# BBB CURRENT SPEC

Updated: 2026-09-30
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
-> Strategy Lab / Research Champion
-> Risk Manager
-> Paper Broker
-> Journal / Report / State
-> Desktop Trading Research Cockpit

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
- Multi-strategy Strategy Lab
- Continuous Research Cycle
- Desktop Trading Research Cockpit
- Paper analytics / equity curve
- read-only public OHLCV chart
- audit snapshot export
- Local AI Fundamental Sentinel Sandbox
- Sokudan auto-start / health state
- Local AI self-test / local sandbox ledger

## 5. Learning definition
現時点の「学習」はLLMやニューラルネットの再学習ではない。
過去データで複数戦略とパラメータ候補を評価し、未見Holdoutを含む時系列検証を通してResearch Championを更新する方式とする。

安全上、リスク上限は自動学習の対象から外す。

## 5.1 Strategy Lab families
以下をChallengerとして比較可能:
- EMA + RSI
- EMA Cross
- Breakout
- Mean Reversion
- Momentum

同一Datasetの再利用だけでは昇格させない。
前回昇格後に十分な新規ローソク足が増えていない場合も昇格を止める。

Paper Runnerは互換性のあるResearch Championを新しいローソク足ごとに再読込し、Paperへ反映する。
Research ChampionからLive実資金への自動昇格は禁止。

今後のStrategy候補:
- MACD
- Bollinger
- ATR Regime
- Multi Timeframe
- Volume / Orderbook

## 5.2 Fundamental Sentinel (SANDBOX IMPLEMENTED / NO TRADE INFLUENCE)
GPUなしPC上の小型Local AIを、ファンダメンタルズ情報の文脈整理専用エージェントとして利用する構想を採用候補とする。

責務分離:
- API / deterministic collector: 経済指標、ニュース、時刻、数値、本文を取得
- deterministic rules: Actual/Forecast差分など単純な数値判定
- Local AI: ニュース・声明の要約、分類、文脈理解、関連度・重要度・不確実性評価
- Fundamental Policy Engine: AI出力を決定論的なBBB指示へ変換
- Risk Manager / Live Gate: 最終安全権限

Local AIはBUY / SELLを直接決定しない。
UNKNOWN / no_overrideを正式な正常出力として許可する。
Local AI停止時にもBBB本体が継続可能なFallbackを持つ。

v0.8でSokudanを用いたFundamental AI Sandboxを実装した。
Local AIは別ローカルプロセスとしてBBB起動時に自動起動可能で、GPUなしCPU運用を前提とする。
Local AI未導入・LOADING・OFFLINE・障害時もBBB本体は継続する。
現在の分類結果は売買へ反映せず、Sandbox Ledgerへ保存して精度を検証する。
将来はFundamental Confidence Ledgerでカテゴリ別の有効性を評価し、十分な実績がある範囲だけRisk調整へ利用する。

詳細:
- checkpoints/BBB_FUNDAMENTAL_SENTINEL_CONCEPT_2026-09-29.md
- agents/Local-AI/README.md
- Harness-wide model catalog: ../../agents/Local-AI/README.md
- checkpoints/BBB_V0.8_LOCAL_AI_SANDBOX_2026-09-30.md

## 6. FX handling
BTC/JPYにはBTC価格変動とUSD/JPY変動が混在するため、判断用シグナルでは

BTC/JPY ÷ USD/JPY

を用いた為替中立化を利用可能とする。
一方、実際の約定・損益・資産評価はJPY建てのまま保持する。

FX中立シグナルで学習したChampionは、Paper側に同一参照フィードが無い限り自動適用しない。

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

## 8. Desktop operation
v0.8はWindows向けTrading Research CockpitとLocal AI Sandboxを持つ。
- BBB_START.bat
- native desktop shell: pywebview
- native shellが利用できない場合: localhost browser console fallback
- Desktop shortcut installer

UI:
- Dashboard
- Training Lab
- History
- Risk & System
- Public OHLCV candlestick chart
- Paper equity curve
- Return / Max DD / decision / fill / error metrics
- Research Champion表示
- Strategy Family cards
- Research Job timeline
- Operational Readiness
- Kill Switch
- Toast notifications
- Ctrl+K command palette
- keyboard navigation
- audit snapshot export

## 9. UI / UX policy
便利機能・UI/UXは過剰気味でも積極的に試す。
ただし以下はUI実験から独立した固定境界:
- PAPER / LIVEを視覚的に明確に分離
- 停止操作を簡単にする
- Live操作は単一クリックで開始させない
- Private SecretをUIやログへ表示しない
- Research ChampionからLiveへの自動昇格を禁止

## 10. Live trading boundary
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

## 11. Credentials
API Key / API Secret はAI-Harnessへ保存しない。
秘密情報はローカル実行環境のSecretとしてのみ扱う。

## 12. Current test state
2026-09-30:
- local pytest: 33 passed
- Python compileall: PASS
- UI JavaScript syntax check: PASS
- 5 strategy families available
- Local AI Sandbox: IMPLEMENTED
- Local AI trade influence: OFF
- live order path: NOT IMPLEMENTED
