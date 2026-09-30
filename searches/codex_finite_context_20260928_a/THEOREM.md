# Finite context filtering by one generic factor operation

This is a mathematical contract for the lane's proposed finite candidate, not
a result receipt. The model family, two latent contexts, two possible world
values, sensor likelihood, transition hazards and retained separator are
supplied controls. Successful inference in this family does not establish
learned observer formation, biological identification or general intelligence.

The proposed implementation uses the existing exact cluster-tree factor rule
for both a witnessed event and a read-only query. Its durable state is the
resulting joint boundary distribution. This removes the earlier Normal–Gamma
candidate's separate conjugate-statistic accumulation formula. The observation
compiler, normalization, boundary projection, custody and commit operations
remain explicit parts of the system; they must not disappear from its source
audit or cost accounting.

## Declared finite generative model

Let `A,B` be static binary relation parameters. Bit 0 denotes world value -2;
bit 1 denotes +2. The current latent context `c` is binary, and the world-value
bit is `q=theta_c`, with `theta_0=A` and `theta_1=B`. The initial joint law on
`(A,B,c)` is uniform unless a test explicitly declares a different fixture.

One witnessed event advances the hidden context according to

```text
T_h(c' | c) = 1-h if c'=c, and h otherwise,
h in {0, 1/16, 1/4}.
```

Each hazard is a separately identified candidate setting. It is not learned
within this model. A step is one admitted event, not a calibrated duration of
physical time. Repeated queries do not advance this transition.

For actual integer observations `y` in `{-8,...,8}`, define a normalized
likelihood

```text
L(y | mu) = 4^(-abs(y-mu)) / Z_mu,
Z_mu = sum_{z=-8}^8 4^(-abs(z-mu)),
mu in {-2,+2}.
```

The observation alphabet is symmetric, so `Z_-2=Z_+2`. All observation rows are
strictly positive. Rational arithmetic represents the law exactly. This is a
supplied discrete noise model, not a fit to biological sensory statistics.
Normalization is required even though its constant happens to cancel between
the two means for the current symmetric alphabet.

## The retained boundary and one-event joint problem

Suppose the retained state is a normalized joint law `pi(A,B,c)`. For a new
witnessed observation `y`, the joint factor model is

```text
J(A,B,c,c',q) ∝ pi(A,B,c)
                * T_h(c' | c)
                * L(y | mu(theta_c'))
                * 1[q=theta_c'].
```

The indicator is a deterministic normalized conditional: summing it over `q`
gives one for every parameter/context assignment. An unobserved output thus
cannot reweight the retained world distribution merely by existing. It becomes
meaningful evidence only if a separately declared actual observation constrains
it; the present output is derived, not witnessed.

The next memory is the normalized boundary marginal

```text
pi'(A,B,c') = L(y | mu(theta_c'))
             * sum_c T_h(c' | c)*pi(A,B,c) / Z,
```

where `Z` is the sum of the numerator over `(A,B,c')`. This displayed formula
is an independent mathematical oracle, not permission to add a task-specific
posterior updater beside the generic factor kernel. The implementation must
obtain the same joint by local factor settlement and boundary marginalization.
Its next memory uses `c'` as the next event's current context `c`.

Because the likelihood is positive, the prior has positive total mass, and
every transition row sums to one, `Z>0` for every allowed observation and
hazard. This conclusion still holds for a sparse prior or `h=0`. Intermediate
zeros must be treated as support restrictions, never divided by unconditionally.

The output law is the `q` marginal of the settled readout factor. A reported
numeric mean `-2*P(q=0)+2*P(q=1)` is measurement of that output law. It is not an
extra learned readout, a copied sensor value, or an observer's independent
choice. The underlying supplied relationship `q=theta_c` must remain visible.

## A valid cluster tree and its cost

A simple chain of prior, transition and likelihood scopes would lose the
running-intersection property for `A,B`. A valid explicit construction has:

- a central bag `(A,B,c,c')` holding `T_h(c'|c)` lifted across `A,B`;
- a prior leaf `(A,B,c)` holding the sole owned copy of `pi`;
- a likelihood leaf `(A,B,c')` holding the sole actual likelihood;
- a readout leaf `(A,B,c',q)` holding the deterministic conditional.

Each leaf connects to the central bag. Every variable's containing bags form
a connected subtree. The largest bag has four binary variables, or 16 entries;
the retained joint has 8 entries; full independent enumeration has 32 states.
The six directed messages carry complete separator tables. A two-pass schedule
needs six message replacements, but actual implementation checks, arbitrary
schedule work, normalization, marginalization and storage must also be counted.

This pays a fixed, explicit width in the tiny model. It is not a theorem that
an arbitrary recurrent network or larger context family keeps that width.
More latent parameters or coupling can require much larger joint separators.

## Exactness and retention theorem

**Finite claim.** Given the declared joint model, exactly owned factors, a
valid cluster tree, exact finite arithmetic, nonzero support, and the generic
sum-product message equations, the qualified cluster beliefs equal the
corresponding marginals of `J`. The retained boundary equals `pi'` above.

For an edge separating two parts of the tree, the outgoing message is the sum
of the sending side's product of owned factors over its variables outside the
separator. This statement holds at a leaf immediately. Induction along the
tree establishes it for each directed edge, since running intersection makes
the separator contain every variable shared with the other side. Multiplying
incoming messages with one bag's owned factor and normalizing therefore gives
its exact marginal. No factor or witnessed event is counted twice.

Under a fresh fair update schedule, each directed message eventually receives
the correct messages from its finite dependency subtree. Nonbacktracking
message dependencies on a tree are acyclic. Thus the equations have a unique
normalized positive-support solution for this supplied problem, and complete
sweeps reach that solution after a finite dependency-depth bound in exact
arithmetic. Fairness alone provides no uniform bound on redundant updates or
wall-clock time. A capped implementation must independently check its message
and separator-belief equations before admitting its state.

**Stream consequence.** If the initial `pi` is the declared prior and each
qualified event is admitted once, induction over events gives

```text
pi_t(A,B,c_t) = P(A,B,c_t | y_1,...,y_t)
```

for this hidden-context model. The earlier context path has been marginalized,
not forgotten incorrectly: static parameters and the current context are a
sufficient Markov boundary for future events under the declared assumptions.
An independent short-horizon oracle may enumerate the complete context path
to test this claim. The implementation must not use that oracle to generate
its own answers.

The retention operation is the same finite sum/product/normalization algebra
used in settlement. It does not insert a learned gradient, a conjugate update
or a second task-specific numerical rule. Whether this satisfies the complete
architectural one-rule requirement still needs source-level review of the
compiler, retained interface and event transaction. This small theorem cannot
automatically mark a general core-replacement gate as passed.

## Queries, event ownership and atomic state

A current-state query substitutes `T_0(c'|c)=1[c'=c]` and a unit likelihood.
Summing the joint over old context and output gives exactly the incoming
`pi`, including every parameter/context correlation. A query may repair a
private computational state, but cannot advance event time, alter memory,
count a likelihood or create an experienced reward. A future-prediction query
that advances context would be a different declared query contract.

Duplicate actual event identifiers must not trigger either another transition
or another likelihood. Both would change the model even if the repeated value
were identical. A cap or qualification failure must leave the old joint and
admitted-event cursor unchanged. Retaining the prospective result is an atomic
commit after qualification, not another numerical learning operation.

Checkpoint validation must require a complete 8-state nonnegative joint with
exact sum one, valid fixed hazard/model identity, and the declared event-custody
fields. A mathematically valid arbitrary prior does not authenticate a claimed
sensor history. Tests that inject arbitrary distributions are explicitly
initial-state/property fixtures; they must not masquerade as learned memories.
This distinction is essential when testing restoration or malicious overwrite.

## Correlations, symmetry and identifiability

The transformation

```text
(A,B,c) -> (B,A,1-c)
```

preserves every public world value, likelihood and symmetric transition. It
also preserves the uniform prior. Context labels are therefore unidentifiable:
the model may infer a public value or switching pattern without choosing a
unique private name for each context. If `A=B`, observations cannot distinguish
the two contexts at all. These are genuine model symmetries, not failed repair.
No readout should reward an arbitrary label choice as recovered knowledge.

Keeping only singleton parameter/context marginals destroys relevant meaning.
For example, the normalized joint laws

```text
pi_zero = 1/2 at (A,B,c)=(0,1,0), and 1/2 at (1,0,1)
pi_one  = 1/2 at (A,B,c)=(0,1,1), and 1/2 at (1,0,0)
```

have identical uniform marginals for `A`, `B` and `c`. Yet `q` is certainly 0
under the first and certainly 1 under the second. Their label-swapped halves
represent the same public result within each law. Replacing either joint by
the product of its marginals makes `P(q=1)=1/2`, erasing that learned/public
distinction. This is a cheap exact counterexample to marginal-only retention.

For `y=0`, the likelihood is equal under -2 and +2. Such an actual event adds
no emission information, so the parameter marginal `P(A,B)` is unchanged.
Its context may nevertheless advance under `T_h`; a query must instead leave
the entire joint unchanged. These two tests distinguish a missing/neutral cue
from an accidental clock step or fabricated evidence.

## Scientific negatives and required controls

The query graph is a jointly conditioned factor model, not a proof of general
recursive self-observation. Latent `c` describes a possible world regime; it
does not inspect another patch's actual current belief, confidence or repair
residual. The deterministic readout is likewise a world relation. Actual
belief-readback interfaces must remain unsupported until they are implemented
and independently tested.

An A→B→A endpoint success alone cannot identify useful retention or parameter
learning. A reset-prior one-event control can already infer the most recent
observed value from the supplied sharply peaked likelihood. Compare that
control, pre-outcome predictions and a neutral-cue/history test. A model with
known fixed `A=0,B=1` can also infer context: it is a supplied-structure control,
not proof that learning unknown parameters caused an improvement.

The zero-hazard candidate pools evidence under a fixed context. Nonzero hazards
permit switching because switching is explicitly in their supplied model.
Selecting a hazard after seeing a development battery is architecture search,
not held-out confirmation. Keep every prespecified setting and failed task in
the record; do not claim a universal best hazard or biological timescale.

The result, if validated, concerns exact forward filtering on a temporal model
compiled into finite cluster trees. It is not general loopy belief propagation,
confluence for arbitrary repair moves, a globally fixed brain/world equilibrium,
continuous physical dynamics, learned structural growth, or a whole-connectome
model. Durable rational numerators/denominators can grow with event count even
though the table has only eight cells: table width is not a proof of bounded
memory in bits or uniform arithmetic cost. The implementation's declared
finite event horizon, integer domain, work caps and serialization limit remain
necessary parts of every qualified result.
