# heldkeys — inventory of credentials reachable by AI agents

- Recorded: 2026-10-18
- Origin: Grok daily observer, Airtable Harness Inbox `recpxVSYqooBXbqyw`; Observer Runs `recUiJWurDxQvMyOr`
- Stage 1 (Grok): MEDIUM
- Stage 2 (ChatGPT): **A / CANDIDATE**
- Implementation: **HOLD / NOT IMPLEMENTED**
- Human decision: **SAVE research record** (2026-10-18); no adoption or installation approval
- Evidence: CONFIRMED for repository and documented capabilities; UNVERIFIED for exhaustive detection, implementation safety and Windows compatibility

## Source and confirmed claims

- Primary: https://github.com/hugomn/heldkeys
- Official README reviewed on 2026-10-18.
- Open-source CLI to inventory **credentials that an agent process could reach** in its execution context, including environment variables, cloud and developer CLI login stores, git/package tokens, SSH, `.env` and MCP configs.
- Also examines potentially risky AI-agent use in GitHub Actions and environment access such as Docker sockets, Kubernetes tokens and metadata endpoints.
- Maintainer claims default operation is read-only, with no telemetry, no secret values printed, and only explicitly requested output files created; these are project claims, not an independent code/security audit.
- README describes Linux/macOS binary use; the planned Windows-first environment requires separate compatibility review.
- A credential inventory is **not** a permission enforcement layer and cannot guarantee that every secret is detected.

## Why relevant to AI-Harness

**A / CANDIDATE** as a possible narrow security audit tool, not a new general-purpose agent control plane:
- `core/ACCESS.md` and existing Human approval rules — verify practical exposure without replacing authority boundaries.
- `incubator/proposals/2026-10-16-grok-agent-permission-approval-hold.md` — previously **Human-deferred** agent permission/approval investigation. That deferral remains in force; saving heldkeys does not resume it.
- `projects/Hermes_Local_Agent/` — potential preflight check for future local execution.
- `incubator/proposals/2026-10-18-grokbot-local-agent-task-webhook.md` — security complement for task handoff agents that may execute shell commands.

## Risks and limits

- A scan may omit unrecognized credentials, remote grants or other capabilities; absence of findings does not prove safety.
- Even fingerprints, file paths and names may reveal sensitive environment metadata; treat reports as sensitive.
- Scanning agent-accessible files requires careful trust boundaries and must not export tokens or credential reports to cloud models by default.
- Tool installation, code provenance, release integrity, OS support and network behavior must be independently checked before any real run.

## Future research (not approved for execution)

1. Compare heldkeys against simpler manual access inventory and native OS/agent permission controls.
2. Review implementation and threat model, supported platforms, installation trust and potential data exposure.
3. In a **dummy-credential sandbox only**, test detection, false positives, omissions and whether secret values ever leak to logs.
4. Only after explicit Human approval consider a narrowly scoped local preflight check; keep access denial/approval separate from reporting.

**Boundary:** Research note only. No installation, credential scan, environment access, Core/ACCESS change or restart of deferred permission research was authorized.
