# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import os
import pathlib
import subprocess
import tempfile
import types
import unittest
from unittest import mock


REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "dispatch-trusted-package-ci"
AUTHORIZER = REPO / "ci" / "authorize-trusted-package-dispatch.py"
BRIDGE = REPO / "ci" / "dispatch-required-checks.sh"
PACKAGE_WORKFLOW = REPO / ".github" / "workflows" / "package-ci.yml"
LOADER = importlib.machinery.SourceFileLoader("trusted_package_dispatch", str(SCRIPT))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
assert SPEC is not None
MODULE = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(MODULE)
AUTHORIZER_LOADER = importlib.machinery.SourceFileLoader("trusted_package_dispatch_authorizer", str(AUTHORIZER))
AUTHORIZER_SPEC = importlib.util.spec_from_loader(AUTHORIZER_LOADER.name, AUTHORIZER_LOADER)
assert AUTHORIZER_SPEC is not None
AUTHORIZER_MODULE = importlib.util.module_from_spec(AUTHORIZER_SPEC)
AUTHORIZER_LOADER.exec_module(AUTHORIZER_MODULE)


FAKE_BRIDGE_GH = r'''#!/usr/bin/env python3
import json
import os
import pathlib
import sys

args = sys.argv[1:]
root = pathlib.Path(os.environ["FAKE_BRIDGE_ROOT"])
statuses = root / "statuses.jsonl"
repo = "yinjiayi/openeuler-riscv-packages"
head = "a" * 40
base = "b" * 40
pr = "2011"
nonce = "900-1-2011"
title = "Package CI PR %s %s %s" % (pr, head, nonce)
scenario = os.environ.get("FAKE_BRIDGE_SCENARIO", "success")

if args[:1] == ["api"]:
    if "--method" in args:
        record = {
            "context": next(value[8:] for value in args if value.startswith("context=")),
            "state": next(value[6:] for value in args if value.startswith("state=")),
        }
        with statuses.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record) + "\n")
        print("{}")
        raise SystemExit(0)
    path = args[1]
    if path.endswith("/pulls/2011"):
        print(json.dumps({
            "state": "open", "merged": False, "auto_merge": None,
            "head": {"repo": {"full_name": repo}, "ref": "infra/ci-image-c382709bffbe", "sha": head},
            "base": {"ref": "main", "sha": base},
        }))
        raise SystemExit(0)
    if path.endswith("/actions/runs/77"):
        print(json.dumps({
            "id": 77, "status": "completed", "conclusion": scenario,
            "display_title": title, "event": "workflow_dispatch", "head_branch": "main",
            "head_sha": base, "path": ".github/workflows/package-ci.yml",
        }))
        raise SystemExit(0)
if args[:2] == ["workflow", "run"]:
    raise SystemExit(0)
if args[:2] == ["run", "list"]:
    counter = root / "lists"
    count = int(counter.read_text(encoding="utf-8")) if counter.exists() else 0
    counter.write_text(str(count + 1), encoding="utf-8")
    if count == 0:
        print("[]")
    else:
        print(json.dumps([{"databaseId": 77, "displayTitle": title, "headSha": base,
                           "status": "completed", "conclusion": scenario,
                           "url": "https://github.com/%s/actions/runs/77" % repo}]))
    raise SystemExit(0)
if args[:2] == ["run", "watch"]:
    raise SystemExit(0 if scenario == "success" else 1)
if args[:2] == ["run", "view"]:
    jobs = [{"name": name, "status": "completed", "conclusion": "success"} for name in (
        "metadata-validate", "source-verify", "rpmbuild-riscv64",
        "rpm-install-smoke", "patch-policy", "merge-policy",
    )]
    print(json.dumps({"status": "completed", "conclusion": scenario, "displayTitle": title,
                      "headSha": base, "jobs": jobs,
                      "url": "https://github.com/%s/actions/runs/77" % repo}))
    raise SystemExit(0)
print("unexpected fake gh invocation: " + repr(args), file=sys.stderr)
raise SystemExit(90)
'''


class TrustedPackageDispatchTests(unittest.TestCase):
    def pr(self, **overrides):
        document = {
            "state": "open",
            "head": {
                "repo": {"full_name": "yinjiayi/openeuler-riscv-packages"},
                "ref": "onboard/demo-1.0",
                "sha": "a" * 40,
            },
            "base": {"ref": "main", "sha": "b" * 40},
            "user": {"login": "yinjiayi"},
            "author_association": "OWNER",
            "changed_files": 2,
            "html_url": "https://example.invalid/pr/1",
        }
        document.update(overrides)
        return document

    def files(self):
        return [
            {"filename": "packages/demo/package.yaml"},
            {"filename": "packages/demo/demo.spec"},
        ]

    def run_snapshot(self, status, conclusion=None, **overrides):
        document = {
            "id": 12345,
            "status": status,
            "conclusion": conclusion,
            "display_title": "Package CI PR 1 " + "a" * 40,
            "event": "workflow_dispatch",
            "head_branch": "main",
            "head_sha": "c" * 40,
            "run_attempt": 1,
            "created_at": "2026-08-31T00:00:00Z",
            "updated_at": "2026-08-31T00:01:00Z",
            "html_url": "https://example.invalid/actions/runs/12345",
        }
        document.update(overrides)
        return document

    def run_view(self, conclusion="success"):
        return {
            "status": "completed",
            "conclusion": conclusion,
            "displayTitle": "Package CI PR 1 " + "a" * 40,
            "url": "https://example.invalid/actions/runs/12345",
            "jobs": [
                {"name": context, "status": "completed", "conclusion": conclusion}
                for context in MODULE.REQUIRED_CONTEXTS
            ],
        }

    def clock(self):
        current = [0.0]

        def now():
            return current[0]

        def sleep(seconds):
            current[0] += seconds

        return now, sleep

    def test_accepts_exact_same_repository_package_pr(self):
        result = MODULE.trusted_pr(self.pr(), self.files(), "demo", "yinjiayi/openeuler-riscv-packages")
        self.assertEqual(result["head_sha"], "a" * 40)
        self.assertEqual(MODULE.run_name(123, "a" * 40), "Package CI PR 123 " + "a" * 40)

    def test_rejects_fork_untrusted_author_and_non_package_scope(self):
        fork = self.pr()
        fork["head"] = dict(fork["head"])
        fork["head"]["repo"] = {"full_name": "attacker/openeuler-riscv-packages"}
        with self.assertRaisesRegex(MODULE.ToolError, "trusted repository"):
            MODULE.trusted_pr(fork, self.files(), "demo", "yinjiayi/openeuler-riscv-packages")

        author = self.pr(author_association="CONTRIBUTOR", user={"login": "attacker"})
        with self.assertRaisesRegex(MODULE.ToolError, "author is not trusted"):
            MODULE.trusted_pr(author, self.files(), "demo", "yinjiayi/openeuler-riscv-packages")

        files = self.files() + [{"filename": ".github/workflows/package-ci.yml"}]
        scope = self.pr(changed_files=3)
        with self.assertRaisesRegex(MODULE.ToolError, "confined"):
            MODULE.trusted_pr(scope, files, "demo", "yinjiayi/openeuler-riscv-packages")

    def test_final_result_must_bind_the_requested_head_and_package(self):
        document = {"package_id": "demo", "commit_sha": "a" * 40, "status": "passed", "classification": "none"}
        MODULE.verify_build_result(document, "demo", "a" * 40)
        document["commit_sha"] = "b" * 40
        with self.assertRaisesRegex(MODULE.ToolError, "does not bind"):
            MODULE.verify_build_result(document, "demo", "a" * 40)

    def test_terminal_polling_waits_past_in_progress_until_verified_completion(self):
        snapshots = [
            self.run_snapshot("queued"),
            self.run_snapshot("in_progress"),
            self.run_snapshot("completed", "failure"),
        ]
        clock, sleeper = self.clock()
        with mock.patch.object(MODULE, "run_snapshot", side_effect=snapshots), mock.patch.object(
            MODULE, "run_view", return_value=self.run_view("failure")
        ):
            api_document, view_document, polling = MODULE.wait_for_terminal_run(
                "yinjiayi/openeuler-riscv-packages",
                12345,
                "Package CI PR 1 " + "a" * 40,
                2,
                30,
                2,
                clock=clock,
                sleeper=sleeper,
            )
        self.assertEqual(api_document["conclusion"], "failure")
        self.assertEqual(view_document["conclusion"], "failure")
        self.assertEqual(polling["attempts"], 3)
        self.assertTrue(polling["terminal_verified"])

    def test_terminal_polling_tolerates_bounded_transient_api_error(self):
        clock, sleeper = self.clock()
        with mock.patch.object(
            MODULE,
            "run_snapshot",
            side_effect=[MODULE.ToolError("temporary EOF"), self.run_snapshot("completed", "success")],
        ), mock.patch.object(MODULE, "run_view", return_value=self.run_view("success")):
            _, _, polling = MODULE.wait_for_terminal_run(
                "yinjiayi/openeuler-riscv-packages",
                12345,
                "Package CI PR 1 " + "a" * 40,
                1,
                10,
                2,
                clock=clock,
                sleeper=sleeper,
            )
        self.assertEqual(polling["transient_errors"], 1)
        self.assertEqual(polling["last_transient_error"], "temporary EOF")
        self.assertTrue(polling["terminal_verified"])

    def test_terminal_polling_fails_after_consecutive_transient_error_bound(self):
        clock, sleeper = self.clock()
        with mock.patch.object(MODULE, "run_snapshot", side_effect=MODULE.ToolError("temporary EOF")):
            with self.assertRaises(MODULE.TerminalWaitError) as raised:
                MODULE.wait_for_terminal_run(
                    "yinjiayi/openeuler-riscv-packages",
                    12345,
                    "Package CI PR 1 " + "a" * 40,
                    1,
                    30,
                    1,
                    clock=clock,
                    sleeper=sleeper,
                )
        self.assertIn("transient-error limit", str(raised.exception))
        self.assertEqual(raised.exception.polling["transient_errors"], 2)
        self.assertEqual(raised.exception.polling["max_consecutive_transient_errors"], 1)

    def test_terminal_polling_times_out_with_last_bound_run_evidence(self):
        clock, sleeper = self.clock()
        with mock.patch.object(MODULE, "run_snapshot", return_value=self.run_snapshot("in_progress")):
            with self.assertRaises(MODULE.TerminalWaitError) as raised:
                MODULE.wait_for_terminal_run(
                    "yinjiayi/openeuler-riscv-packages",
                    12345,
                    "Package CI PR 1 " + "a" * 40,
                    2,
                    5,
                    2,
                    clock=clock,
                    sleeper=sleeper,
                )
        self.assertIn("within 5 seconds", str(raised.exception))
        self.assertEqual(raised.exception.polling["last_run"]["status"], "in_progress")
        self.assertFalse(raised.exception.polling["terminal_verified"])

    def test_terminal_polling_rejects_identity_change_without_retry(self):
        clock, sleeper = self.clock()
        changed = self.run_snapshot("in_progress", id=54321)
        with mock.patch.object(MODULE, "run_snapshot", return_value=changed):
            with self.assertRaisesRegex(MODULE.TerminalWaitError, "expected run id") as raised:
                MODULE.wait_for_terminal_run(
                    "yinjiayi/openeuler-riscv-packages",
                    12345,
                    "Package CI PR 1 " + "a" * 40,
                    1,
                    10,
                    2,
                    clock=clock,
                    sleeper=sleeper,
                )
        self.assertEqual(raised.exception.polling["last_run"]["id"], 54321)

    def test_tool_error_after_dispatch_writes_bound_failure_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = pathlib.Path(temporary) / "dispatch.json"
            args = types.SimpleNamespace(
                repo="yinjiayi/openeuler-riscv-packages",
                pr=1,
                package_id="demo",
                output=output,
                poll_seconds=1,
                run_timeout_seconds=10,
                max_transient_errors=2,
            )
            fake_parser = mock.Mock()
            fake_parser.parse_args.return_value = args
            polling = MODULE.terminal_polling_evidence(
                attempts=2,
                transient_errors=0,
                last_transient_error=None,
                timeout_seconds=10,
                poll_seconds=1,
                max_transient_errors=2,
                last_run=MODULE.run_observation(self.run_snapshot("in_progress")),
                terminal_verified=False,
            )
            posted = []
            with mock.patch.object(MODULE, "parser", return_value=fake_parser), mock.patch.object(
                MODULE, "preflight"
            ), mock.patch.object(MODULE, "fetch_pr", return_value=(self.pr(), self.files())), mock.patch.object(
                MODULE, "post_status", side_effect=lambda *values: posted.append(values)
            ), mock.patch.object(MODULE, "list_dispatches", return_value=[]), mock.patch.object(
                MODULE, "run"
            ), mock.patch.object(
                MODULE,
                "wait_for_dispatch",
                return_value={"databaseId": 12345, "url": "https://example.invalid/actions/runs/12345"},
            ), mock.patch.object(
                MODULE,
                "wait_for_terminal_run",
                side_effect=MODULE.TerminalWaitError("terminal timeout", polling),
            ), mock.patch.object(MODULE, "verify_current"):
                returncode = MODULE.main()

            self.assertEqual(returncode, 2)
            document = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(document["outcome"], "tool-error")
            self.assertEqual(document["head_sha"], "a" * 40)
            self.assertEqual(document["run_id"], 12345)
            self.assertEqual(document["terminal_observation"]["status"], "in_progress")
            self.assertEqual(document["polling"]["attempts"], 2)
            self.assertTrue(document["status_updates"]["fail_close_succeeded"])
            self.assertEqual(document["status_updates"]["pending_posted_count"], 6)
            self.assertEqual(document["status_updates"]["fail_close_posted_count"], 6)
            self.assertEqual([values[3] for values in posted[:6]], ["pending"] * 6)
            self.assertEqual([values[3] for values in posted[6:]], ["error"] * 6)

    def test_completed_workflow_failure_is_recorded_without_becoming_tool_error(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = pathlib.Path(temporary) / "dispatch.json"
            args = types.SimpleNamespace(
                repo="yinjiayi/openeuler-riscv-packages",
                pr=1,
                package_id="demo",
                output=output,
                poll_seconds=1,
                run_timeout_seconds=10,
                max_transient_errors=2,
            )
            fake_parser = mock.Mock()
            fake_parser.parse_args.return_value = args
            api_document = self.run_snapshot("completed", "failure")
            view_document = self.run_view("success")
            view_document["conclusion"] = "failure"
            for job in view_document["jobs"]:
                if job["name"] == "rpmbuild-riscv64":
                    job["conclusion"] = "failure"
            polling = MODULE.terminal_polling_evidence(
                attempts=3,
                transient_errors=0,
                last_transient_error=None,
                timeout_seconds=10,
                poll_seconds=1,
                max_transient_errors=2,
                last_run=MODULE.run_observation(api_document),
                terminal_verified=True,
            )
            with mock.patch.object(MODULE, "parser", return_value=fake_parser), mock.patch.object(
                MODULE, "preflight"
            ), mock.patch.object(MODULE, "fetch_pr", return_value=(self.pr(), self.files())), mock.patch.object(
                MODULE, "post_status"
            ), mock.patch.object(MODULE, "list_dispatches", return_value=[]), mock.patch.object(
                MODULE, "run"
            ), mock.patch.object(
                MODULE,
                "wait_for_dispatch",
                return_value={"databaseId": 12345, "url": "https://example.invalid/actions/runs/12345"},
            ), mock.patch.object(
                MODULE,
                "wait_for_terminal_run",
                return_value=(api_document, view_document, polling),
            ), mock.patch.object(MODULE, "verify_current"), mock.patch.object(
                MODULE, "download_build_result"
            ) as download:
                returncode = MODULE.main()

            self.assertEqual(returncode, 1)
            download.assert_not_called()
            document = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(document["outcome"], "workflow-failed")
            self.assertEqual(document["terminal_observation"]["conclusion"], "failure")
            self.assertEqual(
                next(item for item in document["checks"] if item["name"] == "rpmbuild-riscv64")["conclusion"],
                "failure",
            )
            self.assertIsNone(document["error"])
            self.assertTrue(document["status_updates"]["final_posted"])
            self.assertEqual(document["status_updates"]["final_posted_count"], 6)

    def test_output_contract_rejects_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(MODULE.ToolError, "must name a file"):
                MODULE.atomic_json(pathlib.Path(temporary), {"schema_version": 1})


class TrustedPackageDispatchAuthorizerTests(unittest.TestCase):
    def pr(self, **overrides):
        document = {
            "state": "open",
            "head": {
                "repo": {"full_name": "yinjiayi/openeuler-riscv-packages"},
                "ref": "repair/demo-1.0",
                "sha": "a" * 40,
            },
            "base": {"ref": "main", "sha": "b" * 40},
            "user": {"login": "yinjiayi"},
            "author_association": "OWNER",
            "changed_files": 2,
        }
        document.update(overrides)
        return document

    def files(self):
        return [
            {"filename": "packages/demo/package.yaml"},
            {"filename": "packages/demo/demo.spec"},
        ]

    def authorize(self, **overrides):
        values = {
            "repo": "yinjiayi/openeuler-riscv-packages",
            "package_id": "demo",
            "base_sha": "b" * 40,
            "head_sha": "a" * 40,
            "publish_to_repo": "false",
            "event_ref": "refs/heads/main",
        }
        values.update(overrides)
        AUTHORIZER_MODULE.authorize(self.pr(), self.files(), **values)

    def test_accepts_exact_open_trusted_package_pr(self):
        self.authorize()

    def test_rejects_unbound_head_publication_and_scope(self):
        with self.assertRaisesRegex(AUTHORIZER_MODULE.AuthorizationError, "does not match"):
            self.authorize(head_sha="c" * 40)
        with self.assertRaisesRegex(AUTHORIZER_MODULE.AuthorizationError, "disable repository publication"):
            self.authorize(publish_to_repo="true")
        with self.assertRaisesRegex(AUTHORIZER_MODULE.AuthorizationError, "protected main"):
            self.authorize(event_ref="refs/heads/repair/demo")

        files = self.files() + [{"filename": "ci/compose-build-result.py"}]
        with self.assertRaisesRegex(AUTHORIZER_MODULE.AuthorizationError, "confined"):
            AUTHORIZER_MODULE.authorize(
                self.pr(changed_files=3),
                files,
                repo="yinjiayi/openeuler-riscv-packages",
                package_id="demo",
                base_sha="b" * 40,
                head_sha="a" * 40,
                publish_to_repo="false",
                event_ref="refs/heads/main",
            )

    def test_accepts_only_exact_bot_infrastructure_shapes(self):
        values = {
            "repo": "yinjiayi/openeuler-riscv-packages",
            "package_id": "",
            "base_sha": "b" * 40,
            "head_sha": "a" * 40,
            "publish_to_repo": "false",
            "event_ref": "refs/heads/main",
        }
        image = self.pr(
            changed_files=1,
            user={"login": "github-actions[bot]"},
            author_association="CONTRIBUTOR",
        )
        image["head"] = dict(image["head"], ref="infra/ci-image-c382709bffbe")
        AUTHORIZER_MODULE.authorize(
            image,
            [{"filename": "ci/image.lock", "status": "modified"}],
            **values,
        )

        snapshot_id = "discovery-20260903T014000Z-33704490322"
        catalog = self.pr(
            changed_files=1,
            user={"login": "github-actions[bot]"},
            author_association="CONTRIBUTOR",
        )
        catalog["head"] = dict(catalog["head"], ref="catalog/" + snapshot_id)
        AUTHORIZER_MODULE.authorize(
            catalog,
            [{"filename": "catalog/snapshots/%s.json.gz" % snapshot_id, "status": "added"}],
            **values,
        )

        rejected = (
            (image, [{"filename": "ci/image.lock", "status": "added"}]),
            (
                dict(image, user={"login": "yinjiayi"}),
                [{"filename": "ci/image.lock", "status": "modified"}],
            ),
            (
                dict(image, head=dict(image["head"], ref="infra/unreviewed")),
                [{"filename": "ci/image.lock", "status": "modified"}],
            ),
            (
                catalog,
                [{"filename": "catalog/snapshots/other.json.gz", "status": "added"}],
            ),
            (
                catalog,
                [{
                    "filename": "catalog/snapshots/%s.json.gz" % snapshot_id,
                    "status": "renamed",
                    "previous_filename": "catalog/snapshots/old.json.gz",
                }],
            ),
        )
        for pr, files in rejected:
            with self.subTest(ref=pr["head"]["ref"], files=files):
                with self.assertRaisesRegex(
                    AUTHORIZER_MODULE.AuthorizationError,
                    "allowed bot infrastructure shape",
                ):
                    AUTHORIZER_MODULE.authorize(pr, files, **values)

    def test_bot_pr_bridge_dispatches_only_from_main_and_isolates_concurrency(self):
        bridge = BRIDGE.read_text(encoding="utf-8")
        workflow = PACKAGE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('gh workflow run package-ci.yml --repo "$repo" --ref main', bridge)
        self.assertIn('expected_name="Package CI PR $pr_number $head_sha $dispatch_nonce"', bridge)
        self.assertIn(".displayTitle == $name and .headSha == $base", bridge)
        self.assertIn('-f "dispatch_nonce=$dispatch_nonce"', bridge)
        self.assertIn('.conclusion == "success"', bridge)
        self.assertNotIn(
            'gh workflow run package-ci.yml --repo "$repo" --ref "$ref"',
            bridge,
        )
        self.assertIn("inputs.package_id || inputs.pr_number", workflow)


class BotRequiredCheckBridgeTests(unittest.TestCase):
    def run_bridge(self, scenario: str) -> tuple[subprocess.CompletedProcess[str], list[dict[str, str]]]:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            binary = root / "bin"
            binary.mkdir()
            fake = binary / "gh"
            fake.write_text(FAKE_BRIDGE_GH, encoding="utf-8")
            fake.chmod(0o755)
            output = root / "evidence.json"
            env = dict(os.environ)
            env.update({
                "PATH": str(binary) + os.pathsep + env.get("PATH", ""),
                "FAKE_BRIDGE_ROOT": str(root),
                "FAKE_BRIDGE_SCENARIO": scenario,
                "GITHUB_RUN_ID": "900",
                "GITHUB_RUN_ATTEMPT": "1",
                "GITHUB_REF": "refs/heads/main",
                "GITHUB_WORKFLOW_REF": (
                    "yinjiayi/openeuler-riscv-packages/"
                    ".github/workflows/build-ci-image.yml@refs/heads/main"
                ),
            })
            completed = subprocess.run(
                [
                    str(BRIDGE),
                    "--repo", "yinjiayi/openeuler-riscv-packages",
                    "--pr-number", "2011",
                    "--ref", "infra/ci-image-c382709bffbe",
                    "--head-sha", "a" * 40,
                    "--base-sha", "b" * 40,
                    "--output", str(output),
                ],
                cwd=REPO,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            status_path = root / "statuses.jsonl"
            statuses = [json.loads(line) for line in status_path.read_text(encoding="utf-8").splitlines()]
            if scenario == "success":
                document = json.loads(output.read_text(encoding="utf-8"))
                self.assertEqual(document["dispatch_nonce"], "900-1-2011")
                self.assertEqual(len(document["checks"]), 6)
                self.assertTrue(document["success"])
            else:
                self.assertFalse(output.exists())
            return completed, statuses

    def test_success_posts_all_six_only_after_exact_terminal_success(self):
        completed, statuses = self.run_bridge("success")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual([item["state"] for item in statuses[:6]], ["pending"] * 6)
        self.assertEqual([item["state"] for item in statuses[6:]], ["success"] * 6)
        self.assertNotIn("configure", [item["context"] for item in statuses])

    def test_overall_failure_overwrites_every_context_with_error(self):
        completed, statuses = self.run_bridge("failure")
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual([item["state"] for item in statuses[:6]], ["pending"] * 6)
        self.assertEqual([item["state"] for item in statuses[6:]], ["error"] * 6)
        self.assertFalse(any(item["state"] == "success" for item in statuses))


if __name__ == "__main__":
    unittest.main()
