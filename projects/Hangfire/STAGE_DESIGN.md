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


## 14. Bottom Death Boundary

The lower edge of the playable map is a lethal fall boundary.

If a Gear falls below the defined world-bottom / death line:

- that Gear is eliminated
- it does not continue moving below the map
- the server resolves the elimination authoritatively

This rule applies regardless of remaining HP unless a future explicit rule says otherwise.

### Spawn Safety

Initial spawn candidates MUST NOT be placed too close to the bottom death boundary.

Each spawn candidate must:

- sit on stable terrain
- have enough vertical safety margin below the Gear
- avoid locations where a small movement or minor terrain loss would cause an unavoidable immediate fall
- remain usable for both Scout and Heavy Gear

Define a configurable minimum safety distance such as:

- SPAWN_BOTTOM_SAFE_MARGIN

The exact value may be tuned later.

### Stage Authoring Rule

When creating future stages:

- do not use very low ledges as normal initial spawn candidates
- reserve risky lower ledges for mid-match movement / combat choices
- keep initial spawn slots on stable, readable platforms
- ensure terrain destruction near a spawn does not make an immediate unavoidable fall likely at match start

The visual stage art and spawn guide must respect this rule.

## 15. Fall and Terrain Consistency

A Gear may fall because:

- supporting terrain is destroyed
- movement carries it off a ledge
- gameplay displacement causes it to lose support

The server determines whether the Gear crosses the lethal bottom boundary.

Camera zoom or visual scaling must not change the death boundary.


## 16. Parallax Scrolling

Hangfire uses horizontal parallax scrolling.

When the camera moves left or right:

- Foreground terrain moves at the camera's primary world rate
- Background moves in the same direction but at a slower apparent rate
- The difference in motion helps the player visually separate the playable terrain from distant scenery

This is not only decorative.

Its gameplay / UI purpose is to make the structure of the main playable field easier to recognize.

### Visual Priority

The foreground terrain is the gameplay-critical layer.

The background must not compete with it.

Recommended behavior:

- foreground: 1.0x camera-relative movement
- background: configurable slower factor, e.g. BACKGROUND_PARALLAX_FACTOR < 1.0

Exact values are tunable.

### Readability Rule

Parallax must preserve:

- clear terrain edges
- readable ledges
- readable gaps
- readable firing surfaces
- distinction between decorative background geometry and collidable foreground terrain

Background elements must never visually imply solid collision where none exists.

### Zoom Interaction

Zoom changes the camera view only.

Parallax should remain consistent during zoom and pan.

Zoom must not cause the background and foreground to drift out of logical alignment in a way that confuses the player about playable terrain.

## 17. Camera Readability Goal

Camera movement and parallax together should make it immediately clear which layer is:

- playable terrain
- non-collidable distant background
- temporary visual effect

The player should be able to understand the main field structure through motion contrast even when the stage contains visually dense industrial scenery.


## 18. Experimental Three-Layer Parallax

Prototype visual experiment:

- Far Background
- Mid Background
- Playable Foreground Terrain

The destructible / collision representation remains separate from these visual layers.

This three-layer visual model is EXPERIMENTAL.

Purpose:

- improve depth perception
- make playable terrain easier to distinguish through relative motion
- preserve a modernized 2D artillery presentation

However, visual simplicity has higher priority than extra depth.

If playtesting shows that the mid-background layer makes the stage visually busy or makes terrain harder to read, the prototype may revert to a simpler two-layer presentation:

- Background
- Playable Foreground Terrain

No gameplay rule depends on the presence of the mid-background layer.

Recommended relative motion concept:

- Playable Foreground: 1.0x
- Mid Background: slower than foreground
- Far Background: slower than mid background

Exact parallax factors are tunable.

## 19. Wind Readability Through Ambient Motion

Wind must be readable not only through UI indicators but also through moving environmental objects.

Examples by stage theme:

- outdoor / ruins: leaves, dust, paper scraps, grass particles
- desert / industrial: dust, ash, light debris
- snow / ice: snow particles
- space / low-atmosphere fantasy: small meteor fragments, drifting debris, particles

These objects visually communicate:

- wind direction
- relative wind strength

### Wind Motion Rule

Ambient wind objects:

- move consistently with the authoritative wind direction
- move faster / denser / more strongly under stronger wind
- remain visual-only
- do not collide with Gear
- do not damage terrain
- do not affect projectile physics directly

Projectile physics still uses the authoritative server wind value.

### Readability Goal

The player should be able to estimate wind direction and rough strength from the game scene even before reading a numeric indicator.

The visual motion must not be so dense that it obscures:

- Gear
- projectile
- terrain edge
- spawn / team markers
- damage state

### Theme Independence

The visual carrier of wind may change by stage theme, but the underlying wind system remains the same.

Do not create different wind physics merely because a stage uses leaves, dust, snow, or space debris.

### Optional Simplification

If ambient wind objects create excessive visual noise on a stage, reduce:

- count
- size
- opacity
- animation frequency

before removing the wind readability concept entirely.
