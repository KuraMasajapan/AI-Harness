# Hangfire — Initial Spec Alignment Checkpoint

Date: 2026-09-27
Purpose: 開発途中で、最初に定義したHangfire仕様と現在の実装状況がずれていないか確認するための監査用Checkpoint。

この文書は新しい仕様を追加するものではない。
初期仕様・現在のProject状態・各Layerの完了状況を照合するための記録である。

---

## 1. Initial Product Goal

Hangfireは、最大8人のターン制砲撃対戦ゲームの核を試作する。

完成品ではなくPrototype。

既存作品の名前、機体、マップ、UI、数値、素材、コード、式を再現しない。

---

## 2. Initial Core Gameplay Specification

初期仕様の主要項目:

- 交互またはAction Costに基づく手番制砲撃
- AngleとPowerで着弾が変わる
- Windで軌道が変わる
- MOVEまたはATTACKでResourceを消費する
- 強いActionほど次の手番が遅れる
- HP 0でGearが脱落する
- 最後に生存する側で勝敗が決まる

現在の整合状態:

- [x] Angle / Powerによる弾道
- [x] Windによる軌道変化
- [x] Server-authoritative projectile
- [x] Resource消費
- [x] MOVE / FIRE
- [x] Action Cost
- [x] nextActionTimeによる手番選択
- [x] HP / Damage / Elimination / Winner
  - Layer 3のローカル完成状態で確認済み
  - GitHub developmentへの反映は未完了
- [ ] 強攻撃の種類ごとのAction Cost差
  - 後続Layerで具体化
- [ ] 本番用Balance
  - Human Playtest後に調整

---

## 3. Player Count / Room / Team

初期仕様:

- 最大8人
- 開始人数は2 / 4 / 6 / 8のみ
- 奇数では開始しない
- 開始後の途中参加なし
- Team戦のみ
  - 1v1
  - 2v2
  - 3v3
  - 4v4
- 入室順で自動Team分け
- Room code招待
- Rankingなし
- Auto matchmakingなし
- Spectatorなし
- NPCなし
- 開発時のみDummy可

現在:

- [x] 固定2 PlayerのPrototype
- [ ] Room
- [ ] 2 / 4 / 6 / 8 Player開始
- [ ] 奇数開始拒否
- [ ] Team assignment
- [ ] Room code
- [x] Ranking未実装
- [x] Matchmaking未実装
- [x] Spectator未実装
- [x] NPC未実装

判定:
現状はLayer順どおり。
Room / TeamはLayer 5まで未実装で問題なし。

---

## 4. Gear

初期仕様:

2種類のみ。

- 速機
  - 移動が安い
  - 火力は普通
- 重機
  - 移動が重い
  - 直撃が厚い

現在:

- [ ] 速機
- [ ] 重機
- [x] Gear collision方式は事前仕様化済み
  - Hit Point
  - Direct Hit Radius
  - VisualとCollisionを分離
- [x] Layer 3では共通Gear判定まで
- [ ] Gear差はLayer 6で実装予定

判定:
予定どおり。

---

## 5. Items

初期仕様:

各1回、使用任意。

- 偏流
  - 次の1発だけWindを強くする
- 残熱
  - 大技後の手番遅れを1回だけ軽減する

禁止:
- 3種類目
- Shop
- Heal
- Instant kill

現在:

- [ ] 偏流
- [ ] 残熱
- [x] 追加Item未実装
- [x] Shop未実装
- [x] Heal未実装
- [x] Instant kill未実装

判定:
Layer 6まで未実装で問題なし。

---

## 6. Online / Server Authority

初期仕様:

Clientは入力と表示のみ。

Clientから送信してよい入力:

- Angle
- Power
- MOVE
- Item使用

Serverが決定:

- Wind
- Projectile / Impact
- Damage
- Resource
- Turn
- Delay
- HP
- Elimination
- Winner

現在:

- [x] WindはServer State
- [x] ProjectileはServer authority
- [x] ImpactはServer authority
- [x] ResourceはServer authority
- [x] Turn / nextActionTimeはServer authority
- [x] Damage / HP / Elimination / WinnerはLayer 3ローカル完成状態でServer authority
- [x] Invalid input rejectionあり
- [x] stale revision rejectionあり
- [x] rejected actionでState不変
- [ ] Room単位の本番Match State
- [ ] Item入力

判定:
初期Server-authority方針を維持。

---

## 7. Turn Time Limit

初期仕様:

- 1手15秒

現在:

- [ ] 未実装

予定:
Layer 4「操作と15秒制限」。

判定:
未実装で正しい。

---

## 8. Publish

初期仕様:

- HTML5 client
- index.html + script
- itch.io page play
- Room serverは別host
- 説明:
  - 「招待制の偶数対戦。競技用ではない」
- ROBLOXなし
- Steamなし
- Dedicated launcherなし

現在:

- [x] Browser Client
- [x] HTML / JavaScript / Canvas 2D
- [x] Node.js軽量Server
- [ ] itch.io公開
- [ ] 外部Room server deploy
- [x] ROBLOX未実装
- [x] Steam未実装
- [x] Launcher未実装

判定:
Prototype途中として整合。

---

## 9. Performance / Cost

現行方針:

- 無料枠または極低コストServer
- 1 process優先
- 外部dependency最小
- 低CPU / 低Memory
- 10年前程度の一般的PCでも動きやすい構成
- 2D中心
- ServerでVisual処理しない
- 高解像度Game Stateを持たない

現在:

- [x] Node.js standard library中心
- [x] Canvas 2D
- [x] External dependencyなし
- [x] Event-driven
- [x] 不要なidle simulationなし
- [ ] 無料hosting実測
- [ ] 10年前PCでの実測

判定:
Architectureは方針一致。
実機・hosting検証は未実施として保持。

---

## 10. Destructible Terrain

初期意図:

地形破壊はHangfireの重要要素。

ただし高精細画像そのものをCollision Sourceにしない。

現在:

- [ ] 地形破壊
- [ ] Crater
- [ ] Terrain fallout
- [x] Collision / Rendering分離方針は仕様化済み
- [x] Layer 1 Projectile pathは将来のTerrain / Gear collisionへ接続可能

判定:
まだ未実装。
先回りしていないため問題なし。

---

## 11. Tuning

方針:

完成後にHuman PlaytestでBalance調整。

今はEditorを作らず、調整値だけ集中管理。

現在:

- [x] Layer 1 Tuning集中管理
- [x] Layer 2 Tuning集中管理
- [x] Layer 3 Tuning集中管理（ローカル完成状態）
- [x] Humanが「70%」「+100%」等の相対変更をしやすい構造
- [ ] Full Tuning Editor

判定:
予定どおり。
Full Editorは後回し。

---

## 12. Development Order

初期順序:

1. 弾道と風
2. ターンと資源、手番遅れ
3. 当たりと勝敗
4. 操作と15秒制限
5. 部屋（偶数開始、最大8、チーム）
6. 機体2とアイテム2
7. 見た目

現在:

- [x] Layer 1 completed / development merge済み
- [x] Layer 2 completed / development merge済み
- [x] Layer 3 implemented locally / 25 tests PASS / GitHub push pending
- [ ] Layer 4
- [ ] Layer 5
- [ ] Layer 6
- [ ] Layer 7

重要:
Layer 3はローカルcommit `0a70b0a` に保存済みだが、
GitHub接続障害のためdevelopment未反映。

Layer 4は未着手。

---

## 13. Prohibitions Audit

初期禁止事項:

- 頼まれていない機能追加
- Menu / Campaign / 複数Stage作り込み
- 大きなRefactor
- 既存作品の言及や再現をコード/表示へ残す
- 今のLayer以外を広く編集する

現在確認:

- [x] Layer単位で停止
- [x] 次Layer先回りなし
- [x] Menu未実装
- [x] Campaign未実装
- [x] 複数Stage未実装
- [x] 大規模Refactorなし
- [x] Clean-room境界を維持
- [x] Reference固有数値・式・UI・素材を採用していない

---

## 14. Current Known Gaps

現在の重要な未実装・未確定:

- Layer 3のGitHub push / Draft PR
- 15秒Turn Timer
- Room / Team / max 8 players
- Gear 2種
- Items 2種
- destructible terrain
- final visual
- itch.io deployment
- free-tier server実測
- old-PC実測
- final balance tuning

---

## 15. Current Risk

最大の現在リスクはGame Logicではなく、
Layer 3ローカル完成状態がGitHubへまだ反映されていないこと。

ローカル保全状態:

- Branch: `hangfire/layer-03-hit-win`
- Commit: `0a70b0a`
- Uncommitted changes: none
- Layer 3 tests: 25/25 PASS
- Local Checkpoint: exists
- Local PROJECT: LAYER_3_COMPLETED
- Layer 4: not started

GitHub接続回復後は、
再実装せずこのcommitをpushしてDraft PRを作る。

---

## 16. Overall Alignment Result

初期仕様との大きな逸脱は現時点で確認されていない。

現在は、

**Prototypeの核をLayer順に積み上げている途中**

であり、

- Core projectile
- Turn / Resource
- Hit / Damage / Victory

まで進行。

未実装項目の多くはLayer 4以降に意図的に残されている。

---

## 17. Resume Point

次の作業順:

1. GitHub接続回復確認
2. `0a70b0a` をpush
3. Layer 3 Draft PR作成
4. Layer 3 review / merge
5. 初期仕様との整合を再確認
6. Human GO後にLayer 4開始

Layer 3を再実装しない。
Layer 4を先回りしない。
