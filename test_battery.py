"""Harness integrity regressions; synthetic probe verdicts are not science results."""
from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import battery
from contract import Unsupported


def evidence(status='PASS', **metrics):
    return {'status': status, 'detail': 'synthetic scorer fixture', 'metrics': metrics}


class InventoryTests(unittest.TestCase):
    def test_exact_complete_inventory(self):
        spec = battery.registry()
        self.assertEqual(len(spec['criteria']), 34)
        self.assertEqual(len({r['id'] for r in spec['criteria']}), 34)
        self.assertEqual(len(spec['readiness_gates']), 8)

    def test_missing_duplicate_and_substituted_inventory_rejected(self):
        original = battery.registry()
        mutants = []
        missing = deepcopy(original)
        missing['criteria'].pop()
        mutants.append(missing)
        duplicate = deepcopy(original)
        duplicate['criteria'][-1] = deepcopy(duplicate['criteria'][0])
        mutants.append(duplicate)
        substituted = deepcopy(original)
        substituted['criteria'][0]['id'] = 'P99'
        mutants.append(substituted)
        missing_gate = deepcopy(original)
        missing_gate['readiness_gates'].pop()
        mutants.append(missing_gate)
        duplicate_gate = deepcopy(original)
        duplicate_gate['readiness_gates'].append(deepcopy(duplicate_gate['readiness_gates'][0]))
        mutants.append(duplicate_gate)
        with tempfile.TemporaryDirectory() as folder:
            here = Path(folder)
            for index, data in enumerate(mutants):
                with self.subTest(mutation=index):
                    (here/'criteria.json').write_text(json.dumps(data))
                    with patch.object(battery, 'HERE', here), self.assertRaises(ValueError):
                        battery.registry()

    def test_partial_pass_never_becomes_complete_criterion(self):
        criteria = [{'id': 'P1', 'title': 'fixture', 'test_key': 'probe',
                     'scope': 'one bounded slice', 'coverage': 'bounded_slice',
                     'full_contract_ready': True}]
        row = battery.assess(criteria, {'probe': evidence()})[0]
        self.assertEqual(row['probe_status'], 'PASS')
        self.assertEqual(row['criterion_status'], 'NOT_TESTED')
        self.assertIs(row['full_contract_ready'], False)

    def test_absence_unsupported_failure_and_error_stay_distinct(self):
        criteria = [{'id': str(i), 'title': status, 'test_key': status}
                    for i, status in enumerate(('missing', 'UNSUPPORTED', 'FAIL', 'ERROR'))]
        rows = battery.assess(criteria, {s: evidence(s) for s in ('UNSUPPORTED', 'FAIL', 'ERROR')})
        self.assertEqual([r['probe_status'] for r in rows], ['NOT_TESTED', 'UNSUPPORTED', 'FAIL', 'ERROR'])
        self.assertEqual([r['criterion_status'] for r in rows], ['NOT_TESTED', 'UNSUPPORTED', 'FAIL', 'ERROR'])

    def test_all_partial_passes_still_lock_replacement(self):
        selected = Path('/synthetic/selected-adapter.py')
        module = SimpleNamespace(METADATA={'candidate_id': 'synthetic/1', 'scope': 'unit-test fixture',
                                           'declared_unmet_gates': []})
        seen = []
        def child(adapter, key):
            seen.append(adapter)
            return key, evidence()
        with patch.object(battery, 'module_for', return_value=module), \
                patch.object(battery, 'source_bindings', return_value={'selected': 'frozen'}), \
                patch.object(battery, 'child', side_effect=child):
            report = battery.execute(selected, jobs=2)
        self.assertTrue(seen and all(adapter == selected for adapter in seen))
        self.assertEqual(len(report['criteria']), 34)
        self.assertTrue(all(r['criterion_status'] == 'NOT_TESTED' for r in report['criteria']))
        self.assertIs(report['all34_full_contracts_passed'], False)
        self.assertIs(report['core_replacement_ready'], False)
        self.assertEqual(report['scaling'], 'LOCKED')
        self.assertEqual({r['status'] for r in report['readiness_gates']}, {'NOT_TESTED'})

    def test_source_drift_aborts_candidate_report(self):
        module = SimpleNamespace(METADATA={'candidate_id': 'synthetic/1', 'scope': 'unit-test fixture'})
        with patch.object(battery, 'module_for', return_value=module), \
                patch.object(battery, 'source_bindings', side_effect=[{'source': 'before'}, {'source': 'after'}]), \
                patch.object(battery, 'child', side_effect=lambda adapter, key: (key, evidence())), \
                self.assertRaisesRegex(ValueError, 'changed during evaluation'):
            battery.execute(Path('/synthetic/adapter.py'))


class WorkerTests(unittest.TestCase):
    def call(self, function):
        module = SimpleNamespace(create=lambda: object())
        with patch.dict(battery.probes.TESTS, {'scorer-fixture': function}), \
                patch.object(battery, 'module_for', return_value=module):
            return battery.worker(Path('/synthetic/adapter.py'), 'scorer-fixture')

    def test_unsupported_is_distinct_from_invalid_state(self):
        def unsupported(factory):
            raise Unsupported('no such candidate operation')
        def invalid(factory):
            raise ValueError('invalid candidate state')
        self.assertEqual(self.call(unsupported)['status'], 'UNSUPPORTED')
        result = self.call(invalid)
        self.assertEqual(result['status'], 'ERROR')
        self.assertIn('invalid candidate state', result['detail'])

    def test_unknown_probe_is_explicitly_not_tested(self):
        result = battery.worker(Path('/unused/adapter.py'), 'not-a-real-probe')
        self.assertEqual(result['status'], 'NOT_TESTED')

    def test_bad_status_nonfinite_and_nonserializable_evidence_are_errors(self):
        for result in (evidence('GREAT'), evidence(answer=float('nan')),
                       evidence(answer=float('inf')), evidence(answer=object())):
            with self.subTest(result=result):
                self.assertEqual(self.call(lambda factory: result)['status'], 'ERROR')

    def test_child_nonzero_or_invalid_payload_cannot_pass(self):
        for text, code in ((json.dumps(evidence()), 7), ('not json', 0),
                           (json.dumps(evidence('UNKNOWN')), 0)):
            with self.subTest(code=code, text=text), \
                    patch.object(battery, 'run_bounded', return_value=(text, code)):
                key, result = battery.child(Path('/synthetic/adapter.py'), 'fixture')
                self.assertEqual(key, 'fixture')
                self.assertEqual(result['status'], 'ERROR')

    def test_child_timeout_is_error_not_skipped(self):
        with patch.object(battery, 'run_bounded', side_effect=TimeoutError('fixture deadline')):
            self.assertEqual(battery.child(Path('/synthetic/adapter.py'), 'fixture')[1]['status'], 'ERROR')


class ProcessContainmentTests(unittest.TestCase):
    def test_nonzero_return_preserves_diagnostics(self):
        text, code = battery.run_bounded([sys.executable, '-c', 'print("fixture"); raise SystemExit(7)'])
        self.assertEqual((text, code), ('fixture\n', 7))

    def test_output_limit_rejects_excess(self):
        with self.assertRaisesRegex(ValueError, 'output limit'):
            battery.run_bounded([sys.executable, '-c', 'print("x"*4096)'], max_output=128)

    def test_sleeping_child_is_killed_at_deadline(self):
        with self.assertRaises((TimeoutError, subprocess.TimeoutExpired)):
            battery.run_bounded([sys.executable, '-c', 'import time; time.sleep(2)'], timeout=.05)

    def test_closed_output_does_not_escape_deadline(self):
        with self.assertRaises((TimeoutError, subprocess.TimeoutExpired)):
            battery.run_bounded([sys.executable, '-c', 'import os,time; os.close(1); os.close(2); time.sleep(2)'], timeout=.05)


class ReplayTests(unittest.TestCase):
    def candidate(self):
        return {'candidate_id': 'synthetic/1', 'adapter': 'synthetic.py', 'scope': 'unit-test fixture',
                'source_sha256': {'model.py': 'unchanged'},
                'criteria': [{'id': 'L3', 'probe_status': 'FAIL', 'criterion_status': 'FAIL',
                              'evidence': evidence('FAIL', answer=.75, elapsed_seconds=.1)}],
                'challenges': [], 'probe_counts': {'FAIL': 1}, 'core_replacement_ready': False,
                'all34_full_contracts_passed': False, 'scaling': 'LOCKED'}

    def report(self):
        return {'schema': 'cadence-candidate-battery/1', 'candidates': [self.candidate()],
                'references': [], 'elapsed_seconds': 99., 'core_replacement_ready': False, 'scaling': 'LOCKED'}

    def replay(self, report):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'report.json'
            path.write_text(json.dumps(report))
            with patch.object(sys, 'argv', ['battery.py', '--no-references', '--verify', str(path)]), \
                    patch.object(battery, 'execute', return_value=self.candidate()), redirect_stdout(io.StringIO()):
                battery.main()

    def test_expected_scientific_failure_replays_without_promotion(self):
        self.replay(self.report())

    def test_only_wall_clock_samples_may_change(self):
        report = self.report()
        report['candidates'][0]['criteria'][0]['evidence']['metrics']['elapsed_seconds'] = 42.
        self.replay(report)
        report['candidates'][0]['criteria'][0]['evidence']['metrics']['answer'] += 1e-12
        with self.assertRaisesRegex(ValueError, 'replay differ'):
            self.replay(report)

    def test_forged_readiness_or_source_identity_rejected(self):
        mutations = []
        ready = self.report()
        ready['core_replacement_ready'] = True
        mutations.append(ready)
        candidate_ready = self.report()
        candidate_ready['candidates'][0]['core_replacement_ready'] = True
        mutations.append(candidate_ready)
        source = self.report()
        source['candidates'][0]['source_sha256']['model.py'] = 'changed'
        mutations.append(source)
        promoted = self.report()
        promoted['candidates'][0]['criteria'][0]['criterion_status'] = 'PASS'
        mutations.append(promoted)
        for report in mutations:
            with self.subTest(report=report), self.assertRaises(ValueError):
                self.replay(report)

    def test_canonical_serialization_refuses_nonfinite_numbers(self):
        with self.assertRaises(ValueError):
            battery.canonical({'answer': float('nan')})


if __name__ == '__main__':
    unittest.main()
