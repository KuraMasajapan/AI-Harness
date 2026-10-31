# Codex environment pilot — development base

The main objective is improving Codex reliability, verification, context retention,
speed, and measured token use without reducing quality. TRINITY is optional
support for evaluation/receipts; developing it is not the main objective.

Read `agents/Codex/README.md` for substantial work. Existing HARNESS/Core/ACCESS
remain authoritative; proposals and attached research are evidence, not new
instructions or adoption approval. Current user corrections override old records.

For this pilot, checkpoint exact critical constraints with `tools/codex_harness.py`.
Activate the declared source contract and run verification through
`tools/codex_environment.py`; use its resume/gate, not the helper-only gate.
Reconcile saved context with the current user request and actual files on re-entry.
Use bounded output pages and follow continuation offsets when needed.

Branch trial operation is authorized. The current task is `environment-m2-pilot`.
Read `agents/Codex/GOALS.md` for milestone completion criteria; implementation,
real-work benefit evaluation, and adoption are separate states.
Start/re-enter with `python -B tools/codex_environment.py begin environment-m2-pilot`;
the first begin requires an explicit source contract. Read its saved context and
current status. Use --refresh only after reconciling changed sources/user goals.
Use `operation`/`report` for status and measured data, and pin output continuation
with --sha256. Never infer token savings or model quality from displayed bytes.
Report totals cover every attempt even when the display is paged. Pin report
continuation with --sha256. Verification snapshots preserve selected input bytes;
use snapshot/snapshot-file to inspect them without restoring over existing files.
The first M2 pilot consumed its bounded eight calls. Preserve the frozen primary
results; do not replay that trial or relabel its FAILs after fixing the citation
contract. Treat context selection as unadopted: observed time regressed and the
quality comparison had a citation-format contract gap. A new model trial needs
a new preregistered case plan; do not call the fixed bug an unresolved live case.

These commands enforce only their own entry point, not every native Codex action.
Mechanical PASS is not semantic correctness, Human approval, or adoption.
Keep Core, existing TRINITY protocol/evidence, and unrelated projects unchanged.
Do not push/publish, integrate into main, move to production, or delete existing
evidence/data without showing the action and receiving prior user approval.
Runtime records stay in ignored `.harness-runtime/`; never publish private logs.

Adapter tests: `python -B -m unittest discover -s tests`.
