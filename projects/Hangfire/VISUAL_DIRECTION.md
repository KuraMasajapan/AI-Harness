# Hangfire — Visual Direction

Status: ADOPTED
Date: 2026-09-27

## Core Visual Style

Hangfireのゲーム内表現は、荒めの2D pixel artを正式な方向性として採用する。

目的:
- 10年前程度の一般的PCでも軽く動かしやすい
- 砲撃・風・地形破壊を視認しやすい
- 小さい画面表示でもGearの役割を判別しやすい
- 高精細化よりゲーム性とレスポンスを優先する

## Gear Direction

### Scout / 速機
- 明るめの白〜青系を基調
- オレンジ系アクセント
- 軽量・高機動に見える細いシルエット
- 車輪または軽量脚部
- 砲身は独立レイヤーとして回転可能

### Heavy / 重機
- 黒〜濃いグレーを基調
- 赤系アクセント
- 低重心・厚い装甲・重量感
- 速機より横幅と密度を強調
- 大口径砲
- 砲身は独立レイヤーとして回転可能

## Gameplay Sprite Rule

Gearは最低でも以下を分離する。

- BODY layer
- BARREL layer

BARRELはpivotを基準に角度入力に応じて回転する。

初期の画面表示では粗いpixel artを維持し、
高解像度の細密spriteを前提にしない。

## Stage Direction

1 stageは最低でも以下を分離する。

- Background
- Destructible foreground terrain
- Authoritative collision / destruction representation

Backgroundは破壊しない。
Foreground terrainはゲーム中に破壊される。
Collision / destruction representationは表示画像と分離してよい。

## Resolution Direction

Visual target:
- HD基準 1280x720

ただし、
- rendering detail
- collision resolution
- destruction mask resolution

は同一である必要はない。

Game Logicの計算量を画面解像度に比例させない。

## Performance

Visual qualityより以下を優先する。

1. Input response
2. Stable gameplay
3. Projectile readability
4. Terrain destruction
5. Stable frame rate
6. Effects
7. Decorative detail

Heavy post-processing、複雑なshader、pixel-perfect Gear collisionは不要。

## Source of Truth Boundary

このファイルはHangfire独自のVisual Direction。
既存作品のsprite、UI、map、配色、固有デザインを直接コピーしない。


## Gear Animation

Gearの簡易Animation・BODY/BARREL分離・Aim rotationの正式仕様は、

`GEAR_ANIMATION.md`

を参照する。

荒めのpixel artを維持し、2〜4 frame中心の軽量Animationを採用する。
