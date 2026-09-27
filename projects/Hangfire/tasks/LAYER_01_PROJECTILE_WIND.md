# Hangfire — Layer 01 Task

## Layer

Layer 1 — Projectile & Wind

CURRENT_LAYER: 1. 弾道と風

---

## Goal

Angle・Power・WindによってProjectileの着弾位置が変化する、
最小のオンライン対応Playgroundを作る。

このLayerの目的は、

**弾道計算と風の影響をServer authorityで成立させること。**

見た目の完成度やゲーム全体の完成は目的ではない。

---

## Read Before Work

必ず先に読む。

1. `/projects/Hangfire/ASTRA_START.md`
2. `/projects/Hangfire/PROJECT.md`
3. `/projects/Hangfire/SERVER_ARCHITECTURE.md`
4. `/projects/Hangfire/GEAR_COLLISION.md`
5. `/projects/Hangfire/TUNING_POLICY.md`
6. `/projects/Hangfire/reference/CLEAN_ROOM/HANGFIRE_MAPPING.md`
7. 必要なら `/projects/Hangfire/reference/CLEAN_ROOM/DO_NOT_COPY.md`

---

## Repository Check

実装前に確認する。

- 既存のClient codeがあるか
- 既存のServer codeがあるか
- package manager / build systemがあるか
- test環境があるか
- 既存技術スタックがあるか

既存実装がある場合は、それを無視して作り直さない。

何もない場合は、無料枠・低コスト・低依存の方針に合う最小構成を選ぶ。

---

## Target Behavior

最低限、以下を実現する。

### Client

- angleを変更できる
- powerを変更できる
- fire操作ができる
- windの方向と強さを表示できる
- projectile軌道を表示できる
- 着弾位置を表示できる

UIは仮でよい。

図形、線、文字だけでよい。

---

### Server

Serverは以下の正本を持つ。

- wind
- projectile initial state
- authoritative projectile calculation
- impact result

Clientが送信してよいのは、

- angle
- power
- fire request

のみ。

Clientが、

- 着弾位置
- damage
- projectile result

を決定してServerへ送ってはいけない。

---

## Projectile Model

Projectile計算は、

- simple
- deterministic
- low-cost
- understandable

を優先する。

最低限の入力:

- angle
- power
- gravity
- wind
- initial position

必要に応じて、

- velocity
- time step

を内部値として持ってよい。

元ゲームの式や係数を再現しない。

Hangfire独自の単純な値を使用する。

---

## Wind

最低限、

- zero wind
- wind to right
- wind to left

を確認できるようにする。

WindはServer State。

Client表示はServer Stateを反映する。

Layer 1では複雑な乱数モデルは不要。

---

## Terrain

Layer 1では地形破壊を実装しない。

最低限、

- flat ground
- projectile hit position

が確認できればよい。

ただし将来の地形破壊に備え、

**rendering surfaceとcollision representationを強く結合しない。**

高解像度画像を直接Game Stateの正本にしない。

---

## Tuning Seed

Layer 1では本格的なTuning UIを作らない。

ただし、以下のようなGameplay値は集中管理する。

- WIND_MAX
- WIND_MIN
- GRAVITY
- POWER_MIN
- POWER_MAX
- PROJECTILE_SPEED_SCALE

同じ意味の値を実装コード中へ散在させない。

Human Playtest後に、
「最大風力を現在の70%にする」のような相対変更を容易に反映できる構造にする。

必要ならDEV-onlyでWind vectorや現在値を表示してよい。

詳細は `/projects/Hangfire/TUNING_POLICY.md` を参照する。

---

## Performance

このLayerでも低負荷を優先する。

目標:

- high-end GPU不要
- 2D
- heavy shader不要
- heavy physics engine不要
- Serverで描画しない
- 不要な高頻度loopを回さない

Projectileが1発だけ飛ぶ最小構成でよい。

---

## Allowed Scope

実装に必要な範囲だけ変更する。

想定される対象:

- Client entry files
- Server entry files
- projectile calculation module
- wind state module
- minimal configuration
- Layer 1 test
- Layer 1 run instructions

既存repository構造に合わせて実際のpathは決める。

---

## Do Not Touch / Do Not Build

今回実装しない。

- HP
- damage system
- hit points
- team
- room code
- multiplayer room management
- turn order
- action cost
- resource
- turn delay
- items
- Gear differences
- 15-second timer
- destructible terrain
- terrain fallout
- ranking
- matchmaking
- account
- database
- replay system
- elaborate UI
- final art
- sound
- music

次Layerを先回りしない。

---

## Dependencies

新しいdependencyを追加する場合は先に記録する。

```text
DEPENDENCY:
REASON:
WHY_EXISTING_CODE_IS_NOT_ENOUGH:
SERVER_COST_IMPACT:
```

標準機能または既存dependencyで十分なら追加しない。

大きなframework導入は避ける。

---

## Acceptance Criteria

以下をすべて確認する。

### Startup

- [ ] Serverを起動できる
- [ ] Clientを起動できる
- [ ] BrowserでPlaygroundを表示できる

### Input

- [ ] angleを変更できる
- [ ] powerを変更できる
- [ ] fire requestをServerへ送れる

### Projectile

- [ ] 無風状態で同じ入力から同じ結果を得られる
- [ ] angle変更で着弾位置が変化する
- [ ] power変更で着弾位置が変化する
- [ ] 右風で無風時より着弾点が右方向へ変化する
- [ ] 左風で無風時より着弾点が左方向へ変化する

### Authority

- [ ] Windの正本がServerにある
- [ ] Projectile結果の正本がServerにある
- [ ] Clientは着弾結果を決定しない
- [ ] Client表示だけを改変してもServer結果は変更されない

### Scope

- [ ] Layer 2以降を実装していない
- [ ] 地形破壊を実装していない
- [ ] 不要なDB / Redis / Queueを追加していない
- [ ] 不要なVisual処理をServerへ追加していない

### Quality

- [ ] syntax / type check PASS
- [ ] build PASS
- [ ] relevant test PASS
- [ ] runtime確認 PASS

---

## Suggested Tests

実装方式に合わせて最小限でよい。

最低限、可能なら次を自動確認する。

1. Same input + same wind = same impact
2. Right wind shifts impact right
3. Left wind shifts impact left
4. More power changes range
5. Different angle changes trajectory
6. Invalid angle / power is rejected or clamped according to the chosen explicit rule

Test frameworkを大規模に導入しない。

---

## PRE-FLIGHT

実装開始前にASTRA_STARTのPRE-FLIGHT CHECKを実行する。

加えて確認する。

- [ ] Layer 1 Taskを読んだ
- [ ] Server architecture ruleを読んだ
- [ ] Gear collision ruleを読んだ
- [ ] Tuning policyを読んだ
- [ ] Clean-room mappingを読んだ
- [ ] repository existing stateを確認した
- [ ] 今回の技術選択が必要最小限である

---

## Omission Check

終了前にASTRA_STARTのOMISSION CHECKを実行する。

加えて確認する。

- [ ] WindのServer authorityを維持した
- [ ] ProjectileのServer authorityを維持した
- [ ] 次LayerのTurn systemを追加していない
- [ ] 地形破壊を追加していない
- [ ] Reference作品の固有数値・式・UIをコピーしていない
- [ ] Low-cost server方針を破っていない

---

## Checkpoint

完了時に、

`/projects/Hangfire/checkpoints/LAYER_01_<date>.md`

を作成する。

最低限記録:

- Goal
- Files changed
- Acceptance results
- Build/Test/Runtime results
- Omission Check
- Known issues
- Deliberately not implemented
- Dependencies added
- Next action

---

## PROJECT Update

完了時に `PROJECT.md` を更新する。

成功時:

- Layer 1をCompletedへ追加
- Current Stateを実装済みに更新
- HistoryへLayer 1結果を追加
- Next actionをLayer 2準備へ変更

失敗またはBlocked時:

- 未完了として残す
- Known issuesへ原因を記録
- 次回再開点を明示する

---

## Stop Condition

以下を満たしたら停止する。

- Acceptance Criteria PASS
- Validation PASS
- Omission Check PASS
- Checkpoint保存済み
- PROJECT.md更新済み
- FINAL CLOSE CHECK PASS

その後、Layer 2へ進まない。

HumanのGOを待つ。

---

## Final Report

```text
変更:
起動:
検証:
漏れ確認:
停止:
PROJECT:
```

問題があれば、

```text
問題:
```

を追加する。
