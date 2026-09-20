import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from check_receipt import check


class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = self.root / "receipt.json"
        self.value = json.loads(Path(__file__).with_name("receipt.template.json").read_text())
        self.value.update(evaluation_id="limited-test", test_id="receipt-v1", phase="FINAL",
                          recorded_at="2026-09-20T00:00:00Z", functional_result="PASS",
                          expected_timing="BEFORE_EXECUTION", limitations=[])
        self.evidence = self.root / "evidence.txt"
        self.evidence.write_bytes(b"controlled fixture\n")
        entry = dict(status="PRESENT", path="evidence.txt",
                     sha256=hashlib.sha256(self.evidence.read_bytes()).hexdigest())
        self.value["evidence"] = {k: copy.deepcopy(entry) for k in self.value["evidence"]}
        self.value["ordered_inputs"] = [copy.deepcopy(entry)]

    def run_check(self):
        self.path.write_text(json.dumps(self.value), encoding="utf-8")
        return check(self.path)

    def test_matching_references(self):
        result = self.run_check()
        self.assertEqual(result["check"], "OK")
        self.assertEqual(result["limitations"], [])

    def test_unknown_model_preserves_pass(self):
        self.value["evidence"]["executor_model"] = dict(status="UNRESOLVED", reason="Deployment unavailable")
        result = self.run_check()
        self.assertEqual(result["functional_result"], "PASS")
        self.assertTrue(any("executor_model" in x for x in result["limitations"]))

    def test_declared_limitation_preserved(self):
        self.value["limitations"] = ["Not independently authenticated"]
        self.assertIn("Not independently authenticated", self.run_check()["limitations"])

    def test_changed_bytes_fail_without_mutation(self):
        self.evidence.write_bytes(b"changed\n")
        result = self.run_check()
        self.assertEqual(result["check"], "ERROR")
        self.assertEqual(self.evidence.read_bytes(), b"changed\n")

    def test_missing_file_fails(self):
        self.evidence.unlink()
        self.assertEqual(self.run_check()["check"], "ERROR")

    def test_posthoc_expected_not_preregistered(self):
        self.value["expected_timing"] = "AFTER_EXECUTION"
        result = self.run_check()
        self.assertIn("expected timing: AFTER_EXECUTION", result["limitations"])
        self.assertEqual(result["functional_result"], "PASS")

    def test_incomplete_schema_rejected(self):
        del self.value["evidence"]["execution_log"]
        with self.assertRaises(Exception):
            self.run_check()

    def test_unknown_requires_reason(self):
        self.value["evidence"]["executor_model"] = dict(status="UNRESOLVED", reason="")
        with self.assertRaises(Exception):
            self.run_check()

    def test_invalid_hash_rejected(self):
        self.value["ordered_inputs"][0]["sha256"] = "not-a-hash"
        with self.assertRaises(Exception):
            self.run_check()


if __name__ == "__main__":
    unittest.main()
