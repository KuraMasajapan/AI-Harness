---
status: reference
created: 2026-10-12
origin: external-technology-review
implementation: not-approved
---
# GitHub Actions external execution and iOS build constraints

## Sources
- https://github.com/actions/runner
- https://github.com/nektos/act

## Idea
Distinguish the GitHub Actions workflow orchestration, the runner executing jobs, and the operating system/toolchain required by the job. Evaluate self-hosted runners or compatible local workflow execution as possible AI-Harness execution infrastructure.

## Verified concept / limits
- GitHub publishes an open-source Actions runner; act offers local execution of many Actions workflows.
- Recreating a runner or workflow engine does **not** recreate macOS or Xcode on Windows/iPhone.
- A hosted macOS runner may build iOS projects without owning a Mac, subject to toolchain, signing, export, and usage restrictions.
- AltStore installation/signing and IPA compilation are separate stages; AltStore Classic generally needs AltServer for setup/refresh.
- An anecdotal post about ChatGPT-to-IPA had a local Mac/Codex environment behind it; another commenter described WSL/Ubuntu plus compilation/signing complexity. Neither is proof of general-purpose iPhone-only iOS builds.

## AI-Harness relevance
Potential general-purpose job execution and result collection across PCs and cloud runners; **not** a BBB-specific candidate.

## Decision
REFERENCE / HOLD implementation. Compare existing GitHub Actions and other job execution solutions before building a replacement. No deployment or modification authorized.
