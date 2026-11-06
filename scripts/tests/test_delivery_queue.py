# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit

from helpers import SCRIPTS, write_json

sys.path.insert(0, str(SCRIPTS))
import _delivery_queue as queue
from _lib import ToolError, stable_json

REPO = "yinjiayi/openeuler-riscv-packages"
MAIN = "a" * 40
HEAD = "b" * 40
NOW = "2026-11-06T00:00:00Z"


def pr(number=1, package="demo", state="success"):
    return {"number": number, "head_sha": HEAD, "base_sha": MAIN, "head_ref": "onboard/demo",
            "url": f"https://github.com/{REPO}/pull/{number}", "created_at": "2026-08-08T00:00:00Z",
            "updated_at": NOW, "draft": False, "trusted": True, "package_ids": [package], "package_only": True,
            "labels": [], "checks": [{"name": name, "state": state} for name in queue.REQUIRED]}


def seal(document):
    document.pop("snapshot_id", None)
    document["snapshot_id"] = hashlib.sha256(stable_json(document).encode()).hexdigest()
    return document


def snapshot(prs=None, main=MAIN, now=NOW):
    records = [pr()] if prs is None else prs
    return seal({"schema_version": 1, "kind": "delivery-queue-snapshot", "repo": REPO, "main_sha": main,
                 "started_at": now, "collected_at": now, "complete": True, "mode": "full", "check_selection_version": 2,
                 "managed_packages": ["managed"], "pull_requests": records,
                 "coverage": {"open_prs": len(records), "heads_with_complete_checks": len(records)}, "remote_mutations": False})


def options(db, command="claim", **values):
    args = dict(db=str(db), command=command, repo=REPO, owner="worker-a", queue="merge-review", now=NOW,
                expected_main=MAIN, max_age_seconds=900, lease_seconds=60, lease_id="", reason="", outcome="complete")
    args.update(values)
    return argparse.Namespace(**args)


class DeliveryQueueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = self.root / "queue.sqlite"

    def tearDown(self):
        self.temp.cleanup()

    def test_complete_pagination_and_total_count_failure(self):
        seen = []
        def get(path):
            page = int(parse_qs(urlsplit(path).query)["page"][0])
            seen.append(page)
            return {"total_count": 101, "checks": list(range(100)) if page == 1 else [100]}
        self.assertEqual(len(queue.pages(get, "endpoint", "checks")), 101)
        self.assertEqual(seen, [1, 2])
        with self.assertRaisesRegex(ToolError, "incomplete"):
            queue.pages(lambda _: {"total_count": 2, "checks": [1]}, "endpoint", "checks")

    def api_fixture(self, change_main=False, change_head=False, mismatched_check=False, metadata_changes=0, label_change=False, change_base=False):
        reads = {"main": 0, "prs": 0}
        def get(url):
            parsed = urlsplit(url)
            path = parsed.path
            params = parse_qs(parsed.query)
            page = int(params.get("page", [1])[0])
            if path.endswith("/branches/main"):
                reads["main"] += 1
                return {"commit": {"sha": "c" * 40 if change_main and reads["main"] > 1 else MAIN}}
            if "/git/trees/" in path:
                return {"truncated": False, "tree": [{"path": "packages/managed/package.yaml"}]}
            if path.endswith("/pulls"):
                reads["prs"] += 1
                head = "d" * 40 if change_head and reads["prs"] > 1 else HEAD
                changed = min(reads["prs"] - 1, metadata_changes)
                return [{"number": 1, "head": {"sha": head, "ref": "onboard/demo", "repo": {"full_name": REPO}},
                         "base": {"sha": "e" * 40 if change_base and reads["prs"] > 1 else MAIN, "repo": {"full_name": REPO}}, "html_url": f"https://github.com/{REPO}/pull/1",
                         "user": {"login": "yinjiayi"}, "author_association": "OWNER", "created_at": NOW,
                         "updated_at": f"2026-11-06T00:00:{changed:02d}Z", "draft": False,
                         "labels": [{"name": "needs-native-riscv"}] if changed and label_change else []}]
            if path.endswith("/files"):
                return [{"filename": "packages/demo/package.yaml", "status": "added"}]
            if path.endswith("/check-runs"):
                runs = [{"id": i + 1, "name": name, "head_sha": "f" * 40 if mismatched_check else HEAD,
                         "status": "completed", "conclusion": "success", "app": {"id": 1}} for i, name in enumerate(queue.REQUIRED)]
                runs += [{"id": 100 + i, "name": "configure", "head_sha": HEAD, "status": "completed",
                          "conclusion": "cancelled" if i < 100 else "success", "app": {"id": 1}} for i in range(101)]
                return {"total_count": len(runs), "check_runs": runs[(page - 1) * 100:page * 100]}
            if path.endswith("/statuses"):
                return [{"id": 1, "context": "legacy", "state": "failure"}, {"id": 2, "context": "legacy", "state": "success"}]
            self.fail(url)
        return get

    def test_full_snapshot_includes_files_checks_statuses_main_and_latest_only(self):
        document = queue.collect_snapshot(REPO, 2, self.api_fixture(), NOW)
        self.assertTrue(document["complete"])
        self.assertEqual(document["coverage"]["heads_with_complete_checks"], 1)
        self.assertEqual(document["managed_packages"], ["managed"])
        record = document["pull_requests"][0]
        self.assertEqual(record["package_ids"], ["demo"])
        self.assertEqual(len(record["checks"]), 108)
        self.assertEqual(queue.classify(record, MAIN), ("held", "ci-evidence-ambiguous"))
        queue.sync(self.db, document, now=NOW)

    def graphql_fixture(self, overflow=False, renamed=False):
        def read(query, variables):
            self.assertTrue(query.startswith("query("))
            self.assertNotIn("mutation", query)
            checks = [{"databaseId": i + 1, "name": name, "status": "COMPLETED", "conclusion": "SUCCESS",
                       "detailsUrl": "https://github.com/example/check", "checkSuite": {"app": {"databaseId": 1}, "commit": {"oid": HEAD}}}
                      for i, name in enumerate(queue.REQUIRED)]
            return {"repository": {"p0": {"number": 1, "headRefOid": HEAD, "changedFiles": 1,
                    "files": {"totalCount": 1, "pageInfo": {"hasNextPage": False},
                              "nodes": [{"path": "packages/demo/package.yaml", "changeType": "RENAMED" if renamed else "ADDED"}]},
                    "commits": {"nodes": [{"commit": {"oid": HEAD, "statusCheckRollup": {"contexts": {
                        "totalCount": 101 if overflow else 6, "pageInfo": {"hasNextPage": overflow}, "nodes": checks}}}}]}}}}
        return read

    def test_graphql_batches_full_common_case_without_per_pr_rest_calls(self):
        get = self.api_fixture()
        calls = []
        def bounded(path):
            calls.append(path)
            self.assertFalse(any(part in path for part in ("/files", "/check-runs", "/statuses")), path)
            return get(path)
        result = queue.collect_snapshot(REPO, 2, bounded, NOW, self.graphql_fixture())
        self.assertEqual(len(calls), 5)  # main before/after, membership before/after, tree
        self.assertEqual(queue.classify(result["pull_requests"][0], MAIN)[0], "merge-review")

    def test_graphql_overflow_and_rename_use_complete_rest_fallback(self):
        calls = []
        get = self.api_fixture()
        def recording(path):
            calls.append(path)
            return get(path)
        result = queue.collect_snapshot(REPO, 2, recording, NOW, self.graphql_fixture(overflow=True, renamed=True))
        self.assertTrue(any("/files" in path for path in calls))
        self.assertTrue(any("/check-runs" in path and "page=2" in path for path in calls))
        self.assertEqual(len(result["pull_requests"][0]["checks"]), 108)

    def test_cross_suite_pending_or_failure_is_not_hidden_by_larger_success_id(self):
        normal = self.graphql_fixture()
        for state, conclusion in (("IN_PROGRESS", None), ("COMPLETED", "FAILURE")):
            def conflicting(query, variables):
                response = normal(query, variables)
                contexts = response["repository"]["p0"]["commits"]["nodes"][0]["commit"]["statusCheckRollup"]["contexts"]
                pending = copy.deepcopy(contexts["nodes"][0])
                contexts["nodes"][0]["databaseId"] = 1000
                pending.update(databaseId=1, status=state, conclusion=conclusion)
                pending["checkSuite"]["databaseId"] = 999
                contexts["nodes"].append(pending)
                contexts["totalCount"] += 1
                return response
            document = queue.collect_snapshot(REPO, 2, self.api_fixture(), NOW, conflicting)
            self.assertEqual(len(document["pull_requests"][0]["checks"]), 7)
            self.assertEqual(queue.classify(document["pull_requests"][0], MAIN), ("held", "ci-evidence-ambiguous"))

    def test_changed_main_or_head_and_wrong_check_sha_fail_closed(self):
        for variant in ({"change_main": True}, {"change_head": True}, {"mismatched_check": True}, {"change_base": True}):
            with self.subTest(variant=variant), self.assertRaises(ToolError):
                queue.collect_snapshot(REPO, 2, self.api_fixture(**variant), NOW)

    def test_comment_only_drift_refreshes_changed_record_and_keeps_full_bracket(self):
        document = queue.collect_snapshot(REPO, 2, self.api_fixture(metadata_changes=1), NOW, self.graphql_fixture())
        self.assertEqual(document["refresh_rounds"], 1)
        self.assertEqual(document["refreshes"][0]["pr_numbers"], [1])
        self.assertEqual(document["pull_requests"][0]["updated_at"], "2026-11-06T00:00:01Z")
        self.assertEqual(queue.classify(document["pull_requests"][0], MAIN)[0], "merge-review")

    def test_same_head_label_change_replaces_trust_and_checks_not_old_success(self):
        document = queue.collect_snapshot(REPO, 2, self.api_fixture(metadata_changes=1, label_change=True), NOW, self.graphql_fixture())
        self.assertEqual(document["refresh_rounds"], 1)
        self.assertEqual(queue.classify(document["pull_requests"][0], MAIN), ("held", "needs-native-riscv"))

    def test_metadata_drift_has_two_round_hard_limit(self):
        document = queue.collect_snapshot(REPO, 2, self.api_fixture(metadata_changes=2), NOW, self.graphql_fixture())
        self.assertEqual(document["refresh_rounds"], 2)
        with self.assertRaisesRegex(ToolError, "two refresh rounds"):
            queue.collect_snapshot(REPO, 2, self.api_fixture(metadata_changes=3), NOW, self.graphql_fixture())

    def test_pending_is_waiting_and_human_native_untrusted_are_not_claimable(self):
        records = [pr(1, "pending", "pending"), pr(2, "human"), pr(3, "native"), pr(4, "fork")]
        records[1]["labels"] = ["needs-human"]
        records[2]["labels"] = ["needs-native-riscv"]
        records[3]["trusted"] = False
        queue.sync(self.db, snapshot(records), now=NOW)
        for lane in queue.QUEUES:
            self.assertEqual(queue.lease_action(options(self.db, queue=lane))["status"], "empty")
        self.assertEqual(queue.classify(records[0], MAIN), ("waiting", "ci-pending"))

    def test_failed_and_missing_checks_enter_repair_not_merge(self):
        failed = pr(state="failure")
        missing = pr(2, "missing")
        missing["checks"] = [{"name": "configure", "state": "success"}]
        self.assertEqual(queue.classify(failed, MAIN)[0], "repair")
        self.assertEqual(queue.classify(missing, MAIN), ("repair", "missing-or-incomplete-checks"))
        self.assertEqual(queue.classify(pr(), MAIN)[0], "merge-review")

    def test_canonical_dedup_covers_managed_all_prs_and_input_duplicates(self):
        multi = pr()
        multi["package_ids"] = ["demo", "second"]
        multi["package_only"] = False
        result = queue.sync(self.db, snapshot([multi]), [{"package_id": name} for name in ["managed", "demo", "second", "new", "new"]], NOW)
        self.assertEqual(len(result["excluded_candidates"]), 4)
        claim = queue.lease_action(options(self.db, queue="intake"))
        self.assertEqual(claim["package_id"], "new")
        self.assertFalse(claim["authorizes_remote_mutation"])

    def test_renamed_cross_package_scope_and_path_traversal(self):
        ids, scoped = queue.package_paths([{"filename": "packages/new/a", "previous_filename": "packages/old/a", "status": "renamed"}])
        self.assertEqual(ids, ["new", "old"])
        self.assertFalse(scoped)
        with self.assertRaises(ToolError):
            queue.package_paths([{"filename": "packages/demo/../x", "status": "added"}])

    def test_same_database_many_processes_claim_package_only_once(self):
        queue.sync(self.db, snapshot([pr(1), pr(2)]), now=NOW)
        command = [sys.executable, str(SCRIPTS / "delivery-queue"), "claim", "--db", str(self.db), "--repo", REPO,
                   "--queue", "merge-review", "--expected-main", MAIN, "--now", NOW]
        workers = [subprocess.Popen(command + ["--owner", f"worker-{i}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for i in range(8)]
        outcomes = []
        for worker in workers:
            out, error = worker.communicate(timeout=30)
            self.assertEqual(worker.returncode, 0, error)
            outcomes.append(json.loads(out)["status"])
        self.assertEqual(outcomes.count("claimed"), 1)
        self.assertEqual(outcomes.count("empty"), 7)

    def test_expiry_renew_owner_fencing_and_release(self):
        queue.sync(self.db, snapshot(), now=NOW)
        first = queue.lease_action(options(self.db))
        with self.assertRaisesRegex(ToolError, "another worker"):
            queue.lease_action(options(self.db, "renew", lease_id=first["lease_id"], owner="wrong"))
        result = queue.lease_action(options(self.db, "renew", lease_id=first["lease_id"], now="2026-11-06T00:00:30Z"))
        self.assertEqual(result["status"], "renewed")
        self.assertEqual(queue.lease_action(options(self.db, now="2026-11-06T00:01:20Z"))["status"], "empty")
        second = queue.lease_action(options(self.db, now="2026-11-06T00:01:31Z"))
        self.assertEqual(second["status"], "claimed")
        self.assertNotEqual(first["lease_id"], second["lease_id"])
        with self.assertRaises(ToolError):
            queue.lease_action(options(self.db, "release", lease_id=first["lease_id"], now="2026-11-06T00:01:32Z"))

    def test_targeted_claim_preserves_eligibility_and_exclusion(self):
        held = pr(3, "held", "failure")
        held["labels"] = ["needs-human"]
        queue.sync(self.db, snapshot([pr(1, "older", "failure"), pr(2, "target", "failure"), held,
                                     pr(4, "waiting", "pending"), pr(5, "green")]), now=NOW)
        parsed = queue.parser().parse_args(["claim", "--db", str(self.db), "--repo", REPO,
                                           "--queue", "repair", "--owner", "worker-b", "--expected-main", MAIN,
                                           "--item-key", "pr:2", "--now", NOW])
        claim = queue.lease_action(parsed)
        self.assertEqual(claim["item_key"], "pr:2")
        for target in ("pr:999", "pr:2", "pr:3", "pr:4", "pr:5"):
            with self.subTest(target=target), self.assertRaisesRegex(ToolError, "requested item"):
                queue.lease_action(options(self.db, queue="repair", item_key=target))
        self.assertEqual(queue.lease_action(options(self.db, queue="repair"))["item_key"], "pr:1")
        with queue.database(self.db) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM leases").fetchone()[0], 2)

    def test_remote_repair_routing_keeps_only_existing_owner_and_audits_transition(self):
        before = pr(state="failure")
        before["labels"] = ["repair-queued", "other-label"]
        queue.sync(self.db, snapshot([before]), now=NOW)
        lease = queue.lease_action(options(self.db, queue="repair"))
        after = copy.deepcopy(before)
        after["labels"] = ["codex-repairing", "other-label"]
        for second in (1, 2):
            observed = f"2026-11-06T00:00:0{second}Z"
            queue.sync(self.db, snapshot([after], now=observed), now=observed)
            self.assertEqual(queue.lease_action(options(self.db, "renew", lease_id=lease["lease_id"], now=observed))["status"], "renewed")
            with self.assertRaisesRegex(ToolError, "requested item"):
                queue.lease_action(options(self.db, queue="repair", item_key="pr:1", owner="other", now=observed))
        with queue.database(self.db) as db:
            current = db.execute("SELECT * FROM leases").fetchone()
            self.assertEqual(current["lease_id"], lease["lease_id"])
            self.assertEqual(current["owner"], "worker-a")
            self.assertEqual(current["fingerprint"], queue.task_fingerprint(after))
            self.assertEqual(db.execute("SELECT queue FROM items").fetchone()[0], "held")
            self.assertEqual(db.execute("SELECT COUNT(*) FROM events WHERE action='repair-routing-preserved'").fetchone()[0], 1)
        self.assertEqual(queue.lease_action(options(self.db, "release", lease_id=lease["lease_id"], outcome="waiting",
                                                  reason="repair push handed to CI", now="2026-11-06T00:00:03Z"))["status"], "released")

    def test_remote_repair_routing_never_waives_real_changes_or_expiry(self):
        variants = ("needs-human", "needs-native-riscv", "security-blocked", "checks", "files", "head", "main", "expired", "no-queued-label")
        for variant in variants:
            with self.subTest(variant=variant):
                db_path = self.root / (variant + ".sqlite")
                before = pr(state="failure")
                before["labels"] = [] if variant == "no-queued-label" else ["repair-queued"]
                queue.sync(db_path, snapshot([before]), now=NOW)
                lease = queue.lease_action(options(db_path, queue="repair"))
                after = copy.deepcopy(before)
                after["labels"] = ["codex-repairing"]
                if variant in queue.HOLDS:
                    after["labels"].append(variant)
                elif variant == "checks":
                    after["checks"][0]["state"] = "success"
                elif variant == "files":
                    after["files"] = [{"filename": "packages/demo/changed.spec"}]
                elif variant == "head":
                    after["head_sha"] = "d" * 40
                observed = "2026-11-06T00:01:01Z" if variant == "expired" else "2026-11-06T00:00:01Z"
                main = "e" * 40 if variant == "main" else MAIN
                queue.sync(db_path, snapshot([after], main=main, now=observed), now=observed)
                with queue.database(db_path) as db:
                    self.assertEqual(db.execute("SELECT COUNT(*) FROM leases").fetchone()[0], 0)
                    self.assertEqual(db.execute("SELECT COUNT(*) FROM events WHERE action='repair-routing-preserved'").fetchone()[0], 0)
                with self.assertRaises(ToolError):
                    queue.lease_action(options(db_path, "renew", lease_id=lease["lease_id"], expected_main=main, now=observed))
                self.assertEqual(queue.lease_action(options(db_path, queue="repair", expected_main=main, now=observed))["status"], "empty")

    def test_waiting_release_frees_worker_and_same_snapshot_does_not_resurrect(self):
        document = snapshot()
        queue.sync(self.db, document, now=NOW)
        first = queue.lease_action(options(self.db))
        queue.lease_action(options(self.db, "release", lease_id=first["lease_id"], outcome="waiting", reason="new CI"))
        queue.sync(self.db, document, now=NOW)
        self.assertEqual(queue.lease_action(options(self.db))["status"], "empty")
        with queue.database(self.db) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM leases").fetchone()[0], 0)
        newer = snapshot(now="2026-11-06T00:00:01Z")
        newer["pull_requests"][0]["checks_collected_at"] = "2026-11-06T00:00:01Z"
        seal(newer)
        queue.sync(self.db, newer, now="2026-11-06T00:00:01Z")
        self.assertEqual(queue.lease_action(options(self.db, now="2026-11-06T00:00:01Z"))["status"], "empty")
        newer["pull_requests"][0]["head_sha"] = "d" * 40
        queue.sync(self.db, seal(newer), now="2026-11-06T00:00:01Z")
        self.assertEqual(queue.lease_action(options(self.db, now="2026-11-06T00:00:01Z"))["status"], "claimed")

    def test_blocked_candidate_survives_new_time_and_main_until_explicit_requeue(self):
        candidate = [{"package_id": "candidate", "version": "1.0"}]
        queue.sync(self.db, snapshot([]), candidate, NOW)
        claim = queue.lease_action(options(self.db, queue="intake"))
        queue.lease_action(options(self.db, "release", lease_id=claim["lease_id"], outcome="blocked", reason="Missing test provider; require verified provider before retry"))
        newer = snapshot([], main="c" * 40, now="2026-11-06T00:00:01Z")
        queue.sync(self.db, newer, candidate, "2026-11-06T00:00:01Z")
        args = options(self.db, queue="intake", expected_main="c" * 40, now="2026-11-06T00:00:02Z")
        self.assertEqual(queue.lease_action(args)["status"], "empty")
        retry = options(self.db, "requeue", item_key="intake:candidate", expected_main="c" * 40,
                        now="2026-11-06T00:00:02Z", reason="Provider verified against new target repository manifest")
        self.assertEqual(queue.lease_action(retry)["queue"], "intake")
        self.assertEqual(queue.lease_action(args)["status"], "claimed")

    def test_manual_pr_hold_is_not_cleared_by_main_or_ci_refresh(self):
        queue.sync(self.db, snapshot(), now=NOW)
        claim = queue.lease_action(options(self.db))
        queue.lease_action(options(self.db, "release", lease_id=claim["lease_id"], outcome="blocked", reason="Artifact absent; require newly verified physical evidence"))
        newer = snapshot(main="c" * 40, now="2026-11-06T00:00:01Z")
        newer["pull_requests"][0]["base_sha"] = "c" * 40
        newer["pull_requests"][0]["checks"] = list(reversed(newer["pull_requests"][0]["checks"]))
        queue.sync(self.db, seal(newer), now="2026-11-06T00:00:01Z")
        self.assertEqual(queue.lease_action(options(self.db, expected_main="c" * 40, now="2026-11-06T00:00:02Z"))["status"], "empty")

    def test_explicit_requeue_cannot_clear_needs_human_or_candidate_blocker(self):
        record = pr()
        record["labels"] = ["needs-human"]
        queue.sync(self.db, snapshot([record]), [{"package_id": "blocked", "blocker": "license unresolved"}], NOW)
        for item in ("pr:1", "intake:blocked"):
            result = queue.lease_action(options(self.db, "requeue", item_key=item, reason="Request another inspection"))
            self.assertEqual(result["queue"], "held")

    def test_main_or_head_changes_invalidate_existing_lease(self):
        for change in ("main", "head"):
            with self.subTest(change=change):
                db = self.root / (change + ".sqlite")
                queue.sync(db, snapshot(), now=NOW)
                old = queue.lease_action(options(db))
                newer = snapshot(now="2026-11-06T00:00:01Z")
                if change == "main":
                    newer["main_sha"] = "c" * 40
                    newer["pull_requests"][0]["base_sha"] = "c" * 40
                else:
                    newer["pull_requests"][0]["head_sha"] = "d" * 40
                queue.sync(db, seal(newer), now="2026-11-06T00:00:01Z")
                with self.assertRaises(ToolError):
                    queue.lease_action(options(db, "renew", lease_id=old["lease_id"], now="2026-11-06T00:00:02Z"))

    def test_candidate_input_change_fences_old_renew_and_release(self):
        queue.sync(self.db, snapshot([]), [{"package_id": "candidate", "version": "1.0"}], NOW)
        first = queue.lease_action(options(self.db, queue="intake"))
        newer = snapshot([], now="2026-11-06T00:00:01Z")
        queue.sync(self.db, newer, [{"package_id": "candidate", "version": "2.0"}], "2026-11-06T00:00:01Z")
        for command in ("renew", "release"):
            with self.assertRaises(ToolError):
                queue.lease_action(options(self.db, command, lease_id=first["lease_id"], now="2026-11-06T00:00:02Z"))
        second = queue.lease_action(options(self.db, queue="intake", now="2026-11-06T00:00:02Z"))
        self.assertEqual(second["item"]["version"], "2.0")
        self.assertNotEqual(first["task_fingerprint"], second["task_fingerprint"])

    def test_old_check_normalization_snapshot_is_not_admitted(self):
        older = snapshot()
        older.pop("check_selection_version")
        with self.assertRaisesRegex(ToolError, "superseded"):
            queue.sync(self.db, seal(older), now=NOW)

    def test_stale_partial_tampered_or_rollback_snapshot_fails(self):
        document = snapshot()
        queue.sync(self.db, document, now=NOW)
        with self.assertRaisesRegex(ToolError, "stale"):
            queue.lease_action(options(self.db, now="2026-11-06T00:20:00Z"))
        with self.assertRaisesRegex(ToolError, "expected main"):
            queue.lease_action(options(self.db, expected_main="c" * 40))
        bad = copy.deepcopy(document)
        bad["complete"] = False
        with self.assertRaises(ToolError):
            queue.sync(self.db, bad, now=NOW)
        bad = copy.deepcopy(document)
        bad["main_sha"] = "c" * 40
        with self.assertRaisesRegex(ToolError, "checksum"):
            queue.sync(self.db, bad, now=NOW)
        older = snapshot(now="2026-11-05T00:00:00Z")
        with self.assertRaisesRegex(ToolError, "older snapshot"):
            queue.sync(self.db, older, now=NOW)

    def test_four_agent_forward_delivery_scenario_real_cli_no_remote(self):
        """Coordinator + three workers: A waits, B held, C exclusive, D repair."""
        document = snapshot([pr(1, "package-a", "pending"), pr(4, "package-d", "failure")])
        input_file, candidates = self.root / "snapshot.json", self.root / "candidates.json"
        write_json(input_file, document)
        write_json(candidates, [{"package_id": "package-b", "blocker": "Original test dependency absent; resume after target provider is validated"},
                                {"package_id": "package-c", "source_license_prechecked": True}])
        base = [sys.executable, str(SCRIPTS / "delivery-queue")]
        def invoke(args):
            result = subprocess.run(base + args, text=True, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        invoke(["sync", "--db", str(self.db), "--snapshot", str(input_file), "--candidates", str(candidates), "--now", NOW])
        common = ["--db", str(self.db), "--repo", REPO, "--expected-main", MAIN, "--now", NOW]
        racers = [subprocess.Popen(base + ["claim"] + common + ["--owner", owner, "--queue", "intake"],
                                   text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for owner in ("worker-1", "worker-2")]
        claims = []
        for worker in racers:
            out, err = worker.communicate(timeout=30)
            self.assertEqual(worker.returncode, 0, err)
            claims.append(json.loads(out))
        winners = [claim for claim in claims if claim["status"] == "claimed"]
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0]["package_id"], "package-c")
        repair = invoke(["claim"] + common + ["--owner", "worker-3", "--queue", "repair"])
        self.assertEqual(repair["package_id"], "package-d")
        summary = invoke(["summary", "--db", str(self.db), "--repo", REPO, "--now", NOW])
        self.assertEqual(summary["queues"], {"held": 1, "intake": 1, "repair": 1, "waiting": 1})
        self.assertEqual(len(summary["active_leases"]), 2)
        self.assertFalse(winners[0]["authorizes_remote_mutation"])
        self.assertFalse(repair["authorizes_remote_mutation"])
        for claim in (winners[0], repair):
            invoke(["release", "--db", str(self.db), "--repo", REPO, "--owner", claim["owner"], "--lease-id", claim["lease_id"],
                    "--outcome", "requeue", "--reason", "Fixture drill ended; no remote operation performed", "--now", NOW])


if __name__ == "__main__":
    unittest.main()
