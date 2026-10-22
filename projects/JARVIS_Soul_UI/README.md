# Local AI Soul UI

This directory contains the visual research that led to the Local AI Soul V0.1 product direction.

## Current implementation direction

The implementation target is now defined in:

- [V0.1 Product Specification](V0.1_SPEC.md)

V0.1 uses an external OSS Orb component as the primary renderer and focuses on product integration, setup UX, text/voice interaction, Semantic Reflex, safety, and reliable fallback behavior rather than further development of the custom renderer.

## Existing v0.2 prototype — retained research asset

The previous Local AI Soul UI v0.2 is preserved as an independent visual prototype.

It explored:

- WebGL2 local glow + Canvas 2D flow lines and particles
- Canvas 2D fallback
- Eco / Balanced / High drawing modes
- Ready / Listening / Processing / Speaking / Attention demo states
- reduced-motion, responsive layout, and keyboard-accessible controls

The prototype does **not** include live AI connection, microphone permission handling, STT/TTS, or real CPU/VRAM measurement.

The existing source files and previews remain useful as research history and are not deleted by the V0.1 product decision.

## v0.3 experiments

The `experiments/v0.3/` work is also retained as renderer research.

V0.1 does not promote that custom renderer into the product. The product direction instead adopts the external Orb implementation documented in `V0.1_SPEC.md`.

## Historical prototype launch

For the retained v0.2 prototype:

```powershell
cd C:\Users\Owner\Documents\ChatGPT\UI_develop_lab\local-ai-soul-ui
python -m http.server 8000
```

Open `http://localhost:8000/`.

`file://` direct opening is not the intended verification path because of ES module constraints.

## Preview records

[Preview images and results](docs/previews/README.md)

## Note on naming

The directory name `JARVIS_Soul_UI` is retained as a legacy internal project path for continuity. It is not the default assistant name or final public product brand. In V0.1, the user chooses the assistant's display name during first-run setup.
