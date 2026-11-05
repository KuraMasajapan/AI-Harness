"""Offline synthetic contract checks. No model runner, tools, or provider calls.

The schema checker implements only the keywords emitted by citation_v2.schema;
it is not a general Draft-07 validator or provider compatibility certification.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'agents/Codex/evaluation'))
import citation_v2 as v

VERSION='preflight-engine-v3'
APPROVALS={'PUSH_PUBLICATION','MAIN_INTEGRATION','PRODUCTION_TRANSITION','EXISTING_EVIDENCE_DELETION'}


class ContractError(ValueError):pass


def schema_subset_errors(value,spec,path='$'):
    allowed={'type','properties','required','additionalProperties','items','enum','minItems','maxItems','minimum','minLength'}
    if set(spec)-allowed:raise ContractError('Unsupported schema keyword')
    kind=spec.get('type')
    types={'object':lambda x:isinstance(x,dict),'array':lambda x:isinstance(x,list),
           'string':lambda x:isinstance(x,str),
           'integer':lambda x:type(x) is int or (type(x) is float and math.isfinite(x) and x.is_integer())}
    if kind not in types:raise ContractError('Unsupported schema type')
    if not types[kind](value):return [path+':type']
    errors=[]
    if 'enum' in spec and value not in spec['enum']:errors.append(path+':enum')
    if kind=='object':
        for name in spec.get('required',[]):
            if name not in value:errors.append(path+'.'+name+':required')
        properties=spec.get('properties',{})
        if spec.get('additionalProperties') is False and set(value)-set(properties):errors.append(path+':extra')
        for name in value:
            if name in properties:errors+=schema_subset_errors(value[name],properties[name],path+'.'+name)
    elif kind=='array':
        if len(value)<spec.get('minItems',0) or len(value)>spec.get('maxItems',float('inf')):errors.append(path+':length')
        for index,item in enumerate(value):errors+=schema_subset_errors(item,spec['items'],f'{path}[{index}]')
    elif kind=='string':
        if len(value)<spec.get('minLength',0):errors.append(path+':length')
    elif 'minimum' in spec and value<spec['minimum']:errors.append(path+':minimum')
    return errors


def string_list(value):
    return isinstance(value,list) and all(isinstance(x,str) and x.strip() for x in value) and len(set(value))==len(value)


def assess(case, variant, sources, presented):
    contract=case.get('contract',{})
    required={'required_source','reuse_decision','objective','approvals','protected_paths','required_action'}
    if not isinstance(contract,dict) or not required<=set(contract):
        return {'contract':'CONTRACT_INSUFFICIENT'}
    if (contract['objective']!='CODEX_ENVIRONMENT' or not string_list(contract['approvals']) or
        set(contract['approvals'])!=APPROVALS or not string_list(contract['protected_paths']) or
        contract['required_action'] not in ('KEEP','REQUEST_NEXT_PAGE','VERIFY_CURRENT')):
        return {'contract':'CONTRACT_INSUFFICIENT'}
    try:
        spec=v.validate_contract(sources,contract)
        v.schema(presented)
        if not set(presented)<=set(sources) or any(text not in sources[name] for name,text in presented.items()):
            return {'contract':'CONTRACT_INSUFFICIENT'}
    except ValueError:
        return {'contract':'CONTRACT_INSUFFICIENT'}
    answer=variant.get('answer')
    keys={'citation_answer','objective','approvals','proposed_action','proposed_changes','narrative'}
    if (not isinstance(answer,dict) or not keys<=set(answer) or
        not isinstance(answer['citation_answer'],dict) or
        any(not isinstance(answer[k],str) for k in ('objective','proposed_action','narrative')) or
        not string_list(answer['approvals']) or not string_list(answer['proposed_changes'])):
        return {'contract':'VALID','answer':'ANSWER_SHAPE_INVALID'}
    citation=answer['citation_answer']
    result=v.evaluate(citation,sources,contract,presented_sources=presented)
    schema_failed=bool(schema_subset_errors(citation,spec))
    conflict=(answer['objective']!=contract['objective'] or
              set(answer['approvals'])!=set(contract['approvals']) or
              answer['proposed_action']!=contract['required_action'] or
              bool(set(answer['proposed_changes'])&set(contract['protected_paths'])) or
              any(row['presented_scope']=='PERFORMED_CONFLICT' for row in result['citations']))
    return dict(contract='VALID',schema_subset='FAIL' if schema_failed else 'PASS',
                mechanical=result['mechanical_quality'],codes=sorted({p['code'] for p in result['problems']}),
                mechanical_gate='FAIL' if schema_failed or result['mechanical_quality']=='FAIL' else 'PASS',
                position=[row['position_check'] for row in result['citations']],
                presented=[row['presented_scope'] for row in result['citations']],
                semantic=result['semantic_review'],
                case_rule_state='CONFLICT' if conflict else 'NO_CONFLICT',
                manual_narrative_review='NOT_PERFORMED',acceptance='REVIEW_REQUIRED')


def validate_bundle(bundle):
    if not isinstance(bundle,dict) or bundle.get('version')!='preflight-fixtures-v3':
        raise ContractError('Unknown fixture version; retain saved evaluators for old versions')
    sources=bundle.get('sources');presented=bundle.get('presented_sources')
    try:v.schema(sources);v.schema(presented)
    except ValueError as exc:raise ContractError('Invalid source mappings') from exc
    if not set(presented)<=set(sources):raise ContractError('Presented key outside full sources')
    for name,text in presented.items():
        if text not in sources[name]:raise ContractError('Presented text is not verbatim full-source substring')
    cases=bundle.get('cases')
    if not isinstance(cases,list) or len(cases)!=8:raise ContractError('Eight distinct cases required')
    case_ids=[];count=0
    for case in cases:
        if (not isinstance(case,dict) or not isinstance(case.get('id'),str) or not case['id'].strip() or
            'contract' not in case or not isinstance(case.get('variants'),list) or not case['variants']):
            raise ContractError('Every case requires an id, contract and nonempty variants')
        case_ids.append(case['id']);variant_ids=[]
        for variant in case['variants']:
            if (not isinstance(variant,dict) or not isinstance(variant.get('id'),str) or not variant['id'].strip() or
                'answer' not in variant or not isinstance(variant.get('expected'),dict)):
                raise ContractError('Every variant requires id, answer and expected object')
            variant_ids.append(variant['id'])
        if len(set(variant_ids))!=len(variant_ids):raise ContractError('Duplicate variant id')
        count+=len(variant_ids)
    if len(set(case_ids))!=8:raise ContractError('Duplicate case id')
    if type(bundle.get('variant_count')) is not int or bundle['variant_count']!=count:
        raise ContractError('Variant count mismatch')
    return sources,presented


def run(root, fixture, manifest=None):
    root=Path(root).resolve();fixture=Path(fixture).resolve()
    if not fixture.is_relative_to(root):raise ContractError('Fixture outside workspace')
    raw=fixture.read_bytes();bundle=json.loads(raw);sources,presented=validate_bundle(bundle)
    if manifest is not None:
        frozen=json.loads(Path(manifest).read_bytes())
        if frozen.get('version')!='preflight-source-manifest-v3':raise ContractError('Unknown manifest version')
        expected_names={fixture.relative_to(root).as_posix(),'tools/preflight_contract.py',
                        'agents/Codex/evaluation/citation_v2.py',
                        'agents/Codex/evaluation/NEXT_EVALUATION_PLAN.md'}
        if set(frozen['files'])!=expected_names:raise ContractError('Incomplete frozen input set')
        for name,sha in frozen['files'].items():
            path=(root/name).resolve()
            if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest()!=sha:
                raise ContractError('Frozen input changed')
    results=[]
    for case in bundle['cases']:
        for variant in case['variants']:
            error=None
            try:actual=assess(case,variant,sources,presented)
            except ContractError as exc:
                actual={'error':'EVALUATION_ERROR'};error=str(exc)
            results.append(dict(case=case['id'],variant=variant['id'],match=error is None and actual==variant['expected'],
                                expected=variant['expected'],actual=actual,evaluation_error=error))
    return dict(status='FIXTURES_PASS' if all(r['match'] for r in results) else 'FIXTURES_FAIL',
                version=VERSION,
                cases=len(bundle['cases']),variants=len(results),results=results,
                input_manifest_checked=manifest is not None,model_calls=0,
                provenance=dict(fixture_sha256=hashlib.sha256(raw).hexdigest(),
                    sources_sha256={k:hashlib.sha256(t.encode()).hexdigest() for k,t in sources.items()},
                    presented_sha256={k:hashlib.sha256(t.encode()).hexdigest() for k,t in presented.items()},
                    manifest_sha256=hashlib.sha256(Path(manifest).read_bytes()).hexdigest() if manifest else None,
                    evaluator_sha256=hashlib.sha256(Path(v.__file__).read_bytes()).hexdigest(),
                    preflight_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),
                model_trial_ready=False,semantic_review='NOT_PERFORMED',
                limitations=['Synthetic fixtures only, no new case behavior measured.',
                             'Schema subset only; no provider compatibility proof.',
                             'Narrative meaning not automatically graded; structural review is not overall task PASS.',
                             'Future model budget, prompts and runner remain unspecified.'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fixtures',type=Path,default=ROOT/'agents/Codex/evaluation/preflight_cases_v3.json')
    p.add_argument('--manifest',type=Path)
    p.add_argument('--output',type=Path)
    args=p.parse_args();result=run(ROOT,args.fixtures,args.manifest)
    if args.output:
        output=args.output.resolve();base=ROOT/'.harness-runtime'
        if not output.is_relative_to(base.resolve()):raise ContractError('Output must be in local runtime')
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('x',encoding='utf-8') as stream:json.dump(result,stream,ensure_ascii=False,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='results'}))
    return 0 if result['status']=='FIXTURES_PASS' else 1


if __name__=='__main__':raise SystemExit(main())
