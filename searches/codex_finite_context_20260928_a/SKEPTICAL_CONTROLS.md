# Skeptical controls for the finite context candidate

**Design only; no outcomes recorded here.** This document specifies bounded
controls before running this lane. It does not amend the shared suite or its
seven frozen scalar probes. The [claim](CLAIM.json) reserves only this directory.
All three supplied hazards `h in {0, 1/16, 1/4}` must be reported; no favorable
hazard or sequence may be selected after looking at these controls.

The intended candidate has binary context `c`, persistent binary parameters
`theta_A, theta_B in {-2,+2}`, and eight joint memory weights
`P(theta_A,theta_B,c)`. Context transitions have fixed symmetric hazard `h`.
Witness likelihood is proportional to `4^(-abs(y-theta_c))`, normalized over
the integer observation domain `[-8,8]`. Output `q` is the selected parameter
`theta_c`. The four-cluster construction has the declared central
`(theta_A,theta_B,c_previous,c_next)` factor, prior, likelihood and readout
factors. Its `Factor`/`Network` implementation is the unchanged local kernel
from the [cluster-tree reference](../../../cadence-flagship/experiments/local-observer-repair/README.md).

These are supplied representational choices. The candidate does not discover
the number of contexts, parameter values, likelihood family, transition law
or graph. It can learn posterior uncertainty and dependencies within that
family. It has no stimulus vocabulary with which to demonstrate transfer to
unseen stimuli, and no actual belief-readback observer interface merely because
some random variables are latent.

## 1. What would otherwise be a false positive

The shared A4/B4/A4 test records three predictions **after** each four-event
block. A decoder that simply returns the latest value passes it perfectly.
Thus passing that probe is a necessary short tracking result, not sufficient
evidence of acquired context memory, inference before outcomes or retention
of separate skills. Keep the original result, including failures, but do not
promote it to those stronger claims.

The opposite-history probe is stronger because both histories end in zero,
but a last-nonzero-value decoder or a leaky running average can still produce
different answers. Both are useful cheap controls, not evidence that the
candidate cheated. To support a more specific mechanism claim, inspect and
intervene on the retained joint posterior while holding its marginals fixed.

An exact posterior also is not necessarily the best predictor on a selected
deterministic sequence. Its supplied HMM assumptions can be wrong. Separate:

- conformance to the declared posterior and event semantics;
- a causal effect of retained parameters or dependencies on a response;
- pre-outcome prediction quality on the declared small tasks;
- the stronger, currently unestablished claims of context-specific skill,
  novel-stimulus generalization, actual self-observation and unified brain
  competence.

## 2. Label symmetry is an exact control

With an exchangeable initial parameter prior and symmetric unobserved contexts,
simultaneously swapping `theta_A <-> theta_B` and `c <-> 1-c` leaves the model
and every observed sequence unchanged. Verify that the actual initial prior
has this property before applying the following assertions.

Consequently, `P(c=A)=P(c=B)=1/2` can remain true at every event even when the
selected-value prediction is strongly nonuniform. Context-label entropy and
accuracy against an arbitrarily named A/B sequence are not useful learning
metrics in this symmetric model. They cannot distinguish a correct posterior
from failed inference. Likewise, a context label supplied by the evaluator is
not a cue the unassisted candidate has learned to interpret.

Use label-invariant quantities instead:

```text
P(q=+2) = sum_theta,c P(theta,c) * 1[theta_c=+2]
P(theta_A != theta_B)
P(theta_A,theta_B) and the full P(theta_A,theta_B,c)
dependence gap = TV(P(theta,c), P(theta)*P(c)).
```

Require exact invariance of the predictive distribution under a consistent
latent-label relabeling of the prior, factors and checkpoint. Sign reversal of
every observation should reflect `P(q=+2)` to `1-P(q=+2)` when the prior is
also sign symmetric. Assert those distributional identities, not only rounded
scalar means. If the implementation intentionally breaks either symmetry,
freeze and disclose that supplied asymmetry instead of silently using these
assertions.

## 3. Eight fixed short histories, with predictions before outcomes

Write `A=-2` and `B=+2`. The letters name observable signs, **not** known latent
context identities. Freeze this complete set before inspecting results:

| ID | History | Paired purpose | Optional next witnessed value for the fixed continuation task |
| --- | --- | --- | --- |
| H1 | `A A A A A 0` | H2 has the same latest value and opposite prior experience. | A |
| H2 | `B B B B B 0` | Sign reflection of H1. | B |
| H3 | `A A B B B B B 0` | H6 has exactly the same observation multiset and latest value, in a different order. | B |
| H4 | `B B A A A A A 0` | H5 has exactly the same observation multiset and latest value, in a different order. | A |
| H5 | `A A A A A B B 0` | Longer early A exposure, shorter recent B exposure. | B |
| H6 | `B B B B B A A 0` | Sign reflection of H5 and temporal-order partner of H3. | A |
| H7 | `A A A B B B 0 0` | H8 matches all counts and the last two observations. | B |
| H8 | `B B B A A A 0 0` | Sign reflection and temporal reversal of the nonzero blocks in H7. | A |

These are development diagnostics, not a population estimate. Their lengths
and sequences differ from the known A4/B4/A4 fixture, but the design is public;
do not call them an unseen generalization benchmark after using them for
revision. All fit within the existing 24-event capacity. Do not add padding
observations or change thresholds to obtain a preferred verdict.

At every event retain the forecast **before** supplying its value, then the
accepted posterior and the current-state estimate after it. The declared
target-free `query()` uses the identity transition, so it estimates the
**current** `q`. A forecast for the next witnessed event must instead apply
`T_h` exactly once and use a unit likelihood on a detached copy through the
same kernel. It must not commit that transition. The actual later observation
starts from the original checkpoint and applies its transition once, not from
the advanced forecast copy. If the adapter exposes no such forecast, retain
current-estimate diagnostics and mark next-event forecast scoring unsupported;
do not attribute an oracle's forecast to the candidate.

Before admitting the optional next value in the final column, freeze and
score its next-event forecast separately.
That continuation assumes the most recent nonzero regime persists through the
zero observations. It is a declared task assumption, not a sample guaranteed
to follow every candidate hazard. Report all three hazards even if this task
favors one of them.

For H3/H6, H4/H5 and H7/H8, an order-sensitive answer is possible despite
identical counts. Do not require a nonzero difference merely by decree:
independent exact enumeration must establish whether the candidate's stated
model predicts a difference. If the oracle predictions coincide, this pair
is **nondiscriminating for that model/configuration**, not a successful
demonstration of temporal memory. Preserve the pair and that outcome.

Record both probability and expectation. Use squared error for the mean and
the full categorical likelihood for distributional scoring. For an actually
observed symbol, predictive probability integrates the normalized observation
likelihood, not simply `P(q=symbol)`: zero is an allowed observation but is not
one of the two latent output values. A proper score must not confuse these
two distributions.

## 4. Zero is ambiguous evidence, not a missing input

The declared symmetric observation model gives equal likelihood to zero under
`theta=-2` and `theta=+2`. A zero witness therefore supplies no sign preference.
It still advances the witnessed event clock and applies the hazard transition.
A target-free query instead uses the identity transition and unit likelihood;
it must not age the context, accumulate evidence or alter durable bytes.

For each fixed history, compare on copies:

1. five target-free queries, with byte-identical persistent checkpoints;
2. one additional actual zero witness, with a new source ID;
3. a retry of that zero under the same ID, which must not apply the transition
   a second time;
4. the exact independent transition-only posterior for the new zero witness.

Those cases need not give the same prediction: real time can change a context
belief while a query cannot. An increasingly ambiguous predictive distribution
after ambiguous events can be correct. Calling it failure merely because it
does not pick a definite hidden context would reward unjustified confidence.
In this specific symmetric likelihood, the neutral zero event must leave the
joint parameter marginal `P(theta_A,theta_B)` exactly unchanged: the normalized
transition only moves context mass. Its full joint memory and source cursor
may still change. This is a useful selective persistence assertion.

The scalar interface provides no separate observed context cue. A conditional
query such as fixing internal `c=A` is a structural interrogation of a chosen
coordinate, not demonstrated natural recall from an external cue. Any future
cue-based test needs an explicit sensory cue variable, a learned relationship,
held-out cue combinations and matched controls. It is currently unsupported.

## 5. Ablations that identify what the memory actually stores

Apply interventions only to detached copies of an accepted full checkpoint.
Keep source cursors, hazard, emission tables and query operations identical.
The unmodified original must have the same continuation fingerprint before
and after every diagnostic. Save all eight exact weights, not just the mean.

Let `P(theta,c)` denote the checkpoint, `theta=(theta_A,theta_B)`, and let
`P0(theta)` be the original parameter prior. Use these distinct controls:

| Control | Replacement | What it can isolate |
| --- | --- | --- |
| Full continuation | Original `P(theta,c)` | The candidate's actual result. |
| Dependency cut | `P(theta)*P(c)` | Loss of context–parameter dependence while preserving the **entire joint parameter marginal** and context marginal exactly. This is the primary structural control. |
| Fully factorized memory | `P(theta_A)*P(theta_B)*P(c)` | Additional loss of dependence between the two parameters. Do not attribute its effects solely to context coupling. |
| Parameter-marginal reset | `P0(theta)*P(c|theta)` | Removes acquired parameter marginal while retaining the posterior conditional context law. Require every needed `P(theta)>0`; otherwise report the unsupported conditional, never invent missing values. |
| Fully reset memory | Original full prior | Erases both acquired parameters and current state information; useful but not a selective parameter intervention. |
| Parameter-frozen streaming control | After each admitted event, retain the inferred context marginal but reset parameter information to the declared prior before the next event. | A state-filtering baseline without durable parameter acquisition. It also removes dependencies; report that combined limitation. |

For this positive-likelihood finite model, full-prior support should remain
positive, including at `h=0`, provided the initial context prior has full
support. Assert the support rather than relying on that expectation. All
replacement factors must be normalized and passed through the same kernel.
The test oracle may compute intervention weights; it must not supply the
candidate's predicted answer.

Compare immediate query distributions and the next one or two witnessed
continuations from each intervened copy. Report exact total variation,
predictive differences and task losses. Restoring the original eight weights
must restore its response exactly. The dependency cut should not be labeled
an informative lesion when its distribution already equals the intact one.

A dependency effect after a single observation is possible; it is not proof of
long-term context memory. Include the one-witness checkpoint as a reference and
show separately what changes after the fixed multi-event histories. Exact
parameter learning within the supplied eight-state family does not establish
new relational structure or a generic memory architecture.

## 6. Cheap predictors must remain visible

Run these task controls outside the candidate, using the identical admitted
observation history. None is substituted into a candidate response:

- frozen prior predictor;
- latest-observation value;
- latest **nonzero** value, with a zero initial value;
- cumulative mean with the shared suite's declared prior convention;
- exponential moving average `m <- (m+y)/2`, initialized at zero;
- the parameter-frozen model control above, with its filtering work counted.

Do not optimize an EMA rate or select a window after seeing this set. Report
pre-outcome scores on all events and separately on the optional continuations.
The last-nonzero predictor is intentionally strong for the declared
continuation task. If it matches or beats the candidate, retain that result;
posterior conformance and selective intervention effects can still pass, but
no predictive-utility advantage has been demonstrated.

Do not average away the switch points. Keep post-switch first-prediction,
within-block adaptation, ambiguous-zero behavior and return-to-earlier-sign
behavior separate. A good final answer after repeated exposure cannot show
instant recall at the first event of a new regime.

## 7. Source ownership, caps and exact continuation

Reuse the shared source tests without weakening them: queries, identical
latest retries, conflicting reuse, skipped/old IDs, and derived or imagined
events. Add the following joins for the new context model:

- A duplicate cannot apply the hazard transition again, even when its
  likelihood is neutral.
- A query cannot copy its predicted distribution into the next prior as if a
  new observation occurred.
- A zero-budget **unsettled** witnessed event cannot publish a changed joint
  posterior or consume its ID. Record original residuals and retry once at the
  normal unchanged budget. A state already qualified at budget zero is not a
  manufactured cap failure; choose the declared nontrivial first witness.
- Snapshot/resume before and after the ambiguous event produces exactly the
  same complete next posterior and event ownership as uninterrupted operation.
- Invalid checkpoint masses, support, hazard/configuration identity, source
  cursor or total mass must be rejected atomically. Finite mean agreement alone
  does not validate a checkpoint.

Keep `h=0` as an original control. It represents a stationary latent context,
not a failed implementation of positive-hazard switching. Failure on a changing
stream can be model mismatch while its posterior remains exact. Conversely,
all three arms can be numerically correct without any one passing a useful
continual-learning task.

## 8. Same kernel, not a special decoder or an oracle answer

Record source hashes and count actual `Network.settle` calls, sweeps, message
evaluations, table entries and all cap attempts separately for query, witness,
intervention and generic factor tasks. Independently enumerate the finite
joint distribution from raw factors in the **test harness**, without importing
candidate transition, posterior or prediction helpers. Compare the whole
posterior and every separator marginal using exact arithmetic.

Inspect that both witnessed conditioning and target-free query really use the
same pinned factor/message kernel. Publishing a scalar expectation from its
qualified output marginal is a declared readout; returning the latest witness
or a harness-computed oracle expectation is not. An eight-weight posterior
update implemented directly in a separate hidden filter would not demonstrate
the intended kernel reuse, even if its numerical answers happened to agree.

Check nontrivial messages and shared separators in the event graph. A single
fully enumerated joint factor can be a legitimate exact oracle, but its empty
message residual alone would not demonstrate distributed repair. Count the
largest bag and full table work; a 16-row central factor is supplied grouping,
not constant-cost scaling to an arbitrary graph.
Eight rational weights are a fixed number of coordinates, not a proof of fixed
storage for an unlimited stream. Record numerator/denominator bit lengths and
serialized bytes; the finite 24-event contract is the actual bound here.

Run the existing four-condition `fly_directed_transition` fixture through the
**same adapter instance**, between two scalar-history events. Verify that the
structural call leaves scalar persistent state unchanged and that later
scalar continuation matches its untouched clone. The fixture must use this
adapter's same pinned `Factor`/`Network` kernel, not call another candidate or
read stored expected beliefs. Compare against the existing independent
enumeration and retain all four conditions.

This can establish one implementation handling its declared scalar and finite
factor domains. It does not establish that scalar learning changes fly wiring,
that the original continuous fly dynamics are preserved, that the model flies,
or that it reads its own actual uncertainty. Separate unsupported features
remain unsupported. No structural challenge closes all of P2, O1, O2 or D4.

## 9. Receipt and claim boundaries

Freeze model, likelihood normalization, three hazards, eight histories,
controls, support assumptions and all numerical/resource limits before the
first run. Retain every hazard and every control; do not patch a failed frozen
protocol in place. The lane budget is one local worker, at most 60 seconds per
child and less than 1 MB total artifacts. Exceeding it is a retained resource
failure, not permission to start a larger run.

Each case records source/configuration identity, exact input and event ID,
forecast versus current-estimate timing, pre-outcome and post-outcome
distributions, full eight-weight memory where
relevant, independent oracle result, symmetry and intervention checks, all
solver work, elapsed time and serialized bytes. Invariant/algebra failures,
prediction failures, unsupported interfaces and infrastructure errors remain
separate statuses. No rounding of a probability can turn an exact mismatch
into a pass.

No single aggregate success flag should blend these four questions:

1. Did the same kernel implement the declared finite Bayesian filter correctly?
2. Did retained parameters and joint dependencies causally affect responses?
3. Did those effects improve the declared pre-outcome task over the fixed cheap
   controls, at a disclosed cost?
4. Has the same candidate met the broader capability and replacement gates?

The fourth remains **not established** by this protocol, regardless of the
first three outcomes. This is a small candidate test, not an all-34 capability
result, biological proof, actual-belief self-observer demonstration, or a
license to replace the current core.
