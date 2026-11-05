---
document_type: research_evaluation
date: 2026-11-06
timezone: Asia/Tokyo
title: "Notion Shared Agent Memory and Skills via MCP — official update"
source_primary: "https://x.com/NotionHQ/status/2118059335930744999"
source_secondary: "https://x.com/hidekazu_s/status/2118301461432164541"
branch_target: development
stage_1_rank: A+
stage_2_rank: A
decision: CANDIDATE
implementation: HOLD / NOT_IMPLEMENTED
evidence: "OFFICIAL RELEASE AND DOCUMENTATION CONFIRMED; USER ENVIRONMENT, CONNECTOR PERMISSIONS AND CROSS-AGENT REPRODUCTION UNVERIFIED"
dedup: "NEW OFFICIAL FEATURE VALIDATION; RELATED EXISTING CONTEXT_VAULT RESEARCH"
tags: [notion, mcp, personal-memory, agent-memory, shared-context, skills, cross-agent, codex, muse, hermes, security, research-only]
---

# Notion — Shared Agent Memory / Skills via MCP (official update)

## 1. Decision

- **Stage 1: A+** — AI-Harnessの目的である複数AI間の永続記憶・作業の継続性と高い適合。
- **Stage 2: A** — Notion公式が機能と仕様を公開。Kody等との重複と運用上の信頼境界があるため、実環境での採用価値は未実証。
- **Disposition: CANDIDATE / IMPLEMENTATION HOLD**。研究材料として保存。Notion連携、権限付与、データ移行、スキル自動同期、Core/TRINITY変更を行わない。
- **優先順位**：AI-Harness v1.5 / Codex環境改善を維持。こちらの研究を理由に進行中の作業を中断しない。

## 2. 情報源

- ユーザー提示の日本語紹介投稿（2026-11-05 JST）: https://x.com/hidekazu_s/status/2118301461432164541
- Notion公式発表「Give all your agents one shared brain in Notion」（2026-11-05 JST）: https://x.com/NotionHQ/status/2118059335930744999
- 公式製品更新「Notion 3.8: Context for your agents」: https://www.notion.com/releases/2026-10-13
- Notion MCP概要: https://developers.notion.com/guides/mcp/overview
- Personal memories / Skills / 具体的MCPツール: https://developers.notion.com/guides/mcp/tools-skills-agents
- Notion Skills via MCP: https://developers.notion.com/guides/mcp/notion-skills
- MCP接続方法（Codex, Claude Code, Hermesを含む）: https://developers.notion.com/guides/mcp/get-started-with-mcp
- セキュリティ: https://developers.notion.com/guides/mcp/mcp-security-best-practices

## 3. 何ができるか — 公式確認済み

1. **共有メモリ**：MCPに接続したAIクライアントが、ユーザーの指定した好み・訂正・判断等をNotion内の**個人Memoriesデータベース**に保存し、後のセッションや別クライアントから呼び出せる。初回保存時にMemoriesデータベースと要約用Aboutページが作成されると公式説明。
2. **ユーザーによる編集**：記憶を閲覧、編集、削除可能。個人記憶は非公開であり、接続AIがもともとアクセス権のないページへの権限を取得するものではない。
3. **Skills**：Notionページを再利用可能なSkillとして管理し、MCP接続クライアントが読んで利用できる。公式MCPにはSkill化、取得、ダウンロード、アップロード等の機能が記載される。必要に応じてSKILL.md形式でエクスポート可能。
4. **対応クライアント**：公式はChatGPT、Claude、Muse、Bot等を例示し、Codex CLIとHermesについてもMCP手動設定手順を掲載。
5. **プランと接続条件**：公式によれば個人メモリMCPは、記憶機能が有効な**user-backed（個人ユーザーを主体とする）接続**を通じて全プランで利用可能。**workspace-owned接続では不可**。クライアントごとのMCP/Plugin対応・利用枠は別途確認。

**重要な範囲**：MCPをつないだだけではChatGPT・Claudeなどの既存の全会話履歴は自動移行しない。どの情報をNotionに残すか明示的な入力・記録フローが必要。「共有脳」はNotionに保存された情報の共有を指す。NotionがLLMの内部状態やモデルの記憶を統合するわけではない。

## 4. Kody / AI-Harnessとの関係

| 選択肢 | 主機能 | 向いている役割 | 判断 |
|---|---|---|---|
| **AI-Harness GitHub** | 正式仕様、設計、コード、TRINITYの監査・承認記録 | **Human AuthorityとSource of Truthの一次保管** | 維持 |
| **Notion共有メモリ** | 人間が読める記憶、作業前提、Skills、MCP検索・編集 | AI間の作業用文脈を人間が可視化・編集 | CANDIDATE |
| **Kody** | 記憶だけでなく認証情報、保存プログラム、スケジュールジョブ、クラウド実行 | Agent専用の実行・認証・自動化基盤 | 別途評価、未導入 |
| **Obsidian / 既存Memory** | 個人ノート、参照・検索用情報整理 | 既存Vault・保管方針との比較 | 移行未決 |

Notionを追加しても、TRINITY sealed artifacts、writer lock、Human Disposition、レビュー／Release権限を置き換えない。Notion記憶は便利な**派生文脈／キャッシュ**であり、GitHub一次記録と矛盾した場合はHuman確認なしに正式仕様へ昇格しない。

## 5. 既存記録の重複確認

既存の **`research/2026-10-27-context-vault-startup-injection-reference.md`** はNotionを使う個人のContext Vaultと起動時文脈注入の参考事例。投稿画像のみで実装手順・権限・同期・安全性が不明なため、`REFERENCE / ABSORB CONCEPT` と評価していた。

**今回の新規性**は2026-11-05の**Notion公式**による共有メモリMCP発表と、公式ドキュメントで確認できる個人記憶・Skill操作・接続方式・権限制約。既存資料を削除・上書きしない。既存の「共有文脈は信頼境界を区切って対象Agentごとに整形する」原則と併用する。

関連する別テーマ：`incubator/proposals/2026-10-12-claude-mem-persistent-context.md`、`incubator/proposals/2026-10-31-codebase-memory-mcp-evaluation.md`。後者はコードグラフ索引が中心で、個人の複数AI共有メモリとは目的が異なる。

## 6. リスク・未確認事項

- **共有汚染**：誤った情報や悪意ある外部データが共有Memories/Skillsへ入り、複数の接続AIに広がる可能性。由来・検証時刻・信頼区分・明示的なHuman承認で分離。
- **アクセス権**：Notion MCP接続AIは、接続したユーザーに見えるコンテンツを読み取り、許可に応じて更新可能。専用の検証ページ、最小権限、編集前の確認を推奨。組織管理の一部機能は上位プラン限定。
- **外部転送**：Notion公式も、MCPを使うAIクライアントが取得した情報をNotion外へ送るリスクとプロンプトインジェクションを警告。機密情報、認証キー、個人情報、private GitHub内容を安易に登録しない。
- **同期の意味**：同じSkillをNotionから取得できることと、各AIへ自動・即時にインストール／有効化されることは別。実環境における手順・整合性は未検証。
- **動作再現性**：BOSSのChatGPT Plus、Codex CLI、Muse、Hermesでの実動作、アプリ側サポート、プランの具体的制限、API使用量、料金、遅延、衝突解決は未確認。
- **GitHubとの二重管理**：正式仕様／記録の写しを無制御にNotion側で更新させない。優先ソースと復旧方法を決める必要がある。

## 7. もし後日試すなら（まだ実行しない）

1. Notionに**個人用の隔離した試験ページ**を設け、ダミーの好み・プロジェクト要約だけを登録。機密・秘密・実プロジェクトの正式仕様は入れない。
2. 信頼済みのAIクライアントを**1つだけ**接続し、読み取りと明示的な保存が可能かテスト。認可範囲と撤回手順も確認。
3. 2つ目のクライアントから同じテスト記憶を読み戻し、誤認・重複・古い情報を観察。
4. Skillを1件だけ試し、Notion上の編集内容と各クライアントでの読取結果を比較。自動同期とは仮定しない。
5. 有用性／運用負担／セキュリティ／GitHubとの重複を評価し、**正式採用・保存先変更は別途Human承認**を得る。

## 保存時の境界

- このファイルの追加のみ実施。Notionアカウント作成、MCP接続、Pluginインストール、権限付与、外部サービスへのデータ送信、TRINITYやHarness本体の変更は行わない。
- 調査情報と実装判断を分離し、Harness v1.5の主目的を変えない。
