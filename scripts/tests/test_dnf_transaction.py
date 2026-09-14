# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Optional
import unittest


REPO = Path(__file__).resolve().parents[2]
RUNNER = REPO / "ci" / "run-dnf-transaction"


def make_command(root: Path, body: str) -> Path:
    command = root / "dnf"
    command.write_text("#!/usr/bin/env bash\nset -Eeuo pipefail\n" + body, encoding="utf-8")
    command.chmod(0o755)
    return command


def invoke(
    root: Path,
    *,
    timeouts: str,
    budget: int,
    delay: int = 0,
    kill_after: int = 1,
    command: Optional[list[str]] = None,
) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PATH"] = f"{root}{os.pathsep}{environment['PATH']}"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--evidence",
            str(root / "transaction.json"),
            "--budget-seconds",
            str(budget),
            "--attempt-timeouts-seconds",
            timeouts,
            "--retry-delay-seconds",
            str(delay),
            "--kill-after-seconds",
            str(kill_after),
            "--",
            *(command or ["dnf", "-y", "install", "demo"]),
        ],
        cwd=REPO,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


class DnfTransactionTests(unittest.TestCase):
    def test_retry_records_each_attempt_and_uses_the_reviewed_network_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_command(
                root,
                """
count_file=${DNF_TEST_COUNT:?}
args_file=${DNF_TEST_ARGS:?}
cache_file=${DNF_TEST_CACHE:?}
count=0
[[ ! -f $count_file ]] || count=$(cat "$count_file")
count=$((count + 1))
printf '%s' "$count" >"$count_file"
printf '%s\\n' "$*" >>"$args_file"
if ((count == 1)); then
  printf cached >"$cache_file"
  exit 92
fi
[[ -f $cache_file ]]
""",
            )
            os.environ["DNF_TEST_COUNT"] = str(root / "count")
            os.environ["DNF_TEST_ARGS"] = str(root / "args")
            os.environ["DNF_TEST_CACHE"] = str(root / "cache")
            try:
                completed = invoke(root, timeouts="2,2", budget=6)
            finally:
                os.environ.pop("DNF_TEST_COUNT", None)
                os.environ.pop("DNF_TEST_ARGS", None)
                os.environ.pop("DNF_TEST_CACHE", None)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            evidence_path = root / "transaction.json"
            self.assertEqual(evidence_path.stat().st_mode & 0o777, 0o644)
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            self.assertEqual(evidence["status"], "passed")
            self.assertEqual(evidence["exit_code"], 0)
            self.assertEqual([item["exit_code"] for item in evidence["attempts"]], [92, 0])
            self.assertTrue(all("elapsed_seconds" in item for item in evidence["attempts"]))
            self.assertEqual(
                evidence["network_options"],
                [
                    "--setopt=retries=20",
                    "--setopt=timeout=60",
                    "--setopt=minrate=1000",
                    "--setopt=max_parallel_downloads=1",
                ],
            )
            argument_lines = (root / "args").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(argument_lines), 2)
            self.assertEqual(argument_lines[0], argument_lines[1])
            self.assertIn("--setopt=minrate=1000", argument_lines[0])
            self.assertNotIn("--setopt=minrate=1 ", argument_lines[0])

    def test_timeout_terminates_the_dnf_process_group_and_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            marker = root / "terminated"
            make_command(
                root,
                """
trap 'printf terminated >"${DNF_TERM_MARKER:?}"; exit 143' TERM
sleep 30 &
wait
""",
            )
            os.environ["DNF_TERM_MARKER"] = str(marker)
            try:
                completed = invoke(root, timeouts="1", budget=3)
            finally:
                os.environ.pop("DNF_TERM_MARKER", None)
            self.assertEqual(completed.returncode, 124, completed.stderr)
            self.assertTrue(marker.is_file(), "DNF did not receive container-local TERM")
            evidence = json.loads((root / "transaction.json").read_text(encoding="utf-8"))
            self.assertEqual(evidence["status"], "failed")
            self.assertEqual(evidence["exit_code"], 124)
            self.assertEqual(len(evidence["attempts"]), 1)
            self.assertTrue(evidence["attempts"][0]["timed_out"])

    def test_rejects_a_policy_whose_worst_case_exceeds_the_total_budget(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_command(root, "exit 0\n")
            completed = invoke(root, timeouts="2,2", budget=5, delay=1, kill_after=1)
            self.assertEqual(completed.returncode, 2)
            self.assertIn("exceed the total budget", completed.stderr)
            self.assertFalse((root / "transaction.json").exists())

    def test_rejects_a_caller_override_of_the_protected_network_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_command(root, "exit 0\n")
            completed = invoke(
                root,
                timeouts="1",
                budget=2,
                command=["dnf", "--setopt=minrate=1", "install", "demo"],
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("cannot override protected DNF option minrate", completed.stderr)
            self.assertFalse((root / "transaction.json").exists())


if __name__ == "__main__":
    unittest.main()
