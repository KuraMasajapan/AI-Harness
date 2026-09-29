# BBB Local AI

Status: CONCEPT / BENCHMARK CANDIDATES
Updated: 2026-09-29

## Source of model information

The model-level Source of Truth is the Harness-wide catalog:

- [Local AI Catalog](../../../../agents/Local-AI/README.md)
- [sokudan-ja-310m](../../../../agents/Local-AI/sokudan-ja-310m.md)
- [PLaMo-Embedding-1B](../../../../agents/Local-AI/PLaMo-Embedding-1B.md)
- [TinySwallow-1.5B-Instruct](../../../../agents/Local-AI/TinySwallow-1.5B-Instruct.md)

Do not duplicate model facts here unless they are specific to BBB. This file records BBB-specific roles and selection.

## BBB objective

Use a GPU-less Windows PC to process fundamental information efficiently.

Rule:
- API acquisition and structured numeric processing stay deterministic.
- Local AI handles only semantic tasks that ordinary code cannot perform well.
- AI output never becomes a direct trade command.

## Proposed Small Model Pipeline

```text
Economic / news APIs
        ↓
Collector
        ↓
deterministic normalize / numeric rules
        ↓
unstructured text only
        ↓
PLaMo-Embedding-1B (optional)
  dedup / semantic retrieval / past analogue search
        ↓
sokudan-ja-310m
  bounded classification
        ↓
confidence sufficient?
     ├─ YES -> structured signal
     └─ NO / UNKNOWN
              ↓
       TinySwallow-1.5B-Instruct
       controlled context fallback
              ↓
       schema validation
              ↓
Fundamental Policy Engine
        ↓
BBB Risk Manager
        ↓
Paper
```

This is a sequential pipeline, not an autonomous multi-agent swarm.

## Proposed role differentiation

### sokudan-ja-310m — first benchmark target
BBB role:
- event category
- importance
- BTC relevance
- USD/JPY relevance
- hawkish / dovish / neutral / unknown
- risk-on / risk-off / neutral / unknown
- bounded confidence-bearing judgments

Reason to test first:
- small model footprint;
- no free-text generation;
- bounded outputs align with BBB policy-engine input.

Caution:
- public results are not a BBB financial-news benchmark;
- classification errors remain possible;
- do not interpret confidence as guaranteed correctness.

### PLaMo-Embedding-1B — historical context sensor
BBB role:
- news deduplication
- semantically similar historical event retrieval
- clustering
- "what past event looks like this?" lookup

Potential future feature:
retrieve similar past news and pair it with subsequent BTC/JPY, USD/JPY and volatility outcomes.

It should not directly infer that similar wording guarantees similar market impact.

### TinySwallow-1.5B-Instruct — ambiguity fallback
BBB role:
- interpret nuanced statements when bounded classification is insufficient;
- short summarization;
- controlled schema extraction;
- resolve phrasing before passing back to deterministic policy.

It is not the default classifier because it is generative and has higher CPU and validation cost.

## Phase plan

### Phase A — Benchmark only
Do not connect Local AI output to trade behavior.

Build a labeled financial-text test set covering:
- CPI / inflation
- FOMC / Fed statements
- BOJ statements
- employment data
- ETF / crypto regulation
- exchange / crypto-specific events
- geopolitical events
- ambiguous / irrelevant / low-signal news

Measure:
- per-category accuracy
- false positive / false negative rate
- abstention / UNKNOWN quality
- confidence calibration
- CPU latency
- RAM usage
- batch throughput

### Phase B — Shadow / Sandbox
Run Local AI beside Paper trading.
Record classifications and subsequent market behavior, but do not alter orders.

Feed results into Fundamental Confidence Ledger.

### Phase C — Risk-only influence
Only after evidence supports it:
- pause new entries around high-risk events;
- reduce position size;
- shorten/extend risk TTL;
- never issue direct BUY / SELL from Local AI.

### Phase D — Selective cloud escalation
Only unresolved high-value cases may be sent to a cloud AI.
Cloud use should be measured against cost and actual value added.

## Safety

- UNKNOWN / no_override is a valid output.
- Local AI offline -> deterministic fallback.
- No API secrets are sent to Local AI.
- Local AI cannot promote itself.
- Local AI cannot unlock Live.
- Local AI cannot change Risk limits.
- Research Champion cannot auto-promote to Live.
- Final operational authority remains BBB Risk Manager / Live Trading Gate.

## Related BBB documents
- ../../CURRENT_SPEC.md
- ../../checkpoints/BBB_FUNDAMENTAL_SENTINEL_CONCEPT_2026-09-29.md
