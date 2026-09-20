"""Local immutable records. Trusted controller only; never expose this store to roles."""
import hashlib
import json
import re
import uuid
from pathlib import Path


class ProtocolError(ValueError):
    pass


def identifier():
    return str(uuid.uuid4())


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def write_json(path, value, exclusive=False):
    with Path(path).open("x" if exclusive else "w", encoding="utf-8", newline="\n") as stream:
        stream.write(canonical(value) + "\n")


class ArtifactStore:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, artifact_id):
        if not isinstance(artifact_id, str) or not re.fullmatch(r"[a-zA-Z0-9_-]+", artifact_id):
            raise ProtocolError("Invalid opaque identifier")
        return self.root / (artifact_id + ".json")

    def seal(self, kind, run_id, content, seq, sources=(), **metadata):
        if set(metadata) - {"task_package_hash", "producer_id"}:
            raise ProtocolError("Reserved artifact metadata cannot be overridden")
        record = dict(artifact_id=identifier(), artifact_type=kind, run_id=run_id,
                      content_hash=digest(content), created_event_seq=seq, sealed=True,
                      invalidated=False, source_artifact_ids=list(sources), content=content)
        record.update(metadata)
        record["record_hash"] = digest(record)
        from protocol.schema_validation import validate_named
        validate_named(record, "artifact")
        write_json(self.path(record["artifact_id"]), record, exclusive=True)
        return record

    def get(self, artifact_id):
        try:
            record = json.loads(self.path(artifact_id).read_text(encoding="utf-8"))
            from protocol.schema_validation import validate_named
            validate_named(record, "artifact")
            payload = {k: v for k, v in record.items() if k != "record_hash"}
            if (record["artifact_id"] != artifact_id or digest(payload) != record["record_hash"]
                    or digest(record["content"]) != record["content_hash"]
                    or not record["sealed"] or record["invalidated"]):
                raise ProtocolError("Artifact integrity failure")
            return record
        except ProtocolError as exc:
            raise ProtocolError("Artifact integrity failure: " + str(exc)) from exc
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ProtocolError("Missing or malformed artifact") from exc
