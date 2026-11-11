# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import copy
import json
import pathlib
import runpy
import shutil
import sys
import tempfile
import unittest

from helpers import SCRIPTS, run_tool, write_json

sys.path.insert(0, str(SCRIPTS))
GEN = runpy.run_path(str(SCRIPTS / "generate-dashboard"))
SHA = "a" * 40
TREE = "b" * 40


def current_check(name, number, conclusion="success", status="completed", time="2026-10-09T00:01:00Z", app=15368, suite_time="2026-10-09T00:00:00Z"):
    return {"name": name, "check_run_id": number, "app_id": app, "head_sha": SHA,
            "check_suite_id": number, "check_suite_created_at": suite_time,
            "started_at": time, "completed_at": time if status == "completed" else None,
            "status": status, "conclusion": conclusion}


def current_pr(checks):
    return {"state": "OPEN", "headRefOid": SHA, "checks_complete": True, "snapshot_head_current": True,
            "check_selection_version": 1, "check_selection_metadata_complete": True, "check_runs": checks}


def observation(package_id="libdemo-perl", run_id=1, head=SHA, tree=TREE, event="pull_request", branch="onboard/libdemo-perl-1.0"):
    job = {"id": 1, "name": "rpmbuild-riscv64", "step_name": "Build SRPM and RPM with verified source networking", "step_number": 1, "completed_at": "2026-10-09T00:00:00Z", "runner_labels": ["ubuntu-latest"]}
    return {"id": f"{run_id}:1:{head}:{package_id}", "package_id": package_id, "head_sha": head, "recipe_tree_sha": tree, "recipe_blob_sha": "c" * 40,
            "recipe": {"version": "1.0", "release": "1", "ref": head, "rpm_name": "perl-Demo", "aliases": [], "discovery_keys": []},
            "provenance": {"identity_method": "exact-compare-files", "base_sha": "d" * 40, "api_raw_sha256": ["d" * 64]}, "run_id": run_id, "run_attempt": 1,
            "event": event, "head_branch": branch, "workflow_head_sha": head, "created_at": "2026-10-08T23:00:00Z", "completed_at": "2026-10-09T00:00:00Z",
            "run_url": f"https://github.com/yinjiayi/openeuler-riscv-packages/actions/runs/{run_id}", "build_status": "passed", "smoke_status": "passed", "evidence_strength": "hosted-step", "jobs": {"build": job, "smoke": dict(job, id=2, name="rpm-install-smoke", step_name="Install RPM and run smoke test")}}


def history(items, complete=False):
    return {"schema_version": 1, "kind": "package-build-history", "repository": "yinjiayi/openeuler-riscv-packages", "generated_at": "2026-10-09T00:00:00Z",
            "snapshot": {"cutoff": "2026-10-09T00:00:00Z", "started_at": "2026-10-08T23:00:00Z", "coverage_complete": complete, "lower_bound": not complete, "reasons": [] if complete else [{"reason": "jobs-unavailable", "count": 1}], "listed_run_count": 2, "expected_attempt_count": 2, "processed_attempt_count": 1, "unresolved_count": 0 if complete else 1, "windows": [], "deleted_history_recoverable": False},
            "observations": items, "attempts": [], "summary": {"distinct_package_count": len({item["package_id"] for item in items}), "distinct_recipe_count": len({(item["package_id"], item["recipe_tree_sha"]) for item in items}), "success_tuple_count": len(items)}, "limitations": ["Deleted history cannot be recovered; hosted steps are not physical acceptance."]}


def view(items, prs=None, metadata=None, trees=None, complete=False, builds=None):
    resolver = GEN["CanonicalPackages"]()
    for item in items:
        resolver.add(item["package_id"], [item["recipe"]["rpm_name"]])
    for package_id in metadata or {}:
        resolver.add(package_id, [])
    return GEN["history_view"](history(items, complete), resolver, metadata or {}, trees or {}, prs or {}, builds or {}, {}, {})


def published_fixture():
    generation = "demo-" + SHA + "-1-1"
    origin = "http://2.27.148.101:38080/generations/" + generation + "/"
    repositories, metadata = {}, {}
    for kind in ("riscv64", "source"):
        base = origin + kind + "/"
        repositories[kind] = {"baseurl": base, "repomd_sha256": "b" * 64, "rpm_count": 1}
        metadata[kind] = {"repomd_url": base + "repodata/repomd.xml", "repomd_sha256": "b" * 64, "primary_url": base + "repodata/primary.xml.gz", "primary_sha256": "c" * 64, "primary_open_sha256": "d" * 64, "primary_size": 1, "primary_open_size": 1, "package_count": 1}
    def artifact(kind, arch):
        filename = "demo-1.0-1." + arch + ".rpm"
        return {"filename": filename, "url": origin + kind + "/Packages/" + filename, "sha256": "e" * 64, "size": 10, "arch": arch, "verified_at": "2026-10-09T00:00:00Z"}
    return {"schema_version": 1, "kind": "dashboard-published-state", "started_at": "2026-10-08T23:00:00Z", "generated_at": "2026-10-09T00:00:00Z", "repository": "yinjiayi/openeuler-riscv-packages", "main_sha": SHA,
            "generation": generation, "state_url": "http://2.27.148.101:38080/state.json", "state_sha256": "a" * 64, "generation_state_url": origin + "state.json", "published_at": "2026-10-08T23:00:00Z", "repositories": repositories, "verified_repomd_sha256": {"source": "b" * 64, "riscv64": "b" * 64}, "metadata": metadata,
            "coverage": {"status": "complete", "source_packages": 1, "matched_packages": 1, "verified_packages": 1, "rpm_files": 1, "srpm_files": 1, "verified_files": 2, "verified_bytes": 20, "gaps": []},
            "trust": {"transport": "operator-provided HTTP endpoint", "unsigned_rpms": True, "scope": "Checksum transport/metadata/payload evidence only, no install or signing trust."},
            "verified_artifacts": [artifact("source", "src"), artifact("riscv64", "riscv64")],
            "packages": [{"package_id": "demo", "rpm_name": "demo", "versions": [{"epoch": "0", "version": "1.0", "release": "1", "source": artifact("source", "src"), "binaries": [artifact("riscv64", "riscv64")]}]}]}


class DashboardHistoryGeneratorTests(unittest.TestCase):
    def test_old_success_new_failure_is_cumulative_not_current(self):
        old = observation()
        pr = {"state": "OPEN", "headRefOid": "e" * 40, "canonical_identity_verified": True, "statusCheckRollup": [{"conclusion": "FAILURE"}]}
        result = view([old], {old["package_id"]: pr}, {old["package_id"]: {"rpm": {"name": "perl-Demo"}}}, {old["package_id"]: "f" * 40})
        self.assertEqual(result["metrics"]["cumulative_success_packages"], 1)
        self.assertEqual(result["metrics"]["current_main_success_packages"], 0)
        self.assertEqual(result["metrics"]["current_pr_success_packages"], 0)
        self.assertEqual(result["packages"][0]["current_pr_status"], "failed")
        self.assertTrue(result["packages"][0]["ever_succeeded"])

    def test_duplicate_observations_and_reruns_do_not_multiply_package_count(self):
        old = observation()
        rerun = observation(run_id=2)
        result = view([old, copy.deepcopy(old), rerun])
        self.assertEqual(result["metrics"]["cumulative_success_packages"], 1)
        self.assertEqual(result["packages"][0]["success_observation_count"], 2)
        self.assertEqual(result["duplicate_observations_ignored"], 1)
        conflict = copy.deepcopy(old)
        conflict["recipe_tree_sha"] = "d" * 40
        with self.assertRaisesRegex(GEN["ToolError"], "conflicting"):
            view([old, conflict])

    def test_skipped_build_and_overall_green_never_count(self):
        skipped = observation()
        skipped["build_status"] = "skipped"
        result = view([skipped])
        self.assertEqual(result["metrics"]["cumulative_success_packages"], 0)
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "history.json"
            write_json(path, history([skipped]))
            with self.assertRaisesRegex(GEN["ToolError"], "input-invalid"):
                GEN["load_history"](str(path))

    def test_pr_only_success_visible_but_main_requires_actual_tree_and_ref(self):
        pr_only = observation()
        result = view([pr_only])
        self.assertFalse(result["packages"][0]["on_current_main"])
        self.assertEqual(result["metrics"]["cumulative_success_packages"], 1)
        metadata = {pr_only["package_id"]: {"rpm": {"name": "perl-Demo"}}}
        result = view([pr_only], metadata=metadata, trees={pr_only["package_id"]: TREE})
        self.assertEqual(result["metrics"]["current_main_success_packages"], 0)
        main = observation(event="push", branch="main")
        result = view([main], metadata=metadata, trees={main["package_id"]: TREE})
        self.assertEqual(result["metrics"]["current_main_success_packages"], 1)
        main["head_branch"] = "unreviewed-branch"
        self.assertEqual(view([main], metadata=metadata, trees={main["package_id"]: TREE})["metrics"]["current_main_success_packages"], 0)

    def test_current_pr_needs_actual_identity_and_repair_state_takes_precedence(self):
        item = observation()
        pr = current_pr([current_check(name, number) for number, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)])
        self.assertEqual(view([item], {item["package_id"]: pr})["metrics"]["current_pr_success_packages"], 0)
        pr["check_runs"] = [current_check(name, number, "skipped") for number, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)]
        pr["canonical_identity_verified"] = True
        self.assertEqual(view([item], {item["package_id"]: pr})["metrics"]["current_pr_success_packages"], 0)
        pr["check_runs"] = [current_check(name, number) for number, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)]
        self.assertEqual(view([item], {item["package_id"]: pr})["metrics"]["current_pr_success_packages"], 1)
        for label in ("repair-queued", "codex-repairing", "needs-human"):
            pr["labels"] = [label]
            result = view([item], {item["package_id"]: pr})
            self.assertEqual(result["metrics"]["current_pr_success_packages"], 0)
            self.assertEqual(result["packages"][0]["current_pr_status"], label)

    def test_aliases_are_explicit_unique_not_functional_provider_or_fuzzy(self):
        resolver = GEN["CanonicalPackages"]()
        which = json.loads((SCRIPTS.parent / "packages/which/package.yaml").read_text())
        resolver.add("which", GEN["metadata_aliases"](which))
        self.assertIsNone(resolver.resolve(["debianutils"]))
        resolver.add("libdemo-perl", ["perl-Demo"])
        self.assertEqual(resolver.entry({"discovery_key": "perl-demo", "names": ["perl-Demo"]}), "libdemo-perl")
        self.assertIsNone(resolver.resolve(["demo-perl"]))
        resolver.add("different", ["perl-Demo"])
        self.assertIsNone(resolver.entry({"names": ["perl-Demo"]}))

    def test_real_paths_override_misleading_labels_and_digit_branch_guess(self):
        self.assertEqual(GEN["package_from_pr"]({"files": [{"path": "packages/sha256-tools/package.yaml"}], "labels": ["package:other"]}), "sha256-tools")
        self.assertIsNone(GEN["package_from_pr"]({"files": [{"path": "README.md"}], "labels": ["package:demo"], "headRefName": "onboard/demo-1.0"}))
        self.assertIsNone(GEN["package_from_pr"]({"files": [{"path": "packages/one/a"}, {"path": "packages/two/b"}]}))
        self.assertIsNone(GEN["package_from_pr"]({"headRefName": "onboard/demo-1.0", "labels": ["package:demo"]}))

    def test_coverage_and_publication_unavailable_are_explicit(self):
        partial = view([observation()])
        complete = view([observation()], complete=True)
        self.assertTrue(partial["lower_bound"])
        self.assertFalse(partial["coverage_complete"])
        self.assertEqual(partial["reasons"][0]["count"], 1)
        self.assertTrue(complete["coverage_complete"])
        self.assertIsNone(partial["metrics"]["published_packages"])
        self.assertEqual(partial["publication_coverage"], "unavailable")
        self.assertEqual(GEN["published_links"]("demo", [{"upload": {"status": "staged"}, "verification": {"status": "passed"}}])["rpm"], [])

    def test_latest_head_boolean_does_not_rebind_current_main(self):
        item = observation(event="push", branch="main")
        metadata = {item["package_id"]: {"rpm": {"name": "perl-Demo"}}}
        old_failed = {"status": "failed", "latest_head_verified": True, "recipe_tree_sha": "e" * 40}
        result = view([item], metadata=metadata, trees={item["package_id"]: TREE}, builds={item["package_id"]: old_failed})
        self.assertEqual(result["metrics"]["current_main_success_packages"], 1)
        old_failed.update(recipe_tree_sha=TREE, head_branch="main")
        result = view([item], metadata=metadata, trees={item["package_id"]: TREE}, builds={item["package_id"]: old_failed})
        self.assertEqual(result["metrics"]["current_main_success_packages"], 1)
        self.assertTrue(result["packages"][0]["current_main_recipe_succeeded"])
        self.assertEqual(result["packages"][0]["current_main_status"], "failed")

    def test_open_pr_precedes_newer_closed_and_pending_checks_precede_passed(self):
        opened = {"package_id": "demo", "state": "OPEN", "updated_at": "2026-10-08T00:00:00Z", "number": 1}
        closed = dict(opened, state="CLOSED", updated_at="2026-10-09T00:00:00Z", number=2)
        self.assertEqual(GEN["latest_prs"]([opened, closed])["demo"]["number"], 1)
        pr = current_pr([current_check(name, number) for number, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)] + [current_check("policy", 3, None, "queued")])
        self.assertEqual(GEN["pr_state"](pr), "ci-queued")
        self.assertFalse(GEN["current_pr_success_checks"](pr))

    def test_latest_context_ignores_old_cancelled_but_not_latest_failure(self):
        build = [current_check(name, number) for number, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)]
        older = current_check("configure", 3, "cancelled", time="2026-10-09T00:00:00Z")
        newer = current_check("configure", 4, time="2026-10-09T00:02:00Z")
        for order in ([older, newer], [newer, older]):
            pr = current_pr(build + order)
            self.assertEqual(GEN["pr_state"](pr), "passed")
            self.assertTrue(GEN["current_pr_success_checks"](pr))
        for conclusion, status, expected in (("failure", "completed", "failed"), ("cancelled", "completed", "failed"), (None, "in_progress", "building"), (None, "queued", "ci-queued")):
            pr = current_pr(build + [older, dict(newer, conclusion=conclusion, status=status, completed_at=newer["completed_at"] if status == "completed" else None)])
            self.assertEqual(GEN["pr_state"](pr), expected)
            self.assertFalse(GEN["current_pr_success_checks"](pr))

    def test_missing_conflicting_or_unbound_current_checks_fail_closed(self):
        base = [current_check(name, number) for number, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)]
        for field in ("check_run_id", "app_id", "head_sha", "check_suite_id", "check_suite_created_at", "completed_at"):
            checks = copy.deepcopy(base);checks[0].pop(field)
            self.assertFalse(GEN["current_pr_success_checks"](current_pr(checks)), field)
            self.assertEqual(GEN["pr_state"](current_pr(checks)), "pr-open")
        for changes in ({"head_sha": "f"*40}, {"app_id": 777}, {"check_suite_created_at": "bad time"}, {"status": "invented"}):
            checks = [dict(base[0], **changes), base[1]]
            self.assertFalse(GEN["current_pr_success_checks"](current_pr(checks)))
        pr = current_pr(base + [dict(base[0], conclusion="failure")])
        self.assertEqual(GEN["pr_state"](pr), "pr-open")
        self.assertFalse(GEN["current_pr_success_checks"](pr))
        for flag in ("checks_complete", "snapshot_head_current", "check_selection_metadata_complete"):
            pr = current_pr(base);pr[flag] = False
            self.assertEqual(GEN["pr_state"](pr), "pr-open")
        legacy = {"checks_complete": True, "snapshot_head_current": True, "headRefOid": SHA, "check_runs": base}
        self.assertEqual(GEN["pr_state"](legacy), "pr-open")
        self.assertFalse(GEN["current_pr_success_checks"](legacy))
        self.assertEqual(GEN["pr_state"]({"checks": [{"name": "build", "conclusion": "success"}]}), "pr-open")

    def test_distinct_apps_and_unstarted_checks_cannot_hide_latest_result(self):
        checks = [current_check(name, number) for number, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)]
        failed = current_check("rpmbuild-riscv64", 3, "failure", time="2026-10-09T00:02:00Z")
        foreign = current_check("rpmbuild-riscv64", 4, app=777, time="2026-10-09T00:03:00Z")
        self.assertEqual(GEN["pr_state"](current_pr(checks+[failed, foreign])), "failed")
        old_unstarted = current_check("configure", 5, "cancelled", suite_time="2026-10-08T00:00:00Z", time="2026-10-08T00:01:00Z");old_unstarted["started_at"] = None
        newer = current_check("configure", 6)
        # An older suite may have been reused: absence of an individual start
        # cannot prove that its cancelled check happened before the newer suite.
        self.assertEqual(GEN["pr_state"](current_pr(checks+[old_unstarted,newer])), "pr-open")
        self.assertFalse(GEN["current_pr_success_checks"](current_pr(checks+[old_unstarted,newer])))
        newest = dict(newer, check_run_id=7, status="queued", conclusion=None, started_at=None, completed_at=None)
        self.assertEqual(GEN["pr_state"](current_pr(checks+[newer,newest])), "pr-open")
        self.assertFalse(GEN["current_pr_success_checks"](current_pr(checks+[newer,newest])))
        latest_cancel = dict(old_unstarted, check_run_id=8, check_suite_created_at="2026-10-10T00:00:00Z", started_at="2026-10-10T00:00:30Z", completed_at="2026-10-10T00:01:00Z")
        self.assertEqual(GEN["pr_state"](current_pr(checks+[newer,latest_cancel])), "failed")

    def test_older_suite_later_rerun_never_hides_failure_or_pending(self):
        build = [current_check(name, number) for number, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)]
        newer_suite = current_check("configure", 10, suite_time="2026-10-09T00:02:00Z", time="2026-10-09T00:03:00Z")
        for conclusion, status, expected in (("failure", "completed", "failed"), (None, "in_progress", "building"), (None, "queued", "ci-queued")):
            old_suite_rerun = current_check("configure", 11, conclusion, status, time="2026-10-09T00:04:00Z")
            old_suite_rerun.update(check_suite_id=99, workflow_run_attempt=2)
            for order in ([newer_suite, old_suite_rerun], [old_suite_rerun, newer_suite]):
                pr = current_pr(build + order)
                self.assertEqual(GEN["pr_state"](pr), expected)
                self.assertFalse(GEN["current_pr_success_checks"](pr))
                selected = [check for check in GEN["pr_checks"](pr) if check["name"] == "configure"]
                self.assertEqual(selected[0]["check_run_id"], 11)
            # Real queued reruns often have no startedAt. The old suite's
            # creation/ID cannot establish the individual rerun's ordering.
            old_suite_rerun.update(started_at=None)
            for order in ([newer_suite, old_suite_rerun], [old_suite_rerun, newer_suite]):
                pr = current_pr(build + order)
                self.assertEqual(GEN["pr_state"](pr), "pr-open")
                self.assertFalse(GEN["current_pr_success_checks"](pr))

    def test_observed_two_pr_configure_sequences_still_select_latest_green(self):
        # Minimal immutable October 9 #2494/#2495 check chronology, not a new
        # hosted run or target acceptance. Full raw snapshots accompany review.
        cases = (
            ("19e72e255985cb42a3ffa341b86ce7f2225e91d5", "2026-10-09T17:21:06Z",
             ((113939157271, "17:21:04", "17:21:05"), (113939164454, "17:21:05", "17:21:06"), (113939173514, "17:21:07", "17:21:07")),
             113939182215, "17:21:10", "17:21:20"),
            ("ade25896b3b69bc08710369f732693ee04c775bd", "2026-10-09T18:31:47Z",
             ((113967215859, "18:31:46", "18:31:47"),), 113967225854, "18:31:49", "18:32:00"),
        )
        for head, suite_created, cancelled, number, started, completed in cases:
            build = [current_check(name, n) for n, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)]
            old = [dict(current_check("configure", n, "cancelled", time="2026-10-09T"+start+"Z"), completed_at="2026-10-09T"+end+"Z") for n, start, end in cancelled]
            latest = dict(current_check("configure", number, time="2026-10-09T"+started+"Z", suite_time=suite_created), completed_at="2026-10-09T"+completed+"Z")
            for order in (old+[latest], [latest]+list(reversed(old))):
                pr = current_pr([dict(check, head_sha=head) for check in build+order]);pr["headRefOid"] = head
                self.assertEqual(GEN["pr_state"](pr), "passed")
                self.assertTrue(GEN["current_pr_success_checks"](pr))

    def test_legacy_status_contexts_have_separate_latest_identity(self):
        checks = [current_check(name, number) for number, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)]
        context = {"id": "SC1", "context": "lint", "creator_login": "provider", "head_sha": SHA,
                   "created_at": "2026-10-09T00:00:00Z", "updated_at": "2026-10-09T00:00:00Z", "state": "failure"}
        latest = dict(context, id="SC2", state="success", created_at="2026-10-09T00:01:00Z", updated_at="2026-10-09T00:01:00Z")
        pr = current_pr(checks);pr["status_contexts"] = [latest, context]
        self.assertTrue(GEN["current_pr_success_checks"](pr))
        pr["status_contexts"].append(dict(latest, id="SC3", state="pending", created_at="2026-10-09T00:02:00Z", updated_at="2026-10-09T00:02:00Z"))
        self.assertEqual(GEN["pr_state"](pr), "ci-queued")
        self.assertFalse(GEN["current_pr_success_checks"](pr))

    def test_check_start_ties_are_unknown_but_identical_records_deduplicate(self):
        build = [current_check(name, number) for number, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)]
        first = current_check("configure", 10)
        for conclusion in ("failure", "success"):
            tied = dict(first, check_run_id=11, check_suite_id=99, conclusion=conclusion)
            for order in ([first,tied], [tied,first]):
                pr = current_pr(build+order)
                self.assertEqual(GEN["pr_state"](pr), "pr-open")
                self.assertFalse(GEN["current_pr_success_checks"](pr))
            later = current_check("configure", 12, time="2026-10-09T00:02:00Z")
            self.assertTrue(GEN["current_pr_success_checks"](current_pr(build+[first,tied,later])))
        pr = current_pr(build+[first,copy.deepcopy(first)])
        self.assertTrue(GEN["current_pr_success_checks"](pr))
        self.assertEqual(len(GEN["pr_checks"](pr)), 3)
        cancelled = dict(first, conclusion="cancelled", started_at=None)
        self.assertEqual(GEN["pr_state"](current_pr(build+[cancelled,copy.deepcopy(cancelled)])), "failed")

    def test_status_time_ties_are_unknown_but_identical_records_deduplicate(self):
        build = [current_check(name, number) for number, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)]
        first = {"id":"SC1", "context":"lint", "creator_login":"provider", "head_sha":SHA,
                 "created_at":"2026-10-09T00:01:00Z", "updated_at":"2026-10-09T00:01:00Z", "state":"success"}
        for state in ("failure", "success"):
            tied = dict(first, id="SC2", state=state)
            for order in ([first,tied], [tied,first]):
                pr = current_pr(build);pr["status_contexts"] = order
                self.assertEqual(GEN["pr_state"](pr), "pr-open")
                self.assertFalse(GEN["current_pr_success_checks"](pr))
            pr["status_contexts"].append(dict(first, id="SC3", created_at="2026-10-09T00:02:00Z", updated_at="2026-10-09T00:02:00Z"))
            self.assertTrue(GEN["current_pr_success_checks"](pr))
        pr = current_pr(build);pr["status_contexts"] = [first,copy.deepcopy(first)]
        self.assertTrue(GEN["current_pr_success_checks"](pr))
        self.assertEqual(len(GEN["pr_checks"](pr)), 3)

    def test_raw_connection_complete_is_not_current_selection_complete(self):
        item = observation()
        legacy = {"number": 9, "state": "open", "headRefOid": SHA, "canonical_identity_verified": True,
                  "checks_complete": True, "snapshot_head_current": True,
                  "check_runs": [{"name": "rpmbuild-riscv64", "conclusion": "success"}]}
        source = {"generated_at": "2026-10-09T00:00:00Z", "coverage": {"complete": True}, "pull_requests": [legacy]}
        resolver = GEN["CanonicalPackages"]();resolver.add(item["package_id"], [])
        def result(): return GEN["history_view"](history([item]), resolver, {}, {}, {item["package_id"]: source["pull_requests"][0]}, {}, {}, {}, source)
        value = result()
        self.assertTrue(value["current_pr_source_available"])
        self.assertFalse(value["current_pr_source_complete"])
        self.assertEqual(value["current_pr_selection_gaps"][0]["pr"], 9)
        self.assertEqual(value["metrics"]["cumulative_success_packages"], 1)
        self.assertEqual(value["metrics"]["current_pr_success_packages"], 0)
        good = current_pr([current_check(name, number) for number, name in enumerate(("rpmbuild-riscv64", "rpm-install-smoke"), 1)])
        good.update(number=9, canonical_identity_verified=True);source["pull_requests"] = [good]
        self.assertTrue(result()["current_pr_source_complete"])
        self.assertEqual(result()["current_pr_selection_gaps"], [])
        good["check_runs"].append(dict(good["check_runs"][0], check_run_id=3, status="queued", conclusion=None, started_at=None, completed_at=None))
        self.assertFalse(result()["current_pr_source_complete"])
        self.assertEqual(result()["metrics"]["current_pr_success_packages"], 0)

    def test_successful_ledger_requires_actual_job_step_semantics(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "history.json"
            forged = observation()
            forged["jobs"]["build"]["name"] = "configure"
            write_json(path, history([forged]))
            with self.assertRaisesRegex(GEN["ToolError"], "step identity"):
                GEN["load_history"](str(path))

    def test_summary_seed_duplicate_and_actual_historical_step_contract(self):
        item = observation(event="workflow_dispatch", branch="main")
        item["workflow_head_sha"] = "f" * 40
        item["jobs"]["build"]["step_name"] = "Build SRPM and RPM without network"
        item["provenance"]["identity_method"] = "scope-log+exact-package-tree"
        document = history([item])
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "history.json"
            write_json(path, document)
            loaded = GEN["load_history"](str(path))
            self.assertEqual(loaded["summary"]["success_tuple_count"], 1)
            self.assertEqual(view(loaded["observations"])["metrics"]["cumulative_success_packages"], 1)
            duplicated = history([item, copy.deepcopy(item)])
            write_json(path, duplicated)
            with self.assertRaisesRegex(GEN["ToolError"], "duplicate build-history seed"):
                GEN["load_history"](str(path))
            self.assertEqual(view(duplicated["observations"])["duplicate_observations_ignored"], 1)
            invalid_scope = copy.deepcopy(document)
            invalid_scope["observations"][0]["event"] = "pull_request"
            write_json(path, invalid_scope)
            with self.assertRaisesRegex(GEN["ToolError"], "only valid for dispatch"):
                GEN["load_history"](str(path))
            document["summary"]["distinct_package_count"] = 9999
            write_json(path, document)
            with self.assertRaisesRegex(GEN["ToolError"], "summary disagrees"):
                GEN["load_history"](str(path))
            document = history([observation()])
            document["observations"][0]["jobs"]["build"]["step_name"] = "Build SRPM and RPM"
            write_json(path, document)
            with self.assertRaisesRegex(GEN["ToolError"], "step identity"):
                GEN["load_history"](str(path))

    def test_legacy_dispatch_requires_reviewed_workflow_and_cannot_inflate_main(self):
        item = observation(event="workflow_dispatch", branch="main")
        item["workflow_head_sha"] = "f" * 40
        item["provenance"].update(identity_method="legacy-workflow-contract+exact-package-tree", workflow_contract_sha256="729eb4d5b19325b09ab3f675c0725e54f18eb424d9a880a7df9910c49b9f9e75")
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "history.json"
            write_json(path, history([item]))
            self.assertEqual(len(GEN["load_history"](str(path))["observations"]), 1)
            self.assertEqual(view([item], metadata={item["package_id"]: {}}, trees={item["package_id"]: TREE})["metrics"]["current_main_success_packages"], 0)
            for mutation in ("event", "contract"):
                damaged = copy.deepcopy(item)
                if mutation == "event":
                    damaged["event"] = "push"
                else:
                    damaged["provenance"]["workflow_contract_sha256"] = "0" * 64
                write_json(path, history([damaged]))
                with self.assertRaisesRegex(GEN["ToolError"], "reviewed dispatch workflow contract"):
                    GEN["load_history"](str(path))

    def test_ambiguous_inventory_and_canonical_overlay_have_unique_keys(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            (root / "dashboard").mkdir()
            for name in ("index.html", "app.js", "styles.css"):
                shutil.copyfile(SCRIPTS.parent / "dashboard" / name, root / "dashboard" / name)
            write_json(root / "packages/libdemo-perl/package.yaml", {"package_id": "libdemo-perl", "rpm": {"name": "perl-Demo"}, "version": {"current": "2.0"}})
            inventory = root / "inventory.json"
            write_json(inventory, {"entries": [{"discovery_key": "perl-demo", "names": ["perl-Demo"], "status": "discovered"}]})
            github = root / "github.json"
            write_json(github, {"generated_at": "2026-10-09T00:00:00Z", "coverage": {"complete": True}, "pull_requests": [{"number": 1, "state": "OPEN", "actual_files": ["packages/perl-demo/package.yaml"], "actual_files_complete": True, "head": {"sha": SHA, "ref": "onboard/perl-demo-1.0"}}]})
            output = root / "public"
            run_tool("generate-dashboard", ["--repo-root", str(root), "--package-inventory", str(inventory), "--github-state", str(github), "--output-dir", str(output)], root)
            rows = json.loads((output / "inventory.json").read_text())["entries"]
            self.assertEqual(len(rows), 3)
            self.assertEqual(len({row["inventory_id"] for row in rows}), len(rows))
            original = next(row for row in rows if row["inventory_id"] == "perl-demo")
            self.assertIsNone(original.get("package_id"))
            overlay = next(row for row in rows if row["inventory_id"] == "canonical:perl-demo")
            self.assertEqual(overlay["package_id"], "perl-demo")

    def test_dispatch_candidate_does_not_masquerade_as_main(self):
        item = observation(event="workflow_dispatch", branch="main")
        item["provenance"]["identity_method"] = "scope-log+exact-package-tree"
        item["workflow_head_sha"] = "f" * 40
        self.assertEqual(view([item], metadata={item["package_id"]: {}}, trees={item["package_id"]: TREE})["metrics"]["current_main_success_packages"], 0)
        document = history([item])
        document["attempts"] = [{"id": "1:1:" + "f" * 40, "run_id": 1, "run_attempt": 1, "head_sha": "f" * 40, "terminal": True, "status": "success", "api_raw_sha256": ["d" * 64]}]
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "history.json"
            write_json(path, document)
            self.assertEqual(len(GEN["load_history"](str(path))["observations"]), 1)
            unbound = copy.deepcopy(document)
            unbound["attempts"] = []
            del unbound["observations"][0]["workflow_head_sha"]
            write_json(path, unbound)
            with self.assertRaisesRegex(GEN["ToolError"], "scope identity"):
                GEN["load_history"](str(path))
            document["attempts"][0].update(status="unresolved", terminal=False)
            write_json(path, document)
            with self.assertRaisesRegex(GEN["ToolError"], "terminal reason"):
                GEN["load_history"](str(path))

    def test_complete_actual_paths_and_current_checks_required(self):
        pr = {"actual_files": ["packages/demo/package.yaml"], "actual_files_complete": False}
        self.assertFalse(GEN["complete_pr_identity"](pr, "demo"))
        pr["actual_files_complete"] = True
        self.assertTrue(GEN["complete_pr_identity"](pr, "demo"))
        item = observation()
        pr = {"state": "OPEN", "headRefOid": SHA, "canonical_identity_verified": True}
        self.assertEqual(view([item], {item["package_id"]: pr})["metrics"]["current_pr_success_packages"], 0)

    def test_same_head_old_success_does_not_hide_current_failure(self):
        pr = {"state": "OPEN", "headRefOid": SHA, "statusCheckRollup": [{"conclusion": "FAILURE"}]}
        row = GEN["inventory_row"]({"managed_package": {"package_id": "demo"}, "status": "managed"}, pr, {"status": "passed", "commit_sha": SHA}, None)
        self.assertEqual(row["status"], "failed")

    def test_full_generator_links_perl_inventory_and_history_only_package(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            (root / "dashboard").mkdir()
            for name in ("index.html", "app.js", "styles.css"):
                shutil.copyfile(SCRIPTS.parent / "dashboard" / name, root / "dashboard" / name)
            write_json(root / "packages/libdemo-perl/package.yaml", {"package_id": "libdemo-perl", "rpm": {"name": "perl-Demo"}, "version": {"current": "2.0"}})
            inventory = root / "inventory.json"
            write_json(inventory, {"entries": [{"discovery_key": "perl-demo", "names": ["perl-Demo"], "status": "discovered", "stable_versions": ["1.0"]}]})
            hist = root / "history.json"
            other = observation(package_id="libpr-only-perl", run_id=2)
            other["recipe"]["rpm_name"] = "perl-PR-Only"
            write_json(hist, history([observation(), other]))
            output = root / "public"
            run_tool("generate-dashboard", ["--repo-root", str(root), "--package-inventory", str(inventory), "--build-history", str(hist), "--output-dir", str(output), "--now", "2026-10-09T00:01:00Z"], root)
            data = json.loads((output / "data.json").read_text())
            full = json.loads((output / "inventory.json").read_text())
            self.assertEqual(data["build_history"]["metrics"]["cumulative_success_packages"], 2)
            self.assertFalse(data["build_history"]["current_pr_source_available"])
            self.assertIsNone(data["build_history"]["current_pr_source_generated_at"])
            self.assertFalse(data["update_health"]["source_available"])
            self.assertEqual(len([row for row in full["entries"] if row.get("package_id") == "libdemo-perl"]), 1)
            self.assertEqual(full["entries"][0]["inventory_id"], "perl-demo")
            self.assertEqual(full["entries"][0]["version"], "2.0")
            self.assertTrue(any(row["package_id"] == "libpr-only-perl" for row in data["build_history"]["packages"]))
            self.assertEqual(json.loads((output / "build-history.json").read_text()), data["build_history"])
            self.assertEqual(json.loads((output / "build-history-ledger.json").read_text()), json.loads(hist.read_text()))
            schema = json.loads((SCRIPTS.parent / "schemas/dashboard.schema.json").read_text())
            validate = runpy.run_path(str(SCRIPTS / "validate-metadata"))["schema_errors"]
            self.assertEqual(validate(data, schema, schema), [])
            update = root / "update.json"
            write_json(update, {"coverage": 0, "checked_count": 0, "expected_count": 0})
            run_tool("generate-dashboard", ["--repo-root", str(root), "--package-inventory", str(inventory), "--update-summary", str(update), "--output-dir", str(root / "zero-preview")], root)
            zero = json.loads((root / "zero-preview/data.json").read_text())
            self.assertTrue(zero["update_health"]["source_available"])
            self.assertEqual(zero["update_health"]["coverage_percent"], 0)

    def test_live_publication_bindings_are_required_and_recomputed(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "published.json"
            document = published_fixture()
            write_json(path, document)
            state, links = GEN["load_published_state"](str(path))
            resolver = GEN["CanonicalPackages"]()
            resolver.add("demo", [])
            result = GEN["history_view"](history([]), resolver, {"demo": {"rpm": {"name": "demo"}}}, {}, {}, {}, links, state)
            self.assertEqual(result["metrics"]["published_packages"], 1)
            self.assertEqual(result["metrics"]["cumulative_success_packages"], 0)
            self.assertTrue(result["packages"][0]["published"])
            self.assertEqual(len(links["demo"]["rpm"]), 1)
            for mutation in ("wrong-generation", "wrong-sha", "wrong-count", "wrong-EVR"):
                damaged = copy.deepcopy(document)
                if mutation == "wrong-generation":
                    damaged["generation_state_url"] = damaged["generation_state_url"].replace("demo-", "other-")
                elif mutation == "wrong-sha":
                    damaged["verified_repomd_sha256"]["source"] = "f" * 64
                elif mutation == "wrong-count":
                    damaged["coverage"]["verified_packages"] = 99
                else:
                    damaged["packages"][0]["versions"][0]["version"] = "2.0"
                write_json(path, damaged)
                with self.assertRaises(GEN["ToolError"]):
                    GEN["load_published_state"](str(path))
            document["coverage"].update(status="partial", source_packages=2, matched_packages=1, gaps=[{"reason": "unmapped-source-name"}])
            write_json(path, document)
            state, links = GEN["load_published_state"](str(path))
            result = GEN["history_view"](history([]), resolver, {}, {}, {}, {}, links, state)
            self.assertIsNone(result["metrics"]["published_packages"])
            self.assertEqual(result["metrics"]["observed_published_packages"], 1)
            orphan = copy.deepcopy(document["verified_artifacts"][0])
            orphan.update(filename="orphan-1.0-1.src.rpm", url=orphan["url"].replace("demo-1.0-1.src.rpm", "orphan-1.0-1.src.rpm"))
            document["verified_artifacts"].append(orphan)
            document["coverage"].update(verified_files=3, verified_bytes=30)
            write_json(path, document)
            _, links = GEN["load_published_state"](str(path))
            self.assertEqual(len(links), 1)
            self.assertEqual(links["demo"]["versions"], [{"epoch": "0", "version": "1.0", "release": "1"}])


if __name__ == "__main__":
    unittest.main()
