# Pilot evaluation operations (non-protocol)

These optional operator records do not affect RunManager, Binding, Semantic or
Release. They are not sealed protocol artifacts and do not authenticate humans.

1. Copy receipt.template.json outside this source directory. Assign evaluation
   and test IDs. Before execution, save exact ordered inputs, expected/oracle,
   approval reference, repository snapshot and executor/runtime information.
2. Each evidence entry uses PRESENT with path and SHA-256 of raw bytes, or
   MISSING/PARTIAL/UNRESOLVED with a reason. Do not guess model identity.
   Snapshot evidence should include commit, tree, dirty status and relevant
   working bytes/hashes. A storage commit is not an execution snapshot.
3. Record expected_timing as BEFORE_EXECUTION only when an independent record
   supports that order; otherwise AFTER_EXECUTION or UNRESOLVED. Preserve the
   pre-execution receipt separately and reference it in the final receipt.
4. Save final output and raw execution log, then complete result and reviewer.
   Keep functional result separate from provenance limitations. Unknown model
   identity does not rewrite a functional PASS into FAIL.
5. Run `python check_receipt.py receipt.json`. Relative evidence paths resolve
   from the receipt directory. The read-only check validates structure and
   hashes. OK means supplied references match, not complete reconstruction,
   authentic provenance, semantic alignment, or release approval. Exit 1 means
   malformed structure or broken hash/path; limitations remain explicit on OK.
6. Copy handoff.template.md for human review. Show all three gate outcomes plus
   accepted-item coverage uncertainty together. Never use this table as Semantic.

Do not rewrite historical results or backdate receipts. See historical-notes.md.
No DB, network, automatic execution, model access or new protocol gate is added.
Protected sources and prior sealed runs remain untouched.

Limited tests: from experiments/trinity, run
`python -m unittest discover -s operations -p 'test_*.py' -v`.

Still requires Human design decisions: semantic enforcement boundary, coverage
and materiality rules, checker responsibility, compatibility and the permitted
uses of provenance-incomplete historical evidence. This operations aid does not
resolve R1-B or implement Risk 02/04 production fixes.


## P1 Semantic confirmation and audit packaging

New Semantic checks require two separately supplied validators:
`manager.checks(run, primary, contract, reviewer=reviewer)`.
Both receive the same immutable ValidationRequest, without each other's verdict.
Each is called at most once. The host must use isolated fresh sessions, exclude
oracle/peer outputs, and preserve full requests, raw responses and adapter files.
Different checker IDs are required, but are not authentication or isolation proof.
No service, automatic AI dispatch or retry has been added.

A single ALIGNED no longer authorizes release. Both valid bound results must be
ALIGNED. A reported material failure yields MISALIGNED; missing confirmation or
uncertainty prevents ALIGNED. A missing/broken primary stays UNRESOLVED. Human
review cannot replace either validator. Old sealed receipts remain readable,
but receipts without confirmation cannot authorize a new Release decision.
Binding is unchanged. Release only verifies the Semantic receipt and aggregation.
This changes single-validator compatibility intentionally; configure a separate
reviewer to obtain ALIGNED, rather than copying the primary response or renaming
its identity. Two wrong ALIGNED judgments can still pass: this is a mitigation
of single-verdict trust, not proof of arbitrary semantic truth.

To package a preselected audit directory outside the repository:
`python -B -m operations.audit_package EVIDENCE_DIRECTORY NEW_ZIP_PATH`
The directory must contain adapter-input.json and effective-provenance.json.
For the second validator, include reviewer-adapter-input.json and
reviewer-effective-provenance.json together. Preserve original raw files too.
The tool copies evidence byte-for-byte and adds config hash preimages,
canonicalization rules and packaging-time implementation bytes under audit-support/.
It rejects inconsistent effective hashes and refuses overwriting an existing ZIP.
No oracle/secret filtering is inferred: the operator must preselect blind-safe files.
Support code is the packaging-time snapshot, not retroactive proof of which code
executed a historical run. Existing bundles and historical results are not updated.

Targeted tests: `python -B -m unittest tests.test_semantic_trust -v`.
Fixed verdict injection tests transport, aggregation and fail-closed behavior;
they do not measure real AI detection accuracy, session isolation or false-reject rates.
