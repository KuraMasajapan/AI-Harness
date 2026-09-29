# BBB AI Development Agents

Status: RESEARCH / PAPER
Updated: 2026-09-29

## Purpose

This directory records AI components that may extend BBB.

BBB's current trading core remains deterministic. AI components are research modules and do not receive direct Live trading authority.

## Current AI development map

### Fundamental Sentinel
Purpose:
- interpret unstructured fundamental information after API collection;
- convert text context into bounded structured signals;
- leave the final policy and safety decision to deterministic BBB code.

Local AI implementation notes:
- [BBB Local AI](./Local-AI/README.md)

Harness-wide Local AI catalog:
- [AI-Harness Local AI Catalog](../../../agents/Local-AI/README.md)

### Cloud escalation (future)
Cloud AI may later be called only for difficult, high-value cases that local processing cannot resolve.
It is not intended as an always-on dependency.

### Independent audit
A separate capable AI may be used to audit BBB implementation and safety gates.
Audit authority is distinct from trading authority.

## Fixed authority boundary

```text
AI observation / classification
        ↓
structured signal
        ↓
deterministic BBB policy
        ↓
Risk Manager
        ↓
Paper

Future Live:
Risk Manager
        ↓
Live Trading Gate
        ↓
Human approval / canary controls
```

No AI component in this directory may silently bypass these boundaries.
