---
status: proposal
created: 2026-09-20
origin: ASTRA efficiency / public-data discussion
---

# Efficiency Telemetry and Public-Safe Metrics

## Signal

Optimization is difficult to evaluate from impressions alone.

The current mostly-default workflow can serve as a baseline, but future improvements need comparable measurements across heterogeneous tasks.

## Proposal

Generate a lightweight **Efficiency Report** after each significant task.

Preserve fixed raw metrics where possible, then allow AI to classify the task into a comparison group.

Candidate raw metrics:

- anonymous task / run ID
- task type
- executor / model family when observable
- usage start / end / delta
- elapsed time
- AI instruction count
- Human intervention count
- retry count
- changed-file count
- diff size
- test count / pass count
- unresolved count
- optimization techniques used
- quality regression observed: yes / no / unresolved

Possible derived metric:

```text
Work Compression Ratio
= comparable baseline ASTRA cost / current ASTRA cost
```

This should never replace the underlying metrics.

## Comparing different tasks

Tasks are not naturally identical.

Use:

```text
fixed raw metrics
+ AI-assigned task_type / complexity / comparison_group
+ periodic independent audit
```

Do not force unrelated work into one universal score.

## Public / private separation

Design public metrics to be privacy-safe from the start.

Public data may include normalized operational numbers and anonymous task categories.

Private audit evidence may include detailed logs, prompts, repository paths, and other context needed for internal verification.

Do not publish:

- personal information
- API keys
- private repository content
- private file names when sensitive
- account identifiers
- raw private conversations

## Periodic audit

Routine measurement may be lightweight and largely automatic.

Periodically assemble an independent audit team to check:

- metric correctness
- task classification
- comparison-group selection
- hidden quality regression
- cherry-picked baselines
- public-data privacy

## Why preserve this proposal

A long-running dataset could make Harness optimization measurable and produce useful public evidence about AI-team efficiency rather than anecdotal claims.
