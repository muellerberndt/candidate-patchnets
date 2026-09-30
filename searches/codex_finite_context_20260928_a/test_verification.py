"""Mutation checks for the strict verifier, independent of numerical tests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('context_verification_tests', HERE / 'verify_round.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class VerificationTests(unittest.TestCase):
    def test_boolean_integer_mutation_rejected(self):
        original = {'checks': {'qualified': True}, 'residual': 0}
        mutated = {'checks': {'qualified': 1}, 'residual': False}
        self.assertEqual(original, mutated)  # The original Python-equality trap.
        with self.assertRaises(ValueError):
            verifier.require_identical(original, mutated)

    def test_numeric_type_mutation_rejected(self):
        with self.assertRaises(ValueError):
            verifier.require_identical({'solves': 108}, {'solves': 108.0})

    def test_order_irrelevant_but_values_and_sources_are_not(self):
        verifier.require_identical({'a': [True, 0], 'b': 'hash'}, {'b': 'hash', 'a': [True, 0]})
        with self.assertRaises(ValueError):
            verifier.require_identical({'source': 'abc'}, {'source': 'abd'})

    def test_duplicate_and_nonfinite_json_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'receipt.json'
            for text in ('{"x":true,"x":true}', '{"x":NaN}', '{"x":Infinity}'):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    verifier.read_json(path)

    def test_timing_cannot_be_boolean_or_negative(self):
        for value in (True, -1, float('inf')):
            with self.assertRaises(ValueError):
                verifier.validate_envelope({'elapsed_seconds': value, 'result': {}})
        verifier.validate_envelope({'elapsed_seconds': 1.0, 'result': {}})

    def test_original_check_mutation_rejected(self):
        original = verifier.read_json(HERE / 'search_receipt.json')['result']
        mutated = json.loads(json.dumps(original))
        key = next(iter(mutated['checks']))
        mutated['checks'][key] = 1
        self.assertEqual(original, mutated)
        with self.assertRaises(ValueError):
            verifier.require_identical(original, mutated)


if __name__ == '__main__':
    unittest.main()
