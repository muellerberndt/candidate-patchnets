"""Bind the unchanged retained-observer prototype to shared black-box tests."""
from dataclasses import replace
from pathlib import Path
from contract import Candidate, import_file

SOURCE = Path(__file__).resolve().parents[2]/'cadence-flagship/experiments/retained-observer-probe/model.py'
model = import_file(SOURCE,'battery_normal_gamma_model')
METADATA = {'candidate_id':'normal-gamma-retained/1', 'source_paths':[str(SOURCE)],
            'declared_unmet_gates':['R1'],
            'scope':'Exact conjugate retention with distinct variational readout; scalar stationary model.'}


class Adapter(Candidate):
    def __init__(self):
        self.stream = model.Stream()

    def observe(self,event,value,*,kind='witness',budget=256):
        result = self.stream.observe(event,value,kind=kind,cap=budget)
        return {'accepted':result['committed'],'qualified':result['converged'],
                'duplicate':result['duplicate'],'sweeps':result['sweeps']}

    def query(self):
        result = self.stream.query()
        state = result['state']
        return {'answer':state.mean,'variance':state.variance,'precision':state.precision,
                'qualified':result['converged'],'residual':result['full_residual']}

    def snapshot(self):
        return self.stream.memory.dump()

    def restore(self,state):
        self.stream = model.Stream(model.Memory.restore(state))

    def observer_intervention(self):
        memory = self.stream.memory
        state = self.stream.query()['state']
        observer_before = model.target(memory,state,'precision')
        observer_after = model.target(memory,replace(state,variance=state.variance+.05),'precision')
        lower_before = model.target(memory,state,'variance')
        lower_after = model.target(memory,replace(state,precision=state.precision+.1),'variance')
        recovered = model.settle(memory,replace(state,variance=state.variance+.05),schedule='reverse')
        lesions = {name:model.settle(memory,state,lesion=name) for name in ('variance_blind','feedback_cut')}
        return {'observer_before':observer_before,'observer_after':observer_after,
                'lower_before':lower_before,'lower_after':lower_after,
                'recovered_qualified':recovered['converged'],
                'recovered_residual':recovered['full_residual'],
                'recovered_stationarity':recovered['stationarity'],
                'lesions':{name:{k:r[k] for k in ('converged','full_residual','stationarity')}
                           for name,r in lesions.items()},
                'retained_snapshot':self.snapshot()}


def create():
    return Adapter()
