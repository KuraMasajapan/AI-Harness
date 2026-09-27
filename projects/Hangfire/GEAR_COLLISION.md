# Hangfire — Gear Collision Rule

## Purpose

Hangfireの機体（Gear）への当たり判定は、見た目のスプライトやポリゴン形状そのものでは決めない。

ゲーム上の被弾判定は、各Gearが持つ独立した `Hit Point` を基準にする。

この方式は、描画品質・機体デザイン・解像度とゲームバランスを分離するための正式ルールである。

---

## 1. Core Rule

各Gearは最低限、次の3つの基準を分離して持つ。

- `visualOrigin`
  - 描画上の基準位置
- `hitPoint`
  - 被弾・爆風計算の基準位置
- `groundContactPoint`
  - 地形への接地基準位置

3つは同一位置である必要はない。

---

## 2. Hit Point

`hitPoint` はGear内部に設定する代表点。

通常は機体の重心付近、またはプレイヤーが自然に「中心」と感じる位置を基準にする。

見た目の外形そのものを当たり判定には使用しない。

---

## 3. Direct Hit

直撃判定は完全な1 pixel / 1 point一致ではなく、

**Hit Pointを中心とした小さなDirect Hit Radius**

を使用する。

概念:

```text
        Gear visual
      █████████
         (●)
          ↑
       hitPoint
     + small radius
```

Projectileの移動線分がこの小円に交差した場合、Direct Hitとする。

これにより高速Projectileのすり抜けを防ぐ。

---

## 4. Explosion / Splash Damage

爆風判定は、

**Explosion CenterからGearのhitPointまでの距離**

を基準にする。

```text
Explosion Center ● -------- distance -------- ● hitPoint
```

Blast Radius外ならDamage 0。

Blast Radius内では距離に応じてDamageを減衰させてよい。

具体的なDamage値、Falloff curve、Blast RadiusはTuning対象とし、現時点では固定しない。

---

## 5. Terrain Collision Priority

ProjectileがGearとTerrainの両方に接触し得る場合、

**Projectileの移動経路上で最初に発生した衝突を採用する。**

Gearへ先に接触:
- Direct Hit

Terrainへ先に接触:
- Terrain Impact
- その位置をExplosion CenterとしてSplash Damage判定

---

## 6. Server Authority

以下はすべてServerが決定する。

- Projectile collision
- Direct Hit
- Terrain Impact
- Explosion Center
- Distance to hitPoint
- Damage result

Clientは表示だけを行う。

ClientがHit判定やDamage結果を決定してServerへ送信してはいけない。

---

## 7. Visual Independence

Gearの見た目を変更しても、

`hitPoint` と `Direct Hit Radius` を変更しない限り、
ゲーム上の当たりやすさは変化しない。

以下を分離する。

```text
Visual Size
≠
Hit Point
≠
Direct Hit Radius
```

高解像度化やSprite差し替えだけでBalanceが変わらない構造にする。

---

## 8. Gear Differences

Layer 3までは共通Hit Point設定を使用してよい。

Layer 6でScout / Heavyの外観とBalanceを調整するときに、
各Gearごとに以下を独立設定できる構造にする。

- Hit Point X offset
- Hit Point Y offset
- Direct Hit Radius

ただし、機体の見た目とHit Pointが不自然に離れすぎないこと。

---

## 9. DEV Tuning

開発時には以下を表示できるようにする。

- Hit Point
- Direct Hit Radius
- Projectile collision point
- Explosion Center
- Blast Radius
- groundContactPoint

DEV表示は本番表示とは分離する。

例:

```text
[DEV COLLISION]

Hit Point X
Hit Point Y
Direct Hit Radius
Blast Radius

[Show Hit Point]
[Show Direct Hit Radius]
[Show Blast Radius]
```

具体値はHuman Playtestで調整可能にする。

---

## 10. Tuning Principle

Collision関連の数値を実装コードへ散在させない。

最低限、以下は集中管理する。

- HIT_POINT_X
- HIT_POINT_Y
- DIRECT_HIT_RADIUS
- BLAST_RADIUS
- DAMAGE_FALLOFF

HumanはPlaytest後に、

- 「Hit Pointを6px下げる」
- 「Direct Hit Radiusを85%にする」
- 「Blast Radiusを20%広げる」

のような相対変更を指示できる。

---

## 11. Performance

Collision計算は低コストを優先する。

使用してよい基本計算:

- point / circle distance
- line segment vs circle
- simple terrain collision

Pixel-perfect collisionや高解像度画像ベースのGear collisionは使用しない。

---

## 12. Layer Assignment

このルールは今からSource of Truthとして固定する。

実装時期:

- Layer 1:
  - Projectile pathが将来のline-segment collisionへ接続できる構造を維持
  - Gear collision自体はまだ実装しない

- Layer 3:
  - Hit Point
  - Direct Hit Radius
  - Direct Hit
  - Explosion distance
  - Damage result
  を実装する

- Layer 6:
  - GearごとのHit Point / Radius tuningを必要に応じて行う

---

## 13. Prohibited

使用しない:

- Sprite alpha / pixel-perfect collision
- 描画画像そのものをServer collision sourceにする方式
- Client-authoritative collision
- Reference作品の正確なHit Point位置や数値のコピー
- 見た目変更に追従して自動的にHitboxを変える方式

---

## 14. Acceptance for Layer 3

Layer 3では最低限、

- GearがhitPointを持つ
- Direct Hit Radiusが設定される
- Projectile segment vs Direct Hit RadiusがServerで判定される
- Explosion CenterからhitPointまでの距離をServerで計算する
- Blast Radius外ではDamage 0
- Client表示変更でHit結果が変化しない
- DEV modeでHit PointとRadiusを可視化できる
- Collision tuning valuesが集中管理されている

ことを確認する。
