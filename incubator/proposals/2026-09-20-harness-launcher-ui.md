---
status: proposal
created: 2026-09-20
origin: HARNESS launcher / family-use discussion
---

# HARNESS Launcher UI

## Signal

Starting HARNESS currently involves several separate applications and services such as Chrome, Obsidian, local Harness services, monitoring, and possibly local AI components.

A single launcher could reduce friction while also making the system feel tangible and approachable to family members.

## Proposal

Create a lightweight **HARNESS Launcher UI** that starts the required local components and presents a clear system-status screen.

Possible launch actions:

- start Chrome / preferred browser
- open Obsidian directly to the AI-Harness vault
- start HARNESS Server
- start Usage Monitor
- start local AI services when enabled
- verify required components are reachable

Possible UI elements:

- system boot sequence
- active agents
- current run / task
- ASTRA or fallback executor status
- Usage Monitor summary
- Git / Obsidian sync state
- Human approval pending
- simple GREEN / YELLOW / RED health indicator

## Design direction

The UI may deliberately use a playful "future control room" presentation.

This is not only decorative.

A visually understandable launcher may help:

- make the system easier to operate
- make startup state obvious
- expose failures before work begins
- make the AI team concept understandable to children and non-technical family members
- turn HARNESS into something that feels like a coherent product instead of a collection of tools

## Initial implementation direction

Prefer a small local web UI / PWA or lightweight desktop wrapper rather than a large native application.

The first version can simply:

```text
Launch
→ start required processes
→ verify health
→ show ready state
```

The launcher should not become a new source of truth.

It is a control surface over existing HARNESS state.

## Important limits

- do not hide startup failures behind animation
- do not require internet access for purely local status checks
- do not expose secrets or sensitive local paths in a child-facing screen
- do not make visual polish block basic reliability
- keep the first implementation small

## Why preserve this proposal

A launcher can simultaneously improve usability, operational reliability, and family accessibility while providing a natural home for Usage Monitor and smartphone control features later.
