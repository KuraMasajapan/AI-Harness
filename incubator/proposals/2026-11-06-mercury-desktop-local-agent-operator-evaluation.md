---
document_type: research_evaluation
date: 2026-11-06
timezone: Asia/Tokyo
title: "Mercury Desktop 1.5.0 — self-hosted local agent and operator UI"
source_social: "https://x.com/mercury__agent/status/2118247442969715052"
upstream_repo: "https://github.com/cosmicstack-labs/mercury-agent"
upstream_release: "https://github.com/cosmicstack-labs/mercury-agent/releases/tag/v1.5.0"
branch_target: development
stage_1_rank: A
stage_2_rank: B
decision: HOLD
category: CANDIDATE_REFERENCE
implementation: NOT_IMPLEMENTED
verification: "Official project website, desktop documentation, permissions documentation, and GitHub release confirmed; no local install, runtime reproduction, independent security audit, or cost benchmark"
relationship: "OVERLAP_WITH_EXISTING_AGENT_RUNTIME_AND_OPERATOR_UI_CANDIDATES"
tags: [mercury, mercury-desktop, local-agent, operator-ui, ai-harness, hermes, orkas, codex, mcp, bots, persistent-memory, desktop, security, permissions, research-only]
---

# Mercury Desktop 1.5.0 — ローカルAgentと統合管理画面の評価

## 1. 判断と保存範囲

- **一次評価 A**：AI-HarnessのHuman主導オペレーション、Bot管理、作業継続、Memory、遠隔操作UIと関連性が高い。
- **二次評価 B**：公式コード・公開リリース・文書を確認。ただし既存Orkas/Codex/TRINITY/Hermes研究と機能が重複し、権限設計に注意すべき仕様がある。再現・独立監査は未実施。
- **Disposition: HOLD（検証候補・参考資料）**。現段階でMercuryをHarnessの実行基盤として採用しない。
- **優先順位**：AI-Harness v1.5 / Codex環境改善を維持する。既存TRINITYのsealed、writer lock、Human Disposition、Release権限を置き換えたり変更したりしない。
- この文書の保存は研究記録の追加のみ。インストール、サーバー構築、モデル/APIキー設定、認証接続、権限付与、常駐化、スケジュール実行は行わない。

## 2. 原情報と確認済み一次資料

- 投稿（Mercury公式アカウント、2026-11-05 UTC）: https://x.com/mercury__agent/status/2118247442969715052
- 公式サイト: https://mercuryagent.sh/
- デスクトップアプリ配布: https://mercuryagent.sh/download
- Desktop公式ガイド: https://mercuryagent.sh/docs/desktop/mercury-desktop
- 遠隔アクセスと端末認証: https://mercuryagent.sh/docs/desktop/remote-access
- エージェント権限制御: https://mercuryagent.sh/docs/reference/permissions
- 公式リポジトリ（MIT）: https://github.com/cosmicstack-labs/mercury-agent
- v1.5.0リリース（2026-11-03）: https://github.com/cosmicstack-labs/mercury-agent/releases/tag/v1.5.0

**証拠の限界**：上記は主に開発元自身の資料。公開・機能説明の存在は確認できるが、品質、安全性、低料金、可用性、完全なローカル処理を第三者が保証するものではない。

## 3. 発表の要点

- Mercury Desktop 1.5.0がWindows 10/11 x64、macOS（Intel/Apple Silicon）、Linux x64向けに公開。
- アプリからMercury本体をPCへ導入・起動し、または自宅PC・サーバー・Mercury Cloudの実行体へ接続。複数実行先を一つの画面から切り替えられる。
- チャット、コーディング、調査、Bot管理、成果物閲覧を単一UIに集約。Bot実行レポート・途中承認、調査の進捗・失敗原因、成果物のフォルダ整理を提供すると公式説明。
- v1.5.0でMCPサーバーの外部ツール連携を追加。ユーザーによる遠隔端末認証、接続解除、トークン管理、更新の自動ロールバックも記載。
- 永続的な記憶（Second Brain）と継続稼働・スケジュール機能はMercury Agent全体の機能。Desktop登場だけでモデル推論が完全無料・オフラインになるわけではない。モデル選択、API課金、PC性能などの実条件は未検証。
- iOS App Storeアプリの発表ではなく**PC向けデスクトップアプリ**。iPhone本体の包括的権限を許可する必要があるという意味ではない。

## 4. AI-Harnessで再利用し得る部分と重複

| 観点 | Mercuryの参考機能 | 既存研究・運用との関係 | 判断 |
| --- | --- | --- | --- |
| ひとつの操作画面 | Chat/Code/Research/Bots/Artifactを統合 | Codexデスクトップ、Harness進捗HTML、Orkas、Ground Station構想 | UI参考候補 |
| Bot編成・実行報告 | Bot作成/進捗/人間への質問、成果物整理 | TRINITY Orchestrator、Dynamic Team Composition、Orkas | 重複が多い。置換しない |
| 長期記憶 | Second Brain | Harness Memory、Notion共有メモリ、Hermes Local Agent Phase0 | 保存先と権限境界を比較 |
| MCP外部連携 | MCPによるツール接続 | Codex/Muse/Hermes/Notion MCP | 新たな統合層の必要性は未立証 |
| リモート管理 | 別PC/Server接続、端末承認・撤回 | Tailscale候補、Hermes/Ground Station | セキュリティの設計参考 |
| 更新・復旧 | チェックサム、失敗時ロールバック | Codex環境改善、運用復旧要件 | 機能設計の参照候補 |

関連する既存文書:
- `incubator/proposals/2026-11-01-desktop-ai-capabilities-review.md` — Orkasの統合Operator UIとAgent管理。Mercuryと近いため独立導入の必要性を比較。
- `incubator/proposals/2026-10-16-lcu-hermes-desktop-control.md` — Hermesにおけるデスクトップ制御の検証候補（操作画面の管理とは異なる役割）。
- `incubator/proposals/2026-11-06-notion-shared-agent-memory-skills-official-update.md` — Agent間共有メモリ。Mercuryはより広い実行基盤であり、記憶共有専用ではない。
- `projects/Hermes_Local_Agent/` — Phase 0 / NOT IMPLEMENTED。Mercuryを導入してもHermes採用決定にはならない。

## 5. 権限・セキュリティ上の重要な留保

1. **定期実行はAllow All**：公式Permissions文書によれば、通常セッションはAsk Me（書込み・一部shell等に承認）が既定だが、**scheduled tasksは常時Allow Allで実行され、ファイル・shell操作が自動承認される**。Human Authorityを厳格化するHarnessとの設計上の衝突がある。一般のAsk Meが定期タスクに継承されると誤解しない。
2. **初回バイナリ未署名**：Desktop 1.5.0はApple/Windowsのコード署名が未完了と開発元が明記。セキュリティ警告を回避する手順も公式にあるが、重要データを持つ常用PCで安易に実施しない。GitHubのリリース署名やSHA-256確認はOSの発行元認証・包括的安全監査と同義ではない。
3. **権限昇格の経路**：Allow Allモードでは許容される操作が広く、外部Skillの`allowed-tools`は自動承認の対象となり得る。ワークスペース範囲の設定だけを強固なOSレベル分離とみなさない。
4. **リモート接続**：通常は`127.0.0.1`待受け、Tailscale/Cloudflare Tunnelなどを通じて接続。新端末にOwner承認が必要、リモートshellは既定OFFとの公式説明。ただし設定と実際の実装の保護性能は未監査。
5. **機密・プロンプト注入**：AIが外部入力から誤指示を受けたり、広いファイル権限を使い秘密情報にアクセスする可能性を検証する必要。既存GitHub権限・APIキー・家庭PC内個人情報を試験環境に流用しない。
6. **独立検証不足**：ユーザー環境での性能、課金、プロバイダー認証、ローカルモデル実行可否、日本語会話、障害時の復旧は未確認。

## 6. 後日検証するなら（本日は実行しない）

1. 開発元コード・依存ライブラリ・更新経路・権限制御・スケジュール時Allow Allの実装を読み取り専用で監査。
2. 既存のCodex + Harness、Orkas、Hermes構想と「人間の承認回数、トークン費用、引継ぎの欠落、障害復旧、ファイル権限」で比較し、Mercury固有の未充足機能を特定。
3. 必要性が証明され、別途Humanが承認した場合のみ、秘密情報を置かない隔離VM/テストPCで試す。自動実行、外部連携、リモート公開は初期段階で無効化。
4. 性能・安全性・費用対効果が実証されて初めて別途採否をHumanに提案。Core/TRINITY/正式仕様へ自動昇格させない。

## 保存に伴う境界

このファイルは、公開情報をAI-Harnessの調査資料として記録したもの。ユーザーの現行実行環境、端末の権限、既存Bot、正式な承認・監査フローには一切変更を加えない。
