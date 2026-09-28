"""Small supplied-coordinate witness families shared by current-source checks.

These are deterministic diagnostic tasks, not raw perception, reinforcement
learning, unseen scientific confirmation, or models of biological acquisition.
"""

from itertools import product
from math import tanh


def make_fixture(name):
    """Return independent JSON-safe teaching, check and assessment rows."""
    if name not in ("scalar", "mixing", "nonlinear"):
        raise ValueError("Unknown fixture family")
    if name == "mixing":
        inputs = list(product((-0.8, 0.0, 0.8), repeat=2))
        checks = list(product((-0.4, 0.4), repeat=2)) + [
            (-0.6, 0.2), (0.6, -0.2), (-0.2, -0.6), (0.2, 0.6)
        ]
        assessments = list(product((-0.5, -0.3, 0.3, 0.5), repeat=2))

        def relation(x):
            return [0.45 * x[0] + 0.25 * x[1], 0.2 * x[0] - 0.5 * x[1]]
    else:
        inputs = [(x,) for x in (-0.8, 0.8, -0.4, 0.4)]
        checks = [(x,) for x in (-0.6, 0.6, -0.2, 0.2)]
        assessments = [(x,) for x in (-0.5, 0.5, -0.3, 0.3)]

        def relation(x):
            return [0.6 * x[0] if name == "scalar" else tanh(1.2 * x[0])]

    def rows(values):
        return [
            {"inputs": {"signal": list(x)}, "targets": {"answer": relation(x)}}
            for x in values
        ]

    return {
        "name": name,
        "input_size": len(inputs[0]),
        "output_size": len(relation(inputs[0])),
        "teaching": rows(inputs),
        "checks": rows(checks),
        "assessments": rows(assessments),
        "scope": "Supplied normalized coordinates and immediate supervised witnesses; no delayed reward, sensory encoder or body controller.",
    }
