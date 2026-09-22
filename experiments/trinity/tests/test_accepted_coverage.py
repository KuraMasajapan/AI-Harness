"""Fixed validator verdicts test contracts, not real semantic model accuracy."""
import json
from tests.support import *
from controller.artifact_store import ProtocolError
from validation.accepted_coverage import header, items
from protocol.schema_validation import validate_named


class CoverageValidator(FixtureValidator):
    def __init__(self, status="COVERED", transform=None, checker_id="offline-fixture-adapter"):
        super().__init__(checker_id)
        self.status, self.transform, self.calls = status, transform, 0
        self.provenance["config_hash"] = digest(dict(fixed_status=status, test_only=True))

    def evaluate(self, request):
        self.calls += 1
        self.request = request
        candidate = json.loads(request.candidate_json)
        text = candidate["content"]["text"]
        requirements = json.loads(request.task_json)["content"]["requirements"]
        rows = [dict(requirement_id=r["requirement_id"], status="COVERED",
                     response_evidence=text, notes="Fixed task verdict") for r in requirements]
        coverage = dict(**header(json.loads(request.disposition_json), self.provenance["checker_version"]),
                        items=[dict(item_id=i["item_id"], item_index=i["item_index"], required=True,
                                    status=self.status,
                                    response_evidence=text if self.status in {"COVERED", "CONTRADICTED"} else None,
                                    notes="Predeclared test-double judgment; no semantic classifier")
                               for i in json.loads(request.accepted_items_json)])
        output = dict(requirements=rows, accepted_item_coverage=coverage)
        if self.transform:
            self.transform(output)
        return output


class AcceptedCoverage(Base):
    def prepare(self, accepted=("Disallow public access",), rejected=(), deferred=(),
                text="Only private connections are permitted."):
        task = copy.deepcopy(TASK)
        task["requirements"] = [dict(requirement_id="response", text="Return a response", material=True)]
        run = self.manager.create(task)
        inputs = self.manager.input_manifest(run)
        self.manager.start_analysts(run, inputs, inputs)
        self.manager.register_analyst(run, "A", "fixture A")
        self.manager.register_analyst(run, "B", "fixture B")
        self.manager.start_comparator(run)
        self.manager.register_comparator(run, "fixture C")
        self.manager.disposition(run, "ACCEPT", accepted_items=accepted,
                                 rejected_items=rejected, deferred_items=deferred)
        self.manager.freeze(run, text, "response-producer")
        return run

    def execute(self, status="COVERED", transform=None, **kwargs):
        run = self.prepare(**kwargs)
        adapter = CoverageValidator(status, transform)
        binding, semantic = self.manager.checks(run, adapter, CONTRACT, reviewer=CoverageValidator(checker_id="coverage-confirmation"))
        self.assertEqual(binding["result"], "PASS")
        self.assertEqual(adapter.calls, 1)
        validate_named(semantic, "semantic_result")
        return run, semantic, self.manager.release(run)["decision"]

    def test_A_paraphrase_covered_by_validator(self):
        _, result, release = self.execute()
        self.assertEqual(result["result"], "ALIGNED")
        self.assertTrue(result["accepted_item_coverage"]["coverage_satisfied"])
        self.assertEqual(release, "RELEASE")

    def test_B_missing_disposition_only_item(self):
        _, result, release = self.execute("MISSING", text="A response without access policy.")
        self.assertEqual(result["result"], "MISALIGNED")
        self.assertEqual(release, "DENY")

    def test_C_similar_words_contradicted(self):
        _, result, release = self.execute("CONTRADICTED", text="Disallow public access? No, allow public access.")
        self.assertEqual(result["accepted_item_coverage"]["items"][0]["status"], "CONTRADICTED")
        self.assertEqual(result["result"], "MISALIGNED")
        self.assertEqual(release, "DENY")

    def test_D_unresolved_verdict(self):
        _, result, release = self.execute("UNRESOLVED")
        self.assertEqual(result["result"], "UNRESOLVED")
        self.assertEqual(release, "DENY")

    def test_D_missing_or_fabricated_evidence(self):
        for evidence in (None, "not in the candidate"):
            with self.subTest(evidence=evidence):
                _, result, release = self.execute(transform=lambda o: o["accepted_item_coverage"]["items"][0].update(response_evidence=evidence))
                self.assertEqual(result["result"], "UNRESOLVED")
                self.assertEqual(release, "DENY")

    def test_D_none_validator_including_empty_set(self):
        for accepted in ((), ("policy",)):
            run = self.prepare(accepted=accepted)
            binding, result = self.manager.checks(run, validator=None)
            self.assertEqual(binding["result"], "PASS")
            self.assertEqual(result["result"], "UNRESOLVED")
            self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_E_empty_set(self):
        _, result, release = self.execute(accepted=())
        coverage = result["accepted_item_coverage"]
        self.assertEqual(coverage["items"], [])
        self.assertTrue(coverage["empty_set"])
        self.assertTrue(coverage["coverage_satisfied"])
        self.assertEqual(result["result"], "ALIGNED")
        self.assertEqual(release, "RELEASE")

    def test_F_id_hash_and_versions_mismatch(self):
        for key, value in (("human_disposition_artifact_id", "foreign"),
                           ("human_disposition_content_hash", "0" * 64),
                           ("coverage_version", "old"), ("checker_version", "stale")):
            with self.subTest(key=key):
                _, result, release = self.execute(transform=lambda o: o["accepted_item_coverage"].update({key: value}))
                self.assertEqual(result["result"], "UNRESOLVED")
                self.assertEqual(release, "DENY")

    def test_F_stale_disposition_result_denied(self):
        run = self.prepare()
        self.manager.checks(run, CoverageValidator(), CONTRACT, reviewer=CoverageValidator(checker_id="coverage-confirmation"))
        m = self.manager.load(run)
        old = self.manager.store.get(m["human_disposition_id"])
        new = self.manager.store.seal("HUMAN_DISPOSITION", run, old["content"], m["event_seq"] + 1,
                                      old["source_artifact_ids"])
        self.inject(run, human_disposition_id=new["artifact_id"])
        self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_G_duplicate_occurrences_preserved(self):
        _, result, release = self.execute(accepted=("same", "same"))
        rows = result["accepted_item_coverage"]["items"]
        self.assertEqual([r["item_index"] for r in rows], [0, 1])
        self.assertNotEqual(rows[0]["item_id"], rows[1]["item_id"])
        self.assertEqual(release, "RELEASE")

    def test_G_merged_duplicate_rejected(self):
        _, result, release = self.execute(accepted=("same", "same"),
            transform=lambda o: o["accepted_item_coverage"]["items"].pop())
        self.assertEqual(result["result"], "UNRESOLVED")
        self.assertEqual(release, "DENY")

    def test_H_rejected_and_deferred_excluded(self):
        _, result, release = self.execute(accepted=(), rejected=("reject",), deferred=("defer",))
        self.assertEqual(result["accepted_item_coverage"]["items"], [])
        self.assertEqual(release, "RELEASE")

    def test_I_legacy_sealed_receipt_readable_but_denied_unchanged(self):
        run = self.prepare()
        self.manager.checks(run, CoverageValidator(), CONTRACT, reviewer=CoverageValidator(checker_id="coverage-confirmation"))
        m = self.manager.load(run)
        record = self.manager.store.get(m["semantic_alignment_result_artifact_id"])
        legacy = copy.deepcopy(record["content"])
        legacy.pop("accepted_item_coverage")
        legacy["provenance"].pop("checker_version")
        validate_named(legacy, "semantic_result")
        old = self.manager.store.seal("SEMANTIC_ALIGNMENT_RESULT", run, legacy,
                                      m["event_seq"] + 1, record["source_artifact_ids"])
        self.inject(run, semantic_alignment_result_artifact_id=old["artifact_id"])
        old_path = self.manager.store.path(old["artifact_id"])
        original_path = self.manager.store.path(record["artifact_id"])
        before = old_path.read_bytes(), original_path.read_bytes()
        self.assertEqual(self.manager.release(run)["decision"], "DENY")
        self.manager.audit(run)
        self.assertEqual(before, (old_path.read_bytes(), original_path.read_bytes()))

    def test_I_legacy_validator_not_upgraded_even_empty(self):
        run = self.prepare(accepted=())
        adapter = CoverageValidator()
        original = adapter.evaluate
        adapter.evaluate = lambda request: original(request)["requirements"]
        result = self.manager.checks(run, adapter, CONTRACT, reviewer=CoverageValidator(checker_id="coverage-confirmation"))[1]
        self.assertEqual(result["result"], "UNRESOLVED")
        self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_human_review_not_semantic_override(self):
        run = self.prepare()
        adapter = CoverageValidator()
        adapter.provenance["checker_type"] = "human-local-review"
        self.assertEqual(self.manager.checks(run, adapter, CONTRACT, reviewer=CoverageValidator(checker_id="coverage-confirmation"))[1]["result"], "UNRESOLVED")
        self.assertEqual(adapter.calls, 0)
        with self.assertRaises(ProtocolError):
            self.manager.checks(run, CoverageValidator(), CONTRACT, reviewer=CoverageValidator(checker_id="coverage-confirmation"))

    def test_required_cannot_be_disabled_by_validator(self):
        _, result, release = self.execute(transform=lambda o: o["accepted_item_coverage"]["items"][0].update(required=False))
        self.assertEqual(result["result"], "UNRESOLVED")
        self.assertEqual(release, "DENY")

    def test_missing_rationale_unresolved(self):
        _, result, release = self.execute(transform=lambda o: o["accepted_item_coverage"]["items"][0].update(notes=""))
        self.assertEqual(result["result"], "UNRESOLVED")
        self.assertEqual(release, "DENY")

    def test_invalid_checker_version_fails_closed(self):
        for version in (None, "", " ", 1):
            run = self.prepare()
            adapter = CoverageValidator()
            adapter.provenance["checker_version"] = version
            result = self.manager.checks(run, adapter, CONTRACT, reviewer=CoverageValidator(checker_id="coverage-confirmation"))[1]
            self.assertEqual(result["result"], "UNRESOLVED")
            self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_stored_false_summary_cannot_override_rows(self):
        run = self.prepare()
        self.manager.checks(run, CoverageValidator("MISSING"), CONTRACT, reviewer=CoverageValidator(checker_id="coverage-confirmation"))
        m = self.manager.load(run)
        record = self.manager.store.get(m["semantic_alignment_result_artifact_id"])
        body = copy.deepcopy(record["content"])
        body["result"] = "ALIGNED"
        body["accepted_item_coverage"]["coverage_satisfied"] = True
        replacement = self.manager.store.seal("SEMANTIC_ALIGNMENT_RESULT", run, body,
                                              m["event_seq"] + 1, record["source_artifact_ids"])
        self.inject(run, semantic_alignment_result_artifact_id=replacement["artifact_id"])
        self.assertEqual(self.manager.release(run)["decision"], "DENY")
