# Factory Droid — 個人開発者向けBYOI無料化

- 評価日: 2026-11-26 JST
- Stage 1: A++
- Stage 2: A+
- Decision: CANDIDATE
- Evidence: CONFIRMED（公式無料化発表） / UNVERIFIED（接続・詳細条件）
- Dedup: UNCONFIRMED
- Implementation: HOLD / NOT IMPLEMENTED

## 根拠
- https://x.com/factory/status/2125637084522447202
- https://factory.com/
公式Xの2026-11-25 17:05 UTC投稿は、個人開発者が自前の推論を持ち込む場合にFactoryを無料化し、期間限定でDroid Computerの無料時間も付与すると明記。推論そのものの無償化ではない。公式料金ページの直接取得は失敗。クラウド無料時間数・期限・超過条件は未確認。

## 有用性
Droidは開発エージェントの候補。Codex代替、モデル切替、TRINITY補助、無料APIを利用した開発を検討する。Gemini API、OrcaRouter、OpenRouter、ローカルLLMとの接続は検証候補であり、成功を確認していない。ChatGPTアカウント連携の具体的条件・Codexとの利用枠共有・利用規約も再確認する。Droid Computerは恒久無料常駐環境とみなさない。

## 重複・代替
developmentのファイル一覧を検索し、Factory固有のファイル名は発見せず。全文・Airtable未照合。
関連: 2026-10-12-freellmapi-free-provider-routing.md、2026-10-28-hermit-harness-adapter-evolution.md、2026-11-22-sign-in-with-chatgpt-token-sharing-oss.md、2026-11-23-gemini-api-cli-free-tier-deep-dive.md。
既存Codex/OpenCode等に対する追加価値は無料の開発ハーネスと推論先の選択性。実用性能・保守性・権限・データ送信先は未検証。

## 最小検証
別途承認後、公式料金・規約・認証・データ処理条件を再確認し、無料APIを明示指定した非機密の小規模リポジトリで接続、編集、テスト、消費量を計測。課金への自動切替を防止し、秘密情報を送信しない。既存環境を変更しない。

## Recall triggers
新規開発、Codex利用上限、無料開発エージェント、BYOI、Factory、Droid、Gemini API、OrcaRouter、クラウド開発。
保存は研究記録のみ。導入・認証・実装の承認ではない。
