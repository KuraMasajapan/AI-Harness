from tests.support import *
from validation.semantic_alignment import validate

class SemanticRegression(Base):
    def replace_rows(self, adapter, rows):
        original = adapter.evaluate
        adapter.evaluate = lambda request: dict(original(request), requirements=rows)

    def evaluate(self, adapter, text="The required deployment region is Tokyo."):
        run = self.ready(text)
        return self.manager.checks(run, adapter, CONTRACT, reviewer=FixtureValidator("fixture-confirmation"))[1]

    def test_predeclared_corpus_controls(self):
        for text, expected in (("The required deployment region is Tokyo.", "ALIGNED"),
                               ("The required deployment region is Osaka.", "MISALIGNED"),
                               ("Tokyo deployment region was considered; use the previous Osaka deployment region.", "MISALIGNED"),
                               ("Insufficient information.", "UNRESOLVED")):
            with self.subTest(text=text):
                self.assertEqual(self.evaluate(FixtureValidator(), text)["result"], expected)

    def test_infrastructure_failure_no_retry(self):
        class Broken(FixtureValidator):
            calls = 0
            def evaluate(self, request):
                self.calls += 1
                raise RuntimeError("offline failure")
        adapter = Broken()
        result = self.evaluate(adapter)
        self.assertEqual(result["result"], "UNRESOLVED")
        self.assertEqual(adapter.calls, 1)
        self.assertIn("offline failure", result["infrastructure_error"])

    def test_self_approval_and_comparator_unresolved(self):
        for who in ("response-producer", "C"):
            adapter = FixtureValidator()
            adapter.provenance["checker_id"] = who
            self.assertEqual(self.evaluate(adapter)["result"], "UNRESOLVED")

    def test_missing_and_duplicate_requirement_mapping(self):
        for rows in ([], [dict(requirement_id="region", status="COVERED", response_evidence="Tokyo", notes=None)] * 2):
            adapter = FixtureValidator()
            self.replace_rows(adapter, rows)
            self.assertEqual(self.evaluate(adapter)["result"], "UNRESOLVED")

    def test_missing_material_requirement_is_misaligned(self):
        adapter = FixtureValidator()
        self.replace_rows(adapter, [dict(requirement_id="region", status="MISSING", response_evidence=None, notes=None)])
        self.assertEqual(self.evaluate(adapter)["result"], "MISALIGNED")

    def test_fabricated_evidence_unresolved(self):
        adapter = FixtureValidator()
        self.replace_rows(adapter, [dict(requirement_id="region", status="COVERED", response_evidence="not in candidate", notes=None)])
        self.assertEqual(self.evaluate(adapter)["result"], "UNRESOLVED")

    def test_incomplete_provenance_and_wrong_contract_unresolved(self):
        for key in ("checker_id", "config_hash", "prompt_hash"):
            adapter = FixtureValidator()
            adapter.provenance.pop(key)
            self.assertEqual(self.evaluate(adapter)["result"], "UNRESOLVED")
        adapter = FixtureValidator()
        adapter.provenance["prompt_hash"] = "0" * 64
        self.assertEqual(self.evaluate(adapter)["result"], "UNRESOLVED")


    def test_local_review_adapter_binds_exact_artifacts(self):
        from validation.local_review import LocalReviewValidator
        from pathlib import Path
        run = self.ready()
        m = self.manager.load(run)
        candidate = self.manager.store.get(m["final_candidate_artifact_id"])
        review = dict(task_package_hash=m["task_package_hash"], candidate_artifact_id=candidate["artifact_id"],
                      candidate_content_hash=candidate["content_hash"],
                      provenance=dict(checker_id="external-test-validator", checker_type="test-double", checker_version="fixed-review-v2",
                                      model_name=None, model_version=None, prompt_hash=digest(CONTRACT)),
                      requirements=[dict(requirement_id="region", status="COVERED", response_evidence="Tokyo", notes=None)])
        from validation.accepted_coverage import header, items
        disposition = self.manager.store.get(m["human_disposition_id"])
        review["accepted_item_coverage"] = dict(**header(disposition, "fixed-review-v2"), items=[
            dict(item_id=i["item_id"], item_index=i["item_index"], required=True, status="COVERED",
                 response_evidence="Tokyo", notes="Independent fixed test verdict") for i in items(disposition)])
        path = Path(self.temp.name) / "review.json"
        write_json(path, review)
        adapter = LocalReviewValidator(path)
        # The adapter has already captured the review; later file mutations cannot change it.
        write_json(path, {})
        self.assertEqual(self.manager.checks(run, adapter, CONTRACT, reviewer=FixtureValidator("fixture-confirmation"))[1]["result"], "ALIGNED")
        other = self.ready()
        self.assertEqual(self.manager.checks(other, adapter, CONTRACT, reviewer=FixtureValidator("fixture-confirmation"))[1]["result"], "UNRESOLVED")

    def test_malformed_mapping_fails_closed(self):
        adapter = FixtureValidator()
        self.replace_rows(adapter, [dict(requirement_id="region", status="COVERED", response_evidence="Tokyo")])
        self.assertEqual(self.evaluate(adapter)["result"], "UNRESOLVED")
