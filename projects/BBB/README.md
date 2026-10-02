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
- Human Label Review / 人手ラベルレビュー: Sokudan分類をHuman基準で50件監査
- Historical Fundamental Import: BOJ公式年別アーカイブから過去Case Studyを作成
- UI Skin: Graphite Blue / Deep Navy / Steel Slate / Black Ice
- 主要UI: English / 日本語併記
- Local AI Python: BBB本体と分離した `.venv_local_ai`（Python 3.11-3.13）
- ローカルテスト: 67/67 PASS（v0.8.9 package validation）

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


## Historical Fundamental Import
v0.8.5でBOJ公式年別アーカイブを過去Case Study Sourceとして追加。

- Monetary Policy Decisions / 金融政策に関する決定事項等
- Policy Board Opinions / 金融政策決定会合における主な意見
- Speeches / 講演・挨拶等
- Press Conferences / 記者会見
- default: 2025-01-01 ～ 2025-12-31 / max 100
- Sokudan Sandbox classification
- archive date-only eventは23:59:59 JSTを保守的knowledge boundaryとする
- intraday horizonは採点せず、初期Historical Replayは24hのみ
- 売買 / Risk / Liveへの影響なし

## UI Skin
4 Skinを切替可能。選択はローカル保存される。
- Aurora Mist / オーロラミスト
- Sand Gold / サンドゴールド
- Slate Midnight / スレートミッドナイト
- Dusty Sakura / ダスティサクラ


## v0.8.6 Run Timing / Calm Skin
- background jobは開始から完了までの所要時間を計測。
- Historical Importは実行中のElapsed / 経過時間をリアルタイム表示。
- Historical Replayはreport.json / last_report.jsonへelapsed_secondsを保存。
- 4 Skinは低彩度・オフホワイト/スレート中心に再設計。
- 大きなradial glow、pure white中心、強いgradient、強いshadowを削減。
- 実製品UIギャラリーの情報階層・限定accentの方向を参考にし、特定製品のコピーはしない。


## v0.8.7 Cool Contrast UI
- Main colors: Deep Navy `#0B1622` + Electric Blue `#2F9EE5`
- Sidebar / workspace / card / metricの階層差を強め、ページ内コントラストを明確化
- active navigationはElectric Blueのleft rail
- Primary actionはflat blue
- semantic green / yellow / redは状態表示専用
- Skin:
  - Graphite Blue / グラファイトブルー
  - Deep Navy / ディープネイビー
  - Steel Slate / スチールスレート
  - Black Ice / ブラックアイス
- 4 Skinは色調を大きく散らさず、同じCool Product UI familyに統一


## v0.8.8 Fundamental Confidence Dashboard
Historical Replayの保存済みconfidence ledgerを追加のSokudan推論なしで分析。

- Scored Cases / 採点ケース
- 24H Alignment / 24時間方向一致率
- Avg |Move| / 平均絶対値動き
- Evidence Stage / 標本段階
- Category別: 件数 / 採点 / 方向一致 / 平均絶対値動き / Model Confidence
- Largest Aligned Cases / 大きく一致したケース
- Largest Misses / 大きく外れたケース

AlignmentはHuman正解ラベルによる分類精度ではなく、risk_on/risk_offと24時間後BTC/JPY方向の一致として扱う。


## v0.8.9 Human Label Review
- Historical Fundamentalの分類済みケースをHumanが採点
- 初期Target: 50件
- Human Category: 7カテゴリ
- Human Risk Bias: risk_on / risk_off / unclear（任意）
- 採点中は24h市場結果を非表示
- Human Category Accuracyと24H Market Alignmentを別指標で管理
- AI category別Human一致率と主な修正方向を表示
- labels: data/fundamental_review/human_labels.jsonl
- Sandbox only / Trade influence OFF
