---
status: future-validation-candidate
created: 2026-11-18
origin: "Human-shared X post (2026-11-17) and upstream GitHub read-only review"
source_post: "https://x.com/goan999999/status/2122544596928676108"
source_repository: "https://github.com/patch-gg/pixelfx"
project_scope: [AI-Harness, Hangfire]
stage_1_rank: A++
stage_2_final_rank: A+
evidence_status: "CONFIRMED (repository/source, catalog, SKILL.md, license, documented format); UNVERIFIED (Hangfire integration, game performance, visual acceptance)"
dedup_status: NEW
decision: CANDIDATE
implementation: HOLD / NOT_IMPLEMENTED
human_approval: "2026-11-18: Human approved saving this research note to development/incubator/proposals/2026-11-18-pixelfx-hangfire-pixel-vfx.md; no installation, game project edit or layer promotion approved"
tags: [hangfire, pixel-art, game-effects, vfx, sprite-sheet, canvas2d, codex, game-development, lightweight, visual-layer]
trigger_topics: [Hangfire, pixelfx, muzzle-flash, explosion, hit-spark, smoke, damage-visual, sprite-sheet, visual-layer, pixel-art]
---

# pixelfx — Hangfire向け軽量2D戦闘エフェクト候補

## 0. 判断要約

**結論：A+ / CANDIDATE（研究保存）、実装HOLD。** `patch-gg/pixelfx` は、2Dピクセルアート戦闘ゲームに必要な発射、着弾、爆発、火花、煙、ダメージ表現を、コードまたは書き出したPNGスプライトシートとして使用できる候補。Hangfireの軽量・Canvas 2D・クライアント描画設計に適合する可能性が高い。ただし導入効果・性能・現行ゲームとの見た目の一致は未検証であり、**ソース素材を直ちにゲームへ組み込まない**。

本資料は技術の研究候補であり、Hangfireの`CURRENT_SPEC.md`、`VISUAL_DIRECTION.md`、`GEAR_ANIMATION.md`、レイヤー開発順、Human GO条件、既存の承認境界を変更しない。

## 1. 原典と照合した事実

- 発見元：[2026-11-17のX投稿](https://x.com/goan999999/status/2122544596928676108)。投稿はWeChatミニゲーム市場や他のゲーム開発スキルも紹介しているが、本候補の主対象はpixelfxのみ。投稿者の収益・開発容易性・WeChat公開規則等の宣伝的主張はこの評価の根拠にしない。
- 一次資料：[patch-gg/pixelfx](https://github.com/patch-gg/pixelfx)、[README](https://github.com/patch-gg/pixelfx/blob/main/README.md)、[Catalog](https://github.com/patch-gg/pixelfx/blob/main/docs/CATALOG.md)、[Skill](https://github.com/patch-gg/pixelfx/blob/main/skills/pixelfx/SKILL.md)、[package.json](https://github.com/patch-gg/pixelfx/blob/main/package.json)、[LICENSE](https://github.com/patch-gg/pixelfx/blob/main/LICENSE)、[NOTICE](https://github.com/patch-gg/pixelfx/blob/main/NOTICE.md)。2026-11-18調査時のmain。GitHubメタデータ上は2026-10-30作成の比較的新しいリポジトリ。
- `docs/CATALOG.md` は**21分類・244種類**のピクセルアート効果を列挙。`src/fx/<category>/<name>.js` に個別実装があり、`impacts`、`projectiles`、`explosions`、`fire`、`weather`、`ui`等を確認。
- README/Skillは、JS/TSのCanvas/WebGLゲームにおけるコード実行と、PNGスプライトシート＋JSONメタデータへの事前書き出しの両方を記載。色変更、向き反転、動作確認用のコンタクトシート・GIF/MP4、フレーム・はみ出しなどのチェック用ツールを提供。
- Node.js **18以上**が前提、GIF/MP4プレビューではffmpegはオプション。`package.json`はMIT、`LICENSE`本文もMIT。`NOTICE.md`はSprite Fusion/Hollow Crown由来のMIT表記と、**gallery/fonts内のPatch PixelフォントはリポジトリMITの対象外**であることを明記。
- 専用のClaude Code Skillが同梱される。CodexでもSKILL.md等を説明資料として読むことはできるが、当環境でのプラグインとしての自動動作は未確認。

**証拠の限界：** GitHubの内容と形式は確認したが、実際にpixelfxをインストール・実行したり、Hangfireで描画、FPS計測、素材の見た目のHuman承認を得たりしていない。

## 2. Hangfireへの具体的適合

既存の正式資料：`projects/Hangfire/PROJECT.md`、`CURRENT_SPEC.md`、`VISUAL_DIRECTION.md`、`GEAR_ANIMATION.md`、`GEAR_PERFORMANCE.md`、`tasks/BACKLOG.md`。

- HangfireのVisual Directionは**荒めの2D pixel art**、HD 1280×720を視覚目標とし、**10年前程度の一般的PCでも軽量**であることを優先。
- Gear animationはBODY/BARREL分離、Idle/Move/Fire/Hit等の少フレーム表現、**クライアント描画のみ**が原則。8 Gear同時表示を想定。Server authorityの発射角・命中・HP・地形データを表示エフェクトで変えない。
- プロジェクト索引によると**Layer 5完了・Human Playtest/Review待ち**で、Layer 6以降はHuman GOまで開始しない。正式なゲームルールは現行`CURRENT_SPEC.md`を優先。外部技術研究を理由にVisual実装を前倒ししない。

| ゲーム内の演出 | pixelfx探索候補（IDは上流Catalogに実在） | 注意 |
|---|---|---|
| 砲口炎／砲弾 | `projectiles/cannonball`、`projectiles/muzzle-pistol`、`projectiles/rocket` | 砲弾の実位置・弾道はServer結果を使用。見た目だけに利用 |
| 命中・直撃 | `impacts/bullet-impact`、`impacts/hit-spark`、`impacts/crit-hit` | Hit/Direct Hit判定やダメージ量を変えない |
| 爆発・地形への着弾 | `explosions/small-explosion`、`explosions/dirt-explosion`、`explosions/big-explosion` | 地形破壊マスク・当たり判定は現行ゲーム側が正本 |
| 火炎・損傷 | `fire/torch`などを参考に適切な短い炎・煙素材を探す | HPに応じた5段階の損傷表示と整合させ、行動可能な機体の移動機構を壊れたように見せない |
| 試合演出 | `ui/crit-number`、`ui/health-bar-hit`などを参考にする | 敵HPの正確な数値表示を許可せず、ゲームの情報公開ルールを維持 |

**推奨方式：** まず少数の効果を**透過PNGスプライトシートへ事前変換**し、現行Canvas 2D描画で再生する方式を比較する。pixelfxをゲームの本番ランタイムに常駐させるかどうかは、最小実験の計測後に決める。不要な新規JS依存やサーバ負荷を避ける。

## 3. 重複確認・他候補との差

- `development`ブランチのツリーと関連するHangfire資料を確認。**pixelfx自体の専用研究記録は見つからず、重複区分NEW**（リポジトリ内全テキストや未同期ローカル草稿までの完全検索ではない）。AirtableのHarness Inboxも`pixelfx`で検索し、該当なし。AirtableはGrok情報の受信場所のため、今回の評価を書き込まない。
- `projects/Hangfire/tasks/BACKLOG.md` に既存の**text APNG cut-in maker**候補あり。主に勝敗・ターン開始等の**文字演出**であり、pixelfxの**戦闘VFX**と補完的。
- `incubator/proposals/2026-10-25-motion-infographic-prompts-skills-research.md`は図解・動画向け。
- `incubator/proposals/2026-10-24-hermes-plugins-official-jev-voice-gameforge-botforge.md`のGameForgeは**ゲーム制作や自動プレイテスト全体**を扱う別技術。pixelfxとは役割が異なる。
- 最も単純な代替は、既存のCanvas 2D上で**独自の少フレームPNGと画面揺れ**だけを作る方法。pixelfxを使わなくても要件を満たすなら導入不要。

## 4. 費用・セキュリティ・利用条件

- **本体のソースコードはMIT**。商用利用可能な一般的なライセンスだが、著作権・許諾表示の保持が必要。`NOTICE.md`の由来を確認し、Patch Pixelフォントや別ライセンスの素材を混入させない。
- ソースの公開・MITはセキュリティ監査済みを意味しない。2026-10-30作成の新規OSSで保守継続性、各種動作環境との互換性、供給網リスクは未検証。
- ローカル利用なら専用クラウド登録やAPI課金は必須ではない。Patchサービスへの公開、CLIログイン、外部アカウント接続、リモートインストールスクリプト実行は**今回の用途では不要**。
- 不明なスキルや自動実行コマンドをCodex/Claudeに無条件導入しない。上流ソースとバージョンを固定・点検し、ローカルの隔離作業フォルダで必要最小限を検証。
- 既存ゲームの意匠や第三者のキャラクター/ブランドの直接複製を避け、Hangfireの独自視覚表現を維持。既存の`reference/CLEAN_ROOM/DO_NOT_COPY.md`を遵守。
- 8 Gear表示、古めのPC、CPU/メモリ、描画時間、アセットサイズ、視認性などの実測は未実施。軽量性は**可能性**であり確認済み性能ではない。

## 5. 最小の将来検証（現在は許可も実行もしていない）

1. Visual Layer着手をHumanが許可した後、隔離した作業コピーに上流の**固定コミット**を取り込んで`LICENSE`/`NOTICE`/依存を再確認する。
2. `small-explosion`、`dirt-explosion`、`hit-spark`等の2〜3種類に限定し、接触点・色・表示サイズを変え、コンタクトシートや透過PNGスプライトシートを生成する。
3. 既存Canvas描画の最小テストシーン上で、(A)手作り少フレーム素材、(B)pixelfx書き出し素材を比較。**8 Gear表示**、連続射撃・複数爆発、低スペックPC相当の環境でFPS/フレーム時間・CPU/メモリ・総アセット容量を測る。
4. 視認性・機体シルエット・敵HP非表示・Server authority・入力レスポンス・地形との前後関係・損傷5段階の整合性を確認する。
5. Humanが見た目を承認し、定量的に利益がある場合のみ、限定導入の別タスクを提案。失敗したら生成PNGを捨てて既存Canvas実装に戻せるようにする。

## 6. 評価と境界

- 情報種別：`FACT`（OSSの公開とドキュメント機能）＋ `IDEA`（Hangfireへの効果的な適用）。
- Stage 1：**A++**（Hangfireの具体的な未着手Visual Layerに強く一致）。
- Stage 2：**A+**（上流実装、形式、ライセンスの一次確認。ただし実機での有効性は未測定）。
- Evidence：**CONFIRMED**（GitHub上のソース、Catalog、Skill、ライセンス、API説明）／**UNVERIFIED**（Hangfireへの実際の組込み・速度・品質・独立監査）。
- Disposition：**CANDIDATE**。保存価値あり、導入HOLD、Visual Layer開始のHuman承認待ち。
- Recall triggers：`Hangfire`、`pixelfx`、`砲口炎`、`爆発`、`被弾`、`pixel VFX`、`sprite sheet`、`Canvas 2D`、`Visual Layer`。

**境界：** 本記録は`incubator/proposals/`に保存する研究資料であって、`projects/Hangfire/CURRENT_SPEC.md`、各種正式仕様、タスク・Backlog、実行コード、ゲーム資産への変更命令ではない。GitHub新規ファイル作成自体もHumanの対象・内容承認を経てから実施する。