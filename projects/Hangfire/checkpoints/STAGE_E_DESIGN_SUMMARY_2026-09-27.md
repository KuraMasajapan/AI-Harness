# Hangfire — Stage E Design Summary

Status: RECORDED
Date: 2026-09-27

This document summarizes the currently accepted Stage E design decisions.
It is a checkpoint / handoff summary, not a new gameplay layer implementation.

## 1. Stage Identity

- Baseline: Pattern E
- Viewport target: 1280 x 720
- World target: 1920 x 720
- Horizontal scrolling required
- Entire battlefield is not shown at once
- Stage is a single continuous 2D playable surface
- No stacked upper/lower playable lanes
- No floating independent walkable platforms
- No pseudo-3D playable depth planes

The player fights along the upper contour of one horizontally extended destructible landmass.

## 2. Playable Terrain

The stage is separated conceptually into:

- Far Background
- Mid Background
- Wind Visual Layer
- Playable Foreground Terrain
- Authoritative Collision / Destruction Representation

Only the Playable Foreground Terrain is walkable / collidable.

The collision / destruction representation is authoritative and may be separate from the visible foreground artwork.

## 3. Parallax

Parallax is used not only for visual depth but also to help players recognize the playable terrain structure.

Prototype values:

- Foreground: 1.00x
- Mid Background: 0.55x
- Far Background: 0.25x

The Mid Background layer is experimental.

If it makes the stage visually busy or reduces terrain readability, it may be disabled and the stage may fall back to:

- Background
- Playable Foreground

No gameplay rule depends on the mid-background layer.

## 4. Wind Visualization

The wind visual layer sits between the Playable Foreground and Mid Background.

Use one reusable small moving object sprite.

- one base visual object
- opposite direction may use horizontal mirror
- direction follows authoritative wind direction
- visual speed scales with wind strength
- density may also scale with wind strength
- visual only
- no collision
- no damage
- no direct physics effect

Prototype base visual speed:

- 80 px/s before wind-strength scaling

The visual object should remain small so it reads as ambient motion, not as a foreground obstacle.

Stage theme may change the visual carrier later, but the underlying wind system remains the same.

## 5. Spawn Model

Prototype uses exactly 12 valid spawn candidate points.

Rules:

- active players: 2 / 4 / 6 / 8
- server selects only the required number of spawn candidates
- assignment is randomized server-side
- teams are NOT separated left/right
- allies and enemies may start intermixed
- no duplicate spawn occupancy
- spawn must be on stable terrain
- spawn may not be inside terrain
- spawn may not be outside world bounds
- spawn may not be on stacked alternate playable lanes
- spawn candidate positions must all lie on the same single-surface 2D field

Prototype guide spacing:

- minimum horizontal spacing: 110 px

The current 12 x/y coordinates in `stages/pattern_e/stage.json` are authoring guides.
Final Y positions must be snapped to the actual foreground terrain surface / mask.

## 6. Bottom Death Boundary

The lower edge of the world is a lethal fall boundary.

Prototype value:

- deathY = 720

If a Gear falls below the defined bottom death line:

- that Gear is eliminated
- remaining HP does not prevent the fall elimination
- server resolves elimination authoritatively

Initial spawn candidates must keep a safety margin from the bottom death boundary.

Prototype guide:

- SPAWN_BOTTOM_SAFE_MARGIN = 180 px

Very low or fragile ledges may exist as mid-match tactical positions but should not be normal initial spawn candidates.

## 7. Camera Controls

Desktop prototype camera:

### Edge Pan

Moving the mouse cursor near a screen edge pans the camera in that direction.

The cursor does not need to touch the absolute outermost pixel.

Prototype values:

- EDGE_PAN_MARGIN = 48 px
- EDGE_PAN_SPEED = 600 px/s

Camera remains inside world bounds.

### Mouse Wheel Zoom

Mouse wheel controls zoom.

Prototype values:

- default: 1.0x
- minimum: 0.8x
- maximum: 2.0x

Zoom is intentionally useful for inspecting tiny terrain residue near the active Gear before firing.

Zoom is visual-only and does not alter:

- projectile physics
- collision
- terrain state
- damage
- authoritative positions

## 8. Tiny Terrain Residue

Extremely small remaining terrain pixels after destruction are accepted prototype behavior.

The system does not need to clean every isolated pixel.

However:

- authoritative collision must remain consistent
- intentionally invisible collision should not be introduced
- player zoom is available for close inspection

## 9. Camera / Scene Readability

The camera should prioritize:

1. current Gear inspection
2. manual battlefield navigation
3. projectile tracking
4. low implementation complexity

Do not add at this stage:

- minimap as a required gameplay feature
- drag-to-pan
- cinematic camera system
- advanced camera editor

## 10. Stage Asset Package

Planned package:

```text
projects/Hangfire/stages/pattern_e/
├─ stage.json
├─ background_far.png
├─ background_mid.png
├─ foreground.png
├─ mask.png
└─ wind_object.png
```

Repository state confirmed on 2026-09-28:

- `stage.json` remains the provisional numeric baseline.
- PR #6 merged `foreground.png`, `mask.png`, `background_far.png` and
  `background_mid.png` into `development`; all four images are Git-tracked.
- `foreground.png` and `mask.png` are 1920 × 720.
- `mask.png` contains only 0 and 255 and is the authoritative asset for terrain
  collision / destruction: white (255) is terrain; black (0) is empty space.
- `background_far.png` and `background_mid.png` are visual-only, not collision sources.

This records asset availability only; it does not start Layer 5 or terrain destruction implementation.

## 11. Prototype Numeric Baseline

Current provisional values:

- viewport: 1280 x 720
- world: 1920 x 720
- death line: y = 720
- edge pan margin: 48 px
- edge pan speed: 600 px/s
- zoom: 0.8x to 2.0x
- parallax: 1.00 / 0.55 / 0.25
- spawn candidates: 12
- spawn bottom safety margin: 180 px
- spawn horizontal guide spacing: 110 px
- wind visual base speed: 80 px/s

These are tuning seeds, not permanent sacred values.

## 12. Explicit Non-Goals

Do not add during this stage-design phase:

- stage-specific gameplay modifiers
- scripted hazards
- environmental damage
- moving platforms
- multiple playable vertical lanes
- floating walkable platforms
- heavy post-processing
- complex shader-based terrain systems

The immediate goal is a readable, destructible, scrollable single-surface battlefield.

## 13. Current Handoff State

Stage E design is sufficiently defined for later implementation handoff.

Before implementation:

1. finalize the actual foreground terrain silhouette
2. snap all 12 spawn Y positions to the final terrain surface
3. derive / prepare the authoritative destruction mask
4. prepare far background, optional mid background, foreground and wind-object assets
5. preserve the single-surface 2D terrain rule
6. preserve bottom-death spawn safety

The stage implementation should not start ahead of the approved Hangfire layer order unless Human explicitly changes the order.
