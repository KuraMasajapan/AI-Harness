---
document_type: ecosystem_research_evaluation
date: 2026-10-24
timezone: Asia/Tokyo
title: "Hermes Agent plugins — Official Plugins / Jev Skills / WhatsApp Voice / GameForge / Bot Forge"
source_post: "https://x.com/gittrend0x/status/2113609009676603647"
scope: AI-Harness and Hermes Local Agent
stage_1_rank: A+
stage_2_rank: A
decision: REFERENCE_CANDIDATE
relationship: PARTIAL_OVERLAP_WITH_EXISTING_RESEARCH
implementation: HOLD / NOT_IMPLEMENTED
evidence_status: "X post and five upstream repositories and README examined; integration, benchmarks, security untested"
human_approval: "2026-10-24: save reviewed material for future reference; no implementation permission"
tags: [hermes, plugins, official-plugins, jev, routing, context-filter, whatsapp, voice, gameforge, gamedev, playtesting, bot-forge, agent-teams, skills, memory, local-ai, research-only]
trigger_topics:
  - Hermes
  - Hermes Plugins
  - Jev
  - モデル振り分け
  - ルーティング
  - コンテキストフィルター
  - WhatsApp音声
  - 家族AI音声
  - GameForge
  - 自動プレイテスト
  - ゲーム開発
  - Bot Forge
  - Agent生成
  - 動的Agentチーム
---

# Hermes Agentプラグイン群：公式Plugins・Jev・音声・GameForge・Bot Forge

> **一読で分かる要点**
> 2026-10-23のX投稿が紹介するHermes Agent関連の5リポジトリを一次資料で照合した。いずれも実在する。ただしAI-Harness内には、Jevによるコンテキスト選択、音声操作、動的Agent構成、Hermesの周辺OSS調査など**近い研究が既存**。今回の価値は、関連する新しい**具体的実装や公式Pluginカタログ**を見つけたこと。5件を記録として保持するが、5件の導入・次期アップデートへの組み込みは決定しない。

**調査評価**：一次 A+、二次 A、PARTIAL OVERLAP / REFERENCE CANDIDATE、実装 HOLD。重要度は控えめ。**保存範囲と採用範囲を区別する**。

## 1. 発見元・対象リポジトリ・証拠の区分

- 元投稿：[@GitTrend0x、2026-10-23](https://x.com/gittrend0x/status/2113609009676603647)。中国語の紹介投稿。Hermesが「公式プラグイン集＋低費用の判断モデル＋電話助手＋ゲーム工房＋Bot自動生成」へ発展するという趣旨。
- 投稿は**宣伝的な要約**であり、効果・費用・安定性の独立した証拠ではない。
- 原典の確認先：以下の5つのGitHubリポジトリのREADMEおよびリポジトリ情報。2026-10-24時点の説明を記録。5件ともリポジトリ自体を確認でき、GitHubのメタデータにはMITライセンスと記載。
- **確認できたこと**：プロジェクトの実在と、READMEに記載された機能・前提条件・制約。
- **未確認**：実際の家庭用Windows PCでの稼働、モデル/API費用の実測、比較対象に対する性能優位、継続運用・独立セキュリティ監査、各機能の適法な利用。

| 対象 | 主な役割 | 今回の独立した記録価値 | 判定 |
|---|---|---|---|
| [NousResearch/hermes-official-plugins](https://github.com/NousResearch/hermes-official-plugins) | Nous Research製の第一者Plugin集／カタログ方式 | 公式の拡張・審査・更新モデル | A / REFERENCE |
| [kerpopule/hermes-jev-skills](https://github.com/kerpopule/hermes-jev-skills) | 軽量な意思決定モデルJevによる振り分け・検索・Memory/Skill選択 | **既存Jev研究の具体的な応用例** | A / REINFORCE |
| [ashwanthbalakrishnan5/hermes-whatsapp-voice](https://github.com/ashwanthbalakrishnan5/hermes-whatsapp-voice) | WhatsAppのリアルタイム通話でHermes操作／通知 | 音声入口・能動的な電話通知の事例 | B / REFERENCE |
| [DECRUX9812/hermes-plugin-gameforge](https://github.com/DECRUX9812/hermes-plugin-gameforge) | ゲーム素材作成から自動プレイテスト・出力まで | テスト証跡の仕組みが既存ゲーム開発へ関連 | A / CANDIDATE（比較のみ） |
| [BkashJEE/hermes-bot-forge](https://github.com/BkashJEE/hermes-bot-forge) | 役割から永続的Bot/チームを生成・運用 | 既存の動的Agent構想を具体化 | B+ / REFERENCE |

5件は同じ機能の別製品ではない。前の[Hermes Agent周辺エコシステム調査](2026-10-24-hermes-agent-community-extensions-landscape.md)とは**別の5リポジトリ**であり、同じ機能がある場合でも同一OSSとは言わない。

## 2. 公式Plugins — Hermes本体が目指す「小さなCore＋選択式拡張」

**原典**：https://github.com/NousResearch/hermes-official-plugins

Nous Researchが開発・保守する第一者Pluginをまとめたリポジトリ。Hermes本体のAgent Loop、Memory、Skills、Gateway、Tool runtimeを残し、特定サービスへの連携をPluginへ分離する設計と説明する。

**READMEで確認した代表例**：
- Home Assistant：家庭内デバイスの状態監視とサービス実行。家族用ローカルAI構想と関係するが、機器操作には認証・承認が必要。
- Spotify：再生、検索、Playlist、Libraryの操作。音楽操作にはSpotify Premiumが必要な機能あり。
- Claude Subscription DirectSDK：Claude Code CLI経由のSubscription連携を**実験的**Pluginとして紹介。これは各社の規約・利用資格を無条件に保証するものではない。
- Memory Wiki：ローカル履歴を話題別ページや日次ログで読む。既存AI-Harness Memory/Obsidianとの比較対象。
- Blender、Snyk、Langfuseなど：3D、セキュリティ検査、Tool/Model trace・費用可視化の連携。
- カタログは`official`と`community`の区分を設け、**レビュー済みCommitへPin**する運用を説明。`hermes plugins search/info/install/update`で選択・管理する方式。

**AI-Harnessへの意味**：Pluginが増えても全機能をCoreに取り込まない設計、レビューしたバージョンの固定、必要機能だけの有効化が参考。既存のSkills/Plugins管理方針と類似する。**正式公式の提供先として今回の5件では最も確度が高いが、個別Pluginの安全性・互換性・提供条件まで保証しない。**

## 3. Hermes Jev Skills — 既存Jev候補の具体化

**原典**：https://github.com/kerpopule/hermes-jev-skills

JevはTypeSafeの**分類・選択・採点など限定された意思決定を扱うモデル**という位置づけ。READMEは文章生成役ではないと明記。Hermesだけでなく、Skillフォルダを通じてCodex／Claude Codeでも利用可能と説明する。

**READMEに記載された用途**：
- モデル/Providerの選択（どのモデルへ依頼するか）
- Skillsの選択、検索候補や結果の順位付け、必要なコンテキストのKEEP/DROPに近い判断
- Memory検索結果やWebテキストの扱い、指示混入／プロンプトインジェクションのスクリーニング
- 受信メッセージの優先度付け、Inbox分類、GUI／ブラウザ操作の限られた選択
- `shadow`モードで「Jevが何を選ぶか」のみ記録し、実際のモデル切替はしない比較手順。

**証拠の扱い**：作者のベンチマーク、トークン節約、Web injection検出率、応答遅延、377 Skills等は作者の条件付き結果であり、Harnessで再現したものではない。READMEには、Jevによる圧縮がむしろリコールを下げた事例も記載。全判断をJevに委譲しない。

**既存研究**：`2026-09-21-jev-context-filter-adoption-model.md` は、Jevを置き換え可能なContext Filterに限定し、Rules、Source of Truth、sealed、承認済み判断などをKEEP/DROPから除外する方針。**Jevそのものは既出であり、今回の価値は用途とテスト方法の追加情報**。先日の[2ルーター冗長化研究](2026-10-24-router-redundancy-failover-research.md)にも類似の「振り分け」概念はあるが、**JevはRouterの冗長化装置ではない**。導入はHOLD。

## 4. WhatsApp Voice — 遠隔音声操作と電話によるエスカレーション

**原典**：https://github.com/ashwanthbalakrishnan5/hermes-whatsapp-voice

WhatsAppの電話でHermesと話し、通話中にHermesへ仕事を渡す。Hermes側から電話をかけ、通話後に要約を送信する。実装は`whatsapp-rust`を使った別プロセス（sidecar）とGemini Liveを接続し、Hermes API serverを呼び出す方式と説明。

**主な利用条件と重大な留意事項**：
- Linux/macOSを対象とし、Bot用の**別WhatsApp電話番号**、Gemini API key、Hermes API serverでの認証が必要。
- Gemini Liveによる音声入出力は無料枠・課金条件が関係する。READMEの単価や提供モデルは変わるため再確認する。
- READMEは**非公式のリバースエンジニアリングされたWhatsApp通話プロトコル**を使うと明記。WhatsAppの仕様変更や規約違反のおそれがあり、動作継続性を保証しない。
- WhatsAppのリンク済み端末セッションや音声・通話の内容、Gemini側への音声送信、クラウドデータ管理の影響がある。

**既存との関係**：家族用音声AI/STT/TTS、`speech.cpp`等のローカル音声候補とは入力・出力の構成が違う。今回は**スマホから話しかける入口と重要通知の事例**としての参照価値。高い運用負担と外部依存があり、当面の採用優先度は低い。

## 5. GameForge — ゲームを作るだけでなく「本当に動かして試す」

**原典**：https://github.com/DECRUX9812/hermes-plugin-gameforge

READMEには音楽、効果音、NPC音声、Sprite、Tileset、ローポリ3D生成、Web/Godot/Unity等のプロジェクト生成、Export、ゲームプレイの自動試験を提供するとある。主要な手続き的生成はオフラインを基本とし、fal.ai/Meshy/ElevenLabs/Edge TTS等の外部生成はオプション。

**特徴的なのは`forge_playtest`**：
- Headless Chromeで実際のWebゲームへキー入力する探索プレイヤー、ランダム入力、Vision Modelを使うAgent試験。
- GodotのBot操作、Crash検出、操作不能、進捗停滞、Frame rate、Heatmapなどの検証。
- HTML/Markdown/JSONの試験レポート、失敗フレーム画像、例外のStack traceを成果物として保存。
- 重大エラーなら`BROKEN`などのVerdictとする規則を記載。**テスト報告の自動生成が品質保証の十分条件という意味ではない。**

**AI-Harnessとの関係**：Hermesを使う前提とは切り離しても、既存のゲーム開発／Codexの手動テストと、**証跡付き自動プレイテスト**の比較対象として具体性が高い。実際に特定のゲーム環境で試すには互換性と権限、実測負荷の確認が必要。新規OSSで長期運用の実績は限定的。**この5件の中では追加価値を検証しやすいテーマ**。

## 6. Bot Forge — 一文から持続するBotを構築する

**原典**：https://github.com/BkashJEE/hermes-bot-forge

指示に応じて、名前、SOUL.md、初期Memory、必要なTools/Skills、定期処理、Gateway等を備えたHermesの**永続Bot profile**を作成するPlugin。

**READMEで確認した重要な条件**：
- 既存Bot/Skill/一時委譲で足りないかを先に確認し、持続的な役割に理由がある場合だけ新規生成する設計。
- 「プロフィールはセキュリティsandboxではない」と明記。Chat、Memory、Tools、API鍵継承、権限は個別に考える。
- Approval checkpointや承認待ちの可視化などを説明するが、AI-HarnessのHuman承認と同等の実効的な強制を本調査で確認したわけではない。
- READMEは**Linux/macOSをテスト済み、Windows非対応**と明記。将来の家庭用Windows環境では明確な導入障壁。
- 多Agent化は持続処理、モデル課金、メモリ分離、権限と監査の負荷を生み得る。

**既存研究との関係**：`2026-09-20-dynamic-agent-team-composition.md`（必要なRoleを最小数だけ組む）、TRINITY、Hermes Local AgentのSubagents等と強い重複。持続Botの**具体実装例**としては有用だが、既存の人間承認・Source of Truth・権限制約が置き換わることはない。即導入は不要。

## 7. 既存情報との比較：同じものか、似ているものか

| 既存記録 | 重複の種類 | 今回の増分 |
|---|---|---|
| [Hermes周辺5 OSSの横断調査](2026-10-24-hermes-agent-community-extensions-landscape.md) | **分野が同じ／対象リポジトリは別** | 公式Plugin集＋Jev Skills＋音声通話＋GameForge＋Bot Forgeの具体実装 |
| [Jev Context Filter](2026-09-21-jev-context-filter-adoption-model.md) | **技術の主題が一致／実装は追加** | Hermes/CodexへのSkillsとShadow運用事例 |
| [Dynamic Agent Team Composition](2026-09-20-dynamic-agent-team-composition.md) | **目的・概念が類似** | 永続Bot Profileの生成・運用というOSS実装 |
| [speech.cpp local voice](2026-10-14-speech-cpp-local-voice-preferred-candidate.md) | **音声入力の目的は近いが技術レイヤーが違う** | WhatsApp電話/Gemini Live経由の音声Gatewayと通知 |
| [Router Redundancy](2026-10-24-router-redundancy-failover-research.md) | **振り分けという語が共通だが問題が違う** | Jevは小判断、Router冗長化はRouter故障への退避経路 |
| Hermes本体（`projects/Hermes_Local_Agent/research/2026-10-23-hermes-agent-current-reassessment.md`） | **本体標準機能との重なり** | 外部Pluginならではの差分を将来確認 |

既存の研究に似た概念があることは調査成果であり、**同名の記録がない＝全機能が新規**とはしない。今後も各OSSと既存機能のActual overlap / Complement / Missingを確認する。

## 8. 初回の研究判断と採用ガード

- **Stage 1: A+** — 発見した5件はいずれも実在し、AI-Harness全体の方向性との接点がある。
- **Stage 2: A / REFERENCE CANDIDATE** — 既存のJev、音声AI、動的Agent、Hermesエコシステム記録との重複が強い。公式プラグイン管理とGameForgeの実装方式は具体的な追加価値。
- **Implementation: HOLD** — 現時点でHermes Local AgentはPhase 0。ダウンロード、インストール、設定、外部アカウント連携や本体変更は未承認。
- **現時点の注目箇所**：第一者PluginのCommit pin方式、Jevのshadow評価、自動プレイテストの証跡。**部分採用を既定にせず、すべての構成と制約を記録したうえで**後日判断する。
- **重要リスク**：非公式WhatsApp連携、クラウド音声・家族情報、APIキーや認証の継承、Shell/Files操作、Bot増殖、GPU/CPU/Memory負担、API課金。
- **評価が変わる条件**：本体Phase進行、導入環境・OSの明確化、同一タスクでの既存環境との比較、安全性・利用規約の検証、測定結果による差分の実証。

## 9. 将来の参照手順（まだ実施しない）

1. HermesやPluginの最新版とLICENSE、公式カタログ上のPin先、必要な依存・権限を確認する。
2. 既存機能で実現可能か、用途と機能ごとに**Already present / Partial / Missing / Not needed**を分類する。
3. 必要性が明確なものだけ、分離された低権限テスト環境で同一課題をBaselineと比較する。自動変更・Bot作成・電話・外部通知は事前にHuman承認が必要。
4. コスト、正確性、プライバシー、二重実行、証跡の質、ロールバック難易度を比べて別途採否を決める。
5. この研究文書は情報源として保持し、試験結果や採用・不採用理由を追跡可能にする。

## 10. 保存と権限の境界

2026-10-24、Humanは「まあまあかな。一応保存して」と研究保存を承認。本ファイルのみ新規保存。技術を推奨・採用済みと扱わず、全体の機能説明・確認できた条件・リスクを残す。**5件のソース全体を複製したものではなく、原典リンクから辿れる調査記録**である。

Core/RULES/WORKFLOW/ACCESS、Hermes本体、BBB、その他のProposal、運用権限、GitHub以外の接続は変更しない。実装は別途Human承認を必要とする。
