# One-command candidate battery: complete catalogue, explicit coverage

This is a local development screen, frozen before its own battery execution.
It reports every one of the 34 entries in the
[capability register](../plan/CADENCE_CAPABILITY_AND_PROOF_REGISTER.md)
and every R1–R8 replacement gate. It does **not** implement 34 complete
capability tests. The initial adapters expose a few bounded mechanisms; a
missing interface or test remains visible. Existing scalar and game results
have been seen, so replaying these diagnostic fixtures is not fresh held-out
confirmation.

`criteria.json` is the machine-readable catalogue. Its exact IDs and titles
match the register. Each entry includes a small task, falsifier, required
evidence axes, test key or null, and coverage boundary. The runner and adapter
sources must be pinned with this file and the catalogue before producing an
outcome. No result may be manufactured from the wording of a criterion.

## One invocation, several distinct kinds of evidence

The runner accepts a named, versioned candidate adapter. It emits all 34
criterion rows, the separate challenge rows, and all eight readiness rows in
one receipt. It runs small independent checks with two local workers by default.
It must not
substitute a different candidate when the selected one lacks an interface.

From the workspace root:

```sh
python3 cadence-candidate-test-suite/run.py --all --out /tmp/candidate-battery.json
python3 cadence-candidate-test-suite/run.py --all --verify /tmp/candidate-battery.json
```

`--candidate normal-gamma` and `--candidate finite-cluster` select one adapter;
`--all` runs each separately and never stitches their results into one brain.
`--jobs 1` uses a single local worker. `--no-references` omits the reference
replays and records that omission. The default references are the nine existing
small packages plus the preserved game-arithmetic verifier, when available.
Their actual source identities and individual results are recorded.

Two execution modes are distinct:

- **CANDIDATE:** invoke the selected candidate's real operations on the frozen
  task and compare its result with an independent task oracle or control.
- **REFERENCE:** verify an existing source-bound reference package. A reference
  pass belongs to that package and cannot close a selected-candidate gap.

The retained Normal–Gamma candidate may expose history, source ownership,
scalar acquisition, switching, actual belief readback, cap rollback and bounded
storage. Its conjugate factor accumulation and variational readout are distinct
executed operations. The finite cluster candidate has a different interface
and mathematical domain. Its exact inference cannot supply the Normal–Gamma
candidate's missing capability, or vice versa. Do not combine the two into a
single successful architecture card.

## Status and coverage are separate fields

Every attempted probe uses exactly one status:

| Status | Meaning |
| --- | --- |
| `PASS` | The actual named local task met its frozen checks; display its scope. |
| `FAIL` | A completed candidate execution violated a declared task requirement. |
| `UNSUPPORTED` | The selected candidate has no declared interface/representation for this defined test. No substitute computation is attributed to it. |
| `NOT_TESTED` | A harness or complete bounded protocol is not implemented, or a declared optional reference was not requested/available. |
| `ERROR` | Unexpected exception, source drift, malformed output, missing required dependency or process deadline. Retain the error and attempted work. |

A deliberately capped negative control can help a rollback probe pass if the
candidate rejects admission correctly. It does not turn the capped solve into
a successful equilibrium. A wrong answer is `FAIL`, not an infrastructure
`ERROR`. An unsupported candidate interface is not evidence that every possible
implementation of its mathematical family must fail.

Each criterion has both `probe_status` and `criterion_status` (or equivalent
clearly separate fields). A `bounded_slice` probe pass cannot produce a full
criterion pass. All catalogue entries initially have `full_contract_ready:
false`; a successful slice therefore leaves broader capability `NOT_TESTED`.
A tested necessary-condition `FAIL`, `ERROR` or `UNSUPPORTED` may also be shown
at criterion level, always with the limited tested scope. It is not a universal
impossibility claim about the architecture family. A future
full-criterion `PASS` requires a versioned complete bounded contract, all its
required evidence axes, and explicit review. Removing a failed subtest or
renaming its scope after seeing outcomes requires a new protocol revision and
preservation of the earlier result.

Always show unsupported, untested and error rows. Do not print a percentage of
"brain capabilities achieved" from partial probes or exclude missing rows
from the denominator. Seven slice passes would mean seven small checks passed,
not seven of the 34 broad capabilities discharged. D4 cannot pass merely
because independent fixtures each pass on fresh objects.

## Initial bounded scalar probes

These are diagnostic interface tests for candidates that actually support
the required observations and readouts. No adapter may implement the answer
in a task-specific wrapper. An oracle calculates expected values independently
and never supplies them to the candidate. Except for explicit continuation
tests, separate tasks start with fresh candidate instances of the same frozen
version/configuration. All evidence IDs and input values are recorded.

| Key / catalogue slice | Frozen local task and acceptance boundary | Excluded broader claim |
| --- | --- | --- |
| `m1_history` / M1 | Admit `[-2,-2,-2,0]` and `[2,2,2,0]` in separate instances. Query without a new event; negative-history prediction must be below -0.5 and positive-history prediction above +0.5. Repeated queries preserve persistent bytes. Compare a last-observation-only/erased-memory control. | Ordered item recall, distraction resistance or arbitrary working-memory duration. |
| `m2_source_ownership` / M2 | Exercise valid ordered witnesses, the latest identical retry, conflicting reuse, an older/skipped ID, a hypothetical/derived record, and snapshot/restore continuation. Check no duplicate/new fictitious evidence, proper rejection and unchanged persistent state on invalid calls. | General asynchronous/distributed deduplication, episodic retrieval or delayed action credit. |
| `l1_scalar_acquisition` / L1 | Record target-free predictions while admitting six constant `+2` observations. Final squared prediction error must be less than one quarter of the frozen-prior control, with finite admitted states; restore the original memory and reinstate the learned memory to recover their responses. Count every actual event once. | Learned relational organization, novel task transfer or the one-executed-rule requirement. |
| `l3_context_switch` / L3 | Admit four `-2`, four `+2`, four `-2` values, without providing phase/context IDs to the candidate. Record predictions before outcomes and at the three block endpoints. Require endpoint absolute error at most 0.5 in each block; report acquisition, B-switch and A-return separately, with pooled/frozen controls. | This narrow necessary switching test does not by itself establish context-specific retention, recall or general continual learning. The known pooled candidate is expected to fail; preserve that result. |
| `o2_belief_readback` / O2 | At a qualified, nontrivial posterior, perturb actual lower uncertainty by `+0.05` and observer precision by `+0.1` separately. Each corresponding opposite-side proposal must change by more than `1e-7`; intact repair must meet its own original residual/stationarity contract, without new evidence. Cut the relevant ports and distinguish altered-model solutions from original-model qualification. | Learned observer formation, useful added depth, generic metacognition or a unified retained-learning rule. |
| `d2_cap_rollback` / D2 | Force an unsettled event to exhaust a zero-round repair budget. No durable state or accepted-event cursor may commit. Retry that same event at the unchanged normal budget; one valid admission may commit exactly once. | General neural lesion tolerance, noisy-body adaptation or robust arbitrary composition. |
| `d3_bounded_resources` / D3 | Exercise the adapter's declared finite event capacity and reject its first overflow without mutation. Record actual serialized persistent bytes, all repair attempts/sweeps and process time. The initial scalar fixture permits at most 24 witnesses, 4,096 serialized bytes, a 2-second measured 24-event sample and the separate 10-second task-process cap. | Production p99, asynchronous queue overload, bounded memory for arbitrary dimensions or real-time body control. |

The normal-gamma adapter retains its previously declared prior, integer witness
domain, solver tolerance/stationarity limits and 256-sweep cap. Do not loosen
those gates to make this battery pass. Its posterior center, exact uncertainty
and approximate variational uncertainty must remain distinct. The fixed
readback perturbations above concern its actual live uncertainty/precision,
not a cosmetic activity signal.

These scalar thresholds are fixed diagnostic choices for the initial battery,
not evolved parameters, biological constants or unseen confirmation targets.
Other candidates may be unsupported. A different interface or threshold is a
separate versioned protocol, not silent task coercion.

## Separate challenge fixtures

Challenge results are useful mechanism tests, not automatic P2/O1/O2 or other
full-capability passes. Every challenge record identifies the selected
candidate or reference, input/model hash, changed assumptions, mode, status,
numerical checks and limitations.

1. **`fly_directed_transition`:** use the preserved tiny directed transition
   fixture and its declared oracle. Solving that transformed discrete model
   does not show preservation of the imported continuous rate dynamics,
   whole-connectome behavior, innate food seeking or biological function.
2. **`holonomy_conflict`:** use the contradictory finite parity-loop fixture.
   Preserve semantic frustration while accurately solving the model. Low
   repair residual is not satisfaction of every inconsistent constraint.
3. **`federation_joint_boundary`:** compare the same finite model monolithically
   and through an exact joint boundary, including an outside intervention and
   a deliberately lossy marginal-only summary. No learned boundary is claimed.
4. **`gauge_transport`:** initially reference-only: relabel states, factors and
   ports together, retaining corresponding observable probabilities.
5. **`self_observation_reference`:** optionally verify the preserved readback
   package. It remains evidence about that package's supplied model.
6. **`prior_game_evidence`:** optionally run the existing small arithmetic
   verifier for retained 1942/C64/Atari sources. Do not launch games, training,
   download archives or imply new-candidate game competence.

Candidate-specific challenge inputs and acceptance checks must be explicit in
the frozen runner/adapter source. The existing local-brain verification runner
may verify its preserved package set when requested; the actual list and hashes
are recorded rather than a hard-coded promise about how many packages exist.
Historical source drift or missing local inputs stays visible. Never regenerate
an old receipt to match current code merely to obtain a green reference row.

## Replacement and scale gates cannot be inferred from test totals

R1–R8 are separate `review_only` records, initially `NOT_TESTED`. The runner can
collect supporting evidence and explicit limitations, but cannot invent a
theorem, migration audit, platform qualification or independent review.
An adapter's declared lack of one executed law may mark R1 `UNSUPPORTED` for
that candidate, with the exact reason; it is not a universal falsification of
the architecture hypothesis. It cannot mark R1 `PASS` from an adapter flag.

`core_replacement_ready` remains false unless **one versioned candidate** has:

- all 34 complete required bounded contracts and their distinct evidence axes;
- all R1–R8 gates reviewed with linked artifacts;
- a complete tested inventory for retiring the current APIs and checkpoints;
- an explicit independent readiness decision bound to those exact sources.

The [all-34 pre-scale gate](../plan/CADENCE_LOCAL_FIRST_FLY_GATES_2026-09-28.md)
is unchanged. A pass in expressibility, inference arithmetic or conformance
does not establish learned capability or useful integrated performance. A
candidate may be useful within a narrow domain without satisfying replacement.

## Resource, failure and receipt contract

Run locally with two task workers by default: no cloud, no large dataset, no
model training campaign and no network fetch. Each candidate-task child has a
10-second deadline and at most 8 KiB captured output. Reference children run
sequentially with a 60-second deadline and 64 KiB output limit. Terminate the
child's process group on a deadline or output-limit failure. Generated artifacts
stay below 1 MB for this battery. Report total elapsed time and attempted work
without presenting them as a comparative speed benchmark.

Freeze the catalogue, protocol, harness, adapters and consumed candidate/test
sources before the run. Check source hashes again at completion. The receipt
records every catalogue/challenge/readiness row even if another case fails;
an unrecoverable top-level error produces an explicit partial receipt with
remaining rows `NOT_TESTED`. `--verify` must be read-only, refuse source/body
drift, reconstruct the row set and status/coverage/readiness logic, and never
silently reinterpret an old receipt. Receipt creation refuses overwrite.

Exit code 2 means an execution-integrity `ERROR` or a failed reference check;
exit code 0 can mean a cleanly executed report containing expected capability
`FAIL` or `UNSUPPORTED` results. It does not mean all capabilities passed.
Display counts by status for each candidate and print replacement readiness
false prominently. No automatic retry, parameter change or longer budget
follows from a negative result.
