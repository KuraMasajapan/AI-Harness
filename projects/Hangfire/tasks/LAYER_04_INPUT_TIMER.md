# Hangfire — Layer 4 Turn Input & 20-Second Limit

Status: ADOPTED SPEC
Date: 2026-09-27

## Purpose

Layer 4 adds real-time turn input handling and a 20-second turn limit.

This replaces the earlier provisional 15-second wording.

---

## 1. Turn Time Limit

Each active turn has a 20-second input limit.

- TURN_INPUT_LIMIT_SEC = 20
- Timer starts when the player's turn becomes active
- Server owns the authoritative turn timer / timeout decision
- Client displays the remaining time

At 20 seconds, the turn normally ends automatically.

---

## 2. Timeout Default

If the 20-second limit is reached and the player is NOT currently charging shot power:

- the turn ends immediately
- no automatic shot is fired
- no new move / angle / item / fire input is accepted for that turn
- control passes to the next eligible player according to the turn-order system

This is a forced turn end.

---

## 3. Power Gauge Exception

Shot power is controlled by holding the Space key.

- Space key down: begin power charging
- Hold duration changes the power gauge
- Space key up: lock power and fire

If power charging has already started before the 20-second deadline,
that charging operation may continue beyond the deadline.

This is the ONLY normal input operation allowed to remain active after timeout.

During this over-time charging state:

- existing power charge continues
- Space release remains valid
- releasing Space locks power and fires
- no new movement is allowed
- no new angle adjustment is allowed
- no new item activation is allowed
- no new charge sequence may be started after timeout

The timeout does not cancel a charge already in progress.

---

## 4. Turn End After Overtime Shot

If the player fires from an overtime charge:

the turn does NOT end at the instant the 20-second limit is crossed.

The turn remains in a resolving state until:

1. Space is released
2. Power is locked
3. Shot is fired
4. Projectile flight completes
5. Impact is resolved
6. Damage / terrain / elimination resolution completes
7. Landing / impact visual effect completes

After the firing and landing-effect sequence is complete,
the turn ends and control passes to the next player.

---

## 5. No Indefinite Free Input

After 20 seconds:

- only the already-active Space-key charge may continue
- all other gameplay inputs are locked for that turn

This prevents the overtime exception from becoming extra general decision time.

A future maximum charge duration may be introduced if needed,
but is not defined here unless Human explicitly specifies it.

---

## 6. Authority

Server authority remains unchanged.

The server determines:

- turn start time
- timeout state
- whether charging began before timeout
- whether Space release is still valid
- accepted power value
- shot result
- turn end
- next player

The client may animate the gauge, but cannot extend the turn by forging timer state.

---

## 7. Client UI

Minimum Layer 4 UI:

- visible 20-second countdown
- aim control
- move control
- Space-key power gauge
- clear charging state
- clear timeout / overtime-charge state

The UI should make it obvious when:

- normal input time remains
- the 20-second limit has expired
- the player is only allowed to finish the active power charge

---

## 8. Acceptance

Layer 4 must demonstrate:

1. Turn timer starts at 20 seconds
2. Timer is server authoritative
3. Normal turn ends automatically at timeout
4. No automatic shot on timeout
5. Space hold started before timeout remains valid after timeout
6. Space release after timeout fires with the charged power
7. Other inputs are rejected after timeout
8. Turn does not advance during projectile / impact resolution
9. Turn advances only after shot and landing-effect resolution complete
10. Existing Layer 1–3 behavior remains valid

---

## 9. Explicitly Not Defined Yet

This spec does not yet define:

- a hard maximum Space-hold duration
- network latency compensation policy
- disconnect behavior during a turn
- item timing details
- room synchronization for up to 8 players

Those require later explicit decisions or the appropriate Layer.


## 10. Power Gauge Direction

The power gauge is one-way only.

- Charge starts from minimum power
- Holding Space increases power continuously toward maximum
- The gauge does NOT bounce or reverse
- The gauge does NOT oscillate between min and max

When Space is released before maximum:

- current gauge value is locked
- shot fires at that power

When the gauge reaches maximum while Space is still held:

- charge stops at maximum
- shot fires automatically at MAX power
- the player does not need to release Space
- no additional hold time is allowed beyond MAX

This rule also applies during the overtime-charge exception.

If the 20-second limit has already expired and the active charge reaches MAX:

- the shot fires automatically at MAX power
- projectile / impact / landing-effect resolution completes
- then the turn ends

## 11. Power Gauge Authority

The client may animate the visual gauge.

The server determines the accepted power value from authoritative charge timing / state.

The client cannot:

- hold beyond MAX to gain extra power
- reset charge after timeout
- start a second charge after timeout
- submit power greater than MAX


## 12. Power Charge Time

Prototype tuning seed:

- POWER_CHARGE_TO_MAX_SEC = 5.0

Meaning:

- holding Space from minimum power reaches MAX power in 5 seconds
- power rises continuously in one direction
- releasing before 5 seconds fires at the current proportional power
- reaching 5 seconds while still holding Space auto-fires at MAX power

This is an initial tuning value, not a permanent final balance value.

Human playtest direction:

- start at 5 seconds
- if it feels too fast, increase charge time
- accepted tuned value then becomes the new Source of Truth

The value must be centralized in tuning/configuration and not hard-coded across multiple client/server locations.


## 13. Power Gauge Curve

The power gauge increases at a constant linear rate.

- progression is linear
- no acceleration
- no deceleration
- no easing curve
- no stepped segments
- no bounce / reverse

Prototype mapping:

- t = 0.0 sec -> minimum power
- t = 2.5 sec -> 50% power range
- t = 5.0 sec -> MAX power and automatic fire

Conceptually:

```text
chargeRatio = clamp(heldSeconds / POWER_CHARGE_TO_MAX_SEC, 0, 1)
power = POWER_MIN + (POWER_MAX - POWER_MIN) * chargeRatio
```

The server remains authoritative for the accepted charge duration and resulting power.
Client animation should visually match this same linear relationship.


## 14. Aim Angle Control

Hangfire uses two complementary aim-input methods.

### Keyboard Fine Adjustment

Aim angle changes continuously while the aim key is held.

Prototype tuning seed:

- full aim range: 180 degrees
- full-range traversal time: 5.0 seconds
- constant angular speed
- no acceleration / deceleration curve

This means:

```text
AIM_RANGE_DEG = 180
AIM_FULL_SWEEP_SEC = 5.0
AIM_SPEED_DEG_PER_SEC = 36
```

Keyboard aim is intentionally slower and suited for fine adjustment.

### Mouse Direct Adjustment

The player may directly adjust aim by:

1. left-clicking the active Gear
2. holding the left mouse button
3. moving the pointer to indicate the desired firing direction

While dragging:

- aim angle updates immediately from the pointer direction relative to the Gear / barrel pivot
- this is a direct-positioning input, not a slow sweep
- the player may use mouse input to move quickly near the desired angle
- keyboard input may then be used for fine adjustment

Intended interaction:

```text
mouse drag -> rough / fast angle placement
keyboard hold -> slow precise adjustment
```

### Authority

Client may calculate and display the requested angle interactively.

Server remains authoritative for the accepted aim angle used for firing.

Client may not submit values outside the legal aim range.

### Timeout Interaction

Normal aim input is only valid before the 20-second timeout.

After timeout:

- no new keyboard aim adjustment
- no new mouse aim drag adjustment
- only an already-active power charge may continue under the overtime rule

### Tuning

The 5-second / 180-degree sweep is a provisional prototype value.

If Human playtest finds keyboard aiming too slow or too fast,
adjust `AIM_FULL_SWEEP_SEC` while keeping the control model unchanged.


## 15. Movement Control

Movement uses continuous key-hold input.

Prototype behavior:

- hold left movement key -> Gear moves continuously left
- hold right movement key -> Gear moves continuously right
- release key -> movement stops immediately
- no fixed-step / per-press movement
- no tile-based movement
- no click-to-move

Movement is intended to feel direct and analog-like even though input is digital.

### Movement Speed

Movement speed must be centralized in tuning.

Example concept:

```text
MOVE_SPEED_UNITS_PER_SEC
```

Scout and Heavy may later use different movement tuning in Layer 6.

Layer 4 should preserve the current common movement model unless the current task explicitly authorizes Gear-specific values.

### Resource Use

Existing Layer 2 movement resource rules remain authoritative.

Continuous movement should consume resource according to actual accepted movement distance / duration rather than arbitrary keypress count.

Exact implementation must preserve:

- server-authoritative position
- server-authoritative resource cost
- no client-side teleporting
- no free movement from repeated input events

### Timeout Interaction

Normal movement is valid only before the 20-second turn deadline.

At timeout:

- active movement stops
- further movement input is rejected for that turn
- only an already-started power charge may continue under the overtime rule

### Terrain / Boundary Interaction

Movement must stop or be constrained by authoritative terrain / world rules.

Layer 4 must not introduce stacked-lane or pseudo-3D movement.

The Gear remains on the single-surface 2D terrain model defined for Hangfire.
