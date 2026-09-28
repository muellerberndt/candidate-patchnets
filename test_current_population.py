"""Adversarial receipt checks and tiny current-source execution tests."""

import json
import subprocess
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import current_population as profile
from current_fixtures import make_fixture


class FixtureTests(unittest.TestCase):
    def test_all_families_have_disjoint_supplied_inputs_and_owned_values(self):
        for name in ("scalar", "mixing", "nonlinear"):
            fixture = make_fixture(name)
            groups = [
                {tuple(row["inputs"]["signal"]) for row in fixture[key]}
                for key in ("teaching", "checks", "assessments")
            ]
            self.assertFalse(
                groups[0] & groups[1] or groups[0] & groups[2] or groups[1] & groups[2]
            )
            for key in ("teaching", "checks", "assessments"):
                for row in fixture[key]:
                    self.assertEqual(
                        len(row["inputs"]["signal"]), fixture["input_size"]
                    )
                    self.assertEqual(
                        len(row["targets"]["answer"]), fixture["output_size"]
                    )
            fixture["teaching"][0]["inputs"]["signal"][0] = 900
            self.assertNotEqual(fixture, make_fixture(name))

    def test_no_unknown_fixture_coercion(self):
        with self.assertRaises(ValueError):
            make_fixture("pong")


class ReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = profile.run()

    def mutated(self, change, rebind_events=False):
        result = deepcopy(self.report)
        change(result)
        if rebind_events:
            result["events_sha256"] = profile.digest(result["events"])
        return result

    def test_current_profile_passes_and_has_complete_unpromoted_inventory(self):
        report = self.report
        self.assertEqual(report["execution_status"], "PASS", report["errors"])
        self.assertTrue(profile.validate_report(report))
        self.assertEqual(len(report["criteria"]), 34)
        self.assertEqual(len(report["readiness_gates"]), 8)
        self.assertNotIn("PASS", {r["criterion_status"] for r in report["criteria"]})
        self.assertFalse(report["full_brain_ready"])
        self.assertFalse(report["historical_evidence_used"])
        self.assertEqual(len(report["probes"]["acquisition"]["metrics"]["cases"]), 9)

    def test_all_known_work_including_refusals_is_preserved(self):
        accounting = self.report["accounting"]
        self.assertEqual(accounting["attempts"], 458)
        self.assertEqual(accounting["solves"], 453)
        self.assertEqual(accounting["admissions"], 366)
        self.assertEqual(accounting["capped"], 2)
        self.assertEqual(accounting["refused"], 2)
        self.assertEqual(accounting["duplicates"], 3)
        self.assertEqual(accounting["expected_exceptions"], 2)
        self.assertEqual(len(accounting["calls_without_work_payload"]), 2)
        self.assertGreater(accounting["work"]["evaluations"], 453)
        self.assertLess(self.report["cost"]["elapsed_seconds"], 300)

    def test_false_full_readiness_or_missing_criteria_is_rejected(self):
        for change in (
            lambda r: r.update(full_brain_ready=True),
            lambda r: r.update(core_replacement_ready=True),
            lambda r: r["criteria"].pop(),
            lambda r: r["readiness_gates"].pop(),
            lambda r: r["criteria"][0].update(criterion_status="PASS"),
            lambda r: r.update(historical_evidence_used=True),
            lambda r: r["required_followup_contracts"].pop("retention"),
        ):
            with self.subTest(change=change), self.assertRaises(AssertionError):
                profile.validate_report(self.mutated(change))

    def test_unknown_work_or_refusal_cannot_be_omitted_from_summary(self):
        for key in ("capped", "refused", "expected_exceptions"):
            with self.subTest(key=key), self.assertRaises(AssertionError):
                profile.validate_report(
                    self.mutated(lambda r, key=key: r["accounting"].update({key: 0}))
                )

    def test_missing_return_preserves_unfinished_attempt_and_marks_error(self):
        events = deepcopy(self.report["events"])
        victim = next(
            event
            for event in events
            if event["kind"] == "result" and event["result"].get("reason") == "budget"
        )
        events.remove(victim)
        report = profile.assemble(
            events,
            self.report["source_sha256"],
            self.report["protocol"],
            self.report["cost"],
            [],
        )
        self.assertEqual(report["execution_status"], "ERROR")
        self.assertIn(victim["call"], report["accounting"]["unfinished_calls"])
        self.assertIn(
            victim["call"], report["accounting"]["calls_without_work_payload"]
        )

    def test_missing_work_duplicate_completion_and_invalid_qualification_fail(self):
        for mutate in (
            lambda event: event["result"].pop("work"),
            lambda event: event["result"].update(qualified=False),
            lambda event: event["result"]["work"].update(evaluations=-1),
            lambda event: event["result"].update(duplicate=True),
        ):
            result = deepcopy(self.report)
            event = next(e for e in result["events"] if e["kind"] == "result")
            mutate(event)
            result["events_sha256"] = profile.digest(result["events"])
            with self.assertRaises(AssertionError):
                profile.validate_report(result)
        events = deepcopy(self.report["events"])
        events.append(next(e for e in events if e["kind"] == "result"))
        with self.assertRaises(AssertionError):
            profile.tally(events)

    def test_nonfinite_result_or_mutated_engine_binding_is_rejected(self):
        result = deepcopy(self.report)
        event = next(e for e in result["events"] if e["kind"] == "result")
        event["result"]["energy"] = float("nan")
        with self.assertRaises(ValueError):
            profile.validate_report(result)
        result = deepcopy(self.report)
        result["source_sha256"]["cadence/src/cadence/brain.py"] = "0" * 64
        with self.assertRaisesRegex(AssertionError, "Source drift"):
            profile.validate_report(result)

    def test_assessment_target_clamp_cannot_be_scored_as_learning(self):
        result = deepcopy(self.report)
        event = next(
            e
            for e in result["events"]
            if e["kind"] == "attempt"
            and e["probe"] == "acquisition"
            and e["method"] == "settle"
        )
        event["kwargs"]["targets"] = {"answer": [0.3]}
        result["events_sha256"] = profile.digest(result["events"])
        with self.assertRaises(AssertionError):
            profile.validate_report(result)

    def test_forged_error_score_and_removed_seed_are_rejected(self):
        for mutation in ("score", "seed"):
            result = deepcopy(self.report)
            event = next(
                e
                for e in result["events"]
                if e["kind"] == "probe" and e["name"] == "acquisition"
            )
            if mutation == "score":
                event["metrics"]["cases"][0]["learned"]["mse"] = 0
            else:
                event["metrics"]["cases"].pop()
            result["events_sha256"] = profile.digest(result["events"])
            with self.assertRaises(AssertionError):
                profile.validate_report(result)

    def test_unexpected_exception_cannot_hide_behind_probe_pass(self):
        events = deepcopy(self.report["events"])
        event = next(e for e in events if e["kind"] == "result")
        number = event["call"]
        event.clear()
        event.update(
            kind="exception",
            call=number,
            error="RuntimeError: injected",
            expected=False,
        )
        result = profile.assemble(
            events,
            self.report["source_sha256"],
            self.report["protocol"],
            self.report["cost"],
            [],
        )
        self.assertEqual(result["execution_status"], "ERROR")
        self.assertEqual(result["accounting"]["unexpected_exceptions"], 1)

    def test_empty_or_missing_probe_cannot_become_green(self):
        for events in (
            [],
            [
                e
                for e in self.report["events"]
                if not (e["kind"] == "probe" and e["name"] == "pure")
            ],
            [e for e in self.report["events"] if e["kind"] in ("probe", "setup")],
        ):
            result = profile.assemble(
                events,
                self.report["source_sha256"],
                self.report["protocol"],
                self.report["cost"],
                [],
            )
            self.assertEqual(result["execution_status"], "ERROR")

    def test_fail_is_preserved_without_promotion_or_exception(self):
        events = deepcopy(self.report["events"])
        event = next(e for e in events if e["kind"] == "probe" and e["name"] == "pure")
        event.update(status="FAIL", detail="Synthetic failed purity condition")
        result = profile.assemble(
            events,
            self.report["source_sha256"],
            self.report["protocol"],
            self.report["cost"],
            [],
        )
        self.assertEqual(result["execution_status"], "FAIL")
        self.assertEqual(
            next(r for r in result["criteria"] if r["id"] == "O7")["criterion_status"],
            "FAIL",
        )


class ProcessFailureTests(unittest.TestCase):
    def test_worker_failure_or_timeout_preserves_complete_error_inventory(self):
        for effect in (
            subprocess.TimeoutExpired("worker", 270),
            SimpleNamespace(returncode=9, stderr="injected failure"),
        ):
            options = (
                {"side_effect": effect}
                if isinstance(effect, Exception)
                else {"return_value": effect}
            )
            with patch.object(profile.subprocess, "run", **options):
                result = profile.run()
            self.assertEqual(result["execution_status"], "ERROR")
            self.assertEqual(len(result["criteria"]), 34)
            self.assertEqual(len(result["readiness_gates"]), 8)
            self.assertEqual(
                {r["status"] for r in result["probes"].values()}, {"ERROR"}
            )

    def test_source_drift_cannot_be_green(self):
        before = profile.source_bindings()
        with patch.object(
            profile,
            "source_bindings",
            side_effect=[before, {**before, "injected": "drift"}],
        ):
            result = profile.run()
        self.assertEqual(result["execution_status"], "ERROR")
        self.assertIn("Current source changed during execution", result["errors"])

    def test_journal_flushes_attempt_and_exception_on_failure(self):
        class Broken:
            def settle(self):
                raise RuntimeError("boom")

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "attempts.jsonl"
            log, brain = profile.Journal(path), Broken()
            log.brains[id(brain)] = "broken"
            with self.assertRaises(RuntimeError):
                log.call(brain, "settle")
            events = [json.loads(line) for line in path.read_text().splitlines()]
        self.assertEqual([e["kind"] for e in events], ["attempt", "exception"])
        self.assertEqual(profile.tally(events)["calls_without_work_payload"], [1])


if __name__ == "__main__":
    unittest.main()
