---
status: research_candidate
created: 2026-11-18
source_post: https://x.com/yarad_ai/status/2122387704641986823
upstream: https://github.com/EL4CTEO/blender-skills
upstream_checked_ref: 9e7e04a603c125a0d174
stage_1_rank: A+
stage_2_rank: A
decision: CANDIDATE
implementation: HOLD / NOT_IMPLEMENTED
tags: [blender, agent-skills, codex, 3d, avatar, rigging, threejs, glb, qa, security]
---

# Blender Agent Skills（EL4CTEO）— 一次・二次評価と既存Proposal比較

調査日: 2026-11-18 JST。Humanからの依頼は研究・比較および未保存研究成果の保存。**Skillのインストール、既存Skillの置換、Blender実行、Core/Rules変更、制作プロジェクト変更は行っていない。**

## 1. 調査対象と事実確認

- 発見元: https://x.com/yarad_ai/status/2122387704641986823
- 実体: https://github.com/EL4CTEO/blender-skills （Blender Foundationの公式リポジトリではなく個人アカウントによる公開OSS）。
- X投稿等で「Blender公式チームが制作」と紹介されていても、公式制作である根拠は確認できない。**Blender本体の公式性と第三者Skillの公式性を混同しない。**
- リポジトリ作成: 2026-10-14 UTC。調査時の公開メタデータ: stars 2,094、forks 182、license MIT、default branch main、open issues 0（変動値であり品質保証ではない）。
- 調査時の最新コミット: `9e7e04a603c125a0d174`（2026-11-17）。リリース v1.3.2（2026-11-17、dense meshのrig_check不具合修正）。
- 28種類の `skills/blender-*/SKILL.md` とBlender Pythonスクリプト、導入スクリプト、`tests/`、`.github/workflows/ci.yml` を確認。Blender 5.2 LTS+対象、作者は5.3での検証を説明。Claude Code、Codex、Gemini CLI、Copilot、Cursor、OpenCode等を対象。
- `tools/run_tests.py` と `tests/run_all.py` にBlender headless実機テストの仕組みあり。READMEは67件と説明。CIは5.2.3と5.3.0を対象とし、調査時の2026-11-17の直近push CIはsuccess。**GPU依存レンダーテストは `BAS_SKIP_GPU=1` でスキップされる**。成功ログの存在は最終成果物の美観、アバターの品質、独立したセキュリティ監査を意味しない。
- 参照資料: README.md、LICENSE、install/install.sh、install/install.ps1、tools/validate_skills.py、tools/run_tests.py、.github/workflows/ci.yml、各種SKILL.md、GitHub Actions履歴。

## 2. 価値と用途

28 SkillはBlenderの制作工程を分割し、`blender-core` が作業を専門Skillへ振り分ける。代表機能:
- `blender-scene-setup`: 部屋・家具・シーンの単位、命名、階層、参照アセット管理。
- `blender-geometry-nodes`: JSON仕様からGeometry Nodes構築、反復的な形状・配置の自動化。
- `blender-pbr-materials`, `blender-texturing`, `blender-texture-baking`: PBR材質、テクスチャ、ベイク。
- `blender-character-rigging`, `blender-animation`, `blender-facial-shapekeys`, `blender-hair-grooming`, `blender-clothing`: キャラクター骨格・動作・表情・毛並み・衣服。
- `blender-game-optimization`, `blender-export-pipelines`: LOD、軽量化、GLB/glTF等への書き出し。
- `blender-asset-qa`: z-fighting、浮遊部品、法線、非多様体、UV、ウェイト、テクスチャ不良等のチェックと多視点画像レビュー。
- `blender-workflow-recipes`: モデル制作→UV→ベイク→リグ→QA→出力を連結した手順。AI生成／外部取得メッシュのクリーニング手順もある。
- `blender-core` はMCP経由のライブ操作と、MCPなしのheadless CLI操作の両方を説明。**Blender MCPは必須ではない**。

AI-Harnessの具体的な適合性:
1. **3D「小さな部屋」／Museエージェントのアバター: 最優先の比較候補。** 既定のBlender→GLB→Three.js/AnimationMixerの制作経路に適合。部屋→家具→キャラクターの順で、スケール、リグ、アニメーション、軽量化、GLB出力を支援できる可能性。
2. **UIAP BASEの3D外観／教材: 高い関連性。** ただし電気設計、寸法、製造CAD、KiCadの正本を置き換えない。
3. **Hangfire現行Canvas 2D: 低い直接適合性。** 現在は2Dゲームの既存Skillとpixelfx等を優先。
4. **AI-Harness Core: 直接統合しない。** Blender専用のプロジェクトレベルSkill候補として扱う。

### 制約
- Rigifyを利用する一般的な人型リグの手順が中心。特殊な体形・モフモフの独自アバターは骨格調整・ウェイト・変形テストが必要。
- `blender-hair-grooming` の毛束は描画コストに注意。Web表示には毛カード等の最適化が必要となり得る。
- 既存のBlenderのPython自動化より常に良いか、生成品質がどれほど向上するか、実際の所要時間・トークン費用は**未実測**。
- 新興OSSで長期運用実績は限定的。MITライセンスとCI成功だけで安全性は確定しない。

## 3. 導入・セキュリティ評価

- `install/install.sh` はデフォルトでユーザー共通の `~/.claude/skills` と `~/.agents/skills` にインストールし、同名Skillの既存パスを `rm -rf` してからsymlink/copyする。
- `install/install.ps1` も同名の既存ディレクトリを削除してコピー／junctionを作る。
- **グローバル一括導入は避ける。** 既存の同名Skillや利用環境を破壊しないよう、固定コミット・専用検証プロジェクト・必要最小限の個別Skill・既存ファイルのバックアップ・コードレビューを条件にする。
- 外部のSKILL.mdをHuman承認・Source of Truth・Access規則より上位に置かない。記載されたシェルコマンド、ファイル変更、ネットワーク処理、MCP接続を自動承認しない。
- 現段階で外部サービスの登録・課金は不要と見込むが、追加アセット／任意MCP／外部生成サービスを使う場合は別途審査。
- CIはGPUレンダリングを一部スキップ。実際の外観・glTF再読み込み・Three.js動作を別途確認する。

## 4. 既存のdevelopment Proposalとの重複・差分

| 既存記録 | 役割 | 今回との関係・追加価値 |
|---|---|---|
| `2026-10-22-spline-chatgpt-codex-3d-workflow.md` | Splineアプリ／MCPで対話的な編集可能3Dシーン制作。UIAP BASEの可視化に高い優先度 | **一部競合・補完**。Splineは対話型3Dシーン編集、今回のOSSはローカルBlenderでの3Dアセット工程・QA・GLB制作。Splineの料金・データ境界と異なる |
| `2026-10-24-hermes-plugins-official-jev-voice-gameforge-botforge.md` | Hermes公式PluginのBlender連携言及、GameForgeの素材制作・自動プレイテスト | **部分重複・補完**。GameForgeはゲーム生成／プレイテストまで含む。今回のBlender SkillsはBlenderの細分化された制作・QAに強い。Hermes公式Blender Pluginと同一製品ではない |
| `2026-11-18-hangfire-game-dev-skills-catalog.md` | Hangfireの2D Canvasに適合するgame-feel/game-ui-ux/pixelfx/Playtest等と薄いSkillルータ | **担当領域が異なる**。現在のHangfireへ28件のBlender Skillsを入れない。必要時のみSkill選択する設計原則は共通 |
| `2026-10-23-ui-ux-pro-max-skill-reassessment.md` | UI/UXデザイン判断と実装 | **補完**。3D素材と2D UIを分離 |
| `2026-10-26-addyosmani-agent-skills-evaluation.md` | コーディング工程・レビュー・品質ゲート | **補完**。一般開発プロセスとBlender固有の技術手順は異なる |
| `2026-10-15-ui-design-skill-component-comparison-prep.md` / `2026-10-27-huashu-design-skill-candidate.md` | Web/UIデザインSkill | **直接競合ではない**。3D制作・リグ・GLB QAは未充足の専門領域 |

**重複判定:** 同一OSSの保存済みProposalは2026-11-18時点のdevelopment全ツリーで見つからず。既存Spline／GameForgeと機能的重なりはあるが、Blenderの実作業用Skill＋スクリプト＋QAは独立した追加価値がある。研究情報として保存し、既存候補の置換や削除は行わない。

## 5. 評価・今後の実験条件

- Stage 1: **A+** — 3Dアバター・部屋制作との適合性が高く、実行コードと検証手順がある。
- Stage 2: **A** — 上流の構造・MIT・テストとCI成功を確認。ただし新興OSS、実環境での制作性能未測定、GPUテスト除外、インストーラーによる既存Skill上書きリスク。
- Disposition: **CANDIDATE / Implementation HOLD**。
- 推奨最小試験（**未承認・未実施**）: 既存Codex＋BlenderのみのA条件と、固定コミットの `blender-core` + `blender-scene-setup` + `blender-asset-qa` を専用環境で参照するB条件で、同じ小型家具を制作する。寸法一致、見た目、メッシュQA、GLB再読み込み、Three.js表示、所要時間、修正回数、トークン量を比較。
- 次段階の候補: 必要性が確認できた場合に `blender-geometry-nodes`、`blender-character-rigging`、`blender-animation`、`blender-game-optimization`、`blender-export-pipelines` を**個別に**評価。
- 試験成功でも即座に28件一括採用しない。スキルの参照・導入・実行・既存ファイル編集を別ゲートとする。

## 6. 確認済み／未確認

**確認済み**: 上流リポジトリ実在、ライセンス、28 Skill、代表SKILL.md、実行・検証コード、インストーラーの既存同名Skill削除処理、CI構成と直近成功、developmentの既存関連Proposalとの差分。

**未確認**: Blender Foundationの公式承認、第三者監査、ユーザー実環境でのインストール・実行、実制作の完成品質、3Dアバターのリグ成功率、GPU描画結果、GLBのThree.js互換性実測、トークン・時間の節約幅、外部アセットの個別権利条件。

## 7. 根拠リンク

- https://github.com/EL4CTEO/blender-skills
- https://github.com/EL4CTEO/blender-skills/tree/9e7e04a603c125a0d174/skills
- https://github.com/EL4CTEO/blender-skills/blob/9e7e04a603c125a0d174/install/install.sh
- https://github.com/EL4CTEO/blender-skills/blob/9e7e04a603c125a0d174/install/install.ps1
- https://github.com/EL4CTEO/blender-skills/blob/9e7e04a603c125a0d174/.github/workflows/ci.yml
- https://github.com/EL4CTEO/blender-skills/actions
- https://github.com/EL4CTEO/blender-skills/releases/tag/v1.3.2

## 保存範囲

このファイルは調査・評価・比較・安全上の注意・将来の検証条件のみ。**外部Skill本体のコピー、導入、実行、GitHub上の他ファイルの変更は含まない。**
