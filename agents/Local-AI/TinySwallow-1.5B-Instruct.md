# TinySwallow-1.5B-Instruct

Status: CANDIDATE / NOT YET APPROVED
Reviewed: 2026-09-29

## Identity
- Developer: Sakana AI / Swallow Team
- Model: `SakanaAI/TinySwallow-1.5B-Instruct`
- Class: Japanese autoregressive generative LLM
- Size: 1.5B parameters
- Distillation method: TAID
- Teacher / student lineage documented by the model card: Qwen2.5-32B-Instruct -> Qwen2.5-1.5B-Instruct
- License: Apache-2.0
- Source: https://huggingface.co/SakanaAI/TinySwallow-1.5B-Instruct
- Project information: https://sakana.ai/taid-jp/

## Distinguishing characteristic

This is the flexible option in the current Local AI catalog.

Unlike a bounded classifier, it can:
- summarize;
- follow changing natural-language instructions;
- extract a custom schema;
- interpret ambiguous phrasing;
- reconcile context across multiple sentences.

## Strong-fit tasks
- fallback after a bounded classifier reports low confidence
- short Japanese summarization
- context extraction
- interpretation of nuanced statements
- prototyping a schema before a dedicated classifier exists

## Weak-fit tasks
- high-volume classification where labels are fixed
- tasks requiring fully deterministic output
- direct high-impact action authority
- workloads where CPU latency is more important than flexibility

## Important caution

Because this is a generative model, output validation and schema checks are required.
It has greater parsing and hallucination/error risk than a bounded classification model.

The model card describes it as an experimental prototype for research and development. Project-specific testing is required before operational use.

## Harness selection note

Use as a controlled fallback, not as the first tool for every text task.
