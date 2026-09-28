"""Adversarial regressions for the challenge scorer, not capability promotion."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import unittest
from unittest.mock import patch

from contract import Candidate, Unsupported, import_file
import challenges as c

kernel = import_file(Path(__file__).resolve().parent.parent / 'cadence-flagship/experiments/local-observer-repair/kernel.py', 'battery_challenge_test_kernel')


class LocalCandidate(Candidate):
    def __init__(self):
        self.calls = 0

    def solve_factors(self, factors, edges):
        self.calls += 1
        result = kernel.Network([kernel.Factor(f['scope'], f['values']) for f in factors], edges).settle()
        if not result.converged or result.message_residual or result.edge_residual:
            raise ValueError('Unqualified test candidate')
        return [{'scope': f.scope, 'values': dict(f.values)} for f in result.beliefs]


class ChallengeTests(unittest.TestCase):
    def test_grouped_holonomy_calls_same_candidate_and_rejects_zero_support(self):
        candidate = LocalCandidate()
        result = c.holonomy_grouped(lambda: candidate)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['metrics']['exact_unequal_probability'], '9/14')
        self.assertEqual(candidate.calls, 2)

    def test_soft_answer_cannot_hide_failure_to_reject_hard_contradiction(self):
        class FalseConflict(LocalCandidate):
            def solve_factors(self, factors, edges):
                if not any(factors[0]['values'].values()):
                    return []
                return super().solve_factors(factors, edges)
        self.assertEqual(c.holonomy_grouped(FalseConflict)['status'], 'FAIL')

    def test_joint_separator_reciprocity_and_relabeling_use_candidate(self):
        candidate = LocalCandidate()
        result = c.federation_joint_separator(lambda: candidate)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(candidate.calls, 4)
        self.assertEqual(result['metrics']['compression_error'], '1/8')

    def test_uniform_beliefs_do_not_pass_joint_checks(self):
        class Uniform(Candidate):
            def solve_factors(self, factors, edges):
                return [{'scope': f['scope'], 'values': {a: F(1, len(f['values'])) for a in f['values']}}
                        for f in factors]
        self.assertEqual(c.holonomy_grouped(Uniform)['status'], 'FAIL')
        self.assertEqual(c.federation_joint_separator(Uniform)['status'], 'FAIL')

    def test_wrong_scope_or_nonexact_values_fail(self):
        supplied = [c.factor(('a',), lambda a: 1)]
        class BadScope(Candidate):
            def solve_factors(self, factors, edges):
                return [{'scope': ('b',), 'values': {(0,): F(1, 2), (1,): F(1, 2)}}]
        class FloatAnswer(Candidate):
            def solve_factors(self, factors, edges):
                return [{'scope': ('a',), 'values': {(0,): .5, (1,): .5}}]
        self.assertFalse(c.checked_beliefs(BadScope(), supplied, []))
        self.assertFalse(c.checked_beliefs(FloatAnswer(), supplied, []))

    def test_unsupported_is_not_reclassified_as_a_pass(self):
        for challenge in (c.holonomy_grouped, c.federation_joint_separator):
            with self.assertRaises(Unsupported):
                challenge(Candidate)

    def test_transition_table_rejects_clipping_duplicate_and_missing_rows(self):
        rows = [{'neuron': n, 'parents': [n], 'current': [a], 'clipped': False,
                 'mean_error': '0', 'high_probability': '1/4'} for n in range(4) for a in (0, 1)]
        self.assertEqual(len(c.transition_factors({'rows': rows})), 5)
        for bad in (rows[:-1], rows + [rows[0]], [dict(rows[0], clipped=True), *rows[1:]]):
            with self.assertRaises(ValueError):
                c.transition_factors({'rows': bad})

    def test_fly_task_calls_candidate_not_reference_answer(self):
        rows = [{'neuron': n, 'parents': [n], 'current': [a], 'clipped': False,
                 'mean_error': '0', 'high_probability': '1/4'} for n in range(4) for a in (0, 1)]
        names = ('rest:intact:pulse=False', 'rest:intact:pulse=True',
                 'rest:source_cut:pulse=False', 'rest:inhibitory_cut:pulse=False')
        fixture = {'models': [{'name': name, 'rows': deepcopy(rows)} for name in names]}
        candidate = LocalCandidate()
        with patch.object(c, 'load_fly_fixture', return_value=(fixture, 'fixture-test-only')):
            result = c.fly_transition_fixture(lambda: candidate)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(candidate.calls, 4)
        self.assertIs(result['metrics']['original_dynamics_preserved'], False)
        with patch.object(c, 'load_fly_fixture', return_value=(fixture, 'fixture-test-only')):
            with self.assertRaises(Unsupported):
                c.fly_transition_fixture(Candidate)


if __name__ == '__main__':
    unittest.main()
