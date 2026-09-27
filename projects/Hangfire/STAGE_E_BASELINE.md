# Hangfire — Stage E Prototype Numeric Baseline

Status: PROVISIONAL
Date: 2026-09-27

This document turns the accepted Pattern E visual direction into a concrete implementation-ready baseline.

It does not start the Stage implementation layer.
It only freezes a provisional numeric target so Codex can later implement from explicit values.

## World

- Viewport: 1280 x 720
- World: 1920 x 720
- Horizontal world size: 1.5x viewport width
- Bottom death line: y = 720
- Terrain model: single continuous 2D surface

## Camera

- Edge pan trigger margin: 48 px
- Edge pan speed: 600 px/s
- Default zoom: 1.0x
- Minimum zoom: 0.8x
- Maximum zoom: 2.0x
- Current Gear follow: enabled
- Projectile follow: enabled

These are prototype values and may be tuned after desktop playtest.

## Parallax

- Foreground: 1.00x
- Mid background: 0.55x
- Far background: 0.25x

The middle layer remains experimental.
If field readability gets worse, disable it and fall back to a two-visual-layer presentation.

## Wind Visual Layer

Placement:

Foreground
→ wind visual objects
→ Mid Background
→ Far Background

Only one reusable wind-object sprite is required.

- right-moving form
- horizontally mirrored left-moving form

Direction and speed come from the authoritative wind state.
Visual wind objects have no collision and no gameplay effect.

Prototype base visual speed: 80 px/s before wind-strength scaling.

## Spawn Candidates

Exactly 12 candidate points.

The 12 x/y entries in `stage.json` are provisional authoring guides.

Important:

- The final Y position must be snapped to the actual terrain surface.
- No two candidates should form stacked upper/lower playable lanes.
- Every point must sit on the same single-surface 2D field.
- Minimum horizontal guide spacing: 110 px.
- Bottom death safety guide: 180 px.
- Random assignment is server authoritative.
- Teams are not separated left/right.

## Assets

```text
projects/Hangfire/stages/pattern_e/
├─ stage.json
├─ background_far.png
├─ background_mid.png
├─ foreground.png
├─ mask.png
└─ wind_object.png
```

Only `stage.json` is being committed now.
The image assets are future implementation assets.

## Tuning Rule

These values are not sacred.

After the first playable implementation, Human playtest may request relative changes such as:

- Stage width +20%
- Zoom max 1.6x
- Edge pan slower
- Mid background motion reduced
- Spawn 7 moved right
- Bottom safety margin increased

Accepted tuned values then become the new Source of Truth.
