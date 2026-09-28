"""Fault-injection regressions for the declared bounded candidate probes."""
import unittest
from pathlib import Path

from contract import import_file
import probes
import battery

adapter = import_file(Path(__file__).resolve().parent/'adapters/normal_gamma.py','probe_test_adapter')


class ProbeTests(unittest.TestCase):
    def test_known_context_failure_is_not_a_runner_success_claim(self):
        result = probes.l3_context_switch(adapter.create)
        self.assertEqual(result['status'],'FAIL')
        self.assertEqual(result['metrics']['phase_means'][1],0)
        self.assertEqual(len(result['metrics']['pre_outcome_predictions']),12)
        self.assertEqual(len(result['metrics']['attempts']),12)

    def test_query_memory_drift_fails_history_probe(self):
        class Drift(adapter.Adapter):
            calls = 0
            def query(self):
                self.calls += 1
                return super().query()
            def snapshot(self):
                return super().snapshot()+str(self.calls)
        self.assertEqual(probes.m1_history(Drift)['status'],'FAIL')

    def test_constant_answer_is_not_learning(self):
        class Constant(adapter.Adapter):
            def query(self):
                return {'qualified':True,'answer':2.}
        self.assertEqual(probes.l1_scalar_acquisition(Constant)['status'],'FAIL')

    def test_neutral_or_forged_port_cut_does_not_pass(self):
        class NeutralCut(adapter.Adapter):
            def observer_intervention(self):
                result = super().observer_intervention()
                result['lesions']['variance_blind']['full_residual'] = 0.
                return result
        self.assertEqual(probes.o2_belief_readback(NeutralCut)['status'],'FAIL')

    def test_overflow_must_not_mutate_snapshot(self):
        class MutatingOverflow(adapter.Adapter):
            extra = ''
            def observe(self,event,value,**kwargs):
                if event==25:
                    self.extra = 'BAD'
                return super().observe(event,value,**kwargs)
            def snapshot(self):
                return super().snapshot()+self.extra
        self.assertEqual(probes.d3_bounded_resources(MutatingOverflow)['status'],'FAIL')

    def test_partial_error_preserves_complete_inventory(self):
        report = battery.partial_report(Path('/missing/adapter.py'),ValueError('bad source'))
        self.assertEqual(len(report['criteria']),34)
        self.assertEqual(len(report['readiness_gates']),8)
        self.assertTrue(all(r['probe_status']=='NOT_TESTED' for r in report['criteria']))
        self.assertIn('bad source',report['execution_error'])
        self.assertFalse(report['core_replacement_ready'])

    def test_unqualified_retry_does_not_pass_rollback(self):
        class BadRetry(adapter.Adapter):
            def observe(self,event,value,**kwargs):
                result = super().observe(event,value,**kwargs)
                if kwargs.get('budget',256)>0:
                    result['qualified'] = False
                return result
        self.assertEqual(probes.d2_cap_rollback(BadRetry)['status'],'FAIL')

    def test_omitted_failure_flags_do_not_pass_rollback(self):
        class MissingFlags(adapter.Adapter):
            def observe(self,event,value,**kwargs):
                if kwargs.get('budget')==0:
                    return {}
                return super().observe(event,value,**kwargs)
        self.assertEqual(probes.d2_cap_rollback(MissingFlags)['status'],'FAIL')

    def test_reference_cannot_promote_candidate(self):
        report = battery.partial_report(Path('/missing/adapter.py'),ValueError('bad source'))
        before = [r['probe_status'] for r in report['criteria']]
        battery.attach_references([report],[{'id':'local-reference-packages','status':'PASS'}])
        self.assertEqual([r['probe_status'] for r in report['criteria']],before)
        self.assertTrue(all(r['evidence']['status']=='NOT_TESTED' for r in report['challenges']
                            if r['execution_mode']=='CANDIDATE'))
        self.assertFalse(report['core_replacement_ready'])


if __name__=='__main__':
    unittest.main()
