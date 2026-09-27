# Hangfire — Gear Performance Specification

Status: ADOPTED DIRECTION / PROVISIONAL TUNING
Date: 2026-09-27

## Purpose

Hangfireの2種類のGearに、見た目だけでなく移動・冷却性能の個性を与える。

この差別化はLayer 6で実装する。
Layer 4では共通操作モデルだけを実装し、Gear別数値を先回りして適用しない。

## 1. Cooling Capacity

Each Gear may have its own cooling-capacity value.

Cooling capacity represents the limited action / mobility resource used during battle.

Exact maximum values for Scout and Heavy are not fixed yet.

They must be centralized as Gear-specific tuning values when Layer 6 is implemented.

Example keys:

- SCOUT_COOLING_CAPACITY
- HEAVY_COOLING_CAPACITY

## 2. Movement Efficiency

The two Gear types use different movement efficiency.

Prototype direction:

- Heavy movement efficiency = 1.0x baseline
- Scout movement efficiency = 2.0x baseline

Meaning:

For the same amount of movement-resource / cooling consumption,
Scout can travel approximately twice the distance of Heavy.

Equivalent interpretation:

```text
same cooling cost:
Heavy distance = 1.0
Scout distance = 2.0
```

This is the initial prototype tuning target.

## 3. Design Intent

Scout:

- lighter
- more mobile
- better movement efficiency
- can reposition farther for the same cooling expenditure

Heavy:

- heavier
- lower movement efficiency
- must spend more of its limited cooling resource to reposition the same distance
- compensates through later-defined combat strengths

## 4. Separation of Capacity and Efficiency

Cooling capacity and movement efficiency are separate tuning dimensions.

A Gear may differ in:

- total cooling capacity
- movement distance per unit of cooling
- later action-specific cooling costs

Do not hard-code identity only through one number.

For the current decision:

- movement-efficiency ratio is defined
- exact per-Gear maximum cooling capacity remains TBD

## 5. Layer Boundary

Layer 4:
- continuous movement input
- simultaneous movement + aim
- common server-authoritative movement model

Layer 6:
- Scout / Heavy-specific cooling capacity
- Scout / Heavy-specific movement efficiency
- final tuning values

Do not apply the 2x Scout efficiency early unless Human explicitly changes the layer order.

## 6. Tuning Rule

Initial target:

- HEAVY_MOVE_EFFICIENCY = 1.0
- SCOUT_MOVE_EFFICIENCY = 2.0

Human playtest may later reduce or increase this ratio.

The accepted tuned value becomes the new Source of Truth.
