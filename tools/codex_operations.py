"""Local operation ledger and observed metrics. Never schedules or publishes."""
from datetime import datetime, timezone
import math
from pathlib import Path
import uuid

import codex_harness as h
import codex_environment as e


def latest(root, task_id):
    pointer = h.task_dir(root, task_id) / 'active-operation.json'
    if not pointer.exists():
        return None
    value = h.read_json(pointer)
    folder = h.task_dir(root, task_id) / 'operations' / h.identifier(value['operation_id'])
    events = sorted(folder.glob('event-*.json'))
    h.require(events, 'Operation pointer has no event')
    previous = None
    for number, p in enumerate(events, 1):
        record = h.read_json(p)
        supplied = record.pop('event_hash')
        h.require(record['sequence'] == number and record['previous_hash'] == previous
                  and record['task_id'] == task_id and record['operation_id'] == value['operation_id']
                  and supplied == h.digest(h.encoded(record)), 'Operation event history corrupt')
        previous = supplied
        if previous == value['event_hash']:
            break
    h.require(previous == value['event_hash'], 'Operation pointer/history mismatch')
    return dict(**record, event_hash=previous)


def append(root, task_id, operation_id, values, previous=None):
    record = dict(**values, task_id=task_id, operation_id=operation_id,
                  sequence=previous['sequence'] + 1 if previous else 1,
                  previous_hash=previous['event_hash'] if previous else None, recorded_at=h.stamp())
    record['event_hash'] = h.digest(h.encoded(record))
    folder = h.task_dir(root, task_id) / 'operations' / operation_id
    path = folder / ('event-%06d.json' % record['sequence'])
    h.require(not path.exists(), 'Operation event already exists')
    h.atomic_json(path, record)
    h.atomic_json(h.task_dir(root, task_id) / 'active-operation.json',
                  dict(operation_id=operation_id, event_hash=record['event_hash']))
    return record


def begin(root, task_id, contract=None, refresh=False):
    with h.locked(h.task_dir(root, task_id) / 'operation-writer'):
        saved = h.load_task(root, task_id)
        prior = latest(root, task_id)
        if prior and (contract is None or not refresh):
            try:
                active = h.read_json(h.within(root, prior['activation']))
                h.require(isinstance(active, dict) and isinstance(active.get('contract'), dict),
                          'Activation contract unavailable')
            except (OSError, ValueError) as exc:
                raise h.HarnessError('Activation record unreadable or malformed; supply an explicit --contract with --refresh') from exc
            contract = contract if contract is not None else active['contract']
            if not refresh:
                h.require(contract == active['contract'] and prior['task_contract'] == h.contract_hash(saved['task']),
                          'Operation contract changed; review current context and use begin --refresh')
                e.source_guard(root, task_id, prior['activation'])
                if prior['state'] == 'OPEN':
                    return operation(root, task_id, saved=saved, record=prior, reused=True)
        h.require(contract is not None, 'First begin requires an explicit --contract')
        activation = e.activate(root, task_id, contract)
        values = dict(state='OPEN', activation=activation['activation'], task_contract=h.contract_hash(saved['task']),
                      started_at=prior['started_at'] if prior and prior['state'] == 'OPEN' else h.stamp(),
                      event='REVALIDATED' if prior and prior['state'] == 'OPEN' else 'BEGAN')
        continuing = prior if prior and prior['state'] == 'OPEN' else None
        record = append(root, task_id, continuing['operation_id'] if continuing else uuid.uuid4().hex,
                        values, continuing)
        return operation(root, task_id, saved=saved, record=record)


def operation(root, task_id, saved=None, record=None, reused=False):
    saved = saved or h.load_task(root, task_id)
    record = record or latest(root, task_id)
    if record is None:
        return dict(task_id=task_id, state='NOT_STARTED', saved_context=saved['task'])
    try:
        e.source_guard(root, task_id, record['activation'])
        h.require(record['task_contract'] == h.contract_hash(saved['task']), 'Task contract changed')
        freshness = 'CURRENT'
    except (KeyError, ValueError, OSError):
        freshness = 'STALE'
    return dict(task_id=task_id, operation_id=record['operation_id'], state=record['state'],
                freshness=freshness, reused=reused, activation=record['activation'],
                started_at=record['started_at'], saved_context=saved['task'], verification=e.gate(root, task_id),
                limitation='Branch-local operation only; saved context is not new authorization or model comprehension.')


def finish(root, task_id):
    with h.locked(h.task_dir(root, task_id) / 'operation-writer'):
        prior = latest(root, task_id)
        h.require(prior and prior['state'] == 'OPEN', 'No open operation')
        current = operation(root, task_id, record=prior)
        h.require(current['freshness'] == 'CURRENT' and current['verification']['mechanical_checks_pass'],
                  'Cannot finish: source/task/check evidence is not current and passing')
        values = {k: prior[k] for k in ('activation', 'task_contract', 'started_at')}
        values.update(state='CHECKED', event='FINISHED', acceptance='REVIEW_REQUIRED')
        record = append(root, task_id, prior['operation_id'], values, prior)
        return dict(task_id=task_id, operation_id=record['operation_id'], state=record['state'],
                    acceptance='REVIEW_REQUIRED', report=report(root, task_id))


def observe_view(root, task_id, page):
    """Record actually returned text volume; no estimate of model tokens."""
    h.identifier(task_id)
    h.load_task(root, task_id)
    record = dict(recorded_at=h.stamp(), task_id=task_id, path=page['path'], sha256=page['sha256'],
                  start=page['start'], end=page['end'], raw_bytes=page['raw_bytes'],
                  displayed_text_bytes=len(page['text'].encode('utf-8')), tokens=None)
    path = h.task_dir(root, task_id) / 'views' / (uuid.uuid4().hex + '.json')
    try:
        h.atomic_json(path, record)
        return dict(status='RECORDED', path=path.relative_to(root).as_posix())
    except OSError as exc:
        return dict(status='UNAVAILABLE', reason=str(exc))


def report(root, task_id, offset=0, limit=20, expected=None):
    h.require(type(offset) is int and offset >= 0 and type(limit) is int and 1 <= limit <= 100,
              'Invalid report page')
    h.load_task(root, task_id)
    directory = h.task_dir(root, task_id)
    attempts = []
    complete = True
    for folder in sorted((directory / 'attempts').glob('*')):
        try:
            record = h.read_json(folder / 'result.json')
            final = folder / 'final.json'
            h.require(final.is_file(), 'Final receipt missing')
            evidence = record['evidence']
            elapsed = evidence['elapsed_seconds']
            h.require(isinstance(elapsed, (float, int)) and not isinstance(elapsed, bool)
                      and math.isfinite(elapsed) and elapsed >= 0, 'Invalid duration')
            log = h.within(root, evidence['log'])
            h.require(h.digest(log.read_bytes()) == evidence['log_sha256'], 'Log changed')
            attempts.append(dict(attempt=folder.name, check_id=evidence['check_id'], status=record['status'],
                                 seconds=elapsed, log_bytes=log.stat().st_size))
        except (ValueError, KeyError, OSError):
            complete = False
            attempts.append(dict(attempt=folder.name, status='INCOMPLETE'))
    attempts_complete = complete
    views = []
    for p in sorted((directory / 'views').glob('*.json')):
        try:
            value = h.read_json(p)
            h.require(value['task_id'] == task_id and type(value['displayed_text_bytes']) is int
                      and value['displayed_text_bytes'] >= 0, 'Invalid view record')
            views.append(value)
        except (ValueError, KeyError, OSError):
            complete = False
    observed_logs = {(v['path'], v['sha256']) for v in views}
    missing_views = 0
    for folder in sorted((directory / 'attempts').glob('*')):
        try:
            evidence = h.read_json(folder / 'result.json')['evidence']
            if (evidence['log'], evidence['log_sha256']) not in observed_logs:
                missing_views += 1
        except (ValueError, KeyError, OSError):
            pass
    views_complete = complete and missing_views == 0
    complete = complete and views_complete
    current = latest(root, task_id)
    report_hash = h.digest(h.encoded(dict(attempts=attempts, views=views)))
    h.require(expected is None or report_hash == expected, 'REPORT_STALE: restart from current observations')
    h.require(offset <= len(attempts), 'Report offset beyond attempts')
    elapsed = None
    if current:
        try:
            end = datetime.fromisoformat(current['recorded_at']) if current['state'] != 'OPEN' else datetime.now(timezone.utc)
            value = (end - datetime.fromisoformat(current['started_at'])).total_seconds()
            elapsed = value if value >= 0 and math.isfinite(value) else None
        except (ValueError, TypeError):
            complete = False
    return dict(task_id=task_id, metrics_status='OBSERVED' if complete else 'PARTIAL',
                attempts=attempts[offset:offset+limit], attempt_count=len(attempts),
                report_sha256=report_hash, next_offset=offset+limit if offset+limit < len(attempts) else None,
                ordering='attempt ID; totals cover all attempts, not only this page',
                verification_seconds=sum(a.get('seconds', 0) for a in attempts) if attempts_complete else None,
                log_bytes=sum(a.get('log_bytes', 0) for a in attempts) if attempts_complete else None,
                recorded_view_count=len(views), missing_view_observations=missing_views,
                displayed_text_bytes=sum(v['displayed_text_bytes'] for v in views) if views_complete else None,
                recorded_displayed_text_bytes=sum(v['displayed_text_bytes'] for v in views),
                observed_operation_seconds=elapsed, model_tokens=None, human_interventions=None,
                quality_regression='UNRESOLVED', adoption='BRANCH_TRIAL', verification=e.gate(root, task_id),
                limitations=['Observed operations only, not whole-chat time or model usage.',
                             'Display bytes exclude metadata and do not measure token savings.',
                             'Attempt counts are explicit rechecks, not inferred model retries.',
                             'Local records are not authenticated or tamper-proof.'])
