---
status: research_candidate
date: 2026-11-18
source_post: https://x.com/yarad_ai/status/2122387704641986823
source_repository: https://github.com/EL4CTEO/blender-skills
upstream_commit_checked: 9e7e04a603c125a0d174
stage_1_rank: A+
stage_2_rank: A
decision: CANDIDATE
implementation: HOLD / NOT_IMPLEMENTED
evidence: "GitHub upstream repository, code, CI configuration and recent run results inspected; independent local Blender production test NOT performed"
tags: [blender, 3d, agent-skills, codex, modeling, rigging, animation, asset-qa, glb, threejs, muse, security, comparison]
---

# Blender Agent Skills (28 skills) — evaluation and comparison against AI-Harness proposals

## 0. Scope and disposition

Human-provided source: https://x.com/yarad_ai/status/2122387704641986823 . Research performed 2026-11-18. This is a **research-only record**: no Skill installation, no execution of third-party code, no modifications to existing projects/Core/Skills/TRINITY, and no approval to promote or adopt.

- **Stage 1 A+**: strong potential usefulness for Blender + Codex + Three.js 3D production.
- **Stage 2 A**: tangible scripts, testing and QA, but young repository, third-party execution risk, no independent local benchmark, and partial overlap with existing proposals.
- **Decision CANDIDATE / implementation HOLD**.
- Best-fit application: 3D small room / agent avatar, including furniture, material work, custom rig, animation, GLB export, and performance optimization.
- Conditional application: UIAP BASE appearance mockups (not engineering/manufacturing CAD).
- Poor immediate fit: Hangfire's present custom Canvas 2D game.

## 1. Verified upstream facts and limitations

- Repository: https://github.com/EL4CTEO/blender-skills ; author-owned individual GitHub repository, **not established as an official Blender Foundation / Blender development team product**. Any social post suggesting official Blender authorship is **UNVERIFIED** and must not be repeated as fact.
- Repository created 2026-10-14; latest examined commit 9e7e04a603c125a0d174 (2026-11-17); latest release observed v1.3.2, fixing dense-mesh rig checking.
- README documents **28 Blender agent skills** for Claude Code, Codex, OpenCode, Gemini CLI, GitHub Copilot and Cursor, designed for Blender **5.2 LTS+**, claimed verified on 5.3.
- License: root MIT. Confirm license applicability of any additional bundled assets before distribution.
- Source tree: 266 entries when checked, 28 SKILL.md files, task scripts, test suite, and installer scripts.
- `.github/workflows/ci.yml`: checks metadata/scripts/install and runs Blender headless tests in matrix **5.2.3 and 5.3.0**; GPU rendering tests skipped by BAS_SKIP_GPU=1 on CI. Recent push CI for 2026-11-17 commit showed **success**; this does not establish real-world visual quality, security, or compatibility with the user's particular scene.
- README claims 67 headless Blender tests and provides a with/without comparison page; neither claim constitutes independent measured improvement. No local benchmark was run during this research.
- `blender-core` supports Blender via optional MCP or headless local CLI; **MCP is not mandatory**. Python runner `skills/blender-core/scripts/run_in_blender.py` locates Blender and launches subprocess. An external cloud API is not inherently required for the baseline workflows, but model/tool runtime and external asset providers may carry separate costs.
- Example verified skill files: `blender-core`, `blender-scene-setup`, `blender-geometry-nodes`, `blender-character-rigging`, `blender-hair-grooming`, `blender-game-optimization`, `blender-export-pipelines`, `blender-asset-qa`, `blender-workflow-recipes`.
- `blender-asset-qa` documents checks for z-fighting, detached/floating parts, normals, non-manifold geometry, degenerate faces, UVs, skin weights, materials, textures, and multi-angle visual review. Some subjective issues (proportions, intersections, deformation) still require visual inspection.
- Character rigging is human-oriented by default (Rigify/basic_human). Unusual mascot/animal anatomy and fur may require manual skeleton, weight, topology and export adaptation. Automated success is **not verified**.
- `blender-workflow-recipes` covers a game-ready asset pipeline, AI/downloaded asset cleanup, character-to-rig-to-animation, web/AR export and QA gates.

## 2. Full upstream skill catalog (README)

1. blender-core — execution/routing/API
2. blender-scene-setup — scene units, collections, naming, audit
3. blender-hardsurface-modeling — bevel/boolean/weighted normals
4. blender-sculpting — organic sculpting
5. blender-retopology-uv — retopology, UV, texel density
6. blender-pbr-materials — physically based materials
7. blender-texturing — wear, grime, decals
8. blender-texture-baking — normal/AO/curvature/ORM maps
9. blender-geometry-nodes — procedural geometry
10. blender-character-rigging — Rigify/weights/skeleton
11. blender-facial-shapekeys — visemes, blendshapes
12. blender-animation — animation, retargeting, loops
13. blender-clothing — garments
14. blender-hair-grooming — hair, fur, hair cards
15. blender-game-optimization — triangle budgets, LODs
16. blender-export-pipelines — glTF/GLB, FBX, USD etc.
17. blender-rendering — rendering batches
18. blender-lighting-lookdev — HDRI, turntables
19. blender-stylized-npr — toon/stylized rendering
20. blender-environment-kits — terrain/scattering
21. blender-video-editing — VSE, camera tracking
22. blender-simulation — physics/simulation
23. blender-time-of-day — lighting/time mood
24. blender-weather-fx — rain/snow/wetness
25. blender-addon-development — Blender extensions
26. blender-pipeline-automation — batch conversion
27. blender-asset-qa — geometry/material/rig QA
28. blender-workflow-recipes — end-to-end playbooks

## 3. Relative priority for the 3D small room / avatar

| Skill | Purpose | Priority |
|---|---|---|
| blender-core | Codex headless Blender task entry | HIGH |
| blender-scene-setup | Room/furniture scene organization | HIGH |
| blender-geometry-nodes | Procedural room props/environment | HIGH |
| blender-pbr-materials | Furniture/fabric/metal material quality | HIGH |
| blender-character-rigging | Custom character skeleton | HIGH, conditional on anatomy |
| blender-animation | Idle/walk/pose clips | HIGH |
| blender-hair-grooming | Fur/hair, potentially hair cards | HIGH but performance-sensitive |
| blender-game-optimization | Browser/Three.js triangle/LOD budget | HIGH |
| blender-export-pipelines | GLB/glTF for Three.js | HIGH |
| blender-asset-qa | Mesh, UV, weight, export checks | HIGH |
| blender-workflow-recipes | Reusable end-to-end sequencing | REFERENCE; read only as needed |

These are **priority candidates, not a recommendation to install all eleven**. First pilot should use only `blender-core`, `blender-scene-setup`, `blender-asset-qa`.

## 4. Comparison with current development/incubator/proposals

| Existing proposal | Existing role | Relationship to Blender Agent Skills | Decision |
|---|---|---|---|
| `2026-10-22-spline-chatgpt-codex-3d-workflow.md` | Spline editable interactive 3D scenes, UIAP BASE visual mockups | PARTIAL OVERLAP. Spline is an interactive editor/service; Blender skills are local Blender production workflows and asset pipeline. Can complement each other; compare on artifact editability, export and external service requirements | Preserve both; do not replace |
| `2026-10-24-hermes-plugins-official-jev-voice-gameforge-botforge.md` | Hermes plugins, GameForge game generation/automated playtesting, official plugins catalog mentions Blender | COMPLEMENT. GameForge's gameplay testing and project generation differs from specialized Blender modeling/rig/QA | Preserve both |
| `2026-11-18-hangfire-game-dev-skills-catalog.md` | Canvas 2D game skills, pixelfx, game-feel, UI/UX, selective skill router | DIFFERENT DOMAIN. Blender 3D pipeline not currently needed for Hangfire; do not treat a low Hangfire score as low general value | No Hangfire integration |
| `2026-10-23-ui-ux-pro-max-skill-reassessment.md` | UI design intelligence | COMPLEMENT. UI decisions vs 3D asset production | No replacement |
| `2026-10-15-ui-design-skill-component-comparison-prep.md` | UI design skill/component comparison | COMPLEMENT. Not a 3D Blender pipeline | No replacement |
| `2026-10-26-addyosmani-agent-skills-evaluation.md` | Cross-agent coding procedures, verification gates | PROCESS OVERLAP (QA/checkpoint philosophy), not functional Blender duplication | Reuse existing verification principles |
| `2026-10-12-mattpocock-skills-engineering.md` | Composable general coding skills | Only generic composability overlap | No replacement |
| `2026-10-27-huashu-design-skill-candidate.md` | General design/brand/prototype | Mostly different outputs | No replacement |

The development tree was checked for filename-level existing Blender proposals; no Blender-specific proposal was found before this record. Do not interpret this as exhaustive semantic deduplication of all historical/unindexed material.

## 5. Security, stability, cost and execution boundary

- **Young project**: created 2026-10-14; popularity, recent CI success and MIT license do not demonstrate long-term maintenance, full supply-chain safety or reliable output quality.
- **Installer overwrite hazard**: `install/install.sh` uses `rm -rf` on destination skill names before link/copy; `install/install.ps1` deletes existing same-name skill targets before copy/junction. Default user-scope paths include `~/.claude/skills` and `~/.agents/skills`. **Never execute the default installer without auditing and backing up the exact target**. Use isolated project scope and explicit `--skills` / `-Skills` allowlist, or manually review/copy a single skill. Pin reviewed commit SHA; check contents, scripts, dependencies, output paths, permissions and side effects.
- **Agent instruction boundary**: third-party `SKILL.md` and scripts are lower-trust input; do not permit them to override AI-Harness Human approvals, Source of Truth, repo rules, or file/network privileges. External scripts are executable code, not harmless reference text.
- **Data boundary**: prefer local Blender headless CLI; optional MCP and external assets/services need separate security and data-flow checks. Avoid exposing private models, credentials and private repository contents to unreviewed endpoints.
- **Output integrity**: create backups; avoid destructive `--fix` or output overwrites until verified; require QA plus visual review, GLB re-import, scale/rig/animation checks and Three.js runtime check.
- **Cost**: MIT software and local Blender workflows can avoid paid 3D SaaS, but computing, AI tokens, rendering and optional services remain costs. No measured cost/time savings are available.

## 6. Proposed controlled A/B trial (NOT AUTHORIZED / NOT RUN)

1. Freeze the same simple room furniture asset specification, target triangle count, materials and GLB export requirements.
2. Baseline A: existing Codex + Blender workflow without third-party skills.
3. Candidate B: isolated project-scope `blender-core`, `blender-scene-setup`, `blender-asset-qa` only; exact reviewed commit pin.
4. Record commands, model/token use, wall time, manual interventions, errors, output dimensions, mesh/UV/normal QA, GLB filesize, Three.js rendering/animation integrity and screenshots.
5. Compare **same input and acceptance criteria**, not promotional before/after images.
6. If evidence supports it, expand to `blender-export-pipelines` and `blender-game-optimization`; only later evaluate custom rig/hair.
7. Require fresh Human approval before any install, code execution, existing project edit, external connection or promotion to Skills/Core.

## 7. Evidence references

- https://github.com/EL4CTEO/blender-skills
- https://github.com/EL4CTEO/blender-skills/blob/main/README.md
- https://github.com/EL4CTEO/blender-skills/blob/main/LICENSE
- https://github.com/EL4CTEO/blender-skills/blob/main/install/install.sh
- https://github.com/EL4CTEO/blender-skills/blob/main/install/install.ps1
- https://github.com/EL4CTEO/blender-skills/blob/main/.github/workflows/ci.yml
- https://github.com/EL4CTEO/blender-skills/blob/main/skills/blender-core/SKILL.md
- https://github.com/EL4CTEO/blender-skills/blob/main/skills/blender-asset-qa/SKILL.md
- https://github.com/EL4CTEO/blender-skills/blob/main/skills/blender-workflow-recipes/SKILL.md
- https://github.com/EL4CTEO/blender-skills/releases/tag/v1.3.2
- https://github.com/EL4CTEO/blender-skills/commit/9e7e04a603c125a0d174

**Evidence status:** public source/CI reviewed; no independent execution, performance benchmark, third-party security audit, or production-grade output quality verification. No implementation decision.
