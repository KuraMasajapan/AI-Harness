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
- ローカルテスト: 26/26 PASS（2026-09-29確認）

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
