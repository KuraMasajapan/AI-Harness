# Local AI Catalog

Status: CANDIDATE CATALOG
Updated: 2026-09-29

## Purpose

This directory is the AI-Harness-wide catalog for local AI models.

Local AI is not treated as a smaller copy of a cloud chat model. Select the model class according to the job:

- deterministic code for facts and numeric rules
- classifier / decision model for bounded labels
- embedding model for semantic search, similarity, deduplication, and retrieval
- small generative LLM for ambiguous language that cannot be handled reliably by the above
- cloud AI only when the local pipeline cannot handle the task economically or reliably

The aim is to make future AI selection task-based rather than model-name-based.

## Selection dimensions

When comparing a new local model, record at least:

1. **Model class** — classifier / embedding / generative / multimodal / other
2. **Output form** — typed label, probability, vector, free text, JSON, etc.
3. **CPU suitability** — whether GPU-less operation is realistic for the intended workload
4. **Japanese capability**
5. **Context size**
6. **Parsing burden** — whether output needs fragile text parsing
7. **Failure mode** — misclassification, semantic retrieval error, hallucinated generation, etc.
8. **Confidence semantics** — what a probability or score actually means and whether it is calibrated
9. **Best-fit task**
10. **Poor-fit task**
11. **License**
12. **Maturity / evaluation evidence**
13. **Project-specific benchmark result**

Do not infer that a smaller model is safer merely because it is deterministic in output format. A classifier can still classify incorrectly.

## Current candidates

| Model | Class | Size | Distinguishing strength | Best use in Harness | Main caution | Status |
|---|---|---:|---|---|---|---|
| [sokudan-ja-310m](./sokudan-ja-310m.md) | Typed decision / text classification | ~314.6M | No free-text generation; typed choice/score/bool style decisions with probabilities in one forward pass | Fast bounded classification, routing, importance/relevance judgments | Very new; not a finance-specific benchmark; can misclassify even though it does not generate prose | Candidate |
| [PLaMo-Embedding-1B](./PLaMo-Embedding-1B.md) | Japanese embedding | 1B | 2048-dim semantic vectors; retrieval/classification/clustering use | Similarity search, duplicate detection, historical analogue retrieval, clustering | Does not itself reason or decide causality; label/reference design matters | Candidate |
| [TinySwallow-1.5B-Instruct](./TinySwallow-1.5B-Instruct.md) | Small generative LLM | 1.5B | Japanese instruction following with much greater flexibility than fixed classifiers | Ambiguous context fallback, summarization, structured extraction when bounded models fail | More CPU cost, output parsing, and generative error/hallucination risk | Candidate |

## Practical differentiation

### Use a classifier when:
- the answer space can be defined in advance;
- output should be a label / boolean / bounded score;
- speed and predictable output format matter more than open-ended reasoning.

### Use an embedding model when:
- the question is "what is this similar to?";
- you need retrieval from historical cases;
- duplicate / near-duplicate detection matters;
- you want semantic clustering without generating text.

### Use a small generative LLM when:
- meaning depends on nuanced wording;
- multiple sentences must be summarized or reconciled;
- the required schema changes often;
- the bounded classifier reports low confidence or UNKNOWN.

### Use deterministic code instead of AI when:
- the source is already structured;
- arithmetic or threshold rules are sufficient;
- the answer can be reproduced exactly from numeric inputs.

## Recommended escalation pattern

```text
Structured data
  -> deterministic code

Unstructured text
  -> embedding / dedup / retrieval
  -> typed classifier
  -> if low confidence or unsupported context:
       small generative LLM
  -> if still unresolved and task value justifies cost:
       cloud AI
```

This is a pipeline, not an autonomous multi-agent swarm.

## Evaluation rule

No local model becomes "approved" because of a public benchmark alone.

Before project use:
- build a project-specific labeled dataset;
- compare against a Human / trusted reference;
- measure accuracy by task category;
- measure latency and memory on the actual target PC;
- test UNKNOWN / abstention behavior;
- record false positives and false negatives;
- evaluate confidence calibration;
- keep a deterministic fallback.

## Source references

- sokudan-ja-310m: https://huggingface.co/GeneLab/sokudan-ja-310m
- sokudan code: https://github.com/hiroki-abe-58/sokudan
- PLaMo-Embedding-1B: https://huggingface.co/pfnet/plamo-embedding-1b
- TinySwallow-1.5B-Instruct: https://huggingface.co/SakanaAI/TinySwallow-1.5B-Instruct
- TinySwallow / TAID: https://sakana.ai/taid-jp/

## Project links

- BBB local AI role: ../../projects/BBB/agents/Local-AI/README.md
