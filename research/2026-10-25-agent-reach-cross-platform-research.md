# Agent Reach — cross-platform agent research (2026-10-25)

**Decision: CANDIDATE / ALREADY KNOWN LEAD — RESEARCH ONLY**
**Post:** https://x.com/ozmazzz/status/2113933745204207854 (2026-10-24)
**Primary source:** https://github.com/Panniantong/Agent-Reach
**Scope:** AI-HARNESS Core/Skills, Hermes Local Agent and research ingestion. No installation or access changes authorized.

## Post vs README
- The post presents Agent Reach as a 'universal pass' enabling Codex/Claude Code to search X, Reddit, Xiaohongshu, Bilibili, YouTube and GitHub, read comments, and get subtitles.
- README confirms it is a CLI orchestration layer over per-platform upstream tools, with preferred and fallback implementations. **Not universal unrestricted access**.
- README at review time showed about 101.8k GitHub stars; stars are popularity, not security or performance proof.
- Default channels include Bilibili, V2EX, GitHub, YouTube and web. Optional channels include Xiaohongshu, Xueqiu, Reddit, LinkedIn and others; Twitter/X, Facebook and Instagram are marked **experimental**.
- YouTube audio transcription can require a Groq or OpenAI API key; some platform capabilities require login. 'Zero API fees' must not be treated as guaranteed zero total cost.
- README says tools are **read-only** (search and read, no post/comment/like/DM). This is a project claim, not an independent security audit.
- It can copy website login sessions from a local Chrome profile into a dedicated browser. That is sensitive authentication material even without reading passwords. Avoid primary accounts and do not connect credentials without explicit Human approval.
- README warns the similarly named PyPI `agent-reach` package is unrelated; installation must use the official repository's documented path, after separate review.

## Relevance and overlap
- **Hermes Local Agent (Phase 0 / NOT IMPLEMENTED):** Potential future tool-access experiment, not permission to install or progress Phase.
- **AI-HARNESS research:** Potential discovery of X/Reddit/Chinese platform data not reachable via existing tools.
- **Overlap:** Existing ChatGPT web search, browser and TinyFish already cover part of the need. Measure marginal capability before adoption.
- **Risks:** session theft/accidental exposure, platform bans/ToS, brittle scraping, upstream tool supply chain, version drift, data provenance and user privacy.

## Proposed evaluation gate
1. Identify three concrete unanswered research queries using current approved tools.
2. Compare coverage, accuracy, provenance, failure modes, maintenance and cost against Agent Reach in an isolated account-less test.
3. Review installer/upstream dependencies and session handling; do not import personal browser cookies.
4. Separate research collection from any publication, account access, or automated action.

**Conclusion:** CANDIDATE (continued research), not a novel discovery or urgent installation. No implementation, permissions, secrets, Core rules or approved specification changed.
