# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
AUDITOR = REPO / "ci" / "audit-required-context.py"
CONFIGURATOR = REPO / "ci" / "configure-github.sh"
REPOSITORY = "yinjiayi/openeuler-riscv-packages"


FAKE_GH = r'''#!/usr/bin/env python3
import json
import os
import pathlib
import sys

args = sys.argv[1:]
log_path = os.environ.get("FAKE_GH_LOG")
if log_path:
    with pathlib.Path(log_path).open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(args) + "\n")

if args[:2] == ["auth", "status"]:
    raise SystemExit(0)
if len(args) >= 2 and args[0] == "api" and args[1].startswith("repos/") and args[1] != "graphql":
    print(json.dumps({"visibility": "public", "default_branch": "main"}))
    raise SystemExit(0)
if args[:2] != ["api", "graphql"]:
    print("unexpected fake gh invocation", file=sys.stderr)
    raise SystemExit(90)

scenario = os.environ.get("FAKE_GH_SCENARIO", "success")
if scenario == "api-error":
    raise SystemExit(17)

query = next((item[6:] for item in args if item.startswith("query=")), "")
cursor = next((item[7:] for item in args if item.startswith("cursor=")), None)
context_pass = "statusCheckRollup" in query
head1 = "1" * 40
head2 = "2" * 40

def check(workflow="Auto Merge Policy", app="github-actions", check_id=1):
    return {
        "__typename": "CheckRun",
        "databaseId": check_id,
        "name": "configure",
        "status": "COMPLETED",
        "conclusion": "SUCCESS",
        "detailsUrl": "https://example.invalid/check/%d" % check_id,
        "checkSuite": {
            "app": {"slug": app},
            "workflowRun": {"databaseId": check_id + 100, "workflow": {"name": workflow}},
        },
    }

def status():
    return {
        "__typename": "StatusContext",
        "context": "configure",
        "state": "SUCCESS",
        "targetUrl": "https://example.invalid/status",
        "creator": {"login": "someone"},
    }

def pr(number, head, contexts, total=None, overflow=False, commit=None):
    return {
        "number": number,
        "url": "https://example.invalid/pr/%d" % number,
        "headRefOid": head,
        "commits": {"nodes": [{"commit": {
            "oid": commit or head,
            "statusCheckRollup": {"contexts": {
                "totalCount": len(contexts) if total is None else total,
                "pageInfo": {"hasNextPage": overflow, "endCursor": "nested" if overflow else None},
                "nodes": contexts,
            }},
        }}]},
    }

if context_pass:
    if cursor is None:
        nodes = [pr(1, head1, [check(check_id=1)])]
        next_page = True
        end_cursor = "context-page-2"
    elif cursor == "context-page-2":
        contexts = [check(check_id=2), check(check_id=3)]
        total = None
        overflow = False
        commit = None
        if scenario == "missing":
            contexts = []
        elif scenario == "status-context":
            contexts = [status()]
        elif scenario == "wrong-workflow":
            contexts = [check(workflow="Another Workflow", check_id=2)]
        elif scenario == "wrong-app":
            contexts = [check(app="another-app", check_id=2)]
        elif scenario == "overflow":
            contexts = [check(check_id=2)]
            total = 101
            overflow = True
        elif scenario == "head-mismatch":
            commit = "3" * 40
        nodes = [pr(2, head2, contexts, total=total, overflow=overflow, commit=commit)]
        next_page = False
        end_cursor = None
    else:
        raise SystemExit(91)
else:
    if cursor is None:
        nodes = [{"number": 1, "headRefOid": head1}]
        next_page = True
        end_cursor = "head-page-2"
    elif cursor == "head-page-2":
        verified_head = "4" * 40 if scenario == "unstable" else head2
        nodes = [{"number": 2, "headRefOid": verified_head}]
        next_page = False
        end_cursor = None
    else:
        raise SystemExit(92)

print(json.dumps({
    "data": {
        "repository": {"pullRequests": {
            "totalCount": 2,
            "pageInfo": {"hasNextPage": next_page, "endCursor": end_cursor},
            "nodes": nodes,
        }},
        "rateLimit": {"cost": 1, "remaining": 4999, "resetAt": "2026-09-03T00:00:00Z"},
    }
}))
'''


class RequiredContextAuditTests(unittest.TestCase):
    def environment(self, root: Path, scenario: str) -> tuple[dict[str, str], Path]:
        binary = root / "bin"
        binary.mkdir()
        fake_gh = binary / "gh"
        fake_gh.write_text(FAKE_GH, encoding="utf-8")
        fake_gh.chmod(0o755)
        log = root / "gh-calls.jsonl"
        env = dict(os.environ)
        env.update({
            "PATH": str(binary) + os.pathsep + env.get("PATH", ""),
            "FAKE_GH_SCENARIO": scenario,
            "FAKE_GH_LOG": str(log),
            "PYTHONDONTWRITEBYTECODE": "1",
        })
        return env, log

    def run_audit(self, scenario: str, expected: int) -> tuple[dict, list[list[str]]]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            env, log = self.environment(root, scenario)
            output = root / "audit.json"
            completed = subprocess.run(
                [
                    str(AUDITOR),
                    "--repository", REPOSITORY,
                    "--context", "configure",
                    "--expected-workflow", "Auto Merge Policy",
                    "--expected-app", "github-actions",
                    "--output", str(output),
                ],
                cwd=REPO,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, expected, completed.stderr)
            self.assertTrue(output.is_file())
            self.assertFalse(output.with_name(output.name + ".tmp").exists())
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(json.loads(completed.stdout), result)
            calls = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
            return result, calls

    def test_success_paginates_both_passes_and_allows_trusted_duplicates(self) -> None:
        result, calls = self.run_audit("success", 0)
        self.assertTrue(result["passed"])
        self.assertTrue(result["snapshot_stable"])
        self.assertEqual(result["summary"]["audited_pr_count"], 2)
        self.assertEqual(result["summary"]["verified_head_count"], 2)
        self.assertEqual(result["summary"]["context_scan_page_count"], 2)
        self.assertEqual(result["summary"]["head_verification_page_count"], 2)
        self.assertEqual(result["summary"]["duplicate_context_pr_count"], 1)
        self.assertEqual(len(calls), 4)

    def test_each_unsafe_context_shape_fails_closed(self) -> None:
        cases = {
            "missing": ("missing_pr_count", 1),
            "status-context": ("status_context_pr_count", 1),
            "wrong-workflow": ("unexpected_provenance_pr_count", 1),
            "wrong-app": ("unexpected_provenance_pr_count", 1),
            "overflow": ("context_overflow_pr_count", 1),
            "head-mismatch": ("head_mismatch_pr_count", 1),
            "unstable": ("changed_head_pr_count", 1),
        }
        for scenario, (field, count) in cases.items():
            with self.subTest(scenario=scenario):
                result, _ = self.run_audit(scenario, 1)
                self.assertFalse(result["passed"])
                self.assertEqual(result["summary"][field], count)
                self.assertTrue(result["errors"])

    def test_api_failure_writes_fail_closed_evidence(self) -> None:
        result, calls = self.run_audit("api-error", 1)
        self.assertFalse(result["passed"])
        self.assertFalse(result["snapshot_stable"])
        self.assertEqual(result["records"], [])
        self.assertIn("gh api graphql failed with exit status 17", result["errors"])
        self.assertEqual(len(calls), 1)

    def test_configurator_dry_run_never_executes_gh(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            env, log = self.environment(root, "api-error")
            env["REQUIRED_CONTEXT_AUDIT_OUTPUT"] = str(root / "must-not-exist.json")
            completed = subprocess.run(
                [str(CONFIGURATOR), "--dry-run"],
                cwd=REPO,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertFalse(log.exists())
            self.assertFalse(Path(env["REQUIRED_CONTEXT_AUDIT_OUTPUT"]).exists())
            self.assertFalse(json.loads(completed.stdout)["writes_performed"])

    def test_apply_audit_failure_precedes_every_remote_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            env, log = self.environment(root, "missing")
            output = root / "apply-audit.json"
            env["REQUIRED_CONTEXT_AUDIT_OUTPUT"] = str(output)
            completed = subprocess.run(
                [str(CONFIGURATOR), "--apply"],
                cwd=REPO,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 1, completed.stderr)
            self.assertEqual(completed.stdout, "")
            self.assertIn("required-context audit failed; inspect", completed.stderr)
            self.assertTrue(output.is_file())
            calls = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
            self.assertTrue(any(call[:2] == ["api", "graphql"] for call in calls))
            self.assertFalse(any("--method" in call for call in calls))


if __name__ == "__main__":
    unittest.main()
