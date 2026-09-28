# Candidate qualification battery

**Core replacement: NOT READY. Scaling: LOCKED.**

PASS in a bounded probe does not discharge the full capability. Reference checks are separate.

## normal-gamma-retained/1

Exact conjugate retention with distinct variational readout; scalar stationary model.

| Criterion | Bounded probe | Full criterion |
| --- | --- | --- |
| P1: sensory representation and invariance | NOT_TESTED | NOT_TESTED |
| P2: multisensory binding | NOT_TESTED | NOT_TESTED |
| P3: uncertainty and ambiguity | NOT_TESTED | NOT_TESTED |
| P4: selective attention and active sensing | NOT_TESTED | NOT_TESTED |
| P5: object permanence and latent context | NOT_TESTED | NOT_TESTED |
| T1: order, duration and asynchronous streams | NOT_TESTED | NOT_TESTED |
| T2: ongoing temporal activity | NOT_TESTED | NOT_TESTED |
| M1: working memory | PASS | NOT_TESTED |
| M2: episodic, source and context memory | PASS | NOT_TESTED |
| M3: semantic and relational abstraction | NOT_TESTED | NOT_TESTED |
| M4: procedural learning and habits | NOT_TESTED | NOT_TESTED |
| M5: consolidation, recall and forgetting | NOT_TESTED | NOT_TESTED |
| M6: replay and offline reorganization | NOT_TESTED | NOT_TESTED |
| L1: incidental and associative acquisition | PASS | NOT_TESTED |
| L2: learning from delayed consequences | NOT_TESTED | NOT_TESTED |
| L3: continual adaptation without catastrophic loss | FAIL | FAIL |
| L4: causal world modelling | NOT_TESTED | NOT_TESTED |
| L5: adaptive operating range | NOT_TESTED | NOT_TESTED |
| A1: innate competence and internal drives | NOT_TESTED | NOT_TESTED |
| A2: emotion-like valuation and motivational context | NOT_TESTED | NOT_TESTED |
| A3: smooth embodied control | NOT_TESTED | NOT_TESTED |
| A4: exploration and exploitation | NOT_TESTED | NOT_TESTED |
| A5: goal-directed planning and flexibility | NOT_TESTED | NOT_TESTED |
| O1: composed agreement at multiple scales | NOT_TESTED | NOT_TESTED |
| O2: recursive self-observation | PASS | NOT_TESTED |
| O3: error monitoring and calibrated self-assessment | NOT_TESTED | NOT_TESTED |
| O4: rule abstraction and flexible reasoning | NOT_TESTED | NOT_TESTED |
| O5: social inference, imitation and communication | NOT_TESTED | NOT_TESTED |
| O6: language and symbolic composition | NOT_TESTED | NOT_TESTED |
| O7: imagination and counterfactual construction | NOT_TESTED | NOT_TESTED |
| D1: development and structural adaptation | NOT_TESTED | NOT_TESTED |
| D2: robustness and functional recovery | PASS | NOT_TESTED |
| D3: bounded resources and graceful overload | PASS | NOT_TESTED |
| D4: integrated competence | NOT_TESTED | NOT_TESTED |

| Additional challenge | Result |
| --- | --- |
| fly_directed_transition (CANDIDATE) | UNSUPPORTED |
| holonomy_conflict (CANDIDATE) | UNSUPPORTED |
| federation_joint_boundary (CANDIDATE) | UNSUPPORTED |
| gauge_transport (REFERENCE) | PASS |
| self_observation_reference (REFERENCE) | PASS |
| prior_game_evidence (REFERENCE) | PASS |

Bounded probe details:

- **M1 — PASS:** Same final input after opposite histories; no distractor/delay generalization claim. Metrics: `{"erased_mean": 0.0, "histories": [[-2, -2, -2, 0], [2, 2, 2, 0]], "negative_history": -1.2, "positive_history": 1.2, "queries_preserve_memory": true}`
- **M2 — PASS:** Ordered-source ownership and checkpoint continuation, not episodic recall. Metrics: `{"continuation_equal": true, "rejected_bad_events": 4}`
- **L1 — PASS:** Learning a stationary scalar center; model family and likelihood are supplied. Metrics: `{"attempts": [{"accepted": true, "duplicate": false, "event": 1, "qualified": true, "sweeps": 13, "value": 2}, {"accepted": true, "duplicate": false, "event": 2, "qualified": true, "sweeps": 12, "value": 2}, {"accepted": true, "duplicate": false, "event": 3, "qualified": true, "sweeps": 1, "value": 2}, {"accepted": true, "duplicate": false, "event": 4, "qualified": true, "sweeps": 10, "value": 2}, {"accepted": true, "duplicate": false, "event": 5, "qualified": true, "sweeps": 10, "value": 2}, {"accepted": true, "duplicate": false, "event": 6, "qualified": true, "sweeps": 10, "value": 2}], "learned_error": 0.08163265306122454, "pre_outcome_predictions": [0.0, 1.0, 1.3333333333333333, 1.5, 1.6, 1.6666666666666667], "prior_error": 4.0, "restored_learned": 1.7142857142857142, "restored_prior": 0.0}`
- **L3 — FAIL:** Three phase endpoints must track current regime within0.5; failure is a capability result. Metrics: `{"attempts": [{"accepted": true, "duplicate": false, "event": 1, "qualified": true, "sweeps": 13, "value": -2}, {"accepted": true, "duplicate": false, "event": 2, "qualified": true, "sweeps": 12, "value": -2}, {"accepted": true, "duplicate": false, "event": 3, "qualified": true, "sweeps": 1, "value": -2}, {"accepted": true, "duplicate": false, "event": 4, "qualified": true, "sweeps": 10, "value": -2}, {"accepted": true, "duplicate": false, "event": 5, "qualified": true, "sweeps": 11, "value": 2}, {"accepted": true, "duplicate": false, "event": 6, "qualified": true, "sweeps": 10, "value": 2}, {"accepted": true, "duplicate": false, "event": 7, "qualified": true, "sweeps": 10, "value": 2}, {"accepted": true, "duplicate": false, "event": 8, "qualified": true, "sweeps": 10, "value": 2}, {"accepted": true, "duplicate": false, "event": 9, "qualified": true, "sweeps": 10, "value": -2}, {"accepted": true, "duplicate": false, "event": 10, "qualified": true, "sweeps": 9, "value": -2}, {"accepted": true, "duplicate": false, "event": 11, "qualified": true, "sweeps": 9, "value": -2}, {"accepted": true, "duplicate": false, "event": 12, "qualified": true, "sweeps": 9, "value": -2}], "frozen_prior_control": 0.0, "maximum_allowed_error": 0.25, "phase_means": [-1.6, 0.0, -0.6153846153846154], "pooled_unit_prior_control": [-1.6, 0.0, -0.6153846153846154], "pre_outcome_predictions": [0.0, -1.0, -1.3333333333333333, -1.5, -1.6, -1.0, -0.5714285714285714, -0.25, 0.0, -0.2, -0.36363636363636365, -0.5], "squared_errors": [0.15999999999999992, 4.0, 1.9171597633136093]}`
- **O2 — PASS:** Actual uncertainty readback and reciprocal feedback; no learned observer/depth superiority. Metrics: `{"lesions": {"feedback_cut": {"converged": true, "full_residual": 0.25, "stationarity": 1.0}, "variance_blind": {"converged": true, "full_residual": 0.059259259259259234, "stationarity": 0.9375}}, "lower_delta": -0.09453781512471254, "observer_delta": -0.005381658429517433, "recovery_residual": 3.5493774586115023e-11, "recovery_stationarity": 6.519265127735707e-10}`
- **D2 — PASS:** An unsettled zero-budget event cannot alter witnessed memory; retry can commit. Metrics: `{"rejected": true, "retry_accepted": true, "retry_qualified": true, "unchanged": true}`
- **D3 — PASS:** Bounded24-event fixture:4KiB persistent state and2s elapsed limit; not production throughput. Metrics: `{"attempts": [{"accepted": true, "duplicate": false, "event": 1, "qualified": true, "sweeps": 13, "value": 0}, {"accepted": true, "duplicate": false, "event": 2, "qualified": true, "sweeps": 12, "value": 0}, {"accepted": true, "duplicate": false, "event": 3, "qualified": true, "sweeps": 11, "value": 0}, {"accepted": true, "duplicate": false, "event": 4, "qualified": true, "sweeps": 11, "value": 0}, {"accepted": true, "duplicate": false, "event": 5, "qualified": true, "sweeps": 10, "value": 0}, {"accepted": true, "duplicate": false, "event": 6, "qualified": true, "sweeps": 10, "value": 0}, {"accepted": true, "duplicate": false, "event": 7, "qualified": true, "sweeps": 10, "value": 0}, {"accepted": true, "duplicate": false, "event": 8, "qualified": true, "sweeps": 10, "value": 0}, {"accepted": true, "duplicate": false, "event": 9, "qualified": true, "sweeps": 10, "value": 0}, {"accepted": true, "duplicate": false, "event": 10, "qualified": true, "sweeps": 10, "value": 0}, {"accepted": true, "duplicate": false, "event": 11, "qualified": true, "sweeps": 10, "value": 0}, {"accepted": true, "duplicate": false, "event": 12, "qualified": true, "sweeps": 10, "value": 0}, {"accepted": true, "duplicate": false, "event": 13, "qualified": true, "sweeps": 9, "value": 0}, {"accepted": true, "duplicate": false, "event": 14, "qualified": true, "sweeps": 9, "value": 0}, {"accepted": true, "duplicate": false, "event": 15, "qualified": true, "sweeps": 9, "value": 0}, {"accepted": true, "duplicate": false, "event": 16, "qualified": true, "sweeps": 9, "value": 0}, {"accepted": true, "duplicate": false, "event": 17, "qualified": true, "sweeps": 9, "value": 0}, {"accepted": true, "duplicate": false, "event": 18, "qualified": true, "sweeps": 9, "value": 0}, {"accepted": true, "duplicate": false, "event": 19, "qualified": true, "sweeps": 9, "value": 0}, {"accepted": true, "duplicate": false, "event": 20, "qualified": true, "sweeps": 9, "value": 0}, {"accepted": true, "duplicate": false, "event": 21, "qualified": true, "sweeps": 9, "value": 0}, {"accepted": true, "duplicate": false, "event": 22, "qualified": true, "sweeps": 9, "value": 0}, {"accepted": true, "duplicate": false, "event": 23, "qualified": true, "sweeps": 9, "value": 0}, {"accepted": true, "duplicate": false, "event": 24, "qualified": true, "sweeps": 9, "value": 0}], "elapsed_seconds": 0.00855516700539738, "max_checkpoint_bytes": 98, "overflow_rejected": true, "overflow_unchanged": true}`

Replacement gates: R1 UNSUPPORTED, R2 NOT_TESTED, R3 NOT_TESTED, R4 NOT_TESTED, R5 NOT_TESTED, R6 NOT_TESTED, R7 NOT_TESTED, R8 NOT_TESTED.

## finite-cluster-sum-product/1

Exact finite tree inference; no persistent stream or actual belief-readback interface.

| Criterion | Bounded probe | Full criterion |
| --- | --- | --- |
| P1: sensory representation and invariance | NOT_TESTED | NOT_TESTED |
| P2: multisensory binding | NOT_TESTED | NOT_TESTED |
| P3: uncertainty and ambiguity | NOT_TESTED | NOT_TESTED |
| P4: selective attention and active sensing | NOT_TESTED | NOT_TESTED |
| P5: object permanence and latent context | NOT_TESTED | NOT_TESTED |
| T1: order, duration and asynchronous streams | NOT_TESTED | NOT_TESTED |
| T2: ongoing temporal activity | NOT_TESTED | NOT_TESTED |
| M1: working memory | UNSUPPORTED | UNSUPPORTED |
| M2: episodic, source and context memory | UNSUPPORTED | UNSUPPORTED |
| M3: semantic and relational abstraction | NOT_TESTED | NOT_TESTED |
| M4: procedural learning and habits | NOT_TESTED | NOT_TESTED |
| M5: consolidation, recall and forgetting | NOT_TESTED | NOT_TESTED |
| M6: replay and offline reorganization | NOT_TESTED | NOT_TESTED |
| L1: incidental and associative acquisition | UNSUPPORTED | UNSUPPORTED |
| L2: learning from delayed consequences | NOT_TESTED | NOT_TESTED |
| L3: continual adaptation without catastrophic loss | UNSUPPORTED | UNSUPPORTED |
| L4: causal world modelling | NOT_TESTED | NOT_TESTED |
| L5: adaptive operating range | NOT_TESTED | NOT_TESTED |
| A1: innate competence and internal drives | NOT_TESTED | NOT_TESTED |
| A2: emotion-like valuation and motivational context | NOT_TESTED | NOT_TESTED |
| A3: smooth embodied control | NOT_TESTED | NOT_TESTED |
| A4: exploration and exploitation | NOT_TESTED | NOT_TESTED |
| A5: goal-directed planning and flexibility | NOT_TESTED | NOT_TESTED |
| O1: composed agreement at multiple scales | NOT_TESTED | NOT_TESTED |
| O2: recursive self-observation | UNSUPPORTED | UNSUPPORTED |
| O3: error monitoring and calibrated self-assessment | NOT_TESTED | NOT_TESTED |
| O4: rule abstraction and flexible reasoning | NOT_TESTED | NOT_TESTED |
| O5: social inference, imitation and communication | NOT_TESTED | NOT_TESTED |
| O6: language and symbolic composition | NOT_TESTED | NOT_TESTED |
| O7: imagination and counterfactual construction | NOT_TESTED | NOT_TESTED |
| D1: development and structural adaptation | NOT_TESTED | NOT_TESTED |
| D2: robustness and functional recovery | UNSUPPORTED | UNSUPPORTED |
| D3: bounded resources and graceful overload | UNSUPPORTED | UNSUPPORTED |
| D4: integrated competence | NOT_TESTED | NOT_TESTED |

| Additional challenge | Result |
| --- | --- |
| fly_directed_transition (CANDIDATE) | PASS |
| holonomy_conflict (CANDIDATE) | PASS |
| federation_joint_boundary (CANDIDATE) | PASS |
| gauge_transport (REFERENCE) | PASS |
| self_observation_reference (REFERENCE) | PASS |
| prior_game_evidence (REFERENCE) | PASS |

Bounded probe details:

- **M1 — UNSUPPORTED:** No witnessed streaming operation Metrics: `{}`
- **M2 — UNSUPPORTED:** No witnessed streaming operation Metrics: `{}`
- **L1 — UNSUPPORTED:** No scalar belief query Metrics: `{}`
- **L3 — UNSUPPORTED:** No scalar belief query Metrics: `{}`
- **O2 — UNSUPPORTED:** No witnessed streaming operation Metrics: `{}`
- **D2 — UNSUPPORTED:** No persistent checkpoint Metrics: `{}`
- **D3 — UNSUPPORTED:** No witnessed streaming operation Metrics: `{}`

Replacement gates: R1 NOT_TESTED, R2 NOT_TESTED, R3 UNSUPPORTED, R4 NOT_TESTED, R5 UNSUPPORTED, R6 NOT_TESTED, R7 NOT_TESTED, R8 NOT_TESTED.

## Reference checks

- local-reference-packages: **PASS**. Does not count as selected-candidate evidence.
- prior-game-evidence: **PASS**. Does not count as selected-candidate evidence.
