# Sphinx — Code Understanding Checkpoint (2026-10-25)

Status: **CANDIDATE / HIGH for concept; HOLD installation**  
Original X: https://x.com/imAlsahli/status/2113939945303810394  
Verified upstream: https://github.com/parthh01/sphinx  
Important: distinct from similarly named `sphinx-ci` and `jhiker/sphinx`.

## Source correction / new finding
Initial review had **HOLD for the tool** because its upstream repository was unidentified. Subsequent independent lookup found the primary repository `parthh01/sphinx` and read its README. Thus the *existence and documented mechanism* are now confirmed. **Installation and security suitability remain untested**.

## Verified capabilities (README)
- Open-source MIT project, npm package `sphinx-understand`.
- Git pre-push (optionally pre-commit) understanding checkpoint: separate reviewer model reads committed diff through read-only Git tools, asks about behavior, failure modes and invariants, explains wrong answers and asks another scenario.
- Supports Codex/Claude Code plans, OpenRouter and OpenAI-compatible endpoints including local options; reviewers still incur usage and latency.
- Supports macOS/Linux/WSL with Node >=22.19; **native Windows not supported**.
- `sphinx install` changes global Git `core.hooksPath`, potentially affecting all local repositories; repository-specific policies follow `sphinx init`.
- Matching Git push can wait up to 25 minutes; skip/bypass is possible. Passing is **not a security gate** or proof of genuine comprehension.
- Reviewer provider receives code diff, related files, answers and optional context. Default file exclusions are path-based and do not catch credentials embedded in ordinary source files.
- No default model-call cap; explicit cap/budget recommended.

## AI-Harness fit
Current Human approval and code review check whether a change should proceed, but not necessarily whether the human understands its consequences. An **understanding checkpoint** can ask one or two plain-language, consequence-focused questions on high-impact changes (auth, private data, external API failure, financial actions, irreversible changes) before Human approval.

For this non-engineer workflow, focus on high-level behavior, failure recovery, and decision implications rather than low-level syntax. Avoid turning every commit into a quiz.

## Existing overlap and distinction
- Existing Human-in-the-loop, Definition of Done, code review and Trinity verification remain necessary.
- Sphinx checks *understanding*, not functional correctness, security, or authorization.
- Git hooks do not cover all GitHub web edits, automated API commits, CI merges or deployment actions.

## Risks and alternative
Global hooks, blocked pushes, privacy of code sent to reviewers, unbounded costs, false grading and bypassability are material. Safer simpler pilot: **manual pre-approval questions in ChatGPT/Codex**, without installing any hook, with measurable benefit and burden.

## Minimum future evaluation (not approved to execute)
Use synthetic changes in a disposable repo; assess question quality, false grading, user burden, language quality, code exposure, costs, and bypass cases. Compare manual questioning against Sphinx before any installation.

## Decision
**CANDIDATE HIGH (concept) / HOLD (installation)**. Preserve as research only; do not modify Git configuration, repository hooks, workflow gates, or Core rules.