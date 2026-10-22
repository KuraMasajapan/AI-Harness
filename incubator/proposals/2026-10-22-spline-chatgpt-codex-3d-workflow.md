# Spline for ChatGPT / Codex — interactive 3D creation workflow

- Recorded: 2026-10-22
- Sources:
  - https://x.com/splinetool/status/2112940935478956459
  - https://chatgpt.com/plugins/spline
  - https://spline.design/
- Status: **HIGH-PRIORITY CANDIDATE / HIGH INTEREST**
- Implementation: **HOLD until a concrete trial is approved**
- Evidence boundary: official Spline X announcement, official ChatGPT plugin listing, and Spline public site. No hands-on plugin test, export benchmark, or UIAP BASE scene has been created yet.

## Why this is high priority

Spline is unusually relevant because the integration is not just text-to-image or a detached 3D generator. The official ChatGPT plugin page describes an integrated workflow where a 3D scene or object is created in a Spline editor beside the chat, can be watched while it is built, directly edited by a human, iterated through chat, exported, or deployed as a URL.

The official plugin page exposes a complete composition:

```text
ChatGPT / Codex
    ↓
Spline App
    ↓
Spline Skills
    ↓
Spline MCP
    ↓
Editable interactive 3D scene
    ↓
Human visual review / direct manipulation
    ↓
Export / URL deployment
```

This is a strong reference implementation for the AI-Harness pattern:

```text
AI → Tool → Artifact → Human Review
```

## Verified capabilities from the official ChatGPT plugin page

- Create 3D scenes
- Design websites and app screens
- Edit Spline files
- Review scenes with screenshots
- Create editable 3D presentations
- Create simulations
- Create configurators
- Create 3D illustrations and icons
- Create interactive 3D landing pages and experiences
- Direct manipulation in the Spline editor
- Export to other formats
- Deploy content as URLs

Official listing metadata observed on 2026-10-22:

- App: Spline
- MCP server: `https://mcp.spline.design/mcp`
- Category: Creativity
- Version shown: 1.1.0
- Skills include 3D animation, architecture, boolean operations, scene building, game audio/controls, interactivity, materials, particles, physics, procedural generation, scene optimization, state transitions, texture drawing, and related Spline-specific skills.

Treat the plugin page as the source of truth for the current integration surface; availability and version may change later.

## Priority AI-Harness use case — UIAP BASE

**UIAP BASE is the highest-priority concrete trigger for evaluating Spline.**

The project already requires:

- realistic visual mockups before PCB finalization
- physical placement review
- educational explanation of connectors, LEDs, buttons, sockets and signal paths
- a future public 3D model / mechanical interface
- visuals that work for both children and adult makers

Spline may provide a useful layer between flat concept images and manufacturing CAD.

Candidate uses:

1. Build an editable 3D appearance mock of UIAP BASE using the current physical-dimension baseline.
2. Check visual grouping of the central UIAPduino socket, exposed pin sockets, A/B controls, NORMAL/GAME switch, status LEDs, Grove/Qwiic and terminal blocks.
3. Produce child-friendly labeled scenes for documentation and teaching.
4. Add interactive explanations such as click-to-identify parts or animated signal-flow demonstrations.
5. Reuse the scene for web presentation or future video capture.

### Important boundary

Spline is **not** the source of truth for PCB dimensions, electrical rules, routing, footprints, tolerances, or manufacturing output.

Use authoritative UIAP BASE dimensions, drawings, KiCad/CAD data, exact part references, and physical validation for engineering decisions.

Spline should be treated as:

**visual mockup / interactive explanation / communication layer**

—not as manufacturing CAD.

## Recall trigger for UIAP BASE

When work on `projects/UIAPduino/UIAP_BASE.md` enters any of the following areas, recall this proposal before inventing a new visualization workflow:

- realistic external mock image
- 3D board visualization
- component placement presentation
- physical-layout communication
- enclosure / tray / stand visualization
- child-facing interactive teaching material
- connector / LED / button explanation
- signal-flow animation
- product presentation or landing-page 3D
- public 3D demonstration

At that point:

1. Recheck current Spline plugin availability and pricing/export conditions.
2. Use the latest UIAP BASE physical Source of Truth rather than guessed geometry.
3. Decide whether Spline adds value over a static render, KiCad 3D view, or other existing tool.
4. If a hands-on Spline trial would create or modify external data, request Human approval before connecting or writing.
5. Preserve a human-editable artifact and compare visual correctness against the real design.

## Relationship to HyperFrames / Remotion

Potential future pipeline:

```text
UIAP BASE Source of Truth
    ↓
Spline — editable / interactive 3D scene
    ↓
Human review
    ↓
HyperFrames / Remotion — explanatory or promotional video
```

This relationship is promising but not yet validated. Do not create a combined stack unless the concrete output needs it.

## Risks / verification items

- ChatGPT plugin availability may differ by account, rollout, or product surface.
- Pricing, export capabilities, collaboration limits, private-project handling, and deployment limits need current verification before use.
- AI-created 3D geometry can look plausible while being dimensionally wrong.
- Screenshot review does not replace physical-layout or manufacturing verification.
- Large/complex scenes may introduce performance or iteration overhead.
- Do not upload confidential PCB/source material without checking the data boundary and user approval.

## Evaluation

- Novelty: HIGH
- Relevance to AI-Harness: HIGH
- Relevance to UIAP BASE: **VERY HIGH**
- Immediate implementation need: MEDIUM
- Trial priority when UIAP BASE reaches visual mock / physical presentation work: **HIGH**
- Current disposition: **CANDIDATE / HIGH INTEREST / IMPLEMENTATION HOLD**

## Next trigger

Do not install or connect Spline only to satisfy this research note.

**Trigger a trial when UIAP BASE next needs an editable 3D mock, physical-presentation artifact, or interactive teaching scene.**
