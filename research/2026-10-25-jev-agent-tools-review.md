# Jev applications — AI-HARNESS cross-project research (2026-10-25)

**Status:** RESEARCH ONLY; candidates not approved as features, skills, integrations, or production dependencies.

**X source:** https://x.com/GitTrend0x/status/2113986396062925178 (2026-10-24)
**Primary evidence:** Project GitHub READMEs, checked 2026-10-25.

## Scope and classification
This shared research note contains **four non-BBB projects** from the X post. The trading-specific `jev-trader` is deliberately documented separately under `projects/BBB/research/field-notes/`. Do not automatically load BBB material into unrelated Core, Memory, or browser research.

### 1. browser-use/jev-ultrafast — CANDIDATE
- Source: https://github.com/browser-use/jev-ultrafast
- A browser agent builds a dynamic indexed table of visible elements. Jev chooses an operation and a compatible target in one model request. A smaller text-generation model is called only for typing.
- Repository reports a 7.1-second Google Flights Zürich→London demonstration, **not** a universal booking latency or general benchmark.
- Potential use: AI-HARNESS browser/agent action selection and cost/latency reduction.
- Open questions: reproduction on varied sites, DOM changes, error recovery, human approval for irreversible actions, dependence on TypeSafe and text-model API keys, privacy and browser access.
- Research only: no browser automation permissions or installation approved.

### 2. tamaratran/fast-jev-compaction — CANDIDATE (HIGH PRIORITY)
- Source: https://github.com/tamaratran/fast-jev-compaction
- Claude Code plugin and npm library: pairs tool calls with results, uses Jev to decide which to retain or trim. Retained text is verbatim; unlike generative summarization, it does not rewrite retained content.
- **Important qualification:** this is *not lossless memory*. Calls/results can be discarded or truncated, and even the state sent to Jev is shortened to fit its context budget. User/assistant text is generally preserved in its compaction approach; confirm behavior on real inputs.
- Potential use: evaluate against AI-HARNESS Memory, source provenance, progressive disclosure, exact paths/errors and preservation classes.
- Open questions: erroneous deletion rate, recovery, privacy of conversation sent to external model, cost/latency, Claude-specific hooks vs platform-agnostic reuse.
- No change to approved Memory rules; candidate only.

### 3. dzhng/jevgrep — CANDIDATE (HIGH PRIORITY)
- Source: https://github.com/dzhng/jevgrep
- CLI that locates relevant code by natural-language question, returns file leads and verbatim snippets; provides an agent skill including Codex installation.
- Author reports 8/10 tasks solved for both baseline and Jevgrep in a **ten-task** SWE-bench comparison, at about 30% lower cost. Small, author-reported experiment; not independent proof of general cost savings.
- Potential use: large AI-HARNESS repository and BBB code navigation, complementing rather than replacing existing search, GitHub read, or Codex.
- Open questions: repository coverage, precision/recall, API charges, indexing/data disclosure, provider requirements (Vercel AI Gateway, TypeSafe, etc.), reproducibility on this repo.
- No installation, API credential connection or Skill adoption approved.

### 4. realZachi/pg-jev — HOLD
- Source: https://github.com/realZachi/pg-jev
- PostgreSQL extension evaluates natural-language conditions against rows, including boolean decisions, scores and probabilities; can be used inside WHERE, JOIN or GROUP BY.
- Repository describes batching, read-ahead and session caching. No vector index is needed, **but** model calls, costs, data sharing and semantic errors remain.
- Potential use only if a real PostgreSQL-backed classification requirement emerges. Not currently a justification to add PostgreSQL to AI-HARNESS.
- Open questions: privacy, latency on large tables, nondeterministic filtering, query-planner interactions, provider availability and permission boundaries.

## Shared evaluation criteria
1. Compare with existing AI-HARNESS Core, Memory, Skills, Browser and Codex workflows; avoid redundant tools.
2. Preserve provenance and exact source text; label all probabilistic decisions and unknowns.
3. Reproduce latency/cost claims with a fixed benchmark and log failures, not just successful demos.
4. Confirm license, dependencies, external APIs, model/data transmission and costs before proposing installation.
5. Enforce Human approval for repository writes, rule changes, secrets, browser actions and production execution.

## Decisions
- **CANDIDATE:** browser-use/jev-ultrafast, fast-jev-compaction, jevgrep.
- **HOLD:** pg-jev.
- **Excluded from this file:** jev-trader, recorded separately as BBB-specific research.
- No implementation or formal specification changes. Next step is optional controlled evaluation with explicit Human approval.
