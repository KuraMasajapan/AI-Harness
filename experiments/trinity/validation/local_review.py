"""Adapter for an independently prepared local review JSON; no services or model calls."""
import json
from pathlib import Path
from controller.artifact_store import canonical, digest

def config_hash_receipt(review):
    """Expose the exact existing config hash preimage for offline auditors."""
    preimage = dict(adapter="local-review-v1", review_hash=digest(review))
    return dict(version="local-review-config-hash-v1",
                canonicalization="UTF-8 JSON; sort_keys=True; ensure_ascii=False; separators=(',', ':'); allow_nan=False; no trailing LF",
                review_hash=preimage["review_hash"], preimage=preimage,
                config_hash=digest(preimage))


class LocalReviewValidator:
    def __init__(self, path):
        self._review_json = canonical(json.loads(Path(path).read_text(encoding="utf-8")))
        review = json.loads(self._review_json)
        self.provenance = dict(review["provenance"])
        self.config_hash_receipt = config_hash_receipt(review)
        self.provenance["config_hash"] = self.config_hash_receipt["config_hash"]

    def evaluate(self, request):
        review = json.loads(self._review_json)
        task = json.loads(request.task_json)["content"]
        candidate = json.loads(request.candidate_json)
        if (review["task_package_hash"] != task["task_package_hash"]
                or review["candidate_artifact_id"] != candidate["artifact_id"]
                or review["candidate_content_hash"] != candidate["content_hash"]):
            raise ValueError("Local review belongs to a different task or candidate")
        return dict(requirements=review["requirements"], accepted_item_coverage=review["accepted_item_coverage"])
