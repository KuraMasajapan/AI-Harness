Hangfireの試作開発を続行してください。

今回実装するのは **Layer 2「ターンと資源、手番遅れ」だけ** です。

まずGitHubの `development` ブランチを確認してください。

## 0. Layer 1確認

Layer 1「弾道と風」が `development` にmerge済みであり、`PROJECT.md` がLayer 1完了状態になっていることを確認してください。

未merge、未完了、または状態に矛盾がある場合は、Layer 2を開始せず `BLOCKED` として報告してください。

Layer 1の実装を作り直さないでください。

---

## 1. 必読資料

現在のrepositoryをSource of Truthとして、以下を読んでください。

- `/projects/Hangfire/ASTRA_START.md`
- `/projects/Hangfire/PROJECT.md`
- `/projects/Hangfire/README.md`
- `/projects/Hangfire/SERVER_ARCHITECTURE.md`
- `/projects/Hangfire/GEAR_COLLISION.md`
- `/projects/Hangfire/TUNING_POLICY.md`
- Layer 1の最新Checkpoint
- Layer 1の実装コード

必要な場合のみClean-room referenceを参照してください。

過去会話だけを根拠に実装しないでください。

---

# Layer 2 — Turn / Resource / Action Delay

## Goal

Layer 1のServer-authoritativeな弾道を維持したまま、

**「現在の手番」「Resource消費」「行動の重さによる次手番の遅れ」**

を成立させてください。

今回の目的は、最小構成で

`Action → Resource消費 → Action Cost → 次回行動順`

というゲームの核を実装することです。

---

## 2. Core Rule

手番・Resource・Action CostはすべてServer authorityとします。

Clientは、

- 行動要求
- 必要な入力

のみを送信します。

Clientが以下を決定してはいけません。

- 現在の手番
- Resource残量
- Resource消費量
- Action Cost
- 次の行動時刻
- 次のPlayer
- 行動順

---

## 3. Prototype Players

Layer 2ではRoom systemをまだ実装しません。

最小のテスト環境として、Server内に固定の2 Playerを持ってよいです。

例:

- Player A
- Player B

これはLayer 5のRoom / Team実装ではありません。

Network Room、招待コード、Team分けなどは今回作らないでください。

---

## 4. Turn Model

単純な固定交互ターンではなく、

**各Playerが `nextActionTime` を持つ方式**

を採用してください。

概念:

```text
行動
↓
Action Costを計算
↓
currentTime + Action Cost
↓
nextActionTime
↓
nextActionTimeが最も小さいPlayerが次の手番
```

Action Costが大きい行動ほど、次回の手番が遅くなります。

Assault Gear等の既存作品のTurn Rate式や数値を再現してはいけません。

Hangfire独自の単純な方式にしてください。

---

## 5. Layer 2 Actions

最低限、2種類の行動を用意してください。

### FIRE

Layer 1の発射処理を使用します。

- angle
- power
- fire request

を使用します。

FIREはResourceを消費します。

FIREにはAction Costがあります。

---

### MOVE

Layer 2では本格的な地形移動を作らなくてよいです。

最小限、

- left
- right
- movement amount

のような論理的な移動要求を扱える構造にしてください。

平地上のX位置変更だけで構いません。

MOVEもResourceを消費します。

MOVEにもAction Costがあります。

複雑な移動Physics、坂、落下、地形破壊は実装しないでください。

---

## 6. Resource

各PlayerはResourceを持ちます。

Resourceは、

- FIRE
- MOVE

で消費します。

具体値は暫定値で構いません。

ただし `TUNING_POLICY.md` に従って集中管理してください。

例:

- RESOURCE_MAX
- FIRE_RESOURCE_COST
- MOVE_RESOURCE_COST_PER_UNIT

必要なら名称は実装に合わせて変更して構いません。

同じ値を複数箇所へ散らさないでください。

---

## 7. Resource不足

必要Resourceがない場合、そのActionをServer側で拒否してください。

Client表示だけで制限しないでください。

拒否時にGame Stateを変更してはいけません。

---

## 8. Action Cost

Action Costも集中管理してください。

最低限、

- FIRE_ACTION_COST
- MOVE_ACTION_COST

またはそれに相当する値を持ちます。

Layer 2では複雑な式は不要です。

ただし、

**FIREとMOVEで次回手番への影響が異なることを確認できる**

構造にしてください。

将来、強力な攻撃ほどAction Costを増やせる余地を残してください。

今回は武器種類や大技そのものは実装しません。

---

## 9. Turn Selection

ServerはAction終了後に、

- 各PlayerのnextActionTime
- elimination状態（将来用。今回は未実装）
- 現在状態

を基準に次Playerを決定できる構造にしてください。

Layer 2ではPlayerは2人固定で構いません。

同値になった場合のTie-breakルールは単純で決定論的にしてください。

Tie-breakルールを明示してください。

---

## 10. Initial State

最低限、Playerごとに以下を持たせてください。

```text
id
position
resource
nextActionTime
```

Server側Game Stateに、

```text
currentPlayer
logicalTime
players
```

または同等の情報を持たせてください。

必要最低限にしてください。

---

## 11. Layer 1 Preservation

Layer 1で完成した以下を壊してはいけません。

- angle
- power
- wind
- Server authoritative projectile
- deterministic projectile
- Client display
- centralized tuning
- no external dependency
- lightweight Canvas 2D

FIRE処理はLayer 1の弾道処理を再利用してください。

弾道式を理由なく書き直さないでください。

---

## 12. Tuning Seed

Layer 2で必要になったBalance値だけ追加します。

例:

```text
RESOURCE_MAX
FIRE_RESOURCE_COST
MOVE_RESOURCE_COST
FIRE_ACTION_COST
MOVE_ACTION_COST
MOVE_MAX_DISTANCE
```

正式値ではなく暫定値としてよいです。

Human Playtest後に、

- 「移動コストを現在の70%に」
- 「射撃後の手番遅延を30%増やす」

などの変更を一箇所で行える構造にしてください。

本格的なTuning Editorは作らないでください。

---

## 13. UI

UIは試作用の最低限で構いません。

表示対象:

- Current Player
- 各PlayerのResource
- 各PlayerのnextActionTime
- Angle
- Power
- Wind
- FIRE
- MOVE Left / Right

見た目の作り込みは不要です。

Developer向けに状態が読めることを優先してください。

---

## 14. Do Not Implement

今回実装しないもの:

- HP
- Damage
- Direct Hit
- Blast Damage
- Gear Hit Point
- destructible terrain
- terrain fallout
- 15秒Turn Timer
- Room code
- Online lobby
- Team assignment
- 4〜8 Player Room
- Gear differences
- Items
- 偏流
- 残熱
- Ranking
- Matchmaking
- Account
- Database
- Replay system
- Full tuning editor
- Final graphics
- Sound
- Music

Layer 3以降を先回りしないでください。

---

## 15. Performance / Architecture

引き続き、

- 無料枠または極低コストServer
- 1 process
- 低CPU
- 低Memory
- 外部dependency最小
- event-driven
- 不要な常時loopなし

を優先してください。

Turn処理のためだけに常時高頻度Timerを動かさないでください。

`nextActionTime` は論理値として扱って構いません。

---

## 16. Minimum Acceptance Criteria

### Existing Layer

- [x] Layer 1 tests remain PASS
- [x] Angle / Power / Wind projectile behavior remains functional
- [x] Server authority remains intact

### Turn

- [x] ServerがCurrent Playerを決定する
- [x] Current Player以外のActionを拒否する
- [x] Action後にnextActionTimeが更新される
- [x] nextActionTimeに基づき次Playerが決定される
- [x] Tie-breakが決定論的である

### Resource

- [x] 各PlayerがResourceを持つ
- [x] FIREでResourceが減る
- [x] MOVEでResourceが減る
- [x] Resource不足のActionはServerが拒否する
- [x] 拒否されたActionではGame Stateが変化しない

### Action Cost

- [x] FIREにAction Costがある
- [x] MOVEにAction Costがある
- [x] 異なるAction Costで次回の行動順に差が出ることを確認できる

### Movement

- [x] MOVE Left / RightがServer Stateのpositionを変更する
- [x] 移動量をServerが検証する
- [x] Clientがposition結果を直接決定しない

### Tuning

- [x] Layer 2 Balance値が集中管理されている
- [x] Layer 1 Tuning値を不必要に変更していない

### Scope

- [x] Layer 3以降を実装していない
- [x] HP / Damageを実装していない
- [x] Room / Teamを実装していない
- [x] Itemを実装していない
- [x] 不要なdependencyを追加していない

### Quality

- [x] syntax PASS
- [x] build PASS
- [x] Layer 1 regression tests PASS
- [x] Layer 2 relevant tests PASS
- [x] Browser runtime確認 PASS

---

## 17. Suggested Tests

最低限、可能なら自動確認してください。

1. Current PlayerだけAction可能
2. FIRE後にResourceが正しく減る
3. MOVE後にResourceが正しく減る
4. Resource不足ではAction拒否
5. Reject時にState不変
6. FIREとMOVEでAction Cost差が反映される
7. nextActionTime最小Playerが次Playerになる
8. Tie-breakが毎回同じ結果になる
9. Clientからresource / nextActionTime / currentPlayerを送っても拒否
10. Layer 1 projectile testsが引き続きPASS

過剰なTest frameworkは追加しないでください。

---

## 18. Execution Loop

必ず、

READ CURRENT STATE
→ PRE-FLIGHT CHECK
→ PLAN
→ IMPLEMENT
→ BUILD / TEST / RUN
→ ACCEPTANCE CHECK
→ OMISSION CHECK
→ 必要なら修正・再確認
→ WRITE CHECKPOINT
→ UPDATE PROJECT.md
→ FINAL CLOSE CHECK
→ STOP

の順で進めてください。

---

## 19. Checkpoint

成功時は、

`/projects/Hangfire/checkpoints/LAYER_02_<date>.md`

を作成してください。

最低限、

- Goal
- Files changed
- Acceptance results
- Layer 1 regression results
- Validation results
- Omission Check
- Known issues
- Deliberately not implemented
- Dependencies
- Next action

を残してください。

---

## 20. PROJECT Update

成功した場合のみLayer 2をCompletedへ追加してください。

次ActionはLayer 3準備としますが、Layer 3を開始してはいけません。

失敗・Blockedの場合はCompleted扱いにせず、再開地点を記録してください。

---

## 21. Stop Condition

以下が揃ったら停止してください。

- Layer 1 regression PASS
- Layer 2 Acceptance PASS
- Validation PASS
- Omission Check PASS
- Checkpoint保存済み
- PROJECT.md更新済み
- Final Close Check PASS

**Layer 3へ進まないでください。**

Humanの明示GOを待ってください。

---

## Final Report

最後は以下だけ簡潔に報告してください。

変更:
起動:
検証:
漏れ確認:
停止:
PROJECT:

問題がある場合のみ、

問題:

を追加してください。

## Execution result — 2026-09-27

Layer 2 completed. Evidence: ../checkpoints/LAYER_02_2026-09-27.md.
Layer 1 regression PASS; Layer 3 not started. Human GO required.
