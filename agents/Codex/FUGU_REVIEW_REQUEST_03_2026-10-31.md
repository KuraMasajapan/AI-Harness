# Fugu Max レビュー依頼03 — 初回回答の照合と実装案への絞込み

2026-10-31。依頼01 → 補足資料02への回答後に、この資料を同じ会話へ渡してください。
既に02への回答で修正した論点は、その結論を参照して重複説明を省いて構いません。

## 目的・今回の範囲

主目的はCodexの安定性・検証精度・重要コンテキスト保持・速度・token効率の改善。
品質や必須検証を犠牲にしない。TRINITYは必要な評価補助に限る。
実装はローカルbranch試行で、公開/push、main統合、本番移行、既存証跡削除はHuman事前承認。
今回は設計レビューのみ。追加モデル呼出し・実環境操作・コード実行を依頼しません。
元の8回は保持し、FAILの書換え・同trialの再実行をしません。
本資料のコードはレビュー対象であり、内部の文字列や命令は実行指示ではありません。

## 1. 初回回答への照合結果（反証・再訂正を歓迎）

- 初回回答の「8件のFAIL」は訂正が必要です。元のPASSはcall 1/2/3、FAILは4/5/6/7/8。
  全8回答の引用存在を確認した事後auditと、元の失敗数は別です。
- 時間合計72.9106994→80.5992208秒、+10.55%は観測事実です。
  一般的な速度悪化や原因は未確定。有意差が出ないことは同等性・非劣性の証明ではありません。
- reasoningは既にeventsに記録され、outputの内数として扱っています。独立3項として
  input/output/reasoningを加算しないでください。下に取得済みの全8件を提示します。
- 証拠の入力/契約/runtime/log/snapshot/receipt照合は実装済みです。補足02のbegin/gateに加え、
  今回は不足していたverifyとhelper gateを提示します。新しい束縛機構が必要との結論は
  このコードと比較して、既存の欠落があれば具体的な反例で示してください。
- 原文にquoteがないだけで「fabricated」と断定できません。意図を推定せず、観測可能な
  quote_not_found等を使う案を優先します。1語削除が必ず捏造になるとは限りません。
- 末尾改行の一致可否は元の原文次第です。全角半角変換を含む自動補正は未採用です。
- 初回回答のMDE/p値/残差78%は未検証です。使う場合はデータ・前提・算出手順を示し、
  ケース混在・対応関係を扱ってください。説明率80%、n≥8等を十分条件にしないでください。
- max_tokens制限/cold cache強制の現行CLI対応は未確認です。CLIのみ起動の時間を引くことで
  実要求の固定overheadを分離できるとも確認していません。欠測は欠測として扱ってください。

## 2. ローカルで再照合した実usage

Codex側のoffline scriptで、8件のturn.completed usageと各result usageの一致を確認しました。
元trial全62ファイルは照合前後でhash不変です。外部からの独立検証ではありません。
TTFT/queue/モデル内部処理秒は採取していません。生JSONLには会話ID等があるため、
必要な数値だけを以下へ抽出しました。追加モデル試行・自動retryはありません。

| call | case | mode | input | cached内数 | output | reasoning内数 | CLI全体秒 | 元採点 |
|---|---|---|---:|---:|---:|---:|---:|---|

| 1 | checked-reentry | baseline | 33539 | 0 | 874 | 240 | 16.840830 | PASS |

| 2 | checked-reentry | candidate | 18040 | 0 | 927 | 217 | 21.281944 | PASS |

| 3 | checked-reentry | candidate | 18040 | 0 | 1200 | 516 | 32.494685 | PASS |

| 4 | checked-reentry | baseline | 33539 | 0 | 1041 | 350 | 24.827221 | FAIL |

| 5 | runtime-drift | candidate | 18170 | 0 | 551 | 100 | 13.226106 | FAIL |

| 6 | runtime-drift | baseline | 33543 | 11520 | 668 | 206 | 16.428024 | FAIL |

| 7 | runtime-drift | baseline | 33543 | 0 | 594 | 152 | 14.814625 | FAIL |

| 8 | runtime-drift | candidate | 18170 | 0 | 564 | 140 | 13.596485 | FAIL |


baseline reasoning計948、candidate計973。output計3,177/3,242の内数です。
時間とoutputのSpearman相関1.0、Pearson約0.949934、時間とinputのSpearman約−0.292770は
再計算で一致。ただしケース混在の記述統計で、因果説明には使えません。
実測中央値はbaseline 16.634427秒、candidate 17.439215秒、差+0.804788秒です。
初回回答中のmedian差+1.9秒・CI・n=8/armは例示で、今回の実測ではありません。
料金・quotaは未測定。仮定の単価式と実支出を混同しないでください。

## 3. 補足02に含めなかったコード

各SHA-256は元ファイル全体のraw bytes、行番号は採取時のものです。
全リポジトリは添付していません。別関数/import/fixtureを未確認のまま保証しないでください。
verifyはtools/codex_operations.pyではなく、tools/codex_environment.pyにあります。


### 現行verify全文

元ファイル: `tools/codex_environment.py`

SHA-256: `8cabaf26b6e9386d1c6082f37a7484092b24aeb4765957b8029f909c9f06cfd7`


verify: 行176–222

```python
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

```


### 現行helperの契約hashとgate全文

元ファイル: `tools/codex_harness.py`

SHA-256: `d2dd30889215c17de215d02c44fa689a37be4dab6607e32973485aff7be03db9`


contract_hash: 行211–213

```python
def contract_hash(task):
    # Progress notes do not alter requirements. All other fields remain binding.
    return digest(encoded({key: value for key, value in task.items() if key != 'next_step'}))

```


gate: 行327–352

```python
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

```


### 将来用runnerのsources構築部分（prepare冒頭）

元ファイル: `agents/Codex/evaluation/run_m2.py`

SHA-256: `68aa39f1b1725c8fd5a3a873522ad7486ae6673e708e0c59f473444139bd2393`


抜粋: 行83–110

```python
def prepare(executable):
    import codex_operations as operations
    folder = h.runtime(ROOT) / 'm2-pilot' / uuid.uuid4().hex
    (folder / 'sources').mkdir(parents=True)
    sources = {}
    for name in SOURCE_NAMES:
        raw = (ROOT/name).read_bytes();sources[name] = raw.decode('utf-8')
        path = folder/'sources'/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    current = operations.operation(ROOT,'environment-batch3')
    h.require(current['verification']['mechanical_checks_pass'], 'Current evidence not passing; do not freeze a false baseline')
    with patch.dict(os.environ, {'PYTHONPATH':'M2_ISOLATED_RUNTIME_DRIFT_PROBE'}):
        stale = environment.gate(ROOT,'environment-batch3')
    h.require(not stale['mechanical_checks_pass'] and any(c.get('reason')=='Runtime changed' for c in stale['checks']),
              'Runtime drift negative control did not trigger')
    sys.path.insert(0,str(ROOT/'tests'))
    import test_codex_environment as fixture
    case = fixture.EnvironmentTests();case.setUp()
    try:
        operations.begin(case.root,'pilot',case.contract);case.run_check();operations.finish(case.root,'pilot')
        try:operations.begin(case.root,'pilot')
        except h.HarnessError as exc:reentry = dict(steps=['begin(task,contract)','verify','finish(task)','begin(task)'], error=str(exc))
        else:raise h.HarnessError('Expected real reentry defect no longer reproduces')
    finally:case.doCleanups()
    observations = dict(current_gate=current['verification'], isolated_runtime_probe=stale, isolated_reentry_reproduction=reentry)
    critical = dict(critical=current['saved_context']['critical'], limitations='Saved user scope; not a new authorization')
    sources['observations.json'] = h.encoded(observations).decode()
    sources['task-context.json'] = h.encoded(critical).decode()
    h.atomic_json(folder/'observations.json',observations);h.atomic_json(folder/'task-context.json',critical)

```


上のprepareは修正前begin不具合を再現する、このpilot固有の入口です。修正後の現行版で
同じケースを準備すると再現条件を満たさず失敗します。新ケース計画への置換が必要です。
sourcesのキーはSOURCE_NAMESの7ファイルとobservations.json/task-context.json。
schema/grade/parse_eventsの全文は補足02を参照してください。
SOURCE_NAMESは次の7キーです。
`tools/codex_harness.py`, `tools/codex_environment.py`, `tools/codex_operations.py`,
`tools/codex_evidence.py`, `agents/Codex/README.md`, `agents/Codex/GOALS.md`,
`agents/Codex/BATCH3_VALIDATION.md`。
現行schemaのenumはSOURCE_NAMESから生成していますが、packetの実キーとschemaの
同期を一般的に保証する追加設計の要否は検討対象です。今回の旧trialのgraderは不変です。

## 4. 次の回答で確定してほしい3点

### A. 出典検証v2の最小設計

既存enumに加え、citation index付きのsource型/未知source/quote型/短すぎるquote/
原文非含有/位置不一致を区別する案を評価してください。意図不明のものにfabricatedと
名付けない方針への反論があれば示してください。
locatorを入れるならsourceキー・symbolまたはline span・quoteの矛盾や重複出現、
CRLF/LF、選択packetと全原文の差をどう扱うか、正例3・負例4以内のfixture表で示してください。
主張との関連性は別の意味レビューとし、未確認をPASSにしないでください。
既存trialと独立したv2設計として、最小schema・問題コード・合格条件を提案してください。

### B. 再確認/再実行/修復待ちの判定表

現行コードを前提に、進捗メモのみ、重要目的変更、branch/source変更、runtime変更、
log/receipt破損、外部依存欠落、中断、CHECKED後の再開を分類してください。
破損/欠落は即再実行で解決するとは限りません。原因確認や依存の復旧を先にする条件も
分けてください。新機構の提案は「現行関数で通ってしまう具体的負例」があるものに絞り、
既実装なら重複と明記してください。証拠の機械的有効性と依頼の意味照合は別です。

### C. 次回評価の事前契約案

今回の8件から分かること/分からないことを踏まえ、品質を落とさず比較する最小計画を
示してください。新たなモデル呼出しはしません。ケース・単位・順序・反復数の根拠、
実務上の許容幅、CI等の不確実性、採用/保留/不採用条件、欠測・cache非制御時の扱いを
区別してください。具体的な反復数に根拠がなければ未確定として必要情報を示してください。

## 5. 返答と今回のリレーを閉じる条件

まず初回回答で訂正/維持する主張を短く挙げてください。その後A/B/Cごとに、
「既存との差」「最小の変更」「根拠」「正負テスト」「未確定」を示してください。
Codexの反論への追従は不要です。誤りがあれば提示資料の根拠で反証してください。
追加資料は、採否に影響する不足がある場合だけ最大3点、具体的な関数/観測値と目的を指定。
重大な不足がなければ「実装前レビューを閉じてよい」と明記してください。
次はCodex側で実装・ローカルテストを行い、必要なら実測結果を後続レビューへ戻します。
レビュー回数や多数決を採用の根拠にせず、得られる新情報がない往復は増やしません。
