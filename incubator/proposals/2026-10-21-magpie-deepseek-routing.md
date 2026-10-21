---
document_type: research_evaluation
date: 2026-10-21
timezone: Asia/Tokyo
subject: Magpie / DeepSeek V4.1 Flash routing proposal
stage_1_rank: A
decision: CANDIDATE_MAGPIE / HOLD_DEEPSEEK
implementation: NOT APPROVED
origin: Human-supplied X post by @codexneo4 (2112742167567540284); Human approved archival
branch: development
tags: [model-routing, gateway, magpie, deepseek, codex, opencode, hermes, harnessrouter, cost, security]
---

# Magpie + DeepSeek — model routing research (no implementation)

## Source and claim boundaries

- Original X post: https://x.com/codexneo4/status/2112742167567540284
- Magpie upstream: https://github.com/yetone/magpie
- Magpie documentation: https://usemagpie.ai/docs/start
- DeepSeek API pricing / model terms: consult current official DeepSeek API docs at evaluation time.

The post proposes GPT-6 Astra as a higher-level decision maker, DeepSeek V4.1 Flash for coding/execution, Magpie for routing, and WorkBuddy AI / OpenCode as development environments. Its claim that token restrictions are effectively eliminated is **not established**. This record does not certify any named model's availability, free quota, integration, or the posted performance claims.

## Preliminary verified/documented features

From the Magpie upstream README (documentation inspection only):
- Local gateway to configure model/provider endpoints for multiple coding agents, including Codex, Claude Code and OpenCode.
- Supports model selection and routing groups/failover between providers/accounts.
- Documents Windows, macOS, Linux, Docker and Termux operation.
- Lists Hermes Agent and WorkBuddy among supported agent integrations.
- MIT license claimed in upstream README; verify actual license and release before adoption.
- Some modes discover local sign-in/session credentials. This creates privacy, security, and account-terms concerns.

Not independently verified by runtime tests:
- Actual routing reliability and provider compatibility for specific versions.
- Any claim that DeepSeek V4.1 Flash is perpetually free. Official API usage can incur fees; free access via third parties is conditional and must be verified separately.
- Ability to use ChatGPT Plus/Pro subscription credentials across third-party tools under current terms.
- Automatic strategy delegation from GPT-6 Astra to DeepSeek: this is an **architecture proposal**, not an upstream-guaranteed workflow.
- Any bypass of token limits or quotas.

## AI-Harness relevance and overlap

Potentially useful as a **replaceable candidate** behind HarnessRouter for provider/model selection. Distinguish:
- AI-Harness: Rules, Access, provenance, evaluation and Human approvals.
- HarnessRouter: task classification, escalation, provider/model routing.
- Magpie: potential gateway / account-and-model routing implementation, not policy authority.
- Local inference: Ollama and/or future local model, not provided by Magpie itself.

Existing related record: `incubator/proposals/2026-09-21-jev-context-filter-adoption-model.md`.
Jev was assessed as a possible **context filter**, not a full gateway. Compare roles rather than merging concepts.

Future Hermes Local Agent (currently Phase 0 / NOT IMPLEMENTED) could be a compatibility test target; the Magpie README listing alone does not establish working integration on the user's PC.

## Evaluation

- **Magpie: A / CANDIDATE** — relevant, existing OSS functionality may avoid redundant HarnessRouter development. Do not adopt until security, account terms, compatibility, costs and measured reliability are checked.
- **DeepSeek V4.1 Flash: A / HOLD** — possible low-cost execution model, but no validated zero-cost entitlement, quality benchmark, or current API-cost guarantee for this use case.
- **Social post headline: promotional / unverified** — do not treat "token limits collapsed" as an engineering fact.

## Minimal comparison plan (separate Human approval required)

1. Review Magpie code paths for credential discovery/storage, local gateway exposure, logging and outbound traffic.
2. Verify model/API provider names, free quotas, pricing and current usage terms from official sources.
3. Compare Magpie against a minimal self-built HarnessRouter adapter and any existing routing features.
4. In an isolated environment, test routing, failover, error propagation and explicit approval boundaries using test accounts/keys and capped spend.
5. Measure operational complexity, latency, error rate, real cost and local hardware requirements.

## Boundary

Research-only GitHub note approved by Human on 2026-10-21. No software installed, accounts linked, credentials read, API keys provisioned, subscription bypass attempted, code or Core/Trinity/Hermes/BBB implementation changed.
