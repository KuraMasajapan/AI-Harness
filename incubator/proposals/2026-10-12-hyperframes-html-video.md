# HyperFrames — HTML to video

- Recorded: 2026-10-13 (source review: 2026-10-12)
- Source: https://github.com/heygen-com/hyperframes
- Status: KNOWLEDGE / VERIFICATION CANDIDATE
- Implementation: HOLD (not approved)
- Evidence boundary: public project documentation; no local execution, independent audit or benchmark reproduction

## Overview
Renders HTML/CSS/media and seekable animations into video with local tooling.

## AI-Harness relevance and constraints
Potential future educational animations and product demos. Evaluate rendering dependencies and output fidelity only when needed. HOLD.

## Next step
Revisit only when relevant to a concrete project need. Compare with existing components and verify original source before promoting to implementation. Preserve this note for Obsidian semantic retrieval.

## Follow-up review — multi-tool motion design workflow (2026-10-22)

- Trigger: user-shared social post claiming a 15-minute Claude Code motion-design studio using HyperFrames, Remotion, GSAP, LottieFiles, and Blender MCP.
- Decision: **CANDIDATE (research only)**; **implementation HOLD**. No install, integration, autonomous scheduling, or change to sealed/Core/Trinity behavior authorized.
- Evidence level: repository metadata and README inspection as of 2026-10-22. No local execution, rendered MP4 comparison, security audit, or cost benchmark.

### Primary-source verification

| Component | Official source | Verified role / scope |
| --- | --- | --- |
| HyperFrames (HeyGen) | https://github.com/heygen-com/hyperframes | Open-source HTML/CSS/media/seekable-animation to deterministic MP4 rendering; CLI and agent skills; README documents Claude Code plugin installation and support for Codex and other coding agents. GitHub metadata showed **68,983 stars** at review time (snapshot, not permanent). |
| Remotion Agent Skills | https://github.com/remotion-dev/skills | Official Remotion agent skills for React-based video creation, previews, rendering, captions, and related workflows. |
| GSAP | https://github.com/greensock/GSAP | JavaScript animation library with timelines and visual motion tooling. Licensing and use conditions must be reviewed for the intended use; do not infer unrestricted use from a social post. |
| LottieFiles Motion Design Skill | https://github.com/LottieFiles/motion-design-skill | AI-agent guidance for timing, easing, choreography, UI motion principles, and quality review; guidance, not an independent rendering engine. |
| MCP for Blender | https://github.com/ahujasid/mcp-for-blender | Third-party (not Blender-official) MCP integration for Blender scene manipulation, materials, rendering/visual verification, and Python execution. README documents both Claude Code and Codex setup. Repository was renamed from blender-mcp. |

### Claim boundaries

**Verified from source documentation:** HyperFrames can render HTML-based animations to MP4; agent plugin/skills workflows exist; Remotion, GSAP, LottieFiles, and Blender MCP repositories exist and offer the described categories of capability. HyperFrames documents planning, lint, preview, and rendering as part of its agent workflow.

**Not independently verified:** that the full five-tool stack reliably installs in 15 minutes; that a single prompt always produces a professional-quality finished video; that the entire workflow checks every frame before display; that a weekly /schedule command will work in every environment or safely wait for approval; that all usage is cost-free. Distinguish documented features from reproducible end-to-end behavior.

### AI-Harness fit and overlap

- Potential concrete applications: short demos for JARVIS Soul UI, growgle service introductions, NISA Scout explanation clips, and educational motion assets. These are **possibilities**, not approved requirements.
- Prefer a minimal standalone HyperFrames trial over immediately stacking five integrations. Compare output quality, reproducibility, render time, compute usage, and operator workload against existing HTML/CSS animation or Remotion-only approaches.
- The proposed agent pipeline (brief -> storyboard/plan -> assets -> animation -> preview/quality check -> MP4 -> human approval) is relevant to AI-Harness workflow and evaluation design; avoid duplicating existing Codex/Work capabilities without measurable benefit.
- Existing 2026-10-12 HyperFrames note is the canonical candidate; this review expands it rather than creating a duplicate.

### Safety and cost gates

- Do **not** run remote shell installers blindly (e.g. `curl ... | sh` or PowerShell `irm ... | iex`). Inspect pinned versions, source, permissions, and installer effects first; favor manual/least-privilege setup.
- Treat third-party skills and MCP servers as untrusted code/instructions until reviewed. Blender MCP can execute Python and manipulate local scenes/files; require sandboxing, restricted file/network permissions, and human approval for side effects.
- Distinguish free/open-source renderer components from AI-model/API charges, optional hosted rendering, licensed assets, and local GPU/CPU costs.
- Do not enable autonomous recurring production, publishing, or cloud upload during research. Keep human review before any outward-facing artifact.

### Proposed minimal verification (NOT STARTED)

1. Define a small, reproducible 5–10 second demo and acceptance criteria; inventory dependencies and licensing.
2. Review HyperFrames source/install path and run only in an isolated test workspace after separate human approval.
3. Generate MP4 locally; capture runtime, output size, frame correctness, deterministic re-render behavior, and failures.
4. Compare with a baseline (manual HTML animation or Remotion-only) and decide **PROMOTE / HOLD / REJECT** based on measured benefit.
5. Add GSAP/LottieFiles/Blender only if a specific quality or capability gap remains.

**Current disposition:** retain as **CANDIDATE / HOLD** in Proposal Incubator. This record is knowledge capture only, not authorization to implement.
