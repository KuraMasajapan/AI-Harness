# Hangfire Project

## 1. Purpose

Hangfireは、最大8人のターン制砲撃対戦ゲームの核を試作するプロジェクト。

このファイルは仕様書そのものではなく、

- 過去に何を決めたか
- 現在どこまで進んでいるか
- 次に何をするか
- どの資料を参照すべきか

を確認するためのProject Index / State Ledgerとして使う。

---

## 2. Project Identity

Project name: Hangfire

Status: READY_FOR_LAYER_1

Current phase:
- ASTRA実行ループ整備済み
- PRE-FLIGHT / OMISSION CHECK / CHECKPOINT運用準備済み
- Layer 1実装開始待ち

---

## 3. Source of Truth

Hangfireの仕様は、Project配下の正式な仕様・タスク資料を優先する。

この `PROJECT.md` は仕様の重複保存を目的としない。
仕様変更は、このファイルだけを書き換えて完了扱いにしない。

現時点の主な入口:

- `ASTRA_START.md`
- `README.md`
- `SERVER_ARCHITECTURE.md`
- `GEAR_COLLISION.md`
- `TUNING_POLICY.md`
- `tasks/LAYER_01_PROJECTILE_WIND.md`
- `CODEX_TASK_FORM.html`
- `reference/README.md`
- `reference/CLEAN_ROOM/HANGFIRE_MAPPING.md`
- `reference/CLEAN_ROOM/DO_NOT_COPY.md`

---

## 4. Current State

### Project setup
- Project name fixed as Hangfire
- `projects/Hangfire/` created
- Codex task form created
- Reference directory created
- Assault Gear research reference added
- Clean-room boundary documented
- Low-cost server architecture rule documented
- Gear collision rule documented
- Tuning seed policy documented

### Development
- Game implementation has not started yet
- No gameplay layer is marked complete
- CURRENT_LAYER is Layer 1「弾道と風」
- Layer 1専用Taskを作成済み

### Current objective
Codexによる実装開始前に、
- 指示形式
- Source of Truth
- Reference boundary
- Current-state tracking

を明確にする。

---

## 5. Development Order

1. 弾道と風
2. ターンと資源、手番遅れ
3. 当たりと勝敗
4. 操作と15秒制限
5. 部屋（偶数開始、最大8、チーム）
6. 機体2とアイテム2
7. 見た目は最後

一度に1層だけ進める。

---

## 6. History

### 2026-09-27 — Project structure
- Hangfireをゲーム開発プロジェクト名として採用
- `projects/Hangfire/` を作業場所として使用開始

### 2026-09-27 — Codex task form
- `CODEX_TASK_FORM.html` を追加
- CURRENT_LAYER / TARGET / ALLOWED_FILES / DO_NOT_TOUCH / ACCEPTANCE / STATUS を入力可能
- Codex向けMarkdown生成・コピー・保存に対応

### 2026-09-27 — Reference pack
- Assault Gearの公開資料を研究対象として整理
- 元コードやゲーム資産を直接持ち込まないClean-room方針を採用
- `reference/` 以下に索引と抽象化資料を追加

### 2026-09-27 — Execution loop dry-run
- GitHub上のHangfire実行ループを文書ベースで通し確認
- OMISSION CHECKがCheckpoint / PROJECT更新を先に要求する循環不整合を検出
- OMISSION CHECKを実装内容・漏れ検出に限定
- Checkpoint / PROJECT更新後にFINAL CLOSE CHECKを追加
- Source of Truth入口一覧を現行ファイル構成へ更新
- Layer 1の必読資料にGear collision / Tuning policyを明示

### 2026-09-27 — Tuning seed policy
- `TUNING_POLICY.md` を追加
- Gameplay / Balance値を最初から集中管理する方針を固定
- 本格的なTuning UI / Editorは主要Layer完成後まで作らない
- 各Layerで必要な調整値だけ追加する
- Human Playtestから相対変更を反映しやすい構造を採用

### 2026-09-27 — Gear collision rule
- `GEAR_COLLISION.md` を追加
- Gearの見た目と被弾判定を分離
- Hit Point + small Direct Hit Radiusを正式採用
- ExplosionはExplosion CenterからhitPointまでの距離で判定
- Collision / DamageはServer authority
- Layer 3で実装、Layer 6でGear別調整
- DEV modeでHit Point / Radius可視化を行う方針を固定

### 2026-09-27 — Layer 1 task
- `tasks/LAYER_01_PROJECTILE_WIND.md` を追加
- 弾道・風・Server authorityのAcceptance Criteriaを定義
- Layer 2以降を先回りしない範囲を明示
- Layer 1完了時のCheckpoint / PROJECT更新条件を定義

### 2026-09-27 — Low-cost server architecture
- `SERVER_ARCHITECTURE.md` を追加
- 無料枠または極低コストの小規模Serverを優先
- Serverはauthoritative game stateに限定し、Visual処理はClientへ分離
- 不要なDB / Redis / Queue / Microservice等を初期導入しない方針を追加
- 1 processで複数Roomを扱える単純構成を優先

### 2026-09-27 — ASTRA execution loop
- `ASTRA_START.md` を追加
- PRE-FLIGHT CHECKを追加
- OMISSION CHECKを追加
- Layer終了時Checkpoint保存を追加
- 状態更新はASTRAが自動実行可能とし、仕様変更はHuman Authorityに保持
- `checkpoints/CHECKPOINT_TEMPLATE.md` を追加

---

## 7. Current Work Snapshot

CURRENT_LAYER: 1. 弾道と風

Completed layers:
- なし

Working:
- ASTRAによるLayer 1開始待ち

Known issues:
- 実装技術スタックの詳細はまだ固定していない
- Server runtime / hosting providerは未選定だが、無料枠または極低コスト前提
- 実ゲームコードはまだ存在しない
- Layer 1の最低AcceptanceはASTRA_START.mdに定義済みだが、repository確認後に具体化する

Next action:
- ASTRA_START.mdから開始する
- PRE-FLIGHT CHECKを実行する
- repository状態を確認する
- `/projects/Hangfire/tasks/LAYER_01_PROJECTILE_WIND.md` を読む
- Layer 1「弾道と風」のPlanを作る
- Acceptance Criteriaをrepository状態に合わせて具体化し、Layer 1だけ実装する

---

## 8. Reference Usage

通常のCodex作業では、必要な情報だけ読む。

### Primary
- `CODEX_TASK_FORM.html`
- 今回生成したTask
- この `PROJECT.md`

### When game-mechanic reference is needed
- `reference/CLEAN_ROOM/HANGFIRE_MAPPING.md`

### When source provenance is needed
- `reference/SOURCE_INDEX.md`

### When boundary checking is needed
- `reference/CLEAN_ROOM/DO_NOT_COPY.md`

Reference資料をHangfire仕様より優先しない。

---

## 9. Update Rule

意味のある作業区切りごとに、このファイルの以下だけを更新する。

- Status
- Current phase
- Current State
- History
- Current Work Snapshot
- Next action

長い会話ログや詳細な実装記録をここへ貼り付けない。

重要な仕様・設計判断は、それぞれ正式なSource of Truthへ保存する。

---

## 10. Recovery Rule

作業再開時に現在位置が分からない場合は、まずこのファイルを読む。

確認順:

1. `PROJECT.md`
2. 現在のTask
3. 必要なSource of Truth
4. 必要なreferenceのみ

会話Memoryだけを現在状態の根拠にしない。
