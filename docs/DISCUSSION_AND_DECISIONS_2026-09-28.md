# Discussion and decisions: unified repair and candidate testing

**Research-day record, 2026-09-28.** This document collects the questions,
distinctions, small results and decisions behind this suite. It covers the
current redesign discussion, using earlier game, music and control experiments
as background. It is not a transcript of every earlier Cadence experiment,
an additional production release, or a declaration that the redesign works.

The central question is whether one simple local operation can support both
responding to experience and retaining what experience teaches, with recursive
observers participating in the same coupled state. The practical conclusion
today is to test that question directly, on small cases, before scaling it.
There is no selected candidate ready to replace the current core.

The owning requirements are the [redesign proposal](../../plan/CADENCE_UNIFIED_REPAIR_REDESIGN_2026-09-28.md),
[capability register](../../plan/CADENCE_CAPABILITY_AND_PROOF_REGISTER.md),
[local-first and replacement gates](../../plan/CADENCE_LOCAL_FIRST_FLY_GATES_2026-09-28.md),
and [depth-selection process](../../plan/CADENCE_DEPTH_SELECTION_2026-09-28.md).
This dated record explains them; it does not override later source-bound
results or those current plans. The [suite protocol](../PROTOCOL.md) and
[machine-readable catalogue](../criteria.json) define this particular battery.

## 1. The thesis being tested

The owner clarified a stronger claim than “an equilibrium network can be
trained”: **inference and learning should be the same repair process**.
Observations, current interpretations, retained relationships and observers
should interact through a common primitive. Answer or action variables belong
to that coupled system, rather than being produced by a separate task-solving
head. A federation of patches should expose the same kind of interface as an
individual patch.

Current Cadence supplies useful components, but does not establish this
identity. For example, a `PatchNet` holds parameters fixed while solving free
and nudged phases, then applies a local contrast through `Learner.update`.
The activities are joint equilibrium variables; the parameter update is a
distinct operation. Calling both operations “repair” does not make their
executed mechanisms identical. Other public components use record writes,
finite-window differentiation or sequential composition and must be assessed
under their own contracts. See the [current core contracts](../../cadence/docs/contracts.md)
and [recursive training recipe](../../cadence/docs/recursive-training.md).

The stronger hypothesis is neither established nor refuted by those APIs.
It asks for an explicit new state, local equations, evidence boundary,
persistence rule and executable implementation. The existing implementation
remains a control and usable engineering system while that hypothesis is
tested separately. The convenient `PatchNet.recursive(...)` construction can
be preserved without pretending its present mathematics already supplies the
new primitive.

Four claims must remain separate:

1. A model can **represent** a relationship or task solution.
2. Its stated dynamics have a **conditional mathematical guarantee**.
3. Its own experience actually **learns** the relationship.
4. The resulting system provides **useful, integrated performance at a declared
   cost**, compared with suitable alternatives.

A hand-constructed solution supports the first claim. A converged solve can
support a numerical instance of the second. Neither implies the third or
fourth. Nor can successes from different candidates be combined into a single
system that has never been implemented.

## 2. Why the earlier evidence prompted this review

The review preserved positive evidence while correcting overly broad
interpretations. These are earlier experiments examined during this discussion,
not new game campaigns run by this suite.

| Evidence | What it supports | What it does not establish |
| --- | --- | --- |
| [Doom project](../../cadence-flagship/cadence-doom-project/README.md) | A graph with 1,371 input, 32 hidden and six answer neurons can learn useful visual action values. Local EP and implicit learners each achieved 64/64 kills on the fresh confirmation episodes, with image controls and numerical verification. | One training seed per learner, offline simulator teaching and supplied input history do not establish learning during play, unified repair or a benefit of observer depth. MLP and CNN controls also achieved 64/64. |
| [Streaming control](../../cadence-flagship/experiments/stream-control/confirmation/SUMMARY.md) | Actual online learning and retention can be compared on the same changing actuator stream. The recipe produced qualified solves but did not show a consistent observer advantage. | A negative depth comparison does not identify task simplicity as its cause. MLP and recurrent controls learned online too; online learning is not exclusive to Cadence. |
| [1942](../../cadence-flagship/drsn/1942/README.md) | Saved interrupted training logs permit checks of fitting, attempted work and numerical admission. | There was no completed demonstration of a depth advantage or trained playing competence. Weak conventional fits do not establish superiority over strong conventional learning. |
| [Atari](../../cadence-flagship/drsn/atari/README.md) | Some deeper population arrangements had better saved action-value fits than a flat arrangement. This signal should remain visible. | Validation contexts shared episodes with training. An action-value fit difference is not a fresh-episode game result or proof of an ordered observer mechanism. |
| [C64 Maestro](../../cadence-flagship/drsn/c64maestro/README.md) | Recorded finite-compute pilots expose changed parameters, response behavior and unsettled motor states. | Weight motion alone does not show a useful learned observer. A motor residual does not certify world, phrase or nudged phases that lack the matching check. |
| [Connect Four](../../cadence-flagship/drsn/connect4/README.md) | Small probes and numerical failures provide engineering information. | An interrupted depth sweep supplies no comparison result. The separate search-assisted application cannot be attributed to this unfinished DRSN experiment. |

The [evidence arithmetic audit](../../plan/audits/cadence/unified_redesign_2026-09-28/README.md)
checks the retained small files and source identities without replaying games
or downloading large checkpoints. Its [receipt](../../plan/audits/cadence/unified_redesign_2026-09-28/receipt.json)
and [checker](../../plan/audits/cadence/unified_redesign_2026-09-28/check_evidence.py)
record the exact scope. In particular:

- The 1942 logs contain **13,750 attempts**, not that many demonstrated accepted
  updates. Fourteen of sixteen last logged fits are worse than their earlier
  best. At least six early free-phase failures follow from the retained call
  structure and phase-count deficit; incomplete logs cannot supply every final
  event. A training-mean label predictor has validation MSE approximately
  **0.0607063**, which matters when interpreting the weaker conventional fits.
- C64’s saved 48-iteration motor residual maxima are approximately **2.02** and
  **0.185** for the two reported arms. Calling the smaller value “settled” would
  confuse improvement with satisfaction of an equilibrium tolerance. Window
  means and their exact sample ranges are recomputed in the audit. The small
  receipts do not establish the historical runtime version; current source
  must not be substituted for it.
- Atari’s saved completed endpoints qualify their reported rows, but that
  does not turn episode-overlapping validation into independent confirmation.
  Tied action labels also make plain first-index `argmax` agreement an incomplete
  measure of action quality.

These corrections concern evidence and protocol interpretation. They are not
proof that a joint equilibrium architecture cannot work. Conversely, the
positive Doom result cannot fill the missing unified-learning or recursive
capability evidence. The released warm refinement improves numerical admission
for supported reciprocal equations; it is not a new learning theorem or a
replacement for the proposed local primitive.

## 3. Memory makes the unified-state claim nontrivial

Suppose the **entire** adaptive state has a unique equilibrium determined only
by the present sensory input. Two different histories ending with that same
input must then reach the same state. Such a system cannot retain a distinction
between those histories. Adding more variables does not remove this logical
obstruction if all of them are uniquely reset by the same present boundary.

Possible coherent mechanisms include retained boundary state, protected
experience, multiple history-dependent attractors, or ongoing dynamics. Each
needs its own contract. The present proposal starts with a conditional event
problem: hold actual evidence and preceding memory fixed, jointly repair live
interpretation and candidate memory, then commit the accepted durable component
once. Numerical repair time is distinct from environmental time.

For example, with known input `x`, preceding parameter `m` and positive
retention strength `lambda`, consider

```text
E(y,w; x,m) = (y - w*x)^2/2 + lambda*(w - m)^2/2.
```

If `y` is unobserved, the joint optimum is `w=m`, `y=m*x`: querying preserves
the mapping. If an actual outcome fixes `y=c`, the optimum is
`w=(x*c+lambda*m)/(x^2+lambda)`. The same stated compatibility and retention
terms now acquire information because the evidence boundary changed. This is
a convex scalar construction, not a solution to nonlinear world learning.

The [exact equation audit](../../cadence-flagship/experiments/unified-repair-audit/README.md)
contains a related **soft-witness** fixture, not that hard-clamped numerical
example. Starting with `x=1`, `m=1`, unit retention and a unit-strength witness
of zero, its optimum is `y=1/3`, `w=2/3`; a later query has smaller prediction
error. The distinction between a hard observation and a finite observation
penalty must remain explicit.

The same audit retains three warnings:

| Small witness | Exact lesson | Scope |
| --- | --- | --- |
| Unanchored joint `E=(y-w*x)^2/2` | For `x=1`, starting a query at `y=0` halves `w` under the specified joint gradient flow. Repeating that reset gives `1, 1/2, 1/4, 1/8` while each solve reaches zero defect. | Allowing the memory to move with no retained reference can erase it. This is a counterexample to the naive rule, not to every unified rule. |
| Two Boolean cells copy a neighbor from `01` | Asynchronous orders can end at `00` or `11`; synchronous copying can cycle. | “Every move is local” does not imply confluence, unique interpretation or convergence. |
| A learnable nonnegative precision weights a fixed mismatch | Setting precision to zero can minimize weighted error while the underlying disagreement remains. | Agreement obtained by suppressing all evidence is not successful interpretation. |

One-event ownership is therefore part of the model. Repeated solver sweeps,
queries, retries and self-readback must not fabricate new observations. A cap
or invalid event must leave durable memory and its event cursor unchanged.
Checkpoint continuation must retain both learned state and evidence ownership.
An ordered finite source protocol is a useful initial test, but is not a proof
of unbounded distributed deduplication.

Retention also needs an eventual resource policy. Bounded storage cannot
promise perfect recall of arbitrary histories forever. Selection, forgetting,
consolidation and protected records need explicit behavioral tests, not an
unacknowledged growing archive or removal of inconvenient old examples.
When a raw record is retired, a retained learned summary is still derived
state. Retirement must not relabel that summary as a fresh independent
observation. The deduplication horizon and any loss of reconstructible
provenance must remain explicit.

## 4. What “observer” and “overlap” mean here

An observer patch must read something about the actual state or belief of the
patches it observes and causally feed back into them. An extra hidden group,
copied input or fixed latent label is not enough to establish self-observation.
The observed quantity might include a current estimate, uncertainty, prediction
or relation. Readback is derived information, not an independent witness.

The [biological mapping](../../cadence-flagship/idagrams/BIOLOGICAL_MAPPING.md)
distinguishes a current interpretation, a learned world model and a conscious
percept. The tests address interpretations, memory, behavior and reportable
information. No solve or receipt certifies subjective consciousness.

For local states `s_p`, declared overlap maps define compatible families:

```text
C = {s : rho_pq(s_p) = rho_qp(s_q) for every declared overlap}.
```

If `Gamma` denotes representation redundancy, a normal form is a particular
settled element of `Sigma/Gamma`, subject to the required assumptions. It is
not “the quotient of the overlaps.” Protected evidence and computed readout
have different roles. A readback preserved by every repair is an invariant;
its invariant class alone does not describe the changing computation of an
interpretation. An equivalence intended for a continuing brain must also
respect future inputs and interventions, not merely today's output.

The functional anatomy mapping is deliberately limited:

| Biological role | Candidate computational role | Important boundary |
| --- | --- | --- |
| Cell and intracellular machinery | Private state, local integration and maintenance | Memory is not confined to the soma. |
| Dendritic receiving structures | Input ports and potentially nonlinear input grouping | Anatomical contact does not itself define a semantic overlap. |
| Axon and branches | Published output and directed fan-out | One output may reach many recipients; no one-recipient restriction is intended. |
| Chemical synapse | Recipient-dependent transfer, efficacy and possibly plastic/modulatory state | Coupling two cells does not mean their activities should become equal. |
| Membrane dynamics | Integration, bounded response and time dependence | A rate-model potential is not a biological spike or calibrated physical time. |
| Overlap port | Two representations of a shared quantity, with declared translation and uncertainty | Equal vector width supplies neither shared meaning nor compatible coordinates. |

For a directed contact, `u_ji=h_ji(a_j,m_ji)` can be the transmitted quantity
whose local copies must agree. The receiving activity can remain different
from the sender’s. This preserves the distinction between transmission and
interpretation. Dendrites, axons and synapses inspire roles; they are not a
proof that a particular software primitive reproduces their biology. Fly
neurites also do not obey every detail of a simple mammalian multipolar-cell
cartoon. The source guide links the biological evidence and the actual import.

## 5. Federations, loops and the absence of a deepest authority

The recursive design goal is **closure under composition**: a network of
patches should itself offer a patch interface. Its internal states remain
private; its boundary must preserve the information needed by external
constraints and feedback. That is more demanding than averaging a group of
neurons and naming the average an observer.

The [federation guide](../../cadence-flagship/idagrams/FEDERATION_AGREEMENT.md)
separates several useful, conditional results:

- Fixed linear orthogonal-projection repairs in a common metric have a
  tractable convergence argument under the specified schedule. This does not
  automatically cover moving port maps, learned weights or nonlinear memory.
- A finite probabilistic federation can preserve its outside behavior by
  retaining the full joint boundary factor obtained by summing over private
  variables. A minimum-energy boundary uses minimization instead; it is not
  the same operation as probabilistic marginalization.
- Exact joint boundaries may be large, dense or high order. A cheap factorized
  summary is an approximation whose lost correlations require measurement.
- Regrouping an existing model is different from adding new observer variables
  and feedback. New observers introduce a model assumption; they do not create
  an additional independent observation of the world.

The [finite federation oracle](../../cadence-flagship/experiments/federation-agreement/README.md)
checks exact composition, relabeling and correlation-loss cases. Parity provides
a concrete obstruction: distributions can have the same individual and pair
marginals but different joint relationships. No extra processing of a summary
can reconstruct information the summary discarded. More depth alone cannot
fix that loss. The oracle is algebra evidence, not an implementation of
scalable local learning.

Loops matter because compatibility can depend on composed translations around
a cycle. An odd binary disagreement cycle is a small holonomy/conflict fixture:
its hard constraints cannot all hold. A correct system should represent the
conflict, conditional alternatives or a declared compromise. It should not
return a fabricated zero-mismatch “consensus.” At a valid compromise the
solver's equation defect may vanish while semantic disagreements remain.

Gauge transport changes a redundant description. Coarse-graining may discard
information. They need distinct controls. Similarly, loop sign alone does not
establish memory, oscillation or a biological role: the actual operating point,
nonlinearity and boundary drive matter.

No deepest observer receives final authority. Higher-level constraints must
remain answerable to lower-level evidence and their own feedback effects.
Coherence can be wrong about the world. Learned consequences and new
observations must be able to correct it. Shared evidence also needs ownership
when federations overlap; copying it into several summaries must not multiply
its statistical weight.

Current `PatchNet.recursive` populations are jointly coupled, but that factory
does not itself supply typed semantic ports, sufficient federation boundaries
or an ordered abstraction hierarchy. Its topology is documented in the
[recursive-topology audit](../../cadence-flagship/unodiotres/recursive_topology/README.md).
Increasing population count is not automatically increasing observer depth in
the stronger sense discussed here.

## 6. What the small candidate families actually establish

The [evidence inventory](EVIDENCE.md) links each preserved protocol, producer
and receipt. These results deliberately remain separate.

| Candidate or reference | Positive result | Unresolved or failed requirement |
| --- | --- | --- |
| Anchored scalar joint energy | A retained boundary can make a query preserve memory and an actual outcome change it through the declared objective. | Nonlinear relational learning, continual context, federation and integrated behavior are not demonstrated. |
| [Finite conditional relation](../../cadence-flagship/experiments/relation-patch-probe/README.md) | A precise finite conditioning model can support answering and retained information. | A global finite oracle is not yet a scalable local repair mechanism. |
| [Local cluster-tree repair](../../cadence-flagship/experiments/local-observer-repair/README.md) | Local message operations agree with independent exact finite inference when the declared tree/separator conditions hold. | The latent observer construction does not read actual current uncertainty. General loopy exactness and learned organization are not established. |
| [Self-observation fixture](../../cadence-flagship/experiments/self-observation-probe/README.md) | A precision observer consumes actual lower uncertainty and feeds back into that uncertainty; interventions expose the causal ports. | Its supplied model is not a retained continual learner or evidence of useful learned depth. |
| [Retained Normal–Gamma model](../../cadence-flagship/experiments/retained-observer-probe/README.md) | Experience changes a retained scalar posterior; queries do not. Actual uncertainty and observing precision interact during readout. | Stationary pooling fails context switching, and exact evidence accumulation and numerical readout remain distinct executed operations. |

The retained model is informative precisely because its limits are explicit.
It stores a joint posterior over a scalar world mean and precision. Natural
statistics retain witnessed values without storing an unbounded raw history.
The approximate readout repairs mean `u`, variance `v` and expected precision
`r`; its fixed point has `u=m`, `r=a/b`, `v=b/(k*a)`. The exact marginal variance
is `b/(k*(a-1))` when defined. A small equation residual does not erase that
approximation gap. The [derivation](../../cadence-flagship/experiments/retained-observer-probe/THEORY.md)
states the parameters and assumptions.

After three observations of `-2` or `+2` followed by the same final zero, the
retained means differ: `-1.2` and `+1.2`. This is a genuine bounded history
effect. Queries, duplicate-delivery handling and checkpoint continuation
preserve the evidence. The precision observer changes lower uncertainty, but
does not change the posterior center in this supplied conjugate family.

The A→B→A stream exposes the limit. After four `-2` values followed by four
`+2` values, this stationary learner predicts the pooled mean zero. It does not
infer a new context and promptly adapt to `+2`. Returning to A does not turn
that pooling into context-specific recall. The failure is about this candidate
and frozen task; it is not a theorem that recursive repair cannot represent
contexts. More solver iterations cannot fix a model that assumes a stationary
source.

This distinction is also why “scalar parameter learning” is a fair description
but “learned relational organization” is not. The variables, family and update
structure were supplied. Calling exact factor accumulation and variational
readout one statistical model is accurate; calling them one executed primitive
would hide the remaining R1 gap.

## 7. What the actual fly wiring contributes

The source connectome supplies real cell identities, signed directed contacts
and a concrete challenge to abstractions that silently assume symmetry or
uniform connectivity. The tests use tiny induced motifs with explicit omitted
boundaries; they do not load an entire brain into the scalar candidate.

The [motif](../../cadence-flagship/experiments/fly-motif-probe/README.md) and
[loop-intervention](../../cadence-flagship/experiments/fly-loop-probe/README.md)
references use the supplied browser rate equations and independent checks.
They distinguish original weights from rescaled controls. In the tested loop
conditions there is no washout-history difference above the declared threshold;
cuts change sensitivity and operating point. This is not proof that the living
circuit has no memory or that loop sign determines function.

The new [directed transition adapter](../../cadence-flagship/experiments/fly-transition-probe/README.md)
bridges an actual four-cell motif to finite transition factors and exact local
cluster inference. Its [protocol](../../cadence-flagship/experiments/fly-transition-probe/PROTOCOL.md)
and [receipt](../../cadence-flagship/experiments/fly-transition-probe/receipt.json)
own the numerical counts and checks. The declared two-bin compiler preserves
conditional potential means for its unclipped one-step construction. Quantized
activity and nonlinear multistep responses need not preserve the original
deterministic rate model. Added stochastic variability is a modeling change,
not proof that the original dynamics were reproduced.

The motif output is an interneuron diagnostic, not a demonstrated motor
controller. A real worker input/output test verifies an interface; it does not
establish food seeking, flying competence, endogenous hunger, learned timing or
complete neurotransmitter physiology. The biological mapping lists the source
model's omissions. A named transmitter, signed edge or attractive visualization
cannot supply missing biochemical or behavioral evidence.

For a later tiny embodied test, brain and body responsibilities must be stated
separately. Supplied stabilization or mechanics may execute a checked command;
they must not choose a target or route and attribute that decision to the
brain. Actual action/outcome ownership is required before assigning learning
credit. No such new body capability is inferred from the transition fixture.

## 8. All 34 requirements remain in scope

The register is a functional engineering inventory, not an established
complete account of human cognition. Species, task and resource conditions
matter. Every row requires a bounded definition and separate evidence for
representation, guarantees, implementation, learning and utility as applicable.
The seven available probes cover slices only. No row below is discharged in
full by this suite's initial implementation.

| ID and exact register title | What a discriminating task must expose beyond a label |
| --- | --- |
| P1 — sensory representation and invariance | Relevant identity survives a declared nuisance transformation without discarding useful differences. |
| P2 — multisensory binding | Shared cause versus separate causes, with uncertainty and incompatible observations retained. |
| P3 — uncertainty and ambiguity | Alternatives and calibrated uncertainty, including approximation error and contradictory evidence. |
| P4 — selective attention and active sensing | A learned or inferred information request changes uncertainty or behavior enough to justify its cost. |
| P5 — object permanence and latent context | Hidden objects or contexts persist and reappear without a supplied answer label or one-context-per-event memorization. |
| T1 — order, duration and asynchronous streams | Order and timing affect the right predictions; delayed or duplicate events have explicit ownership. |
| T2 — ongoing temporal activity | Meaningful continuous or recurrent dynamics, rather than equating all useful computation with a static endpoint. |
| M1 — working memory | Retention through delay and distraction; the implemented opposite-history probe tests only a small prerequisite. |
| M2 — episodic, source and context memory | Retrieve the right event and provenance; the implemented source protocol tests only bounded ownership and continuation. |
| M3 — semantic and relational abstraction | Reuse a learned relationship on new combinations instead of memorizing presented cases. |
| M4 — procedural learning and habits | Acquired action competence and its interaction with flexible control. This criterion ID is distinct from the M4 computer used for local tests. |
| M5 — consolidation, recall and forgetting | Preserve relevant skills and deliberately handle interference under a declared finite memory budget. |
| M6 — replay and offline reorganization | Internal rehearsal improves later behavior without inventing extra external evidence or reward. |
| L1 — incidental and associative acquisition | Experience changes later predictions; scalar posterior acquisition does not establish arbitrary relation learning. |
| L2 — learning from delayed consequences | An actual later outcome is credited to the right prior action despite intervening events. |
| L3 — continual adaptation without catastrophic loss | Adapt to B and retain or recover A; pooled averages or a frozen weak policy cannot pass as successful retention. |
| L4 — causal world modelling | Predict intervention consequences, including actions and counterfactuals, beyond correlation fit. |
| L5 — adaptive operating range | Useful sensitivity and stability survive changing input magnitudes and conditions without outcome-selected calibration. |
| A1 — innate competence and internal drives | Declared inherited wiring and physiology support a baseline need; learning cannot excuse every missing starting behavior. |
| A2 — emotion-like valuation and motivational context | Internal state changes valuation in a specified useful way; an engineering variable is not proof of a human emotion. |
| A3 — smooth embodied control | Actual body motion remains stable and useful under latency, perturbations and qualified-command limits. |
| A4 — exploration and exploitation | Information-seeking or exploratory actions earn their cost against a fixed or random policy. |
| A5 — goal-directed planning and flexibility | Select actions by consequences and goals, adapting when a route, reward or action effect changes. |
| O1 — composed agreement at multiple scales | Regrouping retains required joint boundary information and external feedback effects. |
| O2 — recursive self-observation | Actual lower beliefs causally influence observers and receive feedback; copied inputs or static latent nodes are insufficient. |
| O3 — error monitoring and calibrated self-assessment | Detect limitations and predict reliability; low solver residual alone is not confidence about the world. |
| O4 — rule abstraction and flexible reasoning | Derive valid consequences, contradictions and underdetermination on new combinations. |
| O5 — social inference, imitation and communication | Distinguish another agent's information or goal and use communicated evidence with provenance. |
| O6 — language and symbolic composition | Compose and transfer structured meanings beyond a lookup of rehearsed strings. |
| O7 — imagination and counterfactual construction | Construct possible alternatives with explicit assumptions while preserving witnessed history. |
| D1 — development and structural adaptation | Added or removed structure earns a measured benefit, including its search and growth cost. |
| D2 — robustness and functional recovery | Reject invalid states and recover useful behavior; atomic cap rollback is only an initial slice. |
| D3 — bounded resources and graceful overload | Memory, compute and queue limits hold under a stated workload, including failure costs. |
| D4 — integrated competence | One continuing candidate retains and combines the preceding abilities, rather than resetting or changing models between tests. |

**Imagination, planning and reasoning are different tests.** An imagined branch
constructs a possible state. A planner compares consequences against goals and
selects an action. A reasoning task asks which conclusions follow, contradict
one another or remain underdetermined. Success at one does not imply the
others. Private branches carry assumptions and provenance, cannot count an
imagined reward as a witnessed event, and must not overwrite actual history.
Incompatible alternatives need not be forced into one factual consensus.

The suggestion that these functions require deep recursive observers remains
a hypothesis. A few shallow failures cannot prove that necessity. Shallow
recurrent controls must be allowed comparable computation, and conventional
online learners remain valid controls. No current result establishes that
MLPs or transformers are incapable of online learning.

## 9. Additional observers must earn their cost

The agreed rule is practical: start with the simplest candidate that can
represent and learn the task. Add observers when a controlled comparison shows
what useful information or computation they contribute. Keep widths, contact
patterns, memory, training opportunities and total work visible. A population
called “observer” does not receive credit merely for being present.

The [selection process](../../plan/CADENCE_DEPTH_SELECTION_2026-09-28.md)
distinguishes quality, adaptation, retention and deadline compliance from raw
solver speed. A slower system may be useful if it substantially improves the
task while meeting its real-time deadline. A faster system is not better if it
loses the capability. A difficult task is not automatically a depth test, and
a failed deep model cannot be excused solely by calling the task too simple.

There is also a representation check before adding more observers. An
additive linear observer can sometimes be eliminated into an effective
shallower linear map. Under those stated linear assumptions, counting the
extra state does not demonstrate new nonlinear binding or reasoning. This
does not establish such a reduction for every nonlinear observer architecture.
The actual interaction and information available through its ports must be
tested rather than inferred from its name.

Acute cuts establish dependence on the cut mechanism at that checkpoint.
They do not establish that a retrained shallow or differently wired system
could not do the same job. Comparing depth requires appropriate trained
controls, repeated seeds and accounting for added resources. Recursive depth,
number of populations, repair iterations and planning horizon are separate
quantities. Evolution may select proposed wiring and parameters as genes;
that search cost and its supplied founder controls must also be reported.

## 10. Why numerical qualification is necessary but insufficient

Several quantities that were previously easy to conflate have different jobs:

| Quantity | Meaning |
| --- | --- |
| Equation residual | How well the returned state satisfies its declared numerical equations. Small iterate movement is not a substitute. |
| Local curvature | A numerical check of a stated local energy geometry where that energy and its hypotheses apply; not global uniqueness or a global minimum certificate. |
| Semantic mismatch | Disagreement between observations or representations, which can remain at a valid compromise. |
| Inference approximation | Difference between a chosen approximate posterior and the exact target distribution, even at perfect solver convergence. |
| Parameter or memory motion | A change occurred; it may help, harm or be behaviorally irrelevant. |
| Measured learning | An independently evaluated response improves because of retained changes, with suitable restoration or frozen controls. |
| Useful capability | The behavior works across its declared cases, retains earlier skills and meets the resource contract. |

Fixed-weight contraction and stable-phase EP results do not automatically cover
moving parameters, adaptive precisions or learned overlap maps during the same
solve. Termination and local confluence require their actual assumptions.
Uniqueness for one starting state or protected boundary must not be promoted to
uniqueness across different histories. A directed fly graph does not inherit
the reciprocal energy theorem by sharing the project name.

All failed phases, capped attempts, rejected events and fallback work remain
in the receipt. A rollback test may pass because a capped solve was correctly
rejected; the solve itself remains unqualified. An externally supplied dense
solver can be a useful reference or engineering option, but does not prove
that the candidate runs using only its proposed local repairs.

## 11. The M4-first scale gate and full core replacement

The owner requires small local tests before larger experiments or training.
The M4 computer is the present inexpensive development platform, not a claim
that a result observed on this machine generalizes to every deployment. The
resource policy and allowed exceptions belong to the [local-first plan](../../plan/CADENCE_LOCAL_FIRST_FLY_GATES_2026-09-28.md).
This battery uses isolated bounded tasks; it does not authorize a cloud run,
restart a paused campaign or fetch a large model.

Passing a handful of algebra checks does not waive the remaining 34 bounded
capability contracts. Nor should mathematical proof, a constructed witness and
empirical learning be forced into one interchangeable “pass” field. The same
selected candidate must carry the required evidence across those axes before
the scale gate can be reconsidered.

Completely replacing the current building blocks additionally requires:

| Gate | Required decision |
| --- | --- |
| R1 — one primitive | Show the common operation actually executed for response and retained change; a wrapper around separate inference and update mechanisms is insufficient. |
| R2 — joint repair and federation | Establish supported topologies, schedules, boundary sufficiency and feedback under the candidate's precise hypotheses. |
| R3 — owned experience and continuation | Verify event ownership, finite deduplication policy, private imagination, cap rollback and exact continuation. |
| R4 — learned capabilities in the same candidate | Meet all required bounded capability contracts with their separate evidence axes; do not stitch candidates or waive missing rows. |
| R5 — integrated continuing operation | Maintain earlier abilities in one ongoing system and show that added observers earn their cost. |
| R6 — numerical and resource reliability | Handle nonfinite states, invalid parameters, caps, overload and failure accounting without false admission or hidden work. |
| R7 — retire current contracts deliberately | Inventory existing APIs and applications, provide tested replacements or explicit converters, and identify any remaining legacy dependency. Keeping a required old primitive means replacement is partial. |
| R8 — production and independent review | Validate installation, platforms, supported backends, documentation, tests and independent review of the complete candidate. |

These are review gates, not automatic consequences of a successful program
exit. Current `core_replacement_ready` remains false. The scalar candidate's
explicitly separate operations do not satisfy R1; that observation is about
this implementation, not an impossibility proof for the whole hypothesis.
The released core remains available while a replacement is investigated.

## 12. What one-command automation now means

The requested improvement is to stop manually running disconnected checks for
hours. The suite has one entry point, a complete catalogue and small isolated
candidate tasks. It reports every capability and readiness gate, including
what it cannot test. It does not manufacture 34 completed protocols from a
34-row list.

The initial candidate-facing tests are seven slices: opposite histories,
bounded source ownership, scalar acquisition, A→B→A switching, actual belief
readback, cap rollback and bounded resources. Three additional candidate
challenges test a directed fly transition, an inconsistent cycle and a joint
federation boundary. They remain separate challenges, not automatic discharge
of P2 or O1. Transported gauge checks, the preserved self-observation package
and prior-game arithmetic are reference evidence where supported.

The initial adapters are `normal-gamma` and `finite-cluster`. `--all` runs them
separately. It does not borrow one candidate's tree inference to fill the
other's missing structure or borrow the other's retained scalar learner to
claim the tree learned it. A reference replay verifies its own source-bound
package, not the selected candidate's ability to reproduce its science.

The five statuses have deliberately limited meanings:

| Status | Interpretation |
| --- | --- |
| `PASS` | This actual local task met its frozen checks within its stated scope. |
| `FAIL` | A completed execution violated the tested requirement. |
| `UNSUPPORTED` | The selected candidate lacks the declared interface or representation; no substitute answer was credited to it. |
| `NOT_TESTED` | The relevant complete protocol or harness is absent, or an optional reference was not requested or available. |
| `ERROR` | Execution, custody, output validation or a deadline failed; the attempted work and error remain visible. |

A bounded probe pass leaves the broader criterion untested. The initial
catalogue marks every complete capability contract as not yet ready. There
is no meaningful percentage of “brain functions achieved” from these thin
slices. D4 cannot pass because separate fresh objects happen to pass unrelated
checks. Readiness requires additional evidence and review, not a status rename.

The [protocol](../PROTOCOL.md) fixes the concrete values and budgets. Candidate
tasks have a 10-second process limit and 8 KiB output cap; the scalar resource
sample has its own 24-event, 4 KiB and two-second limits. Two local workers are
the default. Reference checks have separate 60-second and 64 KiB limits. Actual
sources and candidate identities are pinned, outputs refuse overwrite, and
verification must use matching candidate/reference flags. Exit zero can mean
an honestly reproduced scientific failure; it never means the core is ready.

Use the [README commands](../README.md#run-it) for execution and verification,
the [adapter guide](ADDING_A_CANDIDATE.md) to add a real implementation, and
[architecture guide](ARCHITECTURE.md) for the evidence flow. Results belong to
their source-bound receipts. This discussion does not anticipate outcomes from
a battery run that has not yet been verified.

## 13. The decisions that remain after the first fixtures

The immediate scientific work is to identify a genuinely common executed
operation, preserve witnessed memory without echo, infer changing contexts,
and show local readback and feedback in one candidate. Composition must retain
the required correlations; a directed-wiring adapter must disclose what it
changes. An integrated tiny body should then expose whether retained models
and actual actions work together before a larger benchmark is attempted.

The provisional failures are useful constraints. Stationary pooling explains
the scalar context failure. Distinct accumulation and readout operations leave
the one-rule claim open. A tree solver's exactness under supplied factors does
not establish learned structure or actual self-observation. A stochastic
two-bin fly bridge does not establish original continuous dynamics. None of
these statements refutes every possible recursive repair system, and none
licenses promoting a successful toy into the complete thesis.

Preserve failed candidates and their receipts. Propose changed rules or tests
as new versions before inspecting their outcomes. Keep the original controls,
charge supplied structure and search, and require the same continuing candidate
to earn each additional capability. Automation makes this process easier to
repeat; it cannot replace the missing definitions, proofs or experiments.
