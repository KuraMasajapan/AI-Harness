"""Development-based Codex pilot: source contract, receipt bridge, bounded logs.

No model, network, hook, global setting, or TRINITY protocol changes. Source
guards apply only to this entry point; native Codex tools remain outside it.
"""
import argparse
import codecs
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

import codex_harness as h


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args]).decode('utf-8').strip()


def capture(root, contract):
    """Snapshot declared sources, not a claim they were read or understood."""
    for key in ('repository', 'branch', 'base_commit', 'sources'):
        h.require(contract.get(key), 'Missing source contract: ' + key)
    h.require(git(root, 'remote', 'get-url', 'origin') == contract['repository'], 'SOURCE_MISMATCH: repository')
    h.require(git(root, 'branch', '--show-current') == contract['branch'], 'SOURCE_MISMATCH: branch')
    h.require(len(contract['base_commit']) == 40 and all(c in '0123456789abcdef' for c in contract['base_commit']),
              'Use a pinned full base commit')
    proc = subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', contract['base_commit'], 'HEAD'], capture_output=True)
    h.require(proc.returncode == 0, 'SOURCE_MISMATCH: development base is not an ancestor')
    entries = []
    seen = set()
    for item in contract['sources']:
        name = item['path']
        h.require(name not in seen, 'Duplicate source path')
        seen.add(name)
        h.require(item.get('authority') in {'ACTIVE', 'PROPOSAL', 'REFERENCE', 'HISTORICAL'},
                  'Explicit source authority required')
        p = h.within(root, name)
        h.require(not p.is_relative_to(h.runtime(root)), 'Source cannot be runtime output')
        h.require(p.is_file(), 'SOURCE_UNAVAILABLE: ' + name)
        data = p.read_bytes()
        entries.append(dict(path=name, authority=item['authority'], sha256=h.digest(data), bytes=len(data),
                            read_status='NOT_ATTESTED'))
    external = []
    for item in contract.get('external_sources', []):
        p = Path(item['path'])
        h.require(p.is_absolute() and p.is_file(), 'Explicit external source unavailable')
        sha = h.digest(p.read_bytes())
        h.require(sha == item['sha256'], 'EXTERNAL_SOURCE_STALE: ' + str(p))
        external.append(dict(path=str(p), sha256=sha, authority='REFERENCE', read_status='NOT_ATTESTED'))
    return dict(repository=contract['repository'], branch=contract['branch'], base_commit=contract['base_commit'],
                head=git(root, 'rev-parse', 'HEAD'), sources=entries, external_sources=external,
                limitation='Hashes establish byte identity, not reading, authority approval, or comprehension.')


def activate(root, task_id, contract):
    h.load_task(root, task_id)
    snapshot = capture(root, contract)
    record = dict(schema=1, task_id=task_id, recorded_at=h.stamp(), contract=contract, snapshot=snapshot)
    record['record_hash'] = h.digest(h.encoded(record))
    path = h.task_dir(root, task_id) / 'activations' / (uuid.uuid4().hex + '.json')
    h.atomic_json(path, record)
    return dict(activation=path.relative_to(root).as_posix(), record_hash=record['record_hash'], snapshot=snapshot)


def source_guard(root, task_id, activation):
    p = h.within(root, activation)
    h.require(p.parent == h.task_dir(root, task_id) / 'activations', 'Activation belongs to another task')
    record = h.read_json(p)
    supplied = record.pop('record_hash')
    h.require(supplied == h.digest(h.encoded(record)), 'Activation record corrupt')
    h.require(record['task_id'] == task_id, 'Activation task mismatch')
    h.require(capture(root, record['contract']) == record['snapshot'], 'SOURCE_STALE: activate current sources again')
    return dict(**record, record_hash=supplied)


def preview(root, name, offset=0, count=2000, expected=None, stream=False):
    """Bound each page even for giant single-line output; always retain raw bytes."""
    h.require(type(offset) is int and offset >= 0 and 1 <= count <= 6000, 'Invalid output range')
    p = h.within(root, name)
    h.require(p.is_file(), 'Output unavailable')
    # Streaming reduced memory but did not consistently improve speed in trials.
    # Preserve the previous default; streaming is an explicit experiment only.
    if not stream:
        raw = p.read_bytes()
        sha = h.digest(raw)
        h.require(expected is None or sha == expected, 'OUTPUT_STALE: restart from the current log version')
        text = raw.decode('utf-8', errors='replace')
        h.require(offset <= len(text), 'Offset beyond output')
        end = min(len(text), offset + count)
        return dict(path=name, sha256=sha, raw_bytes=len(raw), start=offset, end=end,
                    text=text[offset:end], next_offset=end if end < len(text) else None,
                    decoded_with_replacement='\ufffd' in text, tokens=None,
                    limitation='Verbatim decoded page; omitted content must be read as needed. Bytes are not tokens.')
    hasher = hashlib.sha256()
    decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
    total = raw_bytes = 0
    replacement = False
    pieces = []
    with p.open('rb') as stream:
        while True:
            chunk = stream.read(65536)
            hasher.update(chunk)
            raw_bytes += len(chunk)
            text = decoder.decode(chunk, final=not chunk)
            replacement = replacement or '\ufffd' in text
            start = max(0, offset - total)
            stop = min(len(text), offset + count - total)
            if start < stop:
                pieces.append(text[start:stop])
            total += len(text)
            if not chunk:
                break
    h.require(expected is None or hasher.hexdigest() == expected, 'OUTPUT_STALE: restart from the current log version')
    h.require(offset <= total, 'Offset beyond output')
    end = min(total, offset + count)
    return dict(path=name, sha256=hasher.hexdigest(), raw_bytes=raw_bytes, start=offset, end=end,
                text=''.join(pieces), next_offset=end if end < total else None,
                decoded_with_replacement=replacement, tokens=None,
                limitation='Verbatim decoded page; omitted content must be read as needed. Bytes are not tokens.')


def runtime_fingerprint(root, command):
    """Selected runtime inputs only; environment values are never stored in clear."""
    executable = command[0]
    p = Path(executable)
    if p.is_absolute() or p.parent != Path('.'):
        resolved = (root / p).resolve()
    else:
        located = shutil.which(executable)
        resolved = Path(located).resolve() if located else None
    executable_info = dict(path=str(resolved) if resolved else None,
                           sha256=h.digest(resolved.read_bytes()) if resolved and resolved.is_file() else None)
    tracked_env = ('PATH', 'PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV')
    return dict(executable=executable_info, python=sys.version, platform=sys.platform,
                interpreter=entry(sys.executable),
                adapter={p.name: h.digest(p.read_bytes()) for p in
                         (Path(__file__), Path(h.__file__), Path(__file__).with_name('codex_operations.py'),
                          Path(__file__).with_name('codex_evidence.py'))},
                environment={key: h.digest(os.environ[key].encode('utf-8')) if key in os.environ else None
                             for key in tracked_env})


def entry(path):
    p = Path(path).resolve()
    return dict(status='PRESENT', path=str(p), sha256=h.digest(p.read_bytes()))


def receipt(root, attempt_dir, task_id, check_id, phase, evidence):
    result = h.read_json(root / 'experiments/trinity/operations/receipt.template.json')
    result.update(evaluation_id=attempt_dir.name, test_id=check_id, phase=phase,
                  recorded_at=h.stamp(), expected_timing='BEFORE_EXECUTION' if phase == 'PRE_EXECUTION' else 'AFTER_EXECUTION',
                  functional_result='NOT_EXECUTED' if phase == 'PRE_EXECUTION' else evidence['status'])
    result['limitations'] = ['Local pilot record, not a sealed TRINITY artifact or authenticated Human approval.',
                             'Effective model, semantic correctness, and general performance are not certified.']
    for key in result['evidence']:
        result['evidence'][key] = dict(status='UNRESOLVED', reason='Not established by this local mechanical check')
    result['evidence']['fixture_identity'] = entry(attempt_dir / 'invocation.json')
    result['evidence']['expected_oracle'] = entry(attempt_dir / 'oracle.json')
    result['evidence']['repository_snapshot'] = entry(attempt_dir / 'sources.json')
    result['evidence']['runtime_configuration'] = entry(attempt_dir / 'invocation.json')
    result['ordered_inputs'] = [entry(attempt_dir / 'task.json'), entry(attempt_dir / 'sources.json')]
    if phase == 'FINAL':
        execution = evidence['evidence']
        result['evidence']['pre_execution_receipt'] = entry(attempt_dir / 'pre.json')
        result['evidence']['execution_log'] = entry(root / execution['log'])
        result['evidence']['final_output'] = entry(root / execution['log'])
        result['evidence']['current_snapshot_relation'] = entry(attempt_dir / 'result.json')
    return result


def verify(root, task_id, check_id, activation, command, watch, marker, timeout=120):
    """Guard -> persist prerecords -> existing verifier -> final compatible receipt."""
    with h.locked(h.task_dir(root, task_id) / 'environment-verification'):
        sources = source_guard(root, task_id, activation)
        task = h.load_task(root, task_id)
        h.require(check_id in task['task']['required_checks'], 'Check is not required by this task')
        h.require(command and watch and marker.strip() and timeout > 0, 'Explicit verification contract required')
        folder = h.task_dir(root, task_id) / 'attempts' / uuid.uuid4().hex
        fingerprint = runtime_fingerprint(root, command)
        h.atomic_json(h.task_dir(root, task_id) / ('environment-' + check_id + '.json'),
                      dict(status='RUNNING', attempt=folder.relative_to(root).as_posix()))
        names = sorted(set(watch + [item['path'] for item in sources['snapshot']['sources']]))
        import codex_evidence as snapshots
        manifest = snapshots.archive(root, h.watched(root, names), sources['snapshot']['external_sources'])
        h.atomic_json(folder / 'inputs.json', manifest)
        h.atomic_json(folder / 'sources.json', dict(activation=sources, working_snapshot=entry(folder / 'inputs.json')))
        h.atomic_json(folder / 'task.json', task)
        h.atomic_json(folder / 'invocation.json', dict(command=command, watch=watch, timeout=timeout,
                                                      python=sys.version, platform=sys.platform,
                                                      runtime=fingerprint))
        h.atomic_json(folder / 'oracle.json', dict(marker=marker, exit_code=0,
            limitation='Marker and exit code are mechanical checks, not semantic acceptance'))
        h.atomic_json(folder / 'pre.json', receipt(root, folder, task_id, check_id, 'PRE_EXECUTION', None))
        evidence = h.verify(root, task_id, check_id, command, names, marker, timeout)
        try:
            source_guard(root, task_id, activation)
            source_state = 'CURRENT'
        except (h.HarnessError, OSError, subprocess.CalledProcessError):
            source_state = 'STALE'
        status = evidence['status'] if source_state == 'CURRENT' else 'STALE'
        if evidence['contract_sha256'] != h.contract_hash(task['task']):
            status = 'STALE'
        if evidence['inputs'] != manifest['inputs']:
            status = 'STALE'
        if runtime_fingerprint(root, command) != fingerprint:
            status = 'STALE'
        result = dict(status=status, source_state=source_state, activation=activation,
                      activation_hash=sources['record_hash'], evidence=evidence,
                      runtime=fingerprint, attempt=folder.relative_to(root).as_posix())
        h.atomic_json(folder / 'result.json', result)
        h.atomic_json(folder / 'final.json', receipt(root, folder, task_id, check_id, 'FINAL', result))
        h.atomic_json(h.task_dir(root, task_id) / ('environment-' + check_id + '.json'), result)
        page = preview(root, evidence['log'], expected=evidence['log_sha256'])
        import codex_operations as operations
        observation = operations.observe_view(root, task_id, page)
        return dict(status=status, attempt=result['attempt'], receipt=(folder / 'final.json').relative_to(root).as_posix(),
                    output=page, observation=observation, acceptance='REVIEW_REQUIRED')


def gate(root, task_id):
    result = h.gate(root, task_id)
    for check in result['checks']:
        p = h.task_dir(root, task_id) / ('environment-' + check['id'] + '.json')
        try:
            record = h.read_json(p)
            source_guard(root, task_id, record['activation'])
            folder = h.within(root, record['attempt'])
            h.require(h.read_json(folder / 'result.json') == record, 'Result record mismatch')
            current = h.read_json(h.task_dir(root, task_id) / ('check-' + check['id'] + '.json'))
            h.require(current == record['evidence'], 'Another verification superseded this attempt')
            h.require(runtime_fingerprint(root, current['command']) == record['runtime'], 'Runtime changed')
            import codex_evidence as snapshots
            manifest = snapshots.validate(root, folder / 'inputs.json')
            h.require(manifest['inputs'] == current['inputs'], 'Snapshot does not match executed inputs')
            final = h.read_json(folder / 'final.json')
            template = h.read_json(root / 'experiments/trinity/operations/receipt.template.json')
            h.require(set(final['evidence']) == set(template['evidence']), 'Incomplete receipt evidence fields')
            for item in list(final['evidence'].values()) + final['ordered_inputs']:
                if item['status'] == 'PRESENT':
                    h.require(h.digest(Path(item['path']).read_bytes()) == item['sha256'], 'Receipt evidence changed')
            if record['status'] != 'PASS' and check['status'] != 'STALE':
                check['status'] = record['status']
        except (KeyError, ValueError, OSError, subprocess.CalledProcessError) as exc:
            check['status'] = 'NOT_CURRENT'
            check['reason'] = str(exc)
    result['mechanical_checks_pass'] = bool(result['checks']) and all(c['status'] == 'PASS' for c in result['checks'])
    result['acceptance'] = 'REVIEW_REQUIRED' if result['mechanical_checks_pass'] else 'NOT_VERIFIED'
    return result


def check_receipt(root, path, validator_root=None):
    """Reuse the unchanged development checker with an explicit optional dependency."""
    env = os.environ.copy()
    if validator_root is None:
        return dict(status='UNAVAILABLE', reason='development does not supply protocol.schema_validation; pass an explicit trusted validator root')
    validator_root = Path(validator_root).resolve()
    validator = validator_root / 'protocol/schema_validation.py'
    h.require(validator.is_file(), 'Explicit validator dependency unavailable')
    env['PYTHONPATH'] = str(validator_root)
    checker = root / 'experiments/trinity/operations/check_receipt.py'
    proc = subprocess.run([sys.executable, '-B', str(checker), str(Path(path).resolve())],
                          cwd=root, env=env, capture_output=True, text=True, encoding='utf-8')
    return dict(status='OK' if proc.returncode == 0 else 'ERROR', exit_code=proc.returncode,
                checker=entry(checker), validator=entry(validator), stdout=proc.stdout, stderr=proc.stderr,
                limitation='Trusted local dependency; hash/structure only. No protocol or Human approval authority.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('begin'); p.add_argument('task'); p.add_argument('--contract', type=Path); p.add_argument('--refresh', action='store_true')
    p = sub.add_parser('operation'); p.add_argument('task')
    p = sub.add_parser('finish'); p.add_argument('task')
    p = sub.add_parser('report'); p.add_argument('task')
    p.add_argument('--offset', type=int, default=0); p.add_argument('--limit', type=int, default=20); p.add_argument('--sha256')
    p = sub.add_parser('snapshot'); p.add_argument('task'); p.add_argument('attempt')
    p.add_argument('--offset', type=int, default=0); p.add_argument('--limit', type=int, default=20); p.add_argument('--sha256')
    p = sub.add_parser('snapshot-file'); p.add_argument('task'); p.add_argument('attempt'); p.add_argument('path')
    p.add_argument('--offset', type=int, default=0); p.add_argument('--count', type=int, default=2000)
    p.add_argument('--sha256')
    p = sub.add_parser('activate'); p.add_argument('task'); p.add_argument('contract', type=Path)
    p = sub.add_parser('resume'); p.add_argument('task')
    p = sub.add_parser('gate'); p.add_argument('task')
    p = sub.add_parser('output'); p.add_argument('path'); p.add_argument('--offset', type=int, default=0); p.add_argument('--count', type=int, default=2000)
    p.add_argument('--sha256'); p.add_argument('--task')
    p.add_argument('--stream', action='store_true')
    p = sub.add_parser('receipt'); p.add_argument('path', type=Path); p.add_argument('--validator-root', type=Path)
    p = sub.add_parser('verify'); p.add_argument('task'); p.add_argument('check'); p.add_argument('--activation', required=True)
    p.add_argument('--watch', action='append', required=True); p.add_argument('--marker', required=True); p.add_argument('--timeout', type=float, default=120)
    argv = list(sys.argv[1:] if argv is None else argv)
    command = []
    if '--' in argv:
        i = argv.index('--'); command, argv = argv[i+1:], argv[:i]
    args = parser.parse_args(argv); root = args.root.resolve()
    try:
        import codex_operations as operations
        if args.action == 'begin': result = operations.begin(root, args.task, h.read_json(args.contract) if args.contract else None, args.refresh)
        elif args.action == 'operation': result = operations.operation(root, args.task)
        elif args.action == 'finish': result = operations.finish(root, args.task)
        elif args.action == 'report': result = operations.report(root, args.task, args.offset, args.limit, args.sha256)
        elif args.action == 'snapshot':
            import codex_evidence as snapshots
            result = snapshots.listing(root, args.task, args.attempt, args.offset, args.limit, args.sha256)
        elif args.action == 'snapshot-file':
            import codex_evidence as snapshots
            result = snapshots.read_file(root, args.task, args.attempt, args.path, args.offset, args.count, args.sha256)
            result['observation'] = operations.observe_view(root, args.task, result)
        elif args.action == 'activate': result = activate(root, args.task, h.read_json(args.contract))
        elif args.action == 'verify': result = verify(root, args.task, args.check, args.activation, command, args.watch, args.marker, args.timeout)
        elif args.action == 'gate': result = gate(root, args.task)
        elif args.action == 'resume': result = dict(saved_context=h.load_task(root, args.task), verification=gate(root, args.task), instruction='Reconcile current user correction and source contract; TRINITY is optional support, not the main objective.')
        elif args.action == 'receipt': result = check_receipt(root, args.path, args.validator_root)
        else:
            result = preview(root, args.path, args.offset, args.count, args.sha256, args.stream)
            if args.task:
                result['observation'] = operations.observe_view(root, args.task, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.action == 'verify': return 0 if result['status'] == 'PASS' else 1
        if args.action in {'gate','resume'}:
            state = result.get('verification', result)
            return 0 if state['mechanical_checks_pass'] else 1
        if args.action == 'receipt': return 0 if result['status'] == 'OK' else 1
        return 0
    except (h.HarnessError, OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(json.dumps(dict(status='NOT_VERIFIED', error=str(exc)), ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
