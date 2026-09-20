from tests.support import *
from fixtures.runner import run_suite
from protocol.schema_validation import validate_named, validate
from controller.artifact_store import ProtocolError
from pathlib import Path
import json

class Conformance(Base):
    def test_required_fixtures_and_presealed_ground_truth(self):
        results = run_suite(self.temp.name)
        self.assertEqual(len(results), 9)
        self.assertTrue(all(r["result"] == "PASS" for r in results))
        audit = json.loads((Path(self.temp.name) / "test-audit.json").read_text(encoding="utf-8"))
        sealed_seq = next(e["event_seq"] for e in audit["events"] if e["event_type"] == "TEST_MANIFEST_SEALED")
        for record in audit["artifacts"].values():
            if record["artifact_type"] == "TEST_RESULT":
                self.assertGreater(record["created_event_seq"], sealed_seq)
        for path in Path(self.temp.name).glob("*-audit.json"):
            self.validate_audit(json.loads(path.read_text(encoding="utf-8")))

    def validate_audit(self, audit):
        validate_named(audit["manifest"], "run_manifest")
        names = {"TASK_PACKAGE": "task_package", "HUMAN_DISPOSITION": "human_disposition",
                 "BINDING_RESULT": "binding_result", "SEMANTIC_ALIGNMENT_RESULT": "semantic_result",
                 "RELEASE_DECISION": "release_decision", "TEST_MANIFEST": "test_manifest", "TEST_RESULT": "test_result"}
        for event in audit["events"]:
            validate_named(event, "event")
            if event["event_type"] == "OPERATOR_INTERVENTION_RECORDED":
                validate_named(event["metadata"], "intervention")
        for record in audit["artifacts"].values():
            validate_named(record, "artifact")
            if record["artifact_type"] in names:
                validate_named(record["content"], names[record["artifact_type"]])

    def test_schema_rejects_invalid_records(self):
        run = self.ready()
        self.validate_audit(self.manager.audit(run))
        manifest = self.manager.load(run)
        for changes in (dict(state="BOGUS"), dict(event_seq=True), dict(task_package_hash="not-a-hash"), dict(extra=True)):
            with self.assertRaises(ProtocolError):
                validate_named(dict(manifest, **changes), "run_manifest")
        manifest.pop("run_id")
        with self.assertRaises(ProtocolError):
            validate_named(manifest, "run_manifest")
        with self.assertRaises(ProtocolError):
            validate({}, {"unimplementedKeyword": True})

    def test_sources_are_not_implicit_instructions(self):
        task = dict(TASK, source_artifact_ids=["old-transcript"])
        with self.assertRaises(ProtocolError):
            self.manager.create(task)

    def test_materiality_is_explicit(self):
        task = copy.deepcopy(TASK)
        del task["requirements"][0]["material"]
        with self.assertRaises(ProtocolError):
            self.manager.create(task)

    def test_utf8_lf_and_json_files(self):
        root = Path(__file__).parents[1]
        for path in root.rglob("*"):
            if not path.is_file() or ".local" in path.parts or "__pycache__" in path.parts:
                continue
            data = path.read_bytes()
            self.assertFalse(data.startswith(b"\xef\xbb\xbf"), str(path))
            self.assertNotIn(b"\r", data, str(path))
            data.decode("utf-8")
            if path.suffix == ".json":
                json.loads(data)
