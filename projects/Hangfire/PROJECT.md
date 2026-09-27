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

Status: LAYER_5_COMPLETED

Current phase:
- Layer 1をPR #2でdevelopmentへmerge済み
- Layer 5実装・Acceptance・Layer 1〜4回帰・Validation完了（47/47 tests PASS）
- Checkpoint保存済み、Human Playtest / Review待ち
- Layer 6はHuman GOまで開始しない

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
- `TURN_LOAD_MODEL.md`
- `tasks/LAYER_01_PROJECTILE_WIND.md`
- `tasks/LAYER_04_INPUT_TIMER.md`
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
- Visual direction adopted
- Gear animation specification adopted
- Team HP visibility: own + allies visible; enemy exact HP hidden
- Stage spawn: mixed random spawn; teams are not separated left/right
- Stage E numeric baseline prepared for later implementation

### Development
- Layer 1「弾道と風」Completed、PR #2 merge済み（development 4d03e06）
- Layer 2「ターンと資源、手番遅れ」Completed
- Layer 3「当たりと勝敗」Completed
- Layer 4「操作と20秒制限」Completed
- CURRENT_LAYER is Layer 5 (completed; stopped)
- Node.js標準HTTP + Canvas 2Dの既存構成を維持
- Serverがwind / projectile / currentPlayer / logicalTime / players / Resource / Action Costを保持
- 固定2人、FIRE/MOVE、nextActionTime最小選択・ID順Tie-break
- Clientは行動入力と表示のみ。MOVE後のServer位置から既存弾道で発射
- Gameplay値はserver/tuning.jsに集中。採用仕様によりPower0..100/Aim0..180、外部dependencyなし
- ServerがhitPoint / directHitRadius / explosion / damage / HP / elimination / winnerを決定
- Clientは入力と表示のみ。DEV overlayでServer-owned collision anchorsを可視化
- Server時計が20秒期限、5秒充電、連続move/aim、飛翔/着弾effect待ちを管理
- Layer 2コスト互換を維持。4要素Turn Load、Gear効率差は未実装
- Serverがguest session / Player ID、Lobby / Room / Team / Battle metadataとCommunication routingを保持
- Layer 5「Lobby / Room / Team / Communication」Completed
- Layer 6以降は未実装

### Current objective
Layer 5をHumanがPlaytest / Reviewする。Layer 6準備は明示GO後。
Current Task: tasks/LAYER_05_LOBBY_ROOM_TEAM_CHAT.md。起動・操作はREADME.md、Evidenceはcheckpoints/LAYER_05_2026-09-28.md。

---

## 5. Development Order

1. 弾道と風
2. ターンと資源、手番遅れ
3. 当たりと勝敗
4. 操作と20秒制限
5. 部屋（偶数開始、最大8、チーム）
6. 機体2とアイテム2
7. 見た目は最後

一度に1層だけ進める。

---

## 6. History

### 2026-09-28 — Layer 5 completed
- Human確認済みのguest login、host移譲、入室順Team、Battle退出／切断状態仕様で実装
- Lobby / Room / Team / Battle metadataと独立Communication routingを追加
- BATTLE_TEAMは相手Teamへ配信せず、Whisperは所在を問わずsender/targetだけへ配信
- syntax/build、Layer 1〜4回帰39件＋Layer 5テスト8件、Browser Lobby確認PASS
- Omission Check PASS、Checkpoint保存。Layer 6へ進まず停止
- 詳細: checkpoints/LAYER_05_2026-09-28.md

### 2026-09-27 — Layer 4 completed
- Human GOによりdevelopment 58999c9から開始。PRE-FLIGHT/PLAN/IMPLEMENT/BUILD/TEST/RUN完了
- Server authorityで20秒、Space充電例外、MAX自動発射、連続移動/Aim、着弾effect待ちを追加
- Syntax/build、39/39 tests、Browser操作確認PASS。Omission/Checkpoint/Final Close確認
- Layer 5へ進まず停止。詳細: checkpoints/LAYER_04_2026-09-27.md

### 2026-09-27 — Layer 2 completed
- Human指示によりPR #2をdevelopmentへmergeし、4d03e06から開始
- PRE-FLIGHT → PLAN → IMPLEMENT → BUILD/TEST/RUNを実施
- 固定2人のServer-authoritativeな手番・Resource・Action Cost・左右MOVEを追加
- syntax/build、Layer 1回帰7件＋Layer 2テスト8件、Browser runtime PASS
- Omission Check PASS、Checkpoint保存。Layer 3へ進まず停止
- 詳細: checkpoints/LAYER_02_2026-09-27.md

### 2026-09-27 — Layer 3 completed
- Layer 3 taskをCurrent Taskとして確認し、Server-authoritativeなHit Point / Damage / HP / Elimination / Winnerを追加
- syntax/build、Layer 1回帰7件＋Layer 2回帰8件＋Layer 3テスト10件、Browser runtime PASS
- Direct Hit、Splash、Miss、自爆、勝敗、終了後action拒否、payload改変耐性を確認
- Omission Check PASS、Checkpoint保存。Layer 4へ進まず停止
- 詳細: checkpoints/LAYER_03_2026-09-27.md

### 2026-09-27 — Layer 1 completed
- development 5d8f021から既存状態確認、PRE-FLIGHT → PLAN → IMPLEMENTを実施
- 標準HTTP / Canvas、独自の暫定弾道値、Server authorityを実装
- syntax / build / 7自動テスト / Browser操作によるruntime確認PASS
- 無風再現性、Angle / Power変更、左右風の着弾変化、入力検証を確認
- Omission Check PASS、Checkpoint保存。次Layerへ進まず停止
- 詳細: checkpoints/LAYER_01_2026-09-27.md

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

CURRENT_LAYER: 5. Lobby / Room / Team / Communication

Completed layers:
- Layer 1 — 弾道と風（development merge済み）
- Layer 2 — ターンと資源、手番遅れ
- Layer 3 — 当たりと勝敗
- Layer 4 — 操作と20秒制限
- Layer 5 — Lobby / Room / Team / Communication

Working:
- 実装作業停止。Human Playtest / Review待ち
- Branch: hangfire/layer-05-lobby-room-team-chat（development 23cf229基準）

Known issues:
- Layer 2のblocking issueなし
- Balance値はAI-selected / Provisional
- Hosting provider未選定、無料枠実測・10年前の実機性能は未検証
- Stateはmemoryのみ、再起動でPlayer状態と最新shotを初期化
- Resource回復/manual Skipは未実装。枯渇時も20秒timeoutで手番は進むが再起動まで回復しない
- 固定2人のhotseat選択は認証ではない。Room/Team/対戦運用なし
- Clientは100ms polling。latency compensation/切断復帰protocolは未実装
- 共通移動速度・world境界・effect時間・timeout costはAI-selected / Provisional
- 4要素Turn Load/回復式、terrain destruction、Gear差、Itemは未実装
- account DB、password、persistent profile、Battle reconnect、NPC takeover、Voice、moderation、friend/blockは未実装
- Browser短押し/drag確認済み。長押し時間境界は自動テストで検証、Human操作感確認は継続

Next action:
- README.mdの手順でHuman Playtest / Review
- 必要ならLayer 4範囲の修正・Tuningのみ行う
- Humanの明示GO後にLayer 6準備。自動開始しない

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

## 10. Visual Direction

正式なゲーム内Visual Direction:

- `VISUAL_DIRECTION.md`
- `GEAR_ANIMATION.md`
- `GEAR_PERFORMANCE.md`
- `STAGE_DESIGN.md`

荒めの2D pixel artを採用。
速機は明るい白〜青＋オレンジ系アクセント。
重機は黒〜濃いグレー＋赤系アクセント。
BODYとBARRELを分離し、砲身は入力角度に応じて回転する。
StageはBackground / Destructible Terrain / Collision Representationを分離する。

---

## 11. Spec Alignment Checkpoint

初期仕様との進捗照合:

- `checkpoints/SPEC_ALIGNMENT_2026-09-27.md`

このCheckpointは新しい仕様ではなく、
初期仕様と現在状態の監査・再確認用。

---

## 12. Recovery Rule

作業再開時に現在位置が分からない場合は、まずこのファイルを読む。

確認順:

1. `PROJECT.md`
2. 現在のTask
3. 必要なSource of Truth
4. 必要なreferenceのみ

会話Memoryだけを現在状態の根拠にしない。


## Stage E Design Summary

Current consolidated Stage E design checkpoint:

- `checkpoints/STAGE_E_DESIGN_SUMMARY_2026-09-27.md`


## Layer 4 Timing Decision

Human-approved Layer 4 rule:

- turn input limit: 20 seconds
- timeout normally forces turn end with no automatic shot
- if Space-key power charging started before timeout, that charge may continue past 20 seconds
- after timeout, only that active charge and its Space release remain valid
- shot / impact / landing-effect resolution completes before turn end

Source of Truth:

- `tasks/LAYER_04_INPUT_TIMER.md`


## Gear Performance Direction

- Scout move efficiency: 2.0x baseline
- Heavy move efficiency: 1.0x baseline
- Same cooling expenditure gives Scout approximately 2x Heavy movement distance
- Per-Gear cooling-capacity maxima remain to be tuned
- Implementation belongs to Layer 6; Layer 4 keeps the common control model

Source of Truth:

- `GEAR_PERFORMANCE.md`


## Turn Load / Cooling Recovery

Human-approved core rule:

- Next-turn order and Cooling recovery derive from one Turn Load Score
- Turn Load Score combines:
  - elapsed turn time
  - Cooling Resource consumed
  - selected Weapon load
  - Item additional load
- lower score -> earlier next turn
- lower score -> larger Cooling recovery
- immediate manual Skip -> earliest / highest-recovery class
- exact formulas and weights remain Tuning TBD

Source of Truth:

- `TURN_LOAD_MODEL.md`


## Turn Load Tuning Direction

- Start Turn Load playtesting with elapsed turn time weighted more heavily
- Treat all coefficients as provisional
- Rebalance from Human playtest evidence
- Keep Turn Load / Cooling recovery values centralized
- Design data so a later unified tuning tool can adjust the model without gameplay-code rewrites

Sources:
- `TURN_LOAD_MODEL.md`
- `TUNING_POLICY.md`


## Development parameter visibility

Human-approved rule:

- DEV / tuning mode shows all gameplay-relevant parameters and derived values
- normal player mode hides internal debug/tuning values
- Turn Load component values and resulting delay/recovery must be visible during playtest
- future gameplay systems should join the same centralized DEV/Tuning surface

Source:
- `TUNING_POLICY.md`
