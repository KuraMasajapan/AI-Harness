# Archify — interactive diagram research (2026-10-25)

**Decision: CANDIDATE / HIGH PRIORITY FOR EVALUATION — RESEARCH ONLY**
**X post:** https://x.com/Sn0wbrave/status/2114052217590469014 (2026-10-24; Arabic-language description)
**Primary source:** https://github.com/tt-a1i/archify
**Scope:** AI-HARNESS architecture documentation and visualization. No installation or implementation approved.

## What the primary README supports
- Archify is an open-source agent skill for turning descriptions, plans, and repository analysis into interactive diagrams or one-page explainers.
- README describes Codex CLI, Claude Code, Cursor and OpenCode integrations.
- Generated output can be a self-contained interactive HTML file, with optional image/PDF export. A repository is optional; an agent can start from a textual description.
- Supported diagram types documented: Architecture, Workflow, Sequence, Data Flow, Lifecycle, ERD, Class, Tree, Timeline and Waterfall.
- Uses typed JSON intermediate representation (IR), validation and atomic delivery; failed validation should preserve the last good artifact.
- When source-backed mode is explicitly requested, diagram nodes can cite Git-verified file locations pinned to a commit. This is **traceability**, not independent proof that AI inferred the right architecture.
- Optional stable-update checks are documented; README says checks do not transmit project/prompt content and can be disabled with `ARCHIFY_UPDATE_CHECK_DISABLED=1`. Treat as developer claims until code audit.

## AI-HARNESS applications
- Core: visualize access boundaries, decision/approval flow, project separation and Trinity handoffs.
- Hermes Local Agent: map Memory/Skills/Shell/File interfaces **without advancing Phase 0**.
- BBB: depict Training Lab → Champion Freeze → Forward Gate, decision journal and execution parity. **Visualization only; no live or paper trading changes**.
- UIAPduino: design/development flow; do not treat a diagram as verified electrical engineering.
- Repo overview: source-backed map of modules and cross-project relationships.

## Comparative evaluation
- Compare against existing Markdown/Mermaid, HTML diagrams, GitHub Pages and prior visualization efforts.
- Pilot with a small, read-only, pinned-commit repo snapshot. Ask for 8–12 major components, one critical path, trust boundaries and exact citations.
- Check diagram factual accuracy, update effort, browser portability, standalone operation, performance and maintenance burden.
- Do not confuse polished presentation with confirmed runtime topology. No secrets, private files or unreviewed code execution.

**Conclusion:** High-value CANDIDATE for documentation, not automatic adoption as a global Skill. Human approval required for installation, repo changes or formal architecture publication.
