---
name: research-dedup
description: Preflight existing AI-Harness research records, run Stage 1 intake, verify primary sources, and complete Stage 2 research evaluation without duplicating prior work.
status: PILOT / NOT CORE
---

# Research Dedup & Two-Stage Evaluation

## Purpose

Prevent previously investigated OSS, articles, papers, and technical claims from being treated as new discoveries. Execute the established AI-Harness research process while keeping research, saving, and implementation separate.

This is a reusable procedure, **not** an autonomous scheduler, a search index, or an authorization to modify Core.

## Governing sources and scope

- Follow `HARNESS.md`, `core/RULES.md`, `core/WORKFLOW.md`, `core/ACCESS.md`, and `skills/README.md` on the current `development` branch as applicable.
- Apply the existing **AI-Harness 外部情報調査・二段階評価・検証候補保存方針** (2026-10-13) as the research evaluation policy **when its text is available**. This Skill summarizes execution order; it does not replace that policy. If unavailable, disclose the limitation rather than claiming it was loaded.
- Evaluate usefulness for AI-Harness as a whole (Core, Memory, Skills, Evaluation/Trinity, tools, local AI, and relevant Projects); apply BBB-specific checks only where relevant.
- Prefer minimal context loading, existing tools, and read-only operations.

## Trigger and input

Use when the Human provides X/Grok posts, OSS, GitHub URLs, articles, papers, news, or technical proposals for evaluation, or asks whether a candidate has been examined before.

Extract the candidate's canonical name, repository or source URL, aliases, claim, publication/update date if known, and the current question. Do not infer a repository identity from a similar name alone.

## Procedure

### 0. Preflight deduplication (before treating a candidate as NEW)

1. Search the accessible `development` repository for exact names, canonical URLs, aliases, related functions, and prior decisions. Inspect relevant `incubator/proposals/`, research notes, Skills, and project-specific notes as warranted.
2. Search available Airtable research intake and accessible prior drafts/notes where relevant. A GitHub search of the default branch alone is **not** a complete check of `development`; a commit-message search alone is not a content search.
3. Record which sources were **actually searched**, which were inaccessible, and the matching path/URL/date/status. Do not claim exhaustive coverage of inaccessible or unsaved drafts.
4. Assign a *dedup status*:
   - `NEW`: no matching prior record after a sufficiently scoped, successful check;
   - `EXISTING`: prior research exists, with no material new evidence;
   - `UPDATED`: prior research exists and material new evidence or a changed claim warrants delta review;
   - `UNCONFIRMED`: source access, coverage, identity, or prior status remains uncertain.
5. For `EXISTING`, reuse the previous evaluation and report it with a source pointer; do not repeat full research without a reason. For `UPDATED`, investigate the delta and preserve the old assessment. For `UNCONFIRMED`, explicitly avoid saying the record does not exist.

### 1. Stage 1 — Intake / provisional evaluation

Based on the submitted post, summary, and immediately available context, classify claims as `FACT`, `IDEA`, or `ANOMALY` where helpful. Assign the policy's **provisional research priority** `A++ / A+ / A / B / C`, with a short rationale using relevance, novelty, potential value, specificity, verification feasibility, and investigation cost.

Stage 1 is a *priority for further reading*, not confirmation of claims, approval to save, or approval to implement. For already evaluated candidates, show the existing Stage 1 assessment where available and focus on new claims.

### 2. Detailed investigation / primary-source verification

For candidates requiring investigation, inspect official docs, GitHub repository and relevant code, papers, release notes, and credible independent evidence. Separate author claims, verified facts, AI inference, and unknowns. Inspect mechanism, dependencies, recency, reproducibility, security/permissions, privacy, cost, maintenance, and simpler alternatives.

Distinguish confirmation of a README or author's benchmark from independent reproduction of performance. Record inaccessible sources and evidence gaps. Do not install packages, connect services, expose secrets, or run unapproved experiments.

### 3. Stage 2 — Final research evaluation

Compare with current Harness functions, previously installed Skills, prior proposals, and alternatives. Reassess independently of Stage 1 using `A++ / A+ / A / B / C`. Attach an evidence label:
`CONFIRMED / MULTIPLE REPORTS / SINGLE REPORT / UNVERIFIED / CONFLICTING`.
State *what* is confirmed, not just the label.

Consider utility, uniqueness, reproducibility, safety, cost/benefit, Human burden, and a minimal reversible validation test. Give a separate research disposition `CANDIDATE / HOLD / REJECT`. A high rank does not imply adoption.

For a previously completed Stage 2 with no new evidence, cite/reuse it instead of manufacturing a new assessment.

### 4. Report and persistence boundary

Report concisely:
- Candidate and canonical source;
- Dedup status, matched record(s), and search coverage/limitations;
- Stage 1 priority and rationale (existing or newly assessed);
- Primary-source findings and evidence gaps;
- Stage 2 final rank, evidence label, and `CANDIDATE / HOLD / REJECT`;
- Overlap, actual delta, minimal validation, and recommended next action.

The established research policy generally proposes `incubator/proposals/YYYY-MM-DD-<slug>.md` for individually approved candidates. Avoid duplicate files when the existing record suffices. **Read/search/evaluate are allowed; all GitHub writes require prior explicit Human approval of target and content.** A research note is not implementation permission, a Core promotion, or a sealed-boundary change.

## Verification / pilot test

Use **Graphify** as the regression case. A passing run must:
1. Search actual accessible records and identify a previously evaluated Graphify note **if accessible**; cite its location and status, without inventing a saved GitHub path.
2. Distinguish a prior draft from a committed repository record.
3. Return `EXISTING` or `UPDATED` when supported, or `UNCONFIRMED` if the necessary historical material is inaccessible.
4. Preserve the prior Stage 1/Stage 2 evaluations and investigate only meaningful new evidence.
5. Make no unauthorized writes.

A Skill file existing in GitHub does **not** prove it was loaded or automatically triggered by ChatGPT or Codex. Verify invocation and behavior separately before claiming deployment success.
