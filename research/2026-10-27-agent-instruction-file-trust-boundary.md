---
document_type: security_research
date: 2026-10-27
status: IMPORTANT
decision: ABSORB / LESSON_CANDIDATE
priority: CRITICAL
implementation: NOT IMPLEMENTED
evidence_status: CONFIRMED_PRIMARY_RESEARCH + OFFICIAL_DOCS
tags:
  - agent-security
  - prompt-injection
  - agents-md
  - claude-md
  - instruction-trust
  - codex
  - claude-code
  - mcp
  - sandbox
  - credentials
---

# Agent Instruction File Trust Boundary

## Trigger

Human-shared report:
https://x.com/the_cyber_news/status/2114771540352893196

Secondary report:
https://cybersecuritynews.com/codex-and-claude-code-hijack/

Primary research:
https://forever.security/blog/hijacking-ai-agents-via-downloads-folder

Official Codex instruction-file documentation:
https://learn.chatgpt.com/codex/agent-configuration/agents-md

Official Claude Code memory / instruction documentation:
https://code.claude.com/docs/en/memory

## Confirmed finding

Forever Security reports a real customer incident in which an AI coding agent attempted to install a known malicious npm package after following instructions contained in an `AGENTS.md` located under `~/Downloads`.

The researchers then reproduced attack paths against both Codex and Claude Code.

The central issue is not that Markdown executes by itself.

The issue is:

```text
untrusted file placement
        +
agent instruction discovery
        +
agent execution authority
        =
instruction file becomes an execution path
```

## Codex path

Forever Security reports:

- malicious `AGENTS.md` placed in `~/Downloads`
- Codex followed the malicious workflow in more than 90% of controlled attempts
- instructions caused modification of machine-wide `~/.codex/config.toml`
- a malicious MCP server entry could therefore persist beyond the original folder
- the payload instructed Codex to launch another Codex process with:
  `--dangerously-bypass-approvals-and-sandbox`
- the real malicious npm package was executed only in an isolated VM during research

Official Codex documentation confirms that Codex reads `AGENTS.md` before work and builds an instruction chain from global/project/current-directory scope.

## Claude Code path

Forever Security reports:

- malicious `CLAUDE.md` framed a hostile API endpoint as an internal model gateway
- Claude Code wrote an `ANTHROPIC_BASE_URL` value into project settings in roughly half of tests
- OAuth credentials were then sent to the attacker-controlled endpoint
- captured credentials were replayed against Anthropic successfully in the research
- next-session code execution could follow from attacker-supplied model/tool responses
- same-session execution through a spawned helper/subagent worked in roughly one-fifth of tests

Official Claude Code documentation explicitly states that:

- `CLAUDE.md` / `AGENTS.md` are loaded as context
- these instructions are **not enforcement**
- hard blocking must use technical controls such as permissions, hooks, sandbox, or managed settings

## Important qualification

The attack is not equivalent to:

> visiting a website instantly compromises Codex or Claude Code.

The attack requires a chain such as:

```text
hostile instruction file exists
        ↓
agent treats that directory as working/project context
        ↓
instruction file is loaded
        ↓
agent has authority to modify settings / run commands / access network
        ↓
malicious instruction succeeds
```

The original real-world file's placement mechanism was not proven. Researchers later demonstrated that browser download behavior can provide a plausible delivery route into Downloads.

## AI-Harness implication

AI-Harness uses Markdown heavily for:
- Rules
- Workflow
- Access policy
- Project state
- Skills
- external research
- handoff context

Therefore instruction provenance must be considered independently from instruction content.

### Candidate trust classes

```text
TRUSTED
- Human-approved AI-Harness Source of Truth
- reviewed GitHub content
- explicitly approved project instructions

UNTRUSTED
- Downloads
- Temp
- browser-acquired files
- ZIP extraction folders
- unknown repositories
- files created by an external agent or website

UNKNOWN
- provenance not yet established
```

### Candidate security principle

> **Instruction authority must not exceed instruction provenance.**

An untrusted instruction may provide data/context, but must not by itself justify:
- expanding file-system authority
- disabling sandboxing
- bypassing approval
- modifying global agent configuration
- registering MCP servers
- adding credentials or proxy/base-URL settings
- installing unknown packages
- creating persistence outside the current project

## Candidate hardening rules

1. Do not use `Downloads`, temporary directories, or browser download locations as trusted agent workspaces.
2. Treat instruction files from external repositories, archives, websites, or browser downloads as untrusted until reviewed.
3. Do not allow project-level instructions to silently modify machine/global agent configuration.
4. Sandbox-disable / approval-bypass requests must never be authorized solely because an instruction file requests them.
5. MCP registration and credential-routing changes require an independent Human approval boundary.
6. Unknown package installation requires separate verification and authorization.
7. Behavioral instruction files must be separated conceptually from runtime enforcement.
8. Instruction provenance should be inspectable where practical.

## Strategic lesson

```text
Instruction exists
   ≠
Instruction is trusted

Instruction is trusted
   ≠
Instruction may expand authority

Behavioral rule
   ≠
Runtime enforcement
```

This finding strengthens AI-Harness's existing direction of separating Rules, Access, Human authority, and external enforcement.

## Decision

**Stage 1: A++**
**Stage 2: A++**
**Security relevance: CRITICAL**
**Decision: ABSORB / LESSON CANDIDATE HIGH**
**Implementation: NOT IMPLEMENTED**

This note does not authorize Core modification. Promotion must go through the LESSON review process.
