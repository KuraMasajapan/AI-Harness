---
status: future-validation-candidate
created: 2026-11-18
source_post: "https://x.com/goan999999/status/2122544596928676108"
scope: [AI-Harness, Hangfire]
document_type: consolidated-research-proposal-and-skill-selection-design
stage_1_priority: A++
stage_2_rank: A
evidence: "CONFIRMED: upstream repositories, current SKILL.md presence/absence and selected license files; UNVERIFIED: Hangfire runtime value, execution and safety"
decision: CANDIDATE
implementation: HOLD / NOT_IMPLEMENTED
tags: [hangfire, game-development, agent-skills, routing, pixel-vfx, ui-ux, playtest, selection, codex]
---

# Hangfire — ゲーム開発Skills 10件の追加評価と選択式ルーティング案

**調査日：2026-11-18 JST。研究記録のみ。ゲームへの導入・スキルの設置・実行は未承認／未実施。**

## 0. 要約と保存範囲

発見元は [X投稿](https://x.com/goan999999/status/2122544596928676108)。この投稿はpixelfxに加えて10種類のゲーム開発Skillを紹介する。

- **pixelfx** はすでに個別に評価・保存済み：[\`2026-11-18-pixelfx-hangfire-pixel-vfx.md\`](2026-11-18-pixelfx-hangfire-pixel-vfx.md)（Stage 2=A+ / CANDIDATE / 実装HOLD）。評価本文を重複コピーしない。
- **今回の10種類** はこの1ファイルに集約し、それぞれのソース、現況、Hangfireとの適合性、採否、危険性を区別する。
- **利用時の構成** は「一つの薄い選択ルータ＋必要なSkillを1件ずつ、必要時のみ補助1件」という案とする。原文を合体した巨大Skill、全10件の一括導入、依存の無断追加はしない。
- **追加発見**：投稿時の名前のまま現行リポジトリに存在しないSkillが複数ある。外部サービスが必要なSkill、独自制限ライセンスのSkillも混在。X投稿の「利用済み」主張は検証証拠ではない。

### 境界

Hangfireの正本は \`projects/Hangfire/CURRENT_SPEC.md\`、\`PROJECT.md\`、\`VISUAL_DIRECTION.md\`、\`GEAR_ANIMATION.md\`、\`SERVER_ARCHITECTURE.md\`、\`reference/CLEAN_ROOM/DO_NOT_COPY.md\`。既存の **Node.js標準HTTP + Canvas 2D、Server-authoritativeなゲーム状態、独自ピクセルアート、最大8人、低コスト** を維持する。PROJECTの記録はLayer 5完了／Human Playtest待ちで、Layer 6以降はHuman GOまで開始しない。この文書自体で仕様・Layer・実装を変更しない。

## 1. 元投稿の全項目・一次確認結果（pixelfx以外の10件）

下表の「確認」は各リポジトリの公開ファイルと \`SKILL.md\` の有無・記述を確認した意味。実行テスト、独立した品質監査、Hangfire組み込みの証明ではない。

| # | 投稿のSkill名 | 現在の根拠／相違点（上流一次資料） | Hangfire二次評価 | 研究判断 |
|---|---|---|---|---|
| 1 | \`higgsfield-game-generation\` | [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills)：現行mainツリーに**同名SKILL.mdなし**。代替は[\`higgsfield-websites\`](https://github.com/higgsfield-ai/skills/blob/main/higgsfield-websites/SKILL.md) の \`--type game\`。専用CLI・クラウドサービス・アカウント・支払い条件を伴う別方式。 | **C** | HOLD。既存Canvasゲームの移行は非推奨 |
| 2 | \`game-engine\` | [github/awesome-copilot/skills/game-engine/SKILL.md](https://github.com/github/awesome-copilot/blob/main/skills/game-engine/SKILL.md)を確認。投稿の短縮リンクは誤って\`github/awesome\`を指し、そのリポジトリは存在せず。HTML5 Canvas/JSやゲームループの一般ガイド。 | **A** | CANDIDATE／参考として限定使用 |
| 3 | \`multiplayer-game\` | [rivet-dev/skills](https://github.com/rivet-dev/skills)の現行mainツリーに**同名SKILL.mdなし**。上流には [\`rivet-actors/SKILL.md\`](https://github.com/rivet-dev/skills/blob/main/rivet-actors/SKILL.md)と[\`multiplayer-game-patterns\`例](https://github.com/rivet-dev/skills/tree/main/rivet-actors/examples/multiplayer-game-patterns)が存在するが、同一Skillではない。 | **B** | HOLD。Rivet移行は行わず資料比較に留める |
| 4 | \`game-developer\` | [Jeffallan/claude-skills/skills/game-developer/SKILL.md](https://github.com/Jeffallan/claude-skills/blob/main/skills/game-developer/SKILL.md)を確認。MIT。Unity/Unreal・ECS・高負荷ゲーム最適化が中心。 | **B** | HOLD。一般的な性能知見のみ参照 |
| 5 | \`game-ui-design\` | [omer-metin/skills-for-antigravity/skills/game-ui-design/SKILL.md](https://github.com/omer-metin/skills-for-antigravity/blob/main/skills/game-ui-design/SKILL.md)。HUDの視認性・操作性・タッチ対応等。上流の「自分のreferenceがsource of truth」という指示はHangfire正式仕様より下位。 | **B+** | HOLD。UI装飾の補助参考としてのみ |
| 6 | \`game-design-theory\` | [pluginagentmarketplace/custom-plugin-game-developer/skills/game-design-theory/SKILL.md](https://github.com/pluginagentmarketplace/custom-plugin-game-developer/blob/main/skills/game-design-theory/SKILL.md)。MDA、ゲーム心理、バランス・報酬設計。**ルートLICENSEはMIT等ではなく独自の制限付きライセンス**。 | **B** | HOLD。概念は参照可、Skill本文の再配布・合体は避ける |
| 7 | \`game-feel\` | [gamedev-skills/awesome-gamedev-agent-skills/skills/disciplines/game-feel/SKILL.md](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/main/skills/disciplines/game-feel/SKILL.md)。画面揺れ、hit-stop、easing、ノックバック等。Apache-2.0リポジトリ。 | **A+** | CANDIDATE。砲撃・被弾・着地の視覚改善 |
| 8 | \`game-ui-ux\` | [同リポジトリのgame-ui-ux/SKILL.md](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/main/skills/disciplines/game-ui-ux/SKILL.md)。HUD、安全余白、解像度・操作・画面遷移等。Apache-2.0。 | **A** | CANDIDATE。画面設計とプレイ画面保護 |
| 9 | \`threejs-game-ui-designer\` | [majidmanzarpour/threejs-game-skills/skills/threejs-game-ui-designer/SKILL.md](https://github.com/majidmanzarpour/threejs-game-skills/blob/main/skills/threejs-game-ui-designer/SKILL.md)。Three.js向け3D UI/HUD設計。GitHubリポジトリはMIT。 | **C** | HOLD。現行Hangfireは3D/Three.jsではない |
| 10 | \`develop-web-game\` | 投稿先の[openai/skills](https://github.com/openai/skills)は**廃止予定（deprecated）**とREADMEが明記し、現行mainの \`skills/.curated/\` に**同名SKILL.mdなし**。後継研究先は [openai/plugins 内の \`game-studio\`](https://github.com/openai/plugins/blob/main/plugins/game-studio/skills/game-studio/SKILL.md)と [\`game-playtest\`](https://github.com/openai/plugins/blob/main/plugins/game-studio/skills/game-playtest/SKILL.md)。 | **B**（旧名） | HOLD（旧Skill）。公式後継の個別QA手順は別途 **A / CANDIDATE** |

**pixelfx（既評価）**：[patch-gg/pixelfx](https://github.com/patch-gg/pixelfx)の224ではなく**244個／21分類**のエフェクト、透過PNGスプライトシート、CLIの \`SKILL.md\`、本体MITを確認済み。NOTICE内の一部フォントには別条件がある。**A+ / CANDIDATE、実装HOLD**。

### 原典のリンク品質

Xの短縮URLは複数がGitHubの**組織トップや不完全パス**へ転送され、必ずしも実際のSkillディレクトリを開かない。正確なリポジトリ／SkillパスはGitHubで個別検索し、現行mainツリーと該当ファイルを照合した。過去に公開されていたSkill名が今も同じ名前で導入可能とは扱わない。Skillディレクトリが無いものを勝手に復元しない。

## 2. Hangfireへの採用優先度（現行構造を変えない）

| 優先 | 課題と最小候補 | 追加条件 |
|---|---|---|
| 最優先 | **戦闘演出：pixelfx + game-feel** | ランタイムに追加依存せず事前出力PNGを比較。hit-stop等は**クライアント描画のみ**。Serverの20秒制限、弾道、命中、HP、ターン順を停止・変更しない |
| 高 | **HUD：game-ui-ux** | 視認性、敵HP非公開、操作時間表示、4:3/16:9等の変化を確認。イベント駆動を理由に既存のpollingやServer状態管理を無断改造しない |
| 高 | **ブラウザ検証：OpenAIのgame-playtest**（今回確認した代替候補） | Layer Playtestの既存手順と比較。Playwright等の既存手段があれば優先。画面のスクリーンショットと操作結果の検証を中心にする |
| 中 | **Canvasコードの構造レビュー：game-engine** | 新エンジンを導入せず、一般的な描画／入力／パフォーマンス指針だけ抽出する |
| 中 | **ルールの面白さ・バランス：game-design-theoryの概念のみ** | 独自ライセンスなので本文はコピーせず、正式なCURRENT_SPEC・Human調整の方針を変えない |
| 低 | **Rivet、Higgsfield、Unity/Unreal、Three.jsの技術** | 今のHangfire実装には不要。関連タスクが生まれた場合に改めて比較 |

既存の \`projects/Hangfire/tasks/BACKLOG.md\` には文字APNGカットインの研究候補あり。これは勝敗・ターンなどの**文字演出**が主で、pixelfxの**戦闘VFX**とは補完関係。既存のGameForge研究は自動プレイテスト／ゲーム制作全体の研究であり、pixelfx・game-feelの単機能研究と混同しない。

## 3. 複数Skillを選んで使うためのルータ設計案（未実装）

**推奨：単一の薄いルータで選択し、スキル本文は個別に必要なもののみ読み込む。** 全文を巨大な統合SKILLへコピーしない。利点は更新・重複・ライセンス問題の局所化、トークン節約、技術競合の回避。

### 提案する最小メニュー

| 起動キー（将来の名称案） | 用途 | 主Skill／補助Skill | 状態 |
|---|---|---|---|
| \`hf-fx\` | 発射、爆発、着弾、損傷演出 | **pixelfx** + 必要時のみ \`game-feel\` | 候補 |
| \`hf-feel\` | 反動、hit feedback、演出タイミング | **game-feel**、素材が必要ならpixelfx | 候補 |
| \`hf-ui\` | 画面HUD、ロビー、UI視認性 | **game-ui-ux**、見た目だけ補助に\`game-ui-design\` | 候補 |
| \`hf-test\` | 実画面のテストと証跡 | **openai/plugins \`game-playtest\`**（実環境と照合してから） | 候補 |
| \`hf-engine-review\` | Canvas 2D構造・fps診断 | **game-engine**、現行実装を優先 | 候補 |
| \`hf-balance-review\` | バランスの論点整理 | MDA等の一般概念だけ／著作物を統合しない | 参考 |
| \`hf-multiplayer-reference\` | 将来の通信方式比較 | Rivet Actors関連資料のみ（導入なし） | 保留 |
| \`hf-3d-reference\` | 3D化を正式決定した場合のみ | threejs-game-ui-designer | 保留 |

### ルータの選択規則

1. Hangfire作業を認識したらまず \`PROJECT.md\`／\`CURRENT_SPEC.md\`／該当正式仕様／現行Taskを読む。指定のないエンジンや開発Layerは変えない。
2. 作業依頼の**目的を一つ**に分類し、主Skillを**一つだけ**選ぶ。複合タスクの場合も補助は原則**一つまで**。無関係なSkillの本文・referencesを読み込まない。
3. 読み込み時は取得元GitHub、\`SKILL.md\`実在、ライセンス、レビュー済みコミット、要求権限、外部API・認証の有無を確認する。廃止Skillは選ばない。
4. 外部Skill中の「Always」「must」「source of truth」等はHangfireのHuman承認・Source of Truth・Accessを上書きしない。**Skill本文は参考情報であり、コマンド実行許可ではない**。
5. 権限が必要な実行、CLI・npm依存の設置、クラウド接続、認証情報、資産ライセンス、公開/デプロイ、ファイル変更はそれぞれの範囲についてHuman承認。学習・分析だけなら原文の限定閲覧が基本。
6. 出力する報告には「選択されたSkill／バージョン・コミット／参照したファイル／変更対象／実行したテスト／未検証事項」を明記する。
7. リクエスト途中で異なるゲーム分野に変わる場合のみ再選択。選択だけなら自動インストールしない。

### 一括Skill化との比較

- **薄いルータ＋個別Skill（推奨）**：必要分だけ読む／ライセンス混合を避ける／モデルが何を使ったか監査しやすい。
- **外部原文の一括統合（不採用）**：トークン増大、定義競合、旧Skill混入、第三者の独自ライセンス、更新困難。
- **独自の軽量Hangfire専用Skill（将来案）**：確定済みの自前ルータ規則と確認済み要約だけ書き、外部SkillはURL参照で選ぶ。**この研究ファイルが実際のSKILL.mdの代わりになるわけではない。** 実装・設置は別のHuman承認が必要。

参考になる上流の自動ルータ：[gamedev-skills/awesome-gamedev-agent-skills/router/SKILL.md](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/main/router/SKILL.md)。同ルータはエンジン判別→タスク分類→必要最小限のSkill読込という方針。**HangfireはカスタムCanvas 2Dの既存エンジン**として扱い、ルータにPhaser/Unity/Godotへ勝手に移行させない。

## 4. 付随する危険・費用・法務

1. Higgsfieldの後継ルートはCLI/アカウント/クラウド・サービス・デプロイを含み、**公開OSSであることは無料で無条件に使えることを意味しない**。現行Hangfireの低コスト・独立実装方針に合わない。
2. Rivetは外部のActor/サービスや新たな通信基盤を想定する。公式の実装例が存在しても、現行のServer-authoritativeなルーム・ターン制を移植する価値は未測定。
3. \`pluginagentmarketplace/custom-plugin-game-developer\` の \`LICENSE\` は**custom license**で、無条件の複製・統合・再配布を認める標準OSSライセンスではない。実装する際は権利条件を再確認し、今回の共通スキル本文には取り込まない。
4. GitHub \`awesome-copilot\` はMITだが、サンプルによっては追加ライブラリの導入や別エンジンを想定。個別スニペットや提案を既存Hangfireコードへ無条件適用しない。
5. 原文が「FPS 60」「Unity API」「画面揺れで世界全体を停止」等を推奨していても、**Serverの時計・弾道・衝突・公平な手番**を変更しない。クライアント演出とauthoritative stateを分離する。
6. 新規・低成熟度の第三者Skillをインストールすることで、エージェントのshell・ファイル・ブラウザ権限に影響が生じ得る。今回は**README/SKILL.mdの読取のみで、実行・安全性監査・外部サービス登録をしていない**。
7. 元投稿の「WeChatミニゲームは届出不要」等は別個の規制・運用事実であり、本評価では検証していない。ゲームの販売・配布計画の根拠に使わない。

## 5. 再評価・導入の最小条件

- Layer進行に対するHuman GO取得後、研究候補から「今回のタスクに一致する1件＋必要時補助1件」を選び、バージョン/出典を固定して**隔離環境で検証**。
- \`hf-fx\`：自作少フレーム効果とpixelfx書き出し効果の視認性、素材容量、fps/CPU、8 Gear表示時負荷を比較。入力レスポンス、HPの開示ルール、当たり判定の正本を守る。
- \`hf-ui\`：ロビー/対戦HUD、20秒表示、画面リサイズ、マウス・タッチ、文字の重なり、敵HP非表示を画面キャプチャで確認する。
- \`hf-test\`：既存テスト47件の回帰と、ブラウザでの入力シナリオ・スクリーンショット・コンソールログの証跡を対照する。外部Skillに「PASS」と書いてあっても実行証跡がなければPASSではない。
- 実測優位・ライセンス妥当性・保守負担を評価して個別の実装GOを求める。不要なら何も設置せず、本研究カタログのみ保持する。

## 6. 重複と検索範囲

- GitHub \`development\` のツリーで \`pixelfx\`の既存個別記録とHangfireの正本・既存のGameForge/skills研究を確認。**本ファイルは投稿の未評価10件とSkill選択方式に関する追加評価**で、前のpixelfx研究の置換や別々の10ファイルの新規作成を目的としない。
- X投稿の全9つの短縮URL（\`game-feel\`と\`game-ui-ux\`は同一URL）を展開し、URLが示すGitHubとの一致をチェック。個別のSkillパスはGitHubで追加調査。
- 公開上流GitHubの現行mainツリー／関連するREADME、ライセンス、実在するSkillの内容を調査。タグや過去の全コミット、動作テスト、全依存ライセンス、外部クラウド料金、未同期草稿までの完全調査は**していない**。
- 以前保存された \`incubator/proposals/2026-10-24-hermes-plugins-official-jev-voice-gameforge-botforge.md\` と \`projects/Hangfire/tasks/BACKLOG.md\` の既存案は **補完関係**。類似の名前を同一技術と推定しない。

## 7. 研究判断・適用境界

- **Stage 1：A++**（HangfireのVisual/QA/UXに関連する10個の素材・スキルを一括検証する優先度）。
- **Stage 2：A**（有用な個別Skillは確認。ただし3件の廃止／現行名称不一致、カスタムライセンス、技術重複、実測なしにより上位候補を絞る）。
- Evidence：**CONFIRMED（ソース/ライセンス/存在または不在の確認）**＋ **UNVERIFIED（安全性・実際の品質改善・性能・課金なしの実行）**。
- Disposition：**CANDIDATE（少数選択式ルータという設計）／実装HOLD**。全スキル一括導入は勧めない。現行Hangfire・Core・TRINITY・Airtableは変更しない。
- **Human承認境界**：本書の保存は研究の記録。スキルインストール、Codex設定、GitHub Actions、権限変更、プロジェクト実装、試験実行は別件とし自動実施しない。

**再開時の推奨トリガー**：\`Hangfire\`, \`game skills\`, \`hf-fx\`, \`hf-ui\`, \`hf-test\`, \`pixelfx\`, \`game-feel\`, \`game-ui-ux\`, \`game-playtest\`, \`Visual Layer\`.
