"""Explicit offline dashboard and curated Notion handoff. No network or model calls."""
import argparse
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import quote
import uuid

import codex_harness as h
import codex_operations as operations


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True,
                                   encoding='utf-8').strip()


def write_html(path, value):
    fd, name = tempfile.mkstemp(prefix='.pending-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as stream:
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def collect(root, task_id):
    """Read through the existing wrapper; never reinterpret stale checks as PASS."""
    saved = h.load_task(root, task_id)
    current = operations.operation(root, task_id, saved=saved)
    verification = current.get('verification', {})
    h.require(verification.get('revision', saved['revision']) == saved['revision'],
              'Checkpoint changed during collection; retry')
    return dict(schema=1, task_id=task_id, revision=saved['revision'],
                recorded_at=h.stamp(), branch=git(root, 'branch', '--show-current'),
                head=git(root, 'rev-parse', 'HEAD'),
                dirty=bool(git(root, 'status', '--porcelain')),
                operation=current.get('state', 'UNKNOWN'),
                freshness=current.get('freshness', 'UNKNOWN'),
                acceptance=verification.get('acceptance', 'NOT_VERIFIED'),
                checks=[dict(id=x['id'], status=x['status'], reason=x.get('reason', ''))
                        for x in verification.get('checks', [])],
                goal=saved['task']['goal'], next_step=saved['task']['next_step'],
                review_required=saved['task']['review_required'])


def resume_plan(root, task_id):
    """Compact read-only projection. Preserve saved constraints verbatim."""
    saved = h.load_task(root, task_id)
    current = operations.operation(root, task_id, saved=saved)
    verification = current.get('verification', {})
    h.require(verification.get('revision', saved['revision']) == saved['revision'],
              'Checkpoint changed during collection; retry')
    task = saved['task']
    checks = verification.get('checks', [])
    # A missing check or unrecognized status never yields RECONFIRM.
    expected = set(task['required_checks'])
    passing = (bool(expected) and len(checks) == len(expected)
               and {c['id'] for c in checks} == expected
               and all(c['status'] == 'PASS' for c in checks)
               and verification.get('mechanical_checks_pass') is True)
    if current.get('freshness') != 'CURRENT':
        action = 'RECONCILE'
    elif not passing:
        action = 'VERIFY_REQUIRED'
    else:
        action = 'RECONFIRM'
    return dict(task_id=task_id, revision=saved['revision'],
                operation=current['state'], freshness=current.get('freshness', 'UNKNOWN'),
                action=action, checks=checks, acceptance=verification.get('acceptance', 'NOT_VERIFIED'),
                goal=task['goal'], next_step=task['next_step'], critical=task['critical'],
                decisions=task['decisions'], review_required=task['review_required'],
                limitation='Read-only. Reconcile current user instructions; no new authorization or automatic verification.')


def differences(prior, current):
    keys = ('revision', 'branch', 'head', 'dirty', 'operation', 'freshness',
            'acceptance', 'checks', 'goal', 'next_step', 'review_required')
    return [key for key in keys if prior is None or prior.get(key) != current.get(key)]


def render(state, changed, history):
    esc = lambda x: escape(str(x), quote=True)
    rows = ''.join('<tr><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' %
                   tuple(esc(x.get(k, '')) for k in ('id', 'status', 'reason'))
                   for x in state['checks'])
    if not rows:
        rows = '<tr><td colspan="3">検証情報なし — 未確認</td></tr>'
    review = ''.join('<li>%s</li>' % esc(x) for x in state['review_required'])
    links = ''.join('<li><a href="%s">%s — 保存時の表示</a></li>' %
                    (quote(x['file'], safe='/.'), esc(x['recorded_at'])) for x in history)
    return '''<!doctype html><html lang="ja"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Codex 作業状況 — %(task)s</title><style>
:root{font-family:system-ui,sans-serif;color:#172b3a;background:#f3f5f7;line-height:1.65}
body{margin:0}main,header{max-width:64rem;margin:auto;padding:1.5rem}
header{padding-bottom:0}h1{font-size:1.8rem;margin:.3rem 0}h2{font-size:1.2rem}
section{background:white;padding:1.3rem;margin:1rem 0;border:1px solid #c5cfd8;border-radius:.6rem}
.notice{border-left:.4rem solid #986400;background:#fff6df;padding:1rem}
.meta{display:flex;flex-wrap:wrap;gap:.6rem 2rem}p,li,td,th{overflow-wrap:anywhere}
table{width:100%%;border-collapse:collapse;text-align:left}td,th{padding:.6rem;border-bottom:1px solid #c5cfd8}
.scroll{overflow-x:auto}a{color:#00579e;text-underline-offset:.2em}a:focus-visible{outline:3px solid #00579e;outline-offset:3px}
.skip{display:block;padding:.5rem 1.5rem}code{font-size:.85em}li{margin:.4rem 0}
@media(max-width:40rem){main,header{padding:1rem}section{padding:1rem}h1{font-size:1.5rem}}
</style><a class="skip" href="#main">本文へ移動</a>
<header><p>AI-Harness / ブランチ試験運用</p><h1>Codex 作業状況</h1>
<p>%(task)s · revision %(revision)s</p></header><main id="main">
<p class="notice"><strong>保存時点のスナップショットです。現在状態は再生成して確認してください。</strong><br>
自動更新・公開・承認は行いません。全項目PASSでも正式採用を意味しません。</p>
<div class="meta"><p>生成: %(at)s</p><p>運用: %(operation)s / %(freshness)s</p>
<p>判定: <strong>%(acceptance)s</strong></p></div>
<section><h2>現在の目的</h2><p>%(goal)s</p><h2>次の作業</h2><p>%(next)s</p></section>
<section><h2>検証</h2><div class="scroll"><table><caption>生成時に既存environment gateで照合した結果</caption>
<thead><tr><th scope="col">項目</th><th scope="col">状態</th><th scope="col">理由</th></tr></thead><tbody>%(rows)s</tbody></table></div></section>
<section><h2>Humanの確認・未解決事項</h2><ul>%(review)s</ul></section>
<section><h2>前回表示からの変化</h2><p>%(changed)s</p><p>branch: %(branch)s<br>HEAD: <code>%(head)s</code><br>未commit変更あり: %(dirty)s</p>
<p><a href="state.json">今回表示の根拠JSON</a>（既存運用記録からの派生。原証跡は変更しません）</p>
<details><summary>保存済み表示の履歴</summary><ul>%(links)s</ul></details></section>
<p>実作業の品質・速度・token削減効果は未確認。表示生成はモデル呼出し0。</p></main></html>''' % dict(
        task=esc(state['task_id']), revision=state['revision'], at=esc(state['recorded_at']),
        operation=esc(state['operation']), freshness=esc(state['freshness']),
        acceptance=esc(state['acceptance']), goal=esc(state['goal']), next=esc(state['next_step']),
        rows=rows, review=review, changed=esc(', '.join(changed) or '変化なし'),
        branch=esc(state['branch']), head=esc(state['head']), dirty=esc(state['dirty']), links=links)


def dashboard(root, task_id):
    folder = h.within(root, '.harness-runtime/views/' + h.identifier(task_id))
    folder.mkdir(parents=True, exist_ok=True)
    with h.locked(folder / 'writer'):
        prior_path = folder / 'state.json'
        prior = h.read_json(prior_path) if prior_path.exists() else None
        state = collect(root, task_id)  # A failed collection never produces a fresh green view.
        changed = differences(prior, state)
        history = h.read_json(folder / 'history.json') if (folder / 'history.json').exists() else []
        snapshot_id = uuid.uuid4().hex
        entry = dict(file='snapshots/' + snapshot_id + '.html', recorded_at=state['recorded_at'])
        history = history + [entry]
        content = render(state, changed, history)
        snapshots = folder / 'snapshots'
        snapshots.mkdir(exist_ok=True)
        with (snapshots / (snapshot_id + '.json')).open('x', encoding='utf-8') as stream:
            json.dump(state, stream, ensure_ascii=False, indent=2)
        # Snapshot relative links must work from their own directory too.
        with (folder / entry['file']).open('x', encoding='utf-8') as stream:
            stream.write(content.replace('href="state.json"', 'href="' + snapshot_id + '.json"')
                         .replace('href="snapshots/', 'href="'))
        h.atomic_json(folder / 'state.json', state)
        h.atomic_json(folder / 'history.json', history)
        write_html(folder / 'index.html', content)  # Commit visible page last.
    return dict(output=str(folder / 'index.html'), snapshot=snapshot_id,
                changed=changed, acceptance=state['acceptance'], model_calls=0)


def compile_memory(root, packet_path, now=None):
    """Local review draft only. Explicit allowlist; never harvest runtime/chat logs."""
    packet = h.read_json(packet_path)
    h.require(isinstance(packet, dict) and packet.get('schema') == 1, 'Invalid memory packet')
    h.require(packet.get('sharing') == 'DRAFT_NOT_SENT', 'Only local draft packets supported')
    entries = packet.get('entries')
    h.require(isinstance(entries, list) and entries, 'Memory entries required')
    now = now or datetime.now(timezone.utc)
    seen = set()
    lines = ['# Notion共有メモリ — レビュー用下書き', '',
             'DRAFT_NOT_SENT / 派生文脈。外部送信・承認・自動同期は未実施。',
             '最新ユーザー指示と一次記録に照合し、矛盾・失効時には利用を止める。', '']
    for item in entries:
        h.require(isinstance(item, dict), 'Invalid memory entry')
        key = h.identifier(item.get('id'))
        h.require(key not in seen, 'Duplicate memory ID: ' + key)
        seen.add(key)
        h.require(item.get('classification') == 'SHARED_CANDIDATE', 'Private/unclassified memory rejected')
        h.require(type(item.get('revision')) is int and item['revision'] > 0, 'Invalid revision')
        h.require(item.get('status') in ('ACTIVE', 'SUPERSEDED', 'RETRACTED'), 'Invalid memory status')
        for field in ('text', 'project', 'source_path', 'source_sha256', 'expires_at'):
            h.require(isinstance(item.get(field), str) and item[field].strip(), 'Missing ' + field)
        source = item['source_path']
        h.require(source.startswith(('agents/Codex/', 'research/', 'incubator/proposals/'))
                  and source.endswith('.md'), 'Source is not an allowed shared Markdown reference')
        path = h.within(root, source)
        h.require('.harness-runtime' not in path.relative_to(root.resolve()).parts, 'Runtime sources rejected')
        h.require(h.digest(path.read_bytes()) == item['source_sha256'], 'Source changed: ' + key)
        expiry = datetime.fromisoformat(item['expires_at'].replace('Z', '+00:00'))
        h.require(expiry.tzinfo is not None and expiry > now, 'Expired or timezone missing: ' + key)
        # New IDs/revisions never imply that a conflicting old remote entry was removed.
        lines.extend(['## ' + key, '', item['text'], '',
                      '状態: %s / revision %s / project %s' % (item['status'], item['revision'], item['project']),
                      '期限: ' + item['expires_at'], '一次記録: ' + source,
                      'SHA-256: ' + item['source_sha256'], ''])
    return '\n'.join(lines)


def memory_draft(root, packet_path):
    text = compile_memory(root, packet_path)
    folder = h.within(root, '.harness-runtime/notion-drafts/' + uuid.uuid4().hex)
    folder.mkdir(parents=True)
    (folder / 'review.md').write_bytes(text.encode('utf-8'))
    h.atomic_json(folder / 'provenance.json', dict(packet_sha256=h.digest(packet_path.read_bytes()),
                  output_sha256=h.digest(text.encode('utf-8')), recorded_at=h.stamp(),
                  sharing='DRAFT_NOT_SENT', network_calls=0))
    return dict(output=str(folder / 'review.md'), sharing='DRAFT_NOT_SENT', network_calls=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('dashboard').add_argument('task')
    sub.add_parser('resume-plan').add_argument('task')
    sub.add_parser('memory-draft').add_argument('packet', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.command == 'dashboard':
            result = dashboard(root, args.task)
        elif args.command == 'resume-plan':
            result = resume_plan(root, args.task)
        else:
            result = memory_draft(root, args.packet.resolve())
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        parser.exit(1, 'NOT_UPDATED: ' + str(exc) + '\n')


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    main()
