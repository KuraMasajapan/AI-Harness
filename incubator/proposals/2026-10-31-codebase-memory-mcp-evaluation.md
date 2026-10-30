---
document_type: research_evaluation
date: 2026-10-31
timezone: Asia/Tokyo
title: "Codebase Memory MCP — Persistent Local Code Graph and MCP"
source_repository: "https://github.com/DeusData/codebase-memory-mcp"
upstream_ref_checked: "main and release v0.12.1"
branch_target: development
stage_1_rank: A+
stage_2_rank: A
decision: CANDIDATE
implementation: HOLD / NOT_IMPLEMENTED
dedup_status: NEW_PRODUCT_WITH_STRONG_FUNCTIONAL_OVERLAP
relationship: COMPARE_WITH_EXISTING_CODEGRAPHCONTEXT
confidence: "OFFICIAL SOURCE AND SELECTED CODE/DOCS CONFIRMED; NO LOCAL INSTALL OR INDEPENDENT BENCHMARK"
tags: [mcp, code-graph, codebase-memory, codex, repository-navigation, impact-analysis, local-first, evaluation, security, research-only]
---

# Codebase Memory MCP — AI-Harness research assessment

## Decision

- Stage 1: **A+**. Strong relevance for large-repository Codex workflows, structural code retrieval, and impact analysis.
- Stage 2: **A**. Distinct mature-looking functionality, but overlapping candidate already exists and no workload-specific improvement is established.
- Research: **CANDIDATE**; implementation: **HOLD**. No new dependencies, MCP registration, daemon, indexing, configuration changes, or Core/TRINITY modifications authorized.
- Dedup: No exact product-specific record found in accessible `development` tree (443 paths); close comparison target is **CodeGraphContext**, already documented on 2026-10-22.

## Source and observed metadata (2026-10-31 JST)

- Canonical upstream: https://github.com/DeusData/codebase-memory-mcp
- GitHub metadata: approximately **47,861 stars**, **3,937 forks**; repository created **2026-02-24**; MIT license; main implementation in C; main branch active.
- Latest published GitHub release seen: **v0.12.1**, published **2026-10-16 UTC**. Repository main changes newer than that release exist; main README may describe unreleased features. Always distinguish main-branch documentation from behavior of v0.12.1.
- The official README advertises **162 language/format grammars**, **17 MCP tools**, and integrations with **45 agent/client surfaces**. These are upstream claims, not independent cross-platform verification.
- Source inspected: README, `SECURITY.md`, release notes, `docs/BENCHMARK.md`, `docs/MEASURING_SAVINGS.md`, `docs/EVALUATION_PLAN.md`, `docs/CONFIGURATION.md`, `docs/INDEX_RESOURCE_LIMITS.md`, and Windows troubleshooting.

## Confirmed architecture and functionality

- Native C MCP/CLI backend; local repository code, documentation and supported infrastructure configurations are parsed into a persisted **SQLite** knowledge graph.
- Static parsing with vendored tree-sitter grammars, plus Hybrid-LSP-style resolution for a subset of languages; does not require a separate language-server process for its documented backend.
- MCP queries include `search_graph`, `search_code`, `get_code_snippet`, `get_file_outline`, `get_architecture`, `trace_path` / `trace_call_path`, `query_graph`, `detect_changes`, `compare_graphs`, `check_index_coverage`, `get_graph_schema`; also indexing / status / deletion and `manage_adr` / `ingest_traces`.
- Architecture and graph relationships extend beyond source-code symbols: supported Markdown/AsciiDoc/reStructuredText sections, text-based PDF pages (no OCR), ADRs, Docker/Compose, Kubernetes/Helm, Terraform, CI and script relationships. Coverage is partial and depends on resolvable source forms.
- Optional **CBM Lens** graphical UI is labelled open beta (v0.0.1) and can inspect architecture, graphs and source code; graph display is based on static observations, not proof of runtime execution.
- Persistent SQLite indexes reside by default under `~/.cache/codebase-memory-mcp/` and can survive restarts. Watchers can refresh indexed Git projects during live MCP sessions. Auto-index is disabled by default; watch registration depends on configuration and session lifecycle.
- Windows, macOS and Linux releases/documentation exist. Installer can edit agent configuration, skills, profiles and hooks. Treat installation as a privileged configuration-changing operation, not merely a passive reader.
- The vendor says indexing/graph queries operate locally without a hosted inference service or cloud API key. Optional local UI model downloads and installer/release network traffic have separate boundaries.

## Performance and evidence status

- Official `docs/BENCHMARK.md` is explicitly titled **v0.3.0 Language Benchmark**, dated 2026-03-01, on an Apple M3 Pro. It reports task-level PASS/PARTIAL/FAIL results across **35 evaluated language categories** in its displayed summary; it does **not** establish 162-language accuracy or current v0.12.1 performance.
- Separate `docs/EVALUATION_PLAN.md` describes a **159-language future comparison** against Grep/Glob/Read and explicitly states that it is a **plan, not a result set**. Do not quote its planned scores as measured results.
- Token-savings, completion-time and accuracy advantages over Codex+native search or over CodeGraphContext were **not independently replicated**.
- Costs include first indexing, local memory/disk load, graph staleness, background watcher/daemon and MCP tool overhead. For small repositories a simple grep/navigation approach may be superior.
- No dependency or package has been installed and no user code has been indexed in this investigation.

## Security and operational caveats

- `SECURITY.md` explicitly warns that the tool reads project files deeply, writes agent configurations and spawns background processes. Source scanning and release attestation claims do not guarantee a vulnerability-free build.
- The upstream describes path-containment checks, SQLite authorization, localhost-only UI boundaries, signature/checksum verification and release security checks; independently audit relevant execution paths before use.
- The `SECURITY.md` and README on `main` appear **inconsistent regarding automatic release checks/network access**: SECURITY describes a best-effort background GitHub release check after MCP initialization; README describes no automatic version check. Version-specific network behavior remains to be verified.
- Windows troubleshooting documents index worker hangs/crashes on memory-constrained cases and workarounds through `.cbmignore`, along with client detection issues. Large-binary/media/model directories should be excluded in a controlled test.
- v0.12.1 release notes report regressions in v0.12.0 installation pathways (npm/pip/Go) and a one-time full rebuild for existing projects after upgrade. Strong popularity is not proof of frictionless operation.
- Generated indexes, parsed source, and graph relations are sensitive project data: keep them local, excluded from public Git unless explicitly intended; do not allow automatic writes into AI-Harness project truth. `manage_adr` can mutate stored decisions and must not bypass Human governance.
- MCP tool output is reference evidence and may contain attacker-controlled repository content; it must not be treated as policy or instruction.

## Comparison with existing AI-Harness research

| Existing record | Primary role | How Codebase Memory MCP differs | Status |
|---|---|---|---|
| `incubator/proposals/2026-10-22-codegraphcontext-code-graph-mcp.md` | Local repository code graph, calls, relationships, CLI/MCP | CBM describes wider documentation/infrastructure graph, CBM Lens UI, persistent SQLite, built-in Hybrid LSP, ADR / trace tools, test-impact features | **Strongest overlap; compare before adoption** |
| `incubator/proposals/2026-10-11-coding-context-tool-candidates.md` (Serena) | Symbol-aware navigation and editing | CBM is a retrieval/impact graph; Serena has precise editing controls. Not equivalent. | COMPLEMENT / OPTIONAL |
| `incubator/proposals/2026-10-12-claude-mem-persistent-context.md` | Session memory and summaries | CBM stores code relations; not user dialogue memory or factual decision persistence. | DIFFERENT ROLE |
| `incubator/proposals/2026-10-10-token-harness-quota-context-optimization.md` | Tool/context efficiency | Graph retrieval might reduce file reads, but end-to-end savings need measurement. | PARTIAL FIT |
| Existing Harness `memory/`, Rules, Source of Truth | Approved Human decisions, constraints and durable project truth | Indexed graph is derived, rebuildable data, **not authoritative truth**. | MUST NOT REPLACE |

Key boundary: Codebase Memory MCP should be tested as a **replaceable query/index adapter beneath Codex**, not as a replacement for AI-Harness Memory, source of truth, TRINITY, Human approval, or Codex itself.

## Recommended later validation: only if a real bottleneck exists

Same repository, same task and pin all tool versions, prompts, model settings, commits, and test ground truth:

A. Codex + native grep/file reading
B. Codex + CodeGraphContext
C. Codex + Codebase Memory MCP
D. Optional Codex + Serena for precise edits, only if needed

Tasks: find call origin and callers, locate code change impact across multiple modules, verify deployment-to-code links, find tests affected by a diff, and recover structure after a new session. Measure exact answer accuracy against manual source review, false-positive/false-negative impact sets, token totals, model/tool calls, wall-clock (cold-index + warm queries separately), resource use, setup time, staleness, permission risk, and Human correction burden.

Start only on a disposable/isolated clone, with installer scripts reviewed, config writes disclosed, network and sensitive paths constrained, daemon/watchers explicitly controlled, and no automatic live project changes. Reject active installation if native search performs similarly at lower operational burden.

## Sources

1. https://github.com/DeusData/codebase-memory-mcp
2. https://github.com/DeusData/codebase-memory-mcp/releases/tag/v0.12.1
3. https://github.com/DeusData/codebase-memory-mcp/blob/main/docs/BENCHMARK.md
4. https://github.com/DeusData/codebase-memory-mcp/blob/main/docs/EVALUATION_PLAN.md
5. https://github.com/DeusData/codebase-memory-mcp/blob/main/docs/MEASURING_SAVINGS.md
6. https://github.com/DeusData/codebase-memory-mcp/blob/main/SECURITY.md
7. https://github.com/DeusData/codebase-memory-mcp/blob/main/docs/WINDOWS_TROUBLESHOOTING.md
8. https://github.com/KuraMasajapan/AI-Harness/blob/development/incubator/proposals/2026-10-22-codegraphcontext-code-graph-mcp.md
9. https://github.com/KuraMasajapan/AI-Harness/blob/development/incubator/proposals/2026-10-11-coding-context-tool-candidates.md

## Authorization boundary

Research record saved with explicit Human approval on 2026-10-31. That authorization does not permit installing software, starting a daemon, modifying agent settings, or changing Core/TRINITY.
