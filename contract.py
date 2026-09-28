"""Minimal harness interface; an adapter must not supply answers for its model."""
from pathlib import Path
import importlib.util
import sys


class Unsupported(Exception):
    """The unchanged candidate cannot perform this test's declared operation."""


class ProbeFailure(Exception):
    """A completed, well-formed candidate operation failed a task requirement."""
    def __init__(self, message, metrics=None):
        super().__init__(message)
        self.metrics = metrics or {}


class Candidate:
    def observe(self, event, value, *, kind='witness', budget=256):
        raise Unsupported('No witnessed streaming operation')

    def query(self):
        raise Unsupported('No scalar belief query')

    def snapshot(self):
        raise Unsupported('No persistent checkpoint')

    def restore(self, state):
        raise Unsupported('No persistent checkpoint restore')

    def observer_intervention(self):
        raise Unsupported('No actual uncertainty readback and feedback interface')

    def solve_factors(self, factors, edges):
        raise Unsupported('No exact finite joint-factor interface')


def import_file(path, name):
    path = Path(path).resolve()
    spec = importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise ValueError('Cannot load candidate source')
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
