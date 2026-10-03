# BBB v0.9.2 Robustness Check — Checkpoint
Date: 2026-10-03

## Trigger
v0.9.1 target Matched Control results:
- Overall 24h Event Avg |Move| 2.30%
- Control 1.75%
- Excess +0.56pp
- Event / Control 1.32x
- Employment: +0.73pp / 1.47x / Event>Control 70%
- FOMC: +0.56pp / 1.27x / Event>Control 50%
- CPI: +0.38pp / 1.22x / Event>Control 61%

Need to test whether means are stable or driven by a few extreme events.

## Implemented
### Robustness metrics
Per horizon and per source:
- Mean Excess
- Median Excess
- Q25 / Q75 / IQR
- 10% Trimmed Mean
- Top-1 Removed Mean (largest absolute Excess removed)
- Min / Max Excess
- Positive Excess Share
- Deterministic percentile Bootstrap 95% CI for Mean Excess
- 2,000 resamples

### Outlier Diagnostics
- 24h events sorted by largest absolute Excess
- Event |Move|
- Control |Move|
- Excess
- Event / Control Ratio

### Existing-data compatibility
- v0.9.1 matched_control_ledger.jsonl can be reused.
- If old absolute ledger path is stale after overwrite/move, v0.9.2 searches current data_dir/run_*/matched_control_ledger.jsonl.
- last_robustness.json cache avoids repeated bootstrap work.
- No re-import or re-replay required when existing ledger is present.

## Interpretation boundary
Robustness metrics describe sensitivity of the matched sample.
Bootstrap CI is not a causal proof, prediction guarantee, or automatic trading gate.

## Validation
- pytest: 84 passed
- compileall: PASS
- UI JavaScript syntax: PASS
- flat ZIP root: PASS
- extracted ZIP pytest: 84 passed
- package: BBB_v0.9.2_Global_Macro_Robustness_Check.zip
- SHA-256: 0bfd2c44c352938f879ed7df0579022cd1720b022416c3277e48bc0e94743a7a

## Safety
Sandbox / read-only research only.
No Paper / Risk / Live behavior change.
