# Hangfire — Turn Load / Cooling Recovery Model

Status: ADOPTED DESIGN / FORMULA TUNING TBD
Date: 2026-09-27

## Purpose

Hangfireの次回行動順と冷却Resource回復量を、
その手番でプレイヤーがどれだけ時間・Resource・装備負荷を使ったかで決める。

短時間・低負荷で行動を終えるほど、
次回の行動順が早くなり、冷却Resource回復量も大きくなる。

---

## 1. Turn Load Score

各手番終了時に、以下4要素を共通ポイントへ換算して合計する。

1. Turn endまでの消費時間
2. その手番で消費したCooling Resource
3. 選択Weapon固有の追加消費Resource / Load
4. Item使用時のItem固有追加Point

Concept:

```text
TURN_LOAD_SCORE =
  timePoint
+ coolingUsedPoint
+ weaponLoadPoint
+ itemLoadPoint
```

各要素の係数・換算式はTuning対象であり、現時点では未固定。

---

## 2. Next Turn Order

TURN_LOAD_SCOREが小さいほど、
そのGearの次回行動タイミングは早くなる。

Concept:

```text
lower TURN_LOAD_SCORE
=> lower next-action delay
=> earlier next turn
```

短時間で即座に攻撃してTurn Endした場合、
長時間悩んで大きく移動・重いWeapon・Itemを使った場合より、
次の行動順を取りやすい。

---

## 3. Cooling Recovery

同じTURN_LOAD_SCOREをCooling Resource回復量にも使う。

```text
lower TURN_LOAD_SCORE
=> larger cooling recovery

higher TURN_LOAD_SCORE
=> smaller cooling recovery
```

つまり、
「次の行動が早い」ことと「次のTurn開始時のCooling回復が大きい」ことは、
同じTurn負荷の低さから生じる。

---

## 4. Manual Skip / Immediate Turn End

Turn開始直後にPlayerが手動でTurn End / Skipした場合は、
原則として最小負荷の行動になる。

結果:

- next-turn delayが最小クラス
- 次回行動順が最も早い側になる
- Cooling Resource回復量が最大クラスになる

Skipは「何もしなかった罰」ではなく、
次回の行動機会とCoolingを確保するための戦術的選択肢として扱う。

---

## 5. Design Intent

この仕組みにより、

- 素早く射撃してTurnを終える
- 移動を控える
- 軽いWeaponを選ぶ
- Itemを温存する
- 即Skipする

といった低負荷行動に、
次回行動順とCooling回復の両方で利点が生まれる。

逆に、

- 長時間操作する
- 多く移動する
- 重いWeaponを使う
- Itemを使う

ほど次回行動が遅くなり、Cooling回復も抑えられる。

---

## 6. Server Authority

Serverが以下を確定する。

- turn elapsed time
- Cooling Resource consumption
- Weapon load
- Item load
- TURN_LOAD_SCORE
- next-action timing
- Cooling recovery

Clientは表示のみで、Scoreや回復量を直接指定できない。

---

## 7. Relationship to Existing Layer 2

Layer 2の`nextActionTime`モデルは、
将来このTURN_LOAD_SCOREベースの遅延計算へ発展させる。

既存の単純Action CostはPrototype seedであり、
最終的なHangfireのTurn orderはこの4要素モデルをSource of Truthとする。

ただし実装変更はCurrent LayerのScopeに従い、
Human承認なしにLayer順を飛ばさない。

---

## 8. Tuning TBD

未固定:

- timePoint換算率
- Cooling消費量のPoint換算率
- WeaponごとのLoad Point
- Itemごとの追加Point
- TURN_LOAD_SCOREからnext-action delayへの変換式
- TURN_LOAD_SCOREからCooling回復量への変換式
- 最大 / 最小回復量
- Skipの厳密な最小値

これらはPlaytestで調整する。


## 9. Initial Weighting Direction

Human-approved tuning direction:

Start playtesting with elapsed turn time weighted more heavily than the other Turn Load inputs.

Initial design intent:

- elapsed time: primary / heavier influence
- Cooling Resource consumed: secondary
- Weapon load: secondary
- Item load: secondary

Do not treat these weights as final balance.

The purpose of the initial time-heavy weighting is to make the intended behavior clearly observable:

- fast decisions should noticeably improve next-turn timing and Cooling recovery
- slow turns should noticeably cost tempo

After Human playtest, reduce or rebalance the time weight if it dominates too strongly.

Exact coefficients remain TBD and must be changed through centralized tuning rather than scattered formulas.

## 10. Turn Load Tuning Block

The implementation should expose one centralized tuning block for the Turn Load model.

Conceptual structure:

```text
TURN_LOAD_TUNING = {
  timeWeight,
  coolingUsedWeight,
  weaponLoadWeight,
  itemLoadWeight,
  nextActionDelayScale,
  recoveryScale,
  recoveryMin,
  recoveryMax,
  skipBaseLoad
}
```

Names may differ in code, but all related balance values should be adjustable from one place.

A later Human-facing tuning tool may edit these values, but the first implementation should keep the underlying model simple and centralized.
