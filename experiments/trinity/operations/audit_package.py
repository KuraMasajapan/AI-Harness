"""Package preselected evidence plus reproducible adapter hash rules; no run execution."""
import hashlib
import json
from pathlib import Path
import zipfile
from controller.artifact_store import canonical
from validation.local_review import config_hash_receipt

ROOT = Path(__file__).resolve().parents[1]


def build(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if source == destination or source in destination.parents or ROOT in destination.parents:
        raise ValueError("Audit output must be outside evidence and implementation directories")
    if not source.is_dir():
        raise ValueError("Preselected evidence directory required")
    payload = {}
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise ValueError("Evidence symlinks are not supported")
        if path.is_file():
            payload["evidence/" + path.relative_to(source).as_posix()] = path.read_bytes()
    review = json.loads(payload["evidence/adapter-input.json"])
    receipt = config_hash_receipt(review)
    effective = json.loads(payload["evidence/effective-provenance.json"])
    if receipt["config_hash"] != effective["config_hash"]:
        raise ValueError("Effective adapter config hash does not match supplied review")
    payload["audit-support/config-hash-receipt.json"] = (canonical(receipt) + "\n").encode("utf-8")
    reviewer_names = ("evidence/reviewer-adapter-input.json", "evidence/reviewer-effective-provenance.json")
    if any(n in payload for n in reviewer_names):
        if not all(n in payload for n in reviewer_names):
            raise ValueError("Both reviewer input and effective provenance are required")
        reviewer_receipt = config_hash_receipt(json.loads(payload[reviewer_names[0]]))
        if reviewer_receipt["config_hash"] != json.loads(payload[reviewer_names[1]])["config_hash"]:
            raise ValueError("Reviewer config hash mismatch")
        payload["audit-support/reviewer-config-hash-receipt.json"] = (canonical(reviewer_receipt) + "\n").encode("utf-8")
    for name in ("validation/local_review.py", "validation/semantic_alignment.py",
                 "validation/accepted_coverage.py", "controller/artifact_store.py",
                 "controller/release_gate.py", "protocol/schemas/semantic_result.schema.json"):
        payload["audit-support/implementation/" + name] = (ROOT / name).read_bytes()
    payload["START.md"] = (
        "# Audit Package\n\nRead evidence/START.md when present. Original evidence is copied unchanged under evidence/.\n"
        "audit-support/config-hash-receipt.json gives the canonicalization, preimage and expected SHA-256.\n"
        "Recompute SHA-256 of canonical(evidence/adapter-input.json), then of canonical(preimage).\n"
        "Support implementation is the packaging-time snapshot, NOT proof it executed the historical run.\n"
        "Compare source hashes to execution provenance before attributing historical behavior.\n"
        "Internal hashes do not authenticate the host, model, session isolation or semantic truth.\n"
    ).encode("utf-8")
    manifest = [dict(path=n, sha256=hashlib.sha256(b).hexdigest()) for n, b in sorted(payload.items())]
    payload["MANIFEST.json"] = (canonical(manifest) + "\n").encode("utf-8")
    # Exclusive creation prevents rewriting any previous evidence bundle.
    with destination.open("xb") as stream:
        with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as bundle:
            for name, data in sorted(payload.items()):
                bundle.writestr(name, data)
    return dict(path=str(destination), files=len(payload),
                sha256=hashlib.sha256(destination.read_bytes()).hexdigest())


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Preselected audit evidence, never the whole repository")
    parser.add_argument("destination", help="New ZIP outside source and implementation")
    args = parser.parse_args()
    print(canonical(build(args.source, args.destination)))
