# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
loader = importlib.machinery.SourceFileLoader("verified_merge", str(ROOT / "scripts/merge-verified-pr"))
spec = importlib.util.spec_from_loader(loader.name, loader)
M = importlib.util.module_from_spec(spec)
loader.exec_module(M)
H, B, C = "a" * 40, "b" * 40, "c" * 40
D = "sha256:" + "d" * 64
NOW = "2026-11-06T00:00:00Z"


class VerifiedMergeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bundle = {"repository": M.REPO, "pr_number": 7, "package_id": "hello",
                       "head_sha": H, "base_sha": B, "run_id": 123, "run_attempt": 1,
                       "archives": [], "review": {"head_sha": H, "base_sha": B, "reviewed_by": "operator"}}
        for topic in M.REVIEW_TOPICS:
            data = f"Observed exact-head evidence for {topic}, including original results.".encode()
            (self.root / f"{topic}.txt").write_bytes(data)
            self.bundle["review"][topic] = {"finding": data.decode(), "path": f"{topic}.txt",
                                           "sha256": hashlib.sha256(data).hexdigest()}
        target = {"os": "openEuler 24.03 LTS SP3", "arch": "riscv64", "isa": "RVA23"}
        self.source = b"official pinned source fixture"
        self.rpm, self.srpm = b"binary RPM fixture", b"source RPM fixture"
        self.raw = {"schema_version": 1, "kind": "build-result", "status": "passed", "phase": "complete",
                    "started_at": NOW, "completed_at": NOW, "exit_code": 0, "target": target,
                    "commit_sha": H, "package_id": "hello", "failure": None, "timed_out": False,
                    "environment": {"observed_arch": "riscv64", "expected_arch": "riscv64", "arch_ok": True,
                                    "os_release": {"ID": "openEuler", "VERSION_ID": "24.03"},
                                    "expected_os": "openEuler 24.03 LTS SP3", "os_ok": True,
                                    "expected_isa": "RVA23", "isa_probe": "passed"},
                    "commands": [["rpmbuild", "-ba", "hello.spec"]],
                    "source_verification": [{"id": "upstream", "filename": "hello.tar.gz", "url": "https://example.org/hello.tar.gz",
                        "sha256": hashlib.sha256(self.source).hexdigest(), "size": len(self.source),
                        "signature": {"policy": "not-provided", "status": "not-required"}, "materialization": {}, "verified": True}],
                    "artifacts": [{"path": f"work/hello/{name}", "kind": kind, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
                                  for name, kind, data in [("hello.rpm", "rpm", self.rpm), ("hello.src.rpm", "srpm", self.srpm)]]}
        self.final = {"schema_version": 1, "job_id": "123:1:package-ci", "package_id": "hello", "commit_sha": H,
                      "status": "passed", "classification": "none", "pr_number": 7, "started_at": NOW, "finished_at": NOW,
                      "environment": {"os": "openEuler", "release": "24.03-LTS-SP3", "arch": "riscv64", "isa": "RVA23",
                          "repo_url": "https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/",
                          "image_digest": D, "qemu_version": "9.2.0"},
                      "checks": {x: {"status": "passed", "evidence": "fixture"} for x in M.REQUIRED - {"configure", "merge-policy"}},
                      "artifacts": ["fixture"]}
        self.smoke = {"schema_version": 1, "package_id": "hello", "phase": "rpm-install-smoke", "status": "passed",
                      "message": "Actual installation and smoke passed", "started_at": NOW, "finished_at": NOW}
        self.source_result = {**copy.deepcopy(self.raw), "status": "source-verified", "phase": "source-verify", "artifacts": []}
        self.manifest = {"schema_version": 1, "package_id": "hello", "sources": [{"id": "upstream", "kind": "upstream-release",
                         "filename": "hello.tar.gz", "url": "https://example.org/hello.tar.gz", "version": "1",
                         "digests": {"sha256": hashlib.sha256(self.source).hexdigest()}, "signature": None,
                         "redistribution": {"allowed": True, "reason": "Test source under public domain license"}}]}
        self.overlays = {phase: {"schema_version": 1, "kind": "protected-main-package-overlay", "status": "passed",
                                "package_id": "hello", "package_commit_sha": H, "tooling_commit_sha": B, "package_tree_sha": C}
                         for phase in ("source", "build", "smoke")}
        self.rules = [{"type": "required_status_checks", "parameters": {"strict_required_status_checks_policy": True,
                       "required_status_checks": [{"context": x, "integration_id": 15368} for x in M.REQUIRED]}},
                      {"type": "pull_request", "parameters": {"allowed_merge_methods": ["squash"]}}]
        self.rule_detail = {"id": 42, "target": "branch", "enforcement": "active", "source_type": "Repository",
                            "source": M.REPO, "bypass_actors": [], "rules": copy.deepcopy(self.rules)}
        self.meta = {}
        self.write_archives()

    def write_archives(self, *, omit_srpm=False, corrupt_source=False):
        self.bundle["archives"] = []
        files = {"source": {"hello.tar.gz": b"corrupt" if corrupt_source else self.source,
                            "source-phase-result.json": json.dumps(self.source_result).encode()},
                 "build": {"rpmbuild-phase-result.json": json.dumps(self.raw).encode(), "hello.rpm": self.rpm,
                           "rpmbuild-internal.log": b"Executing(%check): all original tests passed"},
                 "smoke": {"build-result.json": json.dumps(self.final).encode(), "smoke-phase-result.json": json.dumps(self.smoke).encode(),
                           "smoke.log": b"DNF installation and installed package smoke passed"},
                 "repository": {"resolution.json": b'{"snapshot":"fixture"}'}}
        for phase, overlay in self.overlays.items():
            files[phase]["tooling-overlay.json"] = json.dumps(overlay).encode()
        if not omit_srpm:
            files["build"]["hello.src.rpm"] = self.srpm
        for artifact_id, (phase, content) in enumerate(files.items(), 1):
            path = self.root / f"{phase}.zip"
            with zipfile.ZipFile(path, "w") as archive:
                for name, data in content.items():
                    archive.writestr(name, data)
            self.bundle["archives"].append({"artifact_id": artifact_id, "path": path.name})
            self.meta[artifact_id] = {"expired": False, "workflow_run": {"id": 123}, "name": f"package-ci-{phase}-hello-123",
                                      "digest": "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(), "size_in_bytes": path.stat().st_size}

    def proof(self):
        def git(argv):
            if argv[-1] == f"{B}:ci/image.lock":
                return f"digest: {D}\n"
            if argv[-1] == f"{H}:packages/hello":
                return C
            if argv[-1] == f"{H}:packages/hello/sources.yaml":
                return json.dumps(self.manifest)
            raise AssertionError(argv)
        with patch.object(M, "api", side_effect=lambda p: self.meta[int(p.rsplit("/", 1)[1])]), \
             patch.object(M, "command", side_effect=git):
            return M.evidence(self.bundle, self.root)

    def test_actual_products_and_sources_are_hashed(self):
        result = self.proof()
        self.assertEqual({x["kind"] for x in result["physical_products"]}, {"rpm", "srpm"})
        self.assertEqual(result["source_count"], 1)

    def test_missing_srpm_rejected(self):
        self.write_archives(omit_srpm=True)
        with self.assertRaisesRegex(ValueError, "missing or ambiguous"):
            self.proof()

    def test_corrupt_source_rejected_even_with_valid_zip_digest(self):
        self.write_archives(corrupt_source=True)
        with self.assertRaisesRegex(ValueError, "source bytes differ"):
            self.proof()

    def test_expired_or_wrong_digest_archive_rejected(self):
        for field, value in [("expired", True), ("digest", "sha256:" + "0" * 64)]:
            with self.subTest(field=field):
                old = self.meta[1][field]
                self.meta[1][field] = value
                with self.assertRaises(ValueError):
                    self.proof()
                self.meta[1][field] = old

    def test_schema_invalid_and_old_attempt_rejected(self):
        self.final["job_id"] = "123:2:package-ci"
        self.write_archives()
        with self.assertRaisesRegex(ValueError, "attempt mismatch"):
            self.proof()
        self.final.pop("environment")
        self.write_archives()
        with self.assertRaisesRegex(ValueError, "schema-invalid"):
            self.proof()

    def test_skipped_build_is_not_success(self):
        self.final["checks"]["rpmbuild-riscv64"]["status"] = "skipped"
        self.write_archives()
        with self.assertRaisesRegex(ValueError, "not all final checks"):
            self.proof()

    def test_changed_review_or_external_path_rejected(self):
        self.bundle["review"]["base_sha"] = C
        with self.assertRaisesRegex(ValueError, "stale"):
            self.proof()
        self.bundle["review"]["base_sha"] = B
        self.bundle["review"]["source_license"]["path"] = "../outside"
        with self.assertRaisesRegex(ValueError, "outside"):
            self.proof()

    def test_wrong_raw_role_environment_or_package_rejected(self):
        original = copy.deepcopy(self.raw)
        cases = [("phase", "source-verify"), ("package_id", "different"), ("timed_out", True),
                 ("environment", {**self.raw["environment"], "arch_ok": False}),
                 ("environment", {**self.raw["environment"], "os_ok": False}),
                 ("environment", {**self.raw["environment"], "observed_arch": "x86_64"}), ("commands", [])]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                self.raw = {**copy.deepcopy(original), field: value}
                self.write_archives()
                with self.assertRaises(ValueError):
                    self.proof()
        self.raw = copy.deepcopy(original)
        self.raw.pop("environment")
        self.write_archives()
        with self.assertRaisesRegex(ValueError, "target environment"):
            self.proof()

    def test_schema_valid_wrong_smoke_role_rejected(self):
        self.smoke = copy.deepcopy(self.raw)
        self.write_archives()
        with self.assertRaisesRegex(ValueError, "smoke role"):
            self.proof()

    def test_source_bytes_must_match_exact_head_pin(self):
        self.manifest["sources"][0]["digests"]["sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "exact-head pin"):
            self.proof()

    def test_source_set_and_both_phase_receipts_are_bound(self):
        self.raw["source_verification"] = []
        self.write_archives()
        with self.assertRaisesRegex(ValueError, "source set"):
            self.proof()
        self.raw["source_verification"] = copy.deepcopy(self.source_result["source_verification"])
        self.source_result["source_verification"][0]["url"] = "https://example.org/other.tar.gz"
        self.write_archives()
        with self.assertRaisesRegex(ValueError, "exact-head pin"):
            self.proof()

    def test_required_signature_cannot_be_downgraded(self):
        self.manifest["sources"][0]["signature"] = {"policy": "required", "url": "https://example.org/hello.sig",
                                                   "path": "hello.sig", "keyring": "keys.gpg", "key_fingerprint": "F" * 40}
        with self.assertRaisesRegex(ValueError, "signature policy"):
            self.proof()
        for receipt in (self.raw, self.source_result):
            receipt["source_verification"][0]["signature"]["policy"] = "required"
        self.write_archives()
        with self.assertRaisesRegex(ValueError, "signature not verified"):
            self.proof()

    def test_every_phase_overlay_binds_protected_base_and_exact_tree(self):
        original = copy.deepcopy(self.overlays)
        for phase in ("source", "build", "smoke"):
            for key in ("tooling_commit_sha", "package_commit_sha", "package_tree_sha"):
                with self.subTest(phase=phase, key=key):
                    self.overlays = copy.deepcopy(original)
                    self.overlays[phase][key] = "f" * 40
                    self.write_archives()
                    with self.assertRaisesRegex(ValueError, "overlay differs"):
                        self.proof()

    def live_api(self, path, *args):
        base = f"repos/{M.REPO}"
        responses = {
            base: {"default_branch": "main", "allow_auto_merge": False, "allow_squash_merge": True, "permissions": {"push": True}},
            base + "/branches/main": {"protected": True, "commit": {"sha": B}},
            base + "/pulls/7": {"state": "open", "merged": False, "draft": False, "auto_merge": None,
                "mergeable": True, "mergeable_state": "clean", "changed_files": 1, "labels": [],
                "head": {"sha": H, "repo": {"full_name": M.REPO}}, "base": {"sha": B, "ref": "main", "repo": {"full_name": M.REPO}}},
            base + f"/compare/{B}...{H}": {"merge_base_commit": {"sha": B}},
            base + "/rulesets/42?includes_parents=true": self.rule_detail,
            base + "/actions/runs/123": {"id": 123, "run_attempt": 1, "head_sha": H, "path": ".github/workflows/package-ci.yml",
                "event": "pull_request", "status": "completed", "conclusion": "success", "repository": {"full_name": M.REPO},
                "head_repository": {"full_name": M.REPO}, "pull_requests": [{"number": 7, "head": {"sha": H}, "base": {"sha": B}}]},
        }
        return responses[path]

    def live_pages(self, path, key=None):
        if path.endswith("/rules/branches/main"):
            return [{**x, "ruleset_id": 42, "ruleset_source_type": "Repository", "ruleset_source": M.REPO} for x in self.rules]
        if "/rulesets?" in path:
            return [{"id": 42, "enforcement": "active", "source_type": "Repository", "source": M.REPO}]
        if path.endswith("/files"):
            return [{"filename": "packages/hello/hello.spec"}]
        if "/check-runs" in path:
            return [{"name": x, "app": {"id": 15368}, "head_sha": H, "status": "completed", "conclusion": "success"} for x in M.REQUIRED]
        if path.endswith("/jobs"):
            return [{"name": x, "status": "completed", "conclusion": "success"} for x in M.REQUIRED - {"configure"}]
        return []

    def test_live_full_gate(self):
        with patch.object(M, "api", side_effect=self.live_api), patch.object(M, "pages", side_effect=self.live_pages):
            self.assertEqual(M.live(self.bundle)["head_sha"], H)

    def test_every_canonical_hold_blocks_even_after_green_checks(self):
        required = {"needs-human", "needs-native-riscv", "repair-queued", "codex-repairing", "do-not-merge",
                    "source-blocked", "license-blocked", "checksum-blocked", "security-blocked", "tests-disabled", "qemu-limitation"}
        self.assertTrue(required <= M.BLOCKING_LABELS)
        for label in M.BLOCKING_LABELS:
            with self.subTest(label=label):
                def blocked(path, *args):
                    result = self.live_api(path, *args)
                    if path.endswith("/pulls/7"):
                        result["labels"] = [{"name": label}]
                    return result
                with patch.object(M, "api", side_effect=blocked), patch.object(M, "pages", side_effect=self.live_pages):
                    with self.assertRaisesRegex(ValueError, "blocking label"):
                        M.live(self.bundle)

    def test_missing_label_visibility_is_not_empty_labels(self):
        def invisible(path, *args):
            result = self.live_api(path, *args)
            if path.endswith("/pulls/7"):
                result.pop("labels")
            return result
        with patch.object(M, "api", side_effect=invisible), patch.object(M, "pages", side_effect=self.live_pages):
            with self.assertRaisesRegex(ValueError, "labels unavailable"):
                M.live(self.bundle)

    def test_changed_main_and_missing_required_check_rejected(self):
        def changed(path, *args):
            result = self.live_api(path, *args)
            if path.endswith("/branches/main"):
                result["commit"]["sha"] = C
            return result
        with patch.object(M, "api", side_effect=changed), patch.object(M, "pages", side_effect=self.live_pages):
            with self.assertRaisesRegex(ValueError, "main changed"):
                M.live(self.bundle)
        def missing(path, key=None):
            values = self.live_pages(path, key)
            return values[:-1] if "/check-runs" in path else values
        with patch.object(M, "api", side_effect=self.live_api), patch.object(M, "pages", side_effect=missing):
            with self.assertRaisesRegex(ValueError, "required check"):
                M.live(self.bundle)

    def test_bypass_actors_must_be_visible_and_empty(self):
        for value in (None, {}, [{"actor_type": "RepositoryRole", "actor_id": 5}]):
            with self.subTest(value=value):
                self.rule_detail["bypass_actors"] = value
                with patch.object(M, "api", side_effect=self.live_api), patch.object(M, "pages", side_effect=self.live_pages):
                    with self.assertRaisesRegex(ValueError, "bypass actors"):
                        M.live(self.bundle)
        self.rule_detail.pop("bypass_actors")
        with patch.object(M, "api", side_effect=self.live_api), patch.object(M, "pages", side_effect=self.live_pages):
            with self.assertRaisesRegex(ValueError, "bypass actors"):
                M.live(self.bundle)

    def test_ruleset_source_and_detail_cannot_change(self):
        self.rule_detail["rules"][0]["parameters"]["strict_required_status_checks_policy"] = False
        with patch.object(M, "api", side_effect=self.live_api), patch.object(M, "pages", side_effect=self.live_pages):
            with self.assertRaisesRegex(ValueError, "differs from ruleset"):
                M.live(self.bundle)
        self.rule_detail["rules"] = copy.deepcopy(self.rules)
        self.rules[1]["parameters"]["allowed_merge_methods"] = ["merge", "squash"]
        self.rule_detail["rules"] = copy.deepcopy(self.rules)
        with patch.object(M, "api", side_effect=self.live_api), patch.object(M, "pages", side_effect=self.live_pages):
            with self.assertRaisesRegex(ValueError, "squash-only"):
                M.live(self.bundle)

    def test_output_cannot_replace_bundle_archive_review_or_hardlink(self):
        path = self.root / "bundle.json"
        path.write_text(json.dumps(self.bundle))
        alias = self.root / "alias.json"
        os.link(path, alias)
        outputs = [path, self.root / "source.zip", self.root / "source_license.txt", alias]
        for output in outputs:
            with self.subTest(output=output), patch.object(M, "live") as live, patch.object(M, "api") as api:
                with self.assertRaisesRegex(ValueError, "overwrite input"):
                    M.execute(types.SimpleNamespace(bundle=str(path), output=str(output), apply=True))
                live.assert_not_called()
                api.assert_not_called()

    def test_effective_rules_require_complete_parent_listing(self):
        def incomplete(path, key=None):
            return [] if "/rulesets?" in path else self.live_pages(path, key)
        with patch.object(M, "api", side_effect=self.live_api), patch.object(M, "pages", side_effect=incomplete):
            with self.assertRaisesRegex(ValueError, "listing changed"):
                M.live(self.bundle)

    def test_rules_and_rulesets_are_both_paginated(self):
        called = []
        def paginated_api(path):
            called.append(path)
            page = int(path.rsplit("=", 1)[1])
            return [{"id": n} for n in range(100)] if page == 1 else [{"id": 100}]
        for endpoint in (f"repos/{M.REPO}/rules/branches/main", f"repos/{M.REPO}/rulesets?includes_parents=true"):
            with patch.object(M, "api", side_effect=paginated_api):
                self.assertEqual(len(M.pages(endpoint)), 101)
            self.assertEqual(called[-2:], [endpoint + ("&" if "?" in endpoint else "?") + f"per_page=100&page={n}" for n in (1, 2)])

    def test_unsupported_run_event_remains_refused(self):
        def dispatched(path, *args):
            result = self.live_api(path, *args)
            if path.endswith("/actions/runs/123"):
                result["event"] = "workflow_dispatch"
            return result
        with patch.object(M, "api", side_effect=dispatched), patch.object(M, "pages", side_effect=self.live_pages):
            with self.assertRaisesRegex(ValueError, "unsupported build provenance"):
                M.live(self.bundle)

    def test_final_lease_change_never_reaches_merge(self):
        path = self.root / "bundle.json"
        path.write_text(json.dumps(self.bundle))
        with patch.object(M, "live", side_effect=[{"head_sha": H}, {"head_sha": H}, {"head_sha": C}]), \
             patch.object(M, "evidence", return_value={}), patch.object(M, "command") as command, \
             patch.object(M, "api", return_value={"login": "operator"}) as api:
            with self.assertRaisesRegex(ValueError, "final remote lease"):
                M.execute(types.SimpleNamespace(bundle=str(path), output=str(self.root / "out.json"), apply=True))
            self.assertEqual(api.call_args_list, [unittest.mock.call("user")])
            self.assertEqual(Path(command.call_args.args[0][0]).name, "github-credential-guard")

    def test_failed_live_recheck_replaces_old_success_receipt(self):
        path = self.root / "bundle.json"
        path.write_text(json.dumps(self.bundle))
        output = self.root / "out.json"
        output.write_text(json.dumps({"kind": "package-merge-admission", "status": "verified-not-merged"}))
        with patch.object(M, "live", side_effect=ValueError("protected main changed")), patch.object(M, "api") as api:
            with self.assertRaisesRegex(ValueError, "protected main changed"):
                M.execute(types.SimpleNamespace(bundle=str(path), output=str(output), apply=True))
            api.assert_not_called()
        receipt = json.loads(output.read_text())
        self.assertEqual(receipt["status"], "refused")
        self.assertNotIn("verified_at", receipt)
        self.assertEqual(receipt["reason"], "protected main changed")

    def test_merge_put_timeout_is_uncertain_not_unmerged(self):
        path = self.root / "bundle.json"
        path.write_text(json.dumps(self.bundle))
        output = self.root / "out.json"
        calls = []
        def uncertain(path, *args):
            calls.append((path, args))
            if path == "user":
                return {"login": "operator"}
            if path.endswith("/merge"):
                self.assertEqual(json.loads(output.read_text())["status"], "merge-request-in-flight")
                raise M.subprocess.TimeoutExpired(["gh", "api"], 180)
            raise AssertionError(path)
        with patch.object(M, "live", return_value={"head_sha": H}), patch.object(M, "evidence", return_value={}), \
             patch.object(M, "command"), patch.object(M, "api", side_effect=uncertain):
            with self.assertRaises(M.subprocess.TimeoutExpired):
                M.execute(types.SimpleNamespace(bundle=str(path), output=str(output), apply=True))
        self.assertEqual(len([call for call in calls if "PUT" in call[1]]), 1)
        receipt = json.loads(output.read_text())
        self.assertEqual(receipt["status"], "needs-reconcile")
        self.assertNotIn("merge_sha", receipt)

    def test_readback_mismatch_leaves_explicit_reconciliation_receipt(self):
        path = self.root / "bundle.json"
        path.write_text(json.dumps(self.bundle))
        calls = []
        def merge_api(path, *args):
            calls.append((path, args))
            if path == "user":
                return {"login": "operator"}
            if path.endswith("/merge"):
                return {"merged": True, "sha": C}
            if path.endswith("/pulls/7"):
                return {"merged": True, "merge_commit_sha": C}
            if "/git/commits/" in path:
                return {"parents": [{"sha": B}]}
            if path.endswith("/git/ref/heads/main"):
                return {"object": {"sha": H}}
            raise AssertionError(path)
        with patch.object(M, "live", return_value={"head_sha": H}), patch.object(M, "evidence", return_value={}), \
             patch.object(M, "command"), patch.object(M, "api", side_effect=merge_api):
            with self.assertRaisesRegex(ValueError, "reconcile before next merge"):
                M.execute(types.SimpleNamespace(bundle=str(path), output=str(self.root / "out.json"), apply=True))
        mutation = [(p, a) for p, a in calls if "PUT" in a]
        self.assertEqual(len(mutation), 1)
        self.assertEqual(mutation[0][1], ("--method", "PUT", "-f", "merge_method=squash", "-f", f"sha={H}"))
        self.assertEqual(json.loads((self.root / "out.json").read_text())["status"], "merged-readback-pending")

    def test_failed_evidence_cannot_reach_merge(self):
        path = self.root / "bundle.json"
        path.write_text(json.dumps(self.bundle))
        with patch.object(M, "live", return_value={"head_sha": H}), \
             patch.object(M, "evidence", side_effect=ValueError("missing RPM")), patch.object(M, "api") as api:
            with self.assertRaisesRegex(ValueError, "missing RPM"):
                M.execute(types.SimpleNamespace(bundle=str(path), output=str(self.root / "out.json"), apply=True))
            api.assert_not_called()

    def test_dry_run_never_mutates(self):
        path = self.root / "bundle.json"
        path.write_text(json.dumps(self.bundle))
        with patch.object(M, "live", return_value={"head_sha": H}), patch.object(M, "evidence", return_value={}), patch.object(M, "api") as api:
            M.execute(types.SimpleNamespace(bundle=str(path), output=str(self.root / "out.json"), apply=False))
            api.assert_not_called()
            self.assertEqual(json.loads((self.root / "out.json").read_text())["status"], "verified-not-merged")


if __name__ == "__main__":
    unittest.main()
