# sokudan-ja-310m

Status: CANDIDATE / NOT YET APPROVED
Reviewed: 2026-09-30

## Identity
- Developer / publisher: GeneLab
- Model: `GeneLab/sokudan-ja-310m`
- Class: Japanese typed decision / text classification model
- Backbone: `sbintuitions/modernbert-ja-310m`
- Total parameters reported by model card: 314,614,274
- License: Apache-2.0
- Source: https://huggingface.co/GeneLab/sokudan-ja-310m
- Code: https://github.com/hiroki-abe-58/sokudan

## Distinguishing characteristic

The model is designed to accept Japanese state text plus typed questions and return bounded answers and probabilities without free-text generation.

This makes it attractive where:
- output labels are known in advance;
- parsing free-form LLM text is undesirable;
- low CPU cost and fast classification are more valuable than open-ended reasoning.

## Strong-fit tasks
- importance: low / medium / high
- relevance: low / medium / high
- category routing
- boolean gates
- ordinal scores
- narrow multi-label or repeated bounded judgments

## Weak-fit tasks
- open-ended economic analysis
- causal market forecasting
- multi-document synthesis with contradictory evidence
- tasks requiring detailed explanation or flexible tool use

## Important caution

"No free-text generation" does **not** mean "cannot be wrong."

The main failure mode changes from generated hallucination to misclassification / poorly calibrated confidence / domain mismatch.

The model is new and the public evidence is not a BBB financial-news benchmark. Treat it as a candidate until evaluated on project-specific data.

## Installation note

As of 2026-09-30, Sokudan v0.3.0 is available from PyPI and the official README documents:

- `pip install sokudan`
- `pip install "sokudan[serve]"` for the local HTTP server
- supported Python: >=3.11,<3.14

For Windows CPU use, the package uses the torch backend. Projects running Python 3.14 should isolate Sokudan in a separate Python 3.11-3.13 environment instead of forcing the main application interpreter to downgrade.

## Harness selection note

Prefer this model over a generative LLM when the decision space can be fixed in advance and a typed answer is sufficient.
