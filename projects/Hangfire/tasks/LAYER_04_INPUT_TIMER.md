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
