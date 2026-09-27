# Hangfire — Stage Design Specification

Status: ADOPTED
Date: 2026-09-27

## Purpose

HangfireのPrototype Stageを、最大8人の砲撃戦・横スクロール・破壊可能地形に対応させる。

Pattern EをVisual baselineとして採用する。

---

## 1. Viewport and World

- Viewport target: 1280 x 720
- Stage world width: approximately 1.5x viewport or larger
- Horizontal scrolling is required
- Entire stage is not shown at once
- World size may be tuned after playtest

The viewport is a camera window, not the full battlefield.

---

## 2. Stage Layers

Each stage is separated into:

1. Background
2. Destructible foreground terrain
3. Authoritative collision / destruction representation

Background is not destructible.

Foreground terrain is visually destructible.

Collision / destruction state is authoritative and may use a lower-resolution mask or compact representation.

---

## 3. Spawn Philosophy

Spawn positions are NOT divided into left-team and right-team zones.

At match start:

- Team membership is determined separately from spawn position
- All participating Gear are distributed across valid spawn slots
- Team A and Team B may begin intermixed across the battlefield
- Adjacent spawn slots may contain opposing teams
- The opening situation should feel immediately tactical rather than forming two clean front lines

This is the default Hangfire prototype spawn model.

---

## 4. Random Spawn Rule

Use predefined valid spawn slots on the stage.

At match start:

1. Collect the active Gear list
2. Shuffle valid spawn slots server-side
3. Assign one slot to each Gear
4. Do not group slots by team
5. Prevent duplicate occupation of the same slot
6. Reject invalid slots that are inside terrain, outside world bounds, or otherwise unusable

Random placement must be server authoritative.

The selected spawn assignment should be reproducible from match state or logged with the match input/state record when practical.

---

## 5. Fairness Constraints

Random does not mean unconstrained.

Spawn slot design should avoid:

- immediate overlap
- unavoidable instant collision
- impossible movement positions
- placement inside terrain
- out-of-bounds placement
- obviously unusable isolated pixels

Stage geometry and spawn slot candidates should be designed so that every valid slot is playable.

No left/right team symmetry is required.

---

## 6. Maximum Player Count

The stage must support:

- 2 players
- 4 players
- 6 players
- 8 players

Only the required number of spawn slots are selected for that match.

Prototype standard:

- Define exactly 12 valid spawn candidate slots
- For 2 / 4 / 6 / 8 player matches, select only the required number
- Selection is randomized server-side
- 12 candidates provide opening variety without making stage authoring unnecessarily complex

---

## 7. Team Readability

Because teams are intermixed at match start, team identity must remain visually readable.

Allowed tools:

- team outline
- small team marker
- accent color
- nameplate / ally marker
- own / ally HP visibility rule

Do not rely on left/right battlefield position to communicate team membership.

---

## 8. Camera

The camera must support horizontal scrolling across the full world.

Prototype camera behavior may be simple:

- center on current Gear
- follow projectile during flight
- allow bounded horizontal view shift where needed

Do not require the full stage to fit on screen.

---

## 9. Terrain Destruction

Terrain destruction is part of the Stage model.

The visible terrain art and authoritative destruction representation may be separate.

Destruction must not depend on high-resolution background art.

---

## 10. Asset Direction

Recommended prototype structure:

```text
stage/
└─ pattern_e/
   ├─ background.png
   ├─ foreground.png
   ├─ mask.png
   └─ stage.json
```

`stage.json` may contain:

- world size
- spawn slot candidates
- asset references
- camera bounds
- collision-mask reference
- future stage metadata

---

## 11. Prototype Constraint

Do not add:

- stage-specific gameplay modifiers
- scripted hazards
- moving platforms
- environmental damage
- multiple stage mechanics

until explicitly specified.

The first goal is a readable, destructible, scrollable battlefield with mixed random spawning.


## 12. Camera Input

Prototype desktop camera controls:

### Edge Panning

The player can move the visible area by moving the mouse cursor near the screen edges.

- Left edge zone -> pan left
- Right edge zone -> pan right
- Top edge zone -> pan up
- Bottom edge zone -> pan down

The trigger zone should begin slightly before the absolute outermost pixel of the viewport.

Do not require the cursor to touch the exact screen border.

Use a small configurable edge margin so camera movement is easy and deliberate.

Recommended concept:

- EDGE_PAN_MARGIN
- EDGE_PAN_SPEED

Camera movement must remain inside world bounds.

### Mouse Wheel Zoom

Mouse wheel controls camera zoom.

Purpose:

- inspect nearby terrain before firing
- notice small debris or tiny remaining terrain pixels
- reduce accidental self-damage caused by firing into unnoticed terrain immediately in front of the Gear

Zoom must be client-side visual camera behavior only.

It must not alter:

- projectile physics
- collision
- hitPoint
- terrain state
- damage
- authoritative positions

### Zoom Limits

Zoom must have configurable minimum and maximum limits.

The player must not be able to zoom so far out that gameplay readability or intended battlefield information is broken.

The player must be able to zoom in enough to inspect terrain immediately around the active Gear.

### Tiny Terrain Residue

After terrain destruction, extremely small remaining terrain pixels may exist.

This is acceptable prototype behavior.

The system does not need to guarantee cleanup of every single isolated pixel.

However:

- collision representation must remain consistent with what the server considers solid
- zoom allows the player to inspect suspicious terrain near the active Gear
- no invisible collision should be intentionally introduced

This behavior is accepted as part of the prototype destruction model.

## 13. Camera Usability

Camera controls should prioritize:

1. quick inspection around the current Gear
2. easy manual stage navigation
3. projectile tracking
4. low implementation complexity

Do not add minimap, drag-to-pan, cinematic camera system, or advanced camera editor unless explicitly requested.
