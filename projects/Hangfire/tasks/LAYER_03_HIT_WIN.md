# Hangfire — Layer 03 Task

## Layer

Layer 3 — Hit / Damage / Victory

CURRENT_LAYER: 3. 当たりと勝敗

---

## Goal

Layer 1・2を維持したまま、

**ProjectileがGearへ当たり、Damageが発生し、HP 0で脱落し、最後に残った側が勝つ**

最小の試作を完成させる。

今回の中心は、

- Hit Point
- Direct Hit Radius
- Explosion / Blast Damage
- HP
- Elimination
- Winner

である。

---

## Start Gate

実装開始前に必ず確認する。

- PR #3が `development` にmerge済み
- `PROJECT.md` がLayer 2 completed
- Layer 1 / Layer 2 testsがbaseline PASS
- 現在branchがLayer 3用である

未merge・矛盾・baseline failureがあればLayer 3を開始せずBLOCKEDとして停止する。

---

## Read Before Work

1. `/projects/Hangfire/ASTRA_START.md`
2. `/projects/Hangfire/PROJECT.md`
3. `/projects/Hangfire/README.md`
4. `/projects/Hangfire/SERVER_ARCHITECTURE.md`
5. `/projects/Hangfire/GEAR_COLLISION.md`
6. `/projects/Hangfire/TUNING_POLICY.md`
7. Layer 1 / Layer 2 latest checkpoints
8. Current Layer 1 / 2 implementation and tests

必要な場合のみClean-room referenceを読む。

---

## Existing State to Preserve

Layer 1:
- angle / power / wind
- deterministic Server-authoritative projectile
- lightweight Canvas 2D
- centralized projectile tuning

Layer 2:
- fixed two-player prototype
- currentPlayer
- resource
- action cost
- nextActionTime
- logicalTime
- FIRE / MOVE
- revision guard
- Server-authoritative state

これらを理由なく作り直さない。

---

## 1. Gear Collision Rule

`GEAR_COLLISION.md` を正式仕様として実装する。

各Gearは最低限、

- visualOrigin
- hitPoint
- groundContactPoint

を分離できる構造を持つ。

Layer 3では共通設定でよい。

---

## 2. Hit Point

各Player / GearはServer側に `hitPoint` を持つ。

最初は、

`player.position + hitPointOffset`

のような単純構造でよい。

Hit Pointは見た目の中心と一致する必要はない。

---

## 3. Direct Hit

完全な1点一致ではなく、

**Hit Pointを中心とした小さなDirect Hit Radius**

を使う。

Projectileの隣接path pointから得られる移動線分と、
Direct Hit circleの交差をServerで判定する。

ClientはDirect Hitを決定しない。

---

## 4. Terrain Impact

Layer 3ではまだ地形破壊を実装しない。

Terrainは引き続きflat groundでよい。

ProjectileがGearより先にgroundへ到達した場合、
そのground impact位置をExplosion Centerとする。

ProjectileがGearへ先に接触した場合、
そのcollision pointをExplosion Centerとしてよい。

最初に衝突したものを採用する。

---

## 5. Explosion / Splash Damage

Explosion Centerから各GearのhitPointまでの距離で判定する。

- Blast Radius外: Damage 0
- Blast Radius内: 距離に応じてDamage減衰
- Direct Hit: Direct Hitとして明確に区別できる

Falloffは単純で理解しやすい方式を採用する。

複雑な物理式は不要。

---

## 6. Damage

ServerがDamageを計算してHPへ適用する。

Clientから以下を受け取らない。

- damage
- hp
- directHit
- explosionCenter
- blastDistance
- winner
- eliminated

Damage値はTuning対象。

---

## 7. HP

各PlayerはServer-owned HPを持つ。

最低限:

- HP_MAX
- current HP

を持つ。

HPは0未満にならないようclampしてよい。

---

## 8. Elimination

HPが0になったPlayerはeliminatedとする。

eliminated Playerは以後Actionできない。

Turn selectionではeliminated Playerを除外する。

Layer 3ではGear落下・破壊animationは不要。

---

## 9. Winner

固定2 Player試作では、

- 相手がeliminated
- 自分が生存

ならwinnerをServerが決定する。

勝敗決定後はmatch stateをfinishedにし、
追加ActionをServer側で拒否する。

Team systemはまだ実装しない。

---

## 10. Self Damage

Explosionは発射Player自身にも届き得るものとして扱う。

自爆を特別免除しない。

ただし今回の最小試作では、
同一Explosionで複数PlayerへDamageが入る場合もServerが一括決定する。

---

## 11. Action / Turn Integration

FIREが成立した場合のみ、

- collision
- explosion
- damage
- elimination
- winner

を処理する。

その後、matchが継続中なら既存Action Cost / nextActionTime処理へ進む。

winner決定時は次Turnへ進めなくてよい。

MOVEは既存Layer 2動作を維持する。

---

## 12. Resource Integration

FIREのResource消費ルールはLayer 2を維持する。

Hit / Miss / Damage量によってResource costを変えない。

Resource不足のFIREは既存どおり拒否し、
collision / damage処理へ進まない。

---

## 13. Tuning Seed

Layer 3で必要な値だけ集中管理する。

例:

- HP_MAX
- HIT_POINT_X
- HIT_POINT_Y
- DIRECT_HIT_RADIUS
- BLAST_RADIUS
- DIRECT_HIT_DAMAGE
- BLAST_DAMAGE_MAX
- DAMAGE_FALLOFF

必要に応じて命名は変更してよい。

Human Playtestで、

- 「Direct Hit Radiusを85%に」
- 「爆風半径を20%広げる」
- 「破壊力を100%上げる」
- 「Hit Pointを6px下げる」

のような変更を一か所で行える構造にする。

本格Tuning Editorは作らない。

---

## 14. DEV Visualization

本格Debug UIは不要。

ただしLayer 3のHuman Playtestを容易にするため、
DEV-onlyで以下を可視化してよい。

- Hit Point
- Direct Hit Radius
- Explosion Center
- Blast Radius
- Collision point

簡単なtoggleまたは常時DEV表示でよい。

見た目の作り込みはしない。

---

## 15. UI

最低限表示:

- 各Player HP
- eliminated state
- currentPlayer
- Resource
- nextActionTime
- winner / match state
- Direct Hit / Splash / Miss の結果
- Damage量

既存Angle / Power / Wind / MOVE / FIRE UIを維持する。

---

## 16. Do Not Implement

今回実装しない:

- destructible terrain
- terrain crater
- terrain fallout
- 15-second timer
- Room code
- lobby
- Team assignment
- 4〜8 player room
- Scout / Heavy differences
- items
- 偏流
- 残熱
- ranking
- matchmaking
- account
- database
- replay
- full tuning editor
- final art
- sound
- music

Layer 4以降を先回りしない。

---

## 17. Performance

引き続き、

- Serverは計算のみ
- Clientは描画のみ
- no heavy physics engine
- no pixel-perfect collision
- line segment vs circle
- point distance
- event-driven
- no unnecessary idle loop
- no new dependency unless required

を維持する。

---

## 18. Minimum Acceptance Criteria

### Regression

- [ ] Layer 1 tests PASS
- [ ] Layer 2 tests PASS
- [ ] FIRE / MOVE / Resource / Turn behavior preserved

### Hit

- [ ] GearがServer-owned hitPointを持つ
- [ ] Direct Hit RadiusがServer tuningにある
- [ ] Projectile segment vs Direct Hit RadiusをServerで判定する
- [ ] ClientはHit結果を決定しない

### Explosion

- [ ] Explosion CenterをServerが決定する
- [ ] hitPointまでの距離をServerが計算する
- [ ] Blast Radius外ではDamage 0
- [ ] Blast Radius内ではDamageが入る
- [ ] Direct HitとSplashを区別できる
- [ ] Self Damageが可能

### HP / Elimination

- [ ] 各PlayerがServer-owned HPを持つ
- [ ] DamageでHPが減る
- [ ] HP 0でeliminatedになる
- [ ] eliminated PlayerはActionできない
- [ ] Turn selectionからeliminated Playerを除外する

### Victory

- [ ] 片方eliminatedでwinnerがServer決定される
- [ ] match finished後のActionをServerが拒否する
- [ ] Clientからwinner / HP等を注入できない

### State Safety

- [ ] invalid / rejected actionではHP等のStateが変化しない
- [ ] stale revision protectionを維持する
- [ ] collision / damage commitがatomicである

### Tuning

- [ ] Layer 3値が集中管理されている
- [ ] Layer 1 / 2 tuning値を理由なく変更していない

### Scope

- [ ] destructible terrain未実装
- [ ] Timer未実装
- [ ] Room / Team未実装
- [ ] Gear differences未実装
- [ ] Items未実装
- [ ] unnecessary dependencyなし

### Quality

- [ ] syntax PASS
- [ ] build PASS
- [ ] all regression tests PASS
- [ ] Layer 3 tests PASS
- [ ] Browser runtime PASS

---

## 19. Suggested Tests

最低限可能なら自動確認する。

1. Known trajectory crosses Direct Hit circle
2. Nearby ground impact causes Splash Damage
3. Outside Blast Radius gives zero Damage
4. Direct Hit is distinguishable from Splash
5. Self Damage works
6. Damage clamps HP at zero
7. HP zero marks eliminated
8. Eliminated Player action rejected
9. Eliminated Player excluded from next turn
10. Winner determined only by Server
11. Finished match rejects further actions
12. Client-supplied HP / Damage / winner / hit fields rejected
13. Rejected action leaves full State unchanged
14. Layer 1 / Layer 2 regressions remain PASS

過剰なTest frameworkは追加しない。

---

## 20. Execution Loop

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

---

## 21. Checkpoint

成功時:

`/projects/Hangfire/checkpoints/LAYER_03_<date>.md`

最低限:

- Goal
- Files changed
- Layer 1 regression
- Layer 2 regression
- Acceptance results
- Validation
- Omission Check
- Known issues
- Deliberately not implemented
- Dependencies
- Next action

を記録する。

---

## 22. PROJECT Update

成功時のみLayer 3をCompletedへ追加する。

Next actionはLayer 4準備。

Layer 4は開始しない。

失敗 / BLOCKEDならCompleted扱いにしない。

---

## 23. Stop Condition

以下すべてを満たしたらSTOP。

- Layer 1 regression PASS
- Layer 2 regression PASS
- Layer 3 Acceptance PASS
- Validation PASS
- Omission Check PASS
- Checkpoint保存済み
- PROJECT.md更新済み
- Final Close Check PASS

Layer 4へ進まない。

Human GOを待つ。

---

## Final Report

変更:
起動:
検証:
漏れ確認:
停止:
PROJECT:

問題がある場合のみ:

問題:
