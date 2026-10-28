---
document_type: research_reference
date: 2026-10-28
status: REFERENCE
decision: KEEP / WATCH / DESIGN_REFERENCE
stage_1: A+
stage_2: A-
novelty: A
ai_harness_relevance: A
implementation: NOT IMPLEMENTED
evidence_status: OFFICIAL_SITE_CONFIRMED + POST_VISUAL_EVIDENCE / INTERNAL_METHOD_UNVERIFIED
tags:
  - rikyu
  - ai-design
  - logo
  - geometry
  - vector
  - svg
  - design-system
  - mcp
  - codex
  - design-tools
---

# Rikyū — Structured / Geometric AI Design Reference

Trigger post:
https://x.com/awe0_io/status/2114891628561510544

Official site:
https://rikyu.ai/

## Why this was saved

The important signal is not simply "AI can make logos."

The post highlights a different direction for AI Design:

> move from raster-like image generation toward design constructed through proportion, geometry, layout, visual systems, and explicit design rules.

This is potentially important because it changes the role of AI from **image generator** toward **design-tool operator / design-system generator**.

## What is confirmed

### From the official Rikyū site

The official site currently presents Rikyū as an AI design tool covering:
- logos
- ads / graphics
- print
- websites
- apps
- 3D
- video

The site also states:
- MCP integration
- works with Claude, Codex and Cursor
- generated work can be used in the user's own project
- a showcased logo asset is served as SVG
- free and paid credit-based plans exist

The official site does **not** by itself document the internal logo-generation algorithm.

### From the shared X post and its four images

The post explicitly claims Rikyū constructs logos using circles, lines and geometric forms rather than only generating a raster image.

The attached images provide meaningful visual evidence consistent with that claim:

1. A crest / emblem construction board shows:
   - many overlapping circles and arcs
   - radial guide lines
   - grid alignment
   - a resolved final emblem

2. A finished winged-horse emblem shows:
   - repeated circular / arc geometry
   - structured negative space
   - clean geometric repetition

3. A lion silhouette shows:
   - repeated curved components
   - simple polygonal base forms
   - clean negative-space cuts

4. A lion-on-rock construction board shows:
   - dense circle construction
   - diagonal and radial guides
   - a horizontal baseline
   - grid-based proportioning
   - a final simplified mark

This is strong evidence that the presented design process is **geometrically structured**.

## Important uncertainty

The public evidence does **not** prove all of the following:

- that Rikyū internally represents every logo as editable geometric primitives
- that the AI actually reasons symbolically over circles / lines rather than generating a shape first and retrofitting construction guides
- that users can edit individual primitive geometry
- that anchor points / Bézier handles / boolean operations are exposed in the product UI
- that all logo outputs are true editable vectors
- that the geometric construction is deterministic or constraint-preserving
- what exact model / rendering stack is used

Therefore:

> **Visible geometric construction ≠ independently verified internal geometric generation engine.**

The distinction should be preserved.

## Strategic signal

The useful design direction is:

```text
Traditional generative-image approach

Prompt
  ↓
Image model
  ↓
Pixels
  ↓
Looks approximately right
```

versus:

```text
Structured AI Design direction

Intent
  ↓
Design constraints
  ↓
Proportion / geometry / layout / visual rules
  ↓
Structured design object
  ↓
Editable / reusable output
```

The second direction is more interesting for serious design automation because it can potentially support:
- consistency
- editability
- reproducibility
- brand systems
- layout constraints
- downstream reuse
- multiple media from the same identity

## AI-HARNESS relevance

This aligns with an existing AI-HARNESS principle:

> **Use a creation method that matches the precision required.**

For technically constrained outputs, deterministic / structured methods such as SVG, CAD or code are preferable to unconstrained image generation.

Rikyū suggests the same idea may become practical for **creative design**, not only engineering diagrams.

Potential future pattern:

```text
Human intent
   ↓
AI-HARNESS constraints / brand requirements
   ↓
Structured design agent
   ↓
vector / layout / reusable design system
   ↓
Human review
   ↓
approved visual asset
```

## Potential applications

### 1. Project identity / logo generation

Possible use for:
- UIAPduino
- GROWGLE
- AI-HARNESS subprojects
- future product identities

The value would be higher when outputs must remain:
- geometrically consistent
- scalable
- reusable across print/web/product surfaces

### 2. Source-locked visual design

A structured design engine could potentially preserve:
- proportions
- grid rules
- approved shapes
- brand colors
- spacing
- minimum clear space

better than unconstrained image generation.

This is a **future comparison hypothesis**, not currently verified for Rikyū.

### 3. Design-system generation

The official site presents cross-medium outputs including logo, graphics, print, web, app, 3D and video.

This suggests a potentially valuable workflow:

```text
Brand concept
   ↓
core visual identity
   ↓
logo
   ↓
print / web / app / ads / 3D / video
```

If consistency across these outputs is real, this is more valuable than one-off image generation.

### 4. Agent-integrated design

Official MCP support for Claude, Codex and Cursor is directly relevant to agent workflows.

Potential future pattern:

```text
Codex / Claude
   ↓
Rikyū MCP
   ↓
structured design asset
   ↓
project repository
   ↓
implementation
```

This should only be tested after reviewing:
- MCP permissions
- credential handling
- file-write scope
- data sent to the external service
- commercial-use terms
- reproducibility / export formats

## Relationship to Huashu Design

Existing AI-HARNESS note:
`incubator/proposals/2026-10-27-huashu-design-skill-candidate.md`

They are not direct substitutes.

### Huashu Design
- open-source Agent Skill package
- prototypes, slides, infographics, motion, review
- broad design workflow
- inspectable scripts / references
- candidate specialized Skill

### Rikyū
- hosted AI design product
- emphasis on direct design creation across brand/media surfaces
- visible geometric logo construction
- MCP integration
- internal generation method not open / not independently verified

Possible future comparison:

```text
Huashu = reusable design workflow / Skill
Rikyū  = external AI design engine / service
```

A future design pipeline could compare them rather than assuming one replaces the other.

## Security / trust considerations

Rikyū is an external service.

MCP connection should be treated under existing AI-HARNESS trust rules:
- external MCP is not automatically trusted
- inspect requested permissions
- minimize filesystem / project access
- do not send private or sensitive project data without explicit need
- verify outputs before committing them to Source of Truth
- generated visual assets remain proposed artifacts until Human approval

The earlier Instruction Trust Boundary principle applies.

## Evaluation

- Stage 1: **A+**
- Stage 2: **A-**
- Novelty: **A**
- AI-HARNESS relevance: **A**
- Visual evidence for geometric design: **STRONG**
- Internal implementation evidence: **UNVERIFIED**
- Product / MCP claims: **CONFIRMED from official site**
- Open-source / inspectability: **LOW / hosted product**

## Decision

**KEEP / WATCH / DESIGN REFERENCE**

The concept is worth preserving even if Rikyū itself is never adopted:

> **AI Design should evolve from "generate an image" toward "construct a design under explicit rules."**

This may become a useful comparison axis for future design tools:

```text
visual quality
+ editability
+ geometric consistency
+ constraint preservation
+ provenance
+ reproducibility
+ agent integration
```

No installation, MCP connection, paid subscription, or AI-HARNESS Core change is authorized by this note.
