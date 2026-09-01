# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import os
import pathlib
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest

from helpers import SCRIPTS, run_tool, write_json

sys.path.insert(0, str(SCRIPTS))


class RepairDashboardTests(unittest.TestCase):
    def test_process_token_is_allowed_but_never_recorded_or_exposed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "safe.txt").write_text("safe\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "safe.txt"], check=True)

            fake_bin = root / "bin"
            fake_bin.mkdir()
            fake_gh = fake_bin / "gh"
            fake_gh.write_text(
                "#!/bin/sh\n"
                "case $1 in\n"
                "  auth) exit 0 ;;\n"
                "  api) printf '%s\\n' yinjiayi; exit 0 ;;\n"
                "  *) exit 1 ;;\n"
                "esac\n",
                encoding="utf-8",
            )
            fake_gh.chmod(0o755)
            token = "gh" + "p_" + ("A" * 36)
            env = dict(os.environ)
            env.update({"GH_TOKEN": token, "PATH": str(fake_bin) + os.pathsep + env.get("PATH", "")})
            output = root / "credential.json"
            command = [
                str(SCRIPTS / "github-credential-guard"),
                "--repo-root",
                str(root),
                "--require-auth",
                "--local-only",
                "--output",
                str(output),
            ]
            completed = subprocess.run(command, cwd=str(root), env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result["authentication_mode"], "process-gh-token")
            self.assertEqual(result["login"], "yinjiayi")
            self.assertFalse(result["token_value_recorded"])
            self.assertNotIn(token, output.read_text(encoding="utf-8"))
            self.assertNotIn(token, completed.stdout + completed.stderr)

            public = root / "public"
            public.mkdir()
            (public / "data.json").write_text('{"credential":"%s"}\n' % token, encoding="utf-8")
            blocked = subprocess.run(command, cwd=str(root), env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(blocked.returncode, 1)
            self.assertIn("public/data.json", blocked.stderr)
            self.assertNotIn(token, blocked.stdout + blocked.stderr)

            (public / "data.json").unlink()
            (root / "staged.txt").write_text(token + "\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "staged.txt"], check=True)
            staged = subprocess.run(command, cwd=str(root), env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(staged.returncode, 1)
            self.assertIn("staged.txt", staged.stderr)
            self.assertIn("<staged-diff>", staged.stderr)
            self.assertNotIn(token, staged.stdout + staged.stderr)

    def test_static_validator_recognizes_token_literals_without_echoing_one(self) -> None:
        validator = runpy.run_path(str(SCRIPTS.parent / "ci" / "validate-repository.py"))
        token = ("gh" + "p_" + ("B" * 36)).encode("ascii")
        self.assertTrue(validator["contains_github_token_literal"](token))
        self.assertFalse(validator["contains_github_token_literal"](b"GH_TOKEN is process scoped"))

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

    def test_release_accepts_only_the_verified_same_branch_pushed_head(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            failed_sha = "a" * 40
            pushed_sha = "c" * 40
            fixture = root / "prs.json"
            write_json(
                fixture,
                [
                    {
                        "number": 7,
                        "title": "repair me",
                        "url": "https://github.com/yinjiayi/openeuler-riscv-packages/pull/7",
                        "author": {"login": "yinjiayi"},
                        "headRefName": "repair/demo-1.0",
                        "headRefOid": failed_sha,
                        "headRepository": {"nameWithOwner": "yinjiayi/openeuler-riscv-packages"},
                        "isCrossRepository": False,
                        "labels": [{"name": "repair-queued"}],
                        "statusCheckRollup": [],
                    }
                ],
            )
            queue = root / "queue.json"
            run_tool(
                "watch-failed-prs",
                [
                    "--repo",
                    "yinjiayi/openeuler-riscv-packages",
                    "--fixture",
                    str(fixture),
                    "--output",
                    str(queue),
                    "--once",
                    "--now",
                    "2026-08-08T00:00:00Z",
                ],
                root,
            )
            state = root / "leases.json"
            failed_view = root / "failed-pr-view.json"
            write_json(failed_view, {"headRefOid": failed_sha, "headRefName": "repair/demo-1.0", "isCrossRepository": False})
            common = [
                "--repo",
                "yinjiayi/openeuler-riscv-packages",
                "--pr",
                "7",
                "--owner",
                "local-a",
                "--state-file",
                str(state),
                "--expected-head-sha",
                failed_sha,
            ]
            run_tool(
                "claim-repair",
                ["claim"] + common + ["--queue", str(queue), "--fixture-pr", str(failed_view), "--lease-seconds", "600"],
                root,
            )

            wrong_ref_view = root / "wrong-ref-view.json"
            write_json(wrong_ref_view, {"headRefOid": pushed_sha, "headRefName": "repair/other", "isCrossRepository": False})
            blocked = run_tool(
                "claim-repair",
                ["release"]
                + common
                + ["--pushed-head-sha", pushed_sha, "--fixture-pr", str(wrong_ref_view), "--now", "2026-08-08T00:01:00Z"],
                root,
                expected=1,
            )
            self.assertIn("head ref changed", blocked.stderr)
            self.assertIn("yinjiayi/openeuler-riscv-packages#7", json.loads(state.read_text())["leases"])

            pushed_view = root / "pushed-pr-view.json"
            write_json(pushed_view, {"headRefOid": pushed_sha, "headRefName": "repair/demo-1.0", "isCrossRepository": False})
            released = root / "released.json"
            run_tool(
                "claim-repair",
                ["release"]
                + common
                + [
                    "--pushed-head-sha",
                    pushed_sha,
                    "--fixture-pr",
                    str(pushed_view),
                    "--output",
                    str(released),
                    "--now",
                    "2026-08-08T00:02:00Z",
                ],
                root,
            )
            result = json.loads(released.read_text())
            self.assertEqual(result["failed_head_sha"], failed_sha)
            self.assertEqual(result["pushed_head_sha"], pushed_sha)
            self.assertEqual(result["observed_head_sha"], pushed_sha)
            persisted = json.loads(state.read_text())
            self.assertEqual(persisted["leases"], {})
            self.assertEqual(persisted["history"][-1]["pushed_head_sha"], pushed_sha)
            schema = json.loads((SCRIPTS.parent / "schemas" / "repair-record.schema.json").read_text())
            schema_errors = runpy.run_path(str(SCRIPTS / "validate-metadata"))["schema_errors"]
            self.assertEqual(schema_errors(result, schema, schema), [])
            self.assertEqual(schema_errors(persisted, schema, schema), [])

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
            self.assertTrue((output / "inventory.json").is_file())

    def test_dashboard_publishes_links_only_for_matching_verified_generation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            (root / "dashboard").mkdir()
            for name in ("index.html", "app.js", "styles.css"):
                shutil.copyfile(SCRIPTS.parent / "dashboard" / name, root / "dashboard" / name)
            package = root / "packages" / "demo"
            (package / "patches").mkdir(parents=True)
            (package / "patches" / "series").write_text("", encoding="utf-8")
            write_json(package / "package.yaml", {"schema_version": 1, "package_id": "demo", "rpm": {"name": "demo", "summary": "demo", "license": "MIT"}, "version": {"current": "1.0", "release": "1"}, "target": {"os": "openEuler", "release": "24.03-LTS-SP3", "arch": "riscv64", "isa": "RVA23", "riscv_status": "unknown"}})
            commit = "a" * 40
            inventory = root / "package-index.json"
            write_json(inventory, {"schema_version": 1, "kind": "package-inventory", "generated_at": "2026-08-08T00:00:00Z", "main_ref": "b" * 40, "source_snapshot": {"snapshot_id": "snapshot-1"}, "entries": [{"discovery_key": "demo", "names": ["demo"], "component_ids": ["example.org-demo"], "decisions": {}, "stable_versions": ["1.0"], "upstream_urls": ["https://example.org/demo"], "status": "managed", "managed_package": {"package_id": "demo", "directory": "packages/demo", "version": "1.0", "summary": "demo"}, "reviewed_release": None, "pull_requests": [{"number": 1, "state": "merged", "head_sha": commit, "updated_at": "2026-08-08T00:30:00Z", "url": "https://github.com/yinjiayi/openeuler-riscv-packages/pull/1"}]}]})
            evidence = root / "evidence"
            write_json(evidence / "smoke" / "build-result.json", {"schema_version": 1, "package_id": "demo", "commit_sha": commit, "job_id": "12345:1:package-ci", "status": "passed", "checks": {"rpm-install-smoke": {"status": "passed"}}, "classification": "none", "finished_at": "2026-08-08T01:00:00Z"})
            generation = "20260808T010000Z-demo-aaaaaaaaaaaa-run12345-attempt1"
            write_json(evidence / "publish" / "upload.json", {"schema_version": 1, "kind": "rpm-repository-upload-batch", "status": "staged", "package_id": "demo", "commit_sha": commit, "generation": generation, "artifacts": [{"kind": "binary", "filename": "demo-1.0-1.riscv64.rpm"}, {"kind": "source", "filename": "demo-1.0-1.src.rpm"}]})
            verification = evidence / "publish" / "result.json"
            write_json(verification, {"schema_version": 1, "kind": "rpm-repository-publication-verification", "status": "passed", "package_id": "demo", "commit_sha": commit, "generation": generation, "verified_at": "2026-08-08T01:05:00Z", "state_url": "http://2.27.148.101:38080/generations/%s/state.json" % generation, "repositories": {"riscv64": {"baseurl": "http://2.27.148.101:38080/generations/%s/riscv64/" % generation}, "source": {"baseurl": "http://2.27.148.101:38080/generations/%s/source/" % generation}}})
            output = root / "public"
            arguments = ["--repo-root", str(root), "--output-dir", str(output), "--package-inventory", str(inventory), "--build-results", str(evidence), "--now", "2026-08-08T02:00:00Z"]
            run_tool("generate-dashboard", arguments, root)
            data = json.loads((output / "data.json").read_text(encoding="utf-8"))
            full = json.loads((output / "inventory.json").read_text(encoding="utf-8"))
            schema_errors = runpy.run_path(str(SCRIPTS / "validate-metadata"))["schema_errors"]
            dashboard_schema = json.loads((SCRIPTS.parent / "schemas" / "dashboard.schema.json").read_text(encoding="utf-8"))
            inventory_schema = json.loads((SCRIPTS.parent / "schemas" / "dashboard-inventory.schema.json").read_text(encoding="utf-8"))
            self.assertEqual(schema_errors(data, dashboard_schema, dashboard_schema), [])
            self.assertEqual(schema_errors(full, inventory_schema, inventory_schema), [])
            self.assertEqual(data["coverage_claim"], "full-package-inventory")
            self.assertEqual(data["inventory"]["entry_count"], 1)
            self.assertEqual(full["entries"][0]["status"], "published")
            self.assertEqual(full["entries"][0]["links"]["rpm"], ["http://2.27.148.101:38080/generations/%s/riscv64/Packages/demo-1.0-1.riscv64.rpm" % generation])
            self.assertEqual(full["entries"][0]["links"]["srpm"], ["http://2.27.148.101:38080/generations/%s/source/Packages/demo-1.0-1.src.rpm" % generation])
            verification.unlink()
            second_output = root / "public-without-verification"
            arguments[3] = str(second_output)
            run_tool("generate-dashboard", arguments, root)
            second = json.loads((second_output / "inventory.json").read_text(encoding="utf-8"))["entries"][0]
            self.assertEqual(second["status"], "build-succeeded")
            self.assertEqual(second.get("links", {}).get("rpm", []), [])
            self.assertEqual(second.get("links", {}).get("srpm", []), [])


if __name__ == "__main__":
    unittest.main()
