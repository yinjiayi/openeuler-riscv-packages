# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import importlib.machinery
import importlib.util
from pathlib import Path
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "approve-bot-pr-workflows"
LOADER = importlib.machinery.SourceFileLoader("approve_bot_pr_workflows", str(SCRIPT))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
assert SPEC is not None
MODULE = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(MODULE)
REPO = MODULE.REPOSITORY
HEAD = "a" * 40
BASE = "b" * 40
MAIN = "c" * 40


def pr_document(path: str = "packages/snappy/package.yaml") -> dict:
    return {
        "number": 2055, "state": "open", "merged": False, "merged_at": None,
        "auto_merge": None, "draft": False, "changed_files": 1,
        "user": {"login": "github-actions[bot]"},
        "head": {"sha": HEAD, "ref": "update/snappy/1.3.0", "repo": {"full_name": REPO}},
        "base": {"sha": BASE, "ref": "main", "repo": {"full_name": REPO}},
        "file": path,
    }


def workflow_run(name: str, path: str, run_id: int) -> dict:
    return {
        "id": run_id, "name": name, "path": path,
        "event": "pull_request", "head_sha": HEAD,
        "status": "completed", "conclusion": "action_required",
        "repository": {"full_name": REPO}, "head_repository": {"full_name": REPO},
        "actor": {"login": "github-actions[bot]"},
        "triggering_actor": {"login": "github-actions[bot]"},
        "pull_requests": [{"number": 2055, "head": {"sha": HEAD}, "base": {"sha": BASE}}],
    }


class ApprovalTests(unittest.TestCase):
    def fixture(self, *, extra_path: str | None = None) -> dict[str, object]:
        pr = pr_document()
        if extra_path is not None:
            pr["changed_files"] = 2
        files = [{"filename": pr["file"], "status": "modified"}]
        if extra_path is not None:
            files.append({"filename": extra_path, "status": "modified"})
        runs = [workflow_run(name, path, index) for index, (name, path) in enumerate(MODULE.WORKFLOWS.items(), 101)]
        return {
            f"repos/{REPO}/pulls/2055": pr,
            f"repos/{REPO}/pulls/2055/files?per_page=100&page=1": files,
            f"repos/{REPO}/git/ref/heads/main": {"ref": "refs/heads/main", "object": {"type": "commit", "sha": MAIN}},
            f"repos/{REPO}/actions/runs?head_sha={HEAD}&event=pull_request&per_page=100": {
                "total_count": 2, "workflow_runs": runs,
            },
            f"repos/{REPO}/actions/runs/101": runs[0],
            f"repos/{REPO}/actions/runs/102": runs[1],
        }

    def test_exact_bot_package_and_two_suppressed_runs(self) -> None:
        fixture = self.fixture()
        with mock.patch.object(MODULE, "api", side_effect=fixture.__getitem__):
            pr = MODULE.inspect_pr(2055)
            runs = MODULE.inspect_runs(pr)
        self.assertEqual(pr["package_id"], "snappy")
        self.assertEqual(pr["current_main_sha"], MAIN)
        self.assertEqual([run["decision"] for run in runs], ["approve", "approve"])

    def test_rejects_mixed_package_scope(self) -> None:
        fixture = self.fixture(extra_path="packages/other/other.spec")
        with mock.patch.object(MODULE, "api", side_effect=fixture.__getitem__):
            with self.assertRaisesRegex(MODULE.ApprovalError, "outside packages/snappy"):
                MODULE.inspect_pr(2055)

    def test_rejects_armed_auto_merge(self) -> None:
        fixture = self.fixture()
        fixture[f"repos/{REPO}/pulls/2055"]["auto_merge"] = {"enabled_by": "bot"}
        with mock.patch.object(MODULE, "api", side_effect=fixture.__getitem__):
            with self.assertRaisesRegex(MODULE.ApprovalError, "not an open, disarmed"):
                MODULE.inspect_pr(2055)

    def test_rejects_run_from_wrong_actor(self) -> None:
        fixture = self.fixture()
        fixture[f"repos/{REPO}/actions/runs/101"]["actor"]["login"] = "someone-else"
        with mock.patch.object(MODULE, "api", side_effect=fixture.__getitem__):
            pr = MODULE.inspect_pr(2055)
            with self.assertRaisesRegex(MODULE.ApprovalError, "provenance"):
                MODULE.inspect_runs(pr)

    def test_rejects_incomplete_run_listing(self) -> None:
        fixture = self.fixture()
        fixture[f"repos/{REPO}/actions/runs?head_sha={HEAD}&event=pull_request&per_page=100"]["total_count"] = 3
        with mock.patch.object(MODULE, "api", side_effect=fixture.__getitem__):
            pr = MODULE.inspect_pr(2055)
            with self.assertRaisesRegex(MODULE.ApprovalError, "incomplete"):
                MODULE.inspect_runs(pr)

    def test_rechecks_lease_before_post(self) -> None:
        target = {"name": "Package CI", "run_id": 101, "decision": "approve"}
        plan = {"number": 2055, "head_sha": HEAD}
        with mock.patch.object(MODULE, "command") as command, \
             mock.patch.object(MODULE, "inspect_pr", return_value={**plan, "head_sha": BASE}), \
             mock.patch.object(MODULE, "inspect_runs") as inspect_runs:
            with self.assertRaisesRegex(MODULE.ApprovalError, "changed"):
                MODULE.approve_run(plan, target, Path("/tmp/example"))
        self.assertEqual(command.call_count, 1)  # guard only, no approval POST
        inspect_runs.assert_not_called()


if __name__ == "__main__":
    unittest.main()
