from fractions import Fraction as F
from pathlib import Path
import json
import sys
import unittest
from unittest.mock import patch
from types import SimpleNamespace

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from contract import import_file
model=import_file(HERE/'model.py','context_test_model')


class Tests(unittest.TestCase):
    def test_normalized_likelihood_and_neutral_cue(self):
        for bit in (0,1):
            self.assertEqual(sum(model.likelihood(y,bit) for y in range(-8,9)),1)
        self.assertEqual(model.likelihood(0,0),model.likelihood(0,1))

    def test_query_no_evidence_no_time(self):
        brain=model.Brain()
        brain.observe(1,-2)
        before=brain.snapshot()
        for _ in range(3):
            self.assertTrue(brain.query()['qualified'])
        self.assertEqual(before,brain.snapshot())

    def test_failed_admission_and_rejected_events_atomic(self):
        brain=model.Brain()
        before=brain.snapshot()
        self.assertFalse(brain.observe(1,-2,budget=0)['accepted'])
        self.assertEqual(before,brain.snapshot())
        brain.observe(1,-2)
        before=brain.snapshot()
        self.assertTrue(brain.observe(1,-2)['duplicate'])
        for event,value,kind in [(1,2,'witness'),(3,0,'witness'),(2,0,'derived')]:
            with self.assertRaises(ValueError):
                brain.observe(event,value,kind=kind)
            self.assertEqual(before,brain.snapshot())

    def test_checkpoint_invalid_does_not_mutate(self):
        brain=model.Brain()
        brain.observe(1,2)
        before=brain.snapshot()
        data=json.loads(before)
        for key,value in [('weights',['1']*8),('count',True),('last',9),('h','1/4')]:
            changed={**data,key:value}
            with self.assertRaises(ValueError):
                brain.restore(json.dumps(changed))
            self.assertEqual(before,brain.snapshot())

    def test_all_hazards_and_schedules_query_same_law(self):
        for h in (F(0),F(1,16),F(1,4)):
            states=[]
            for schedule in ('forward','reverse','synchronous'):
                brain=model.Brain(h,schedule=schedule)
                for event,y in enumerate([-2,2,-2],1):
                    self.assertTrue(brain.observe(event,y)['accepted'])
                states.append(brain.memory)
            self.assertEqual(states[0],states[1]);self.assertEqual(states[1],states[2])

    def test_forged_success_cannot_commit_bad_messages(self):
        brain=model.Brain()
        network=model.build(brain.memory,brain.h,-2)
        unfinished=network.settle(max_sweeps=0)
        fake=SimpleNamespace(messages=unfinished.messages,beliefs=unfinished.beliefs,
                             converged=True,sweeps=0,updates=0,message_evaluations=0)
        before=brain.snapshot()
        with patch.object(model.kernel.Network,'settle',return_value=fake):
            self.assertFalse(brain.observe(1,-2)['accepted'])
        self.assertEqual(before,brain.snapshot())

    def test_capacity(self):
        brain=model.Brain()
        for event in range(1,25):
            self.assertTrue(brain.observe(event,0)['accepted'])
        before=brain.snapshot()
        with self.assertRaises(ValueError):
            brain.observe(25,0)
        self.assertEqual(before,brain.snapshot())

    def test_correlation_cut_keeps_singleton_marginals(self):
        memory=model.Memory((F(0),F(0),F(1,2),F(0),F(0),F(1,2),F(0),F(0)))
        cut=model.discard_dependence(memory)
        for i in range(3):
            for bit in (0,1):
                self.assertEqual(sum(w for s,w in zip(model.BITS,memory.weights) if s[i]==bit),
                                 sum(w for s,w in zip(model.BITS,cut.weights) if s[i]==bit))

    def test_structural_challenges_use_same_instance_without_memory_loss(self):
        import challenges
        brain=model.Brain()
        brain.observe(1,-2)
        before=brain.snapshot()
        for challenge in challenges.TESTS.values():
            self.assertEqual(challenge(lambda:brain)['status'],'PASS')
            self.assertEqual(brain.snapshot(),before)
        self.assertTrue(brain.observe(2,2)['accepted'])


if __name__=='__main__':
    unittest.main()
