# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import pathlib
import tempfile
import types
import unittest
from unittest import mock


REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "dispatch-trusted-package-ci"
AUTHORIZER = REPO / "ci" / "authorize-trusted-package-dispatch.py"
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


if __name__ == "__main__":
    unittest.main()
