---
document_type: research_evaluation
date: 2026-10-24
timezone: Asia/Tokyo
title: "Tailscale as an AI-Harness private connectivity layer — Muse integration case"
primary_subject: "Tailscale"
secondary_case: "Meta Muse"
source_post: "https://x.com/studio_yebisu/status/2113660702439391318"
stage_1_rank: A++
stage_2_rank: A+
decision: CANDIDATE
implementation: HOLD / NOT APPROVED
evidence_status: "X POST CONFIRMED; TAILSCALE OFFICIAL MUSE INTEGRATION DOCUMENTED; HARNESS INTEGRATION NOT TESTED"
human_approval: "2026-10-24: save complete research with Tailscale as the central theme, not Muse"
tags: [tailscale, tailnet, remote-access, muse, ai-agent, mobile, local-first, network-security, human-approval, hermes, research-only]
---

# Tailscale — AI-Harnessのプライベート接続レイヤー候補（Muse連携を発見事例として保存）

## 0. この記録の目的・決定権
**主題はTailscaleであり、Museの採用検討が主目的ではない。** AI-Harnessのスマホ／ローカルPC／クラウドAI／エージェント間接続に共通利用できるプライベートネットワーク技術として、機能全体、原典、実装の可能性、限界、危険性、Museで発見した事例をまとめて保持する。「使える部分を抜き出す」のは**将来の利用判断**であり、研究記録の保存対象を最初から削ることではない。

Humanは2026-10-24に本研究の保存を明示承認。「MuseよりもTailscale中心」と範囲を指示した。これは調査Proposalの新規ファイル作成のみの承認。Tailscale/Museのアカウント連携、PC接続、SSH/API公開、エージェント実行、BBBへの導入、GitHubの他の変更、Core/Trinityの変更は承認されていない。

## 1. 発見の経緯：X投稿の全体像
- 2026-10-23の投稿（@studio_yebisu）: https://x.com/studio_yebisu/status/2113660702439391318
- 投稿内容: **「MuseがTailscaleと連携できる」**との発見。Tailscaleを、離れた端末を同じLANのように結ぶものと説明し、PC上のAI Agent（投稿例: DSH、Codex等）をMuseから遠隔操作できる可能性を提起。
- これは投稿者の**発見・推論**を含む。Muse連携の存在は公式情報で裏付けられるが、任意のDSH/Codexに接続して実行できることまで証明した投稿ではない。
- 投稿の引用元はMuseを「基本無料」「汎用AI秘書」と紹介。機能範囲・無料枠は公式情報や現行アプリで個別に確認する。
- Humanの直接の使用感: **スマホにMuse導入済み、性能は「まあまあ」、汎用性にポテンシャルを感じる**。これは主観的な現場観察であり、製品の客観性能評価ではない。
- 時系列に注意: 2026-09-30のTailscale公式ブログはすでにMuseとの連携を説明している。10-23のX投稿を**Tailscaleによる連携の初公開**と見なさない。

## 2. 一次資料（2026-10-24に確認）
1. Tailscale公式ブログ「Your agent, your network: How Meta’s Muse agent works with Tailscale」（2026-09-30）
   https://tailscale.com/blog/meta-muse-ai-agent-tailscale
2. Tailscaleの基本構造
   https://tailscale.com/docs/concepts/what-is-tailscale
3. ネットワーク接続種別（Direct / DERP / Peer Relay）
   https://tailscale.com/docs/reference/connection-types
4. アクセス制御（Grants / ACLs）
   https://tailscale.com/docs/features/access-control
   https://tailscale.com/docs/features/access-control/acls
   https://tailscale.com/docs/reference/syntax/grants
5. Tailscale SSHとその対応OS
   https://tailscale.com/docs/features/tailscale-ssh
6. Tailscale Serve（tailnet内）／Funnel（公開インターネット）
   https://tailscale.com/docs/features/tailscale-serve
   https://tailscale.com/docs/features/tailscale-funnel
7. 料金（Personal無料プランと有料機能）
   https://tailscale.com/pricing
8. Meta Muse日本提供開始（2026-10-23）
   https://about.fb.com/ja/news/2026/10/muse-personal-ai-agent-launches-in-japan/

公式記事に記載された仕様の確認と、対象環境における動作の実証は区別する。この調査で接続実験・設定変更・料金契約・負荷検証・セキュリティ監査は行っていない。

## 3. Tailscaleとは何か — Museと独立した技術
TailscaleはWireGuardを使って、別のネットワーク上の端末・サービスを**認証したプライベートネットワーク（tailnet）**で結ぶための接続基盤。NAT越え、端末識別、接続経路、アクセス規則を扱い、一般的に家庭ルーターでポート開放をするより導入・保守を単純化できる。可能であれば端末同士が直接接続し、できない場合は暗号化を維持したリレー接続を使用する。

**Tailscaleが提供するもの**
- 端末・サービス間の暗号化された通信経路
- 参加端末の認証・一覧・管理、MagicDNS等
- Grants/ACLによる送信元・接続先・ポート等のアクセス制御
- 特定条件でTailscale SSH、内部サービス公開のServe、別用途のFunnel
- モバイル・PC・ローカルサーバー・外部AIエージェントなどの間で再利用可能なネットワーク接続方法

**Tailscaleだけでは提供しないもの**
- AIモデルの推論、エージェント実行、Codex/Hermesへの指示API
- チャット、ダッシュボード、ファイル・コード操作UI
- アプリケーション独自の認証・権限管理、Human最終承認
- 保存済みタスク・チェックポイント・障害復旧・永続Memory
- オフラインPCを自動起動して働かせる保証
- 追加接続したクラウドエージェントを「安全・信頼できる存在」にする保証

Tailscaleは**Connectivity（到達性）**。Agent Runtime、Tool/API、Authority、Durabilityとは別のレイヤー。無暗な一体化を避ける。

## 4. Muse連携は何を確認できたか
Tailscale公式ブログによると:
- Meta MuseにはTailscaleコネクターがあり、連携するとMuseが自身の**独立したtailnetノード**として参加する。
- 携帯端末側ですでにTailscaleログイン済みでも**Muse用に別途認証**する。Museアプリ・デスクトップ・Webクライアントで同様の方式。
- 権限がある範囲のノード状態確認、セルフホストサービスとの連携、Tailscale SSHセッション補助などが説明されている。
- 同記事はLM StudioのLM Linkや、OpenClaw、Hermes WebUI、Pi系ツールなど、**Muse以外のエージェント連携例**も紹介している（各組み合わせの動作を本調査で確認したわけではない）。
- Meta公式発表によるとMuseは2026-10-23に日本提供開始、iOS/Android/Web対応、基本機能は多くが無料で一部有料機能あり。Metaは重要な操作の確認やセキュリティ対策を説明しているが、第三者がHuman承認を独立強制できる証拠ではない。

**注意：スマホのMuseアプリ経由でも、クラウド側のMuseが別ノードとして家庭内ネットワークにアクセスする構造。これは単なる「スマホ自体のVPN接続」とは異なる信頼・データ境界である。** 提供会社のクラウド側から何に到達できるか、どの情報を取得できるか、操作の承認がどこで強制されるかを個別に考える必要がある。

## 5. AI-Harnessの候補構成（実装設計ではない）
A. Museなしの最小構成:
iPhone Tailscale client → tailnetの限定アクセス → 自宅PC上の**認証付き・読み取り専用**状態表示/API（将来候補） → AI-Harness

B. Museを入口にする拡張構成:
Human → Muse（独立したtailnetノード、第三者サービスの権限） → tailnetの**限定サービス／限定ポート** → Human承認を強制するHarness側の操作受付 → ローカルAgent/Tools

C. 別のエージェント／実行環境:
許可されたエージェント端末 → tailnet → ローカルPCの必要なAPIまたは明示的に制約したSSH → Hermes候補／その他Agent
※Codex/Hermesが接続先APIや受信リスナーを持つことはTailscaleによって自動的には実現しない。

D. 非常時／停止時:
PCが休止・電源OFF → PC上サービスには到達できない。タスクの継続・待機・Humanへの通知を行うなら、PiDurableKitやDurable Runtime等**別機構**が必要。

以上はいずれも**仮説図**。現行AI-Harnessにネットワークエージェント基盤が実装済みであると推定しない。

## 6. 既存Proposalとの比較（developmentの本文を照合）
- **近い構想**: incubator/proposals/2026-09-20-harness-server-mobile-control.md
  - スマホを軽い制御端末、PCをHarness Serverとするアイデア。遠隔接続の認証とポート非公開が未解決。今回のTailscaleは**接続経路候補の具体化**。上記を否定／自動更新しない。
- **別のruntime選択**: incubator/proposals/2026-10-09-pidurablekit-iphone-durable-runtime.md
  - iPhoneをDurable Runtime、PCを必要時のワーカーとする構想。PC常時起動を前提にしない点で重要。Tailscaleはその場合も通信経路であり、永続Task Stateにはならない。
- **タスク受渡し**: incubator/proposals/2026-10-18-grokbot-local-agent-task-webhook.md
  - Task ID、Owner、pending/ack、Webhook等。接続経路とタスクライフサイクルは別。
- **ツール実行面**: incubator/proposals/2026-10-20-cloud-harness-mcp.md
  - 認証付きcoding-agentのMCP tool surface。Tailscale単体はファイル/シェル実行APIを提供しない。
- **デスクトップ操作**: incubator/proposals/2026-10-16-lcu-hermes-desktop-control.md
  - GUI操作を提供する仮説候補。Tailscaleで接続可能にしても操作制限が自動成立するわけではない。
- **権限保護**: incubator/proposals/2026-10-16-grok-agent-permission-approval-hold.md、core/ACCESS.md
  - 外部AIの接続権限と、Humanによる書き込み・実行承認は独立して制御する。
- **Hermes Local Agent**: 現状は研究段階／実装は未承認。TailscaleはHermes導入を前提にしない。
- **BBB**: 取引APIキー、発注、ローカルログや制御面は一般家庭AIの検証環境から厳格に分離すべき。Museの接続先・汎用agentのコマンド実行権限に含めない。

**重複判定**: モバイルHarnessアクセスという目的は既存、しかしTailscale固有の機能・権限モデル・Muse連携事例のまとまった研究記録は今回のIncubatorに独立保存する意味がある。接続・実行・Human Gate・Durabilityを混同しないことが新規価値。

## 7. 安全性：導入前に必ず確認すべき事項
1. **最も重要: 新規tailnetの初期ポリシーはallow-allの場合がある。** Tailscale公式ACL文書によれば、tailnetを最初に作成した時の標準設定は端末間の通信を広く許可する。Grantsや個別ACLがdeny-by-defaultで評価されることと、初期設定で既にallow-all規則が存在することを混同しない。Muse等の外部agentノードを参加させる前に、実効ポリシーを確認し、**最小権限で明示許可したサービスだけ**に到達できるよう制御・テストする。
2. ネットワーク許可はHuman承認を代替しない。書き込み・Shell・Git push・取引・課金・設定変更はアプリケーションレイヤーの認証・操作ごとの承認・Auditが別途必要。
3. 外部エージェントをtailnetに入れることは、外部サービスに家庭内資源への通路を与える行為。プロンプトインジェクション、機密データ持ち出し、過剰権限、権限失効、操作ログを別途検証。
4. Tailscale SSHの**サーバー側**サポートは公式資料ではLinuxと所定のmacOS構成。WindowsのTailscaleクライアントから送信できることと、Windows PCがTailscale SSHサーバーになることは別。OS未確定の家庭用PCへのSSH制御を当然視しない。
5. 接続先はまず使い捨ての読み取り専用テスト用サービスに限定。私的ファイル・GitHub credentials・SSH keys・MCP secrets・家族データ、BBB取引系と分離する。
6. Tailscale Serveはtailnet内の共有、Funnelは**一般インターネット向け公開**。Funnelを初期実験で使用しない。アクセス規則とOSファイアウォール等も確認する。
7. 認証解除・端末撤去・アカウント乗っ取り時の隔離・復旧、別端末からの不正な横移動、全員のtailnet共有問題を検討する。
8. 速度は端末間の経路（直接/リレー）や端末のオンライン状態に依存。ネットワークの暗号化自体はZero Riskを意味しない。

## 8. コストと実用条件
Tailscale公式料金ページ（2026-10-24参照）ではPersonalは非商用の自宅用途で**無料、最大6人のユーザー、ユーザーデバイス無制限**。タグ付きリソースやephemeral resources、ACLグループ等にはプラン依存の上限があり、高度な機能は有料の場合がある。Muse側にも無料機能と有料機能がある。**Tailscaleが無料でも、Museの利用条件・PCの稼働費用・外部モデル/Agentの課金は別。** 実装検討時にその日の料金・日本での機能提供範囲を再確認する。

無課金・既存資産活用優先の場合、まず**Museを使わないTailscaleの基本接続**と既存ブラウザUIで要求を満たすか比べる。Museは任意の追加UX/Agent層であり必須ではない。

## 9. 将来の最小・可逆な検証ガイド（まだ実行しない）
**Stage 0（読取のみ）**: 対象OS、端末、必要な到達先、接続主体、データ分類、リスク、無料枠の確認。既存機能で実現できるか判断。

**Stage 1（別途Human承認が必要）**: 本番PCや私的アカウントを使わず、無害なダミーのWebページ等をtailnet内で公開するテストを計画。ネットワークポリシーが必要な宛先ポート以外を拒否することを先に確認。

**Stage 2（別途Human承認が必要）**: iPhoneのTailscale接続のみで閲覧・切断・ネットワーク遮断をテスト。家庭の非公開ネットワークへ広範囲のアクセスを与えない。

**Stage 3（別途Human承認が必要）**: 必要性がある場合のみMuseの独立ノード参加を検討し、前後で到達可能ホスト・ポートを比較。Muse側で見られるデータ、拒否・Human承認・接続解除を検証。Codex/Hermesのコマンド権限は与えない。

**判定軸**:
- 接続できるか／アクセス禁止先に実際アクセスできないか
- PC停止や回線切断時の挙動
- 本人認証、端末紛失・アクセス撤回、操作監査
- iPhone単独接続に対するMuse追加価値
- コスト、管理負担、速度、家庭運用の簡単さ
- GitHub書込・Family Private・BBBを独立ガードできるか

通った場合のみ、採用形態を「無採用 / Museなし部分採用 / Muse連携の追加 / HOLD」から別途Humanが判断する。今回の保存から自動実装しない。

## 10. 二段階評価と保存判断
- Stage 1: **A++**。スマホ・ローカルPC・将来エージェントの通信レイヤーとして広い波及可能性。
- Stage 2: **A+**。公式Tailscale記事でMuse連携が裏付けられ、基本のネットワーク機能とアクセス制御、無料プランが明文化。価値は高いがHarness環境で接続・権限を実証していない。
- Evidence: 公式文書で仕様説明**CONFIRMED**／Human利用体感**ANECDOTAL**／実環境の動作・安全性・費用対効果**UNVERIFIED**。
- Decision: **CANDIDATE（全体研究記録として保存）/ IMPLEMENTATION HOLD**。
- 独自性: 目的は既存モバイル制御Proposalと重複するが、**Tailscaleという可逆的な接続層を選択可能にする具体的根拠**が追加された。Museは主題ではなく使用例。
- Revision trigger: Tailscale/Museの料金、個人向け権限、初期アクセス規則の変更、明確なスマホ→Harness要求、HermesがPhase 0から進む時、代替接続方式の比較時。

## 11. Source-of-Truth境界
本ファイルはGitHub Incubatorに置く**研究・比較用の記録**。仕様の採用、インストール、ネットワークへの追加、SSH有効化、端末公開、外部クラウドの権限付与は別案件。使用時には公式一次資料と実環境を再検証し、必要に応じて新たな承認を得る。既存Proposalを勝手に編集・削除・統合しない。
