# Codex finite-context search lane

This lane is isolated from the concurrent Fable searches. Ownership, budget
and the suite revision are in [CLAIM.json](CLAIM.json). No shared suite/core
files are edited, no existing receipts are rewritten, and no commits are made.

The candidate asks whether one exact local conditioning kernel can both answer
queries and retain a context-dependent joint model. It uses the existing finite
factor primitive for every task, including the fly-derived factors; it adds no
gradient or conjugate-statistic update formula. It retains an eight-state joint
boundary over two unknown binary values and their current hidden context.

The architecture and its restrictions are in [THEOREM.md](THEOREM.md).
[PROTOCOL.md](PROTOCOL.md) freezes three supplied hazards and every main trial.
[SKEPTICAL_CONTROLS.md](SKEPTICAL_CONTROLS.md) motivates the adversarial controls;
its broader proposals are not all claimed as executed. The receipt specifies
exactly which controls ran. Actual belief self-observation remains unsupported.

[RESULTS.md](RESULTS.md) reports the first search round, every supplied setting,
the negative forecasting result, protocol deviations and replay commands.
Independent reviews are in [MATH_REVIEW.md](MATH_REVIEW.md) and
[EVIDENCE_REVIEW.md](EVIDENCE_REVIEW.md). The first bounded round is complete;
this directory contains no continuing background job.

Run from the workspace root:

```sh
python3 cadence-candidate-test-suite/searches/codex_finite_context_20260928_a/verify_round.py --verify
python3 -m unittest discover -s cadence-candidate-test-suite/searches/codex_finite_context_20260928_a
python3 cadence-candidate-test-suite/run.py --adapter cadence-candidate-test-suite/searches/codex_finite_context_20260928_a/adapter_h16.py --jobs 1 --no-references
```

The scientific receipt was produced by `probe.py`, which refuses to overwrite
it. The separate `verify_round.py` adds strict replay without changing that
receipt. All three adapters are evaluated separately. Missing or failing capabilities
stay visible. The model has two supplied slots and only two possible centers;
it is a tiny component hypothesis, not a complete brain or proof of mammalian
implementation. Exact rational tables also become expensive as width/history
increase. No large run or core promotion follows.

Use the supplemental strict verifier above for replay; the original probe's
comparison does not distinguish all JSON types. The frozen v1 checkpoint parser
also accepts formats whose parsing cost is not adequately bounded. It is for
the small trusted fixtures in this lane, not untrusted input or production use.
Both audit findings and the preserved source history are described in RESULTS.

## Why investigate this as a possible brain component?

The owner's biological constraint is functional: use mammalian and human brains
to ask what a reusable component must accomplish. Experience should help select
an interpretation of an ambiguous situation; incompatible experiences should
not always overwrite or collapse into one averaged value.

A mouse hippocampal study found that prior experience influenced contextual
remapping during virtual navigation. This motivates a history-sensitive context
test; it does not identify our factor equations with hippocampal circuitry.
[Plitt and Giocomo,2021](https://www.nature.com/articles/s41593-021-00816-6).

In humans, hippocampal–entorhinal activity patterns in an ambiguous virtual
context predicted context-dependent spatial behavior. This motivates retaining
uncertainty and measuring actual choices, rather than rewarding an arbitrary
internal context label. [Julian and Doeller,2021](https://www.nature.com/articles/s41593-021-00835-3).

A human single-neuron study linked learning to infer covert context switches
with an abstract context/stimulus representation. Transferring a changed rule to
an unseen stimulus is therefore a useful future discriminator. This binary toy
has no stimulus vocabulary and **cannot test that ability**.
[Abstract representations emerge in human hippocampal neurons during inference,2024](https://www.nature.com/articles/s41586-024-07799-x).

Those findings guide the tests; they are not evidence that the entire brain
implements this HMM, that simple endpoint tracking is contextual recall, or
that settlement is the only possible computational implementation.
