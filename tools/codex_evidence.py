"""Immutable, content-addressed copies of explicitly selected verification inputs.

Local evidence, not a cache. Never repairs, deletes, or restores existing data.
"""
import os
from pathlib import Path
import re
import tempfile

import codex_harness as h


def object_path(root, sha):
    h.require(isinstance(sha, str) and re.fullmatch('[0-9a-f]{64}', sha), 'Invalid object hash')
    return h.within(root, '.harness-runtime/objects/' + sha[:2] + '/' + sha)


def archive(root, inputs, external=()):
    external = {item['path']: item['sha256'] for item in external}
    with h.locked(h.runtime(root) / 'object-writer'):
        sources = [(h.within(root, name), sha) for name, sha in inputs.items()
                   if sha not in ('file', 'directory')]
        for name, sha in external.items():
            h.require(Path(name).is_absolute(), 'External snapshot requires an absolute path')
            sources.append((Path(name), sha))
        for source, sha in sources:
            target = object_path(root, sha)
            data = source.read_bytes()
            h.require(h.digest(data) == sha, 'Input changed before snapshot: ' + str(source))
            if target.exists():
                h.require(h.digest(target.read_bytes()) == sha, 'Existing evidence object corrupt; inspect without overwriting')
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, temporary = tempfile.mkstemp(prefix='.pending-', dir=target.parent)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(data); stream.flush(); os.fsync(stream.fileno())
                os.replace(temporary, target)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
    manifest = dict(schema=1, inputs=inputs, external_sources=external)
    manifest['manifest_hash'] = h.digest(h.encoded(manifest))
    return manifest


def validate(root, path):
    manifest = h.read_json(path)
    supplied = manifest.pop('manifest_hash')
    h.require(manifest['schema'] == 1 and supplied == h.digest(h.encoded(manifest)), 'Snapshot manifest corrupt')
    hashes = set()
    for name, sha in manifest['inputs'].items():
        h.within(root, name[1:] if sha in ('file', 'directory') else name)
        if sha not in ('file', 'directory'):
            hashes.add(sha)
    for name, sha in manifest['external_sources'].items():
        h.require(Path(name).is_absolute(), 'Invalid external snapshot path')
        hashes.add(sha)
    for sha in hashes:
        p = object_path(root, sha)
        h.require(p.is_file() and h.digest(p.read_bytes()) == sha, 'Snapshot object missing or corrupt')
    return dict(**manifest, manifest_hash=supplied)


def manifest_path(root, task_id, attempt_id):
    return h.task_dir(root, task_id) / 'attempts' / h.identifier(attempt_id) / 'inputs.json'


def listing(root, task_id, attempt_id, offset=0, limit=20, expected=None):
    h.require(type(offset) is int and offset >= 0 and type(limit) is int and 1 <= limit <= 100,
              'Invalid snapshot page')
    manifest = validate(root, manifest_path(root, task_id, attempt_id))
    h.require(expected is None or manifest['manifest_hash'] == expected, 'SNAPSHOT_STALE')
    rows = []
    for name, sha in manifest['inputs'].items():
        if sha not in ('file', 'directory'):
            rows.append(dict(source_type='WORKTREE', path=name, sha256=sha,
                             object_path=object_path(root, sha).relative_to(root).as_posix()))
    for name, sha in manifest['external_sources'].items():
        rows.append(dict(source_type='EXTERNAL_REFERENCE', path=name, sha256=sha,
                         object_path=object_path(root, sha).relative_to(root).as_posix()))
    rows.sort(key=lambda r: (r['source_type'], r['path']))
    h.require(offset <= len(rows), 'Snapshot offset beyond files')
    return dict(task_id=task_id, attempt=attempt_id, manifest_hash=manifest['manifest_hash'],
                files=rows[offset:offset+limit], file_count=len(rows),
                next_offset=offset+limit if offset+limit < len(rows) else None,
                limitation='Exact local bytes only; not semantic correctness or authenticated authority. No automatic restore.')


def read_file(root, task_id, attempt_id, name, offset=0, count=2000, expected=None):
    manifest = validate(root, manifest_path(root, task_id, attempt_id))
    h.require(expected is None or manifest['manifest_hash'] == expected, 'SNAPSHOT_STALE')
    sha = manifest['inputs'].get(name)
    h.require(sha not in (None, 'file', 'directory'), 'File not in working snapshot')
    import codex_environment as e
    page = e.preview(root, object_path(root, sha).relative_to(root).as_posix(), offset, count, sha)
    return dict(**page, original_path=name, manifest_hash=manifest['manifest_hash'])
