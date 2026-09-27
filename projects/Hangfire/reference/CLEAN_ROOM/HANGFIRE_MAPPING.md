# Hangfire Clean-room Mapping

このファイルをCodex向け参考資料の中心とする。

Assault Gearを実装の答えとして使わない。
使う順序は次とする。

Observed behavior
→ General mechanic
→ Hangfire independent design

## Projectile
Observed:
角度、威力、風によって着弾が変化する。

General mechanic:
Player skill comes from predicting projectile behavior under environmental variation.

Hangfire:
- angle
- power
- wind
- server-side deterministic projectile calculation

Do not copy:
- original projectile constants
- original angle limits
- original power scale
- original HUD

## Turn timing
Observed:
行動やアイテムのTurn Rateが次の手番に影響する。

General mechanic:
Powerful actions have temporal cost.

Hangfire:
`actionCost -> nextActionTime`

Do not copy:
- original Turn Rate values
- original internal formula

## Resource
Observed:
Fuelが移動や強い行動の選択に関係する。

General mechanic:
Movement and offense compete for a limited tactical resource.

Hangfire:
独自Resourceを移動または攻撃に消費する。

Do not copy:
- original Fuel maximum
- recovery values
- attack costs

## Terrain
Observed:
地形・位置・落下によってHP以外の戦術が生まれる。

General mechanic:
Projectile impact can change positional risk.

Hangfire:
CURRENT_LAYERに入るまでは先回り実装しない。

## Units
Observed:
機体ごとに移動・防御・攻撃特性が異なる。

Hangfire:
- 速機
- 重機

2種類のみ。元機体を再現しない。

## Items
Observed:
Limited-use items temporarily modify tactical state.

Hangfire:
- 偏流
- 残熱

元ゲームのアイテムセットを再現しない。

## Multiplayer
Observed:
多人数チーム戦がゲーム構造の中心。

Hangfire:
- 2 / 4 / 6 / 8 players
- 1v1 / 2v2 / 3v3 / 4v4
- odd count cannot start
- room-code invite
- no matchmaking in prototype

# Boundary for Codex
1. この資料は参考でありAssault Gear再現仕様ではない。
2. 固有コード、名称、数値、画像、音声、マップ、UIをコピーしない。
3. HangfireのSource of Truthを常に優先する。
4. 矛盾時はHangfire仕様を優先する。
5. 未定義項目をAssault Gearから推測して補完しない。
