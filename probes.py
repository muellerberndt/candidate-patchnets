"""Shared tasks call candidate ports; reference answers stay in the test runner."""
import math
import time
from contract import ProbeFailure


def outcome(ok,detail,**metrics):
    return {'status':'PASS' if ok else 'FAIL','detail':detail,'metrics':metrics}


def query(candidate):
    result = candidate.query()
    if result.get('qualified') is False:
        raise ProbeFailure('Candidate query did not qualify',{'returned':result})
    if result.get('qualified') is not True or not math.isfinite(result['answer']):
        raise ValueError('Candidate returned an unqualified or nonfinite answer')
    return result['answer']


def feed(candidate,values,start=1):
    attempts = []
    for event,value in enumerate(values,start):
        result = candidate.observe(event,value)
        if result.get('accepted') is not True or result.get('qualified') is not True:
            if type(result.get('accepted')) is bool and type(result.get('qualified')) is bool:
                raise ProbeFailure('Fresh valid witness did not qualify/commit',
                                   {'attempts':attempts+[{'event':event,'value':value,**result}]})
            raise ValueError('Malformed admission flags')
        attempts.append({'event':event,'value':value,**result})
    return attempts


def m1_history(factory):
    results,unchanged = [],True
    for sign in (-1,1):
        candidate = factory()
        feed(candidate,[sign*2]*3+[0])
        results.append(query(candidate))
        snapshot = candidate.snapshot()
        for _ in range(5):
            query(candidate)
        unchanged &= candidate.snapshot()==snapshot
    erased = factory()
    feed(erased,[0])
    erased_mean = query(erased)
    return outcome(results[0]<-.5 and results[1]>.5 and unchanged
                   and abs(erased_mean)<min(abs(x) for x in results),
                   'Same final input after opposite histories; no distractor/delay generalization claim.',
                   negative_history=results[0],positive_history=results[1],
                   erased_mean=erased_mean,queries_preserve_memory=unchanged,
                   histories=[[-2,-2,-2,0],[2,2,2,0]])


def m2_source_ownership(factory):
    candidate = factory()
    feed(candidate,[2,-2,0])
    before = candidate.snapshot()
    for _ in range(5):
        query(candidate)
        retry = candidate.observe(3,0)
        if retry.get('accepted') or retry.get('duplicate') is not True:
            return outcome(False,'Latest witness retry committed twice')
    rejected = 0
    for event,value,kind in [(3,2,'witness'),(2,-2,'witness'),(5,0,'witness'),(4,0,'derived')]:
        try:
            candidate.observe(event,value,kind=kind)
        except ValueError:
            rejected += 1
        if candidate.snapshot()!=before:
            return outcome(False,'Bad witness mutated persistent state')
    resumed = factory()
    resumed.restore(before)
    feed(candidate,[2],start=4)
    feed(resumed,[2],start=4)
    return outcome(rejected==4 and candidate.snapshot()==resumed.snapshot(),
                   'Ordered-source ownership and checkpoint continuation, not episodic recall.',
                   rejected_bad_events=rejected,continuation_equal=candidate.snapshot()==resumed.snapshot())


def l1_scalar_acquisition(factory):
    candidate = factory()
    before = query(candidate)
    original = candidate.snapshot()
    predictions,attempts = [],[]
    for event in range(1,7):
        predictions.append(query(candidate))
        attempts.extend(feed(candidate,[2],event))
    after = query(candidate)
    learned = candidate.snapshot()
    candidate.restore(original)
    restored_prior = query(candidate)
    candidate.restore(learned)
    restored_learned = query(candidate)
    old_error,new_error = (before-2)**2,(after-2)**2
    return outcome(old_error>0 and new_error < .25*old_error and restored_prior==before and restored_learned==after,
                   'Learning a stationary scalar center; model family and likelihood are supplied.',
                   prior_error=old_error,learned_error=new_error,pre_outcome_predictions=predictions,
                   restored_prior=restored_prior,restored_learned=restored_learned,attempts=attempts)


def l3_context_switch(factory):
    candidate = factory()
    frozen = query(factory())
    predictions,attempts,endpoints,pooled = [],[],[],[]
    values = [-2]*4+[2]*4+[-2]*4
    for event,value in enumerate(values,1):
        predictions.append(query(candidate))
        attempts.extend(feed(candidate,[value],event))
        if event%4==0:
            endpoints.append(query(candidate))
            pooled.append(sum(values[:event])/(event+1))
    a,b,restored = endpoints
    errors = [(a+2)**2,(b-2)**2,(restored+2)**2]
    return outcome(max(errors)<=.25,
                   'Three phase endpoints must track current regime within0.5; failure is a capability result.',
                   phase_means=[a,b,restored],squared_errors=errors,maximum_allowed_error=.25,
                   pre_outcome_predictions=predictions,attempts=attempts,
                   pooled_unit_prior_control=pooled,frozen_prior_control=frozen)


def o2_belief_readback(factory):
    candidate = factory()
    feed(candidate,[-2,2,-2])
    before = candidate.snapshot()
    result = candidate.observer_intervention()
    values = [result[k] for k in ('observer_before','observer_after','lower_before','lower_after','recovered_residual')]
    if not all(math.isfinite(x) for x in values):
        raise ValueError('Nonfinite intervention trace')
    bottom = result['observer_after']-result['observer_before']
    top = result['lower_after']-result['lower_before']
    ok = (abs(bottom)>1e-7 and abs(top)>1e-7 and result['recovered_qualified'] is True
          and result['recovered_residual']<=1e-10 and result['recovered_stationarity']<=1e-8
          and candidate.snapshot()==before and len(result['lesions'])==2
          and all(r['converged'] is True and r['full_residual']>1e-7 and r['stationarity']>1e-7
                  for r in result['lesions'].values()))
    return outcome(ok,'Actual uncertainty readback and reciprocal feedback; no learned observer/depth superiority.',
                   observer_delta=bottom,lower_delta=top,recovery_residual=result['recovered_residual'],
                   recovery_stationarity=result['recovered_stationarity'],lesions=result['lesions'])


def d2_cap_rollback(factory):
    candidate = factory()
    before = candidate.snapshot()
    result = candidate.observe(1,-2,budget=0)
    rejected = result.get('accepted') is False and result.get('qualified') is False
    unchanged = candidate.snapshot()==before
    retry = candidate.observe(1,-2)
    return outcome(rejected and unchanged and retry.get('accepted') is True and retry.get('qualified') is True,
                   'An unsettled zero-budget event cannot alter witnessed memory; retry can commit.',
                   rejected=rejected,unchanged=unchanged,retry_accepted=retry.get('accepted'),
                   retry_qualified=retry.get('qualified'))


def d3_bounded_resources(factory):
    candidate = factory()
    started = time.monotonic()
    sizes,attempts = [],[]
    for event in range(1,25):
        attempts.extend(feed(candidate,[0],event))
        sizes.append(len(candidate.snapshot().encode('utf-8')))
    rejected = False
    before_overflow = candidate.snapshot()
    try:
        candidate.observe(25,0)
    except ValueError:
        rejected = True
    elapsed = time.monotonic()-started
    unchanged = candidate.snapshot()==before_overflow
    return outcome(max(sizes)<=4096 and elapsed<=2 and rejected and unchanged,
                   'Bounded24-event fixture:4KiB persistent state and2s elapsed limit; not production throughput.',
                   max_checkpoint_bytes=max(sizes),elapsed_seconds=elapsed,overflow_rejected=rejected,
                   overflow_unchanged=unchanged,attempts=attempts)


TESTS = {f.__name__:f for f in (m1_history,m2_source_ownership,l1_scalar_acquisition,l3_context_switch,
                              o2_belief_readback,d2_cap_rollback,d3_bounded_resources)}
