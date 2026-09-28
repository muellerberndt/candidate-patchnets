# Current population qualification profile

This profile runs the sibling Cadence 0.48.0 population implementation through
its real public methods. It reuses `criteria.json`'s 34 capability requirements
and R1–R8 replacement gates. Historical adapters and receipts never populate its
current-source results.

```sh
python3 cadence-candidate-test-suite/current_population.py --out /tmp/population-smoke.json
python3 cadence-candidate-test-suite/current_population.py --verify /tmp/population-smoke.json
python3 -m unittest discover -s cadence-candidate-test-suite -p test_current_population.py -v
```

The first command starts one isolated Python worker with a 270-second deadline,
leaving 30 seconds of the declared five-minute local M4 budget for reporting.
It needs Python 3.11+ and the standard library. No network, ROM, tensor package
or reference experiment is needed. The worker is terminated on timeout and its
already flushed attempts remain in the report. Existing receipts are never
overwritten. With `--out`, stdout contains a compact summary; without it the
complete JSON receipt is printed. Exit 0 means all six diagnostic probes passed, 1 means a completed
probe failed, and 2 means execution/evidence errors. **None means full-brain
readiness.** All complete capability and replacement contracts remain unpassed.

## Frozen diagnostic scope

The protocol is `current_protocol.json`. It fixes seed, layout, fixture,
acceptance thresholds and resource limits before execution. Deliberately chosen
sizes and thresholds are controls, not evolved or generally optimal settings.

| Probe | What is checked | What is excluded |
| --- | --- | --- |
| Numerics | One-patch unclamped response against a closed form; joint witness parameter repair against an independent bisection solution under the original anchor; unclamped recall | Arbitrary-graph theorem, uniqueness or confluence |
| Pure query | Query and hypothetical-clamp purity; zero-budget refusal; live-state step leaves parameters and witness count unchanged | Planning, imagination policy or new experience |
| Witness custody | Capped admission rollback, retry, duplicate, conflicting/older identifier rejection, allowed identifier gaps | Authentication, asynchronous producers or episodic recall |
| Continuation | Exact checkpoint, subsequent query, duplicate, actual admission and live-step continuation | Cross-version migration or biological memory |
| Reciprocity | Perturb each population and measure the other within the same solve; exact error-readback edges exist | Learned metacognition, useful depth or cut-feedback advantage |
| Acquisition | Flat four-patch, composed 4+2 and recursive 4+2 populations; seeds 0/1/2; 40 ordered immediate witnesses each; subsequent unclamped error versus their unchanged initial response | Raw perception, reinforcement learning, broad reliability or integrated cognition |

Acquisition uses `y=0.6*x`: teaching inputs ±0.8 and ±0.4; assessment inputs ±0.5
and ±0.3. Assessment must have maximum absolute error at most 0.15 and MSE at
most one quarter of the frozen initialization's MSE. Every planned case and
admission stays visible. The separate `checks` amplitudes ±0.6 and ±0.2 are
available to the defaults-qualification lane but are not used for selection in
this smoke profile. Three independent seeds/layouts are separate small brains;
their successes are not pooled into an integrated continuing brain.

`current_fixtures.make_fixture(name)` also supplies two-output independent
linear mixing and a `tanh(1.2*x)` family for defaults qualification. Each returns
JSON-safe `teaching`, `checks` and `assessments` lists with disjoint inputs,
input/output sizes, and a scope statement. Each row contains `inputs` and
`targets` mappings. All values are supplied normalized coordinates. An external
formula supplies actual immediate teaching witnesses; there is no sensory
encoder, reward credit, body controller or action execution. These known,
fixed assessment examples are held out from admission, not fresh independent
scientific confirmation.

## Evidence and accounting

The receipt includes exact hashes of the loaded core source files, profile,
catalogue, protocol and fixture data. Each constructed brain supplies its full
resolved configuration, its hash, layout, initial checkpoint and engine source
hashes. Source hashes are checked again after execution. A changed source is an
error, never a successful current-source report.

Every operation is written to an append-only journal before execution. Returned
results retain complete numerical diagnostics and `work`, including refused
and capped solves. Duplicate retries are counted separately from solves.
Exceptions and interrupted calls retain attempt identity and explicitly unknown
work; the library supplies no solver counters for an exception. The two
intentional custody validation errors are reported separately, not hidden.
The aggregate is recomputed from that journal. Wall time, parent-plus-worker
CPU, and maximum per-process RSS include interpreter/startup and journal-reading
overhead; final report assembly and output serialization are excluded. RSS is a
process high-water mark, not summed concurrent memory. Rejected work counts
toward cost. The local budget is not a production latency or GPU claim.

`--verify` independently checks hashes, inventory, configuration bindings and
accounting against the stored event journal and current source tree. It
recomputes acquisition error and acceptance from the logged unclamped outputs,
and rejects target clamps or a changed teaching schedule in those checks. It does
not independently replay all numerical updates or authenticate environmental
witnesses. Rerunning the first command is the execution replay; resource samples
will vary. Receipts must be regenerated after producer or core source changes.

Statuses are `PASS`, `FAIL`, `UNSUPPORTED`, `NOT_TESTED` and `ERROR`. A probe pass
is a bounded slice; it never upgrades its broad criterion to `PASS`. No native
delayed reward-credit or structural-growth interface is attributed to the
engine. Raw perception (#58), temporal credit (#57), retention (#60), planning
(#62), depth attribution (#59), and hardware/deadline claims (#64) remain explicit
follow-up contracts. Application protocols, matched conventional controls,
independent confirmation and all complete R1–R8 contracts are still required.
