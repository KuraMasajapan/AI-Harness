---
status: proposal
created: 2026-10-26
decision: CANDIDATE
priority: A-/B+
implementation: NOT IMPLEMENTED
---

# Nango — Agent Integration Layer Candidate

Source: https://github.com/NangoHQ/nango

## Confirmed scope
Nango provides:
- OAuth / API-key connection management
- token refresh
- proxying authenticated API requests
- syncs and webhooks
- actions / write operations
- observability and retries
- 1,000+ API integrations
- MCP / AI tool-calling use cases
- self-hosting options

## AI-Harness relevance
Potential future layer:

Agent
→ Nango
→ external services / APIs

This could reduce repeated custom authentication and integration code.

## Limits
- Large platform; complexity may exceed current needs.
- Free self-hosting has feature limits.
- Credential custody and write permissions require separate ACCESS review.
- Do not add merely because many APIs are supported.

## Decision
**CANDIDATE — future integration reference**

No implementation until a concrete external-service integration gap appears.
