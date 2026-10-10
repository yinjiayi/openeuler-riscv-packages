# SPDX-License-Identifier: Apache-2.0
import copy
import json
import pathlib
import runpy
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[2]
M = runpy.run_path(str(ROOT / "ci/collect-github-state.py"))
SHA = "a" * 40


class CurrentGitHubStateTests(unittest.TestCase):
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
