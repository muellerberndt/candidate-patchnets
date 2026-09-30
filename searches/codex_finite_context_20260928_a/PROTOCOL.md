# Codex lane: retained joint context through local conditioning

Frozen before candidate trials. This lane owns only this directory; the suite,
other search lanes, core and previous receipts are read-only. No staging or
commits. Local concurrency1, each child<=60seconds, artifacts<1MB, no cloud.
All three declared settings run; no outcome-based retuning or omitted failures.

## Candidate family

Two persistent unknown binary parameters A,B represent centers in{-2,+2}.
One hidden context C selects the active center. Initial joint P(A,B,C) is
uniform on8states. The only search parameter is supplied switching probability
h in {0,1/16,1/4}; its control is h=0. These are fixed candidate genes, not
learned transition laws or biology. Likelihood for integer y in[-8,8] is
`L(y|mu)=4^(-abs(y-mu))/sum(z=-8..8,4^(-abs(z-mu)))`.

Every real witness conditions the same four-cluster exact factor tree:

- prior on(A,B,C_previous);
- central transition on(A,B,C_previous,C_next), using P(C_next|C_previous);
- likelihood on(A,B,C_next);
- normalized deterministic answer relation on(A,B,C_next,Q), Q=A or B.

The central cluster connects to all three leaves. Largest table16entries,
32global assignments. Use the existing source-pinned local sum-product kernel.
The settled marginal on(A,B,C_next) becomes the next retained joint. Query uses
the same kernel with identity transition and unit likelihood; it cannot advance
time, add evidence or overwrite memory. Numerical work computes both the answer
and retained posterior; no conjugate coefficient increment or weight optimizer.
Boundary marginalization/renaming and transactional event admission are explicit.
This is exact finite filtering on a supplied tree model, not a biological circuit,
arbitrary recurrent solver, learned topology or actual belief self-observation.

One ordered source, capacity24, integer domain[-8,8]. Same latest ID/value is
idempotent; conflicting/stale/skipped IDs, derived records and overflow reject.
Cap256 sweeps. Commit requires the returned messages independently satisfy every
message equation and all separator beliefs. Zero-budget unfinished admission
must leave both joint and ledger unchanged. Persistent joint and cursor serialize.

## Frozen execution

1. For each h run all12events of A4/B4/A4 with A=-2,B=+2 under forward, reverse
   and synchronous schedules. Record every step, prior prediction and posterior
   distribution. Compare the full8-state joint after each event with an
   independent nested-sum Bayesian filter (never candidate message code).
   Equality is exact. A phase endpoint's error against its current center must
   be <=0.5 to pass that narrow switching task; report failures without retuning.
2. For every one of the32 length5 streams over{-2,+2}, advance only the first4
   events then score the last event before observing it. Use log predictive
   probability and squared center error. Compare full learning with a known
   parameter filter (A=-2,B=+2), a filter resetting the parameter prior after
   each event while preserving the context marginal, a last-value predictor
   using the same likelihood, and a frozen uniform predictor. This exhaustive
   uniform stream set is a diagnostic, not representative biological data or
   evidence that the learning candidate ought to win. No superiority threshold.
3. Same final neutral0 after three -2 or +2 witnesses: measure how history changes
   the posterior answer. Include reset-to-prior before that0. Also use pairs
   (-2,-2,+2,+2,0) and (+2,+2,-2,-2,0) to distinguish order-sensitive belief
   from a bag of observations. No claim of contextual recall from an unknowable
   cue:0 has identical emission likelihood under both centers.
   Also execute all eight fixed histories H1–H8 in SKEPTICAL_CONTROLS.md;
   report last-value, last-nonzero and fixed half-decay controls. Verify exact
   latent-label swap symmetry and quantify parameter/context dependence.
4. Preserve correlations: the two constructed joint laws
   0.5[(0,1,0)+(1,0,1)] and0.5[(0,1,1)+(1,0,0)] have equal singleton marginals
   but opposite certain Q. Query each and its product-of-singletons lesion.
   The lemma checks representational sufficiency, not learned acquisition of
   those constructed joints. In actual streams also compare the full retained
   joint with its product-of-singletons version without changing marginals.
5. Real y=0 advances context but cannot change the parameter joint. A read-only
   query preserves the whole memory byte-for-byte. Latest retries, checkpoint
   resume, rejected events and capped admission obey custody. A forged successful
   solver state with inconsistent messages must not commit. Test invalid snapshots.
6. Run the unchanged shared candidate battery separately for each h, jobs1,
   no reference replays needed (their frozen receipts remain available). The
   adapter uses this same exact kernel for the fly, holonomy and federation
   problems. Actual uncertainty readback remains UNSUPPORTED. All broad untested
   criteria and core-replacement gates remain unpassed. Shared-source drift
   invalidates that run rather than authorizing edits to another worker's files.

## Interpretation

This is a finite, context-dependent memory construction. The binary centers,
two slots, emission shape and switch probabilities are supplied. It cannot
learn an arbitrary real center, discover the number of contexts, infer goals
or demonstrate cortical/hippocampal implementation. Learned parameter dependence
must be separated from simply inferring an active state under supplied structure.
The endpoint switching score can be solved by a latest-value shortcut; the
pre-outcome, neutral-input and joint-lesion controls expose that alternative.

Success would justify a next small test of one common conditioning primitive,
not promotion to a complete brain. No current worker's candidate is displaced.
