# Grok -> Airtable -> ChatGPT Production v1 Decision

Date: 2026-10-04
Status: APPROVED FOR PRODUCTION v1
Human approval: YES

## Decision

Promote the external observer flow from pilot to production operation.

Runtime path:

`Grok Automation -> Airtable Harness Inbox -> ChatGPT downstream review -> Human decision`

GitHub is not part of the runtime path. It stores the canonical prompt, architecture notes, checkpoints, and change history.

## Why production is justified

- Grok -> Airtable MCP handoff was verified.
- Airtable -> ChatGPT read/review was verified.
- Existing Airtable records were preserved during unattended submission.
- New records entered as NEW.
- Human Approved remained false.
- A real temporal interpretation error was caught by downstream ChatGPT review before adoption.
- The discovered failure mode was converted into explicit prompt guards.
- Final authority remains Human.

## Production v1 boundaries

Grok may:
- discover,
- perform rough evaluation,
- check freshness and evidence,
- deduplicate,
- submit high-value IN_WINDOW candidates as NEW.

Grok may not:
- enable Human Approved,
- modify or delete existing Airtable records during the scheduled run,
- auto-approve,
- alter AI-Harness Core,
- start implementation,
- treat SNS or research claims as final evidence without verification.

ChatGPT:
- independently verifies and organizes candidates when invoked.

Human:
- makes the final adoption / hold / rejection decision.

## Operating mode

Production v1 remains intentionally semi-automatic.

No additional manual pilot rerun is required before use.
The next scheduled 18:00 JST Automation run is the first production run.

## Canonical prompt

See:

`incubator/proposals/grok-ai-technology-observer/AUTOMATION_PROMPT.md`

Status of canonical prompt:

`PRODUCTION v1 / ACTIVE AUTOMATION`
