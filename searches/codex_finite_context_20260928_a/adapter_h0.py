from fractions import Fraction as F
from pathlib import Path
from contract import import_file
model = import_file(Path(__file__).with_name('model.py'),'codex_finite_context')
METADATA = {'candidate_id':'finite-context-local-conditioning/1:h=0',
 'source_paths':[str(Path(__file__).with_name('model.py')),str(model.KERNEL_PATH)],
 'declared_unmet_gates':['R4','R5','R6','R7','R8'],
 'scope':'Same exact local factor primitive for scalar retention and structural tasks; supplied binary contexts, no actual uncertainty self-observer.'}
def create():
    return model.Brain(F(0))
