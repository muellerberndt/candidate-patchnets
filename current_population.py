#!/usr/bin/env python3
"""Bounded current-population profile; no historical adapter results are read.

Every call is journaled before execution. Exceptions and killed workers retain
their attempted calls; unavailable work is unknown, never fabricated as zero.
The complete catalogue is reused, while every full-capability gate stays closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import resource
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

from battery import registry
from current_fixtures import make_fixture

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CORE = ROOT / "cadence/src"
STATUSES = {"PASS", "FAIL", "UNSUPPORTED", "NOT_TESTED", "ERROR"}
WORK = ("evaluations", "patch_visits", "edge_visits", "proposals", "backtracks")
PROBES = ("numerics", "pure", "custody", "continuation", "reciprocity", "acquisition")
SLICES = {
    "M2": ("custody", "Ordered witness ownership, not episodic retrieval."),
    "L1": (
        "acquisition",
        "Supervised scalar relation; no reward credit or depth advantage.",
    ),
    "O2": (
        "reciprocity",
        "Live state/error wiring with reciprocal intervention; no useful metacognition claim.",
    ),
    "O7": ("pure", "Pure hypothetical clamps, not learned imagination or planning."),
    "D2": (
        "custody",
        "Zero-budget refusal and atomic retry; not general damage recovery.",
    ),
}
UNSUPPORTED = {
    "L2": "No native delayed-reward temporal credit in this profile (#57).",
    "D1": "No within-life structural growth interface in the selected engine.",
}
DEPENDENCIES = {
    "raw_perception": 58,
    "temporal_credit": 57,
    "retention": 60,
    "planning": 62,
    "depth_attribution": 59,
    "hardware_deadlines": 64,
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def source_bindings():
    paths = set((CORE / "cadence").glob("*.py")) | {
        HERE / name
        for name in (
            "current_population.py",
            "current_fixtures.py",
            "current_protocol.json",
            "test_current_population.py",
            "criteria.json",
            "battery.py",
            "contract.py",
            "probes.py",
            "docs/CURRENT_POPULATION.md",
        )
    }
    return {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(paths)
    }


def peak_bytes(usage):
    # Darwin reports bytes; Linux and other supported Unix runners report KiB.
    return usage.ru_maxrss * (1 if sys.platform == "darwin" else 1024)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def build(layout="recursive", seed=0):
    from cadence import Cortex

    cortex = Cortex(seed=seed)
    signal = cortex.input("signal", shape=1)
    if layout == "scalar":
        final = cortex.column("base", patches=1, inputs=signal)
    else:
        base = cortex.column("base", patches=4, inputs=signal)
        if layout == "flat":
            final = base
        elif layout == "composed":
            final = cortex.column("upper", patches=2, inputs=(signal, base))
        elif layout == "recursive":
            final = cortex.observer("upper", patches=2, inputs=signal, observes=base)
        else:
            raise ValueError("Unknown layout")
    cortex.output("answer", shape=1, reads=final)
    return cortex.build()


class Journal:
    """Append-only, flushed attempt log owned by one worker process."""

    def __init__(self, path):
        self.path = Path(path)
        self.probe = "setup"
        self.calls = 0
        self.brains = {}

    def emit(self, kind, **fields):
        with self.path.open("a") as output:
            output.write(canonical({"kind": kind, **fields}) + "\n")

    def register(self, brain, name):
        layout = brain.inspect()
        self.brains[id(brain)] = name
        self.emit(
            "brain",
            name=name,
            config=dict(brain.config),
            config_sha256=digest(dict(brain.config)),
            layout=layout,
            initial_checkpoint=brain.snapshot(),
        )
        return brain

    def call(self, brain, method, *args, expected_error=False, **kwargs):
        self.calls += 1
        number = self.calls
        self.emit(
            "attempt",
            call=number,
            probe=self.probe,
            brain=self.brains[id(brain)],
            method=method,
            args=args,
            kwargs=kwargs,
            expected_error=expected_error,
        )
        start = time.perf_counter()
        try:
            result = getattr(brain, method)(*args, **kwargs)
        except Exception as error:
            self.emit(
                "exception",
                call=number,
                error=f"{type(error).__name__}: {error}",
                expected=expected_error and isinstance(error, ValueError),
                elapsed_seconds=time.perf_counter() - start,
                solver_work=None,
                work_complete=False,
            )
            if expected_error and isinstance(error, ValueError):
                return None
            raise
        # Preserve the complete result, including every refused proposal's work.
        self.emit(
            "result",
            call=number,
            result=result,
            elapsed_seconds=time.perf_counter() - start,
        )
        require(not expected_error, "Invalid witness was accepted instead of raising")
        return result


def qualified(result):
    require(result.get("qualified") is True, f"Solver refused: {result.get('reason')}")
    return result


def numerical_probe(log, protocol):
    """Independent one-patch closed form and bisection, not clamped accuracy."""
    brain = log.register(build("scalar"), "numerics")
    value = 0.7
    prior = brain.config["state_prior"]
    w, b = brain.weights[0], brain.biases[0]
    answer = qualified(log.call(brain, "settle", {"signal": [value]}))
    expected = math.tanh(w * value + b) / (1 + prior)
    error = abs(answer["outputs"]["answer"][0] - expected)
    require(
        error <= protocol["scalar_oracle_tolerance"], "Scalar query oracle mismatch"
    )
    target = 0.6
    penalty = brain.config["parameter_prior"]
    end = (math.atanh(target) - w - b) / 2
    low, high = min(0, end), max(0, end)
    for _ in range(80):
        t = (low + high) / 2
        p = math.tanh(w + b + 2 * t)
        derivative = (p - target) * (1 - p * p) + penalty * t
        if derivative < 0:
            low = t
        else:
            high = t
    delta = (low + high) / 2
    learned = qualified(
        log.call(brain, "observe", {"signal": [1.0]}, {"answer": [target]}, event_id=0)
    )
    parameter_error = max(
        abs(brain.weights[0] - w - delta), abs(brain.biases[0] - b - delta)
    )
    require(learned["accepted"], "Qualified witness did not commit")
    require(
        parameter_error <= protocol["scalar_oracle_tolerance"],
        "Witness oracle mismatch",
    )
    recalled = qualified(log.call(brain, "settle", {"signal": [1.0]}))
    recall_expected = math.tanh(w + b + 2 * delta) / (1 + prior)
    recall_error = abs(recalled["outputs"]["answer"][0] - recall_expected)
    require(
        recall_error <= protocol["scalar_oracle_tolerance"],
        "Unclamped recall oracle mismatch",
    )
    return {
        "query_error": error,
        "parameter_error": parameter_error,
        "unclamped_recall_error": recall_error,
        "scope": "One scalar fixture checks original prior/anchor objective numerically; no general convergence theorem.",
    }


def pure_probe(log, protocol):
    brain = log.register(build(), "pure")
    before = brain.snapshot()
    for targets in (None, {"answer": [0.7]}):
        qualified(log.call(brain, "settle", {"signal": [0.4]}, targets=targets))
        require(brain.snapshot() == before, "Pure query changed continuation")
    result = log.call(brain, "settle", {"signal": [0.4]}, budget=0)
    require(
        not result["qualified"] and result["reason"] == "budget", "Cap did not refuse"
    )
    require(brain.snapshot() == before, "Refused query changed continuation")
    live = qualified(log.call(brain, "step", {"signal": [0.4]}))
    require(live["accepted"], "Live state not accepted")
    saved = json.loads(before)
    require(
        list(brain.weights) == saved["weights"]
        and list(brain.biases) == saved["biases"],
        "Step learned without a witness",
    )
    require(brain.inspect()["admissions"] == 0, "Query or step fabricated a witness")
    return {"pure_checkpoint_equal": True, "step_witness_count": 0}


def custody_probe(log, protocol):
    brain = log.register(build(), "custody")
    inputs, targets = {"signal": [0.8]}, {"answer": [0.48]}
    original = brain.snapshot()
    capped = log.call(brain, "observe", inputs, targets, event_id=0, budget=0)
    require(
        not capped["accepted"] and capped["reason"] == "budget",
        "Expected refusal missing",
    )
    require(brain.snapshot() == original, "Capped admission partially committed")
    require(
        log.call(brain, "observe", inputs, targets, event_id=0)["accepted"],
        "Retry failed",
    )
    after = brain.snapshot()
    duplicate = log.call(brain, "observe", inputs, targets, event_id=0)
    require(
        duplicate
        == {"accepted": False, "qualified": True, "duplicate": True, "event_id": 0},
        "Latest identical retry contract failed",
    )
    require(brain.snapshot() == after, "Duplicate changed state")
    log.call(
        brain, "observe", inputs, {"answer": [-0.48]}, event_id=0, expected_error=True
    )
    require(brain.snapshot() == after, "Conflicting witness changed state")
    require(
        log.call(brain, "observe", inputs, targets, event_id=2)["accepted"],
        "Gap not allowed",
    )
    after = brain.snapshot()
    log.call(brain, "observe", inputs, targets, event_id=0, expected_error=True)
    require(brain.snapshot() == after, "Older witness changed state")
    return {
        "admissions": brain.inspect()["admissions"],
        "last_event_id": 2,
        "expected_validation_exceptions": 2,
        "scope": "Single ordered producer custody; application authenticates witness origin.",
    }


def continuation_probe(log, protocol):
    from cadence import Brain

    brain = log.register(build(), "continuation-original")
    first = {"signal": [0.8]}, {"answer": [0.48]}
    require(
        log.call(brain, "observe", *first, event_id=0)["accepted"],
        "First event refused",
    )
    saved = brain.snapshot()
    clone = log.register(Brain.from_snapshot(saved), "continuation-clone")
    require(clone.snapshot() == saved, "Checkpoint round trip differs")
    for method, args, kwargs in (
        ("settle", ({"signal": [-0.3]},), {}),
        ("observe", first, {"event_id": 0}),
        ("observe", ({"signal": [-0.8]}, {"answer": [-0.48]}), {"event_id": 1}),
        ("step", ({"signal": [-0.3]},), {}),
    ):
        left = qualified(log.call(brain, method, *args, **kwargs))
        right = qualified(log.call(clone, method, *args, **kwargs))
        require(
            left == right and brain.snapshot() == clone.snapshot(),
            "Continuation diverged",
        )
    return {
        "exact_continuation": True,
        "final_checkpoint_sha256": hashlib.sha256(
            brain.snapshot().encode()
        ).hexdigest(),
    }


def reciprocal_probe(log, protocol):
    brain = log.register(build(), "reciprocity")
    original = brain.snapshot()
    effects = {}
    for population, width, indices in (
        ("upper", 2, slice(0, 4)),
        ("base", 4, slice(4, 6)),
    ):
        pair = [
            qualified(
                log.call(
                    brain,
                    "settle",
                    {"signal": [0.3]},
                    interventions={population: [value] * width},
                )
            )
            for value in (-0.6, 0.6)
        ]
        effect = max(
            abs(a - b)
            for a, b in zip(pair[0]["state"][indices], pair[1]["state"][indices])
        )
        require(
            effect > protocol["reciprocal_min_effect"],
            "Joint returning influence absent",
        )
        effects[population] = effect
    require(brain.snapshot() == original, "Intervention fabricated experience")
    require(
        any(edge[0] == "residual" for edge in brain.graph.edges),
        "No error-readback edges",
    )
    return {
        "max_opposite_population_changes": effects,
        "scope": "Structural reciprocal intervention only; no cut-feedback advantage or learned metacognitive capability.",
    }


def acquisition_probe(log, protocol):
    fixture = make_fixture(protocol["fixture"])
    cases = []
    for layout in protocol["layouts"]:
        for seed in protocol["seeds"]:
            case = {"layout": layout, "seed": seed, "admitted": 0}
            try:
                brain = log.register(
                    build(layout, seed), f"acquisition-{layout}-{seed}"
                )

                def assess(brain=brain):
                    errors, predictions = [], []
                    for item in fixture["assessments"]:
                        result = qualified(log.call(brain, "settle", item["inputs"]))
                        value = result["outputs"]["answer"][0]
                        predictions.append(value)
                        errors.append(value - item["targets"]["answer"][0])
                    return {
                        "mse": sum(e * e for e in errors) / len(errors),
                        "max_error": max(map(abs, errors)),
                        "predictions": predictions,
                    }

                case["frozen"] = assess()
                for event_id in range(protocol["admissions"]):
                    item = fixture["teaching"][event_id % len(fixture["teaching"])]
                    result = log.call(
                        brain,
                        "observe",
                        item["inputs"],
                        item["targets"],
                        event_id=event_id,
                    )
                    case["admitted"] += int(result["accepted"])
                case["learned"] = assess()
                passed = (
                    case["admitted"] == protocol["admissions"]
                    and case["learned"]["max_error"] <= protocol["max_assessment_error"]
                    and case["learned"]["mse"]
                    <= protocol["max_mse_fraction_of_frozen"] * case["frozen"]["mse"]
                )
                case["status"] = "PASS" if passed else "FAIL"
            except AssertionError as error:
                case.update(status="FAIL", detail=str(error))
            except Exception as error:  # noqa: BLE001 -- retain every scheduled case on engine failure
                case.update(status="ERROR", detail=f"{type(error).__name__}: {error}")
            cases.append(case)
    statuses = {case["status"] for case in cases}
    return {
        "status": "ERROR"
        if "ERROR" in statuses
        else "FAIL"
        if "FAIL" in statuses
        else "PASS",
        "cases": cases,
        "scope": "Fixed scalar acquisition with withheld amplitudes across nine independent brains; not integrated competence or depth attribution.",
    }


FUNCTIONS = dict(
    zip(
        PROBES,
        (
            numerical_probe,
            pure_probe,
            custody_probe,
            continuation_probe,
            reciprocal_probe,
            acquisition_probe,
        ),
    )
)


def worker(path):
    sys.path.insert(0, str(CORE))
    import cadence

    log = Journal(path)
    protocol = json.loads((HERE / "current_protocol.json").read_text())
    require(
        Path(cadence.__file__).resolve().parent == CORE / "cadence",
        "Wrong imported Cadence",
    )
    require(
        cadence.__version__ == protocol["engine_version"],
        "Protocol/engine version mismatch",
    )
    log.emit(
        "setup", engine_version=cadence.__version__, protocol_sha256=digest(protocol)
    )
    for name in PROBES:
        log.probe = name
        start, cpu = time.perf_counter(), time.process_time()
        try:
            metrics = FUNCTIONS[name](log, protocol)
            status = metrics.pop("status", "PASS")
            require(status in STATUSES, "Invalid probe status")
            detail = "Declared bounded fixture executed"
        except AssertionError as error:
            status, metrics, detail = "FAIL", {}, str(error)
        except Exception as error:  # noqa: BLE001 -- runner boundary records unexpected errors
            status, metrics, detail = "ERROR", {}, f"{type(error).__name__}: {error}"
        log.emit(
            "probe",
            name=name,
            status=status,
            detail=detail,
            metrics=metrics,
            elapsed_seconds=time.perf_counter() - start,
            cpu_seconds=time.process_time() - cpu,
            process_peak_memory_bytes=peak_bytes(
                resource.getrusage(resource.RUSAGE_SELF)
            ),
        )


def tally(events):
    """Reconstruct accounting without treating incomplete calls as zero work."""
    attempts, completed = {}, {}
    total = {key: 0 for key in WORK}
    counters = Counter()
    unknown = []
    for event in events:
        kind = event["kind"]
        if kind == "attempt":
            require(event["call"] not in attempts, "Duplicate attempt identifier")
            attempts[event["call"]] = event
        elif kind in ("result", "exception"):
            number = event["call"]
            require(
                number in attempts and number not in completed,
                "Orphan/duplicate completion",
            )
            completed[number] = event
            if kind == "exception":
                require(
                    event["expected"]
                    == (
                        attempts[number]["expected_error"]
                        and event["error"].startswith("ValueError:")
                    ),
                    "Exception classification differs from attempted contract",
                )
                counters[
                    "expected_exceptions"
                    if event["expected"]
                    else "unexpected_exceptions"
                ] += 1
                # Core raises no solver-work payload. Even validation exceptions
                # remain explicitly unmetered instead of inventing counters.
                unknown.append(number)
                continue
            result = event["result"]
            if result.get("duplicate"):
                require("work" not in result, "Duplicate unexpectedly ran a solver")
                require(
                    result
                    == {
                        "accepted": False,
                        "qualified": True,
                        "duplicate": True,
                        "event_id": attempts[number]["kwargs"]["event_id"],
                    },
                    "Malformed duplicate",
                )
                counters["duplicates"] += 1
                continue
            require(type(result.get("qualified")) is bool, "Missing qualification")
            require(
                result.get("reason") in ("qualified", "budget", "line_search"),
                "Missing reason",
            )
            require(
                result["qualified"] == (result["reason"] == "qualified"),
                "Inconsistent qualification",
            )
            work = result.get("work")
            require(
                isinstance(work, dict) and set(work) == set(WORK), "Missing solver work"
            )
            for key in WORK:
                require(
                    type(work[key]) is int and work[key] >= 0, "Malformed solver work"
                )
                total[key] += work[key]
            require(
                type(result.get("sweeps")) is int and result["sweeps"] >= 0,
                "Missing sweeps",
            )
            counters["sweeps"] += result["sweeps"]
            counters["solves"] += 1
            counters["qualified" if result["qualified"] else "refused"] += 1
            counters["capped"] += int(result["reason"] == "budget")
            counters["line_search_refused"] += int(result["reason"] == "line_search")
            counters["admissions"] += int(
                attempts[number]["method"] == "observe"
                and result.get("accepted") is True
            )
            if attempts[number]["method"] in ("observe", "step"):
                require(
                    result.get("accepted") == result["qualified"],
                    "Admission differs from qualification",
                )
    unfinished = sorted(set(attempts) - set(completed))
    unknown.extend(unfinished)
    return {
        "attempts": len(attempts),
        **dict(counters),
        "work": total,
        "unfinished_calls": unfinished,
        "calls_without_work_payload": sorted(unknown),
        "solver_results_fully_metered": not unfinished
        and not counters["unexpected_exceptions"],
        "exception_work_note": "Expected pre-solve validation exceptions have no work payload; unknown work is never added as zero.",
    }


def check_event_contract(events, probes, protocol):
    """Reject empty greens and recompute acquisition from unclamped raw outputs."""
    setup = [event for event in events if event["kind"] == "setup"]
    require(
        len(setup) == 1
        and setup[0]["engine_version"] == protocol["engine_version"]
        and setup[0]["protocol_sha256"] == digest(protocol),
        "Missing or mismatched worker identity",
    )
    attempts = [event for event in events if event["kind"] == "attempt"]
    results = {
        event["call"]: event["result"] for event in events if event["kind"] == "result"
    }
    brains = {event["name"]: event for event in events if event["kind"] == "brain"}
    for call in attempts:
        require(call["brain"] in brains, "Unbound brain invocation")
        result = results.get(call["call"])
        if result and not result.get("duplicate"):
            tolerance = brains[call["brain"]]["config"]["tolerance"]
            require(
                result["qualified"] == (result["stationarity"] <= tolerance),
                "Reported qualification differs from measured stationarity",
            )
    for name, count in {
        "numerics": 3,
        "pure": 4,
        "custody": 6,
        "continuation": 9,
        "reciprocity": 4,
    }.items():
        if probes[name]["status"] == "PASS":
            require(
                sum(a["probe"] == name for a in attempts) == count,
                f"Missing attempts for {name}",
            )
    cases = probes["acquisition"]["metrics"].get("cases", [])
    if probes["acquisition"]["status"] == "PASS" or cases:
        scheduled = [
            (layout, seed)
            for layout in protocol["layouts"]
            for seed in protocol["seeds"]
        ]
        require(
            [(c["layout"], c["seed"]) for c in cases] == scheduled,
            "Missing scheduled acquisition case",
        )
        fixture = make_fixture(protocol["fixture"])
        assessments = fixture["assessments"]
        for case in cases:
            require(
                case["status"] in ("PASS", "FAIL", "ERROR"),
                "Invalid acquisition status",
            )
            if "learned" not in case:
                require(case["status"] != "PASS", "Unfinished acquisition cannot pass")
                continue
            name = f"acquisition-{case['layout']}-{case['seed']}"
            calls = [event for event in attempts if event["brain"] == name]
            require(
                len(calls) == 2 * len(assessments) + protocol["admissions"],
                "Acquisition attempt count differs",
            )
            for offset, phase in (
                (0, "frozen"),
                (len(calls) - len(assessments), "learned"),
            ):
                predictions, errors = [], []
                for call, item in zip(
                    calls[offset : offset + len(assessments)], assessments
                ):
                    require(
                        call["method"] == "settle"
                        and call["args"] == [item["inputs"]]
                        and call["kwargs"] == {},
                        "Assessment supplied a target or wrong input",
                    )
                    result = results[call["call"]]
                    require(result["qualified"], "Unqualified assessment cannot pass")
                    prediction = result["outputs"]["answer"][0]
                    predictions.append(prediction)
                    errors.append(prediction - item["targets"]["answer"][0])
                require(
                    case[phase]
                    == {
                        "mse": sum(e * e for e in errors) / len(errors),
                        "max_error": max(map(abs, errors)),
                        "predictions": predictions,
                    },
                    "Acquisition metrics differ",
                )
            admitted = 0
            for event_id, call in enumerate(
                calls[len(assessments) : -len(assessments)]
            ):
                item = fixture["teaching"][event_id % len(fixture["teaching"])]
                require(
                    call["method"] == "observe"
                    and call["args"] == [item["inputs"], item["targets"]]
                    and call["kwargs"] == {"event_id": event_id},
                    "Teaching schedule differs",
                )
                admitted += int(results[call["call"]]["accepted"])
            require(case["admitted"] == admitted, "Admission count differs")
            passed = (
                admitted == protocol["admissions"]
                and case["learned"]["max_error"] <= protocol["max_assessment_error"]
                and case["learned"]["mse"]
                <= protocol["max_mse_fraction_of_frozen"] * case["frozen"]["mse"]
            )
            require(
                case["status"] == ("PASS" if passed else "FAIL"),
                "Acquisition verdict differs",
            )
        expected_status = (
            "ERROR"
            if any(c["status"] == "ERROR" for c in cases)
            else "FAIL"
            if any(c["status"] == "FAIL" for c in cases)
            else "PASS"
        )
        require(
            probes["acquisition"]["status"] == expected_status,
            "Acquisition summary omitted failure",
        )


def inventory(probe_results):
    spec = registry()
    rows = []
    for criterion in spec["criteria"]:
        key, scope = SLICES.get(
            criterion["id"],
            (None, "No current-source executable slice in this profile."),
        )
        status = probe_results[key]["status"] if key else "NOT_TESTED"
        if criterion["id"] in UNSUPPORTED:
            status, scope = "UNSUPPORTED", UNSUPPORTED[criterion["id"]]
        rows.append(
            {
                "id": criterion["id"],
                "title": criterion["title"],
                "probe": key,
                "probe_status": status,
                "criterion_status": status
                if status in ("FAIL", "ERROR", "UNSUPPORTED")
                else "NOT_TESTED",
                "full_contract_ready": False,
                "scope": scope,
                "coverage": "bounded_slice" if key else "none",
            }
        )
    return rows, [
        {
            "id": row["id"],
            "title": row["title"],
            "status": "NOT_TESTED",
            "scope": "Requires its complete reviewed contract; slice passes do not promote this gate.",
        }
        for row in spec["readiness_gates"]
    ]


def assemble(events, sources, protocol, resource_record, errors):
    probes = {
        name: {
            "status": "ERROR",
            "detail": "Scheduled probe did not produce a result",
            "metrics": {},
        }
        for name in PROBES
    }
    seen = set()
    for event in events:
        if event["kind"] == "probe":
            name = event["name"]
            if (
                name not in probes
                or name in seen
                or event.get("status") not in STATUSES
            ):
                errors.append("Invalid or duplicate probe result")
            else:
                probes[name] = event
                seen.add(name)
    try:
        accounting = tally(events)
    except (AssertionError, KeyError, TypeError) as error:
        errors.append(f"Work accounting: {error}")
        accounting = {"solver_results_fully_metered": False}
    if accounting.get("unfinished_calls"):
        errors.append("Interrupted calls have unknown remaining work")
    if accounting.get("unexpected_exceptions"):
        errors.append("Unexpected operation exceptions remain in the journal")
    try:
        check_event_contract(events, probes, protocol)
    except (AssertionError, KeyError, TypeError) as error:
        errors.append(f"Fixture accounting: {error}")
    rows, gates = inventory(probes)
    return {
        "schema": "population-smoke/1",
        "candidate": f"cadence/{protocol['engine_version']}/population",
        "protocol": protocol,
        "protocol_sha256": digest(protocol),
        "data": make_fixture(protocol["fixture"]),
        "data_sha256": digest(make_fixture(protocol["fixture"])),
        "source_sha256": sources,
        "events": events,
        "events_sha256": digest(events),
        "probes": probes,
        "criteria": rows,
        "readiness_gates": gates,
        "cost": resource_record,
        "accounting": accounting,
        "errors": errors,
        "required_followup_contracts": {
            name: {"issue": issue, "status": "NOT_TESTED"}
            for name, issue in DEPENDENCIES.items()
        },
        "evidence_axes": {
            "mathematical_scope": "One scalar query/admission oracle; no general confluence theorem.",
            "expressibility": "Current population layouts and reciprocal state/error interventions.",
            "acquired_behavior": "Nine fixed immediate-witness scalar relations with unclamped assessment.",
            "held_out_confirmation": "NOT_TESTED: withheld amplitudes are diagnostic, not fresh independent confirmation.",
        },
        "historical_evidence_used": False,
        "all34_full_contracts_passed": False,
        "full_brain_ready": False,
        "core_replacement_ready": False,
        "execution_status": "ERROR"
        if errors or any(p["status"] == "ERROR" for p in probes.values())
        else "FAIL"
        if any(p["status"] == "FAIL" for p in probes.values())
        else "PASS",
    }


def validate_report(report, *, check_sources=True):
    """Independent receipt accounting/inventory verification, not training replay."""
    canonical(report)  # Reject nonfinite data anywhere, including resource fields.
    require(report["schema"] == "population-smoke/1", "Wrong schema")
    require(
        report["protocol_sha256"] == digest(report["protocol"]),
        "Protocol digest mismatch",
    )
    require(report["data_sha256"] == digest(report["data"]), "Data digest mismatch")
    require(
        report["events_sha256"] == digest(report["events"]), "Event digest mismatch"
    )
    require(
        report["data"] == make_fixture(report["protocol"]["fixture"]), "Fixture differs"
    )
    require(
        report["protocol"] == json.loads((HERE / "current_protocol.json").read_text()),
        "Protocol differs",
    )
    if check_sources:
        require(report["source_sha256"] == source_bindings(), "Source drift")
    expected = assemble(
        report["events"],
        report["source_sha256"],
        report["protocol"],
        report["cost"],
        list(report["errors"]),
    )
    for key in (
        "probes",
        "criteria",
        "readiness_gates",
        "accounting",
        "required_followup_contracts",
        "evidence_axes",
        "historical_evidence_used",
        "all34_full_contracts_passed",
        "full_brain_ready",
        "core_replacement_ready",
        "execution_status",
    ):
        require(report[key] == expected[key], f"Invalid derived field: {key}")
    for event in report["events"]:
        if event["kind"] == "brain":
            require(
                event["config_sha256"] == digest(event["config"]),
                "Brain config digest mismatch",
            )
            snapshot = json.loads(event["initial_checkpoint"])
            require(snapshot["config"] == event["config"], "Checkpoint config differs")
            for name, sha in snapshot["implementation"].items():
                require(
                    report["source_sha256"][f"cadence/src/cadence/{name}"] == sha,
                    "Engine binding differs",
                )
    require(
        report["cost"]["elapsed_seconds"] >= 0 and report["cost"]["cpu_seconds"] >= 0,
        "Invalid resource cost",
    )
    require(report["cost"]["peak_memory_bytes"] > 0, "Missing peak memory")
    return True


def run():
    start, cpu = time.perf_counter(), time.process_time()
    protocol = json.loads((HERE / "current_protocol.json").read_text())
    sources = source_bindings()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    errors, events = [], []
    with tempfile.TemporaryDirectory(prefix="cadence-population-") as directory:
        journal = Path(directory) / "calls.jsonl"
        try:
            child = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    "--worker",
                    str(journal),
                ],
                capture_output=True,
                text=True,
                timeout=protocol["worker_deadline_seconds"],
                check=False,
            )
            if child.returncode:
                errors.append(f"Worker exit {child.returncode}: {child.stderr[-2000:]}")
        except subprocess.TimeoutExpired:
            errors.append("Worker exceeded the frozen smoke deadline; terminated")
        if journal.exists():
            with journal.open("rb") as source:
                raw = source.read(protocol["max_journal_bytes"])
                if source.read(1):
                    errors.append(
                        "Journal exceeds resource cap; truncated work remains unknown"
                    )
            for line in raw.decode("utf-8", errors="replace").splitlines():
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    errors.append("Partial journal event after interrupted worker")
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    cost = {
        "elapsed_seconds": time.perf_counter() - start,
        "cpu_seconds": time.process_time()
        - cpu
        + after.ru_utime
        + after.ru_stime
        - before.ru_utime
        - before.ru_stime,
        "peak_memory_bytes": max(
            peak_bytes(after), peak_bytes(resource.getrusage(resource.RUSAGE_SELF))
        ),
        "memory_scope": "Maximum per-process RSS high-water mark, not summed simultaneous footprint; includes interpreter.",
        "cpu_scope": "Parent plus child user/system CPU, including refused work and startup.",
        "host": {
            "system": platform.system(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
    }
    if cost["elapsed_seconds"] > protocol["total_budget_seconds"]:
        errors.append("Total smoke budget exceeded")
    if source_bindings() != sources:
        errors.append("Current source changed during execution")
    return assemble(events, sources, protocol, cost, errors)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path, help="New JSON receipt path; never overwrites"
    )
    parser.add_argument(
        "--verify",
        type=Path,
        help="Verify receipt hashes/accounting against current sources",
    )
    parser.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        worker(args.worker)
        return
    if args.verify:
        report = json.loads(args.verify.read_text())
        validate_report(report)
        print(
            f"Receipt hashes, inventory and accounting verified; execution_status={report['execution_status']}; full_brain_ready=false."
        )
        return
    if args.out and args.out.exists():
        parser.error("Receipt exists; choose a new path")
    report = run()
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x") as output:
            output.write(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(
        canonical(
            report
            if not args.out
            else {
                "execution_status": report["execution_status"],
                "probes": {k: v["status"] for k, v in report["probes"].items()},
                "cost": report["cost"],
                "accounting": report["accounting"],
                "full_brain_ready": report["full_brain_ready"],
                "errors": report["errors"],
                "receipt": str(args.out) if args.out else None,
            }
        )
    )
    raise SystemExit(
        2
        if report["execution_status"] == "ERROR"
        else 1
        if report["execution_status"] == "FAIL"
        else 0
    )


if __name__ == "__main__":
    main()
