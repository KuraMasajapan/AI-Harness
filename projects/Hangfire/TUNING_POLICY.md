# Hangfire — Tuning Seed Policy

## Purpose

Hangfireでは、ゲーム完成後にHuman Playtestを使ってBalanceを詰める。

今は本格的なTuning UIやEditorを作らない。

代わりに、将来の調整を容易にするために、
**Gameplay / Balanceに関わる数値を最初から集中管理できる構造にしておく。**

これは機能実装の「種まき」であり、今すぐEditorを完成させる要求ではない。

---

## 1. Core Rule

Gameplay / Balanceに関わる値を実装コード中へ散在させない。

同じ意味の値を複数箇所に重複定義しない。

可能な限り、

- config
- constants
- tuning values
- balance values

として一か所または責務ごとの少数ファイルへ集約する。

---

## 2. Tuning UI

現段階では本格的なTuning UIを実装しない。

必要になったLayerで、
簡単なDEV-only controlを追加してよい。

例:

- numeric input
- slider
- +/- button
- show/hide debug overlay

ただし、UI自体を作り込まない。

---

## 3. Human Playtest

Humanは実際にDesktop環境でPlaytestし、
自然言語で相対変更を指示できる。

例:

- 「最大風力はいまの70%を最大値にする」
- 「破壊力を100%上げる」
- 「爆風半径を20%広げる」
- 「Hit Pointを6px下げる」

ASTRAは対象値だけを変更し、
関係しないBalance値や仕様を同時に変更しない。

---

## 4. Layer-by-Layer Seeding

各Layerでは、そのLayerに必要なTuning値だけ追加する。

### Layer 1
例:
- WIND_MAX
- WIND_MIN
- GRAVITY
- POWER_MIN
- POWER_MAX
- PROJECTILE_SPEED_SCALE

### Layer 2
例:
- MOVEMENT_COST
- ATTACK_COST
- ACTION_COST
- TURN_DELAY

### Layer 3
例:
- DIRECT_HIT_RADIUS
- BLAST_RADIUS
- DAMAGE
- DAMAGE_FALLOFF
- CRATER_RADIUS

### Layer 4
例:
- TURN_TIME_LIMIT
- INPUT-related thresholds

### Layer 5
Room / TeamのうちBalance調整が必要な値だけ。

### Layer 6
例:
- Scout values
- Heavy values
- Item values

### Layer 7
Visual-only tuning values。

未実装Layerの値を先回りして大量に作らない。

---

## 5. Source of Truth

現在採用中のTuning値は、
repository内の定義をSource of Truthとする。

会話中の数字だけを正式値として扱わない。

Humanが調整を承認したら、
repositoryの該当値を更新する。

---

## 6. Change Discipline

Tuning変更では、

1. 対象値
2. 変更前
3. 変更後
4. 理由
5. Validation結果

を必要最小限記録する。

大きなBalance変更を別の仕様変更と混ぜない。

---

## 7. Safety Range

数値変更でGame Stateが壊れないように、
必要な値には合理的なmin / maxを設定してよい。

ただし、過度に狭いrangeを勝手に決めない。

Human Playtestで広げる可能性を残す。

---

## 8. DEV Debug Visualization

調整が必要なLayerでは、
DEV-only表示を追加してよい。

例:

- Wind vector
- Projectile path
- Hit Point
- Direct Hit Radius
- Blast Radius
- Collision point

本番UIとは分離する。

---

## 9. Do Not Do Yet

現段階では作らない。

- full game editor
- visual scripting
- complex tuning dashboard
- remote admin panel
- database-backed balance editor
- live production config service
- versioned balance service

---

## 10. ASTRA Rule

ASTRAは新しいGameplay数値を追加するとき、

- hard-codeが本当に必要か
- tuning対象か
- 既存集中定義へ入れられるか

を確認する。

Tuning対象なら集中管理する。

将来のEditor実装を理由に、
不要な抽象化やframeworkを追加しない。

---

## 11. Completion

このPolicyの目的は、

**完成後にHuman Playtestで高速にBalanceを詰められる構造を維持すること。**

本格的なTuning UI / Editorの実装時期は、
ゲームの主要Layer完成後に判断する。


## Turn Load Tuning Tool Readiness

Turn-order / Cooling-recovery tuning is a high-priority balance area.

Implementation should keep all related values centralized so a later tuning tool can adjust them without changing gameplay code.

At minimum, the future tool should be able to expose:

- elapsed-time weight
- Cooling-used weight
- Weapon load values
- Item load values
- next-action delay scaling
- Cooling recovery scaling
- minimum / maximum recovery
- Skip baseline

Initial playtest direction:

- start with elapsed time weighted more heavily
- observe actual turn tempo and Skip usage
- tune from playtest evidence
- avoid hard-coding final balance early

The first development step does not require a polished editor UI.
The requirement is that the data model is ready for one centralized tuning surface later.
