#!/usr/bin/env python3
"""One command inventories all criteria and runs the implemented bounded tasks.

A passed slice or reference run is never a complete criterion or release gate.
Each adapter is local executable code chosen by the user, not an untrusted plugin.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import hashlib
import json
import math
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time

from contract import Unsupported, ProbeFailure, import_file
import probes

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPERIMENTS = ROOT/'cadence-flagship/experiments'
ADAPTERS = {'normal-gamma':HERE/'adapters/normal_gamma.py', 'finite-cluster':HERE/'adapters/finite_cluster.py'}
STATUSES = {'PASS','FAIL','UNSUPPORTED','NOT_TESTED','ERROR'}


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def stable(value):
    """Keep all outcomes and numeric answers; wall-clock samples vary on replay."""
    if isinstance(value,dict):
        return {k:stable(v) for k,v in value.items() if k not in ('elapsed_seconds',)}
    if isinstance(value,list):
        return [stable(v) for v in value]
    return value


def run_bounded(command,cwd=HERE,timeout=10,max_output=8192):
    started,output = time.monotonic(),bytearray()
    process = subprocess.Popen(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                               start_new_session=True,shell=False)
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout,selectors.EVENT_READ)
            while selector.get_map():
                remaining = timeout-(time.monotonic()-started)
                if remaining<=0:
                    raise TimeoutError(f'Exceeded {timeout}s task limit')
                for key,_ in selector.select(remaining):
                    block = os.read(key.fd,4096)
                    if not block:
                        selector.unregister(key.fd)
                    output.extend(block)
                    if len(output)>max_output:
                        raise ValueError('Child output limit exceeded')
            process.wait(timeout=max(.001,timeout-(time.monotonic()-started)))
        return output.decode('utf-8'),process.returncode
    finally:
        try:
            os.killpg(process.pid,signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        process.stdout.close()


def module_for(adapter):
    module = import_file(adapter,'selected_candidate_adapter')
    if not callable(getattr(module,'create',None)) or not isinstance(module.METADATA,dict):
        raise ValueError('Adapter must expose create() and METADATA')
    if not module.METADATA.get('candidate_id') or not module.METADATA.get('source_paths'):
        raise ValueError('Adapter must identify its candidate and implementation source')
    return module


def registry():
    data = json.loads((HERE/'criteria.json').read_text())
    rows = data['criteria']
    ids = {r['id'] for r in rows}
    expected = ({f'P{i}' for i in range(1,6)}|{f'T{i}' for i in range(1,3)}|
                {f'M{i}' for i in range(1,7)}|{f'L{i}' for i in range(1,6)}|
                {f'A{i}' for i in range(1,6)}|{f'O{i}' for i in range(1,8)}|
                {f'D{i}' for i in range(1,5)})
    if len(rows)!=34 or ids!=expected:
        raise ValueError('The complete34-criterion inventory is required')
    if len(data['readiness_gates'])!=8 or {r['id'] for r in data['readiness_gates']}!={f'R{i}' for i in range(1,9)}:
        raise ValueError('The complete8-gate replacement inventory is required')
    return data


def source_bindings(adapter):
    module = module_for(adapter)
    paths = set(HERE.glob('*.py')) | {HERE/'README.md',HERE/'PROTOCOL.md',HERE/'criteria.json',Path(adapter).resolve()}
    paths |= {Path(p).resolve() for p in module.METADATA['source_paths']}
    # Pin imported finite fixtures and their source custody, even for an adapter
    # that will report that it cannot operate on those fixtures.
    for package in ('fly-transition-probe','fly-motif-probe','local-observer-repair'):
        directory = EXPERIMENTS/package
        paths |= set(directory.glob('*.py'))|set(directory.glob('*.mjs'))|set(directory.glob('*.md'))|{directory/'receipt.json'}
    result = {}
    for path in sorted(paths):
        if not path.is_file():
            raise ValueError(f'Missing source/fixture: {path}')
        result[os.path.relpath(path,ROOT)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def worker(adapter,key):
    import challenges
    functions = {**probes.TESTS,**challenges.TESTS}
    if key not in functions:
        return {'status':'NOT_TESTED','detail':'No executable task for this key','metrics':{}}
    try:
        result = functions[key](module_for(adapter).create)
        if result.get('status') not in STATUSES:
            raise ValueError('Invalid task verdict')
        canonical(result)  # Reject NaN/Infinity and nonserializable evidence.
        return result
    except Unsupported as error:
        return {'status':'UNSUPPORTED','detail':str(error),'metrics':{}}
    except ProbeFailure as error:
        return {'status':'FAIL','detail':str(error),'metrics':error.metrics}
    except Exception as error:
        return {'status':'ERROR','detail':f'{type(error).__name__}: {error}','metrics':{}}


def child(adapter,key):
    started = time.monotonic()
    try:
        text,code = run_bounded([sys.executable,str(HERE/'battery.py'),'--worker',key,'--adapter',str(adapter)])
        if code:
            raise ValueError(f'Child exited{code}: {text[-1000:]}')
        result = json.loads(text)
        if result.get('status') not in STATUSES:
            raise ValueError('Child omitted a valid status')
    except Exception as error:
        result = {'status':'ERROR','detail':f'{type(error).__name__}: {error}','metrics':{}}
    return key,{**result,'elapsed_seconds':time.monotonic()-started}


def assess(criteria,results):
    rows = []
    for criterion in criteria:
        key = criterion.get('test_key')
        result = results.get(key,{'status':'NOT_TESTED','detail':'Acceptance task is not implemented','metrics':{}})
        probe_status = result['status']
        # Currently every implemented protocol is a bounded slice. Never let a
        # thin PASS claim perception/memory/metacognition in full.
        criterion_status = probe_status if probe_status in ('FAIL','ERROR','UNSUPPORTED') else 'NOT_TESTED'
        rows.append({'id':criterion['id'],'title':criterion['title'],'test_key':key,
                     'probe_status':probe_status,'criterion_status':criterion_status,
                     'scope':criterion.get('scope'),'coverage':criterion.get('coverage'),
                     'full_contract_ready':False,'evidence':result})
    return rows


def execute(adapter,jobs=2):
    if type(jobs) is not int or not 1<=jobs<=4:
        raise ValueError('Use1..4 local workers')
    spec = registry()
    module = module_for(adapter)
    before = source_bindings(adapter)
    keys = {r['test_key'] for r in spec['criteria'] if r.get('test_key')}
    keys |= {r['test_key'] for r in spec['challenge_fixtures'] if r.get('test_key') and r.get('execution_mode')=='CANDIDATE'}
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = dict(pool.map(lambda key:child(adapter,key),sorted(keys)))
    if source_bindings(adapter)!=before:
        raise ValueError('Candidate, harness or fixture changed during evaluation')
    rows = assess(spec['criteria'],results)
    gaps = module.METADATA.get('declared_unmet_gates',[])
    gates = [{'id':r['id'],'status':'UNSUPPORTED' if r['id'] in gaps else 'NOT_TESTED',
              'detail':'Candidate declares an unmet requirement' if r['id'] in gaps else 'Requires the named independent artifacts/review'}
             for r in spec['readiness_gates']]
    fixtures = []
    for fixture in spec['challenge_fixtures']:
        if fixture.get('execution_mode')=='CANDIDATE':
            result = results.get(fixture.get('test_key'),{'status':'NOT_TESTED','detail':'No executable fixture','metrics':{}})
            fixtures.append({'id':fixture['id'],'execution_mode':'CANDIDATE','evidence':result})
        else:
            fixtures.append({'id':fixture['id'],'execution_mode':'REFERENCE',
                             'evidence':{'status':'NOT_TESTED','detail':'See separately executed reference section','metrics':{}}})
    return {'candidate_id':module.METADATA['candidate_id'],'adapter':os.path.relpath(adapter,ROOT),
            'scope':module.METADATA.get('scope'),'source_sha256':before,'criteria':rows,
            'challenges':fixtures,'readiness_gates':gates,
            'probe_counts':dict(Counter(r['probe_status'] for r in rows)),
            'all34_full_contracts_passed':False,'core_replacement_ready':False,'scaling':'LOCKED'}


def references():
    cases = [('local-reference-packages',[sys.executable,'run.py','--verify'],EXPERIMENTS/'local-brain-gates'),
             ('prior-game-evidence',[sys.executable,'check_evidence.py','--verify'],
              ROOT/'plan/audits/cadence/unified_redesign_2026-09-28')]
    results = []
    for name,command,cwd in cases:
        if not cwd.is_dir():
            results.append({'id':name,'execution_mode':'REFERENCE','status':'NOT_TESTED',
                            'detail':'Optional local reference inputs unavailable','counts_as_candidate_evidence':False})
            continue
        try:
            source_before = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in cwd.iterdir() if p.is_file() and p.suffix in ('.py','.json','.md')}
            output,code = run_bounded(command,cwd,timeout=60,max_output=65536)
            source_after = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in cwd.iterdir() if p.is_file() and p.suffix in ('.py','.json','.md')}
            if source_before!=source_after:
                raise ValueError('Reference sources changed during verification')
            results.append({'id':name,'execution_mode':'REFERENCE','status':'PASS' if code==0 else 'FAIL',
                            'output':output,'source_sha256':source_before,'counts_as_candidate_evidence':False})
        except Exception as error:
            results.append({'id':name,'execution_mode':'REFERENCE','status':'ERROR',
                            'detail':str(error),'counts_as_candidate_evidence':False})
    return results


def partial_report(adapter,error):
    """A source/setup failure never loses the required inventory or looks green."""
    spec = registry()  # An unreadable catalogue cannot support a qualified report.
    rows = assess(spec['criteria'],{})
    return {'candidate_id':'UNRESOLVED: '+Path(adapter).name,
            'adapter':os.path.relpath(adapter,ROOT),'scope':'Evaluation aborted; no readiness evidence.',
            'execution_error':f'{type(error).__name__}: {error}',
            'source_sha256':{},'criteria':rows,
            'challenges':[{'id':r['id'],'execution_mode':r['execution_mode'],
                           'evidence':{'status':'NOT_TESTED','detail':'Evaluation aborted','metrics':{}}}
                          for r in spec['challenge_fixtures']],
            'readiness_gates':[{'id':r['id'],'status':'NOT_TESTED','detail':'Evaluation aborted'}
                               for r in spec['readiness_gates']],
            'probe_counts':{'NOT_TESTED':34},'all34_full_contracts_passed':False,
            'core_replacement_ready':False,'scaling':'LOCKED'}


def attach_references(candidates,reference_results):
    lookup = {r['id']:r for r in reference_results}
    for candidate in candidates:
        for fixture in candidate['challenges']:
            if fixture['execution_mode']!='REFERENCE':
                continue
            owner = 'prior-game-evidence' if fixture['id']=='prior_game_evidence' else 'local-reference-packages'
            if owner in lookup:
                fixture['evidence'] = {'status':lookup[owner]['status'],
                    'detail':f'Separate {owner} verification; not selected-candidate evidence',
                    'metrics':{'reference_id':owner,'counts_as_candidate_evidence':False}}


def markdown(report):
    lines = ['# Candidate qualification battery','',
             '**Core replacement: NOT READY. Scaling: LOCKED.**','',
             'PASS in a bounded probe does not discharge the full capability. Reference checks are separate.','']
    for candidate in report['candidates']:
        lines += [f"## {candidate['candidate_id']}",'',candidate['scope'],'',
                  '| Criterion | Bounded probe | Full criterion |','| --- | --- | --- |']
        lines += [f"| {r['id']}: {r['title']} | {r['probe_status']} | {r['criterion_status']} |" for r in candidate['criteria']]
        lines += ['','| Additional challenge | Result |','| --- | --- |']
        lines += [f"| {r['id']} ({r['execution_mode']}) | {r['evidence']['status']} |" for r in candidate['challenges']]
        lines += ['','Bounded probe details:','']
        for row in candidate['criteria']:
            if row['test_key']:
                evidence = row['evidence']
                lines.append(f"- **{row['id']} — {evidence['status']}:** {evidence['detail']} Metrics: `{json.dumps(evidence.get('metrics',{}),sort_keys=True)}`")
        lines += ['','Replacement gates: '+', '.join(f"{r['id']} {r['status']}" for r in candidate['readiness_gates'])+'.','']
        if candidate.get('execution_error'):
            lines += ['**Execution error:** '+candidate['execution_error'],'']
    lines += ['## Reference checks','']
    for reference in report['references']:
        lines.append(f"- {reference['id']}: **{reference['status']}**. Does not count as selected-candidate evidence.")
    return '\n'.join(lines)+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--candidate',choices=sorted(ADAPTERS))
    selection.add_argument('--adapter',type=Path)
    selection.add_argument('--all',action='store_true')
    parser.add_argument('--jobs',type=int,default=2)
    parser.add_argument('--no-references',action='store_true')
    parser.add_argument('--worker',help=argparse.SUPPRESS)
    parser.add_argument('--out',type=Path)
    parser.add_argument('--verify',type=Path)
    args = parser.parse_args()
    if args.worker:
        if not args.adapter:
            parser.error('Worker requires an adapter')
        print(json.dumps(worker(args.adapter,args.worker),allow_nan=False))
        return
    if args.out and args.verify:
        parser.error('Choose --out or --verify')
    if args.out and (args.out.exists() or args.out.with_suffix('.md').exists()):
        raise FileExistsError('Refusing to overwrite a report')
    selected = list(ADAPTERS.values()) if args.all else [args.adapter.resolve() if args.adapter else ADAPTERS[args.candidate or 'normal-gamma']]
    started = time.monotonic()
    candidates = []
    for adapter in selected:
        try:
            candidates.append(execute(adapter,args.jobs))
        except Exception as error:
            candidates.append(partial_report(adapter,error))
    reference_results = [] if args.no_references else references()
    attach_references(candidates,reference_results)
    report = {'schema':'cadence-candidate-battery/1','candidates':candidates,
              'references':reference_results,
              'elapsed_seconds':time.monotonic()-started,'core_replacement_ready':False,'scaling':'LOCKED'}
    if args.verify:
        previous = json.loads(args.verify.read_text())
        # Reference tools print their own wall times; their exit verdict and
        # source hashes are stable evidence, their console text is diagnostic.
        def comparable(value):
            value = stable(value)
            for ref in value['references']:
                ref.pop('output',None)
            return value
        if canonical(comparable(previous))!=canonical(comparable(report)):
            raise ValueError('Candidate verdicts, numeric evidence or source-bound replay differ')
    elif args.out:
        with args.out.open('x') as output:
            json.dump(report,output,indent=2,allow_nan=False)
            output.write('\n')
        with args.out.with_suffix('.md').open('x') as output:
            output.write(markdown(report))
    else:
        print(markdown(report))
    for candidate in report['candidates']:
        print(candidate['candidate_id']+': '+json.dumps(candidate['probe_counts'],sort_keys=True))
        print('  Challenges: '+', '.join(f"{r['id']}={r['evidence']['status']}" for r in candidate['challenges'] if r['execution_mode']=='CANDIDATE'))
    print(f"All34 criteria reported per candidate; replacement NOT READY; elapsed{report['elapsed_seconds']:.3f}s")
    # A scientifically expected FAIL remains a negative verdict. A verification
    # replay can succeed at reproducing it without turning it into a PASS.
    errors = any(r['probe_status']=='ERROR' for c in report['candidates'] for r in c['criteria'])
    errors |= any(c.get('execution_error') for c in report['candidates'])
    errors |= any(r['evidence']['status']=='ERROR' for c in report['candidates'] for r in c['challenges'])
    errors |= any(r['status'] in ('ERROR','FAIL') for r in report['references'])
    if errors:
        raise SystemExit(2)


if __name__=='__main__':
    main()
