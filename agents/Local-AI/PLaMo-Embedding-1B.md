# PLaMo-Embedding-1B

Status: CANDIDATE / NOT YET APPROVED
Reviewed: 2026-09-29

## Identity
- Developer: Preferred Networks, Inc.
- Model: `pfnet/plamo-embedding-1b`
- Class: Japanese text embedding model
- Size: 1B parameters
- Maximum context length: 4096 tokens
- Embedding dimensionality: 2048
- Similarity: cosine similarity
- License: Apache-2.0
- Source: https://huggingface.co/pfnet/plamo-embedding-1b

## Distinguishing characteristic

Converts Japanese text into numerical semantic vectors.

Its value in the Harness is not primarily "make a decision" but:
- retrieve semantically similar past cases;
- detect duplicates / near-duplicates;
- cluster documents;
- support semantic search;
- provide features to a downstream deterministic classifier.

## Strong-fit tasks
- historical analogue retrieval
- news deduplication
- semantic clustering
- retrieval before a downstream classifier or LLM
- search across a growing local knowledge base

## Weak-fit tasks
- direct causal reasoning
- direct BUY / SELL decisions
- producing explanations
- treating nearest-neighbor similarity as proof of identical market impact

## Harness selection note

Prefer an embedding model when the real question is:
"Which past item is most similar to this one?"

Do not force it into a generative or causal-analysis role.
