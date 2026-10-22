---
document_type: research_evaluation
date: 2026-10-23
title: "CC Switch — Human-facing AI Coding Control Plane Candidate"
source_repository: "https://github.com/farion1231/cc-switch"
decision: CANDIDATE
implementation: HOLD
stage_1_rank: A+
stage_2_rank: A
evidence_status: "OFFICIAL REPOSITORY / README CONFIRMED; SECURITY / TOS / LOCAL FIT REQUIRE SECONDARY VALIDATION"
tags:
  - cc-switch
  - codex
  - claude-code
  - hermes
  - routing
  - provider-switching
  - mcp
  - skills
  - prompts
  - usage
  - desktop
---

# CC Switch — Human-facing AI Coding Control Plane Candidate

## Status

**Stage 1: A+**  
**Stage 2: A (provisional)**  
**Decision: CANDIDATE**  
**Implementation: HOLD**

Earlier conversation treated CC Switch mainly as a provider/model switcher.

The current project is materially broader and deserves a standalone evaluation.

## 1. Officially confirmed scope

Official repository:

- https://github.com/farion1231/cc-switch
- MIT license
- Tauri 2 desktop application
- Windows 10+, macOS and Linux support

Current official README describes support for:

- Claude Code
- Claude Desktop
- Codex
- Gemini CLI
- Grok Build
- OpenCode
- OpenClaw
- Hermes
- Pi
- MiniMax Code
- Kimi Code

Capabilities include:

- provider switching
- local routing and failover
- multi-provider aggregation
- MCP management
- Skills management
- prompt management
- session reading/search
- usage / token / spending tracking
- quota and balance display
- tool installation / upgrade management
- WebDAV / S3-compatible cloud sync
- Hermes memory editing

## 2. Best AI-Harness interpretation

CC Switch is not merely a router.

Useful distinction:

```text
OmniRoute
= routing / provider-selection engine

Token Harness
= quota / context optimization

CC Switch
= Human-facing operator console for AI coding tools
```

That Human-facing control-plane role is the most interesting candidate function.

## 3. Potential value

For a non-engineer or mixed-tool environment, CC Switch could reduce manual editing of:

- JSON
- TOML
- YAML
- MCP configs
- provider endpoints
- Skills directories
- prompt files

Potential AI-Harness role:

```text
Human
  ↓
CC Switch GUI
  ↓
Codex / Claude / Hermes / Gemini configuration
  ↓
AI-Harness policy remains authoritative
```

It could become a practical operator surface without replacing the Harness itself.

## 4. Important security boundary

CC Switch manages sensitive local state.

The official README documents storage such as:

- SQLite configuration database
- provider data
- OAuth credential files
- Codex OAuth state
- backups
- Skills
- local logs
- cloud-sync configuration

It also rewrites supported AI tools' configuration files.

Therefore a future trial requires careful review of:

- credential storage
- permissions
- backup contents
- cloud-sync exclusions
- logs
- update mechanism
- deep-link imports
- local routing behavior

Do not place the configuration directory in cloud storage until sensitive-file behavior is fully understood.

## 5. Terms-of-service boundary

The official README itself warns that using some subscription accounts outside official clients may violate vendor terms.

Therefore:

- do not assume every account mode is allowed,
- prefer official API / supported authentication paths,
- verify terms at use time,
- do not use third-party relay/provider offers merely because they are listed in the README.

## 6. Overlap with existing candidates

### OmniRoute

Overlap:

- provider switching
- routing
- failover

Difference:

- OmniRoute is routing-engine oriented.
- CC Switch is UI/control-plane oriented.

### Token Harness

Overlap:

- usage / quota visibility

Difference:

- Token Harness focuses on optimization and allowance efficiency.
- CC Switch focuses on broad configuration and operational management.

### Hermes

CC Switch can manage some Hermes-facing configuration and memory surfaces, but does not replace Hermes itself.

## 7. Suggested secondary evaluation

Before any install:

1. inspect release provenance and update mechanism,
2. inspect credential storage implementation,
3. identify which files can enter cloud sync,
4. verify local-only operation,
5. verify rollback/backups,
6. compare direct provider switch against OmniRoute,
7. compare usage reporting against Token Harness,
8. test only with dummy API credentials first.

## Decision

**Stage 1 A+ / Stage 2 A provisional / CANDIDATE / IMPLEMENTATION HOLD**

The strongest hypothesis is:

> CC Switch may be useful as a Human-facing operator console above multiple coding-agent tools.

Do not treat it as the new HarnessRouter without separate evidence.

No installation, OAuth account connection, provider credential import, cloud sync, routing, or config rewrite is authorized by this record.
