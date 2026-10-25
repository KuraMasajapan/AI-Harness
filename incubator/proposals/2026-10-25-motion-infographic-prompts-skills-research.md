# Motion Infographic Prompts & Skills — Research Candidate

- Date: 2026-10-25
- Status: **B / CANDIDATE — Research only / NOT IMPLEMENTED**
- Scope: AI-Harness visual documentation, animated system map (v5), future UI/UX workflows
- Origin: user-supplied X post digest; posts' quotation counts, exact claims, and demonstration outcomes **not independently verified**.
- Source of truth: user-provided digest in the 2026-10-25 conversation; this record is an evaluated summary, not an approved skill.

## Sources and claims (unverified social posts)
1. Sprite sheet → GIF using image generation and frame slicing (reported Quotes 24): https://x.com/shota7180/status/1714099104463368384
2. NotebookLM / infographic style prompting to reduce stereotypical AI aesthetics (reported Quotes 9): https://x.com/ChatgptAIskill/status/2021524633108009186
3. ~40 diagram slash commands, including `/infographic`, `/timeline`, `/flowchart`, `/mindmap`, `/comparison`, `/process`, `/roadmap`, `/explodedview`, `/cutaway`, `/isometric`: https://x.com/xxx_inoue/status/2112697666295705648
4. Claude Code infographic-to-motion prompt, prioritizing preserving original text/colors/data: https://x.com/Grow_withAI/status/2112527071230791866
5. Clean illustrations (avoid unnecessary particles/noise, preserve crisp edges and readability): https://x.com/aiwatap/status/2111016097667588246
6. Remotion sequence-based motion prompt: https://x.com/nasim_haiderQ/status/2112128971462914300
7. Higgsfield Vibe Motion / infographic / bar chart race: https://x.com/namake_neko_ai/status/2021578396346515674

## Verified external technical references
- Remotion supports frame/timeline-based composition and timed sequences; useful for video output, but not necessary for a single offline Safari HTML file: https://www.remotiondocs.com/docs/sequence
- GSAP MotionPathPlugin supports animating objects along SVG paths; dependency/packaging and Safari testing would be needed: https://gsap.com/docs/v3/Plugins/MotionPathPlugin/

## Assessment for AI-HARNESS LIVE v5
- **High-value requirement**: preserve original diagram's complete inventory of nodes, text, icons, edges, and role descriptions; check completeness before motion work.
- **High-value implementation candidate**: use individually addressable SVG/HTML elements, explicit animation timeline, visible icon shapes, and path motion synchronized to highlighted boxes.
- **High-value acceptance criteria**: all original labels and descriptions retained; center vertical path visibly animated; each icon actually moves; loop automatically at 1.5x prior speed; brighter box-edge glow with unchanged text legibility; iPhone Safari smoke test.
- **Low relevance**: GIF sprite sheets (good for character loops, poor for crisp searchable diagram text); watercolor/hand-drawn style prompts conflict with current English neon/angular visual brief.
- **Conditional**: Remotion for exported MP4/video; GSAP for complex web motion if native SVG/CSS/JS proves inadequate; slash-command skill only after repeated successful use.
- **Caution**: A prompt alone does not preserve source content; capture a structured node/edge/text checklist before animating. Don't assume social metrics imply reliability.

## Decision
**B / CANDIDATE**. Keep as research reference in Proposal Incubator. No automatic skill installation, architectural changes, implementation, or modification of existing AI-Harness rules. Promote only after test and Human approval.
