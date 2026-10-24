---
document_type: ecosystem_research_evaluation
date: 2026-10-24
timezone: Asia/Tokyo
title: "Hermes Agent community extensions — five-project landscape and AI-Harness assessment"
source_post: "https://x.com/haoge6699/status/2113546970606289064"
project_context: "Hermes Local Agent / AI-Harness"
stage_1_rank: A+
stage_2_rank: A+
decision: CANDIDATE
implementation: HOLD / NOT IMPLEMENTED
relationship: "REINFORCE + COMPLEMENT + COMPARE; not five approvals"
evidence_status: "X POST READ; ALL FIVE GITHUB REPOSITORIES AND READMEs EXAMINED; REAL-WORLD BENEFITS AND INTEGRATION UNTESTED"
human_approval: "2026-10-24: preserve a cohesive full-landscape research record, readable standalone"
tags: [hermes, hermes-agent, ecosystem, community-oss, agents, skills, self-improvement, evaluation, workspace, memory, privacy, security, distilly, tailscale, local-first]
---

# Hermes Agent 周辺エコシステム調査 — 5つのOSSを一つの全体像として読む

> **要点（初読の方向け）**
>
> X投稿は「Hermesが自己進化する5つの拡張」として5つのGitHubプロジェクトを紹介している。しかし実態は、**分析方法、失敗からの改善、操作画面、運用プラグイン、人物知識のSkill化**という、役割の異なる独立したコミュニティOSS群である。
>
> AI-Harnessとの関連は強い。特に**Hermes Workspace**はUIとTailscale経由の遠隔操作構想、**Hermes Dojo**は検証と改善の記録に価値がある。一方で「自動改善」の宣伝と実効的な改善は別物であり、権限・プライバシー・複雑性・費用が採用判断の中心になる。
>
> **全件を研究記録として保持する。ただし5件を一括導入しない。Hermes Local Agentは引き続きPhase 0 / NOT IMPLEMENTED。**

## 1. 研究の出発点・承認範囲

### 提供情報
- Humanが共有したX投稿：2026-10-23、@haoge6699
- 投稿本文：https://x.com/haoge6699/status/2113546970606289064
- 投稿のフレーミング：「ただ使うAI」から「自分で学ぶ・改善するHermesへ」。5方向（Super Hermes、Hermes Dojo、Hermes Workspace、Hermes Plugins、Colleague Skill）を紹介。
- 投稿本文とリンク5件は実際に取得・確認。**有料記事ではなく公開のX投稿とGitHubへのリンク集**である。

### Humanの保存意図（2026-10-24）
単なる5件の抜粋や紹介ではなく、**一つのファイルを最初から読めば、話題の全体像と5件の関係・メリット・限界・AI-Harnessとの関係を理解できる文章**として保存する。

「全部を記録」することと「全部を採用する」ことは異なる。各OSSの役割・機能・原典・制約を保持し、実際の利用は後から用途・実証・安全性で決める。実装は今回未承認。外部リポジトリのソースコード全体をGitHubへ複製・ミラーリングする趣旨ではなく、**読解に必要な調査情報を一体化して、原典リンクで全体を追跡可能にする**。

## 2. 先に全体像：5件は何を分担するのか

| No. | 主な対象 | 何を加えるか | 導入後に期待される役割（仮説） | 現在の判断 |
|---|---|---|---|---|
| 1 | [Cranot/super-hermes](https://github.com/Cranot/super-hermes) | 問題ごとの分析レンズ、見落とし・制約の報告 | 分析の**方法**を変える | A / REFERENCE |
| 2 | [Yonkoo11/hermes-dojo](https://github.com/Yonkoo11/hermes-dojo) | ログで弱点測定、Skill改善、改善前後の報告 | **失敗→改善→再測定**の循環 | A+ / CANDIDATE |
| 3 | [outsourc-e/hermes-workspace](https://github.com/outsourc-e/hermes-workspace) | Chat・Files・Memory・Skills・Terminal・Jobsの統合Web UI | エージェント操作・可観測性の**画面** | A++ / CANDIDATE |
| 4 | [42-evey/hermes-plugins](https://github.com/42-evey/hermes-plugins) | 複数モデルの選択、予算、記録、メッセージ連携、自治的判断 | 運用を支える**拡張機能群** | A / REFERENCE |
| 5 | [Distilly（旧 titanwings/colleague-skill）](https://github.com/titanwings/distilly) | 文書・会話等から人の知識・判断・語り口をPerson Profile/Skill化 | 人に由来する**専門性の再利用** | A / PRIVACY HOLD |

この5件は同じ技術の競争製品ではなく、レイヤーが違う。ただし一緒に使えば相乗効果があると確かめたわけではない。

**概念上の関係（実装図ではない）:**

\`\`\`text
Human（最終判断、権限付与）
       │
       ▼
Hermes Workspace ── UI / 表示 / 操作受付
       │
       ▼
Nous Research Hermes Agent ── 基本ランタイム / Model / Tools / Memory / Skills
       │
       ├─ Super Hermes ────── 分析フレーム・見落とし報告
       ├─ Hermes Dojo ─────── 失敗観測 → 改善案 / Skill変更 → 再評価
       ├─ Evey's Plugins ──── Cost / Telemetry / Routing / Bridgeなど
       └─ Distilly ───────── 人物資料に由来するProfile Skill（独立して利用可能）
       
Tailscale（オプション）= モバイルや遠隔端末との通信経路のみ
AI-Harness = ルール・Access・Human承認・Source of Truth
\`\`\`

Hermes本体にもMemory、Skillsの生成・改善、Cron、モデル切替、Gateway、Subagents等があるため、**周辺OSSは標準機能との差分があって初めて採用意義がある**。製品群の同時導入を前提にしない。

## 3. No.1 Super Hermes — 「考える手順」を生成するSkill群

**一次資料:** https://github.com/Cranot/super-hermes （公式README、公開事例と研究へのリンク）。MIT。HermesのSkillとして動く想定だが、分析用「prism」自体は他のLLMのsystem promptにも利用できる設計。

**READMEで確認できた機能・主張**
- 目の前の問題に合う「cognitive prism（分析レンズ）」を生成する \`/prism-scan\`。
- \`/prism-full\`（複数の分析観点で自己批判）、\`/prism-3way\`（WHERE/WHEN/WHY）、\`/prism-discover\`（分析範囲発見）、\`/prism-reflect\`（見落とした領域やトレードオフを出力）。
- 7つの事前作成した分析用Prism、事例の分析結果と制約レポート。
- \`.prism-history.md\` に過去の見落としを残し、後続の分析に参照する軽量フィードバック。**学習するのはモデルの重みではなく、プロンプトとプロジェクト内の分析履歴**。

**限界と検証上の注意**
- README自ら「単一ファイル中心」「モデル依存」「学習ループはappend-onlyで枝刈り・意味検索・改善確認なし」「外部標準ベンチマークなし」と記す。
- README中のバグ件数・深さスコア・安価なモデルでの勝利などは**作者側の事例・採点基準**。AIによる独自評価を、そのまま再現性のある性能証拠と扱わない。
- 長い出力や派手な「不可能性・保存則」の表現は、正確な証明や修正提案の正しさを保証しない。
- ファイルに自動記録するSkillは、記録場所や権限、誤認の蓄積を管理しなければならない。

**AI-Harnessとの関係:** \`core/WORKFLOW\` の証拠と不確実性の区別、Trinityの複数観点、反証検討、Lessonsと機能思想が重複。最小の分析レンズが今の作業に上乗せで有益かを将来比較できる。**A / REFERENCE / 実装HOLD**。

## 4. No.2 Hermes Dojo — 実行ログから弱点を探し、改善を試みる

**一次資料:** https://github.com/Yonkoo11/hermes-dojo （README）、MIT、Python、Hermes Agentに依存。Self-evolution（GEPA）を含む一部処理では \`hermes-agent-self-evolution\` も必要。

**READMEで確認できた流れ**
1. Performance Monitor: \`state.db\` のセッション履歴を読み、ツールエラー、リトライ反復、ユーザー修正・不満、Skill別成績を集計。
2. Weakness Analyzer: 再発原因、足りないSkill、改善の優先度を候補化。
3. Auto-Fixer: Skillの修正・新規生成やGEPA最適化を実行する設計。
4. Reporter / Learning Curve: CLI、Telegram、JSON履歴で変化を示す。
5. \`/dojo auto\`: Cronを使う夜間実行が案内されている。

**「自己進化」の意味:** 失敗を測ってSkillのコード・指示・構成を変更する**ソフトウェアのフィードバックループ**であり、モデル重みの自動再学習を実証するものではない。

**重要リスク**
- 失敗と正解の自動分類が誤ると、誤った改善で成績が下がる。
- 同じ自己採点器で改善案を採点するだけでは、指標への過適合を防げない。
- \`state.db\` を解析すると個人的な会話・ツールログ・秘密情報へのアクセス可能性が増す。
- Auto-Fixer、Cron、Telegram通知は外部送信や変更を伴い得る。**無人実行・自動Skill上書きは現段階で不適合**。
- 公開READMEに流れの説明はあるが、実環境の統計的な継続改善、ロールバック耐性、権限強制の独立監査は未確認。

**AI-Harnessとの関係:** 過去のLesson/評価、Trinity、失敗検出、Skillsの改善という問題意識が非常に近い。**最も価値があるのは「検出→原因候補→提案→独立再評価→Human承認」のプロセス**。自動修復を前提にしない。**A+ / CANDIDATE / 実装HOLD**。

## 5. No.3 Hermes Workspace — Hermesを扱う統合Web作業台

**一次資料:** https://github.com/outsourc-e/hermes-workspace （公式README、バージョン表示 v2.3.0）、MIT、TypeScript/React系、Node 22+等。公式Hermes本体とは別のコミュニティ実装。

**確認したREADME機能の範囲**
- Chat、セッション、Memory閲覧・編集、Skills、MCP、Files、Terminal。
- Jobs、Dashboard、Token・Costの表示、Agent View、複数AgentのSwarm Mode、Kanban Task Board、Reports、Conductor。
- PWA対応、Webブラウザからの操作、Tailscale/VPN/LAN上の離れた端末からのアクセス方法。
- Hermes GatewayとDashboard APIがある場合に拡張機能が動き、通常のOpenAI互換モデルAPIのみでは「Portable Mode」となり、MemoryやJobs等の一部が利用できない構成。
- 外部のOllama/LM StudioなどOpenAI互換エンドポイントを扱う説明あり。**Hermes本体の全機能を使えるかはGateway要件に依存**。
- バージョン・機能はREADMEに説明された範囲であり、AI-Harnessの実環境での可用性・品質は未検証。

**先ほどのTailscale調査との接点**
- WorkspaceのREADMEには **Remote host (Tailscale / VPN / LAN)** と **PWA + Tailscale** の項があり、ローカルPCのWeb作業台をスマホから操作する設計例がある。
- これは既存 \`harness-server-mobile-control.md\` と今回の \`tailscale-private-network-agent-access-muse-case.md\` にある**目的を具体化する証拠**。
- Museを必須としない。**スマホブラウザ + Tailscale + 認証済みWorkspace**という構成を比較対象にできる。
- ただしWorkspace READMEが挙げる \`API_SERVER_HOST=0.0.0.0\` やDockerのポート公開設定を**安全であると推奨しているわけではない**。bind全開、未設定のAPI鍵、 \`GATEWAY_ALLOW_ALL_USERS\` や広いtailnet許可は個人・家族PCへの不適切な到達を生む恐れがある。

**重要リスク・採用判断**
- File / Terminal / MCP / Skills編集は高権限。画面表示の認証とAI-HarnessのHuman操作承認は独立して強制が必要。
- リモート接続・Cloudブラウザ・Tailscaleを加えると横移動や認証情報露出の経路が増える。
- DashboardやGatewayが複数プロセスとなるなど、CPU/RAM・運用保守の負担がある。
- READMEの「zero-fork」「無制限swarm」「全面対応」は上流実装の主張。安定性・モデル料金・各モードの対応を独立検証する。
- **A++ / CANDIDATE / 実装HOLD**。今回は5件中、現行Harnessのモバイル制御とHermes研究に最も具体的な接点を持つ。

## 6. No.4 Evey's Hermes Plugins — 運用・安全・コスト等の拡張セット

**一次資料:** https://github.com/42-evey/hermes-plugins （公式README）、MIT、Python等。READMEは23プラグインと共有ユーティリティを列挙。

**公式READMEに記載されたカテゴリ・具体的なもの**
- 自律判断・複数AI: \`evey-autonomy\`、\`evey-council\`、\`evey-delegate-model\`。
- 観測・コスト: \`evey-telemetry\`（ツールのJSONログ）、\`evey-status\`、\`evey-mqtt\`、\`evey-cost-guard\`（Langfuse連携）。
- 品質・安全: \`evey-reflect\`、\`evey-validate\`、\`evey-email-guard\`、\`evey-sandbox\`、\`evey-session-guard\`。
- Memory/学習: \`evey-learner\`、\`evey-memory-adaptive\`、\`evey-memory-consolidate\`、\`evey-cache\`、\`evey-identity\`。
- 連携・タスク: \`evey-bridge\`（Claude Code連携）、\`evey-goals\`、\`evey-telegram-ux\`、\`evey-research\`、\`evey-digest\`、\`evey-delegation-score\`。

**コスト上の留意点:** READMEには「無料モデルを利用」「$0/day operating cost」といった説明と、同じREADME中のハードウェア約$69/月への支援記述がある。**推論API費用がゼロになる場合でも、ホスティング・HW・通信・保守まで無料と同一視しない**。具体的な費用と上限はサービス・運用形態で変わる。

**安全と重複**
- \`evey-autonomy\`、Memoryの自動書き換え、外部モデル委譲、MQTT、MCP、Cron等は既存Access/Human承認・Private情報分離と衝突し得る。
- Regex + LLMによる安全判定や“sandbox”という名前だけでは、OS分離・機密保護・プロンプトインジェクションへの完全耐性を示せない。
- 依存サービス（Langfuse/Qdrant等）の運用コスト、ログ中の個人情報、APIキー、ネットワーク経路は要確認。
- 単機能を今後比較する価値はあるが、セット全体を導入すると既存Harnessと機能重複が大きい。
- **A / REFERENCE / 実装HOLD**。

## 7. No.5 Distilly（旧 Colleague Skill） — 人に由来する知識をSkill化する

**名称・所在に重要な訂正**
- X投稿の旧リンク：https://github.com/titanwings/colleague-skill
- 2026-10-24にGitHub APIで旧repoの移動（redirect）を確認。**現在の実体**：https://github.com/titanwings/distilly
- 旧READMEは「colleague.skill」。現行repoの \`dot-skill\` ブランチREADMEでは **Distilly** と説明。MIT。
- したがって「Hermes専用の自己進化Plugin」ではなく、**複数エージェント環境で人の経験・判断傾向等を再利用するPerson Profile生成ツール**。

**公式READMEで確認できたこと**
- 会話・ドキュメント・メール・PDF・公開情報・ユーザーの記述等を入力し、人のWork Skill・Personaのような形のProfileを生成する。
- 当初は「退職・異動した同僚の引き継ぎ」を扱ったが、現在は職場・親しい人・有名人等、複数の対象に拡張。
- ソースとしてSlack、Feishu、DingTalk、メール、Markdown、画像、PDF等の対応を説明。各取得方式・API費用・権限は異なる。
- READMEはClaude Code、Hermes、Codex、OpenClaw等のAgent Skills形式を説明。Muse/DotsへのProfile handoffは将来計画の項として区別されている。
- **本人そのものを再現・複製できるという科学的・倫理的証明ではなく、資料由来の振る舞いを整理した近似Profile**。事実と推測・演出を分ける。

**AI-Harnessに特に重要な安全上の境界**
- 家族・同僚・第三者の私的発言やメール、画像の収集は、**本人同意、利用目的、再配布、アクセス権、保存期限、削除方法**の事前確認を要する。
- ソースに含まれる秘密・業務情報・Private層を、そのままShared Skillや外部モデルへ渡さない。
- 個人の判断や声を模した応答は誤帰属や心理的混同を生み得る。Skillは本人の意思、専門資格、権限の代替ではない。
- 将来の家族AI構想との概念的接点はあるが、**収集や人格化を今すぐ進める根拠はない**。
- **A / PRIVACY HOLD / 実装未承認**。

## 8. 既存AI-Harness／Hermes研究との重複・補完

現行リポジトリ（\`development\`）で確認した関係資料：
- \`projects/Hermes_Local_Agent/research/2026-10-23-hermes-agent-current-reassessment.md\`
  - Hermes本体のMemory/Skills自動生成・自己改善・Gateway等をすでに公式確認。**本体の能力を知らずに周辺拡張を積まない**。
- \`projects/Hermes_Local_Agent/research/2026-10-15-hermes-agent-reinforcement.md\`
  - Phase 0、GPUなしから段階評価、ChatGPT Work/Codexとの二重投資回避。
- \`incubator/proposals/2026-09-20-harness-server-mobile-control.md\`
  - スマホUI→PCのHarness Serverという目標。Workspaceが一案。
- \`incubator/proposals/2026-10-24-tailscale-private-network-agent-access-muse-case.md\`
  - Tailscaleはプライベート通信経路。WorkspaceはUI、HermesはRuntime。**レイヤーの区別**が重要。
- \`incubator/proposals/2026-10-09-pidurablekit-iphone-durable-runtime.md\`
  - iPhone側を継続性の支点とする**別構成**。常時稼働PCを前提としないのでWorkspace構想と競合する可能性もある。
- \`incubator/proposals/2026-10-16-grok-agent-permission-approval-hold.md\`
  - 自動変更・命令実行・外部通信を権限レイヤーとHumanで守る。
- \`incubator/proposals/2026-10-16-harness-minimalism-counterhypothesis.md\`
  - 重厚な拡張が常に性能向上を生むとは限らない。
- \`incubator/proposals/2026-10-23-ecc-agent-harness-reference.md\`
  - 他Harnessから大量のRules/Skillsを取り込む際の衝突・冗長化リスク。
- \`incubator/proposals/2026-10-02-trinity-persistence-enforcement-completion-evaluation.md\`
  - 何を実行・承認・評価するかの境界が中心。
- \`core/ACCESS.md\`、\`core/RULES.md\`、\`core/WORKFLOW.md\`、\`HARNESS.md\`
  - Coreが定める最終的なアクセス・Human承認・検証ルール。

**総合重複判定**
- Hermes本体や既存Harness構想との**大きな機能重複あり**。
- 5件すべてが新機能を意味するわけではないが、**5つの別レイヤーを横断して比較できるエコシステムの記録**は既存Proposal単体にない。
- 既存文書は上書き・統合せず、新規横断レファレンスとして残す。採用時は個々の現行機能を再照合する。

## 9. 組み合わせで分かる可能性と衝突

### 組み合わせ候補（参考であって設計承認ではない）
- **Hermes + Workspace**: UIだけを外付けして、チャット・ログ・状態が見やすくなる可能性。既存Dashboardで十分かを先に比べる。
- **Hermes + Workspace + Tailscale**: スマホからローカル環境を閲覧する候補。GUIの認証と権限、tailnetのアクセス制御を別に強制する。
- **Hermes + Dojo**: 失敗検出・改善サイクルを増強する可能性。変更の自動実行を止めた**提案・比較モード**から設計上検討する（存在する機能として断定しない）。
- **Super Hermes + 評価系**: 見落としを明示する文章品質への寄与を、小さなベースラインで比較する。
- **Plugins + Harness**: Cost/Telemetry等は既存機構を置き換える可能性もあるが、コンテキスト・依存・保守負担に見合う証拠が必要。
- **Distilly + Family/Skills**: Person Profileによる専門知識の再利用という長期的な方向。ただし実データは同意とPrivate管理が最優先。

### ありがちな誤認
1. 「GitHubで公開」≠「安全／保証済み／公式Nous製」
2. 「自己進化」≠「モデル重みの更新／精度改善が立証済み」
3. 「自己評価で高得点」≠「外部条件への汎化・安全性」
4. 「Tailscaleで到達できる」≠「SSH/API操作の認可とHuman承認が成立」
5. 「OpenAI互換APIでチャットできる」≠「Hermes Gatewayが提供するMemory/Jobsを利用できる」
6. 「無料OSS」≠「GPU・API・クラウド・保守が無料」
7. 「人物からSkill生成」≠「本人の同意／正確な人格の再現」

## 10. 二段階評価・根拠の確実性

| 対象 | Stage 1 | Stage 2 | 記録上の結論 | 確認と未確認 |
|---|---|---|---|---|
| Super Hermes | A+ | A | REFERENCE / HOLD | 公式READMEでPrism方式確認、独立した性能優位は未検証 |
| Hermes Dojo | A+ | A+ | CANDIDATE / HOLD | 公式READMEで失敗観測・Auto-fix構成確認、改善効果は未検証 |
| Hermes Workspace | A++ | A++ | CANDIDATE / HOLD | READMEで統合UI・PWA/Tailscale説明確認、実装・安全性は未検証 |
| Evey Plugins | A+ | A | REFERENCE / HOLD | 23プラグインの説明を確認、費用・権限・個別品質は未検証 |
| Distilly | A | A | PRIVACY HOLD | 改名先・人物Profile機能を確認、実用価値・本人同意設計は未検証 |
| **横断ランドスケープ** | **A+** | **A+** | **CANDIDATE / 全件を研究保存・実装HOLD** | 5件を個別に実証するものではない |

**証拠レベル**
- **CONFIRMED**：X投稿本文とリンク5件の内容、GitHub上のプロジェクト存在、READMEに記載された機能の説明、旧Colleague Skill→Distilly移転、READMEにあるTailscale接続方法。
- **CLAIM / AUTHOR REPORT**：各作者の性能・「進化」・費用・安定性の主張、自己評価スコア、README内の機能数・サポート範囲の実動作。
- **INFERENCE**：AI-Harnessにとっての適合性、5件の連携可能性、最終的な導入優先度。
- **UNVERIFIED**：この家庭PC／既存Codex／Hermes構成でのインストール、負荷、GPU不要の実用速度、独立安全監査、継続的性能向上、複数OSSの実接続、最終費用。

## 11. 将来の検証手順（今回は実行しない）

**Phase A：研究**
- Hermes本体が持つ標準のMemory/Skills/Jobs/UI/APIを最新版で再点検し、各OSSとのAlready present / Partial / Missing / Contradictoryを分類。
- README／設計資料／依存関係／LICENSE／ログ・Secretの扱いを検査。
- 既存ChatGPT Work/Codexと比較し、追加機能の必要性が明確かを判断。

**Phase B：隔離された比較実験（別途Human承認）**
1. 一つのOSSだけを使い捨て環境でテスト（全件一括導入はしない）。
2. 同一課題をBaselineとCandidateで実行し、正確性、失敗、再実行、消費Token/時間/金額、監査性、権限逸脱を比較する。
3. 自己改善系はまず**変更を適用しない評価のみ**の構成を設計する。適用前後の独立テスト・ロールバック・Human承認を別レイヤーで強制する。
4. Workspace系は読み取り専用UIから検討。個人・家族情報、取引APIキー、GitHub write、Shell操作を隔離。
5. 第三者データ・家族会話は同意取得と利用範囲の合意なしにProfile化しない。

**Phase C：採否（Human）**
- 部分採用、全体採用、別実装、HOLD、REJECTを対象ごとに判断。
- 意思決定時点のコード・料金・規約・最新リリースを必ず再取得。
- 成果・失敗を元の全体研究と結びつけて保持する。

## 12. 最終判断と記録の扱い

- **記録:** 一つの文書に、5件と相互関係を全文脈で保存。
- **横断評価:** **A+ / CANDIDATE（研究レファレンス）**。
- **突出する検証対象:** Hermes Workspace（実際の操作UI・Tailscale）、Hermes Dojo（測定と改善提案）。ただし初期優先順位は暫定。
- **Hermes Local Agent:** **Phase 0 / NOT IMPLEMENTEDを維持**。この記録を自動実装の根拠にしない。
- **権限:** GitHub Incubatorへの研究ファイル1件保存のみ。Core、RULES、WORKFLOW、ACCESS、Trinity、本体コード、他Proposalの無断修正を行わない。
- **呼び出しキーワード:** Hermes extensions, super-hermes, prism, hermes-dojo, hermes-workspace, Evey plugins, colleague-skill, Distilly, self-evolution, Tailscale, Muse, agent memory, skill governance.
- **再評価条件:** Hermes Phase 0の進展、Tailscale接続の実験判断、Workspaceの新機能、Dojoの独立評価、Distillyのプライバシー要件の確認、既存Skillsとの具体的な機能差。

## 13. 原典と関連するAI-Harness記録

### 原典（個別読解の起点）
- 発見元 X: https://x.com/haoge6699/status/2113546970606289064
- Super Hermes: https://github.com/Cranot/super-hermes
- Hermes Dojo: https://github.com/Yonkoo11/hermes-dojo
- Hermes Workspace: https://github.com/outsourc-e/hermes-workspace
- Evey's Hermes Plugins: https://github.com/42-evey/hermes-plugins
- Distilly（旧 Colleague Skill）: https://github.com/titanwings/distilly
- Hermes公式本体: https://github.com/NousResearch/hermes-agent

### 現行AI-Harness参照
- [Hermes本体再評価](../../projects/Hermes_Local_Agent/research/2026-10-23-hermes-agent-current-reassessment.md)
- [Hermes Phase 0強化調査](../../projects/Hermes_Local_Agent/research/2026-10-15-hermes-agent-reinforcement.md)
- [Tailscale連携レイヤー](2026-10-24-tailscale-private-network-agent-access-muse-case.md)
- [スマホ操作Harness構想](2026-09-20-harness-server-mobile-control.md)
- [PiDurableKit iPhone実行系](2026-10-09-pidurablekit-iphone-durable-runtime.md)
- [Agent権限・Human承認](2026-10-16-grok-agent-permission-approval-hold.md)
- [Harnessミニマリズムの反証仮説](2026-10-16-harness-minimalism-counterhypothesis.md)
- [ECCの重複評価](2026-10-23-ecc-agent-harness-reference.md)

**注記:** 読取時点は2026-10-24。原典更新、移転、料金・互換性変更があるため、採用判断前には更新版を別途検証すること。
