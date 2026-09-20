# Unresolved implementation details

The user's current request resolves serialization (JSON), schemas (JSON Schema),
hashing (SHA-256), encoding (UTF-8), newlines (LF), prototype persistence (local
files), no DB and no external services. No existing automated repository test
framework was found; Python unittest is the selected lightweight baseline.

The following remain explicit review/integration points:

1. Human TASK_AMENDMENT UI wording and authenticated command integration.
   The API requires the specified explicit declaration. It does not classify text.
2. Production definition of material required item. The caller must declare a
   material boolean per requirement; this is an explicit prototype encoding, not
   a definition or automatic materiality policy.
3. Semantic infrastructure retry limit. No automatic retry is implemented. A null
   config value denotes an unresolved limit, not approval of a numeric policy.
4. Whether an actual C runtime may serve as semantic validator. C is rejected by
   this adapter boundary until the specified independence conditions are verified.
5. Numeric semantic regression acceptance threshold. No threshold is selected.
   Fixture tests cover the contract with a test double and do not establish
   production semantic accuracy or formal protocol conformance.
6. Production storage and concurrency. Local files satisfy this prototype request.
   A writer marker prevents overlapping mutations; production scheduling and
   transactional concurrency remain unspecified.
7. Crash recovery. Partially written or inconsistent journals fail closed.
   No automatic recovery, rollback or transaction guarantees are claimed.
8. Actual analyst/runtime isolation and identity authentication. The host must
   supply fresh contexts and give roles only detached input packages. This
   prototype exposes no AI runtime or operating-system sandbox.
9. Imported immutable evidence lineage. The initial prototype uses empty external
   source lists and rejects nonempty analyst extras. Supporting imported evidence
   requires an explicit immutable input adapter; old analyst transcripts must
   remain excluded.

Representation notes (not protocol policy changes): artifact metadata is an
envelope with typed content; event snapshots and record hashes are additive audit
fields; the initial RUN_CREATED event precedes TASK_PACKAGE_SEALED and therefore
has an empty task hash. Replacement-link and audit-correction events may append
to a terminal run without changing its terminal state. JSONL is used as an
appendable sequence of JSON event objects.

No new mutually exclusive protocol design choice was discovered. No Required
control is classified as optional or removed. This prototype must not be promoted
until the runtime/semantic acceptance review is completed by Human Authority.
