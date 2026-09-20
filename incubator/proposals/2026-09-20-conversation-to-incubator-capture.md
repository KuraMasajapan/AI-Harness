---
status: proposal
created: 2026-09-20
origin: ChatGPT / AI-Harness operating discussion
---

# Conversation-to-Incubator Capture

## Signal

Useful design ideas are often created during ordinary conversation before they become formal tasks, Lessons, specifications, or implementation work.

If a discussion reaches AI-Harness-level value but is left only inside a chat transcript, semantic discovery, later synthesis, and cross-project reuse become unnecessarily difficult.

## Proposal

Adopt a lightweight habit:

```text
useful conversation signal
→ preserve a concise proposal note promptly
→ GitHub durable storage
→ Obsidian semantic discovery
→ later synthesis / review if the idea becomes important
```

The purpose is not to archive every conversation.

The purpose is to avoid losing ideas that are already valuable enough to influence future Harness design.

## Capture threshold

A conversation fragment is a candidate when it introduces one or more of:

- a reusable mechanism
- a recurring operational problem
- a new role or orchestration pattern
- a measurable optimization opportunity
- a privacy or audit principle
- a promising connection between existing proposals

Weak or speculative ideas may still be captured because the Incubator is explicitly non-authoritative.

## Obsidian role

Obsidian should be used actively as the human-facing exploration layer.

GitHub remains durable storage and history.

Smart Connections or similar semantic discovery may surface relationships, but similarity alone must not promote a proposal or alter the Harness.

## Important limits

Do not automatically promote captured conversation notes to Lessons, Workflow, or Core.

Do not store private or sensitive conversation content in the public repository.

Prefer concise abstraction over verbatim chat logs when the original discussion contains irrelevant or private material.

## Why preserve this proposal

A system designed to learn from its own operation should not depend on humans remembering which chat contained an important idea.

The capture step should be cheap enough that preserving a useful signal is easier than rediscovering it later.
