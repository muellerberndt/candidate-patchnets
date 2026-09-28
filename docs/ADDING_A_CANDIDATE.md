# Add one candidate without changing the tests

Write a local Python module exporting `METADATA` and `create()`. The adapter
only translates calls and results. It must not answer using the test oracle,
swap to another brain, add task-specific learning, or silently turn repair
failures into successful outputs. An unavailable operation raises
`contract.Unsupported`; an invalid event should be rejected by the candidate.

```python
from contract import Candidate

METADATA = {
    "candidate_id": "my-repair-rule/1",
    "source_paths": ["/absolute/path/to/my_implementation.py"],
    "declared_unmet_gates": [],
    "scope": "Precisely state the supported equations and boundaries.",
}

class Adapter(Candidate):
    # Implement only operations the unchanged candidate actually provides.
    pass

def create():
    return Adapter()
```

Run it from the workspace:

```sh
python3 cadence-candidate-test-suite/run.py --adapter /path/to/adapter.py --out /tmp/my-candidate.json
```

The empty example correctly reports unsupported implemented probes. It does
not pass because it avoided exceptions. Naming no unmet gates in metadata
also does not certify any gate; proof and independent review remain necessary.

## Initial operation contract

| Operation | Required behavior |
| --- | --- |
| `observe(event,value,kind='witness',budget=256)` | Process one ordered real event. Return `accepted`, `qualified`, `duplicate`; preserve ownership and reject invalid/derived events. A failed admission cannot mutate committed memory. |
| `query()` | Return the candidate's actual scalar `answer`, with `qualified`; the implemented readback model also reports variance, precision and residual. A query cannot acquire a witness. |
| `snapshot()` / `restore(text)` | Serialize and restore all persistent state needed for the tested continuation, including source ownership. The test compares snapshots around queries, rejected events and resumed execution. |
| `observer_intervention()` | Expose actual lower-uncertainty and observer-precision perturbation proposals, joint recovery qualification and residual. This diagnostic hook needs source review: manufactured numbers cannot demonstrate causal readback. |
| `solve_factors(factors,edges)` | Use the candidate to solve the given binary factor problem. Return the complete normalized beliefs for corresponding clusters or reject an unsupported/contradictory problem. |

Factor specs are neutral dictionaries:

```python
{
    "scope": ("a", "b"),
    "values": {(0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3},
}
```

The initial exact challenges require integer or `Fraction` belief values.
An approximate candidate needs a separately frozen tolerance/calibration
contract; do not convert its rounded floats to fractions and claim exactness.
Likewise, supporting other sensor types or asynchronous events requires a
declared interface, not reinterpretation of these scalar tasks.

## Extend the battery

1. Choose a missing capability from `criteria.json`. Freeze the smallest task,
   allowed information, budget, falsifier, controls and success threshold.
2. State whether it tests a bounded slice or a complete bounded capability
   contract. An informal task name is not a theorem or a full capability.
3. Add an independent test function that calls candidate operations. Keep
   answers and controls outside the adapter. Add negative/mutation regressions
   that catch the tempting shortcut.
4. Declare fixture custody and candidate source files. Use deterministic
   cases or frozen seeds. Retain all attempts, including caps and failures.
5. Link its test key in the catalogue; review protocol/source changes before
   producing a new receipt. Preserve earlier receipts rather than updating
   them to make a new candidate look successful.
6. Review combined operation in one persistent candidate. Passing separate
   fresh-instance probes does not establish D4 integration, depth benefit,
   lifelong adaptation or production readiness.

The intended next interfaces cover latent context, structured sensory binding,
counterfactual branches, action/consequence credit and recursive readback.
Those interfaces and complete protocols are still open work, explicitly shown
in the report. Existing exact algebra and rate-model receipts remain in their
original directories; adding an adapter cannot transfer their scientific claims.
