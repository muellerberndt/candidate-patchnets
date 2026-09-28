# Cadence candidate test suite

**Final goal.** A patch-net equilibrium brain that is more scalable, more capable and more efficient than a transformer. Every Cadence result is measured against that goal at matched information, matched task and a declared resource model. The Amen jungle composer is the first test platform.

**Principles.** The main hypothesis stays: a brain that settles in global equilibria. The building block stays as simple as possible, like in nature, and every part of the brain answers with a settled state of that same patch rule; a feed-forward readout or a copied input is a baseline, never a result. Natural evolution is preferred to design: any parameter that looks designed is a gene, picked by selection against the hand-set value, which stays as the control. Within a life only the patch rule learns; across lives the genome evolves.

One command evaluates a candidate on small local tasks and reports **all34
capability criteria, eight replacement gates, and the additional fly/loop/
federation challenges**. This is the executable home for the redesign tests.

The initial suite implements **seven bounded capability probes and three
structural challenges**, not34 complete capability protocols. Every remaining
criterion is visible as `NOT_TESTED`; a missing candidate interface is
`UNSUPPORTED`. A passing small probe does not certify an entire brain function.
Neither current candidate is ready to replace Cadence core.

## Run it

From the enclosing `oph-meta` workspace:

```sh
python3 cadence-candidate-test-suite/run.py --all
```

This prints the complete report. Add `--out /tmp/my-candidate-report.json` to
save a machine-readable JSON receipt and a Markdown report beside it. Existing
reports are never overwritten. To reproduce the checked-in baseline:

```sh
python3 cadence-candidate-test-suite/run.py --all --verify cadence-candidate-test-suite/results/baseline.json
python3 -m unittest discover -s cadence-candidate-test-suite -v
```

Use `--candidate normal-gamma` or `--candidate finite-cluster` for one model,
`--adapter path/to/adapter.py` for another, and `--jobs 1` for sequential
execution. Two isolated workers are the default; at most four are allowed.
`--no-references` records that historical reference checks were omitted.
Use the same candidate/reference flags when verifying an earlier report.

The candidate workers need Python3.11+ and the standard library. The default
reference replay additionally uses the installed Node.js runtime and existing
workspace fixtures. Nothing downloads data, trains a game agent, starts cloud
compute or changes the public fly demo. Keep this directory beside
`cadence-flagship/`, `cadence-examples/` and `plan/`; it consumes their pinned
small artifacts. Reports are small local files.

An exit status0 means the invocation completed or reproduced its recorded
verdicts. It can include a scientific `FAIL`. Infrastructure errors and failed
reference verification exit2. **Read `core_replacement_ready`, not exit0, as
the readiness verdict:** it remains false. This runner has no automatic
promotion path.

## What runs through the selected candidate

| Probe | Question |
| --- | --- |
| History | Do different experiences change the answer to the same current input? |
| Source ownership | Can queries/retries fabricate evidence? Does checkpoint continuation preserve ownership? |
| Scalar acquisition | Does real experience improve a later prediction in the supplied model? |
| Context switch | Does an A→B→A stream track the changing situation? |
| Belief readback | Does actual lower uncertainty change the observer, and does observer feedback change the lower belief? |
| Cap rollback | Does an unfinished solve leave witnessed memory unchanged? |
| Resource bounds | Does a bounded stream respect its declared storage and runtime limits? |
| Fly transition | Can this candidate solve factors compiled from an actual directed four-neuron fly motif? |
| Holonomy/conflict | Can it represent a frustrated odd cycle and reject impossible hard constraints? |
| Federation boundary | Does it preserve shared correlations that singleton summaries lose? |

The two initial adapters deliberately expose different abilities. The
Normal–Gamma model retains scalar evidence and performs uncertainty readback;
the finite cluster model solves exact finite joint-factor trees. `--all`
reports them **separately**, and never combines their successes into a fictional
unified model.

## What remains reference evidence

The nine existing mini-experiment packages are replayed through their original
source-bound verifiers. They include transported gauge relabelings, exact
relation learning, federation algebra, actual fly-loop interventions,
self-observation, retained beliefs and the discrete fly adapter. The suite also
checks the preserved1942/C64/Atari evidence arithmetic when its inputs exist.
These checks are labeled `REFERENCE`: they are not a new candidate playing a
game or running the old experiment's solver as its own.

The fly fixture preserves imported cell identities, signed directed edges and
declared boundary omissions. Its two-bin transition compiler preserves
conditional potential means at one step, but adds substantial stochastic noise
and does not preserve the original multistep rate dynamics. This distinction is
part of the test, not hidden assistance.

## Documentation

- [Today’s discussion and decisions](docs/DISCUSSION_AND_DECISIONS_2026-09-28.md):
  hypotheses, mathematical and biological mappings, results and open questions.
- [Architecture and evidence flow](docs/ARCHITECTURE.md): what a candidate is,
  how tests run and why a reference pass cannot qualify it.
- [Adding a candidate](docs/ADDING_A_CANDIDATE.md): adapter contract and examples.
- [Evidence inventory and limits](docs/EVIDENCE.md): all existing local packages,
  their numerical outcomes and what they actually establish.
- [Frozen execution protocol](PROTOCOL.md) and [complete catalogue](criteria.json):
  every criterion, task, falsifier, scope and required evidence axis.
- [Replacement decision](../plan/CADENCE_LOCAL_FIRST_FLY_GATES_2026-09-28.md#when-replacing-the-current-building-blocks-becomes-justified)
  and [capability register](../plan/CADENCE_CAPABILITY_AND_PROOF_REGISTER.md):
  the owning requirements and the unchanged larger-run lock.

Current priorities are a genuinely common executed repair rule, inferred
context with retention, and an integrated small body test. Building a fast
runner removes repetitive execution work; designing discriminating tests and
proving their assumptions still requires scientific work.
