# Google Gemini API CLI — 既存エージェント向けマルチモーダルAPI呼び出し・Managed Agents

- Date: 2026-11-23
- Source repository: https://github.com/google-gemini/gemini-api-cli
- Primary source: README.md; docs/self-hosted/README.md; GitHub releases v0.5.0; Gemini CLI README; Google API pricing
- Stage 1: A++
- Stage 2 Final: A+ (public implementation/docs verified; no practical test of paid endpoints/sandbox)
- Evidence: CONFIRMED for code/docs/release/license, UNVERIFIED for user-specific API entitlement, costs, runtime quality, security of a deployment
- Decision: CANDIDATE
- Status: KNOWLEDGE / FUTURE VALIDATION CANDIDATE / NOT IMPLEMENTED
- Authorization: Human standing approval for B+ research proposal saves only; no implementation, installation, app credentials, or Core adoption authorized.

## Identity and freshness

Official Google Gemini organization's repository, created 2026-04-29, Go source, Apache-2.0 license, public experimental beta, latest release verified v0.5.0 published 2026-11-20 (as of 2026-11-23). README warns about breaking changes and recommends pinning version in CI. Google does not accept external PRs to this repository currently.

## What it does

Stateless CLI executable `gemini-api` bridges any shell-capable host agent (Codex, Claude Code, Antigravity, OpenClaw, Hermes) to Gemini API / Interactions API. It does not replace agent's planning or context system. Key commands:
- generate, image, tts, music, video (model-based media and text outputs)
- analyze (PDF/images/audio/video/CSV/YouTube), transcribe (md/text/json/SRT)
- agent run/status/cancel and managed agent creation + background interaction ID
- files API, model catalog, voice management
- environments create/connect/poll/serve, webhooks, credentials, triggers
- machine introspection: --usage KDL command tree, --schema JSON Schema, --agent-mode, --no-interactive, --dry-run redacted HTTP request, --output-format json/toon, --jq, explicit exit codes.
- Credentials: GEMINI_API_KEY env var, OS credentials/secure config via configure; do not put secrets in git/logs.

CLI itself runs on Windows/macOS/Linux (Go binary) but inference is via Google online API. No inference offline. API models listed in README are examples and may change. Multi-modal output and managed agents are separate billable services.

## Crucial difference from Gemini CLI

Official https://github.com/google-gemini/gemini-cli README (2026-11) says standard `gemini` terminal coding agent is now for enterprise Code Assist; free personal / Google AI Pro & Ultra accounts transitioned to Antigravity CLI effective 2026-06-18. `gemini-api` is stateless REST API interface, not a coding harness, and requires an API key. Google AI subscription is not equivalent to unrestricted Gemini Developer API free usage.

## Self-hosted managed agent capability & security

Docs: https://github.com/google-gemini/gemini-api-cli/blob/main/docs/self-hosted/README.md
- Managed agent can execute file operations and bash in user's own containers/VM via outbound-only HTTPS, no inbound ports.
- Single-worker connects using a scoped environment key; split poller/worker architecture uses short-lived lease tokens in untrusted containers.
- Structured file read/write confined to --root-dir via os.Root, but execute_bash is arbitrary shell execution NOT effectively confined by --root-dir. Explicit upstream CRITICAL warning: isolate in VM/microVM/container; `--disable-bash` where unnecessary.
- Hardening: non-root user, drop Linux capabilities, no-new-privileges, egress allowlist, block cloud metadata, no project-wide API key inside worker.
- Can integrate with self-hosted execution, but this is not a free VPS, and API billing and infra provider billing are separate.

## Cost and limitations

- CLI install is free; Gemini API depends on model/endpoint, some free tier and some paid only. Check https://ai.google.dev/gemini-api/docs/pricing and https://ai.google.dev/gemini-api/docs/rate-limits before any call. Deep Research and Managed Agents may bill all model invocations including intermediate steps.
- Not equivalent to free unlimited Google AI Pro account; API key and API plan govern access.
- Managed agent interaction may be background/triggered, but no promise of 24/7 free operation. Files API retention documented as 48h in README.
- Untrusted tool outputs & prompts, malicious repos, prompt injection, secret exfiltration via shell, data uploads to Google, API cost overruns need formal gates.

## Harness impact / related proposals

- Existing AI-Harness orchestrator (A/B/C evaluations, usage, Human Disposition), Codex CLI, Muse, Hermès agent designs can delegate task-specific Gemini inference or media creation using a single binary without replacing host agent.
- Strongest incremental value: machine-readable introspection (`--usage`, `--schema`), dry-run preflight, JSON/TOON and explicit exit codes; typed CLI wrapper + usage metering + approval gate.
- Images/voice TTS for avatar and 3D room, media ingestion/research, external model independent peer review are relevant.
- More consequential: self-hosted environment worker and managed agent handoff; isolate separately from access-controlled Harness and TRINITY, sandbox, writer lock, deterministic execution logs. Never unilaterally replace current architecture.
- Prior related candidate categories (not exact duplication found among top-level proposal filenames): audio/TTS OSS, Codex environment, Token Sharing SIWC, cloud free workspaces. SIWC pertains OpenAI plan and is not a Gemini auth method.
- Disposition: CANDIDATE for constrained integration study, NOT IMPLEMENTED.

## Proposed validation (read-only / no secrets)

1. Download pinned official release (v0.5.0 at evaluation), verify checksum. Avoid executing remote curl | sh without inspection.
2. Run `gemini-api --help`, `gemini-api --usage`, `gemini-api image --schema`, `gemini-api generate "hello" --dry-run --output-format json` without API keys and network, inspect outputs.
3. Implement sample candidate adapter interface conceptually in incubator; contrast Gemini SDK / direct REST / Antigravity CLI by integration cost.
4. Before actual Gemini API execution, Human to confirm account, credentials, API rate/price, budget cap; execute smallest allowed free test with logging.
5. For managed agents in self-hosted environments, separate container sandbox, deny bash unless needed, audit egress, credentials/leases, output redaction, concurrency and writer lock.
6. Keep research documentation separate from implementation and deployment.

## References

- https://github.com/google-gemini/gemini-api-cli
- https://github.com/google-gemini/gemini-api-cli/blob/main/README.md
- https://github.com/google-gemini/gemini-api-cli/blob/main/docs/self-hosted/README.md
- https://github.com/google-gemini/gemini-api-cli/releases/tag/v0.5.0
- https://github.com/google-gemini/gemini-cli/blob/main/README.md
- https://ai.google.dev/gemini-api/docs/pricing

## Recall triggers
Gemini API CLI, gemini-api, Gemini CLI, Antigravity CLI, Managed Agents, Interactions API, google-gemini, A2A, API cost, media generation, agent host, lease token, self-hosted, sandbox
