"""One-shot fixed verdict injection, not a production semantic classifier."""
import copy
import hashlib
import json
from pathlib import Path
import zipfile
from tests.support import Base
from controller.artifact_store import digest, write_json
from protocol.schema_validation import validate_named
from validation.accepted_coverage import header
from validation.local_review import LocalReviewValidator, config_hash_receipt
from operations.audit_package import build

FIXTURE = json.loads((Path(__file__).parents[1] / "fixtures/p1_trust_boundary.json").read_text(encoding="utf-8"))


class Verdict:
    def __init__(self, checker_id, status="COVERED", transform=None):
        self.calls, self.requests = 0, []
        self.status, self.transform = status, transform
        self.provenance = dict(checker_id=checker_id, checker_type="test-double",
            checker_version="p1-semantic-contract-v1", model_name=None, model_version=None,
            config_hash=digest(dict(test_only=True, status=status)), prompt_hash=digest(FIXTURE["contract"]))

    def evaluate(self, request):
        self.calls += 1
        self.requests.append(request)
        task = json.loads(request.task_json)["content"]
        text = json.loads(request.candidate_json)["content"]["text"]
        rows = [dict(requirement_id=r["requirement_id"],
                     status="COVERED" if r["requirement_id"] == "R1" else self.status,
                     response_evidence=text, notes="Predeclared injection verdict, not a model judgment")
                for r in task["requirements"]]
        coverage = dict(**header(json.loads(request.disposition_json), self.provenance["checker_version"]),
            items=[dict(item_id=i["item_id"], item_index=i["item_index"], required=True,
                        status="COVERED", response_evidence="配置先はTokyoです。", notes="Tokyo coverage retained")
                   for i in json.loads(request.accepted_items_json)])
        output = dict(requirements=rows, accepted_item_coverage=coverage)
        if self.transform:
            self.transform(output)
        return output


class SemanticTrustBoundary(Base):
    def prepare(self, normal=False):
        run = self.manager.create(FIXTURE["task"])
        inputs = self.manager.input_manifest(run)
        self.manager.start_analysts(run, inputs, inputs)
        self.manager.register_analyst(run, "A", "固定A fixture: Tokyo")
        self.manager.register_analyst(run, "B", "固定B fixture: Tokyo")
        self.manager.start_comparator(run)
        self.manager.register_comparator(run, "固定C fixture: Tokyo")
        self.manager.disposition(run, "ACCEPT", accepted_items=FIXTURE["accepted_items"])
        self.manager.freeze(run, FIXTURE["normal_candidate" if normal else "problem_candidate"], "fixture-producer")
        return run

    def execute(self, primary, reviewer, normal=False):
        run = self.prepare(normal)
        b, s = self.manager.checks(run, primary, FIXTURE["contract"], reviewer=reviewer)
        self.assertEqual(b["result"], "PASS")
        validate_named(s, "semantic_result")
        decision = self.manager.release(run)["decision"]
        self.outcome = dict(binding=b["result"], semantic=s["result"], release=decision)
        return run, s, decision

    def test_p1_2_injected_false_covered_without_confirmation_denied(self):
        p = Verdict("primary")
        _, s, decision = self.execute(p, None)
        self.assertEqual(s["semantic_confirmation"]["primary_result"], "ALIGNED")
        self.assertTrue(s["accepted_item_coverage"]["coverage_satisfied"])
        self.assertEqual((s["result"], decision), ("UNRESOLVED", "DENY"))
        self.assertEqual(p.calls, 1)

    def test_p1_2_injected_false_covered_detected_by_separate_reviewer(self):
        p, r = Verdict("primary"), Verdict("reviewer", "CONTRADICTED")
        _, s, decision = self.execute(p, r)
        self.assertEqual((s["result"], decision), ("MISALIGNED", "DENY"))
        self.assertTrue(s["accepted_item_coverage"]["coverage_satisfied"])
        self.assertEqual((p.calls, r.calls), (1, 1))
        self.assertEqual(p.requests, r.requests)
        self.assertEqual(set(vars(r.requests[0])), {"task_json", "candidate_json", "contract_json", "disposition_json", "accepted_items_json"})

    def test_normal_candidate_two_aligned_releases(self):
        _, s, decision = self.execute(Verdict("primary"), Verdict("reviewer"), normal=True)
        self.assertEqual((s["result"], decision), ("ALIGNED", "RELEASE"))

    def test_correlated_false_verdicts_remain_a_documented_limit(self):
        _, s, decision = self.execute(Verdict("primary"), Verdict("reviewer"))
        # This is an explicit residual-risk control, not a safety success.
        self.assertEqual((s["result"], decision), ("ALIGNED", "RELEASE"))

    def test_uncertain_reviewer_fails_closed(self):
        _, s, decision = self.execute(Verdict("primary"), Verdict("reviewer", "UNRESOLVED"))
        self.assertEqual((s["result"], decision), ("UNRESOLVED", "DENY"))

    def test_primary_none_remains_unresolved(self):
        _, s, decision = self.execute(None, Verdict("reviewer", "CONTRADICTED"))
        self.assertEqual((s["result"], decision), ("UNRESOLVED", "DENY"))

    def test_reviewer_cannot_upgrade_primary_failure(self):
        _, s, decision = self.execute(Verdict("primary", "CONTRADICTED"), Verdict("reviewer"))
        self.assertEqual((s["result"], decision), ("MISALIGNED", "DENY"))

    def test_same_instance_or_declared_id_is_rejected(self):
        p = Verdict("primary")
        _, s, decision = self.execute(p, p)
        self.assertEqual((s["result"], decision, p.calls), ("UNRESOLVED", "DENY", 1))
        r = Verdict("primary")
        _, s, decision = self.execute(Verdict("primary"), r)
        self.assertEqual((s["result"], decision, r.calls), ("UNRESOLVED", "DENY", 0))

    def test_reviewer_human_cannot_override(self):
        r = Verdict("reviewer")
        r.provenance["checker_type"] = "human-review"
        _, s, decision = self.execute(Verdict("primary"), r)
        self.assertEqual((s["result"], decision, r.calls), ("UNRESOLVED", "DENY", 0))

    def test_stale_disposition_and_bad_evidence_denied(self):
        for mutate in (lambda o: o["accepted_item_coverage"].update(human_disposition_content_hash="0"*64),
                       lambda o: o["requirements"][1].update(response_evidence="invented quote")):
            _, s, decision = self.execute(Verdict("primary"), Verdict("reviewer", transform=mutate))
            self.assertEqual((s["result"], decision), ("UNRESOLVED", "DENY"))

    def test_missing_legacy_confirmation_denied_without_rewriting(self):
        run = self.prepare(normal=True)
        self.manager.checks(run, Verdict("primary"), FIXTURE["contract"], reviewer=Verdict("reviewer"))
        m = self.manager.load(run)
        record = self.manager.store.get(m["semantic_alignment_result_artifact_id"])
        body = copy.deepcopy(record["content"])
        body.pop("semantic_confirmation")
        validate_named(body, "semantic_result")
        legacy = self.manager.store.seal("SEMANTIC_ALIGNMENT_RESULT", run, body, m["event_seq"]+1, record["source_artifact_ids"])
        path = self.manager.store.path(legacy["artifact_id"])
        before = path.read_bytes()
        self.inject(run, semantic_alignment_result_artifact_id=legacy["artifact_id"])
        self.assertEqual(self.manager.release(run)["decision"], "DENY")
        self.assertEqual(path.read_bytes(), before)

    def test_stale_or_forged_confirmation_summary_denied(self):
        for mutate in (lambda c: c["review"].update(candidate_content_hash="0"*64),
                       lambda c: c["review"].update(task_package_hash="0"*64),
                       lambda c: c["review"]["requirements"][1].update(status="CONTRADICTED")):
            run = self.prepare(normal=True)
            self.manager.checks(run, Verdict("primary"), FIXTURE["contract"], reviewer=Verdict("reviewer"))
            m = self.manager.load(run)
            record = self.manager.store.get(m["semantic_alignment_result_artifact_id"])
            body = copy.deepcopy(record["content"])
            mutate(body["semantic_confirmation"])
            injected = self.manager.store.seal("SEMANTIC_ALIGNMENT_RESULT", run, body, m["event_seq"]+1, record["source_artifact_ids"])
            self.inject(run, semantic_alignment_result_artifact_id=injected["artifact_id"])
            self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_reviewer_exception_once(self):
        r = Verdict("reviewer")
        def broken(request):
            r.calls += 1
            raise RuntimeError("review unavailable")
        r.evaluate = broken
        _, s, decision = self.execute(Verdict("primary"), r)
        self.assertEqual((s["result"], decision, r.calls), ("UNRESOLVED", "DENY", 1))


class AuditPackage(Base):
    def setup_evidence(self):
        source = Path(self.temp.name)/"evidence"
        source.mkdir()
        review = dict(provenance=dict(checker_id="external", config_hash="0"*64), requirements=[])
        write_json(source/"adapter-input.json", review)
        write_json(source/"effective-provenance.json", dict(config_hash=config_hash_receipt(review)["config_hash"]))
        (source/"raw-response.txt").write_bytes(b'{"raw": "unchanged"}\r\n')
        return source, review

    def test_reproducible_hash_rule_and_unchanged_evidence(self):
        source, review = self.setup_evidence()
        before = {p.name:p.read_bytes() for p in source.iterdir()}
        destination = Path(self.temp.name)/"audit.zip"
        build(source, destination)
        self.assertEqual(before, {p.name:p.read_bytes() for p in source.iterdir()})
        with zipfile.ZipFile(destination) as z:
            receipt = json.loads(z.read("audit-support/config-hash-receipt.json"))
            self.assertEqual(receipt["config_hash"], digest(dict(adapter="local-review-v1", review_hash=digest(review))))
            for name, data in before.items(): self.assertEqual(z.read("evidence/"+name), data)
            for row in json.loads(z.read("MANIFEST.json")):
                self.assertEqual(hashlib.sha256(z.read(row["path"])).hexdigest(), row["sha256"])
            self.assertIn("audit-support/implementation/validation/local_review.py", z.namelist())
        adapter = LocalReviewValidator(source/"adapter-input.json")
        self.assertEqual(adapter.provenance["config_hash"], receipt["config_hash"])
        with self.assertRaises(FileExistsError): build(source, destination)

    def test_wrong_effective_hash_refuses_package(self):
        source, _ = self.setup_evidence()
        write_json(source/"effective-provenance.json", dict(config_hash="0"*64))
        with self.assertRaises(ValueError): build(source, Path(self.temp.name)/"audit.zip")
        self.assertFalse((Path(self.temp.name)/"audit.zip").exists())

    def test_reviewer_hash_rule_included_and_mismatch_rejected(self):
        source, review = self.setup_evidence()
        write_json(source/"reviewer-adapter-input.json", review)
        write_json(source/"reviewer-effective-provenance.json", dict(config_hash=config_hash_receipt(review)["config_hash"]))
        path = Path(self.temp.name)/"reviewer.zip"
        build(source, path)
        with zipfile.ZipFile(path) as z:
            receipt = json.loads(z.read("audit-support/reviewer-config-hash-receipt.json"))
            self.assertEqual(receipt["config_hash"], config_hash_receipt(review)["config_hash"])
        write_json(source/"reviewer-effective-provenance.json", dict(config_hash="0"*64))
        with self.assertRaises(ValueError): build(source, Path(self.temp.name)/"bad.zip")
