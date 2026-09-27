# Hangfire — ASTRA_START

## Purpose

このファイルは、Codex ASTRAがHangfire開発を開始・再開するときの実行入口。

目的は、会話Memoryだけに依存せず、repository上の現在状態を読み、
各Layerを1つずつ実装・検証・記録して停止すること。

---

## 1. Read Order

開始時は次を順に読む。

### Harness
1. `/HARNESS.md`
2. `/core/RULES.md`
3. `/core/WORKFLOW.md`
4. `/core/ACCESS.md`

必要部分だけ読む。無関係な大量Contextは読み込まない。

### Hangfire
5. `/projects/Hangfire/PROJECT.md`
6. `/projects/Hangfire/README.md`
7. `/projects/Hangfire/SERVER_ARCHITECTURE.md`
8. `/projects/Hangfire/GEAR_COLLISION.md`
9. `/projects/Hangfire/TUNING_POLICY.md`
10. 現在TaskがあればそのTask
   - 初回は `/projects/Hangfire/tasks/LAYER_01_PROJECTILE_WIND.md`
11. 必要なら `/projects/Hangfire/reference/CLEAN_ROOM/HANGFIRE_MAPPING.md`
12. 境界確認が必要なら `/projects/Hangfire/reference/CLEAN_ROOM/DO_NOT_COPY.md`

---

## 2. Authority

優先順位:

1. System / Safety
2. Current explicit Human instruction
3. Hangfire current Source of Truth
4. Current Task / Acceptance Criteria
5. PROJECT.md
6. Clean-room reference
7. General assumptions

Reference資料をHangfire仕様より優先しない。

---

## 3. Automatic Write Boundary

ASTRAは以下をHumanへの逐次確認なしで更新してよい。

- Hangfire実装コード
- 現在LayerのTask
- テスト
- `PROJECT.md` の状態・履歴・次Action
- `checkpoints/` の実行記録
- Known Issues
- 起動・検証手順の軽微な更新

ただし、次は自動確定しない。

- ゲーム仕様の意味変更
- Layer順序変更
- Scope拡大
- Server authority変更
- 公開形態の変更
- 大幅な技術スタック変更
- 大きな新規dependency追加
- Clean-room境界変更
- 既存の禁止事項解除

必要なら提案として記録し、Human判断を待つ。

---

## 4. PRE-FLIGHT CHECK

コード変更前に必ず確認する。

- [ ] `PROJECT.md` を読んだ
- [ ] CURRENT_LAYERを確認した
- [ ] Completed layersを確認した
- [ ] 現在Task / Acceptance Criteriaを確認した
- [ ] 必要なSource of Truthだけ読んだ
- [ ] `SERVER_ARCHITECTURE.md` を確認した
- [ ] `GEAR_COLLISION.md` を確認した
- [ ] `TUNING_POLICY.md` を確認した
- [ ] 必要なreferenceだけ読んだ
- [ ] DO_NOT_TOUCHを確認した
- [ ] repositoryの現在コードを確認した
- [ ] 既存実装を無視した作り直しになっていない
- [ ] 今回の作業が1 Layerに限定されている

不足があれば実装前に補う。

---

## 5. Development Order

1. 弾道と風
2. ターンと資源、手番遅れ
3. 当たりと勝敗
4. 操作と20秒制限
5. 部屋（偶数開始、最大8、チーム）
6. 機体2とアイテム2
7. 見た目は最後

一度に1 Layerだけ。

次Layerを先回りしない。

---

## 6. Current Default Start

`PROJECT.md` がPRE-DEVELOPMENTかつCURRENT_LAYER未指定なら、
最初のLayerは:

`Layer 1 — 弾道と風`

とする。

Layer 1のGoal:

Angle・Power・WindによってProjectileの着弾位置が変化する最小Playgroundを作る。

---

## 7. Minimum Layer 1 Acceptance

最低条件:

1. ClientとServerを起動できる
2. angleを変更できる
3. powerを変更できる
4. 発射できる
5. 無風で再現可能な軌道になる
6. 右風で着弾点が右へ変化する
7. 左風で着弾点が左へ変化する
8. Projectile計算結果はServerが決定する
9. Client表示値の改変だけではServer結果を変更できない
10. Layer 1以外を作り込んでいない
11. Build / syntax errorがない
12. 実際に起動確認する

Balance値は完成条件ではない。

---

## 8. Implementation Loop

各Layerで次の順序を守る。

```text
READ CURRENT STATE
  ↓
PRE-FLIGHT CHECK
  ↓
PLAN
  ↓
IMPLEMENT
  ↓
BUILD / TEST / RUN
  ↓
ACCEPTANCE CHECK
  ↓
OMISSION CHECK
  ↓
FAIL → FIX → RECHECK
  ↓
PASS
  ↓
WRITE CHECKPOINT
  ↓
UPDATE PROJECT.md
  ↓
FINAL CLOSE CHECK
  ↓
STOP
```

順序を飛ばさない。

---

## 9. OMISSION CHECK

Layer終了前に必ず確認する。

- [ ] CURRENT_LAYERだけを実装した
- [ ] Acceptance Criteriaを全項目確認した
- [ ] 禁止機能を追加していない
- [ ] 次Layerを先回りしていない
- [ ] Server authorityを破っていない
- [ ] Reference固有要素をコピーしていない
- [ ] 未承認dependencyを追加していない
- [ ] Known Issueを隠していない
- [ ] Validation結果を記録した
- [ ] 次回保存すべきKnown Issue / 未実装項目を洗い出した
- [ ] 現時点の実装内容だけで次回再開に必要な情報を特定できる

1つでもFAILなら実装修正または記録整理を行い、PASSするまでCheckpoint作成へ進まない。

---

## 10. Checkpoint

各Layer終了時に、

`/projects/Hangfire/checkpoints/`

へCheckpointを保存する。

命名例:

`LAYER_01_YYYY-MM-DD.md`

Checkpointには最低限:

- Layer
- Goal
- Files changed
- Acceptance results
- Validation results
- Known issues
- Deliberately not implemented
- Dependencies added
- Commit / repository state if available
- Next action

を記録する。

Checkpointは詳細な会話ログではなく、再開に必要なEvidenceとして残す。

---

## 11. PROJECT.md Update

Layer終了時に `PROJECT.md` の以下を更新する。

- Status
- Current phase
- Current State
- History
- Current Work Snapshot
- Next action

完了したLayerを明示する。

未解決事項はKnown issuesへ残す。

仕様変更をPROJECT.mdだけで行わない。

---

## 12. FINAL CLOSE CHECK

Checkpoint保存とPROJECT.md更新の後に、最後の整合確認を行う。

- [ ] Checkpointが実際に保存されている
- [ ] PROJECT.mdが現在状態へ更新されている
- [ ] CheckpointとPROJECT.mdのLayer / Status / Next actionが矛盾していない
- [ ] Completed扱いにした項目はAcceptance / ValidationのEvidenceを持つ
- [ ] Known Issue / BLOCKED事項が消えていない
- [ ] 次回、repositoryだけで現在位置を復元できる

1つでもFAILならSTOPせず、記録を修正して再確認する。

---

## 13. Stop Condition

次をすべて満たしたら停止する。

- CURRENT_LAYERが動作する
- Acceptance Criteria PASS
- Validation完了
- OMISSION CHECK PASS
- Checkpoint保存済み
- PROJECT.md更新済み
- 既存完成Layerに明確な破損なし

その後、自主的に次Layerへ進まない。

次LayerはHumanのGOを待つ。

---

## 14. Resume Rule

新しいsession、長い中断、Context圧縮後は、
過去会話だけで続行しない。

再開時:

1. `PROJECT.md`
2. 最新Checkpoint
3. Current Task
4. 必要なSource of Truth
5. 必要なreference

の順で現在状態を再構成する。

---

## 15. Final Report

Layer終了時は簡潔に次を返す。

```text
変更:
起動:
検証:
漏れ確認:
停止:
PROJECT:
```

問題があれば追加で:

```text
問題:
```

とする。


## Current Layer Task Discovery

現在の `PROJECT.md` がLayer 3開始を示す場合は、
`/projects/Hangfire/tasks/LAYER_03_HIT_WIN.md`
をCurrent Taskとして読む。

Current LayerとTaskが一致しない場合は実装を開始せず、BLOCKEDとして報告する。

Layer 4開始時は、
`/projects/Hangfire/tasks/LAYER_04_INPUT_TIMER.md`
をCurrent Taskとして読む。

Layer 5開始時は、
`/projects/Hangfire/tasks/LAYER_05_LOBBY_ROOM_TEAM_CHAT.md`
をCurrent Taskとして読む。
