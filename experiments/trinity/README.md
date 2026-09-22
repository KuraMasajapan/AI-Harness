# TRINITY V0.1 local prototype

This experimental implementation follows the supplied TRINITY V0.1 Implementation
Specification. It is not formally adopted, production-ready, or a claim of semantic
conformance. All changes are contained in experiments/trinity/.

## Run locally

Python 3.10 or newer; standard library only. No installation, database, network,
external service, or model access is required.

From this directory:

```text
python -m unittest discover -s tests -v
```

This one command validates generated records against the JSON Schemas, runs
state-machine, artifact integrity, binding, release, isolation, conformance and
semantic adapter regression tests, and prints PASS/FAIL for all nine required
fixtures. Run the fixture suite with retained audit files using:

```text
python -m fixtures.runner --output .local/fixture-audit
```

Each fixture produces a JSON audit, and test-audit.json contains the sealed Test
Manifest, input hashes and Test Results. Expected results are loaded and sealed
before any checker runs. The fixed response corpus is a **test double**: it tests
the adapter contract and release controls, not real semantic detection quality.
The production semantic regression acceptance threshold remains unresolved.

## Architecture and role boundaries

- A and B receive separately deserialized copies of the same sealed task, with
  no shared workspace, peer outputs, or old transcript references.
- C first receives both sealed analyst artifacts when comparator execution starts.
  Its input includes the canonical task, operator log and explicit comparison
  instructions. C compares once; it does not select a winner or certify truth.
- O is RunManager and the deterministic gates. O validates structure, hashes,
  ordering and routing; it does not interpret task text or perform reasoning.
- H records a separate immutable disposition. H can disagree with C without
  changing C's historical artifact.

The trusted host owns RunManager and ArtifactStore. Reasoning roles receive only
the detached JSON from role_inputs(); do not give roles the controller object,
store directory, host filesystem access or shared model/session history. This
prototype is a local protocol controller, not a sandbox for arbitrary hostile
Python code. A real runtime must provide fresh isolated contexts and enforce that
host boundary. No AI execution engine is included.

Evidence is data. The controller never executes instruction-like artifact text.
Only the explicit task instructions field is routed as task instructions; the
prototype rejects extra analyst input references, source imports and transcripts.
An imported immutable evidence lineage adapter is not included.

## Lifecycle and API

The public API is controller.run_manager.RunManager:

1. create(task) seals a task. Supply title, objective, instructions,
   required_output, constraints and requirements. Each requirement explicitly
   supplies requirement_id, text and material (boolean), declared by the caller.
2. input_manifest(run) returns a clean input descriptor.
   start_analysts(run, a_input, b_input) checks exact descriptor equality before
   either analyst starts. A mismatch invalidates the run.
3. role_inputs(run, "A") / role_inputs(run, "B") return independent input copies.
   register_analyst(run, role, text) seals each externally produced final output.
4. start_comparator(run) returns C's inputs only after both analysts are sealed.
   register_comparator(run, text) seals C's externally produced comparison.
5. disposition(run, decision, ...) logs the human intervention and seals it.
6. freeze(run, exact_text, producer_id) creates the exact user-visible candidate.
7. checks(run, validator, contract) writes separate binding and semantic artifacts.
8. release(run) records RELEASE or DENY. Only RELEASE returns the exact frozen
   text and transitions to RELEASED. A terminal-run attempt returns DENY without
   changing the historical release decision.

A new candidate can be frozen after an unsuccessful check/decision. It gets a new
artifact ID and clears both checks and the prior decision reference. Historical
artifacts remain available. Checks are never retried automatically; invoking
checks twice for the same frozen candidate is rejected. A recorded decision is
immutable. No downstream rewriting is permitted.

Task-changing amendments require an explicit declaration:

```python
replacement = manager.amend(
    run_id,
    {"type": "TASK_AMENDMENT", "reason": "Human changes the objective",
     "changes_task_conditions": True},
    updated_task,
)
```

The old run terminates before the new task/run is created. The manifests link
previous/replacement IDs. Both new analyst starts use identical empty-history
inputs. There is no same-run amendment, negotiation, or C-to-A/B channel.
Non-task-changing operator notices may be logged for audit; injecting additional
material into active A/B contexts is deliberately unavailable in this prototype.

## Binding and semantic alignment

Binding checks run/task/candidate identity, hashes, required sealed A/B/C/H
artifacts, current-run source lineage and terminal/invalidation status. It never
uses text similarity. Semantic alignment receives immutable JSON strings for the
exact task, exact candidate and checker contract.

validation.semantic_alignment.Validator defines the adapter interface.
validation.local_review.LocalReviewValidator accepts a separately prepared local
review JSON containing task_package_hash, candidate_artifact_id,
candidate_content_hash, provenance and requirements. provenance must supply
checker_id, checker_type, checker_version, model_name, model_version and prompt_hash (SHA-256 of
the canonical contract). The adapter derives config_hash from the review content.
The gate adds a unique execution_id. Each requirement row supplies requirement_id,
status, response_evidence and notes. Evidence for COVERED/CONTRADICTED must be a
literal excerpt in the frozen response. The JSON is read once so subsequent file
edits cannot alter that invocation.

Any contradiction or explicitly material missing item yields MISALIGNED.
Unresolved material coverage, missing/malformed validator output, infrastructure
failure, stale local review or unavailable validator yields UNRESOLVED. Otherwise
the declared requirement mapping yields ALIGNED. This aggregation is in the
validation boundary, not the controller's reasoning. Producer self-validation
is rejected. C-as-validator is disabled until its runtime lifecycle is reviewed.
The host must authenticate human/validator identities; these strings are
provenance identifiers, not authentication credentials.

Release requires a fresh Binding PASS, Semantic ALIGNED, human disposition and
all required sealed artifacts. FAIL, MISALIGNED, UNRESOLVED, stale results,
corruption or missing artifacts deny release. Human disposition decision values
are preserved as specified; no new decision-enum policy is invented.

## Storage and audit

JSON and JSONL use UTF-8 without BOM and LF. Each JSONL line is one JSON event.
The canonical serialization is Python JSON with sorted keys, compact separators,
ensure_ascii=False, allow_nan=False. SHA-256 always hashes its UTF-8 bytes.
No cross-language canonicalization standard is claimed.

Task hash excludes only its own task_package_hash field. Artifact content_hash
hashes content; record_hash additionally protects the complete metadata envelope.
Events carry a hash chain and monotonically increasing event_seq plus the
resulting manifest snapshot. Timestamps are informational/null.

Artifacts are created exclusively and never edited through the API. Operator
log entries live in the append-only journal referenced by the immutable log
artifact. audit_repair records the original hash, exact added visible transcript
and reason, including after termination/release, without reopening the state or
modifying sealed proposals. It does not capture hidden reasoning.

audit(run) exports manifests, events, intervention entries, recursively referenced
artifacts and validity diagnostics. Invalid/missing records remain identifiable
in validity_records. The decision references the exact released artifact.

A local exclusive writer marker rejects overlapping mutations. Normal completed
runs reload from files. Interrupted or inconsistent journals fail closed and
require manual review; the marker is not a crash-recovery protocol. Filesystem
administrators can rewrite unsigned hashes; signatures, remote attestation and
host-level adversary resistance are outside V0.1.

## Schemas and scope

protocol/schemas/ contains draft 2020-12 JSON Schemas for envelopes and typed
contents. Artifact bodies are validated separately by artifact_type; envelope
fields such as run_id and sealed are not duplicated in every body. The offline
validator implements only the vocabulary used here and rejects unsupported
keywords; it is not a replacement for a general JSON Schema engine.

config.json records fixed implementation choices and unresolved configuration
points. It is descriptive, not a switch that can change protocol policy.
UNRESOLVED.md documents review/runtime decisions. protocol/state_machine.md
describes allowed transitions.

Not included: models/services, DB, UI, imported evidence routing, production
concurrency/recovery, voting, consensus scores, analyst debate, AI orchestrator,
autonomous retries, hidden chain-of-thought capture, or automatic Core / RULES /
LESSONS promotion. Optional/Future features remain outside this prototype.


## Accepted-item Semantic coverage (R1-B v0.1)

Binding remains identity/seal/lineage only. Semantic now supplies the immutable
Human Disposition and ordered accepted-item occurrences to the external validator
in disposition_json and accepted_items_json, alongside the existing task,
candidate and contract strings. Each occurrence has a Disposition-ID/index based
item_id, item_index, original text and required=true. Equal strings are not merged;
rejected/deferred entries are not included. The current Disposition schema has no
optional-item metadata: all accepted entries are required. No exception is inferred.

Validator.evaluate returns one object with requirements (the existing task rows)
and accepted_item_coverage. The latter contains coverage_version="accepted-items-v0.1",
checker_version matching provenance.checker_version, human_disposition_artifact_id,
human_disposition_content_hash, and items. Each row carries item_id, item_index,
required=true, status, response_evidence, and nonblank notes explaining the verdict.
Statuses are COVERED/MISSING/CONTRADICTED/UNRESOLVED only. COVERED/CONTRADICTED
require an exact nonblank candidate excerpt. Checking excerpt provenance does not
infer semantic coverage: the external validator supplies the semantic judgment.
There is no keyword/substring coverage classifier in production code.

The Semantic boundary validates structure, occurrence identity, Disposition binding
and aggregation. It adds empty_set and coverage_satisfied to the stored result.
All required items must be COVERED for coverage_satisfied. MISSING/CONTRADICTED
produce MISALIGNED; unresolved coverage cannot produce ALIGNED. Existing task
requirement checks must also pass. Empty items are explicitly marked empty_set=true;
vacuous satisfaction does not claim meaningful coverage. validator=None remains
UNRESOLVED and Release DENY, including for an empty set.

LocalReviewValidator imports an independently produced validator result with the
same requirements and accepted_item_coverage fields, plus existing task/candidate
bindings and provenance. Human-local-review/human-review types cannot substitute
for this contract. There is no manual override of a stored UNRESOLVED result.
The trusted host must authenticate checker identity; strings are not credentials.

Legacy Semantic schema bodies remain readable without rewriting/backfill. Newly
created Semantic results always include coverage; Release checks its versioned
binding through the Semantic receipt validator and fails closed for legacy/missing/
stale coverage. Release does not interpret meaning. Old fixtures' saved artifacts
are unchanged. Fixture set 2-r1b expects UNRESOLVED rather than ALIGNED for foreign-run
and old-candidate coverage, with Binding FAIL / Release DENY unchanged.

Tests use explicitly labeled fixed verdicts, including paraphrase and contradiction
cases, to test the contract. They do not validate a production semantic model's
accuracy. No model/service integration or Risk 02/04 production change is included.
