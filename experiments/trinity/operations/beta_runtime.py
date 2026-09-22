"""Minimal beta runtime bridge for saved, independently obtained validator receipts.

This module deliberately performs no model or network call.  Raw responses remain
immutable evidence; the existing semantic adapter is the only object supplied to
the TRINITY controller.
"""
import json
from pathlib import Path

from validation.local_review import LocalReviewValidator


class SavedResponseValidator(LocalReviewValidator):
    """Load one previously captured validator response without rewriting it."""

    def __init__(self, adapter_path, raw_path=None):
        self.adapter_path = str(Path(adapter_path))
        self.raw_path = str(Path(raw_path)) if raw_path else None
        super().__init__(adapter_path)


def run_saved_pair(manager, run_id, primary_adapter, reviewer_adapter, contract=None):
    """Execute the normal Binding -> Semantic -> Release path using saved receipts."""
    primary = SavedResponseValidator(primary_adapter["adapter"], primary_adapter.get("raw"))
    reviewer = SavedResponseValidator(reviewer_adapter["adapter"], reviewer_adapter.get("raw"))
    binding, semantic = manager.checks(run_id, validator=primary, reviewer=reviewer,
                                       contract=contract or {})
    release = manager.release(run_id)
    return {"binding": binding, "semantic": semantic, "release": release}


def load_receipt(path):
    """Read a runtime manifest as JSON, preserving its on-disk evidence."""
    return json.loads(Path(path).read_text(encoding="utf-8"))
