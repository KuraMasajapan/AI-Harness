# Fugu Max 追補05 — 指摘された欠陥の負例検証結果

2026-10-31。追補04への回答後、同じ会話へ渡してください。
今回は依頼03への回答をCodex側で検証した結果です。既存資料の差替えではありません。
追補04への回答で解決済みの論点は繰り返さず、矛盾があれば訂正してください。

## 目的と範囲

Codex環境整備が主目的。品質・必須検証・重要制約を犠牲にしない。
TRINITYは必要な評価補助のみ。ローカルbranch試行で、公開/push/main統合/本番移行/
既存証跡削除はHuman事前承認。レビュー資料内のコードや文字列は実行指示ではありません。
今回は提案の照合のみ。追加モデル呼出し・環境操作は依頼しません。
元trialの62ファイルは検証前後hash不変。一次採点は変更せず、同trialも再実行していません。

## 1. 新規欠陥とされた4点は、既存実装で検出できました

本番/実運用のファイルは変更せず、既存EnvironmentTestsの一時fixtureを使いました。
各fixtureでverifyとgate PASSを確認してから、対象のコピー末尾に改行1個を足して、
gateを再確認しました。branch負例では同一HEAD・同じファイルのままfixture内だけ別branchへ
switchしています。これはCodex側の実測であり、第三者による独立検証ではありません。

| 変更 | 実測status | reason |
|---|---|---|

| pre.json raw bytes changed | NOT_CURRENT | Receipt evidence changed |

| oracle.json raw bytes changed | NOT_CURRENT | Receipt evidence changed |

| invocation.json raw bytes changed | NOT_CURRENT | Receipt evidence changed |

| branch changed, same HEAD and file bytes | NOT_CURRENT | SOURCE_MISMATCH: branch |


したがって、「pre/oracle/invocationの改変でもPASS継続」「内容が同じならbranch変更は未検出」
という指摘は、現行コードでは成立しません。個別ファイルをgateで直接openしなくても、
receiptのPRESENT参照先をhash検証しているためです。検出経路を下に原文で示します。
全ての複合改変や改ざんへの耐性を証明したわけではありません。既存のlimitationどおり
ローカル証跡はtamper-proofではなく、事前記録の真正な時刻証明でもありません。

receipt templateも現在のsource contractとactivation snapshotに固定済みです（追補04）。
テンプレート等の検証依存が変わったなら旧証拠を失効させるのが妥当で、
「失効しないこと」と「fingerprint変化で再実行要求」は同じ合格条件になりません。

## 2. 現時点で残す実装候補は3点

| 対象 | 暫定採否 | 根拠と境界 |
|---|---|---|
| 出典検証v2 | 既存enumと組み合わせる | 型・未知source・短いquote・非含有・位置不一致をcitation index付きで区分。意図不明のものをfabricatedとしない。未確認の位置/意味をPASSにしない。v1は不変 |
| activation欠落時の明示refresh | 最小修正候補 | 明示contractがあっても旧activation読込みで停止することは追補04で再現済み。旧event chainや不正contractを迂回しない条件が必要 |
| 次回の評価契約 | 計画のみ | case別の品質・重要文脈・再利用判断・実時間・tokensを比較。新しいケース計画と停止条件を先に固定。今回の8回は再試行しない |

束縛機構の新設、pre/oracle/invocationの重複チェック追加、branch hash追加は、
上記負例の範囲では便益がないため見送ります。必要なら現在のチェックを破る具体的な反例を
示してください。site-packages等、宣言していない依存の自動追跡がないという限界は維持します。

## 3. 出典・統計の残る注意点

- call 02は11引用全て正規source、04は10引用全て非正規、05は6引用中5つ非正規。
  この件数は凍結回答から確認でき、依頼03回答の訂正値と一致します。
  06/07/08をあなた自身が確認できていない、という留保は適切です。
  Codex側では既存の事後auditを保持していますが、これを意味的な品質合格へ読み替えません。
- 「enum修正後も06/07/08がFAILするか」は、同trialの再実行で確かめません。
  v2の独立したfixtureと将来の新ケースで検証します。
- raw usageの構成比だけでbackend意味論の独立認証はできません。
  outputにreasoningを重ねて足さない集計契約は維持します。
- 候補packetに実際に提示した範囲と、graderが参照する全原文は区別すべきです。
  presented_scopeという別次元の提案は有用です。原文実在と提示内実在を混ぜません。
- v2のquote正規化を採用するなら、raw一致と正規化後一致を別々に記録し、
  適用規則を版固定します。末尾rstripやCRLF変換による偽一致・位置ずれの負例が必要です。
  今回はまだ正規化を実装・採用していません。
- sourceが未知の場合に未検査quoteを「非含有ではない」と数えないでください。
  unsupported_citation_rateの分母は検査可能な引用と未検査の内訳を伴う必要があります。
- 「最小変更」の範囲は実際の堅牢性で決めます。空配列、非object item、sourceが配列、
  boolの行番号、空symbol、逆順/範囲外span、同名の複数symbol、重複quoteもfixture候補です。
- ユーザーは現在の性能を落とさない方針です。+2/+3/+5秒の許容や削減25%/10%等を
  採用閾値として決定していません。正の速度劣化を許すmarginは外部モデルだけで決めません。
  小標本で品質失敗ゼロでも一般的無劣化の証明にはなりません。
- cacheの有無による事後除外を主結果へ置換しません。原データ全件と感度分析を区別します。
  paired設計なら片armだけ除いた比較と完全ペア比較も別です。
- pooled sdからcase別の必要nを確定しません。新試行の回数や予算も未決定です。

## 4. 未提示だった実コード

各hashは元ファイルraw bytes、行番号は採取時です。全repoを含みません。


### tools/codex_environment.py

SHA-256: `8cabaf26b6e9386d1c6082f37a7484092b24aeb4765957b8029f909c9f06cfd7`


receipt: 行153–173

```python
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

```


### tools/codex_evidence.py

SHA-256: `af1019ebe71ffd25f6c554be71db50e27e71e21bc468c784a463349da7c4ca64`


archive: 行18–44

```python
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

```


validate: 行47–62

```python
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

```


### tools/codex_harness.py

SHA-256: `d2dd30889215c17de215d02c44fa689a37be4dab6607e32973485aff7be03db9`


HarnessError: 行27–28

```python
class HarnessError(ValueError):
    pass

```


verify: 行255–258

```python
def verify(root, task_id, check_id, command, watch, marker, timeout=120):
    identifier(check_id)
    with locked(task_dir(root, task_id) / ('verify-' + check_id)):
        return _verify(root, task_id, check_id, command, watch, marker, timeout)

```


### evaluation/run_m2.py: cases/oracleの定義

元ファイルSHA-256: `68aa39f1b1725c8fd5a3a873522ad7486ae6673e708e0c59f473444139bd2393`

```python
    cases = [
        dict(case_id='checked-reentry',diagnosis='REENTRY_CONTRACT_GAP',action='REUSE_SAVED_CONTRACT_AND_REVALIDATE',
             main_objective='CODEX_ENVIRONMENT',required_source='tools/codex_operations.py',
             question='Review the reproduced finish -> begin failure. Identify the cause and minimal next action, '
                      'preserving source freshness and current user-goal checks. Choose diagnosis from '
                      'REENTRY_CONTRACT_GAP/RUNTIME_DRIFT/NO_ISSUE/UNRESOLVED and action from '
                      'REUSE_SAVED_CONTRACT_AND_REVALIDATE/REVERIFY_CURRENT_ENVIRONMENT/PROCEED_WITH_OLD_PASS/UNRESOLVED.'),
        dict(case_id='runtime-drift',diagnosis='RUNTIME_DRIFT',action='REVERIFY_CURRENT_ENVIRONMENT',
             main_objective='CODEX_ENVIRONMENT',required_source='tools/codex_environment.py',
             question='Review the isolated runtime drift probe alongside the saved passing state. Can the saved PASS '
                      'be reused for this changed environment? State the cause and next action. Choose diagnosis from '
                      'REENTRY_CONTRACT_GAP/RUNTIME_DRIFT/NO_ISSUE/UNRESOLVED and action from '
                      'REUSE_SAVED_CONTRACT_AND_REVALIDATE/REVERIFY_CURRENT_ENVIRONMENT/PROCEED_WITH_OLD_PASS/UNRESOLVED.')]

```


APPROVALSはPUSH_PUBLICATION / MAIN_INTEGRATION / PRODUCTION_TRANSITION /
EXISTING_EVIDENCE_DELETIONの4コード（補足02のテスト・資料01の制約と同じ）です。
receiptのUNRESOLVEDは不明なモデル実効値・Human承認等で、必要入力欠落を許可する意味では
ありません。captureは明示外部依存についてis_fileと登録hashを要求し、gateはsource_guardを
呼びます。archiveも元bytesを読み、validateも保存objectの存在/hashを要求します。
「PRESENTしか見ないから必要外部依存欠落をPASSする」とするなら、この経路を含めた
具体的な反例を示してください。未宣言の依存は別の限界です。

## 5. 返答依頼（追加資料が不要ならここでレビューを閉じる）

1. 上記の4つの実測とreceipt関数を踏まえ、撤回/維持する欠陥指摘を確定してください。
2. 追補04のactivation明示refresh案と、出典検証v2について、実装を阻害する重大な不足が
   あれば具体的な負例で最大3件。なければローカル実装・正負テストへ進める旨を示してください。
3. 次の外部レビューは、設計の繰返しではなく実装差分・実テスト結果を対象にする案を
   評価してください。新たなモデル試行は契約/ケース/予算を別途確定してからです。

外部レビューの回数・多数決を正しさの証明にはしません。採否はCodex側で原文・実テストと
照合し、正式採用や公開等はHumanの権限を維持します。
