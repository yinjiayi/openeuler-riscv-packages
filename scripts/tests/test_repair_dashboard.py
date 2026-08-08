# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import pathlib
import shutil
import tempfile
import unittest

from helpers import SCRIPTS, run_tool, write_json


class RepairDashboardTests(unittest.TestCase):
    def test_watcher_filters_and_lease_enforces_head(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            sha = "a" * 40
            fixture = root / "prs.json"
            write_json(
                fixture,
                [
                    {"number": 1, "title": "untrusted text", "url": "https://github.com/yinjiayi/openeuler-riscv-packages/pull/1", "author": {"login": "yinjiayi"}, "headRefName": "update/demo-2.0", "headRefOid": sha, "headRepository": {"nameWithOwner": "yinjiayi/openeuler-riscv-packages"}, "isCrossRepository": False, "labels": [{"name": "repair-queued"}], "statusCheckRollup": []},
                    {"number": 2, "title": "fork", "url": "https://example.invalid/2", "author": {"login": "attacker"}, "headRefName": "update/demo-2.0", "headRefOid": "b" * 40, "headRepository": {"nameWithOwner": "attacker/fork"}, "isCrossRepository": True, "labels": [{"name": "repair-queued"}]},
                ],
            )
            queue = root / "queue.json"
            run_tool("watch-failed-prs", ["--repo", "yinjiayi/openeuler-riscv-packages", "--fixture", str(fixture), "--output", str(queue), "--once", "--now", "2026-08-08T00:00:00Z"], root)
            self.assertEqual(json.loads(queue.read_text())["summary"], {"queried": 2, "queued": 1, "ignored": 1})
            state = root / "leases.json"
            claim = root / "claim.json"
            pr_view = root / "pr-view.json"
            write_json(pr_view, {"headRefOid": sha, "headRefName": "update/demo-2.0", "isCrossRepository": False})
            common = ["--repo", "yinjiayi/openeuler-riscv-packages", "--pr", "1", "--owner", "local-a", "--state-file", str(state), "--expected-head-sha", sha, "--queue", str(queue), "--fixture-pr", str(pr_view)]
            untrusted_claim = run_tool(
                "claim-repair",
                [
                    "claim",
                    "--repo",
                    "yinjiayi/openeuler-riscv-packages",
                    "--pr",
                    "1",
                    "--owner",
                    "local-a",
                    "--state-file",
                    str(state),
                    "--expected-head-sha",
                    sha,
                    "--fixture-pr",
                    str(pr_view),
                    "--output",
                    str(root / "untrusted-claim.json"),
                ],
                root,
                expected=1,
            )
            self.assertIn("trusted queue", untrusted_claim.stderr)
            run_tool("claim-repair", ["claim"] + common + ["--max-attempts", "1", "--lease-seconds", "600", "--output", str(claim), "--now", "2026-08-08T00:00:00Z"], root)
            self.assertEqual(json.loads(claim.read_text())["lease"]["status"], "codex-repairing")
            verified = root / "verified.json"
            run_tool("claim-repair", ["verify-head"] + common + ["--output", str(verified), "--now", "2026-08-08T00:01:00Z"], root)
            self.assertFalse(json.loads(verified.read_text())["safe_to_push_same_branch"])
            failed = root / "failed.json"
            run_tool("claim-repair", ["fail"] + common + ["--reason", "known failure remains", "--output", str(failed), "--now", "2026-08-08T00:02:00Z"], root)
            self.assertEqual(json.loads(failed.read_text())["outcome"], "needs-human")

    def test_static_dashboard_uses_factual_pr_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            (root / "dashboard").mkdir()
            for name in ("index.html", "app.js", "styles.css"):
                shutil.copyfile(SCRIPTS.parent / "dashboard" / name, root / "dashboard" / name)
            package = root / "packages" / "demo"
            (package / "patches").mkdir(parents=True)
            (package / "patches" / "series").write_text("", encoding="utf-8")
            write_json(package / "package.yaml", {"schema_version": 1, "package_id": "demo", "rpm": {"name": "demo", "summary": "demo", "license": "MIT"}, "version": {"current": "1.0", "release": "1", "latest_detected": "1.0"}, "discovery": {"snapshot_id": "x", "lineage": [{"source": "arch-extra", "package_name": "demo", "evidence_url": "https://example.org", "observed_at": "2026-08-01T00:00:00Z"}]}, "target": {"os": "openEuler", "release": "24.03-LTS-SP3", "arch": "riscv64", "isa": "RVA23", "riscv_status": "unknown"}, "updates": {"enabled": True, "last_checked_at": "2026-08-08T00:00:00Z", "last_successful_check_at": "2026-08-08T00:00:00Z"}})
            github = root / "github.json"
            write_json(github, {"pull_requests": [{"number": 7, "url": "https://github.com/yinjiayi/openeuler-riscv-packages/pull/7", "labels": [{"name": "package:demo"}, {"name": "repair-queued"}], "state": "OPEN", "updatedAt": "2026-08-08T01:00:00Z", "statusCheckRollup": []}]})
            output = root / "public"
            run_tool("generate-dashboard", ["--repo-root", str(root), "--output-dir", str(output), "--github-state", str(github), "--now", "2026-08-08T02:00:00Z"], root)
            data = json.loads((output / "data.json").read_text())
            self.assertEqual(data["packages"][0]["status"], "repair-queued")
            self.assertEqual(data["coverage_claim"], "observed-managed-packages-only")
            self.assertTrue((output / "index.html").is_file())


if __name__ == "__main__":
    unittest.main()
