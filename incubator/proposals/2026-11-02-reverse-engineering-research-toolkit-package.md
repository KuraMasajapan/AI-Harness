---
document_type: research_package
date: 2026-11-02
title: "Reverse Engineering Research Toolkit — REA-centered 18-repository capability map"
scope: "AI-Harness cross-project / authorized reverse engineering / research only"
branch: development
status: CANDIDATE
implementation: HOLD
installation: NONE
operational_integration: NONE
stage_1: A+
stage_2: A
evidence: "User-shared roundup; GitHub repository metadata and selected READMEs checked; no source-code security audit or local test"
source_post: "Human-provided Japanese roundup, 18 repositories and 2 workflows; original post URL not supplied"
canonical_existing_rea: "incubator/proposals/2026-10-25-rea-reverse-engineering-agent-evaluation.md"
related_clean_room: "projects/Hangfire/reference/CLEAN_ROOM/HANGFIRE_MAPPING.md"
tags: [reverse-engineering, rea, codex, ghidra, mcp, apk, dotnet, native-binary, forensic-analysis, clean-room, oracle, security, research-package, evaluation, authorized-analysis]
trigger_topics: [REA, Reverse Engineer Anything, Ghidra, GhidraMCP, ida-pro-mcp, jadx, Apktool, Frida, ILSpy, radare2, x64dbg, ImHex, angr, mitmproxy, dnSpy, rizin, raddebugger, reverse-engineering-toolkit, clean-room, oracle, SPEC.md]
---

# Reverse Engineering Research Toolkit — 18 repositories + 2 workflows

> **Human decision (2026-11-02):** Preserve the introduced collection as **one research package**, and link items not already covered to **existing GitHub knowledge**. No mass installation, operating-system access change, reverse-engineering run, copied software or promotion into Core/Trinity/project code. Components may be individually tested only after a concrete authorized need and separate Human approval.

## 0. What this package is (and is not)

A **functional catalog / research entry point** centered on [REA](https://github.com/morluto/rea), not a prebuilt, compatible, ready-to-run set of 20 applications. The roundup consists of **18 distinct GitHub repositories plus 2 conceptual workflows** ("REA investigation flow" and "clean-room reconstruction loop"). Some tools are alternatives; some require licensed commercial software; some may already be reachable through REA itself. Treat each upstream repository independently for release, dependency, license, OS, permissions and threat model.

The proposed loop is a **research hypothesis**:

1. Select an **owned, expressly authorized or clearly permitted** target and document rights, version, checksum and scope.
2. Observe known behavior and inspect artifacts using **REA** and only the required optional tool.
3. Separate evidence (what was observed), inference (what is hypothesized) and unknowns; create a narrow **SPEC.md** with provenance, test cases and expected outcomes.
4. If independently implementing functionality is permitted, write original code in a separate environment without copying restricted source/assets.
5. Compare actual behavior to the documented **oracle** (a permitted reference implementation, owned test harness, published format specification or fixed examples). Record matches / mismatches / untested and repeat only within the authorized scope.
6. Preserve a reviewable result; **do not claim complete functional parity or legality** just because a test set passes.

The words "reverse engineer any app", "all evaluated", "security SAFE" and "matches until done" are marketing/generalizations, not verified guarantees.

## 1. Catalog — original 18 repositories

Status meanings: **EXISTING** = a preexisting AI-Harness record is linked and remains source of truth; **CANDIDATE / HOLD** = useful optional tool subject to a scoped trial; **REFERENCE** = keep as background knowledge; **SENSITIVE / HOLD** = do not enable unless scope, authority and sandboxing are justified.

| Original group | Repository (official link) | Practical role / functional difference | Priority / boundaries |
| --- | --- | --- | --- |
| 01 Analysis core | [morluto/rea](https://github.com/morluto/rea) | AI-oriented MCP/workflow across application, source/artifact and native analysis; may use external analyzers | **EXISTING / A / HOLD**; canonical evaluation linked below |
| 01 Analysis core | [NationalSecurityAgency/ghidra](https://github.com/NationalSecurityAgency/ghidra) | Free native disassembler/decompiler and scripting environment | **CANDIDATE / A** for PE/ELF/firmware; substantial setup and environment isolation |
| 01 Analysis core | [LaurieWired/GhidraMCP](https://github.com/LaurieWired/GhidraMCP) | Extra MCP bridge between an agent and a running Ghidra environment | **CONDITIONAL / HOLD**: may overlap REA's own Ghidra integration; no exposed unauthenticated MCP service |
| 01 Analysis core | [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | MCP bridge for **IDA Pro** | **REFERENCE**: commercial IDA Pro required (IDA Free unsupported in this repo); creator recommends the newer [official Hex-Rays IDA MCP](https://github.com/HexRaysSA/ida-mcp) |
| 02 Mobile/apps | [skylot/jadx](https://github.com/skylot/jadx) | Android DEX/APK decompilation to Java-like representations | **CANDIDATE / A** for authorized Android app investigation |
| 02 Mobile/apps | [iBotPeaches/Apktool](https://github.com/iBotPeaches/Apktool) | APK resources, manifest and Smali disassembly/rebuild | **CANDIDATE / A**; complementary to jadx; rebuilding another party's APK requires permission |
| 02 Mobile/apps | [frida/frida](https://github.com/frida/frida) | Runtime process instrumentation and API tracing | **SENSITIVE / HOLD**; live target execution/injection and privilege boundaries |
| 02 Mobile/apps | [icsharpcode/ILSpy](https://github.com/icsharpcode/ILSpy) | .NET decompiler and metadata/source view | **CANDIDATE / A** for permitted .NET Windows desktop binaries; often sufficient without native toolchain |
| 03 Binaries/low-level | [radareorg/radare2](https://github.com/radareorg/radare2) | CLI-based native binary inspection and debugging | **REFERENCE / CONDITIONAL**; overlaps Ghidra and Rizin |
| 03 Binaries/low-level | [x64dbg/x64dbg](https://github.com/x64dbg/x64dbg) | Windows x86/x64 user-mode debugger | **CONDITIONAL / HOLD**; runtime analysis in isolated Windows test machine |
| 03 Binaries/low-level | [WerWolv/ImHex](https://github.com/WerWolv/ImHex) | Hex/binary structure viewer with pattern language | **CANDIDATE / B+** for file formats, firmware and data-layout analysis |
| 03 Binaries/low-level | [angr/angr](https://github.com/angr/angr) | Symbolic execution and program analysis | **REFERENCE / SPECIALIZED**; resource intensive; only if simpler methods fail |
| 04 Network/runtime | [mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy) | HTTP(S) interception and inspection for **authorized** traffic | **SENSITIVE / HOLD**; traffic contents, credentials, private data and TLS trust changes |
| 04 Network/runtime | [dnSpyEx/dnSpy](https://github.com/dnSpyEx/dnSpy) | .NET assembly inspection, debugging and editing | **CONDITIONAL / HOLD**; overlaps ILSpy; prefer ILSpy first for read-only analysis |
| 04 Network/runtime | [rizinorg/rizin](https://github.com/rizinorg/rizin) | Independent fork of radare2, command-line binary analysis | **REFERENCE / ALTERNATIVE**; choose Rizin **or** radare2 for a given experiment |
| 04 Network/runtime | [EpicGames/raddebugger](https://github.com/EpicGames/raddebugger) | Native graphical debugger | **CONDITIONAL / HOLD**; compare to x64dbg only when native debugging is justified |
| 05 Reconstruction/validation | [zhuyansen/awesome-ai-reverse-engineering](https://github.com/zhuyansen/awesome-ai-reverse-engineering) | Dynamic AI-specific curated/reviewed repo index | **REFERENCE**; "AI/security-rated" is **not** an independent code audit |
| 05 Reconstruction/validation | [morluto/awesome-reverse-engineering](https://github.com/morluto/awesome-reverse-engineering) | REA creator's general, task-oriented RE links and learning list | **REFERENCE**; directory, not an executable unified tool |

**License caveat (from GitHub metadata checked 2026-11-02):** REA/IDA-MCP/ILSpy/mitmproxy/raddebugger MIT; Ghidra/GhidraMCP/jadx/Apktool Apache-2.0; ImHex GPL-2.0; angr BSD-2-Clause; dnSpyEx GPL-3.0; Rizin LGPL-3.0; morluto awesome list CC0-1.0. Frida, radare2, x64dbg and the zhuyansen list had ambiguous/NOASSERTION metadata in this check; **inspect their actual applicable license files before copying, bundling or redistributing anything**. Licensing of the analysis tool never grants permission to copy the analyzed target.

## 2. Two workflows — deliberately not counted as extra repositories

### 19. REA investigation workflow (concept / existing REA knowledge)

Signal: binary / app → investigation → evidence → candidate specification. REA's README and [reconstruction readiness documentation](https://github.com/morluto/rea/blob/main/docs/reconstruction-readiness.md) describe useful processes, but **a successful readiness or synthetic test is not proof of complete runtime equivalence**.

- Minimum useful research artifact: scope + permissions + sample hash + observed input/output + tool/commit versions + findings tagged OBSERVED / INFERRED / UNKNOWN.
- Do not assume REA orchestrates every tool in this catalog or that all listed MCP servers work with it without integration work.
- Existing primary evaluation: [2026-10-25 REA standalone research](2026-10-25-rea-reverse-engineering-agent-evaluation.md). **Do not duplicate the existing REA assessment**.

### 20. Clean-room SPEC / oracle loop (methodology / existing Hangfire precedent)

- Separate raw observation, generalized mechanics, independent specification and newly authored implementation.
- Oracle = an explicit, permitted behavior reference and documented test procedure; a black-box output may have multiple explanations, so oracle comparison does not prove all internal behavior.
- Maintain legal/ethical boundaries for EULAs, DRM, platform controls, confidential information, protected content and authorization.
- Where separation between research and implementation people is feasible, preserve that boundary; otherwise require provenance, source-exclusion checks and Human review before implementation.
- **Existing project-specific precedent**: [Hangfire independent mechanics mapping](../../projects/Hangfire/reference/CLEAN_ROOM/HANGFIRE_MAPPING.md) and [DO_NOT_COPY policy](../../projects/Hangfire/reference/CLEAN_ROOM/DO_NOT_COPY.md). This package does not modify or loosen those rules. Its generic methodology is only a reference; Hangfire's accepted Source of Truth remains authoritative.

## 3. Cross-reference map — no duplicate research records

| Existing AI-Harness document | Linkage and interpretation | Action |
| --- | --- | --- |
| [REA standalone evaluation](2026-10-25-rea-reverse-engineering-agent-evaluation.md) | Existing assessment covers REA's value, individual/private-use caveats, capability claims, non-adoption decision | **CANONICAL / unchanged judgment; add backlink** |
| [Hangfire reference entry](../../projects/Hangfire/reference/README.md) | Concrete clean-room separation and prohibition on copying the referenced game's code/assets/parameters | **EXISTING precedent / add optional backlink only** |
| [BBB: REA/Kronos/TradingAgents cross-reference](../../projects/BBB/research/field-notes/2026-10-24-rea-kronos-tradingagents-bbb-crossreference.md) | Prior finding: REA is not a financial forecast tool, only a software investigation reference | **EXISTING / add backlink; no trading integration** |
| [Mac.apk Android compatibility / safety](2026-10-25-mac-apk-android-compatibility-security-review.md) | Android runtime isolation risks are different from JADX/APK reverse engineering; related threat-boundary reminder only | **RELATED / link from package, no change** |
| [Agent OS OSS Landscape](2026-10-02-agent-os-oss-landscape.md) | E2B and isolation as optional future safe-execution references | **RELATED / link from package, no install** |

**Newly indexed without a prior dedicated record found in the AI-Harness development-tree filename audit:** Ghidra, GhidraMCP, ida-pro-mcp, JADX, Apktool, Frida, ILSpy, radare2, x64dbg, ImHex, angr, mitmproxy, dnSpyEx, Rizin, raddebugger and the two Awesome directories. These are each **individual rows in this one package**, not 17 new files or 17 separate adoption decisions. Existing mentions embedded elsewhere are not ruled out by a filename-only audit.

## 4. Facts verified vs unverified claims

**Confirmed at the repository/README level:** the 18 named projects exist with the linked owners, broad functions above, and (where disclosed) platform/dependency prerequisites. GhidraMCP requires a separate Ghidra installation. The maintainer of mrexodia/ida-pro-mcp currently recommends the official Hex-Rays server and says IDA Free is unsupported. The zhuyansen README **currently says 117 repos**, whereas the shared post claims **122**; this index is time-sensitive.

**Not established:** "all 122 repos fully security audited", compatibility of the 18 tools as a single installation, absence of malicious code, independent accuracy or complete app recreation, that an MCP connector necessarily respects a least-privilege boundary, and legality of analyzing/rebuilding arbitrary proprietary apps. The zhuyansen README states its screening is made by a *decision model reading each README*, not a manual security review of all executable code.

**Risk warning:** A reverse-engineering target is untrusted data, and its imported resources and metadata can contain malicious or misleading instructions. Do not let an agent convert source text, observed strings, captured network responses or embedded docs into privileged instructions. Do not expose GhidraMCP/SSH/HTTP/control endpoints to the internet or whole tailnet by default. Restrict tool and OS permissions and keep target samples isolated.

## 5. Minimal package workflow for AI-Harness (proposal, not implementation)

| Stage | Initial default | Optional escalation only if necessary |
| --- | --- | --- |
| 0. Authorization and intake | Owned/approved sample + checksum + threat model + reference license | Stop if legal/permission status is unclear |
| 1. Quick triage | Static inspection and existing Codex source review | REA in isolated workspace; avoid a permanent global MCP |
| 2. Native PE/ELF/firmware | Ghidra as the first conditional engine | GhidraMCP only if REA cannot safely perform required bridge; later x64dbg/raddebugger or radare2/Rizin/angr for specific gaps |
| 3. Android | JADX for read-only source-like view | Apktool for resources/Smali; Frida only for explicitly authorized runtime tests |
| 4. .NET | ILSpy for read-only analysis | dnSpyEx for permission-scoped debugging/editing if truly needed |
| 5. Protocol / files | Ordinary logs, format docs, ImHex for file layout | mitmproxy for controlled own-traffic inspection only |
| 6. SPEC and oracle | Evidence-based narrow specification + explicit reference tests | Original code in clean-room partition after separate approval |
| 7. Acceptance | Compare behavior, record mismatches and uncertainty, peer/Human review | Re-evaluate or reject; **no automatic release** |

Initial experiment, if separately approved: **an owned trivial command-line executable** with a known function and known build inputs. Compare current Codex-only inspection vs REA-assisted inspection on accuracy, provenance, elapsed time, tokens, dependency footprint and permission safety. Do not start with a protected commercial binary, production endpoint, private login or third-party network traffic.

## 6. Security/authority and implementation status

- **Default: no install.** No new global MCP servers, admin rights, file-system-wide read access, network listener, SSH bridge, registry changes or code execution.
- Prefer a disposable local sandbox or VM, read-only samples, non-admin account, network off unless required and approved, explicit input/output directories and logs.
- Never ingest third-party credentials, decrypted secrets, customer data or restricted/proprietary code into the model context without a clear authorization and handling plan.
- **No bypassing entitlement/paywall/DRM/authentication**, mass cloning of proprietary app behavior or distribution of protected software/assets.
- Human approval before extraction with additional privileges, live process hooking, interception, downloading executables, installing MCP servers, copying licensed source or any independent reconstruction project.
- Existing **sealed TRINITY**, **Core/RULES/ACCESS**, **Hermes phase**, **BBB live safeguards** and **Hangfire CLEAN_ROOM** are unchanged.
- Result status: **Stage 1 A+ / Stage 2 A / CANDIDATE / IMPLEMENTATION HOLD**. This measures research relevance only; not product quality, security rating, or operational readiness.

## 7. Recall / future maintenance

Search terms: REA, 18 repositories + 2 workflows, 20 reverse engineering tools, Ghidra, GhidraMCP, jadx, Apktool, ILSpy, Frida, ImHex, angr, radare2, rizin, x64dbg, raddebugger, dnSpy, mitmproxy, MCP, SPEC.md, evidence, oracle, clean room, reconstruct, Hangfire, source provenance, sandbox, legal review.

New tools are added to this catalog **when they add a distinct function**, or are linked to an existing canonical record if the function is already researched. Do not copy entire third-party awesome lists into the repository, turn them into automatic installers or grow the package into a second global agent-orchestration system.

Related sources:
- https://github.com/morluto/rea
- https://github.com/morluto/awesome-reverse-engineering
- https://github.com/zhuyansen/awesome-ai-reverse-engineering
- https://github.com/mrexodia/ida-pro-mcp
