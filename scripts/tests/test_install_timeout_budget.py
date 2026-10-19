# SPDX-License-Identifier: Apache-2.0
"""Bounded install budgets preserve full tests and time for failure evidence."""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
POLICY = REPO / "ci/package-policy.py"
BUDGET = REPO / "ci/rpmbuild-timeout-budget.py"


class InstallTimeoutBudgetTests(unittest.TestCase):
    def test_all_schema_minutes_have_bounded_install_policy(self):
        # Exercise the real policy CLI at the floor, default and upper bound.
        for minutes, expected in ((5, 70), (60, 70), (70, 70), (120, 120), (240, 240), (360, 360)):
            with self.subTest(minutes=minutes), tempfile.TemporaryDirectory() as tmp:
                root = pathlib.Path(tmp)
                package = root / "demo"
                package.mkdir()
                (package / "package.yaml").write_text(json.dumps({
                    "package_id": "demo",
                    "build": {"profile": "qemu-user", "timeout_minutes": minutes},
                }))
                subprocess.run([sys.executable, str(POLICY), "--package-dir", str(package),
                                "--output", str(root / "policy.json"),
                                "--github-output", str(root / "github-output")], check=True)
                document = json.loads((root / "policy.json").read_text())
                self.assertEqual(document["timeout_minutes"], minutes)
                self.assertEqual(document["install_timeout_minutes"], expected)
                self.assertIn(f"install_timeout_minutes={expected}\n", (root / "github-output").read_text())

    def test_invalid_policy_never_emits_a_job_budget(self):
        for minutes in (True, False, 4, 361, "240", 240.0, None):
            with self.subTest(minutes=minutes), tempfile.TemporaryDirectory() as tmp:
                root = pathlib.Path(tmp)
                package = root / "demo"
                package.mkdir()
                (package / "package.yaml").write_text(json.dumps({
                    "package_id": "demo", "build": {"profile": "qemu-user", "timeout_minutes": minutes},
                }))
                result = subprocess.run([sys.executable, str(POLICY), "--package-dir", str(package),
                                         "--output", str(root / "policy.json"),
                                         "--github-output", str(root / "github-output")], capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((root / "github-output").exists())
                self.assertFalse((root / "policy.json").exists())

    def test_setup_time_is_deducted_and_expiry_is_structured(self):
        for minutes in (70, 240, 360):
            with self.subTest(minutes=minutes), tempfile.TemporaryDirectory() as tmp:
                root = pathlib.Path(tmp)
                subprocess.run([sys.executable, str(BUDGET), "start", "--phase", "rpm-install-smoke",
                                "--timeout-minutes", str(minutes), "--reserve-seconds", "600",
                                "--now-epoch", "1000", "--output", str(root / "start.json"),
                                "--github-output", str(root / "github-output")], check=True)
                start = json.loads((root / "start.json").read_text())
                self.assertEqual(start["phase"], "rpm-install-smoke-timeout-budget")
                deadline = 1000 + minutes * 60 - 600
                self.assertEqual(start["deadline_epoch"], deadline)
                command = [sys.executable, str(BUDGET), "remaining", "--phase", "rpm-install-smoke",
                           "--deadline-epoch", str(deadline), "--output", str(root / "remaining.json"),
                           "--failure-output", str(root / "expired.json")]
                ready = subprocess.run(command + ["--now-epoch", "1123"], capture_output=True, text=True)
                self.assertEqual(ready.returncode, 0)
                self.assertEqual(int(ready.stdout), minutes * 60 - 600 - 123)
                self.assertFalse((root / "expired.json").exists())
                expired = subprocess.run(command + ["--now-epoch", str(deadline)], capture_output=True)
                self.assertEqual(expired.returncode, 124)
                self.assertEqual(expired.stdout, b"")
                document = json.loads((root / "expired.json").read_text())
                self.assertEqual(document["phase"], "rpm-install-smoke-timeout-budget")
                self.assertEqual(document["classification"], "failure:infrastructure")
                self.assertIn("rpm-install-smoke", document["message"])

    def test_workflow_binds_job_deadline_and_command_without_routing_changes(self):
        workflow = (REPO / ".github/workflows/package-ci.yml").read_text()
        job = workflow.split("\n  rpm-install-smoke:\n", 1)[1].split("\n  publish-rpm-repository:", 1)[0]
        self.assertIn("install_timeout_minutes: ${{ steps.policy.outputs.install_timeout_minutes }}", workflow)
        self.assertIn("timeout-minutes: ${{ fromJSON(needs.prepare.outputs.install_timeout_minutes || '70') }}", job)
        self.assertLess(job.index("Establish the validated install deadline"), job.index("Materialize only the exact package tree"))
        self.assertIn("--reserve-seconds 600", job)
        self.assertIn("INSTALL_DEADLINE_EPOCH: ${{ steps.install_budget.outputs.deadline_epoch }}", job)
        self.assertIn('--deadline-epoch "$INSTALL_DEADLINE_EPOCH"', job)
        self.assertIn('--max-bytes 52428800 --timeout-seconds "$install_timeout_seconds" --', job)
        self.assertNotIn("--timeout-seconds 3600", job)
        self.assertIn('ci/install-smoke.sh "packages/$PACKAGE_ID" "work/$PACKAGE_ID"', job)
        self.assertIn("if: always()", job)
        self.assertIn("github.ref == 'refs/heads/main'", job)
        self.assertIn("needs.prepare.outputs.needs_native != 'true'", job)


if __name__ == "__main__":
    unittest.main()
