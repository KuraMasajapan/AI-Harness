# BBB v0.9.39 — Risk & System snapshot audit (2026-10-27)

Source: user-supplied local JSON snapshot `BBB_snapshot_20261027T122250Z.json`, captured 2026-10-27 **21:22:50 JST**. This checkpoint only saves *sanitized derived findings*; original local snapshot, its PII path, data rows, strategy dataset and credentials are **not** uploaded.

## Confirmed observations

- Status `PAPER`; **Paper runner stopped**, both continuous research and Shadow research toggles false; Kill Switch currently false; Live locked true. Kill Switch off is not a fault while only Paper/research is authorized; no live order path.
- Risk configuration: per-order ¥5,000, max gross position ¥50,000, daily loss stop 2%. These are config values, not tests proving the circuit breakers work.
- Operational Readiness: paper/research/journal/fundamental collector/fundamental replay labeled pass; local AI and public streaming todo; private API, reconciliation, live gate locked; independent code audit todo.
- **Sokudan Local AI NOT_INSTALLED**, although enabled and auto_start true. Package version and runtime Python version absent; health null and generic last_error. Previously READY on an older release. Root cause undetermined: missing/invalid local venv, package import failure, environment path mismatch, or negative runtime-probe result cached within running application.
- **117 pending classifications**, while BOJ latest news RSS, BOJ statistics RSS and Fed press RSS all report state OK, recent polling done, zero source errors. Collection works; classification backlog blocked until Local AI restored.
- **Paper fee_rate=0.0, slippage_bps=0.0**; `config.example.json` defaults are also zero. Research/Shadow cost-model figures are independent hypothetical models and **do not imply** Paper's PnL is net of execution costs.
- Paper was explicitly stopped, and most recent Paper journal/decision timestamp was in early October; Paper cannot be described as ongoing live-like prospective execution. Research Forward is a separate on-demand historical-fetch calculation.
- Full v0.9.39 ZIP source inspected: `src/bbb/desktop.py` still hardcodes `"version": "0.9.38"`, while shadow prospective report correctly identifies v0.9.39. **Confirmed metadata bump omission**, not proof of mixed deployment.
- Research status preserved: Active Forward 5485/8640 5m candles; public taker + hypothetical slippage net -3.17%; Shadow Forward 1990 candles, baseline net -2.24%, entry_buffer_06 net -1.59%, model stress -2.41%, EARLY; still economic-unqualified.
- Separate `data_sources.bitbank_public` state CONNECTED, but `last_fetch:null` in snapshot. Since Research has fresh market data and collectors work, do not treat this null as confirmed outage; verify scope of field first.
- Empty transient `jobs` list is not evidence that historic jobs never ran.

## Deterministic diagnostic in shipped v0.9.39

The ZIP includes `BBB_LOCAL_AI_DIAGNOSTIC.bat`, which reads/checks existence of `.venv_local_ai\\Scripts\\python.exe`, runs Python/pip-package import/version probes and optionally checks the local Sokudan `/health` endpoint. It writes **`BBB_LOCAL_AI_DIAGNOSTIC.txt` in the BBB folder** and does not reinstall the Local AI. Run this and inspect the text before recommending any environment recreation.

Do **not** run `BBB_LOCAL_AI_SETUP.bat` preemptively: it explicitly removes the current `.venv_local_ai` before recreating a venv and installing dependencies. First diagnose, then stop BBB and repair as necessary. If repairing after a cached negative runtime probe, restart BBB to invalidate the cached state.

## Action plan

1. Have Human double-click `BBB_LOCAL_AI_DIAGNOSTIC.bat` in their currently deployed BBB root, submit the generated `BBB_LOCAL_AI_DIAGNOSTIC.txt` (check for local sensitive paths before sharing). No setup/Live/Freeze changes.
2. Distinguish 'venv missing', 'venv exists, module missing', 'probe exception' and 'runtime negative cache'; implement minimal safe fix and user retest.
3. At next release bump metadata consistently; expose Local AI probe failure reason and one-click diagnosis, show pending classification backlog in Risk & System.
4. Before any meaningful Paper trade performance claim, establish coherent fee/slippage assumptions and properly account for stale Paper journal.
5. Do not auto-enable Live, alter risk limits, reset Active/Shadow Freeze timestamps, or promote strategy while this audit is being resolved.

Snapshot-based analysis only; Python source inspection based on distributed `BBB_v0.9.39_SHADOW_PROSPECTIVE_FORWARD_FULL.zip`, not user device binaries.

## Follow-up: Windows Local AI diagnostic, 2026-10-27 22:03 JST

User executed `BBB_LOCAL_AI_DIAGNOSTIC.bat` and supplied the output. Confirmed:
- BBB `.venv` **FOUND**, runtime Python **3.14.0**.
- Dedicated `.venv_local_ai` **FOUND**, runtime Python **3.13.15**.
- `importlib.util.find_spec('sokudan') is None` (**sokudan installed: False**); diagnostic version n/a.
- Local HTTP `127.0.0.1:8766/health` **times out** at 1-second request timeout. This alone cannot distinguish stopped/unresponsive service, but it is consistent with local package absence.

A minimal, non-destructive repair BAT `BBB_LOCAL_AI_REPAIR_INPLACE.bat` was produced as a ChatGPT attachment. It is NOT committed as a runnable tool to the repository and needs to be copied to the user's BBB root next to `BBB_START.bat`. It checks the local Python version and venv identity, then installs `sokudan[serve]>=0.3,<0.4` using ONLY `.venv_local_ai\\Scripts\\python.exe -m pip`, verifies `import sokudan`, and logs to `BBB_LOCAL_AI_REPAIR_INPLACE.log`. The existing `.venv_local_ai`, BBB `.venv`, data/config, Champion, and prospective freezes are not deleted, reset, or intentionally changed. Installation requires internet and could update dependencies inside the isolated venv; no execution on user's Windows device has yet been observed. **The user should close BBB before the repair and restart after.** If the package install fails or UI remains NOT_INSTALLED/LOADING, inspect the resulting log and local server health. Do not assume repair succeeded on target until verified.

## Follow-up 2: pip missing, 2026-10-27 22:15 JST

Human ran the in-place repair and supplied `BBB_LOCAL_AI_REPAIR_INPLACE.log`. Output:
- Local AI Python 3.13.15 successfully ran in the existing virtual environment.
- `No module named pip`; the first repair exited with **ERROR - pip is unavailable** before it attempted to install Sokudan. No installer success is claimed.
- A second one-click Windows script `BBB_LOCAL_AI_REPAIR_INPLACE_V2.bat` was generated for conversation delivery. It first validates the dedicated venv, tests pip, if missing invokes Python standard library `-m ensurepip --upgrade`, tests pip again, then uses *only* that venv's pip to install the same `sokudan[serve]>=0.3,<0.4` spec used by the shipped setup BAT. It verifies `import sokudan` and records `BBB_LOCAL_AI_REPAIR_INPLACE_V2.log`.
- In-place repair does not remove or regenerate `.venv_local_ai`; it intentionally leaves trading data, config and frozen research untouched. Python package installation itself changes the dedicated venv and requires internet. Static checks passed in packaging; execution on Windows has **not** yet been observed.
- Next: close BBB, copy V2 BAT next to `BBB_START.bat`, run it, review log result; only restart BBB and validate Local AI state if the installer reports success. On failure, upload new log; do not fall back to destructive generic setup without review.

## Follow-up 3: in-place repair V2 succeeded — 2026-10-27 22:21 JST

The Human ran `BBB_LOCAL_AI_REPAIR_INPLACE_V2.bat` and supplied `BBB_LOCAL_AI_REPAIR_INPLACE_V2.log`.
- Local Python **3.13.15** and dedicated virtual environment were recognized.
- `ensurepip --upgrade` successfully installed **pip 26.2.1** after `No module named pip`.
- `sokudan[serve]` installation completed; **sokudan 0.3.0** and `import sokudan` verification both succeeded.
- Final log: `RESULT: SUCCESS - pip available; Sokudan import succeeded`.
- This confirms package installation, **not** BBB-managed local server startup, HTTP /health, model inference, or the 117 queued classifications. Those are pending Windows runtime verification after relaunch.
- Next: launch BBB, inspect Risk & System Local AI state, then check health and pending classification backlog. Do not modify frozen research windows or Live gate.

## Follow-up 4: Sokudan OFFLINE caused by PyTorch import failure — 2026-10-27 ~22:28 JST

User screenshot after in-place repair shows package `sokudan 0.3.0` detected but `Local AI: OFFLINE` and no last inference. Original historical `data/local_ai/sokudan_server.log` (~11 MB) was shared. Inspected all 178,980 lines: prior 50 successful `sokudan serve: loaded` occurrences; the 2026-10-27 attempt has one traceback. Its last startup attempt was 2026-10-27T13:28:37.804080+00:00. After reading cached Hugging Face model files it failed at `from sokudan.backends.torch_backend import TorchBackend` -> `import torch` with:

```
ImportError: cannot import name 'amp' from partially initialized module 'torch'
(most likely due to a circular import)
```

The log shows **previously healthy model loads** on 2026-09-30 through 2026-10-06, including local `GET /health` and inference `POST /v1/systemone` HTTP 200, so the present failure is a **runtime dependency regression**, not absence of model-cache downloads or a mistaken 127.0.0.1 endpoint. Whether the torch install is corrupt or a torch package regression is not proven yet.

Harness historical launch/setup references checked:
- `development/projects/BBB/DECISION_LOG.md` (v0.8.1 Python 3.11-3.13 isolated venv and v0.8.2 successful READY; v0.8.4 recovery of misleading NOT_INSTALLED).
- `development/projects/BBB/checkpoints/BBB_V0.8_LOCAL_AI_SANDBOX_2026-09-30.md` (separate server on 127.0.0.1:8766, backend torch, CPU, model ID).
- `development/projects/BBB/CURRENT_SPEC.md` (separate `.venv_local_ai`, failure fallback, dedicated setup BAT).
- Shipped `BBB_LOCAL_AI_SETUP.bat` re-creates the venv, so do not invoke it without choosing to rebuild.

A **conservative, same-venv torch repair** conversation attachment `BBB_LOCAL_AI_TORCH_REPAIR_V3.bat` has been created and statically inspected, but not run on user's Windows PC. When BBB is closed, it checks the dedicated Python, Sokudan/Torch metadata, tests importing `torch` and `torch.amp`, re-installs *only* `torch==2.14.1` from pip when import fails *and* installed metadata agrees with the previously observed 2.14.1, then verifies `torch`, `amp`, and Sokudan's TorchBackend imports. It logs to `BBB_LOCAL_AI_TORCH_REPAIR_V3.log`. It does not remove venvs, change Paper settings, or touch data or freezes. `--force-reinstall` does modify the isolated torch installation and may require a large network download; it is not guaranteed to repair a compatibility regression. If unexpected version or validation errors occur, script stops and asks for log. **Do not claim runtime repair succeeded until the Windows log and READY/inference evidence arrive.**

## Follow-up 5: PyTorch in-place repair succeeded — 2026-10-27 22:41 JST

Human ran `BBB_LOCAL_AI_TORCH_REPAIR_V3.bat`. Log confirms:
- Python 3.13.15, Sokudan 0.3.0, Torch metadata 2.14.1.
- Initial `import torch; from torch import amp` failed with the prior circular/partial-init error.
- Version-locked reinstall of `torch==2.14.1` completed successfully.
- Post-reinstall imports passed: `Torch: 2.14.1+cpu`, `Sokudan: 0.3.0`, `Torch + Sokudan backend imports PASS`.
- Final: `RESULT: SUCCESS - torch and Sokudan backend import OK.`

This verifies the isolated Python package/runtime layer only. BBB-managed server startup, `/health`, inference, and queued-classification drain still require target-runtime confirmation after BBB restart.

## Follow-up 6: Local AI READY restored on target Windows — 2026-10-27 23:09 JST

User shared Risk & System screenshot after torch repair and BBB restart. UI evidence:
- Operational Readiness `Local AI Fundamental Sentinel`: **pass / READY**.
- Detail card state: **READY**.
- Model: **GeneLab/sokudan-ja-310m**.
- Sokudan package: **0.3.0**.
- Device: **CPU**.
- Last inference: **1861 ms** at **2026/10/27 23:09:27 JST**.
- Sandbox / Trade influence OFF remains intact; Live Gate remains CLOSED/locked.

This closes the immediate Local AI runtime recovery incident across package, torch import, server startup, health/readiness and at least one successful inference. Remaining follow-up is to verify the previously observed 117-item classification backlog drains normally and to fix the stale System metadata version (`0.9.38`) in the next release.

## Follow-up 7: post-recovery audit snapshot — 2026-10-27 23:11 JST

User exported a new audit snapshot after Local AI recovery and successful self-test.

Confirmed from the snapshot:
- Local AI: `installed=true`, package **0.3.0**, Python **3.13.15**, state **READY**, health **ok**, CPU, owned process, Sandbox only, Trade influence false.
- Successful self-test at **2026-10-27 23:09:27 JST**, client elapsed **1861 ms**.
- Fundamental Collector: enabled, auto-start, **running**, 15-minute poll.
- BOJ News / BOJ Statistics / Fed Press sources: **OK**, no current source error.
- Pending classifications remain **117**.
- Collector last run: **2026-10-27 23:06:20 JST**, which occurred before Local AI reached READY. Its deferred retry therefore attempted 0 and classified 0.
- Source inspection of v0.9.39 confirms `FundamentalCollector._retry_pending(limit=5)`: at most 5 pending events are reclassified per collector cycle. Full feed poll interval is 15 minutes. Thus a backlog of 117 can require up to 24 successful poll cycles (~6 hours of continuous runtime) if no newer mechanism intervenes.
- This is not data loss: pending rows remain persisted in `data/fundamental/pending_classification.json`, and successful retries append classification-update audit rows.
- Operational deficiency: recovery backlog catch-up is too slow and also waits for the next 15-minute feed cycle when Local AI becomes READY after the most recent collector pass.

Next-release design target:
1. Keep normal public feed polling at 15 minutes.
2. Add a bounded background pending-classification catch-up path that activates only when Local AI is READY, serializes inference (concurrency 1), works in small batches, backs off on zero-success/error, and stops cleanly with BBB.
3. Expose pending backlog / catch-up progress in Risk & System.
4. Correct current-release metadata still showing `0.9.38` while v0.9.39 Shadow Prospective is deployed.
5. Preserve Sandbox-only / Trade influence OFF / Live locked boundaries.

No need to refreeze or alter Active/Shadow research state while this operational fix is prepared.
