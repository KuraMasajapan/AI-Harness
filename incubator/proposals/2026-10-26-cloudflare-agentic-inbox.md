---
status: proposal
created: 2026-10-26
decision: CANDIDATE
priority: B
implementation: HOLD
---

# Cloudflare Agentic Inbox — AI Mailbox Candidate

Source: https://github.com/cloudflare/agentic-inbox

## Confirmed
Self-hosted email client on Cloudflare Workers with:
- Email Routing receive
- Email Service send
- per-mailbox Durable Object + SQLite
- R2 attachments
- Workers AI agent
- email read/search/draft tools
- auto-draft on incoming mail
- explicit confirmation before send
- MCP endpoint

## AI-Harness relevance
Potential future **AI-dedicated mailbox**, avoiding broad access to an existing personal Gmail account.

## Risks / limits
- Requires Cloudflare account and domain.
- Production trust boundary is Cloudflare Access.
- README states there is no per-mailbox authorization behind that boundary; MCP clients can operate on any mailbox with mailboxId.
- Email is a high-risk prompt-injection surface.

## Decision
**CANDIDATE — B / later experiment**

No deployment or email routing changes.
