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

Status: PRE-DEVELOPMENT

Current phase:
- 開発環境と指示形式の整備
- 参考資料の整理
- Codex実装開始前

---

## 3. Source of Truth

Hangfireの仕様は、Project配下の正式な仕様・タスク資料を優先する。

この `PROJECT.md` は仕様の重複保存を目的としない。
仕様変更は、このファイルだけを書き換えて完了扱いにしない。

現時点の主な入口:

- `README.md`
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

### Development
- Game implementation has not started yet
- No gameplay layer is marked complete
- CURRENT_LAYER is not yet fixed for implementation

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

---

## 7. Current Work Snapshot

CURRENT_LAYER: 未指定

Completed layers:
- なし

Working:
- Codex開発開始前の準備

Known issues:
- 実装技術スタックの詳細はまだ固定していない
- 最初のAcceptance Criteriaは未設定
- 実ゲームコードはまだ存在しない

Next action:
- Layer 1「弾道と風」の実装タスクを定義する
- Acceptance Criteriaを設定する
- CodexへPlanを出させる

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
