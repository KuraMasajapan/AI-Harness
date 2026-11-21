# crosswalk — ChatGPTプラグイン研究候補

- Date: 2026-11-21
- Origin: Human提供のChatGPTプラグイン一覧スクリーンショットと公開資料
- Stage 1 Rank: A+
- Stage 2 Rank: A+（一次公開資料に基づく暫定、実動作は未検証）
- Decision: CANDIDATE
- Status: KNOWLEDGE / FUTURE VALIDATION CANDIDATE / NOT IMPLEMENTED
- Evidence: 確認できたサービス説明と公式掲載機能のみCONFIRMED、実運用効果・安全性はUNVERIFIED
- Research-only save approved by Human's B-and-above standing instruction. This does NOT authorize installation, account linking or production adoption.

## 一次資料
- https://crosswalk.to/docs
- https://crosswalk.to/agents/dots/tasks
- https://github.com/jekajeka2/crosswalk-plugin

## 内容とAI-Harness関連性
Muse、ChatGPT、Codex、dots等のMCPエージェントが共通掲示板でメッセージ、タスク、ファイルをやり取り。Streamable HTTP + OAuth。AI-HarnessのTransport、TRINITYの受け渡し、家族共有ボードとの比較が有用。

## 未確認事項・安全性
既存の共有ボード・アクセス境界と重複。外部SaaSへデータを複製しない。プライベート情報、権限、監査、メッセージ取り違えを試験。公開リポジトリにはサーバー本体のソースは含まれない。

## 最小検証
機能・料金・認証権限を再確認し、ダミーデータ・読み取り専用の最小テストを実施する。新規アカウント作成、実データ接続、正式採用、Core変更は実施しない。

## Recall triggers
crosswalk、Dots、ChatGPT plugin、MCP、AI-Harness、research candidate
