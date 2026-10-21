"""Offline tests: no network, no publishing."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_sources import analyze, markdown

BASE = "projects/GROWgle/"
def record(path, sha, scope, state):
    return {"path": BASE+path, "blob_sha":sha, "scope":scope,
            "document_status":state, "prototype_record_ids":[]}
def tree(rows, truncated=False):
    return {"truncated":truncated,
            "tree":[{"type":"blob", "path":BASE+p, "sha":s} for p,s in rows]}

class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.m = {"snapshot_date":"2026-10-20", "files":[
            record("CROSS_CATEGORY/OKAYAMA.md", "aaa", "OKAYAMA_PILOT", "PARTIAL_PROTOTYPE"),
            record("KURASHIKI/RESEARCH.md", "bbb", "OKAYAMA_PILOT", "UNASSESSED"),
            record("RESEARCH_RULES.md", "ccc", "REFERENCE_OR_POLICY", "REFERENCE_ONLY"),
            record("HIROSHIMA/RESEARCH.md", "ddd", "FUTURE_REGION", "OUT_OF_CURRENT_PILOT")]}
    def test_unchanged_backlog_not_completed(self):
        items=[(x["path"][len(BASE):], x["blob_sha"]) for x in self.m["files"]]
        r=analyze(self.m, tree(items))
        self.assertEqual(len(r["changes"]), 0)
        self.assertEqual(len(r["pending"]), 2)
        self.assertIn("一部実装", markdown(r, "main"))
    def test_new_updated_removed_and_excluded_tracking_file(self):
        rows=[("CROSS_CATEGORY/OKAYAMA.md","changed"), ("KURASHIKI/RESEARCH.md","bbb"),
              ("RESEARCH_RULES.md","ccc"), ("EXTRA.md","zzz"),
              ("OSAKA/EXTRA.md","yyy"),
              ("implementation_tracking/STATUS_BOARD.md","sss")]
        r=analyze(self.m, tree(rows))
        kinds={x["path"][len(BASE):]:x["change"] for x in r["changes"]}
        self.assertEqual(kinds, {"CROSS_CATEGORY/OKAYAMA.md":"UPDATED",
                                  "HIROSHIMA/RESEARCH.md":"REMOVED_OR_MOVED",
                                  "EXTRA.md":"NEW", "OSAKA/EXTRA.md":"NEW"})
        other=[x for x in r["changes"] if x["path"].endswith("OSAKA/EXTRA.md")][0]
        self.assertEqual(other["scope"], "FUTURE_REGION")
        self.assertEqual(len(r["pending"]), 1)
    def test_refuse_truncated_and_empty(self):
        with self.assertRaises(ValueError):
            analyze(self.m, tree([], truncated=True))
        with self.assertRaises(ValueError):
            analyze(self.m, tree([]))
if __name__ == "__main__":
    unittest.main()
