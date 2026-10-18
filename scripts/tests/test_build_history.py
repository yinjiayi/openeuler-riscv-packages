# SPDX-License-Identifier: Apache-2.0
import copy
import datetime
import pathlib
import runpy
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[2]
M = runpy.run_path(str(ROOT / "ci/collect-build-history.py"))
H = "a" * 40


class BuildHistoryTests(unittest.TestCase):
    def run_fixture(self):
        return {"id": 42, "head_sha": H, "event": "pull_request"}

    def jobs(self):
        return [{"id": i, "name": name, "head_sha": H, "run_id": 42, "run_attempt": 2,
                 "status": "completed", "conclusion": "success", "labels": ["ubuntu-24.04"],
                 "completed_at": "2026-10-08T00:00:00Z", "steps": [{"name": step, "number": 7,
                 "status": "completed", "conclusion": "success", "completed_at": "2026-10-08T00:00:00Z"}]}
                for i, name, step in [(1, "rpmbuild-riscv64", "Build SRPM and RPM with verified source networking"),
                                       (2, "rpm-install-smoke", "Install RPM and run smoke test")]]

    def test_real_steps_required_not_overall_green(self):
        f = M["successful_jobs"]
        self.assertIsNotNone(f(self.jobs(), self.run_fixture(), 2, "2026-10-09T00:00:00Z"))
        old = self.jobs(); old[0]["steps"][0]["name"] = "Build SRPM and RPM without network"
        self.assertIsNotNone(f(old, self.run_fixture(), 2, "2026-10-09T00:00:00Z"))
        jobs = self.jobs(); jobs[0]["steps"][0]["conclusion"] = "skipped"
        self.assertIsNone(f(jobs, self.run_fixture(), 2, "2026-10-09T00:00:00Z"))
        jobs = self.jobs(); jobs[1]["steps"] = []
        self.assertIsNone(f(jobs, self.run_fixture(), 2, "2026-10-09T00:00:00Z"))

    def test_exact_attempt_and_head_and_cutoff(self):
        f = M["successful_jobs"]
        with self.assertRaisesRegex(ValueError, "attempt"):
            f(self.jobs(), self.run_fixture(), 1, "2026-10-09T00:00:00Z")
        jobs = self.jobs(); jobs[0]["head_sha"] = "b" * 40
        self.assertIsNone(f(jobs, self.run_fixture(), 2, "2026-10-09T00:00:00Z"))
        self.assertIsNone(f(self.jobs(), self.run_fixture(), 2, "2026-10-07T00:00:00Z"))

    def test_forbidden_pr_self_hosted(self):
        jobs = self.jobs(); jobs[0]["labels"].append("self-hosted")
        with self.assertRaisesRegex(ValueError, "self-hosted"):
            M["successful_jobs"](jobs, self.run_fixture(), 2, "2026-10-09T00:00:00Z")

    def test_package_identity_never_title_or_branch(self):
        self.assertEqual(M["canonical_package"](["packages/libperl-x/package.yaml", "packages/libperl-x/tests/smoke.sh"]), "libperl-x")
        for paths in [["ci/tool.py"], ["packages/x/a", "packages/y/b"], ["packages/x/a", "ci/tool.py"]]:
            with self.assertRaises(ValueError):
                M["canonical_package"](paths)

    def test_partition_crosses_1000_without_truncation(self):
        runs = [{"id": i, "path": ".github/workflows/package-ci.yml", "head_sha": H,
                 "created_at": "2026-10-08T00:00:%02dZ" % (i % 60)} for i in range(1, 1201)]
        class Fake:
            def get(self, endpoint):
                query = endpoint.split("created=")[1]
                interval, page = query.split("&page=")
                lo, hi = interval.split("..")
                matches = [r for r in runs if M["timestamp"](lo) <= M["timestamp"](r["created_at"]) <= M["timestamp"](hi)]
                n = int(page); return {"total_count": len(matches), "workflow_runs": matches[(n-1)*100:n*100]}
        found, windows = M["list_runs"](Fake(), M["timestamp"]("2026-10-08T00:00:00Z"), M["timestamp"]("2026-10-08T00:01:00Z"))
        self.assertEqual(len(found), 1200)
        self.assertTrue(all(w["expected"] < 1000 and w["complete"] for w in windows))

    def test_same_second_cap_and_truncated_page_fail(self):
        class Capped:
            def get(self, _): return {"total_count": 1000, "workflow_runs": []}
        with self.assertRaisesRegex(ValueError, "same-second"):
            M["list_runs"](Capped(), M["timestamp"]("2026-10-08T00:00:00Z"), M["timestamp"]("2026-10-08T00:00:01Z"))
        class Truncated:
            def get(self, _): return {"total_count": 1, "workflow_runs": []}
        with self.assertRaisesRegex(ValueError, "count mismatch"):
            M["list_runs"](Truncated(), M["timestamp"]("2026-10-08T00:00:00Z"), M["timestamp"]("2026-10-08T00:00:01Z"))

    def test_dispatch_workflow_main_is_not_candidate(self):
        run = self.run_fixture(); run["event"] = "workflow_dispatch"
        with self.assertRaisesRegex(ValueError, "materialized candidate"):
            M["resolve_recipe"](None, run, None)

    def test_aliases_are_explicit_metadata_not_fuzzy(self):
        result = M["recipe_metadata"]({"rpm": {"name": "perl-Foo"}, "version": {"current": "1", "release": "2"},
            "discovery": {"lineage": [{"package_name": "libfoo-perl", "package_base": "perl-foo"}]},
            "upstream": {"component": "cpan-foo"}}, H)
        self.assertEqual(result["aliases"], ["cpan-foo", "perl-Foo"])
        self.assertEqual(result["ref"], H)

    def test_functional_provider_lineage_is_not_identity(self):
        result = M["recipe_metadata"]({"rpm": {"name": "which"}, "version": {"current": "1", "release": "1"},
            "discovery": {"lineage": [{"package_name": "debianutils", "package_base": "which-git"}]}}, H)
        self.assertNotIn("debianutils", result["aliases"])
        self.assertNotIn("which-git", result["aliases"])

    def seed_fixture(self):
        return {"schema_version": 1, "kind": "package-build-history", "repository": "a/b",
            "generated_at": "2026-10-09T00:00:00Z", "snapshot": {"cutoff": "2026-10-09T00:00:00Z",
             "started_at": "2026-10-09T00:00:00Z", "coverage_complete": False, "lower_bound": True, "reasons": [],
             "listed_run_count": 0, "expected_attempt_count": 0, "processed_attempt_count": 0,
             "unresolved_count": 0, "windows": [], "deleted_history_recoverable": False},
            "observations": [], "attempts": [{"id": "42:1:" + H, "run_id": 42, "run_attempt": 1,
             "head_sha": H, "terminal": True, "status": "not-successful", "api_raw_sha256": ["a"*64]}],
            "summary": {"distinct_package_count": 0, "distinct_recipe_count": 0, "success_tuple_count": 0}, "limitations": []}
    def test_incomplete_or_duplicate_seed_checkpoint_rejected(self):
        seed = self.seed_fixture()
        M["merge_seed"](seed, "a/b")
        bad = copy.deepcopy(seed); del bad["attempts"][0]["api_raw_sha256"]
        with self.assertRaises(Exception): M["merge_seed"](bad, "a/b")
        bad = copy.deepcopy(seed); bad["attempts"].append(copy.deepcopy(bad["attempts"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"): M["merge_seed"](bad, "a/b")

    def test_seed_requires_valid_rfc3339_generated_at(self):
        import jsonschema
        M["validate_seed"](self.seed_fixture(), "a/b")
        for value in ["", "not a time", "2026-10-09", "2026-10-09T00:00:00", "2026-10-09 00:00:00Z"]:
            with self.subTest(value=value):
                bad = self.seed_fixture(); bad["generated_at"] = value
                with self.assertRaises(jsonschema.ValidationError):
                    M["validate_seed"](bad, "a/b")

    def test_seed_rejects_missing_required_format_handler(self):
        import jsonschema
        checker = jsonschema.FormatChecker()
        checker.checkers.pop("date-time", None)
        with patch.object(jsonschema, "FormatChecker", return_value=checker):
            with self.assertRaisesRegex(ValueError, "format handlers unavailable: date-time"):
                M["validate_seed"](self.seed_fixture(), "a/b")

    def test_required_formats_include_nested_and_future_schema_formats(self):
        checker = M["required_format_checker"]({"allOf": [{"properties": {"x": {"format": "date-time"}}}]})
        self.assertIn("date-time", checker.checkers)
        with self.assertRaisesRegex(ValueError, "format handlers unavailable: future-history-format"):
            M["required_format_checker"]({"$defs": {"x": {"format": "future-history-format"}}})
        # A format-less schema does not require unrelated optional plugins.
        M["required_format_checker"]({"type": "object"})

    def test_generated_paths_are_selected_package_specific(self):
        f = M["canonical_package"]
        self.assertEqual(f(["packages/x/a", "catalog/package-index.json", "dashboard/data/index.json", "dashboard/data/packages/x.json"]), "x")
        with self.assertRaises(ValueError): f(["packages/x/a", "dashboard/data/packages/y.json"])

    def test_structured_scope_overlay_candidate_and_workflow_are_separate(self):
        candidate = "b" * 40; tree = "c" * 40
        overlay = {"kind": "protected-main-package-overlay", "schema_version": 1, "status": "passed",
            "package_id": "x", "package_commit_sha": candidate, "package_tree_sha": tree, "tooling_commit_sha": H}
        import json
        text = ('##[group]Run ci/materialize-package-head.py --repo-root . \\\n'
            '  PACKAGE_ID: x\n  PACKAGE_COMMIT_SHA: ' + candidate + '\n  TOOLING_COMMIT_SHA: ' + H +
            '\n##[endgroup]\n' + json.dumps(overlay, separators=(",", ":")) + '\n')
        result = M["scope_log_identity"](text, {"event": "workflow_dispatch", "head_sha": H})
        self.assertEqual(result["head_sha"], candidate)
        with self.assertRaisesRegex(ValueError, "tooling"):
            M["scope_log_identity"](text, {"event": "workflow_dispatch", "head_sha": "d"*40})
        with self.assertRaisesRegex(ValueError, "PR workflow head"):
            M["scope_log_identity"](text, {"event": "pull_request", "head_sha": H})
        with self.assertRaisesRegex(ValueError, "classification"):
            M["scope_log_identity"](text, {"event": "pull_request", "head_sha": candidate})
        self.assertEqual(M["scope_log_identity"](text + 'change scope: package x\n', {"event": "pull_request", "head_sha": candidate})["recipe_tree_sha"], tree)

    def test_published_seed_origin_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "exact normal-HTTPS"):
            M["published_seed"]('https://untrusted.example/build-history-ledger.json', 'a/b', ROOT, None)

    def test_original_configure_scope_requires_exact_head_and_actual_output(self):
        text = ('##[group]Run mkdir -p artifacts/scope\nci/detect-change-scope.py --base "$BASE_SHA" --head "$HEAD_SHA"\n'
            '  BASE_SHA: ' + 'b'*40 + '\n  HEAD_SHA: ' + H + '\n##[endgroup]\nchange scope: package old-x\n')
        result = M["scope_log_identity"](text, {'event': 'pull_request', 'head_sha': H})
        self.assertEqual(result['package_id'], 'old-x')
        self.assertIsNone(result['recipe_tree_sha'])
        for invalid in [text.replace('change scope: package old-x', 'title: package old-x'), text.replace(H, 'c'*40)]:
            with self.assertRaises(ValueError): M["scope_log_identity"](invalid, {'event': 'pull_request', 'head_sha': H})

    def test_dispatch_existing_main_package_requires_independent_whole_tree(self):
        import json
        tree = 'c'*40
        overlay = {'kind':'protected-main-package-overlay','schema_version':1,'status':'passed','package_id':'x',
                   'package_commit_sha':H,'package_tree_sha':tree,'tooling_commit_sha':H}
        text = ('##[group]Run ci/materialize-package-head.py --repo-root .\n  PACKAGE_ID: x\n'
                '  PACKAGE_COMMIT_SHA: '+H+'\n  TOOLING_COMMIT_SHA: '+H+'\n##[endgroup]\n'+json.dumps(overlay,separators=(',',':'))+'\n')
        class API:
            def job_log(self, _): return text
        run = {'id':42,'event':'workflow_dispatch','head_sha':H}
        jobs = [{'id':3,'name':'change-scope','run_id':42,'run_attempt':1,'head_sha':H,'status':'completed','conclusion':'success'}]
        def git(_root,args):
            if args[0]=='show': return json.dumps({'package_id':'x','version':{'current':'1','release':'1'}}).encode()
            if args[0]=='rev-parse': return (tree if args[1].endswith(':packages/x') else 'd'*40).encode()
            raise AssertionError('existing-main dispatch must not require any full-commit delta')
        fn=M['resolve_recipe']
        with patch.dict(fn.__globals__, {'git_read':git}):
            result=fn(API(),run,ROOT,jobs,1)
        self.assertEqual(result['provenance']['identity_method'],'scope-log+exact-package-tree')
        self.assertEqual(result['recipe_tree_sha'],tree)
        def badgit(root,args):
            if args[0]=='rev-parse' and args[1].endswith(':packages/x'):return ('e'*40).encode()
            return git(root,args)
        with patch.dict(fn.__globals__, {'git_read':badgit}), self.assertRaisesRegex(ValueError,'materialized tree'):
            fn(API(),run,ROOT,jobs,1)

    def test_legacy_dispatch_requires_reviewed_contract_actual_checkout_and_selection(self):
        import json
        candidate='b'*40; tree='c'*40; contract=next(iter(M['LEGACY_DISPATCH_WORKFLOWS']))
        text=('##[group]Run actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n'
              '  ref: '+candidate+'\n  repository: a/b\n##[endgroup]\n'
              '[command]/usr/bin/git checkout --progress --force '+candidate+'\n'
              '[command]/usr/bin/git log -1 --format=%H\n'+candidate+'\n'
              '##[group]Run mkdir -p artifacts/scope\nci/select-package-scope.py \\\n'
              '  --package-id "$EXPLICIT_PACKAGE" --head "$HEAD_SHA" \\\n'
              '  HEAD_SHA: '+candidate+'\n  EXPLICIT_PACKAGE: x\n##[endgroup]\n'
              '##[group]Run if [[ "$MODE" = package ]]; then\n'
              'ci/package-policy.py --package-dir "packages/$PACKAGE_ID"\n'
              '  MODE: package\n  PACKAGE_ID: x\n##[endgroup]\n')
        class API:
            repository='a/b'
            def job_log(self,_):return text
        run={'id':42,'event':'workflow_dispatch','head_sha':H}
        jobs=[{'id':3,'name':'change-scope','run_id':42,'run_attempt':1,'head_sha':H,'status':'completed','conclusion':'success'}]
        def git(_root,args):
            if args==['show',H+':.github/workflows/package-ci.yml']:return b'reviewed workflow mock'
            if args[0]=='show':return json.dumps({'package_id':'x','version':{'current':'1','release':'1'}}).encode()
            if args[0]=='rev-parse':return (tree if args[1].endswith(':packages/x') else 'd'*40).encode()
            raise AssertionError('legacy explicit dispatch must not infer package from generic commit delta')
        f=M['legacy_dispatch_identity'];resolver=M['resolve_recipe']
        with patch.dict(f.__globals__, {'git_read':git,'digest':lambda _:contract}):
            self.assertEqual(f(text,run,ROOT,API())['head_sha'],candidate)
            result=resolver(API(),run,ROOT,jobs,1)
            self.assertEqual(result['provenance']['identity_method'],'legacy-workflow-contract+exact-package-tree')
            self.assertEqual(result['provenance']['workflow_contract_sha256'],contract)
            self.assertNotEqual(result['head_sha'],run['head_sha']) # not a current-main run
            for bad in [text.replace('  ref: '+candidate,'  ref: '+H),
                        text.replace('[command]/usr/bin/git log -1 --format=%H\n'+candidate,'[command]/usr/bin/git log -1 --format=%H\n'+H),
                        text.replace('  MODE: package','  MODE: infrastructure'),
                        text.replace('  HEAD_SHA: '+candidate,'  HEAD_SHA: '+H+'\n  HEAD_SHA: '+candidate),
                        text.replace('  EXPLICIT_PACKAGE: x','  EXPLICIT_PACKAGE: y\n  EXPLICIT_PACKAGE: x'),
                        text.replace('  PACKAGE_ID: x','  PACKAGE_ID: y\n  PACKAGE_ID: x'),
                        text.replace('  ref: '+candidate,'  ref: '+H+'\n  ref: '+candidate),
                        text.replace('--force '+candidate,'--force '+candidate+' unverified-tail'),
                        text+text,
                        text.replace('ci/select-package-scope.py','echo title-guessed-package')]:
                with self.assertRaises(ValueError):f(bad,run,ROOT,API())
            with self.assertRaisesRegex(ValueError,'dispatch-only'):f(text,dict(run,event='pull_request'),ROOT,API())
        with patch.dict(f.__globals__, {'git_read':git}), self.assertRaisesRegex(ValueError,'reviewed contract'):
            f(text,run,ROOT,API())


if __name__ == "__main__": unittest.main()
