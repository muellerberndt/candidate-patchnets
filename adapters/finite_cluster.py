"""Use the same frozen local factor kernel for every finite-graph challenge."""
from pathlib import Path
from contract import Candidate, import_file

SOURCE = Path(__file__).resolve().parents[2]/'cadence-flagship/experiments/local-observer-repair/kernel.py'
kernel = import_file(SOURCE,'battery_finite_cluster_kernel')
METADATA = {'candidate_id':'finite-cluster-sum-product/1','source_paths':[str(SOURCE)],
            'declared_unmet_gates':['R3','R5'],
            'scope':'Exact finite tree inference; no persistent stream or actual belief-readback interface.'}


class Adapter(Candidate):
    def solve_factors(self,factors,edges):
        # Accept neutral factor specs; never use a challenge's reference answer.
        local = [kernel.Factor(tuple(f['scope']),dict(f['values'])) for f in factors]
        network = kernel.Network(local,edges)
        result = network.settle(schedule='forward',max_sweeps=32)
        if not result.converged:
            raise ValueError('Candidate did not qualify its tree equations')
        return [{'scope':b.scope,'values':dict(b.values)} for b in result.beliefs]


def create():
    return Adapter()
