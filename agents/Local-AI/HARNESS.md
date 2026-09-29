# Local AI Harness

Status: CANDIDATE
Updated: 2026-09-29

## Role

Local AI models are replaceable components used for narrow tasks that benefit from on-device inference, low recurring cost, privacy, or low-latency processing.

They are not granted broad autonomous authority by default.

## Default permissions

A Local AI may:
- classify permitted text;
- create embeddings from permitted text;
- summarize or extract structured fields when explicitly assigned;
- return confidence / uncertainty information when the model supports it;
- propose a result to deterministic application logic.

A Local AI must not by default:
- receive API secrets or credentials;
- change Core rules;
- modify its own production permissions;
- promote itself from research to production;
- directly execute financial trades or other high-impact actions;
- silently convert low-confidence results into high-confidence actions.

## Preferred operating pattern

```text
Input
-> deterministic validation
-> narrow Local AI task
-> schema validation / confidence check
-> deterministic policy
-> Human or project-specific safety gate where required
```

## Selection

See `README.md` in this directory for model differentiation and candidate selection.

Project-specific permission and evaluation rules take precedence over generic capability descriptions.
