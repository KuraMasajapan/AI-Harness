# BITBANK-BOT (BBB)

## 概要
BITBANK-BOT（略称 BBB）は、bitbank を対象とした暗号資産取引Botプロジェクト。

当面の方針は **エージェントなし・LLMなしで動く軽量Bot** を先に完成させ、Paper Trade / Backtest / Historical Replay / 改善ループで十分に検証した後、必要に応じてAI Supervisorを追加する。

## 現在位置
- 開発段階: Research / Paper
- 実注文: 未実装
- 取引所: bitbank
- 接続層: CCXT
- 初期対象: BTC/JPY
- 現物のみ
- 空売りなし
- レバレッジなし
- 基準戦略: EMA + RSI
- 為替分離: USD/JPYを使ったFX-aware検証を実装済み
- Local AI Sandbox: Sokudan CPU統合済み（売買影響OFF）
- Fundamental Data Collector: BOJ RSS自動分類 + Fed RSS収集
- Fundamental Replay Lab α: 観測済みイベントと後続BTC/JPY反応をSandbox照合
- Local AI Python: BBB本体と分離した `.venv_local_ai`（Python 3.11-3.13）
- ローカルテスト: 43/43 PASS（v0.8.4 package validation）

## Source of Truth
bitbank公式API仕様:
https://github.com/bitbankinc/bitbank-api-docs

API仕様に関しては上記公式リポジトリを一次資料とする。

## セキュリティ境界
- API Key / API Secret をAI-Harnessへ保存しない
- API Key / API Secret をChatGPT・GitHub・README・ログへ貼らない
- 将来のLive運用ではローカル環境変数またはSecret Storeから読み込む
- 出金権限をBBBへ付与しない方針
- Live Tradingは専用Gate通過前に有効化しない

## 主要文書
- `CURRENT_SPEC.md`: 現在の設計・安全境界
- `DECISION_LOG.md`: Human決定と重要判断
- `checkpoints/`: 節目ごとの状態記録

## AI発展構想
BBBのAI拡張は `agents/` 配下で管理する。

- `agents/README.md`: BBB向けAI発展マップ
- `agents/Local-AI/README.md`: Fundamental Sentinel向けLocal AIの役割・Benchmark・段階導入
- Harness全体のモデル情報は `../../agents/Local-AI/README.md` をSource of Truthとして参照する

BBBではモデル情報を重複保存せず、プロジェクト固有の「何に使うか」「どのGateを通すか」だけを記録する。


## Fundamental Data Sources
v0.8.3で以下の公開SourceをSandbox接続。

- BOJ News RSS: https://www.boj.or.jp/rss/whatsnew.xml
- BOJ Statistics RSS: https://www.boj.or.jp/rss/statistics.xml
- Federal Reserve Press RSS: https://www.federalreserve.gov/feeds/press_all.xml

BOJはSokudanへ自動分類。Fedは英語のため現段階ではCollect Only。
既定15分poll。取得結果は売買へ影響しない。


## Fundamental Replay Lab α
v0.8.4で、分類済みFundamental Eventをbitbank Public BTC/JPY履歴と照合するReplay Labを追加。

- knowledge time: BBBが実際に観測した `recorded_at`
- forward horizons: 5m / 30m / 1h / 4h / 24h
- 未到来horizon: nullのまま保持
- output: Market Dataset / Confidence Ledger / Report
- Sandbox only / Trade influence OFF
- Feed UIは同一event_idを1行に統合表示。監査JSONLはappend-onlyを維持
- BBB終了時にowned Sokudan processを明示停止
