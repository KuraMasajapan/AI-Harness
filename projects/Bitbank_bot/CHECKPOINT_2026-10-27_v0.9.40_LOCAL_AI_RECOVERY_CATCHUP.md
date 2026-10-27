# BBB Checkpoint — v0.9.40 Local AI Recovery Catch-up

Recorded: 2026-10-27 JST
Status: **Full ZIP packaged, locally verified, and Windows runtime acceptance confirmed.**

## Why this release exists

The target Windows PC recovered Sokudan Local AI after an operational incident:
- missing Sokudan package in the dedicated `.venv_local_ai`,
- missing pip in that venv,
- then a broken PyTorch import (`torch.amp` partial/circular initialization),
- repaired in place without deleting BBB data or research freezes.

After recovery, the audit snapshot showed Local AI READY and a successful inference, but **117 Fundamental classifications remained pending**. v0.9.39 retried only up to 5 deferred items inside the normal 15-minute feed cycle, so a large recovery backlog could take hours to drain.

## v0.9.40 implementation

### Bounded background classification catch-up
- Existing RSS/feed polling remains **15 minutes** by default.
- Separate daemon catch-up path processes pending classifications only when Local AI is READY.
- Default batch size: **3**.
- Default catch-up interval: **10 seconds**.
- Error backoff: **30 seconds**.
- Dedicated retry lock prevents feed-retry and background catch-up from classifying the same backlog concurrently.
- BBB-originated Sokudan inference is serialized with a Local AI inference lock.
- On classification failure, the current batch stops and backs off rather than hammering the local model.
- Successful deferred classifications keep the existing append-only `classification_update` audit behavior and are removed from `pending_classification.json`.
- Local AI unavailable/errors do not stop BBB, market data, Paper core, or Strategy Lab.

### Risk & System observability
Local AI card now shows:
- **Pending AI / 分類待ち**
- **Catch-up / 追いつき処理**
- latest batch classified count
- recovery-session cumulative classified count
- error count when present

Fundamental status now exposes a `catchup` object for audit snapshots.

### Diagnostics
`BBB_LOCAL_AI_DIAGNOSTIC.bat` now checks:
- BBB Python environment
- dedicated Local AI Python
- Sokudan install/version
- pip availability
- Torch package metadata
- `import torch`
- `from torch import amp`
- Sokudan `TorchBackend` import
- local `/health` endpoint

This folds the October 27 recovery lessons into the shipped diagnostic path. It diagnoses only; it does not automatically reinstall packages.

### Version metadata
Application-level surfaces are corrected to **v0.9.40**:
- `bbb.__version__`
- `pyproject.toml`
- `BBB_START.bat`
- Local AI setup banner/log
- desktop status / audit snapshot
- desktop header/footer
- README / first-read guide

Historical feature-version labels and historical report schemas are not rewritten.

## Safety boundaries unchanged

- PAPER / RESEARCH only.
- Local AI remains **SANDBOX ONLY** and **Trade influence OFF**.
- Private API remains unused/locked.
- Live order path remains NOT IMPLEMENTED / Live Gate CLOSED.
- Catch-up cannot modify Active Champion, Shadow Champion, Active Forward Freeze, Shadow Prospective Freeze, risk limits, Paper state, or Live eligibility.
- No API credentials are included.

## Validation

Source test suite:
- **295 passed**

Additional validations:
- Python compileall: PASS
- UI JavaScript syntax: PASS
- package re-extraction: PASS
- re-extracted full test suite: **295 passed**
- re-extracted version: **0.9.40**
- default catch-up enabled, batch size 3: PASS

A regression test models the observed **117-item backlog** and confirms it drains deterministically in **39 batches of 3** using the bounded catch-up helper.

## Package

`BBB_v0.9.40_LOCAL_AI_RECOVERY_CATCHUP_FULL.zip`

SHA-256:
`038bf910ee111e56084f842ec8da19ce100986cde3f031bac0875c9a4cb90788`

## Target-PC update procedure

1. Close BBB normally.
2. Preserve existing `data/`, `config.json`, `.venv`, and especially the repaired `.venv_local_ai`.
3. Overlay/extract the v0.9.40 Full ZIP into the BBB folder.
4. Launch with `BBB_START.bat`.
5. Open Risk & System.
6. Verify System version shows `0.9.40`.
7. Verify Local AI remains READY.
8. Observe Pending AI decrease automatically and Catch-up transition through CATCHING_UP/IDLE.
9. Do **not** re-Freeze Active or Shadow.
10. Live remains locked.

Windows runtime acceptance is not complete until the Human confirms Pending decreases on the target machine.

## Windows runtime acceptance — 2026-10-27

Human confirmed on the target Windows machine that:
- Local AI remained **READY** after upgrading to v0.9.40.
- Risk & System displayed the new `Pending AI / 分類待ち` and `Catch-up / 追いつき処理` fields.
- Pending count was observed decreasing over time without manual classification commands.
- Example observed count: **112** after previously recorded **117** backlog.
- Human explicitly observed the number continuing to decrease, confirming the new background catch-up loop is active on the deployed machine.

This completes Windows acceptance for the v0.9.40 recovery-catch-up feature. The classification backlog still needs time to drain fully, but no manual intervention is required while BBB remains running and Local AI stays READY.

Safety boundaries remain unchanged: Local AI Sandbox only, Trade influence OFF, Live Gate locked, Active/Shadow Freeze timestamps unchanged.
