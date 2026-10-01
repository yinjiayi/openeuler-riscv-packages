# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO = pathlib.Path(__file__).resolve().parents[2]
HELPER = REPO / "ci" / "rpmbuild-timeout-budget.py"
SPEC = importlib.util.spec_from_file_location("rpmbuild_timeout_budget", HELPER)
if SPEC is None or SPEC.loader is None:
    raise AssertionError(f"cannot load {HELPER}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RpmBuildTimeoutBudgetTests(unittest.TestCase):
    def test_declared_boundaries_produce_positive_deadlines(self) -> None:
        for minutes in (5, 180, 360):
            with self.subTest(minutes=minutes):
                document = MODULE.start_budget(minutes, 300, 1_000)
                self.assertGreater(document["deadline_epoch"], 1_000)
                self.assertLess(document["deadline_epoch"], 1_000 + minutes * 60)

    def test_short_budget_clamps_the_evidence_reserve(self) -> None:
        document = MODULE.start_budget(5, 300, 1_000)
        self.assertEqual(document["effective_reserve_seconds"], 150)
        self.assertEqual(document["deadline_epoch"], 1_150)

    def test_invalid_policy_values_fail_closed(self) -> None:
        for minutes in (4, 361):
            with self.subTest(minutes=minutes):
                with self.assertRaises(ValueError):
                    MODULE.start_budget(minutes, 300, 1_000)
        for value in ("0", "-1", "1.5", " 180", "180 ", "abc"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    MODULE.parse_positive_integer("value", value)

    def test_remaining_budget_reports_ready_and_expired_states(self) -> None:
        ready, ready_status = MODULE.remaining_budget(2_000, 1_000)
        self.assertEqual(ready_status, 0)
        self.assertEqual(ready["remaining_seconds"], 1_000)
        expired, expired_status = MODULE.remaining_budget(1_000, 1_001)
        self.assertEqual(expired_status, 124)
        self.assertEqual(expired["classification"], "failure:infrastructure")

    def test_cli_records_deadline_and_structured_expiry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            github_output = root / "github-output"
            start_output = root / "start.json"
            subprocess.run(
                [
                    sys.executable,
                    str(HELPER),
                    "start",
                    "--timeout-minutes",
                    "180",
                    "--reserve-seconds",
                    "300",
                    "--now-epoch",
                    "1000",
                    "--output",
                    str(start_output),
                    "--github-output",
                    str(github_output),
                ],
                check=True,
            )
            self.assertEqual(github_output.read_text(), "deadline_epoch=11500\n")
            failure_output = root / "failure.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(HELPER),
                    "remaining",
                    "--deadline-epoch",
                    "11500",
                    "--now-epoch",
                    "11501",
                    "--output",
                    str(root / "remaining.json"),
                    "--failure-output",
                    str(failure_output),
                ],
                check=False,
            )
            self.assertEqual(completed.returncode, 124)
            self.assertIn('"failure:infrastructure"', failure_output.read_text())


if __name__ == "__main__":
    unittest.main()
