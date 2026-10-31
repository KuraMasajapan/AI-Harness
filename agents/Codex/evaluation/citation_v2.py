"""Offline v2 citation diagnostics. No calls, v1 imports, or primary-result writes.

Mechanical quality excludes position/presented-scope/semantic judgments, reported
separately. Raw matching is default; CRLF-only normalization is explicit opt-in.
This schema is local, not an assertion of compatibility with a provider API.
"""
import ast
import hashlib
import json
from pathlib import Path
import re
import uuid

VERSION = 'citation-v2.2'
DECISIONS = ('RE_CONFIRM', 'RE_EXECUTE', 'DIAGNOSE')


def schema(sources):
    if not isinstance(sources, dict) or not sources or any(not isinstance(k,str) or not isinstance(v,str) for k,v in sources.items()):
        raise ValueError('Sources must be a nonempty filename/text mapping')
    return {'type':'object','additionalProperties':False,'required':['evidence','reuse_decision'],
            'properties':{'reuse_decision':{'type':'string','enum':list(DECISIONS)},
            'evidence':{'type':'array','minItems':1,'items':{'type':'object','additionalProperties':False,
            'required':['source','quote'],'properties':{
                'source':{'type':'string','enum':sorted(sources)},'quote':{'type':'string','minLength':12},
                'symbol':{'type':'string','minLength':1},
                'lines':{'type':'array','minItems':2,'maxItems':2,'items':{'type':'integer','minimum':1}}}}}}}


def validate_contract(sources, oracle):
    contract = schema(sources)
    if not isinstance(oracle,dict) or not isinstance(oracle.get('required_source'),str) or oracle['required_source'] not in sources or oracle.get('reuse_decision') not in DECISIONS:
        raise ValueError('Oracle must name an available source and known decision')
    return contract


def occurrences(text, quote):
    start=0; found=[]
    while quote:
        offset=text.find(quote,start)
        if offset<0:break
        found.append(offset);start=offset+1
    return found


def position(source, citation, quote, normalize):
    if 'symbol' not in citation and 'lines' not in citation:
        return 'NOT_PERFORMED', None
    # Match Python physical lines; CRLF is atomic, Unicode separators are data.
    lines=re.findall(r'[^\r\n]*(?:\r\n|\r|\n)|[^\r\n]+$',source);lo,hi=1,len(lines)
    if 'symbol' in citation:
        symbol=citation['symbol']
        if not isinstance(symbol,str) or not symbol.strip():return 'UNRESOLVED','LOCATOR_UNRESOLVED'
        try:tree=ast.parse(source)
        except (SyntaxError,ValueError):return 'UNRESOLVED','LOCATOR_UNRESOLVED'
        nodes=[n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and n.name==symbol]
        if len(nodes)!=1:return 'UNRESOLVED','LOCATOR_UNRESOLVED'
        lo,hi=nodes[0].lineno,nodes[0].end_lineno
    if 'lines' in citation:
        span=citation['lines']
        if not isinstance(span,list) or len(span)!=2 or any(type(x) is not int for x in span):
            return 'UNRESOLVED','LOCATOR_UNRESOLVED'
        a,b=span
        if not 1<=a<=b<=len(lines):return 'UNRESOLVED','LOCATOR_UNRESOLVED'
        lo,hi=max(lo,a),min(hi,b)
    if lo>hi or normalize(quote) not in normalize(''.join(lines[lo-1:hi])):
        return 'PERFORMED_CONFLICT','LOCATOR_CONFLICT'
    return 'PERFORMED_MATCH',None


def evaluate(answer, sources, oracle, *, normalize_crlf=False, presented_sources=None):
    """Evaluate v2-only fields, never general task quality or Human approval.

    Invalid frozen contracts raise before answer processing; malformed answers
    return indexed diagnostics. No guessed filenames, fuzzy matching, or rstrip.
    """
    validate_contract(sources,oracle)
    if type(normalize_crlf) is not bool:raise ValueError('Normalization must be explicit boolean')
    if presented_sources is not None:
        schema(presented_sources)
        if not set(presented_sources)<=set(sources):raise ValueError('Presented source outside frozen sources')
    norm=(lambda x:x.replace('\r\n','\n')) if normalize_crlf else (lambda x:x)
    problems=[]; rows=[]
    def problem(code,index=None):problems.append({'code':code,'citation_index':index})
    if not isinstance(answer,dict):
        problem('ANSWER_NOT_OBJECT');answer={}
    if set(answer)-{'evidence','reuse_decision'}:problem('ANSWER_FIELDS')
    if answer.get('reuse_decision')!=oracle['reuse_decision']:problem('REUSE_DECISION_MISMATCH')
    citations=answer.get('evidence')
    if not isinstance(citations,list):problem('EVIDENCE_NOT_ARRAY');citations=[]
    elif not citations:problem('EVIDENCE_EMPTY')
    required=False;checked=0;not_found=0
    for index,citation in enumerate(citations):
        row={'citation_index':index,'raw_match':None,'normalized_match':None,
             'raw_occurrences':[],'normalized_occurrences':[],
             'position_check':'NOT_PERFORMED','presented_scope':'NOT_PERFORMED',
             'semantic_review':'NOT_PERFORMED'}
        rows.append(row)
        if not isinstance(citation,dict):problem('CITATION_NOT_OBJECT',index);continue
        if set(citation)-{'source','quote','symbol','lines'}:problem('CITATION_FIELDS',index)
        # Offline input is not protected by provider-side schema enforcement.
        # Type/domain errors are formal failures, not independent position results.
        locator_invalid = ('symbol' in citation and (not isinstance(citation['symbol'],str) or not citation['symbol'].strip())) or (
                'lines' in citation and (not isinstance(citation['lines'],list) or len(citation['lines'])!=2 or
                                        any(type(x) is not int or x<1 for x in citation['lines'])))
        if locator_invalid:problem('CITATION_TYPE_INVALID',index)
        name=citation.get('source');quote=citation.get('quote')
        if not isinstance(name,str):problem('SOURCE_NOT_STRING',index);continue
        if name not in sources:problem('SOURCE_UNKNOWN',index);continue
        required=required or name==oracle['required_source']
        if not isinstance(quote,str):problem('QUOTE_NOT_STRING',index);continue
        if len(quote.strip())<12:problem('QUOTE_TOO_SHORT',index);continue
        checked+=1
        raw=occurrences(sources[name],quote)
        normalized=occurrences(norm(sources[name]),norm(quote)) if normalize_crlf else []
        row.update(raw_match=bool(raw),raw_occurrences=raw,
                   normalized_match=bool(normalized) if normalize_crlf else None,
                   normalized_occurrences=normalized)
        if not raw and not normalized:
            not_found+=1;problem('QUOTE_NOT_FOUND',index);continue
        if not locator_invalid:
            pos,code=position(sources[name],citation,quote,norm)
            row['position_check']=pos
            if code:problem(code,index)
        if presented_sources is not None:
            row['presented_scope']='PERFORMED_MATCH' if name in presented_sources and norm(quote) in norm(presented_sources[name]) else 'PERFORMED_CONFLICT'
    if not required:problem('REQUIRED_SOURCE_MISSING')
    mechanical=[p for p in problems if not p['code'].startswith('LOCATOR_')]
    return {'version':VERSION,'mechanical_quality':'FAIL' if mechanical else 'PASS',
            'acceptance':'REVIEW_REQUIRED','semantic_review':'NOT_PERFORMED',
            'normalization':'CRLF_TO_LF' if normalize_crlf else 'NONE',
            'problems':problems,'citations':rows,
            'unsupported_citation_rate':not_found/checked if checked else None,
            'literal_checked':checked,'literal_unchecked':len(citations)-checked,
            'position_matches':sum(r['position_check']=='PERFORMED_MATCH' for r in rows),
            'source_hashes':{k:hashlib.sha256(v.encode('utf-8')).hexdigest() for k,v in sources.items()},
            'limitation':'V2 fields only. Position and presented scope are independent; not semantic/task correctness or adoption.'}


def write_derived(root, answer, sources, oracle, **options):
    """New directory only; keep schema, exact texts/options and implementation hash.

    No destination override or write path into primary trials. No regrading is
    implicit: callers supply an explicit v2 answer/oracle, not a v1 conversion.
    """
    result=evaluate(answer,sources,oracle,**options)
    bundle={'version':VERSION,'schema':validate_contract(sources,oracle),
            'answer':answer,'sources':sources,'oracle':oracle,'options':options,
            'evaluator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'result':result}
    payload=json.dumps(bundle,ensure_ascii=False,indent=2).encode('utf-8')
    base=Path(root).resolve()/'.harness-runtime'/'derived'/VERSION
    # Refuse redirected runtime folders rather than writing through symlinks.
    if not base.resolve().is_relative_to(Path(root).resolve()):raise ValueError('Derived directory escapes root')
    base.mkdir(parents=True,exist_ok=True)
    folder=base/uuid.uuid4().hex;folder.mkdir()
    path=folder/'evaluation.json'
    with path.open('xb') as stream:stream.write(payload)
    return {'path':path.relative_to(Path(root).resolve()).as_posix(),
            'sha256':hashlib.sha256(payload).hexdigest(),'mechanical_quality':result['mechanical_quality']}


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('answer','sources','oracle'):parser.add_argument('--'+name,required=True,type=Path)
    parser.add_argument('--presented',type=Path)
    parser.add_argument('--normalize-crlf',action='store_true')
    args=parser.parse_args()
    load=lambda p:json.loads(p.read_bytes())
    result=write_derived(Path(__file__).resolve().parents[3],load(args.answer),load(args.sources),load(args.oracle),
                         normalize_crlf=args.normalize_crlf,
                         presented_sources=load(args.presented) if args.presented else None)
    print(json.dumps(result))


if __name__=='__main__':main()
