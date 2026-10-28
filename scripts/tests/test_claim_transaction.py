# SPDX-License-Identifier: Apache-2.0
"""Claim transaction regressions; all GitHub operations are mocked."""
from __future__ import annotations

import copy
import json
import pathlib
import runpy
import sys
import tempfile
import unittest
from unittest import mock

from helpers import SCRIPTS, write_json

sys.path.insert(0, str(SCRIPTS))


class ClaimTransactionTests(unittest.TestCase):
    repo = "yinjiayi/openeuler-riscv-packages"
    head = "a" * 40
    key = repo + "#7"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.tool = runpy.run_path(str(SCRIPTS / "claim-repair"))
        self.globals = self.tool["command_claim"].__globals__
        self.args = self.tool["parser"]().parse_args([
            "claim", "--repo", self.repo, "--pr", "7", "--owner", "worker-a",
            "--state-file", str(self.root / "state.json"), "--expected-head-sha", self.head,
            "--queue", str(self.root / "queue.json"), "--lease-seconds", "600",
            "--max-attempts", "3", "--now", "2026-10-28T00:00:00Z",
            "--output", str(self.root / "claim.json"),
        ])
        self.pr = {"headRefOid": self.head, "headRefName": "repair/demo", "labels": [{"name": "repair-queued"}]}
        self.calls = []
        self.remote_labels = {"repair-queued"}
        self.comments = []
        self.initial = {"schema_version": 1, "leases": {}, "attempts": {self.key + "@" + "b" * 40: 1}, "history": []}
        write_json(pathlib.Path(self.args.state_file), self.initial)
        # A test failure must never fall through to actual gh or another process.
        deny = mock.patch("subprocess.run", side_effect=AssertionError("external call in offline test"))
        deny.start()
        self.addCleanup(deny.stop)

    def state(self):
        return json.loads(pathlib.Path(self.args.state_file).read_text())

    def check(self, args):
        return dict(self.pr, labels=[{"name": x} for x in sorted(self.remote_labels)]), self.head

    def gh(self, command):
        self.calls.append(list(command))
        if command[:2] == ["pr", "edit"]:
            self.remote_labels.discard("repair-queued")
            self.remote_labels.add("codex-repairing")
        elif command[:2] == ["pr", "comment"]:
            self.comments.append(command[-1])
        else:
            raise AssertionError(command)
        return ""

    def claim(self, gh=None, check=None):
        with mock.patch.dict(self.globals, {"gh": gh or self.gh, "check_head": check or self.check}):
            return self.tool["command_claim"](self.args)

    def assert_blocked(self, phase):
        state = self.state()
        lease = state["leases"][self.key]
        self.assertEqual(lease["status"], "reconciliation-required")
        self.assertEqual(lease["remote_sync_phase"], phase)
        self.assertEqual(state["attempts"][self.key + "@" + self.head], 1)
        self.assertEqual(state["attempts"][self.key + "@" + "b" * 40], 1)
        self.assertEqual(state["history"], [])
        self.assertFalse(pathlib.Path(self.args.output).exists())
        return state, lease

    def test_partial_label_error_retains_attempt_and_blocks_every_owned_action(self):
        def partial(command):
            self.calls.append(command)
            self.remote_labels.discard("repair-queued")
            raise self.tool["ToolError"]('gh command failed: Post "https://api.github.com/graphql": EOF', 1)
        with self.assertRaises(self.tool["ToolError"]):
            self.claim(partial)
        state, lease = self.assert_blocked("before-label-command")
        self.assertEqual(self.remote_labels, set())
        self.assertEqual(len(self.calls), 1)
        for require_live in (True, False):
            with self.subTest(require_live=require_live), self.assertRaises(self.tool["ToolError"]):
                self.tool["owned_lease"](self.args, state, self.tool["parse_now"](self.args.now), require_live=require_live)
        with mock.patch.dict(self.globals, {"check_head": self.check}):
            for action in ("command_verify", "command_renew", "command_fail", "command_release"):
                with self.subTest(action=action), self.assertRaises(self.tool["ToolError"]):
                    self.tool[action](self.args)
        self.assertEqual(self.state(), state)

    def test_comment_error_is_not_rollback_of_successful_labels(self):
        def comment_failure(command):
            if command[:2] == ["pr", "comment"]:
                self.calls.append(command)
                raise self.tool["ToolError"]("comment transport failed", 1)
            return self.gh(command)
        with self.assertRaises(self.tool["ToolError"]):
            self.claim(comment_failure)
        self.assert_blocked("before-comment-command")
        self.assertEqual(self.remote_labels, {"codex-repairing"})
        self.assertEqual(self.comments, [])
        self.assertEqual(len(self.calls), 2)

    def test_interruption_retains_reconciliation_state(self):
        def interrupted(command):
            raise KeyboardInterrupt
        with self.assertRaises(KeyboardInterrupt):
            self.claim(interrupted)
        self.assert_blocked("before-label-command")

    def test_initial_head_read_failure_never_reserves_or_mutates(self):
        def failed(args):
            raise self.tool["ToolError"]("head read failed", 1)
        with self.assertRaises(self.tool["ToolError"]):
            self.claim(check=failed)
        self.assertEqual(self.state(), self.initial)
        self.assertEqual(self.calls, [])

    def test_pending_never_grants_concurrent_verify_or_idempotent_claim(self):
        def assert_pending(command):
            state = self.state()
            self.assertEqual(state["leases"][self.key]["status"], "claim-pending")
            with self.assertRaises(self.tool["ToolError"]):
                self.tool["owned_lease"](self.args, state, self.tool["parse_now"](self.args.now))
            with self.assertRaises(self.tool["ToolError"]):
                self.tool["command_claim"](self.args)
            return self.gh(command)
        self.assertEqual(self.claim(assert_pending), 0)
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.state()["leases"][self.key]["status"], "codex-repairing")

    def test_pending_or_uncertain_is_not_replaced_after_expiry_or_head_owner_change(self):
        with self.assertRaises(self.tool["ToolError"]):
            self.claim(lambda command: (_ for _ in ()).throw(self.tool["ToolError"]("EOF", 1)))
        blocked = self.state()
        for status in ("claim-pending", "reconciliation-required"):
            state = copy.deepcopy(blocked)
            state["leases"][self.key]["status"] = status
            write_json(pathlib.Path(self.args.state_file), state)
            self.args.now = "2026-10-29T00:00:00Z"
            self.args.owner = "worker-b"
            with self.subTest(status=status), self.assertRaises(self.tool["ToolError"]):
                self.claim()
            self.assertEqual(self.state(), state)

    def test_remote_postcondition_failure_keeps_consumed_attempt(self):
        calls = 0
        def changed(args):
            nonlocal calls
            calls += 1
            return dict(self.pr, headRefOid=self.head if calls == 1 else "c" * 40)
        # Use the real check_head implementation on the mocked live responses.
        with mock.patch.dict(self.globals, {"current_pr": changed, "gh": self.gh}):
            with self.assertRaisesRegex(self.tool["ToolError"], "head SHA changed"):
                self.tool["command_claim"](self.args)
        self.assert_blocked("before-postcondition-read")
        self.assertEqual(len(self.comments), 1)

    def test_successful_commands_but_wrong_live_labels_are_not_confirmation(self):
        def no_label_effect(command):
            self.calls.append(command)
            return ""
        with self.assertRaises(self.tool["ToolError"]):
            self.claim(no_label_effect)
        self.assert_blocked("before-postcondition-read")
        self.assertEqual(len(self.calls), 2)

    def test_prior_current_head_claim_count_is_not_decremented_after_error(self):
        state = copy.deepcopy(self.initial)
        state["attempts"][self.key + "@" + self.head] = 1
        write_json(pathlib.Path(self.args.state_file), state)
        with self.assertRaises(self.tool["ToolError"]):
            self.claim(lambda command: (_ for _ in ()).throw(self.tool["ToolError"]("EOF", 1)))
        after = self.state()
        self.assertEqual(after["attempts"][self.key + "@" + self.head], 2)
        self.assertEqual(after["attempts"][self.key + "@" + "b" * 40], 1)
        self.assertEqual(after["history"], state["history"])

    def test_success_is_confirmed_then_idempotent_and_schema_valid(self):
        self.assertEqual(self.claim(), 0)
        state = self.state()
        lease = state["leases"][self.key]
        self.assertEqual(lease["status"], "codex-repairing")
        self.assertEqual(lease["remote_sync_phase"], "postconditions-verified")
        self.assertEqual(self.claim(), 0)
        self.assertEqual(self.state(), state)
        self.assertEqual(len(self.calls), 2)
        self.args.output = str(self.root / "verified.json")
        with mock.patch.dict(self.globals, {"check_head": self.check}):
            self.assertEqual(self.tool["command_verify"](self.args), 0)
        verified = json.loads(pathlib.Path(self.args.output).read_text())
        self.assertTrue(verified["safe_to_push_same_branch"])
        self.assertEqual(verified["verification_source"], "live-gh-pr-view")
        self.assertEqual(self.state(), state)
        schema = json.loads((SCRIPTS.parent / "schemas/repair-record.schema.json").read_text())
        errors = runpy.run_path(str(SCRIPTS / "validate-metadata"))["schema_errors"]
        for status in ("codex-repairing", "claim-pending", "reconciliation-required"):
            record = copy.deepcopy(state)
            record["leases"][self.key]["status"] = status
            self.assertEqual(errors(record, schema, schema), [])
        self.assertEqual(errors(json.loads(pathlib.Path(self.args.output).read_text()), schema, schema), [])


if __name__ == "__main__":
    unittest.main()
