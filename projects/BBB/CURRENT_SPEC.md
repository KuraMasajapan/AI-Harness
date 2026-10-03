# BBB CURRENT SPEC

Updated: 2026-10-01
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
- Fundamental Data Collector
- BOJ News RSS / BOJ Statistics RSS
- Federal Reserve Press RSS (collect only)
- Data Sources Hub / Fundamental Feed

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
v0.8.1でBBB本体とSokudanのPython環境を分離し、Sokudanは専用 `.venv_local_ai` (Python 3.11-3.13) で動かす。BBB本体がPython 3.14でもLocal AIを独立導入できる。
v0.8.2でLocal AIセットアップを堅牢化し、Python Launcherの指定から実際の `sys.executable` を解決して専用venvを作成する。初回導入順は `BBB終了 -> BBB_LOCAL_AI_SETUP.bat -> BBB_START.bat` とする。
v0.8.3でFundamental Data Collectorを実装。BOJ News RSS / Statistics RSSを取得し、日本語項目をSokudanへSandbox分類する。Federal Reserve Press RSSは英語のため現段階ではCollect Onlyとする。既定15分poll、重複排除、初回Feed大量投入防止、Local AI未READY時の分類待ち再試行を持つ。
v0.8.4でFundamental Replay Lab αを実装。Feed監査ログはappend-onlyを維持しつつ、UI Current Viewはevent_id単位で重複統合する。分類Schema v2では financial_markets を追加。ReplayはBBBが実際に観測した recorded_at をknowledge timeとし、その後のBTC/JPYを5分/30分/1時間/4時間/24時間で照合する。未到来の未来horizonはnullのまま保持し、結果はConfidence Ledgerへ保存する。ReplayはSandbox onlyで売買へ影響しない。BBB終了時にはowned Sokudan processを明示停止する。
v0.8.5でHistorical Fundamental Importを実装。BOJ公式年別アーカイブ（金融政策に関する決定事項等 / 金融政策決定会合における主な意見 / 講演・挨拶 / 記者会見）から過去Eventを取得し、SokudanでSandbox分類する。初期UIは2025年・最大100件。BOJ archiveはdate-onlyのため、正確な時刻を推定せず当日23:59:59 JSTを保守的knowledge boundaryとし、短期5m〜4hは採点しない。初期Historical Replayは24h BTC/JPY反応だけを評価する。UIはAurora Light / Sunrise Gold / Midnight / Sakura Techの4 Skin切替と主要英日併記を追加。
v0.8.6でRun Timingを追加。全background jobで実行開始から完了までelapsed_secondsを計測し、Historical Importは実行中もリアルタイム経過時間をUI表示、Historical Replayはreportへ所要時間を保存する。
v0.8.7でCool Contrast UIへ再設計。Human評価でv0.8.6は明るさを抑えた結果ページ全体のコントラストが弱く見えたため、Deep Navy (#0B1622) + Electric Blue (#2F9EE5) の2色を主軸に固定。Sidebar / workspace / card / metricのsurface階層を明確化し、active navigationはblue left rail、primary actionはflat blue、semantic green/red/yellowは状態表示だけに限定する。4 SkinはGraphite Blue / Deep Navy / Steel Slate / Black Iceとし、すべて同一のcool product UI familyで運用する。
Local AIは別ローカルプロセスとしてBBB起動時に自動起動可能で、GPUなしCPU運用を前提とする。
Local AI未導入・LOADING・OFFLINE・障害時もBBB本体は継続する。
現在の分類結果は売買へ反映せず、Sandbox Ledgerへ保存して精度を検証する。
将来はFundamental Confidence Ledgerでカテゴリ別の有効性を評価し、十分な実績がある範囲だけRisk調整へ利用する。

v0.9.0でGlobal Macro Impact Labを実装。BOJ中心のCase StudyからGlobal / USへ重心を移し、Relevance GateでTier Aだけを採用する。初期SourceはFed FOMC Statement / BLS CPI / BLS Employment Situation。公式発表時刻をknowledge timeとしてBTC/JPYの30m / 1h / 4h / 24h後の絶対値動きを測る。Global Macro Schema v3は rates_liquidity / inflation / employment / regulation_etf / crypto_native / geopolitical / jpy_japan_overlay。英語本文は現行Japanese-only Sokudanへ送らず、Source種別で決定論的に分類する。Impactは発表後の関連測定であり因果関係を主張しない。
v0.9.1でMatched Controlを追加。各Tier-A Eventに対し、同曜日・同じ公式発表時刻の近傍±1/2/3/4週から、import済みTier-A Eventの±24時間を除外した非イベント窓を最大4つ対応付ける。30m / 1h / 4h / 24hでEvent平均絶対値動き、Control平均絶対値動き、Excess、Event/Control Ratio、Event>Control Shareを算出する。通常変動・近いregimeの影響を減らす比較であり、因果関係は主張しない。

v0.8.8でFundamental Confidence Dashboardを実装。Historical Replayのconfidence_ledgerを追加推論なしで読み、24時間方向一致率、平均絶対値動き、カテゴリ別件数/採点数/方向一致率/平均Model Confidence、大きな一致/外れケースを表示する。AlignmentはHuman正解ラベルによるAI分類精度ではなく、risk_on/risk_offと24時間後BTC/JPY方向の一致として明確に分離する。
v0.8.9でHuman Label Reviewを実装。Historical Fundamentalの分類済みケースをHumanがまず50件採点し、Human Category Accuracyと24h Market Alignmentを別指標として管理する。採点中は24h市場結果をUIへ出さず、hindsight biasを抑える。Human labelsはappend-onlyで data/fundamental_review/human_labels.jsonl に保存し、Paper / Risk / Liveへ影響しない。

詳細:
- checkpoints/BBB_FUNDAMENTAL_SENTINEL_CONCEPT_2026-09-29.md
- agents/Local-AI/README.md
- Harness-wide model catalog: ../../agents/Local-AI/README.md
- checkpoints/BBB_V0.8_LOCAL_AI_SANDBOX_2026-09-30.md
- checkpoints/BBB_V0.8.1_LOCAL_AI_PYTHON_FIX_2026-09-30.md
- checkpoints/BBB_V0.8.2_LOCAL_AI_SETUP_FIX_2026-09-30.md
- checkpoints/BBB_V0.8.3_FUNDAMENTAL_COLLECTOR_2026-10-01.md
- checkpoints/BBB_V0.8.4_REPLAY_CLEANUP_2026-10-01.md
- checkpoints/BBB_V0.8.5_HISTORICAL_IMPORT_SKINS_2026-10-01.md
- checkpoints/BBB_V0.8.8_FUNDAMENTAL_CONFIDENCE_2026-10-02.md

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
v0.9.8はWindows向けTrading Research Cockpit、Local AI Sandbox、Global Macro Impact Lab、Matched Control、Robustness Check、Global BTC / JPY Overlay Decomposition、FX Evidence Gate、Global Macro Expansion、4種Cool Skinを持つ。
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
2026-10-01:
- local pytest: 113 passed
- Python compileall: PASS
- UI JavaScript syntax check: PASS
- 5 strategy families available
- Local AI Sandbox: IMPLEMENTED
- Local AI trade influence: OFF
- Fundamental Collector: IMPLEMENTED / SANDBOX ONLY
- BOJ RSS: CLASSIFY
- Fed Press RSS: COLLECT ONLY
- live order path: NOT IMPLEMENTED

- checkpoints/BBB_V0.8.9_HUMAN_LABEL_REVIEW_2026-10-02.md

- checkpoints/BBB_V0.9.0_GLOBAL_MACRO_IMPACT_2026-10-02.md

- checkpoints/BBB_V0.9.1_MATCHED_CONTROL_2026-10-03.md


v0.9.2でRobustness Checkを実装。Matched Controlのevent-level Excessを使い、Median / Q25-Q75 / 10% Trimmed Mean / 最大|Excess| 1件除外平均 / Mean Excessのdeterministic percentile bootstrap 95% CI（2,000 resamples）/ 最大外れケースを表示する。既存v0.9.1のmatched_control_ledger.jsonlが残っていれば再Import・再Replayなしで自動集計する。これらはMatched Sample内の記述的頑健性確認であり、因果関係・統計的有意性・将来の売買優位性を単独では証明しない。

- checkpoints/BBB_V0.9.2_ROBUSTNESS_CHECK_2026-10-03.md


v0.9.3でGlobal BTC / JPY Overlay Decompositionを実装。Tier-A Global Macro Eventをbitbank BTC/JPYとpublic BTC/USD referenceへ同じ公式発表時刻から当て、30m / 1h / 4h / 24hで分解する。BTC/USD referenceはCCXT Coinbaseを優先し、取得失敗時はKrakenへfallbackする。Implied JPY Overlayは (1+BTCJPY return)/(1+BTCUSD return)-1 のcross-rate residualで、実USD/JPYそのものではなくJPY要因と取引所間basisを含む。UIは24h Global BTC |Move| / JPY Overlay |Move| / Global Dominant Shareと、FOMC/CPI/Employment別の各horizon比較を表示。Public read-only / Sandbox onlyで売買影響なし。

- checkpoints/BBB_V0.9.3_GLOBAL_BTC_JPY_OVERLAY_2026-10-03.md


v0.9.4でDirect USD/JPY Validationを実装。v0.9.3のImplied JPY OverlayをDukascopy public historical USD/JPY tick midpointで直接検証し、Overlay = Direct USD/JPY × Basis Residualへ再分解する。各Tier-A Eventについて30m / 1h / 4h / 24hを比較し、Direct FX |Move|、Basis Residual |Move|、FX magnitude share、FX dominant shareをFOMC / CPI / Employment別に表示する。Historical tickはevent-local hour fileだけを取得して data/fx_cache/dukascopy へcacheする。Basis Residualにはcross-exchange BTC basisやmicrostructure差が残り得る。Public read-only / Sandbox onlyでPaper / Risk / Liveへの影響なし。

- checkpoints/BBB_V0.9.4_DIRECT_USDJPY_VALIDATION_2026-10-03.md


v0.9.5でFX Coverage Recoveryを実装。v0.9.4実機初回Direct USD/JPY Validationは62件中3件のみ成功・59件失敗、所要15:41だったため、3件の集計値はpipeline疎通確認としてのみ保持し分析結論には使わない。Dukascopy public datafeedの一時的5xx/timeoutを想定したretry、anchor優先prefetch、controlled repair、run-level failure memoization、最大3並列、cache再利用を追加。Coverage stateをCOMPLETE / PARTIAL / LOW_COVERAGEで明示し、UIへcoverage率・cache/network/retry/failure reason diagnosticsを追加する。

- checkpoints/BBB_V0.9.5_FX_COVERAGE_RECOVERY_2026-10-03.md



v0.9.7でFX Evidence Gateを実装。FRED DEXJPUSの日次公式基準とDukascopy intraday精密層を別レイヤーで評価し、Daily Baseline / Intraday Precisionを個別READY / CAUTION / BLOCKED表示する。FREDが95%以上でもDirect FXが95%未満なら日次基準だけ利用可能とし、30m / 1h / 4hの短期結論はBLOCKEDのまま保持する。FRED fast jobはDONE / 件数 / <1sまたはms所要時間を表示する。Sidebar選択項目は全Skinで濃色背景 + Electric Blue左ライン + 高コントラスト文字に統一し、選択時に文字と背景が同系色で潰れる問題を修正。

- checkpoints/BBB_V0.9.7_FX_EVIDENCE_GATE_2026-10-03.md

## Next / Proposed
- v0.9.8 proposed: Global Macro Expansion.
- Add Tier-A official U.S. events: PCE / Personal Income and Outlays, PPI, GDP.
- Reuse existing official-time replay, matched-control, robustness, BTC/USD decomposition, and FX Evidence Gate.
- Compare new event families against FOMC / CPI / Employment before expanding to Crypto Native Tier-A events.

## v0.9.8 approved scope: Global Macro Expansion
- Add official Tier-A U.S. PCE / Personal Income and Outlays, PPI, and national GDP release families.
- Preserve FOMC / CPI / Employment baseline cohorts.
- Reuse existing official-time replay, matched-control, robustness, BTC/USD decomposition, and FX Evidence Gate.
- Exclude low-priority/state/regional GDP releases from the initial cohort.
- Research-only; no automated trading influence.

v0.9.8でGlobal Macro Expansionを実装。既存FOMC / CPI / Employmentに、BEA Personal Income and Outlays (PCE)、BLS Producer Price Index (PPI)、BEA national GDPを追加。PCE/PPIはinflation、GDPはgrowthへ分類する。BEA公式年次release scheduleとBLS公式年次scheduleの公表時刻をknowledge timeとして使用。GDPは全国GDPのみを初期cohortとし、State / County / Puerto Rico等の地域系を除外する。既存Matched Control / Robustness / Global BTC decomposition / FX Evidence Gateをそのまま再利用。Global Macro import既定上限は200件へ拡張。Public read-only / Research onlyで売買影響なし。

- checkpoints/BBB_V0.9.8_GLOBAL_MACRO_EXPANSION_2026-10-03.md

