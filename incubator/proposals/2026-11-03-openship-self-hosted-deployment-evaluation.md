---
document_type: research_evaluation
date: 2026-11-03
timezone: Asia/Tokyo
title: "OpenShip — self-hosted deployment and MCP operations platform"
source_post: "https://x.com/EngMoElgaraihy/status/2117086174032400883"
upstream_repository: "https://github.com/oblien/openship"
branch_target: development
stage_1_rank: A+
stage_2_rank: A
dedup_status: "NEW_DEDICATED_PROPOSAL_WITH_FUNCTIONAL_OVERLAP; CONTENT_WIDE_CHECK_INCOMPLETE"
evidence: "CONFIRMED_OFFICIAL_DOCUMENTATION; PERFORMANCE_AND_SECURITY_NOT_INDEPENDENTLY_REPRODUCED"
decision: CANDIDATE
implementation: "HOLD / NOT_IMPLEMENTED"
human_approval: "2026-11-03: user explicitly instructed saving the preceding OpenShip assessment; no implementation authority"
tags: [openship, self-hosting, deployment, paas, devops, ci-cd, mcp, codex, hermes, low-cost, infrastructure, research-only]
---

# OpenShip — 自己ホスト型デプロイ・MCP運用基盤の評価

## Decision / 概要

- **Stage 1: A+** — 低コストの個人用AI基盤、複数アプリの公開・管理、AIエージェントからの運用支援に関連性が高い。
- **Stage 2: A** — 実体と主要機能は公式リポジトリ・ドキュメントで確認できるが、Coolify / Dokploy等と重なり、AI-Harness固有の優位性は未測定。
- **Research: CANDIDATE / Implementation: HOLD**。現時点でインストール、サーバー接続、API/MCP登録、アカウント作成、本番移行はしない。
- **Evidence**: プロジェクト実在・機能仕様は公式資料レベルでCONFIRMED。性能、安全性、安定稼働、価格優位性の独立再現はUNVERIFIED。

## Origin / 投稿と広告性

2026-11-02 JST公開のX投稿（Mo Elgaraihy）は、OpenShipを「Vercel/AWSへの無料の代替」と紹介。TinyFishで投稿本文と返信スレッドを確認した。Xには **Paid partnership**（有料提携）の表示があるため、実体を確認するための情報の入口として扱い、広告上の効果やコストゼロの主張をそのまま採用しない。

- Original: https://x.com/EngMoElgaraihy/status/2117086174032400883
- Promoted project: https://x.com/openshipio/status/2078143909125923137
- Upstream: https://github.com/oblien/openship
- Official docs: https://openship.io/docs/
- Developer: Oblien / https://openship.io/about

## Official verification / 主張ごとの検証

| Claim | Verified scope / qualification |
| --- | --- |
| 100% open source / free | Openship-authored codeはApache 2.0、self-hostedソフトウェアは無償。iRedMail等の同梱第三者コンポーネントには別ライセンスがある。VPS、通信、ストレージ、運用・監視、バックアップ費用は消えない。 |
| Git deployment, CI/CD | Gitを起点とするビルド・デプロイ、Webhook、ダッシュボード、CLI、デスクトップ操作がREADMEと公式Docsに記載されている。 |
| Zero downtime / rollback | 以前の成功済みリリースへ戻す操作と保持済みビルドの再利用が公式ガイドにある。ただし構成依存で停止ゼロの保証はできず、ロールバックはアプリコード中心でDBとボリュームを巻き戻さない。 |
| PostgreSQL, Redis, MongoDB, Supabase, Kafka | 前四者はREADME/カタログ等で確認。Kafkaの個別サポート範囲は今回の一次資料確認では未確定。 |
| Built-in mail | self-hostedでSMTP/IMAP・Webmailのセットアップを提供。DNS・逆引き、ポート25、配信レピュテーション等の運用条件を別途満たす必要あり。Cloud側のメール提供と混同しない。 |
| MCP / AI-managed server | /api/mcp のHTTPエンドポイント、OAuth 2.1、read-only/full control、リソース単位のgrantが文書化されている。ただし一部のMCPツールはデプロイやリソース変更ができ、Human承認・監査境界を自動的には代替しない。 |

Official sources:
1. https://github.com/oblien/openship/blob/main/README.md
2. https://openship.io/pricing
3. https://openship.io/docs/mcp
4. https://openship.io/docs/guides/rollback-redeploy
5. https://openship.io/docs/guides/email-webmail
6. https://openship.io/apps

## Why relevant to AI-Harness / 適合性

- **Hermes Local Agent / future Ground Station:** 自分が管理するLinuxサーバーへアプリ、データベース、管理画面を配置する基盤の比較対象。Hermes Phase 0のままであり、統合可否は未確認。
- **Codex / AI-Harness:** MCP経由でデプロイ、ログ、稼働状態を閲覧・操作できる可能性。最初は読み取り専用権限のみで検証する。
- **Web Projects:** 公開する複数サイト・WebアプリのCI/CD、ドメイン、証明書、ロールバックの管理が候補用途。
- **TRINITY:** インフラを用意できてもsealed artifacts、A/B独立実行、評価、Human dispositionの正しさは別問題。既存TRINITYの役割・承認境界を置き換えない。
- **BBB:** 管理画面や付属サービスの配置は研究対象になり得るが、実資金・注文・本番戦略の操作とは結び付けない。

## Overlap / 既存研究・代替との比較

2026-11-03にAI-Harness developmentのrecursive tree（446 paths）でOpenShip専用Proposalのファイル名が見当たらないことを確認。関連するProposalも個別確認した。ただし全446ファイルの本文を網羅検索したわけではないため、既出の言及なしと断定しない。

- incubator/proposals/2026-09-20-accessible-zero-cost-agent-infrastructure.md — 低コスト・既存OSS活用の原則。OpenShipはその具体的運用候補。
- incubator/proposals/2026-10-20-cloud-harness-mcp.md — コーディング作業環境/ツール搬送のMCP。OpenShipのデプロイ管理とは主用途が異なる。
- incubator/proposals/2026-10-21-vercel-durable-harness.md — 永続的な実行履歴・再開。OpenShipのアプリ公開/管理とは別レイヤ。
- Vercel Drives既存研究 — ファイル永続化とFork。OpenShipのデプロイ運用はその代替ではない。
- Coolify: https://coolify.io/docs/core/what-is-coolify — 自己ホスト型PaaS、Docker/SSH/CI/CDが強く重複。
- Dokploy: https://docs.dokploy.com/docs/core — 自己ホスト型デプロイプラットフォームで機能が重複。

OpenShipの比較焦点は、特にMCPの権限粒度、UI+CLI+SDKの統合、メールや周辺サービス管理での実質的な運用差。単にOSS/無料という理由で採用しない。

## Security, operations and uncertainty

- 自己ホスト時のCompose構成はホストのDocker socketをAPIコンテナへマウントし、ホスト級の強い操作権限を持つ。インターネットや信頼できないネットワークへ管理APIを無防備に公開しない。
- MCPはOAuthと権限限定を提供するが、実運用では最小権限、操作のHuman承認、監査、接続の取り消し、秘密情報の範囲を別途確認。
- 2026-09-05の公式SECURITY.mdには3件のHigh severity authorization gapを扱った限定的コード監査があり、同文書の2026-09-16追記は一部を「PR #892 merge待ち」と記す。GitHub PR #892 は実際に2026-09-16にmerged済みであり、この文書のmerge待ち表記は古い。修正PRの存在は完全なセキュリティ認証ではない。
- 専用VPS・DNS・SSL・メール到達率・データバックアップ・更新/障害対応・容量を総保有コストに含める。公式のクラウド料金とself-hostedのソフトウェア無償を混同しない。
- READMEとドキュメントは活発に更新される。調査時点のmain説明を固定リリース版の動作保証として扱わない。

Primary security references:
- https://github.com/oblien/openship/blob/main/SECURITY.md
- https://github.com/oblien/openship/pull/892
- https://github.com/oblien/openship/blob/main/docker/docker-compose.yml
- https://openship.io/docs/security/auth

## Small future validation / 将来の最小検証（未承認・未実行）

必要性が発生した場合に限り、秘密情報のない使い捨てLinuxホスト、公開不要のテストアプリ、固定バージョンを用いて以下を比較する。

1. 既存GitHub/サイト公開手段、Coolify、Dokploy、OpenShipのセットアップ手間と維持管理時間。
2. 同一アプリのdeploy、失敗時restore、ビルド履歴、停止時間、ログ、利用CPU/RAM/ディスク。
3. MCPの読取専用・リソース範囲制限を確認し、書込みやserver操作が拒否されるか。
4. Docker socket、ネットワーク公開、資格情報、バックアップ、更新失敗時の回復。
5. Codex/ChatGPT/現行フローだけで十分であれば採用しない。

No software installation, token creation, API call, cloud enrollment, DNS, deployment, MCP registration, Core, TRINITY, BBB, Hermes, or production change is authorized by the research record.

## Recall triggers

OpenShip, Openship, oblien/openship, self-hosted PaaS, self-hosting, VPS, deployment, CI/CD, Git push-to-deploy, MCP deployments, infrastructure control plane, Hermes server, Ground Station, Coolify, Dokploy, rollback, web hosting, SSL, mail server, 低コスト基盤, 自己ホスト, サーバー管理, アプリ公開。

## Persistence and approval

2026-11-03、Humanが前段の評価を「保存して」と明示承認。保存対象は本評価Proposal 1件のみ。実装・インストール・既存ProposalやCore/TRINITY/BBBの変更は承認対象外。
