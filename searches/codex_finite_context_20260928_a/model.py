"""Exact finite context memory, retained through the same local factor kernel."""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from contract import import_file, Candidate

WORKSPACE = Path(__file__).resolve().parents[3]
KERNEL_PATH = WORKSPACE/'cadence-flagship/experiments/local-observer-repair/kernel.py'
kernel = import_file(KERNEL_PATH,'codex_context_local_kernel')
BITS = tuple(product((0,1),repeat=3))
SCOPE = ('A','B','old')
CENTRAL = ('A','B','old','new')
NEW = ('A','B','new')
CENTERS = (-2,2)
NORMALIZERS = tuple(sum((F(4)**(-abs(y-mu)) for y in range(-8,9)),F(0)) for mu in CENTERS)


def likelihood(y,bit):
    return F(4)**(-abs(y-CENTERS[bit]))/NORMALIZERS[bit]


def factor(scope,rule):
    return kernel.Factor(scope,{bits:F(rule(bits)) for bits in product((0,1),repeat=len(scope))})


@dataclass(frozen=True)
class Memory:
    weights: tuple = (F(1,8),)*8
    count: int = 0
    last: int | None = None

    def __post_init__(self):
        if (type(self.weights) is not tuple or len(self.weights)!=8 or
                any(type(w) is not F or w<0 for w in self.weights) or sum(self.weights)!=1):
            raise ValueError('Memory must be a normalized exact8-state joint')
        if type(self.count) is not int or not 0<=self.count<=24:
            raise ValueError('Event count outside capacity')
        if self.count==0 and self.last is not None or self.count>0 and (type(self.last) is not int or not -8<=self.last<=8):
            raise ValueError('Invalid latest witness')


def build(memory,h,y=None):
    prior = kernel.Factor(SCOPE,dict(zip(BITS,memory.weights)))
    transition = factor(CENTRAL,lambda a:h if a[2]!=a[3] else 1-h)
    emission = factor(NEW,lambda a:1 if y is None else likelihood(y,a[a[2]]))
    readout = factor(NEW+('Q',),lambda a:int(a[3]==a[a[2]]))
    return kernel.Network([transition,prior,emission,readout],[(0,1),(0,2),(0,3)])


def qualify(network,result):
    """Recompute from actual messages rather than accepting diagnostic flags."""
    try:
        actual = network.beliefs(result.messages)
        if actual!=result.beliefs or network.edge_residual(actual)!=0:
            return False
        for edge in network.separators:
            if network._message(*edge,result.messages)!=result.messages[edge]:
                return False
        return result.converged is True
    except (ValueError,KeyError,TypeError,AttributeError):
        return False


def completion(memory,h,y=None,budget=256,schedule='forward'):
    if type(budget) is not int or not 0<=budget<=256:
        raise ValueError('Invalid repair budget')
    net = build(memory,h,y)
    result = net.settle(schedule=schedule,max_sweeps=budget)
    if not qualify(net,result):
        return None,result
    boundary = result.beliefs[0].marginal(NEW)
    output = result.beliefs[3].marginal(('Q',))
    weights = tuple(boundary.values[b] for b in BITS)
    return {'weights':weights,'positive':output.values[(1,)],
            'answer':sum(CENTERS[b]*output.values[(b,)] for b in (0,1))},result


class Brain(Candidate):
    def __init__(self,h=F(1,16),memory=None,schedule='forward'):
        if h not in (F(0),F(1,16),F(1,4)):
            raise ValueError('This version has exactly three frozen settings')
        self.h,self.memory,self.schedule = h,memory or Memory(),schedule

    def observe(self,event,value,*,kind='witness',budget=256):
        if kind!='witness' or type(event) is not int or type(value) is not int or not -8<=value<=8:
            raise ValueError('Requires an ordered owned integer witness')
        if self.memory.count and event==self.memory.count and value==self.memory.last:
            return {'accepted':False,'qualified':True,'duplicate':True,'sweeps':0}
        if event!=self.memory.count+1 or self.memory.count==24:
            raise ValueError('Conflicting/stale/skipped/overflowing event')
        completed,result = completion(self.memory,self.h,value,budget,self.schedule)
        if completed is not None:
            self.memory = Memory(completed['weights'],event,value)
        return {'accepted':completed is not None,'qualified':completed is not None,
                'duplicate':False,'sweeps':result.sweeps,'message_updates':result.updates,
                'message_evaluations':result.message_evaluations}

    def exact_query(self):
        completed,result = completion(self.memory,F(0),schedule=self.schedule)
        if completed is None:
            raise ValueError('Read-only query failed exact qualification')
        return completed,result

    def query(self):
        completed,result = self.exact_query()
        if completed['weights']!=self.memory.weights:
            raise ValueError('An unobserved normalized output changed the prior')
        mean = completed['answer']
        return {'answer':float(mean),'variance':float(4-mean*mean),
                'positive':float(completed['positive']),'qualified':True,'residual':0.}

    def prediction(self):
        """One event of context motion with no observation, on a private branch."""
        completed,result = completion(self.memory,self.h,schedule=self.schedule)
        if completed is None:
            raise ValueError('Prediction failed')
        return completed

    def snapshot(self):
        return json.dumps({'schema':'finite-context-local-conditioning/1','h':str(self.h),
                           'weights':[str(w) for w in self.memory.weights],
                           'count':self.memory.count,'last':self.memory.last},sort_keys=True)

    def restore(self,text):
        if not isinstance(text,str) or len(text)>8192:
            raise ValueError('Invalid bounded checkpoint')
        data = json.loads(text)
        if (not isinstance(data,dict) or set(data)!={'schema','h','weights','count','last'} or
                data['schema']!='finite-context-local-conditioning/1' or data['h']!=str(self.h) or
                not isinstance(data['weights'],list) or len(data['weights'])!=8 or
                any(not isinstance(w,str) or len(w)>800 for w in data['weights'])):
            raise ValueError('Checkpoint schema or candidate mismatch')
        memory = Memory(tuple(F(w) for w in data['weights']),data['count'],data['last'])
        self.memory = memory

    def solve_factors(self,factors,edges):
        net = kernel.Network([kernel.Factor(tuple(f['scope']),f['values']) for f in factors],edges)
        result = net.settle(schedule=self.schedule,max_sweeps=32)
        if not qualify(net,result):
            raise ValueError('Unqualified structural solve')
        return [{'scope':f.scope,'values':dict(f.values)} for f in result.beliefs]


def discard_dependence(memory):
    marginals = [[sum(w for bits,w in zip(BITS,memory.weights) if bits[i]==v) for v in (0,1)] for i in range(3)]
    weights = tuple(marginals[0][a]*marginals[1][b]*marginals[2][c] for a,b,c in BITS)
    return Memory(weights,memory.count,memory.last)
