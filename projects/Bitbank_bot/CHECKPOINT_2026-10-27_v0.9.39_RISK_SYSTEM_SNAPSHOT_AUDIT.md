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
