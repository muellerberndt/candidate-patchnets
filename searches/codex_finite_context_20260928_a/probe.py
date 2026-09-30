#!/usr/bin/env python3
"""Bounded candidate search with an independent8-state filter oracle."""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import math
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from contract import import_file
model = import_file(HERE/'model.py','context_probe_model')
STATES = tuple(product((0,1),repeat=3))
HAZARDS = (F(0),F(1,16),F(1,4))
STREAM = [-2]*4+[2]*4+[-2]*4
HISTORIES = ((-2,-2,-2,0),(2,2,2,0),(-2,-2,2,2,0),(2,2,-2,-2,0),
             (-2,)*5+(0,),(2,)*5+(0,),(-2,)*2+(2,)*5+(0,),
             (2,)*2+(-2,)*5+(0,),(-2,)*5+(2,)*2+(0,),
             (2,)*5+(-2,)*2+(0,),(-2,)*3+(2,)*3+(0,0),
             (2,)*3+(-2,)*3+(0,0))


def emission(y,bit):
    center = 4*bit-2
    values = [F(1,4**abs(z-center)) for z in range(-8,9)]
    return values[y+8]/sum(values)


def oracle(weights,h,y=None):
    out = []
    for a,b,new in STATES:
        mass = sum(weights[STATES.index((a,b,old))]*(1-h if old==new else h) for old in (0,1))
        if y is not None:
            mass *= emission(y,(a,b)[new])
        out.append(mass)
    total = sum(out)
    return tuple(w/total for w in out)


def positive(weights):
    return sum(w for (a,b,c),w in zip(STATES,weights) if (a,b)[c]==1)


def parameter_joint(weights):
    return tuple(sum(w for (a,b,c),w in zip(STATES,weights) if (a,b)==pair) for pair in product((0,1),repeat=2))


def split_parameters_context(weights,reset_parameters=False):
    params = (F(1,4),)*4 if reset_parameters else parameter_joint(weights)
    context = tuple(sum(w for bits,w in zip(STATES,weights) if bits[2]==c) for c in (0,1))
    return tuple(params[2*a+b]*context[c] for a,b,c in STATES)


def score(probability,y):
    prob_y = probability*emission(y,1)+(1-probability)*emission(y,0)
    return {'negative_log_probability':-math.log(float(prob_y)),
            'squared_center_error':float((4*probability-2-y)**2)}


def run():
    checks,trials,outcomes = {},[],{}
    def check(name,value):
        if name in checks:
            raise ValueError('Repeated check name')
        checks[name] = bool(value)
    for hazard in HAZARDS:
        key = str(hazard)
        for schedule in ('forward','reverse','synchronous'):
            brain = model.Brain(hazard,schedule=schedule)
            reference = (F(1,8),)*8
            endpoints=[]
            for event,y in enumerate(STREAM,1):
                prediction = brain.prediction()
                reference = oracle(reference,hazard,y)
                result = brain.observe(event,y)
                check(f'{key}/{schedule}/{event}/joint',brain.memory.weights==reference)
                check(f'{key}/{schedule}/{event}/admission',result['accepted'] and result['qualified'])
                query = brain.query()
                check(f'{key}/{schedule}/{event}/answer',query['positive']==float(positive(reference)))
                trials.append({'h':key,'schedule':schedule,'event':event,'value':y,
                               'prediction_positive':str(prediction['positive']),
                               'posterior_positive':str(positive(reference)),
                               'joint':[str(w) for w in reference],**result})
                if event%4==0:
                    endpoints.append(query['answer'])
            errors=[abs(mean-target) for mean,target in zip(endpoints,(-2,2,-2))]
            if schedule=='forward':
                outcomes[key]={'phase_means':endpoints,'phase_errors':errors,
                               'switching_pass':max(errors)<=.5}
        # Exhaustive small predictive tasks; no future data is shown to the brain.
        scored={name:[] for name in ('learned','known_parameters','reset_parameters','last_value','frozen')}
        for sequence in product((-2,2),repeat=5):
            brain=model.Brain(hazard)
            known=tuple(F(1,2) if (a,b)==(0,1) else F(0) for a,b,c in STATES)
            reset=(F(1,8),)*8
            for event,y in enumerate(sequence[:4],1):
                result=brain.observe(event,y)
                check(f'{key}/holdout/{sequence}/{event}',result['accepted'])
                known=oracle(known,hazard,y)
                reset=split_parameters_context(oracle(reset,hazard,y),reset_parameters=True)
            answers={'learned':brain.prediction()['positive'],
                     'known_parameters':positive(oracle(known,hazard)),
                     'reset_parameters':positive(oracle(reset,hazard)),
                     'last_value':F(int(sequence[3]>0)),'frozen':F(1,2)}
            for name,answer in answers.items():
                scored[name].append({'sequence':sequence,'prediction_positive':str(answer),**score(answer,sequence[4])})
        outcomes[key]['predictive_trials']=scored
        outcomes[key]['mean_predictive_scores']={name:{metric:sum(r[metric] for r in rows)/len(rows)
                    for metric in ('negative_log_probability','squared_center_error')} for name,rows in scored.items()}
        histories={}
        for sequence in HISTORIES:
            brain=model.Brain(hazard)
            for event,y in enumerate(sequence,1):
                before=brain.memory
                result=brain.observe(event,y)
                check(f'{key}/neutral/{sequence}/{event}',result['accepted'])
                if y==0:
                    check(f'{key}/neutral/{sequence}/{event}/parameter_invariance',parameter_joint(before.weights)==parameter_joint(brain.memory.weights))
            full=brain.query()['answer']
            # Preserve the complete parameter joint AND context marginal.
            erased=model.Brain(hazard,model.Memory(split_parameters_context(brain.memory.weights),brain.memory.count,brain.memory.last))
            swapped=tuple(brain.memory.weights[STATES.index((b,a,1-c))] for a,b,c in STATES)
            check(f'{key}/symmetry/{sequence}',swapped==brain.memory.weights)
            cutjoint=split_parameters_context(brain.memory.weights)
            ema=0.
            for y in sequence:
                ema=.5*ema+.5*y
            histories[str(sequence)]={'answer':full,'parameter_context_cut_answer':erased.query()['answer'],
                                     'parameter_joint':[str(w) for w in parameter_joint(brain.memory.weights)],
                                     'different_parameters_probability':str(sum(w for (a,b,c),w in zip(STATES,brain.memory.weights) if a!=b)),
                                     'dependency_total_variation':str(sum(abs(p-q) for p,q in zip(brain.memory.weights,cutjoint))/2),
                                     'cheap_controls':{'last_value':sequence[-1],'last_nonzero':next(y for y in reversed(sequence) if y),'ema_half':ema},
                                     'context_marginal':[str(sum(w for bits,w in zip(STATES,brain.memory.weights) if bits[2]==c)) for c in (0,1)]}
        cold=model.Brain(hazard)
        cold.observe(1,0)
        outcomes[key]['histories']=histories
        outcomes[key]['neutral_reset_mean']=cold.query()['answer']

    # Exact isolated representation witness, not an acquired memory claim.
    fixtures=[]
    for assignments in (((0,1,0),(1,0,1)),((0,1,1),(1,0,0))):
        memory=model.Memory(tuple(F(1,2) if bits in assignments else F(0) for bits in STATES))
        brain=model.Brain(F(1,16),memory)
        before=brain.snapshot()
        original=brain.query()['answer']
        altered=model.Brain(F(1,16),model.discard_dependence(memory)).query()['answer']
        check(f'fixture{len(fixtures)}/query_preserves',brain.snapshot()==before)
        fixtures.append({'intact_answer':original,'product_singletons_answer':altered})
    check('same marginals different public value', [x['intact_answer'] for x in fixtures]==[-2.,2.] and
          all(x['product_singletons_answer']==0 for x in fixtures))
    # Transaction and restart properties across all supplied hazards.
    for hazard in HAZARDS:
        brain=model.Brain(hazard)
        saved=brain.snapshot()
        cap=brain.observe(1,-2,budget=0)
        check(str(hazard)+'/cap',not cap['accepted'] and not cap['qualified'] and brain.snapshot()==saved)
        for event,y in enumerate(STREAM[:6],1):
            brain.observe(event,y)
        saved=brain.snapshot()
        for _ in range(5):
            brain.query(); brain.observe(6,2)
        check(str(hazard)+'/no_echo',brain.snapshot()==saved)
        restored=model.Brain(hazard)
        restored.restore(saved)
        for event,y in enumerate(STREAM[6:],7):
            brain.observe(event,y); restored.observe(event,y)
        check(str(hazard)+'/resume',brain.snapshot()==restored.snapshot())
    sources=[HERE/name for name in ('PROTOCOL.md','THEOREM.md','SKEPTICAL_CONTROLS.md',
              'model.py','probe.py','test_model.py','adapter_h0.py','adapter_h16.py','adapter_h4.py')]
    source_sha={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(sources)}
    source_sha[str(model.KERNEL_PATH.relative_to(model.WORKSPACE))]=hashlib.sha256(model.KERNEL_PATH.read_bytes()).hexdigest()
    return {'schema':'codex-finite-context-search/1','checks':checks,'primary_trials':trials,
            'outcomes':outcomes,'constructed_correlation_witness':fixtures,'sources':source_sha,
            'scope':{'brain_equivalence':False,'actual_belief_self_observation':False,
                     'general_context_discovery':False,'core_replacement_ready':False,'scaling':'LOCKED'}}


def main():
    path=HERE/'search_receipt.json'
    verify='--verify' in sys.argv
    if path.exists() and not verify:
        raise FileExistsError('Refusing to overwrite search receipt')
    start=time.monotonic()
    result=json.loads(json.dumps(run(),allow_nan=False))
    if verify:
        if json.loads(path.read_text())['result']!=result:
            raise ValueError('Source or scientific replay differs')
    else:
        with path.open('x') as out:
            json.dump({'elapsed_seconds':time.monotonic()-start,'result':result},out,indent=2)
            out.write('\n')
    if not all(result['checks'].values()):
        raise ValueError('Required exact/custody check failed')
    print(json.dumps({'checks':len(result['checks']),'primary_solves':len(result['primary_trials']),
                      'switching':{h:r['switching_pass'] for h,r in result['outcomes'].items()},
                      'elapsed_seconds':time.monotonic()-start,'core_replacement_ready':False}))


if __name__=='__main__':
    main()
