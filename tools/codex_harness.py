#!/usr/bin/env python3
"""Local Codex support: exact-source retrieval, durable context, evidence, evals.

Python standard library only. Never calls a model, network, or external service.
Runtime files are deliberately excluded from Git. Commands are explicit argv,
never read from retrieved documents and never passed through a shell.
"""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import gzip
import json
import math
import os
from pathlib import Path
import re
import statistics
import subprocess
import sys
import tempfile
import time
import uuid
import zlib


class HarnessError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise HarnessError(message)


def stamp():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.pending-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            raw = encoded(value)
            stream.write(gzip.compress(raw, mtime=0) if path.suffix == '.gz' else raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def identifier(value):
    require(isinstance(value, str) and re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}', value), 'Invalid identifier')
    return value


def within(root, relative):
    require(isinstance(relative, str) and relative and not Path(relative).is_absolute(), 'Use a relative path')
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), 'Path escapes repository')
    require('.git' not in path.relative_to(root.resolve()).parts, 'Git internals are excluded')
    return path


def runtime(root):
    return within(root, '.harness-runtime')


@contextmanager
def locked(directory):
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory / '.lock'
    try:
        lock.mkdir()
    except FileExistsError:
        raise HarnessError(f'Concurrent update or interrupted writer: {lock}; inspect before removing lock')
    try:
        yield
    finally:
        lock.rmdir()


def git_files(root):
    proc = subprocess.run(['git', 'ls-files', '-z', '--', '*.md'], cwd=root, capture_output=True, check=True)
    return sorted(p for p in proc.stdout.decode('utf-8').split('\0') if p)


def build_index(root):
    """Always hash current tracked files; only parse changed files. No stale mtime cache."""
    target = runtime(root) / 'index.json.gz'
    with locked(runtime(root) / 'index-lock'):
        recovered = False
        try:
            cached = json.loads(gzip.decompress(target.read_bytes())) if target.exists() else {'files': {}}
            require(cached.get('schema', 1) == 1 and isinstance(cached.get('files'), dict), 'Invalid index')
            old = cached['files']
            require(all(isinstance(v, dict) and isinstance(v.get('lines'), list)
                        and all(isinstance(line, str) for line in v['lines'])
                        and isinstance(v.get('sha256'), str) for v in old.values()), 'Invalid index entries')
        except (ValueError, EOFError, gzip.BadGzipFile, zlib.error, AttributeError):
            old, recovered = {}, True
        files, parsed = {}, 0
        for name in git_files(root):
            path = within(root, name)
            if not path.is_file():
                continue
            raw = path.read_bytes()
            sha = digest(raw)
            if old.get(name, {}).get('sha256') == sha:
                files[name] = old[name]
                continue
            lines = raw.decode('utf-8-sig').splitlines()
            files[name] = {'sha256': sha, 'bytes': len(raw), 'lines': lines,
                           'headings': [{'line': i + 1, 'text': line} for i, line in enumerate(lines) if re.match(r'^#{1,6} ', line)]}
            parsed += 1
        value = {'schema': 1, 'files': files}
        if recovered or not target.exists() or old != files:
            atomic_json(target, value)
    return value, {'files': len(files), 'parsed': parsed, 'reused': len(files) - parsed, 'recovered_cache': recovered}


def search(root, query, limit=8, offset=0):
    terms = query.casefold().split()
    require(terms and 1 <= limit <= 50 and offset >= 0, 'Invalid query or pagination')
    index, stats = build_index(root)
    hits = []
    for path, item in index['files'].items():
        matches = [(n + 1, line) for n, line in enumerate(item['lines']) if any(t in line.casefold() for t in terms)]
        path_hits = sum(t in path.casefold() for t in terms)
        if matches or path_hits:
            score = path_hits * 10 + sum(any(t in l.casefold() for _, l in matches) for t in terms)
            hits.append({'path': path, 'sha256': item['sha256'], 'score': score,
                         'matched_lines': len(matches), 'locations': [n for n, _ in matches[:5]],
                         'preview': matches[0][1][:240] if matches else path,
                         'preview_only': True})
    hits.sort(key=lambda x: (-x['score'], x['path']))
    end = offset + limit
    return {'query': query, 'matches': len(hits), 'hits': hits[offset:end],
            'next_offset': end if end < len(hits) else None, 'index': stats,
            'scope': 'tracked Markdown only; keyword matching, not semantic completeness',
            'next': 'read exact source ranges; broaden terms/rg when needed; proposal text is not active policy'}


def source(root, name, start=1, count=120, expected=None):
    require(start >= 1 and 1 <= count <= 300, 'Invalid line range')
    path = within(root, name)
    require(path.is_file() and path.suffix.lower() == '.md', 'Source must be a Markdown file')
    raw = path.read_bytes()
    sha = digest(raw)
    require(expected is None or sha == expected, 'Source changed; refresh selection')
    lines = raw.decode('utf-8-sig').splitlines()
    require(start <= max(1, len(lines)), 'Start is beyond source')
    end = min(len(lines), start - 1 + count)
    return {'path': name, 'sha256': sha, 'start': start, 'end': end, 'total_lines': len(lines),
            'text': '\n'.join(lines[start - 1:end]), 'next_start': end + 1 if end < len(lines) else None,
            'scope': 'verbatim range, not the whole document; keep source status and authority'}


def validate_task(task):
    require(isinstance(task, dict), 'Task must be an object')
    for key in ('goal', 'next_step'):
        require(isinstance(task.get(key), str) and task[key].strip(), f'Missing {key}')
    for field in ('critical', 'decisions', 'required_checks', 'review_required'):
        require(isinstance(task.get(field), list), f'Missing list: {field}')
    require(task['critical'], 'At least one critical context item is required')
    seen = set()
    for item in task['critical']:
        require(isinstance(item, dict), 'Invalid critical item')
        identifier(item.get('id'))
        require(item['id'] not in seen, 'Duplicate critical ID')
        seen.add(item['id'])
        require(all(isinstance(item.get(k), str) and item[k].strip() for k in ('text', 'source')), 'Critical item needs exact text and source')
    for item in task['decisions']:
        require(isinstance(item, dict) and all(isinstance(item.get(k), str) and item[k].strip() for k in ('text', 'reason', 'source')), 'Decision needs text, reason, source')
    for name in task['required_checks']:
        identifier(name)
    require(len(task['required_checks']) == len(set(task['required_checks'])), 'Duplicate required checks')
    require(all(isinstance(x, str) and x.strip() for x in task['review_required']), 'Invalid review requirement')


def task_dir(root, task_id):
    return within(root, '.harness-runtime/tasks/' + identifier(task_id))


def load_task(root, task_id):
    directory = task_dir(root, task_id)
    files = sorted(directory.glob('revision-*.json'))
    require(files, f'No saved task: {task_id}')
    value = read_json(files[-1])
    require(value['revision'] == len(files), 'Incomplete task history; inspect revisions')
    validate_task(value['task'])
    return value


def contract_hash(task):
    # Progress notes do not alter requirements. All other fields remain binding.
    return digest(encoded({key: value for key, value in task.items() if key != 'next_step'}))


def checkpoint(root, task_id, task, expected_revision, reason=''):
    validate_task(task)
    directory = task_dir(root, task_id)
    with locked(directory):
        files = sorted(directory.glob('revision-*.json'))
        previous = load_task(root, task_id) if files else None
        revision = previous['revision'] if previous else 0
        require(type(expected_revision) is int and expected_revision == revision, 'Stale revision; reload before updating')
        if previous:
            prior = {x['id']: x for x in previous['task']['critical']}
            current = {x['id']: x for x in task['critical']}
            changed = [key for key in prior if current.get(key) != prior[key]]
            require(not changed or reason.strip(), 'Critical context changed or removed; explicit correction reason is required')
        value = {'schema': 1, 'task_id': task_id, 'revision': revision + 1,
                 'recorded_at': stamp(), 'correction_reason': reason, 'task': task}
        atomic_json(directory / f'revision-{revision + 1:06d}.json', value)
    return {'task_id': task_id, 'revision': revision + 1, 'critical_count': len(task['critical']),
            'evidence': 'checks remain valid only if the task contract and watched inputs are unchanged'}


def watched(root, names):
    require(names, 'Explicit watch paths are required')
    result = {}
    for name in sorted(set(names)):
        path = within(root, name)
        require(path.exists(), f'Watch path missing: {name}')
        require(not path.is_relative_to(runtime(root)), 'Do not watch runtime output')
        candidates = sorted(path.rglob('*')) if path.is_dir() else [path]
        result['@' + name] = 'directory' if path.is_dir() else 'file'
        for child in candidates:
            rel = child.relative_to(root).as_posix()
            if set(child.relative_to(root).parts) & {'.git', '.harness-runtime', '__pycache__'}:
                continue
            child = within(root, rel)
            if child.is_file():
                result[rel] = digest(child.read_bytes())
    return result


def verify(root, task_id, check_id, command, watch, marker, timeout=120):
    identifier(check_id)
    with locked(task_dir(root, task_id) / ('verify-' + check_id)):
        return _verify(root, task_id, check_id, command, watch, marker, timeout)


def _verify(root, task_id, check_id, command, watch, marker, timeout=120):
    """Capture actual stdout, exit, watched inputs and running interpreter/platform."""
    identifier(check_id)
    require(command and all(isinstance(x, str) and x for x in command), 'Explicit command argv required')
    require(marker.strip() and timeout > 0, 'A success marker and positive timeout are required')
    task = load_task(root, task_id)
    require(check_id in task['task']['required_checks'], 'Check is not in the task contract')
    before = watched(root, watch)
    started = time.perf_counter()
    output = within(root, '.harness-runtime/evidence/' + uuid.uuid4().hex + '.log')
    output.parent.mkdir(parents=True, exist_ok=True)
    attempt = {'schema': 2, 'task_id': task_id, 'check_id': check_id,
               'task_revision': task['revision'], 'contract_sha256': contract_hash(task['task']),
               'status': 'RUNNING', 'recorded_at': stamp(), 'command': command,
               'watch': watch, 'inputs': before,
               'environment': {'python': sys.version, 'platform': sys.platform},
               'log': output.relative_to(root).as_posix(), 'log_sha256': None}
    # Invalidate the previous PASS before execution. If final persistence fails,
    # the latest attempt stays non-PASS rather than exposing an older success.
    with locked(task_dir(root, task_id)):
        atomic_json(task_dir(root, task_id) / ('check-' + check_id + '.json'), attempt)
    status, code = 'FAIL', None
    with output.open('wb') as stream:
        try:
            proc = subprocess.run(command, cwd=root, stdout=stream, stderr=subprocess.STDOUT,
                                  shell=False, timeout=timeout, check=False)
            code = proc.returncode
            status = 'PASS' if code == 0 else 'FAIL'
        except subprocess.TimeoutExpired:
            status = 'TIMEOUT'
        except OSError as error:
            stream.write(str(error).encode('utf-8'))
            status = 'BLOCKED'
    raw = output.read_bytes()
    marker_found = marker in raw.decode('utf-8', errors='replace')
    if status == 'PASS' and not marker_found:
        status = 'UNCONFIRMED'
    text = raw.decode('utf-8', errors='replace')
    unittest_count = re.search(r'Ran (\d+) tests? in ', text)
    skipped = re.search(r'OK \(skipped=(\d+)\)', text)
    if status == 'PASS' and (('no tests ran' in text) or
            (unittest_count and (int(unittest_count[1]) == 0 or
             (skipped and int(skipped[1]) == int(unittest_count[1]))))):
        status = 'UNCONFIRMED'
    try:
        after = watched(root, watch)
    except HarnessError:
        after = None
    if before != after:
        status = 'STALE'
    if contract_hash(load_task(root, task_id)['task']) != contract_hash(task['task']):
        status = 'STALE'
    evidence = {'schema': 2, 'task_id': task_id, 'task_revision': task['revision'], 'check_id': check_id,
                'contract_sha256': contract_hash(task['task']),
                'status': status, 'exit_code': code, 'command': command, 'marker': marker,
                'marker_found': marker_found, 'watch': watch, 'inputs': before,
                'environment': {'python': sys.version, 'platform': sys.platform},
                'elapsed_seconds': time.perf_counter() - started, 'recorded_at': stamp(),
                'log': output.relative_to(root).as_posix(), 'log_sha256': digest(raw)}
    # Latest completed run wins, but each immutable log and evidence record is retained.
    atomic_json(output.with_suffix('.json'), evidence)
    with locked(task_dir(root, task_id)):
        atomic_json(task_dir(root, task_id) / ('check-' + check_id + '.json'), evidence)
    return evidence


def gate(root, task_id):
    state = load_task(root, task_id)
    checks = []
    for name in state['task']['required_checks']:
        path = task_dir(root, task_id) / ('check-' + name + '.json')
        status = 'NOT_RUN'
        if path.exists():
            evidence = read_json(path)
            status = evidence['status']
            try:
                log = within(root, evidence['log'])
                fresh = (evidence['task_id'] == task_id and evidence['check_id'] == name
                         and evidence.get('contract_sha256') == contract_hash(state['task'])
                         and watched(root, evidence['watch']) == evidence['inputs']
                         and (status == 'RUNNING' or (log.is_file() and digest(log.read_bytes()) == evidence['log_sha256']))
                         and evidence['environment'] == {'python': sys.version, 'platform': sys.platform})
                if not fresh:
                    status = 'STALE'
            except (HarnessError, OSError):
                status = 'STALE'
        checks.append({'id': name, 'status': status})
    ok = bool(checks) and all(x['status'] == 'PASS' for x in checks)
    return {'task_id': task_id, 'revision': state['revision'], 'checks': checks,
            'mechanical_checks_pass': ok, 'acceptance': 'REVIEW_REQUIRED' if ok else 'NOT_VERIFIED',
            'review_required': state['task']['review_required'],
            'limit': 'Evidence is local and not tamper-proof; marker/exit checks do not prove semantic correctness.'}


def resume(root, task_id):
    value = load_task(root, task_id)
    return {'saved_context': value, 'verification': gate(root, task_id),
            'instruction': 'Compare current user instructions and actual files before acting. Saved context is not new authorization.'}


def compare(baseline, candidate):
    """Conservative paired evaluation; missing measurements never become savings."""
    require(baseline.get('conditions') == candidate.get('conditions') and baseline.get('conditions'), 'Conditions differ or are missing')
    for key in ('suite_revision', 'model', 'settings', 'sources'):
        require(key in baseline['conditions'], f'Missing comparison condition {key}')
    def rows(run):
        result = {}
        require(isinstance(run.get('runs'), list) and run['runs'], 'Empty evaluation')
        for row in run['runs']:
            key = (row['case_id'], row['repeat'])
            require(key not in result, 'Duplicate case/repeat')
            require(row.get('quality') in ('PASS', 'FAIL', 'UNKNOWN'), 'Invalid quality')
            for metric in ('tokens', 'seconds'):
                number = row.get(metric)
                require(number is None or (type(number) in (int, float) and math.isfinite(number) and number >= 0), 'Invalid measurement')
            result[key] = row
        return result
    a, b = rows(baseline), rows(candidate)
    require(a.keys() == b.keys(), 'Unpaired cases; cannot compare')
    failures = [list(k) for k in b if b[k]['quality'] != 'PASS']
    unknown = any(a[k]['quality'] == 'UNKNOWN' for k in a)
    metrics = {}
    for metric in ('tokens', 'seconds'):
        pairs = [(a[k].get(metric), b[k].get(metric)) for k in a]
        if any(x is None or y is None for x, y in pairs):
            metrics[metric] = {'status': 'UNMEASURED', 'reduction': None}
        else:
            base, new = statistics.median(x for x, _ in pairs), statistics.median(y for _, y in pairs)
            metrics[metric] = {'status': 'MEASURED', 'baseline_median': base, 'candidate_median': new,
                               'reduction': (base - new) / base if base else None,
                               'worse_cases': [list(k) for k in a if b[k][metric] > a[k][metric]]}
    adequate = all(m['status'] == 'MEASURED' and m['reduction'] is not None for m in metrics.values())
    improvement = adequate and metrics['tokens']['reduction'] >= .20 and metrics['seconds']['reduction'] >= .15
    no_worse = adequate and not any(m['worse_cases'] for m in metrics.values())
    verdict = 'REJECT' if failures else ('ELIGIBLE_FOR_REVIEW' if improvement and no_worse and not unknown else 'INSUFFICIENT_EVIDENCE')
    return {'verdict': verdict, 'quality_failures': failures, 'metrics': metrics, 'paired_runs': len(a),
            'case_results': [{'case_id': k[0], 'repeat': k[1], 'baseline': a[k], 'candidate': b[k]} for k in sorted(a)],
            'limit': 'Input quality labels need independent evidence; this report never certifies future performance.'}


def audit_legacy(root):
    """Do not migrate historical PASS by number; expose both original meanings."""
    paths = ['evaluation/TEST_CASES.md', 'evaluation/RESULTS.md']
    suites = []
    for path in paths:
        raw = within(root, path).read_bytes()
        cases = {}
        for line in raw.decode('utf-8-sig').splitlines():
            match = re.match(r'^#{2,3}\s+(TEST-\d+)\s*(?:[:—–-])\s*(.*)', line)
            if match:
                require(match[1] not in cases, 'Duplicate legacy case heading')
                cases[match[1]] = match[2]
        suites.append({'path': path, 'sha256': digest(raw), 'cases': cases})
    left, right = [s['cases'] for s in suites]
    return {'suites': suites, 'mapping': [{'legacy_id': key, 'case_title': left.get(key),
             'result_title': right.get(key), 'status': 'UNMAPPED'} for key in sorted(left.keys() | right.keys())],
            'note': 'Different historical suites. No PASS transferred; semantic mapping needs review.'}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    command = []
    if '--' in argv:
        split = argv.index('--')
        command, argv = argv[split + 1:], argv[:split]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('search'); p.add_argument('query'); p.add_argument('--limit', type=int, default=8); p.add_argument('--offset', type=int, default=0)
    p = sub.add_parser('read'); p.add_argument('path'); p.add_argument('--start', type=int, default=1); p.add_argument('--count', type=int, default=120); p.add_argument('--sha256')
    p = sub.add_parser('checkpoint'); p.add_argument('task_id'); p.add_argument('input', type=Path); p.add_argument('--expected-revision', type=int, required=True); p.add_argument('--reason', default='')
    for action in ('resume', 'gate'):
        p = sub.add_parser(action); p.add_argument('task_id')
    p = sub.add_parser('verify'); p.add_argument('task_id'); p.add_argument('check_id'); p.add_argument('--watch', action='append', required=True); p.add_argument('--marker', required=True); p.add_argument('--timeout', type=float, default=120)
    p = sub.add_parser('compare'); p.add_argument('baseline', type=Path); p.add_argument('candidate', type=Path)
    sub.add_parser('audit-legacy')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.action == 'search': result = search(root, args.query, args.limit, args.offset)
        elif args.action == 'read': result = source(root, args.path, args.start, args.count, args.sha256)
        elif args.action == 'checkpoint': result = checkpoint(root, args.task_id, read_json(args.input), args.expected_revision, args.reason)
        elif args.action == 'resume': result = resume(root, args.task_id)
        elif args.action == 'gate': result = gate(root, args.task_id)
        elif args.action == 'verify':
            result = verify(root, args.task_id, args.check_id, command, args.watch, args.marker, args.timeout)
        elif args.action == 'audit-legacy': result = audit_legacy(root)
        else: result = compare(read_json(args.baseline), read_json(args.candidate))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.action == 'verify': return 0 if result['status'] == 'PASS' else 1
        if args.action == 'gate': return 0 if result['mechanical_checks_pass'] else 1
        if args.action == 'compare': return 0 if result['verdict'] == 'ELIGIBLE_FOR_REVIEW' else 1
        return 0
    except (HarnessError, OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(json.dumps({'error': str(error), 'status': 'NOT_VERIFIED'}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
