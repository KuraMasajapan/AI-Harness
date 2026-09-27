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

### Approved core assets — 2026-09-28

The Human-approved Stage E core images are placed in `stages/pattern_e/`:

- `foreground.png`: approved foreground terrain, 1920 × 720 RGBA.
- `mask.png`: matching terrain mask, 1920 × 720, 8-bit grayscale.
  White (255) means destructible / collidable terrain; black (0) means empty space.

These files are the core asset Source of Truth. `stage.json` already references them
through `assets.foreground` and `assets.collisionMask`, relative to its directory.
Checksums are recorded in the accompanying `ASSET_MANIFEST.txt` and were verified
against both files. The mask contains only 0 and 255 across all 1,382,400 pixels.
No image regeneration, processing or resizing was performed during verification.

This confirmation covers only the foreground and mask. Other asset names above
remain separate references; this does not approve them or implement stage loading,
terrain destruction, spawn snapping or Layer 5.

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
