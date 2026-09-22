"""Targeted beta runtime bridge test; no model or network call is made."""
import copy
import json
import tempfile
from pathlib import Path

from tests.support import Base
from operations.beta_runtime import run_saved_pair
from tests.test_semantic_trust import FIXTURE
from controller.artifact_store import digest, write_json


class BetaRuntime(Base):
    def test_saved_pair_uses_normal_gates(self):
        run = self.manager.create(FIXTURE["task"])
        inputs = self.manager.input_manifest(run)
        self.manager.start_analysts(run, inputs, inputs)
        self.manager.register_analyst(run, "A", "fixture A")
        self.manager.register_analyst(run, "B", "fixture B")
        self.manager.start_comparator(run)
        self.manager.register_comparator(run, "fixture C")
        self.manager.disposition(run, "ACCEPT", accepted_items=FIXTURE["accepted_items"])
        candidate = FIXTURE["normal_candidate"]
        self.manager.freeze(run, candidate, "beta-runtime-test")
        manifest = self.manager.load(run)
        task = self.manager.store.get(manifest["task_artifact_id"])
        final = self.manager.store.get(manifest["final_candidate_artifact_id"])
        disp = self.manager.store.get(manifest["human_disposition_id"])
        base = {
            "task_package_hash": task["content"]["task_package_hash"],
            "candidate_artifact_id": final["artifact_id"],
            "candidate_content_hash": final["content_hash"],
            "provenance": {
                "checker_id": "beta-runtime-primary",
                "checker_type": "external-chatgpt-saved-response",
                "checker_version": "beta-semantic-contract-v1",
                "model_name": None, "model_version": None,
                "config_hash": digest({"runtime_test": True}),
                "prompt_hash": digest(FIXTURE["contract"]),
            },
            "requirements": [{"requirement_id": "R1", "status": "COVERED",
                               "response_evidence": "配置先はTokyoです。", "notes": "saved receipt"},
                              {"requirement_id": "R2", "status": "COVERED",
                               "response_evidence": "model API呼出しはありません。", "notes": "saved receipt"},
                              {"requirement_id": "R3", "status": "COVERED",
                               "response_evidence": "未記録でnetwork isolationも未試験", "notes": "saved receipt"}],
            "accepted_item_coverage": {
                "coverage_version": "accepted-items-v0.1",
                "checker_version": "beta-semantic-contract-v1",
                "human_disposition_artifact_id": disp["artifact_id"],
                "human_disposition_content_hash": disp["content_hash"],
                "items": [{"item_id": disp["artifact_id"] + ":0", "item_index": 0,
                           "required": True, "status": "COVERED",
                           "response_evidence": "配置先はTokyoです。", "notes": "saved receipt"}]
            }
        }
        with tempfile.TemporaryDirectory() as tmp:
            primary = copy.deepcopy(base)
            reviewer = copy.deepcopy(base)
            reviewer["provenance"]["checker_id"] = "beta-runtime-reviewer"
            p, r = Path(tmp) / "primary.json", Path(tmp) / "reviewer.json"
            write_json(p, primary); write_json(r, reviewer)
            result = run_saved_pair(self.manager, run,
                                    {"adapter": p}, {"adapter": r}, FIXTURE["contract"])
        self.assertEqual(result["binding"]["result"], "PASS")
        self.assertEqual(result["semantic"]["result"], "ALIGNED")
        self.assertEqual(result["release"]["decision"], "RELEASE")
