# SPDX-License-Identifier: Apache-2.0
import copy
import json
import pathlib
import runpy
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[2]
M = runpy.run_path(str(ROOT / "ci/collect-github-state.py"))
SHA = "a" * 40


class CurrentGitHubStateTests(unittest.TestCase):
    def _assert_actual_collection_fence(self, mode, exception, reason=None):
        node = {"number": 1, "title": "infra", "url": "https://github.com/a/b/pull/1",
            "state": "OPEN", "isDraft": False, "createdAt": "2026-01-01T00:00:00Z",
            "updatedAt": "2026-01-01T00:00:00Z", "mergedAt": None, "headRefName": "x",
            "headRefOid": SHA, "baseRefName": "main", "baseRefOid": SHA,
            "author": {"login": "a"}, "autoMergeRequest": None,
            "labels": {"totalCount": 0, "nodes": []}, "headRef": None,
            "files": {"totalCount": 2 if mode == "head" else 1,
                "pageInfo": {"hasNextPage": mode == "head", "endCursor": "files"},
                "nodes": [{"path": "ci/x.py"}]}}
        initial_cursors = []; calls = []
        def execute(argv, input, **kwargs):
            body = json.loads(input); query = body["query"]; cursor = body["variables"].get("cursor")
            calls.append(query)
            if 'pullRequest(number:' in query:
                self.assertEqual(mode, "head")
                repo = {"pullRequest": {"headRefOid": "b"*40, "files": {"totalCount": 2,
                    "pageInfo": {"hasNextPage": False, "endCursor": None}, "nodes": [{"path": "ci/y.py"}]}}}
            elif 'pullRequests' in query:
                initial_cursors.append(cursor)
                head = "b"*40 if mode == "main" and cursor else SHA
                selected = [copy.deepcopy(node)]
                if mode == "duplicate": selected.append(copy.deepcopy(node))
                if mode == "cursor" and cursor: selected[0]["number"] = 2
                continuing = mode == "cursor" or (mode == "main" and cursor is None)
                repo = {"defaultBranchRef": {"target": {"oid": head}}, "pullRequests": {
                    "totalCount": 3 if mode == "cursor" else 1 if mode == "head" else 2,
                    "pageInfo": {"hasNextPage": continuing, "endCursor": "same" if continuing else None},
                    "nodes": selected}}
            else: self.fail("unexpected query past fatal collection fence")
            return types.SimpleNamespace(returncode=0, stdout=json.dumps({"data": {"repository": repo}}).encode(), stderr=b"")
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory); receipt = base/"safe.json"
            with patch.object(M["subprocess"], "run", side_effect=execute):
                with self.assertRaises(exception):
                    M["collect_snapshot"]("a/b", ROOT, base/"private", receipt)
            safe = json.loads(receipt.read_text()); self.assertEqual(safe["status"], "failed")
            self.assertNotIn("accepted_attempt", safe)
            if reason:
                self.assertEqual(len(safe["attempts"]), 2)
                self.assertTrue(all(a["reason"] == reason for a in safe["attempts"]))
                self.assertEqual(initial_cursors.count(None), 2)
            else:
                self.assertEqual(len(safe["attempts"]), 1)
                self.assertEqual(safe["attempts"][0]["status"], "fatal")
                self.assertEqual(initial_cursors.count(None), 1)
            self.assertEqual(len(calls), 4 if mode in ("main", "head") else 2 if mode == "cursor" else 1)

    def test_actual_main_change_is_typed_and_restarts_only_whole_snapshot(self):
        self._assert_actual_collection_fence("main", M["SnapshotDrift"], "main-during-pages")

    def test_actual_paginated_file_head_change_is_typed_and_bounded(self):
        self._assert_actual_collection_fence("head", M["SnapshotDrift"], "pr-head-during-files")

    def test_actual_non_advancing_cursor_is_fatal_without_snapshot_retry(self):
        self._assert_actual_collection_fence("cursor", ValueError)

    def test_actual_duplicate_census_ids_are_fatal_without_snapshot_retry(self):
        self._assert_actual_collection_fence("duplicate", ValueError)

    def test_population_drift_restarts_whole_snapshot_without_mixing_pages(self):
        def node(number):
            return {"number": number, "title": "infra", "url": "https://github.com/a/b/pull/%d" % number,
                "state": "OPEN", "isDraft": False, "createdAt": "2026-01-01T00:00:00Z",
                "updatedAt": "2026-01-01T00:00:00Z", "mergedAt": None, "headRefName": "x",
                "headRefOid": SHA, "baseRefName": "main", "baseRefOid": SHA,
                "author": {"login": "a"}, "autoMergeRequest": None,
                "labels": {"totalCount": 0, "nodes": []}, "headRef": None,
                "files": {"totalCount": 1, "pageInfo": {"hasNextPage": False, "endCursor": None},
                          "nodes": [{"path": "ci/x.py"}]}}
        initial_calls = []
        def execute(argv, input, **kwargs):
            body = json.loads(input); query = body["query"]
            repo = {"defaultBranchRef": {"target": {"oid": SHA}}}
            if 'nodes{number updatedAt headRefOid}' in query:
                repo["pullRequests"] = {"totalCount": 1, "pageInfo": {"hasNextPage": False},
                    "nodes": [{"number": 2, "updatedAt": "2026-01-01T00:00:00Z", "headRefOid": SHA}]}
            elif 'pullRequests' in query:
                initial_calls.append(body["variables"].get("cursor"))
                first = len(initial_calls) == 1
                repo["pullRequests"] = {"totalCount": 2 if len(initial_calls) == 2 else 1,
                    "pageInfo": {"hasNextPage": first, "endCursor": "next" if first else None},
                    "nodes": [node(1 if first else 2)]}
            return types.SimpleNamespace(returncode=0, stdout=json.dumps({"data": {"repository": repo}}).encode(), stderr=b"")
        class API:
            receipts = []
            def __init__(self, *args): pass
            def get(self, _): return {"workflow_runs": [], "total_count": 0}
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory); raw = base/"private"; receipt = base/"public-receipt.json"
            with patch.object(M["subprocess"], "run", side_effect=execute), patch.dict(M["H"], {"API": API}):
                result = M["collect_snapshot"]("a/b", ROOT, raw, receipt)
            self.assertEqual([r["number"] for r in result["pull_requests"]], [2])
            self.assertEqual(initial_calls, [None, "next", None])
            safe = json.loads(receipt.read_text())
            self.assertEqual(safe["accepted_attempt"], 2)
            self.assertEqual([a["status"] for a in safe["attempts"]], ["snapshot-drift", "collected"])
            self.assertEqual(safe["attempts"][0]["reason"], "pr-population-during-pages")
            runs = list(raw.glob("snapshot-*")); self.assertEqual(len(runs), 1)
            first, second = runs[0]/"attempt-01", runs[0]/"attempt-02"
            self.assertTrue((first/"pr-page-001.json").is_file())
            self.assertFalse((first/"receipt.json").exists())
            self.assertTrue((second/"receipt.json").is_file())
            self.assertTrue(all(str(second) in r["path"] for r in result["raw_receipts"]))
            self.assertNotIn(str(raw), receipt.read_text())

    def test_persistent_drift_is_bounded_with_safe_failed_receipt(self):
        globals_ = M["collect_snapshot"].__globals__
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory); receipt = base/"safe.json"; paths = []
            def fail(repository, root, raw):
                paths.append(raw); raw.mkdir(); (raw/"partial.json").write_text('{"old":true}')
                raise M["SnapshotDrift"]("main-during-pages")
            with patch.dict(globals_, {"collect": fail}):
                with self.assertRaises(M["SnapshotDrift"]):
                    M["collect_snapshot"]("a/b", ROOT, base/"private", receipt)
            self.assertEqual(len(paths), 2); self.assertNotEqual(*paths)
            safe = json.loads(receipt.read_text())
            self.assertEqual(safe["status"], "failed")
            self.assertEqual(safe["maximum_attempts"], 2)
            self.assertNotIn("accepted_attempt", safe)
            self.assertTrue(all(a["status"] == "snapshot-drift" for a in safe["attempts"]))

    def test_arbitrary_api_schema_identity_errors_are_fatal_and_redacted(self):
        globals_ = M["collect_snapshot"].__globals__
        failures = [ValueError("GraphQL read failed secret"), ValueError("PR tree/blob identity mismatch secret"),
                    json.JSONDecodeError("secret", "secret", 0), KeyError("secret")]
        for failure in failures:
            with self.subTest(error=type(failure).__name__), tempfile.TemporaryDirectory() as directory:
                base = pathlib.Path(directory); receipt = base/"safe.json"
                with patch.dict(globals_, {"collect": unittest.mock.Mock(side_effect=failure)}):
                    with self.assertRaises(type(failure)):
                        M["collect_snapshot"]("a/b", ROOT, base/"private", receipt)
                    self.assertEqual(globals_["collect"].call_count, 1)
                text = receipt.read_text(); self.assertNotIn("secret", text)
                safe = json.loads(text); self.assertEqual(safe["status"], "failed")
                self.assertEqual(safe["attempts"][0]["reason"], "fatal-input-or-api-error")

    def test_repeated_invocations_never_overwrite_private_attempts(self):
        globals_ = M["collect_snapshot"].__globals__
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory); paths = []
            def success(repository, root, raw):
                paths.append(raw); raw.mkdir(); (raw/"proof").write_text("original")
                return {"raw_receipts": []}
            with patch.dict(globals_, {"collect": success}):
                for number in (1, 2):
                    M["collect_snapshot"]("a/b", ROOT, base/"private", base/("safe%d.json" % number))
            self.assertNotEqual(paths[0].parent, paths[1].parent)
            self.assertTrue(all((p/"proof").read_text() == "original" for p in paths))

    def test_cli_fatal_error_writes_no_public_snapshot_or_exception_text(self):
        globals_ = M["main"].__globals__
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory); output = base/"github-state.json"; receipt = base/"safe.json"
            argv = ["collector", "--repository", "a/b", "--raw-dir", str(base/"private"),
                    "--output", str(output), "--receipt", str(receipt)]
            with patch.object(sys, "argv", argv), patch.dict(globals_, {
                    "collect": unittest.mock.Mock(side_effect=ValueError("do-not-expose-token"))}), patch.object(sys, "stderr") as stderr:
                with self.assertRaises(SystemExit) as error: M["main"]()
            self.assertEqual(error.exception.code, 1)
            self.assertFalse(output.exists()); self.assertEqual(json.loads(receipt.read_text())["status"], "failed")
            self.assertNotIn("do-not-expose-token", str(stderr.write.call_args_list))

    def test_cli_refuses_stale_or_colliding_public_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory); stale = base/"snapshot.json"; stale.write_text("user-data")
            for output, receipt in [(stale, base/"receipt.json"), (base/"new.json", stale),
                                     (base/"same.json", base/"same.json")]:
                with patch.object(sys, "argv", ["collector", "--repository", "a/b", "--raw-dir", str(base/"private"),
                        "--output", str(output), "--receipt", str(receipt)]), patch.object(sys, "stderr"):
                    with self.assertRaises(SystemExit) as error: M["main"]()
                self.assertEqual(error.exception.code, 2)
                self.assertEqual(stale.read_text(), "user-data")
            self.assertFalse((base/"private").exists())

    def test_collector_retains_current_check_provenance_and_partial_connections(self):
        check = {"databaseId": 123, "name": "configure", "status": "COMPLETED", "conclusion": "SUCCESS",
            "detailsUrl": "https://github.com/a/b/actions/runs/88/job/123", "startedAt": "2026-01-01T00:01:00Z",
            "completedAt": "2026-01-01T00:02:00Z", "checkSuite": {"databaseId": 44, "createdAt": "2026-01-01T00:00:00Z",
            "app": {"databaseId": 15368}, "commit": {"oid": SHA}, "workflowRun": {"databaseId": 88, "runAttempt": 2}}}
        status = {"id": "SC1", "context": "lint", "state": "SUCCESS", "targetUrl": "https://example.com/lint",
            "createdAt": "2026-01-01T00:00:00Z", "updatedAt": "2026-01-01T00:01:00Z", "commit": {"oid": SHA}, "creator": {"login": "provider"}}
        node = {"number": 1, "title": "infra", "url": "https://github.com/a/b/pull/1", "state": "OPEN", "isDraft": False,
            "createdAt": "2026-01-01T00:00:00Z", "updatedAt": "2026-01-01T00:00:00Z", "mergedAt": None,
            "headRefName": "x", "headRefOid": SHA, "baseRefName": "main", "baseRefOid": SHA, "author": {"login": "a"},
            "autoMergeRequest": None, "labels": {"totalCount": 0, "nodes": []},
            "files": {"totalCount": 1, "pageInfo": {"hasNextPage": False, "endCursor": None}, "nodes": [{"path": "ci/x.py"}]},
            "headRef": {"target": {"oid": SHA, "statusCheckRollup": {"state": "SUCCESS", "contexts": {
            "totalCount": 2, "pageInfo": {"hasNextPage": False, "endCursor": None}, "nodes": [check, status]}}}}}
        class API:
            receipts = []
            def __init__(self, *args): pass
            def get(self, _): return {"workflow_runs": [], "total_count": 0}
        def execute(argv, input, **kwargs):
            query = json.loads(input)["query"]
            if 'nodes{number updatedAt headRefOid}' in query:
                connection = {"totalCount": 1, "pageInfo": {"hasNextPage": False}, "nodes": [{"number": 1, "updatedAt": node["updatedAt"], "headRefOid": SHA}]}
            elif 'pullRequests' in query:
                self.assertIn("databaseId createdAt app{databaseId}", query)
                self.assertIn("startedAt completedAt", query)
                self.assertIn("workflowRun{databaseId runAttempt}", query)
                connection = {"totalCount": 1, "pageInfo": {"hasNextPage": False}, "nodes": [copy.deepcopy(node)]}
            else: connection = None
            repo = {"defaultBranchRef": {"target": {"oid": SHA}}}
            if connection: repo["pullRequests"] = connection
            return types.SimpleNamespace(returncode=0, stdout=json.dumps({"data": {"repository": repo}}).encode(), stderr=b"")
        def collect():
            with tempfile.TemporaryDirectory() as directory, patch.object(M["subprocess"], "run", side_effect=execute), patch.dict(M["H"], {"API": API}):
                return M["collect"]("a/b", ROOT, pathlib.Path(directory))["pull_requests"][0]
        row = collect()
        self.assertTrue(row["checks_complete"])
        self.assertTrue(row["check_selection_metadata_complete"])
        self.assertEqual(row["check_selection_version"], 1)
        self.assertEqual(row["check_runs"][0]["check_run_id"], 123)
        self.assertEqual(row["check_runs"][0]["app_id"], 15368)
        self.assertEqual(row["check_runs"][0]["workflow_run_attempt"], 2)
        self.assertEqual(row["status_contexts"][0]["creator_login"], "provider")
        check["checkSuite"]["app"] = None
        self.assertFalse(collect()["check_selection_metadata_complete"])
        check["checkSuite"]["app"] = {"databaseId": 15368}
        node["headRef"]["target"]["statusCheckRollup"]["contexts"]["pageInfo"]["hasNextPage"] = True
        self.assertFalse(collect()["checks_complete"])
        self.assertFalse(collect()["check_selection_metadata_complete"])
        node["headRef"]["target"]["statusCheckRollup"]["contexts"]["pageInfo"]["hasNextPage"] = False
        status["commit"]["oid"] = "b" * 40
        self.assertFalse(collect()["checks_complete"])

    def test_freshness_frontier_past_first_100_withholds_changed_head(self):
        nodes = [{"number": n, "title": "infrastructure", "url": "https://github.com/a/b/pull/%d" % n,
            "state": "OPEN", "isDraft": False, "createdAt": "2026-01-01T00:00:00Z",
            "updatedAt": "2099-01-01T00:00:00Z", "mergedAt": None, "headRefName": "x", "headRefOid": SHA,
            "baseRefName": "main", "baseRefOid": SHA, "author": {"login": "a"}, "autoMergeRequest": None,
            "labels": {"totalCount": 0, "nodes": []}, "headRef": {"target": {"oid": SHA, "statusCheckRollup": None}},
            "files": {"totalCount": 1, "pageInfo": {"hasNextPage": False, "endCursor": "1"}, "nodes": [{"path": "ci/x.py"}]}}
            for n in range(1, 126)]
        def execute(argv, input, **kwargs):
            body = json.loads(input); query = body["query"]; cursor = body["variables"].get("cursor")
            if 'nodes{number updatedAt headRefOid}' in query:
                start = int(cursor or 0); selected = [{"number": r["number"], "updatedAt": r["updatedAt"],
                    "headRefOid": "b"*40 if r["number"] == 101 else SHA} for r in nodes[start:start+100]]
                size = 100
            elif 'pullRequests' in query:
                start = int(cursor or 0); selected = copy.deepcopy(nodes[start:start+25]); size = 25
            else:
                return types.SimpleNamespace(returncode=0, stdout=json.dumps({"data": {"repository": {"defaultBranchRef": {"target": {"oid": SHA}}}}}).encode(), stderr=b"")
            repo = {"defaultBranchRef": {"target": {"oid": SHA}}, "pullRequests": {"totalCount": 125,
                "nodes": selected, "pageInfo": {"hasNextPage": start+size < 125, "endCursor": str(start+size)}}}
            return types.SimpleNamespace(returncode=0, stdout=json.dumps({"data": {"repository": repo}}).encode(), stderr=b"")
        class API:
            receipts = []
            def __init__(self, *args): pass
            def get(self, _): return {"workflow_runs": [], "total_count": 0}
        with tempfile.TemporaryDirectory() as directory, patch.object(M["subprocess"], "run", side_effect=execute), patch.dict(M["H"], {"API": API}):
            result = M["collect"]("a/b", ROOT, pathlib.Path(directory))
        self.assertEqual(result["coverage"]["freshness_frontier_pages"], 2)
        self.assertEqual(len(result["pull_requests"]), 125)
        changed = next(r for r in result["pull_requests"] if r["number"] == 101)
        self.assertFalse(changed["snapshot_head_current"])
        self.assertFalse(changed["checks_complete"])
        self.assertFalse(result["coverage"]["complete"])
        self.assertIn("checks_observed_at", changed)


if __name__ == "__main__": unittest.main()
