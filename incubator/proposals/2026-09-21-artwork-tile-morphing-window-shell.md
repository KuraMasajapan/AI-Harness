---
status: proposal
created: 2026-09-21
origin: desktop visual shell / spatial notebook UI discussion
---

# Artwork Tile Morphing Window Shell

## Concept

Desktop-facing entry points should not look like ordinary application icons.

Each tool appears as a visually consistent rectangular or square tile using a selected artwork image (for example, a classical painting or another curated image set).

The artwork is a cover layer only.

When the user activates a tile, the tile visually transforms into the application window rather than abruptly opening a separate UI.

## Intended transition

```text
ARTWORK TILE
→ click / tap
→ tile lifts to foreground
→ tile expands toward target window rectangle
→ artwork gradually fades
→ application chrome/content gradually appears
→ expansion completes
→ normal familiar application window is fully visible
```

Closing can optionally run the exact reverse transition:

```text
normal window
→ content/chrome fades
→ window contracts toward its source tile
→ artwork fades back in
→ tile restored
```

## UX goals

- consistent desktop appearance
- ordinary tools hidden behind a calm visual vocabulary
- playful / memorable interaction
- no need for users to learn a novel application UI after opening
- preserve familiar window behavior once transition finishes

## Recommended shell architecture

Prefer a dedicated launcher/shell layer rather than modifying Windows desktop icons directly.

Possible structure:

```text
Desktop
  ↓
HARNESS visual launcher / shell
  ├─ artwork tile A
  ├─ artwork tile B
  └─ artwork tile C
        ↓ activate
transition overlay / shared visual proxy
        ↓
real application window or local HARNESS panel
```

A transition proxy can animate between the tile rectangle and final window rectangle, which avoids depending on whether the OS-native window itself can be animated smoothly.

## Visual specification draft

### Tile state
- fixed family of aspect ratios
- artwork edge-to-edge
- little or no visible app chrome
- optional small title on hover/focus
- subtle selection/focus indication
- no desktop-icon-style labels unless requested

### Opening state
- source tile remains visually anchored
- animation begins from its exact screen rectangle
- scale + position animate together
- artwork opacity decreases during expansion
- application surface opacity increases after expansion has clearly begun
- final state becomes visually indistinguishable from an ordinary window

### Suggested motion
- target duration: roughly 350–500 ms
- ease-out for opening
- ease-in/ease-out for reverse close
- avoid bounce unless explicitly chosen as part of the visual identity
- respect reduced-motion setting with a short crossfade/no zoom fallback

## State rules

Each tile needs:
- tile ID
- application/board target
- artwork reference
- last window position
- last window size
- open/closed state
- optional source board/context

If the application was previously positioned elsewhere, the transition can target its remembered rectangle.

## Multi-window behavior

Options to decide later:

A. One tile = one window instance.
B. One tile can open several windows.
C. One tile opens a single shell that can host multiple internal boards.

Default recommendation for simplicity:
One tile = one persistent tool/shell window, with internal navigation.

## Accessibility and failure behavior

- keyboard activation must work
- focus indicator must remain available
- reduced-motion mode must disable large zoom motion
- if the target app fails to open, the tile must return to its resting state
- transition must never leave an invisible blocking overlay
- artwork must not be required to identify the tool; name/accessible label remains available

## Relation to the Reference-First Spatial File Notebook

The Spatial File Notebook can use this shell as its desktop entry point:

```text
artwork tile
→ morph open
→ normal notebook window
→ boards / inbox / file references
```

The visual shell is therefore reusable for other HARNESS tools as well.

## Why preserve this proposal

This provides a consistent, intentionally designed desktop layer without forcing every underlying tool to adopt a custom interface.


## Window surface: lightweight canvas texture

Once the morph transition completes, the opened window should keep a familiar application layout but use a subtle canvas-cloth visual treatment.

Goal:
- tactile and warm rather than glossy
- visually unified with the artwork-tile launcher
- light enough not to hurt responsiveness
- texture should sit behind ordinary controls, not compete with them

Recommended implementation direction:
- use a lightweight CSS/procedural texture or a very small repeating local texture asset
- avoid large background images, blur-heavy effects, continuous animation, or GPU-expensive filters
- keep the central working area bright and readable
- use restrained paper/canvas grain at low opacity
- preserve normal window chrome and predictable controls
- allow the texture layer to be disabled independently if performance or readability suffers

The visual hierarchy should remain:

```text
artwork tile
→ morph transition
→ familiar window structure
→ subtle canvas texture as atmosphere
→ practical content remains dominant
```

This keeps the opening playful while keeping long work sessions calm and familiar.


## Flat line-based canvas treatment

Avoid simulated depth as the default visual language.

Use thin linework and spacing to suggest structure:

- 1px hairline borders
- slightly darker/lighter nested rectangles
- restrained separators instead of shadows
- no bevels, glossy highlights, or heavy gradients
- subtle canvas texture remains in the background
- panels should feel drawn onto the canvas rather than floating above it
- selected/focused states can use a clearer outline instead of drop shadows

Target impression:

```text
flat
+ tactile background
+ precise linework
+ generous spacing
= elegant, lightweight, calm
```

This also reduces rendering cost and keeps the visual system consistent with the lightweight requirement.
