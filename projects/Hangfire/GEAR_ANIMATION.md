# Hangfire — Gear Animation Specification

Status: ADOPTED
Date: 2026-09-27

## Purpose

HangfireのGearは、荒めの2D pixel artを維持しながら、
最低限の簡易Animationでゲームらしさを出す。

高コストなskeletal animationや3D animationは使用しない。

---

## 1. Core Structure

各Gearは最低限、以下を分離する。

- BODY
- BARREL

BARRELはBODYとは別spriteとして扱い、
pivotを中心にAim Angleへ追従して回転する。

BODYのAnimationとBARREL rotationは独立させる。

---

## 2. File Direction

推奨素材形式:

- BODY static / animation: PNG
- BARREL: PNG
- Animation: sprite sheet PNG
- Optional effect sprites: PNG

例:

```text
gear/
├─ scout/
│  ├─ scout_body_idle.png
│  ├─ scout_body_move.png
│  ├─ scout_body_fire.png
│  ├─ scout_body_hit.png
│  └─ scout_barrel.png
└─ heavy/
   ├─ heavy_body_idle.png
   ├─ heavy_body_move.png
   ├─ heavy_body_fire.png
   ├─ heavy_body_hit.png
   └─ heavy_barrel.png
```

Prototype初期はさらに簡略化してよい。

最小構成:

```text
body.png
body_move_sheet.png
barrel.png
```

---

## 3. Animation Budget

1 stateあたりの目安:

- Idle: 2 frames
- Move: 2–4 frames
- Fire recoil: 1–2 frames
- Hit reaction: 1–2 frames
- Destroyed: 2–4 frames optional

高フレーム数を要求しない。

ゲームの可読性を優先する。

---

## 4. BARREL Rotation

BARRELはAim Angleに応じて連続回転する。

Animation frameで角度を表現しない。

必要情報:

- barrel pivot X
- barrel pivot Y
- barrel visual origin
- minimum angle
- maximum angle

BARREL回転はClient visual。

実際のProjectile angleはServer authority。

Clientの見た目だけを変更してServer projectile angleを変更できない。

---

## 5. Scout Gear Animation

速機のVisual Theme:

- 軽量
- 高機動
- 明るい白〜青
- Orange accent
- 細いsilhouette

### Idle
2 frames程度。

例:
- BODYを1px上下
- suspensionの微小変化
- small heat / light pulse

### Move
3–4 frames推奨。

表現:
- wheel rotation
- leg / suspension motion
- body lean
- small dust

軽快に見えることを優先。

### Fire
1–2 frames。

表現:
- BODYがわずかに後退
- BARREL recoil
- small muzzle flash

### Hit
1–2 frames。

表現:
- short body shake
- 1–2px knockback visual
- small spark

---

## 6. Heavy Gear Animation

重機のVisual Theme:

- Heavy
- Low center of gravity
- Black / dark gray
- Red accent
- Thick silhouette
- Large cannon

### Idle
2 frames程度。

表現:
- heavy body vibration
- heat core pulse
- subtle suspension compression

速機より動きを小さく、重く見せる。

### Move
2–3 frames。

表現:
- heavy wheel / track-like motion
- slow suspension travel
- small dust / debris

速機よりAnimation speedを遅くしてよい。

### Fire
2 frames推奨。

表現:
- visible body recoil
- stronger BARREL recoil
- stronger muzzle flash
- short dust burst

### Hit
1–2 frames。

表現:
- short heavy shake
- sparks
- minimal displacement

---

## 7. Recoil

Fire時は以下を分離してよい。

- BARREL backward recoil
- BODY backward visual offset
- muzzle flash

RecoilはVisual effect。

Game Stateのpositionを勝手に変更しない。

---

## 8. Effects

軽量な2D effectのみ使用する。

使用可:

- muzzle flash
- 2–4 frame explosion
- small smoke
- small dust
- spark
- short screen shake

使用しない:

- heavy particle simulation
- volumetric smoke
- expensive post-processing
- complex shader-based destruction

---

## 9. Performance

目標:

- 10年前程度の一般的PCでも軽く動く
- high-end GPU不要
- 8 Gear同時表示を想定
- AnimationでServer負荷を増やさない

AnimationはClient側のみ。

Serverはframe stateを管理しない。

---

## 10. Gameplay Readability

Animationは見た目のためだけにGame Stateを曖昧にしない。

以下を常に優先する。

1. Current Gear位置
2. Aim方向
3. Projectile発射点
4. Hit / Damage結果
5. Visual effect

EffectがHit Pointや地形を隠しすぎない。

---

## 11. Collision Independence

Visual AnimationとCollisionを分離する。

BODY frameが変わっても、

- hitPoint
- Direct Hit Radius
- groundContactPoint

はServer側のCollision Ruleに従う。

Animation frameごとのpixel-perfect collisionは使用しない。

---

## 12. Sprite Scale

Gear spriteはStage上で小さく表示されても、
Scout / Heavyをsilhouetteで区別できること。

細密pixel artより、

- shape
- color
- cannon size
- body height
- body width

を優先する。

---

## 13. Initial Implementation Order

Visual Layer実装時の順序:

1. BODY / BARREL分離
2. BARREL Aim rotation
3. Move animation
4. Fire recoil
5. Hit reaction
6. Explosion / destroyed effect

一度に全部作り込まない。

---

## 14. Tuning

Visual Animation関連の値も集中管理可能にする。

例:

- IDLE_FPS
- MOVE_FPS
- FIRE_RECOIL_PIXELS
- FIRE_RECOIL_MS
- HIT_SHAKE_PIXELS
- HIT_SHAKE_MS

ただし本格Animation Editorは作らない。

---

## 15. Acceptance

Visual Layer実装時は最低限:

- Scout / HeavyのBODYを区別できる
- BARRELがAim Angleに追従する
- BODY animationとBARREL rotationが独立
- Move animationが軽量
- Fire recoilがGame State positionを変更しない
- Hit reactionがCollision結果を変更しない
- 8 Gear表示を想定した軽量構造
- ServerへAnimation負荷を持ち込まない

ことを確認する。


## 16. HP Visibility

Prototype default:

- Own Gear: HP visible
- Ally Gear: HP visible
- Enemy Gear: exact HP hidden
- Enemy Gear: damage state communicated by visual damage only

Enemy damage readability uses staged visual states such as:

- normal
- lightly scorched / small smoke
- heavier scorch / more smoke
- severe damage / strong smoke or heat
- destroyed / visibly crushed wreck with smoke or flame

Exact thresholds remain centralized tuning values and should not be encoded into sprite art itself.

### Future Option

将来はPlayer preferenceとしてHP表示を切り替えられる余地を残す。

Candidate options:

- own HP only
- own + ally HP
- bar only
- bar + number

PrototypeではSettings UIを作らず、

`own + ally visible / enemy hidden`

を固定標準とする。


## 17. Damage State Visual Rules

Enemy Gear damage readability uses 5 visual stages.

### Stage 1 — Normal
- No visible damage
- No smoke
- Mobility system visually intact

### Stage 2 — Light Damage
- Small scorch marks
- Small amount of smoke
- Minor cosmetic damage only
- Mobility system visually intact

### Stage 3 — Medium Damage
- More scorch marks
- Moderate smoke
- Visible armor / exterior damage
- Mobility system visually intact

### Stage 4 — Heavy Damage
- Strong smoke
- Small flame / heat glow may appear
- Large exterior damage is allowed
- Mobility system MUST still look functional
- Do not depict wheels, tracks, suspension or legs as fully destroyed while HP > 0

### Stage 5 — Destroyed / HP 0
- Mobility system may collapse
- Gear may become visibly crushed / flattened
- Large smoke and flame are allowed
- Detached debris is allowed
- Wreck must be visually unmistakable as non-operational

## Mobility Consistency Rule

For any Gear with HP > 0:

- It must remain visually plausible that the Gear can move
- Wheels / tracks / legs / suspension must not appear completely broken
- Cosmetic deformation is allowed
- Functional destruction of mobility parts is reserved for HP 0 unless a future gameplay rule explicitly introduces mobility damage

This rule exists to keep visual state consistent with gameplay capability.

## 18. Visual Damage vs Gameplay State

Damage visuals are descriptive only.

They do not independently:

- reduce movement
- change projectile behavior
- alter hitPoint
- alter groundContactPoint
- disable actions

Any future gameplay effect from subsystem damage requires a separate explicit specification and must not be inferred from artwork alone.


## 19. Damage State Thresholds

Prototypeの正式なHP外観閾値は以下とする。

- Stage 1 — Normal: HP 100%〜71%
- Stage 2 — Light Damage: HP 70%〜41%
- Stage 3 — Medium Damage: HP 40%〜11%
- Stage 4 — Heavy Damage: HP 10%〜1%
- Stage 5 — Destroyed: HP 0%

Reference points:

- 100%
- 70%
- 40%
- 10%
- 0%

Threshold values are centralized tuning values and may be tuned later,
but the five-stage visual model remains the default prototype rule unless explicitly changed.
