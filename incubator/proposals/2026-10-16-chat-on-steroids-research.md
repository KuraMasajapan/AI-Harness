---
document_type: research_evaluation
date: 2026-10-16
subject: Chat on Steroids
stage_1_rank: A+
stage_2_rank: A
decision: HOLD
relationship: COMPARE
implementation: NOT APPROVED
---
# Chat on Steroids — research candidate

## Signal
An X post claims that Chat on Steroids turns ChatGPT into a Codex-like development environment while consuming ChatGPT rather than Codex quotas, and calls GPT-6 effectively unlimited. **Treat those quota and unlimited-use claims as unverified, not an entitlement or approved workaround.**

Upstream candidate: https://github.com/totec448-spec/chat-on-steroids

## Evaluation
- **Stage 1 A+**: relevant to agent development workflows, conversation continuation, and inexpensive use of existing subscriptions.
- **Stage 2 provisional A / HOLD**: overlaps current ChatGPT Work, Codex and GitHub-connected workflows. Incremental value and terms/quotas are not demonstrated.
- Investigate compact/resume, local execution logs, access boundaries, maintenance, costs, and whether the software actually uses supported official interfaces.
- Do not install, grant filesystem/shell permissions, or rely on quota-bypass claims without independent validation.

## Related research
- [LCU desktop-control candidate](2026-10-16-lcu-hermes-desktop-control.md) — separate software, not equivalent.
- [Hermes reinforcement](../../projects/Hermes_Local_Agent/research/2026-10-15-hermes-agent-reinforcement.md) — existing local agent project; compare overlap rather than silently adopting another agent.

## Boundary
Research only. No Core/Workflow promotion, runtime deployment or authorization changes.
