---
document_type: research_evaluation
date: 2026-10-20
timezone: Asia/Tokyo
subject: Cloud Harness MCP
stage_1_rank: A+
stage_2_rank: A+
decision: HOLD
relationship: COMPARE / REINFORCE
implementation: NOT APPROVED
origin: Grok Observer Run dated 2026-10-19, Harness Inbox
branch: development
tags: [mcp, coding-agent, runtime, local-first, tool-surface, cost, security, human-approval]
---

# Cloud Harness MCP — Coding harness through MCP (research only)

## Chronology and evidence provenance

- **2026-10-18 — Signal date**: According to the later Grok observation record, the X/OSS signal concerned Cloud Harness MCP on this date. This is **the signal date as recorded by Grok**, not an independently verified repository release timestamp.
- **2026-10-19 — Grok collection**: The **AI-Harness / Observer Runs** Airtable record reports **COMPLETE** with 1 discovered, 1 written, and 1 read-back verified entry. Its corresponding **Harness Inbox** entry was **NEW**, titled *CloudHarness MCP: full coding harness as single MCP server*. These counts verify the observation workflow's write/read-back, **not** the full truth of the OSS's advertised claims.
- **2026-10-20 — ChatGPT follow-up review**: Read the upstream GitHub README, package metadata, MIT license, and security model. Research judgment **A+ / HOLD**. This date is the review/recording date (JST, date-only); no unverified event clock-time is asserted.

### Sources (rechecked 2026-10-20)

- Upstream: https://github.com/bestagentkits/cloud-harness-mcp
- Architecture / usage: https://github.com/bestagentkits/cloud-harness-mcp/blob/main/README.md
- Security model: https://github.com/bestagentkits/cloud-harness-mcp/blob/main/docs/security-model.md
- MCP semantics: https://github.com/bestagentkits/cloud-harness-mcp/blob/main/docs/mcp-api.md
- License: https://github.com/bestagentkits/cloud-harness-mcp/blob/main/LICENSE
- Package metadata: https://github.com/bestagentkits/cloud-harness-mcp/blob/main/package.json

## Verified upstream capabilities (documented, not independently executed)

1. **MCP entry point for coding work**: The upstream implementation describes a Streamable HTTP MCP service with authenticated access and a local **stdio** mode; the exposed operations cover workspace lifecycle, file and code search/editing, commands, shells, sessions, tasks, Git/worktrees, skills/hooks, memory, and certain repository-defined deployment actions.
2. **Remote execution architecture**: An API/control plane delegates work to a runner managing time-limited Docker executor workspaces. Repository credentials and network Git transfers are separated into an ephemeral Git helper and a broker, according to upstream architecture/security docs.
3. **Local project mode**: `--transport stdio --workspace <path>` lets an MCP client operate against an explicitly chosen local directory. Local v1 targets POSIX hosts (Linux/macOS); Windows is directed to WSL.
4. **Git safeguards in local mode**: Network fetch/pull and push are off by default unless enabled with `--git-network` / `--git-push`. This restricts some operations but does **not** make the process read-only or sandboxed.
5. **MIT license**: The repository's LICENSE is MIT. Root package metadata at review showed version `0.71.0` and Node `>=24` (snapshot, subject to change).

**Evidence limit:** Documentation and source structure were inspected; no installation, test run, security audit, performance measurement, actual client authorization test, or production deployment was performed.

## Potential relevance to AI-Harness

- **Tool consolidation / context economy**: May reduce the burden of wiring many coding tools separately into agent clients. The Grok Inbox describes “MCP-in-MCP” and a constant five-tool client surface; the README also enumerates numerous named operations. **The exact externally exposed tool-count, token savings and client-specific negotiation behavior were NOT verified.** Test the actual `tools/list` result and prompt-token overhead before treating either description as fact.
- **Model/client independence**: Could provide common coding operations to different MCP-capable agents without rebuilding identical file/shell/Git functionality for each; a concrete advantage over current tooling remains unproven.
- **Local-first exploration**: stdio mode could be assessed on a separate test directory without renting a VPS. Any approach must preserve Human-approved Git writes.
- **Runtime persistence and handoff**: Workspace sessions, tasks and retained artifacts might support interrupted jobs, but must be compared to existing Work/Codex and AI-Harness checkpoints rather than assumed superior.

### Overlap / comparison candidates

- **ChatGPT Work / Codex / existing GitHub access**: Already cover much of the user-visible workflow. Quantify incremental value instead of deploying a redundant control plane.
- **Cua Spaces / Cua Driver research (2026-10-20)**: Cua centers desktop/computer-use and multi-computer Spaces, while Cloud Harness MCP centers coding workspaces, commands, Git and agent tooling. They are potential complements or competing execution substrates, not automatically interchangeable. Cua was researched in conversation; its proposal was not assumed saved.
- **LCU / Hermes desktop control proposal**: `incubator/proposals/2026-10-16-lcu-hermes-desktop-control.md`; focuses GUI interaction and OS compatibility, not a fully equivalent coding harness.
- **Agent permissions/Human approval backlog**: `incubator/proposals/2026-10-16-grok-agent-permission-approval-hold.md`; review independent enforcement rather than relying on agent self-restraint.

## Security, cost, and feasibility cautions

1. **Arbitrary code execution** is an intended capability, not an incidental side effect. Remote commands, hooks, skills and deployment extensions can execute untrusted repository-supplied code.
2. **Local stdio mode runs commands as the host user.** Path confinement is **not OS sandboxing**; it must not be granted access to a personal/family PC or live credentials on the assumption that a workspace path is a security boundary.
3. **Remote Docker shares the host kernel.** Upstream warns it is built for mutually trusted operators in one security domain, **not hostile multi-tenancy**. The runner's Docker-socket authority is highly privileged even if executor containers lack that socket.
4. **Access and Human approval**: Any network write, Git push, filesystem modification, privilege expansion, paid deployment or executable skill/hook requires an independent authorized boundary. MCP authentication by itself is not a full Human approval system.
5. **Unverified cost claim**: The Grok Inbox mentioned a "$24/month VPS" example. It is **not established here as a minimum or official price**; local hardware, hosting, token/model use and administration cost vary.
6. **Maintenance/complexity**: Node >=24 for the observed package, WSL needed for Windows local mode, and Docker/server/credential configuration for remote use increase operational burden. This may outweigh savings compared with existing ChatGPT/Codex/Work features.

## Research evaluation

| Criterion | Assessment |
|---|---|
| Stage 1 relevance | **A+** — local agent execution, MCP, tool orchestration and reusable coding operations |
| Stage 2 evidence-grounded rank | **A+ (provisional)** — specific implementation, docs and license verified, incremental benefit not benchmarked |
| Decision | **HOLD / COMPARE** — preserve as research; do not adopt into Core or install |
| Affected areas | AI-Harness Runtime, Tools, Skills, Access, Memory; possible Hermes complement |
| Reversibility | Potentially high for isolated throwaway test; unknown for integrated production use |

### Proposed future validation — not approved for execution

1. Establish a **baseline** using existing ChatGPT Work/Codex/GitHub for a small, low-risk coding task; measure steps, tool-schema/context overhead, Human interventions, latency and outcome.
2. In a **disposable local test account and directory**, compare only the selected local stdio capability, validate `tools/list` count, path handling, prompts/permissions, token cost and whether the claimed tool consolidation holds.
3. Inspect startup scripts, transitive dependencies and execution policy; test whether mutating operations can be blocked independently of agent instructions. Avoid secrets, real repos and outward Git writes.
4. Only if extra value is demonstrated, separately examine remote Docker/VPS option with threat model, expense and recovery plan; do not deploy on the strength of README statements alone.
5. Compare against **Cua Spaces** and the existing **LCU/Hermes** candidate to avoid duplicated control planes.

## Governance

**Research and implementation are separate.** This note records an investigation, not consent to install a plugin/MCP server, run commands, register a hosted account, create a VPS, link credentials, write to other repositories, approve Git pushes, change Core/Workflow/Access, or enable unattended execution. A future proposal for execution must identify affected paths, permissions, costs and acceptance criteria and receive Human approval before acting.
