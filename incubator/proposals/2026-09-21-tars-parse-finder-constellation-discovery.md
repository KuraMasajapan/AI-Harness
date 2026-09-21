---
status: proposal
created: 2026-09-21
origin: ChatGPT / Obsidian constellation-discovery discussion
tags:
  - tars
  - parse-finder
  - obsidian
  - constellation
  - semantic-discovery
  - trinity
  - harness
trigger_topics:
  - tars
  - parse-finder
  - obsidian-graph
  - constellation-discovery
  - hidden-relationships
  - local-graph
---

# TARS — Parse-Finder Protocol for Constellation Discovery

## Purpose

TARS is a proposed AI-Harness role for discovering hidden relationships and emerging structures across Obsidian notes.

The working metaphor is:

```text
note / idea / signal = star
link / relationship  = line
cluster candidate     = constellation candidate
validated concept     = constellation
current architecture  = star map
```

TARS does not decide that a constellation is true.

Its role is to observe the existing note universe, identify potentially meaningful relationships, and surface **candidate constellations** for later evaluation.

---

## Working Name

Formal concept:

```text
Parse-Finder Protocol
```

Codename:

```text
TARS
```

The name references the exploratory AI character from *Interstellar* and also connects naturally to the project metaphor:

```text
TARS finds STARS
```

A possible interpretation for the added "S" concept is:

```text
S = Signal
```

This keeps the meaning provisional:

a note or fragment may be a useful signal, or it may still be noise.

---

## Intended Role

TARS should help answer questions such as:

- Which notes appear semantically related even when they are not directly linked?
- Which concepts repeatedly bridge otherwise separate areas?
- Where are clusters beginning to form?
- Which apparently unrelated ideas may share a deeper structure?
- Where is there enough density or recurring connection to justify a new concept hypothesis?

TARS should prefer discovery over classification.

It should not force every note into a taxonomy.

---

## Relationship to Obsidian

Obsidian is treated as the human-facing observation interface for the knowledge space.

Current metaphor:

```text
Obsidian
= sky / knowledge universe

Notes
= stars

Links
= visible relationships

TARS
= observer that searches for hidden constellations
```

The goal is not to make the graph visually tidy.

Dense or irregular graphs may be useful because they can reveal unexpected structure.

Local Graph is a likely observation surface for TARS-style analysis.

---

## Relationship to TRINITY

TARS proposes.

TRINITY validates.

Preferred boundary:

```text
Obsidian notes
→ TARS observation
→ constellation candidate
→ TRINITY review
→ Human decision
→ accepted concept / architecture update if justified
```

TARS must not promote its own discoveries into Core, Workflow, Project Source of Truth, or authoritative architecture.

A TARS result remains a hypothesis until separately validated.

---

## Candidate Output

A future TARS output may include:

```text
Candidate constellation:
- involved notes
- observed relationships
- bridge notes
- evidence / links
- why the pattern may matter
- uncertainty
- candidate status
```

No confidence score or ranking system is required at this stage.

Keep the first implementation simple.

---

## Initial Operating Principle

TARS V0.1 should begin read-only.

Preferred first behavior:

```text
read Markdown
→ inspect titles / content / links
→ detect recurring or hidden relationships
→ output a small number of constellation candidates
→ do not modify source notes
```

The initial success criterion is practical:

> TARS should occasionally surface a meaningful relationship that the human did not already notice.

---

## Important Boundaries

TARS should not:

- rewrite existing notes automatically
- treat semantic similarity as proof
- promote candidate relationships into facts
- alter Core or Source of Truth
- merge proposals automatically
- assume every dense cluster is meaningful
- replace TRINITY validation
- replace Human judgment

---

## Future Integration

A likely future sequence is:

```text
Conversation / external information
→ Capture
→ Obsidian star
→ TARS
→ constellation candidate
→ TRINITY
→ Human
→ durable accepted structure
```

Capture and TARS are separate roles.

Capture places stars into the universe.

TARS looks for constellations among them.

---

## Current Status

This is a proposal only.

No TARS runtime, parser, plugin, Obsidian automation, or TRINITY handoff contract is implemented by this file.

The purpose of this note is to preserve the idea and its intended boundaries so later design work does not depend on conversation memory alone.
