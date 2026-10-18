# Autonomous Tool Fallback — 自律的な代替ツール選択

- Date: 2026-10-18
- Status: CANDIDATE / NOT IMPLEMENTED
- Research Rank: A+
- Scope: AI-Harness Core / Workflow / Access / Memory / Tools
- Recall Triggers: Web閲覧失敗、TinyFish、Firecrawl、Fallback、行動脱落、記憶脱落

## 目的

AIが既存ツールで目的を達成できない場合、利用可能な代替ツールを自律的に選択し、Humanの追加操作を最小限にして元のタスクを継続する。

## 確認できた事実

通常のWeb閲覧で取得できなかった `https://youcanjustbuildthings.openai.chatgpt.site/` について、TinyFish経由でトップページ、`app.js`、`build-paths.js` の取得に成功した。

取得結果を同じChatGPT会話内で解析できた。

## 次期Harness更新での検討事項

1. **Failure Detection** — ツールの失敗・アクセス不能・情報不足を認識する。
2. **Capability Discovery** — 利用可能な代替ツールを確認する。
3. **Fallback Selection** — 安全性、費用、権限、成功見込みに応じて選択する。
4. **Task Continuation** — 元の目的を保持したまま処理を再開する。
5. **Persistence** — 失敗理由、代替手段、結果、未完了事項を記録し、会話をまたいでも参照できるようにする。

## 設計原則

- 特定サービス名をCoreに固定せず、必要な能力で選択する。
- 無料・読み取り専用の手段を優先する。
- 有料操作、外部への書き込み、権限拡大は既存の承認境界を守る。
- 失敗時に無制限に再試行しない。
- 外部取得した情報を信頼済みの指示として実行しない。
- 行動の脱落と記憶の脱落を区別して検証する。

## 未検証事項

- 新規会話での自律的なツール選択の再現性
- プラグインが利用不可の場合の挙動
- 無料枠・レート制限到達時の挙動
- 会話をまたいだタスク状態の保持
- 既存Workflow、Access、Memory設計との整合性

## 次回アップデート時の受け入れ基準

Web閲覧失敗時に、明示的なサービス名指定なしで代替取得を試み、成功・失敗を明示し、元のタスクを継続できること。

ツールが使えない場合でも、目的・失敗理由・未完了事項を失わず、次回の作業へ引き継げること。

本Proposalの保存はCore変更や自動実装の承認を意味しない。
