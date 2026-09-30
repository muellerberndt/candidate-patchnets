# Independent mathematical and evidence review

Reviewed on 2026-09-28 by the independent `federation_math` worker. This is an
audit note, not a source-pinned experiment result or a promotion decision. No
candidate source, frozen protocol or scientific receipt was changed in this
review. No files were staged or committed.

The reviewed scientific receipt is `search_receipt.json`, SHA-256
`cb44f16cf9be79fc085d3a56681f05b220400326b3585de87dc7f9686b92f9e5`.
It contains 1,032 true checks and 108 primary event solves. Those counts do not
mean 1,032 independently demonstrated capabilities.

## Mathematical conclusion

The candidate implements the finite conditioning model stated in `THEOREM.md`.
No incorrect posterior equation or future-outcome leakage was found.

- `model.py:45` builds a valid cluster tree. The prior, transition, likelihood
  and deterministic output conditional are each owned once. The output factor
  sums to one over its output, so merely adding this unobserved readout does
  not alter the retained law.
- `model.py:53` independently recomputes the beliefs and the message and
  separator consistency equations before accepting a solver result.
- `model.py:67` obtains the retained eight-cell boundary and output marginal
  from qualified cluster beliefs. It does not call the direct filtering
  oracle used by the probe.
- `model.py:87` commits a new boundary only after qualification. A latest
  identical retry inserts neither a likelihood nor a transition.
- `model.py:101` uses an identity transition and no likelihood for a query.
  `model.py:115` performs future prediction on a private branch. Both leave
  durable state unchanged.
- Pre-outcome predictions in `probe.py:95` consume only the first four
  observations of each five-observation sequence. The fifth is used for
  scoring afterward.

An independent read-only check enumerated complete context paths, rather than
using either the candidate's local messages or the probe's recursive filter.
For each static `(A,B)` and context path `(c_0,...,c_n)`, it accumulated

```text
pi_0(A,B,c_0) * product_i T_h(c_i | c_(i-1)) L(y_i | theta_(c_i)),
```

then normalized and marginalized the old contexts. All 24 cases consisting
of the eight length-three sign sequences at all three hazards matched the
candidate's entire retained joint exactly. Another 15 cases used the
nonuniform prior `(1,2,...,8)/36`, all three hazards, and observations
`{-8,-2,0,2,8}`. Their query marginals and one-event posteriors also matched
exactly, and queries preserved the snapshot. These 39 supplemental audit
cases ran in under one second. They are not additional trials retroactively
inserted into the frozen search receipt.

The theorem's limitations are appropriate: this is exact forward filtering on
a supplied finite model, compiled into cluster trees. It is not arbitrary
loopy confluence, a biological brain, or actual observation of another patch's
belief. The same local numerical kernel handles retained inference and
queries; the compiler, selected model family, boundary projection and event
transaction remain separate, explicit architecture. The text does not claim
that this alone passes the complete one-rule or core-replacement requirement.

## Concrete integrity and protocol findings

1. **The original convenience verifier has a typed-comparison weakness.**
   `probe.py:189` compares Python dictionaries. Replacing a stored check's
   JSON `true` with integer `1` leaves that equality true. This was reproduced
   on an in-memory copy of the actual receipt; canonical JSON distinguishes
   the mutation. It does not alter the current scientific values, but the
   original `probe.py --verify` is insufficient as a strict receipt check.

   The subsequently added `verify_round.py` addresses this without changing
   the original scientific artifact: canonical typed comparison, duplicate-key
   and nonfinite rejection, exact check types, and source hashes before and
   after replay. Its six mutation tests passed independently during this
   review. No blocker was found in that wrapper. Use its `--verify` entry point.

2. **The original standalone source pinning is incomplete.**
   `probe.py:171` hashes the lane sources and kernel after computation, but
   omits the imported shared `contract.py` and does not compare before/after
   source identity. The supplemental verifier pins that dependency and itself
   and checks source stability during its replay. Its explicit
   `original_run_full_source_custody_proven: false` is correct: a later replay
   cannot retroactively prove the original run's full source custody.

3. **One promised lesion differs from the executed lesion.**
   Protocol item 4 promises an all-singleton product lesion on actual learned
   histories. `probe.py:123` instead preserves the full parameter joint
   `P(A,B)` and context marginal `P(c)`, replacing only their dependence by
   `P(A,B)P(c)`. This is a useful and more selective lesion, but it is not the
   promised all-singleton product. The constructed two-state witnesses at
   `probe.py:142` do test the all-singleton product. Thus the scientific
   distinction must be retained: selective lesion on acquired histories;
   full singleton lesion on constructed fixtures. The omitted acquired-history
   control remains unrun in this frozen round.

4. **Checkpoint parsing is not a hostile-input boundary.**
   `model.py:127` checks text length and each weight's string length, then
   passes those strings to `Fraction`. Short exponent notation can represent
   integers much larger than its text length suggests. Duplicate JSON keys
   are also accepted by the original parser. No large or hostile input was
   executed in this review. Treat restoration as trusted-fixture-only until
   a separately versioned parser restricts canonical integer/rational syntax
   and arithmetic bit length. This limitation does not invalidate the
   candidate's current small, internally generated checkpoints.

## Interpretation of the negative predictive result

The predictive evaluation at `probe.py:95` weights all 32 length-five sign
sequences equally. Consequently the final sign is independent of its prefix.
The frozen forecast `P(+2)=1/2` is optimal on this distribution by construction.
This is an informative mismatch control, not a task on which history is
expected to improve prediction.

For any predicted center mean `m`, the average squared error over the two
possible final signs is `4 + m^2`; zero is optimal. Let
`a=L(+2|+2)` and `b=L(+2|-2)`, with `a>b`. For predicted positive probability
`p`, the two scored probabilities are `b+(a-b)p` and `a-(a-b)p`. Their product
is maximized at `p=1/2`, so that forecast also minimizes mean negative log
probability. The frozen control's winning scores therefore do not establish
that temporal retention is useless; conversely, the candidate cannot claim
predictive superiority from this evaluation.

The switching endpoints are valid model-conditional results. The zero-hazard
model cannot explain a regime change in this way, while nonzero hazards can
because switching is explicitly part of their supplied family. Endpoint
success does not isolate an advantage over a cheap recency rule, prove that
learning static parameters helps, or establish general context discovery.
Label symmetry keeps the context marginal uniform, while parameter/context
correlations can still convey the public value. Thus the reset-parameter
control's collapse to the frozen prediction is expected; it is not a clean
isolation of the utility of learned parameters.

## Small, discriminating next checks

These are proposals for a new frozen round, not claims about completed work:

- Compare predictive scores on an explicitly specified switching-process
  distribution, with known-parameter, prior-reset and cheap recency controls
  receiving identical observations. Keep the present independent-sign task
  as the negative control and preserve every preselected hazard.
- Add the promised all-singleton lesion on actual retained histories beside
  the existing selective parameter/context lesion. Preserve their distinct
  interpretation and verify the marginals each lesion is intended to retain.
- Make the supplemental complete-path and arbitrary-prior oracle checks
  permanent. Include sparse valid priors, repeated private predictions,
  neutral-event retries, and continuation after structural challenges against
  an untouched clone. A neutral actual event may advance context; a retry or
  query may not.
- Test actual belief readback in a separately declared extension. Adding more
  latent world variables is not itself an observer of the lower solver's
  current belief or repair state.

The scope flags correctly remain false for brain equivalence, actual belief
self-observation, general context discovery and core replacement. Scaling
remains locked. The candidate is a coherent small retention mechanism with
useful exact controls; this review does not support production promotion.

Strict replay command from the workspace root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 cadence-candidate-test-suite/searches/codex_finite_context_20260928_a/verify_round.py --verify
```
