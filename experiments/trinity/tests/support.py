import copy
import tempfile
import unittest
from controller.run_manager import RunManager
from controller.artifact_store import digest, write_json
from fixtures.support import TASK, CONTRACT, FixtureValidator, prepared

class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.manager = RunManager(self.temp.name)
    def ready(self, text="The required deployment region is Tokyo."):
        return prepared(self.manager, text)
    def inject(self, run, **changes):
        m = self.manager.load(run)
        m.update(changes)
        self.manager._event(m, "OPERATOR_INTERVENTION_RECORDED", metadata={"test_fault_injection": True})
    def reseal_candidate(self, run, **changes):
        m = self.manager.load(run)
        original = self.manager.store.get(m["final_candidate_artifact_id"])
        args = dict(kind=original["artifact_type"], run_id=run, content=original["content"],
                    seq=m["event_seq"] + 1, sources=original["source_artifact_ids"],
                    task_package_hash=original["task_package_hash"], producer_id=original["producer_id"])
        args.update(changes)
        record = self.manager.store.seal(**args)
        self.inject(run, final_candidate_artifact_id=record["artifact_id"])
        return record
