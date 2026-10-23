# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import hashlib
import json
import pathlib
import runpy
import tempfile
import unittest
from typing import Optional

from helpers import SCRIPTS, run_tool, write_json


def package(
    root: pathlib.Path,
    package_id: str,
    release_api: str,
    version: str = "1.0",
    release_regex: Optional[str] = None,
    source_url_template: Optional[str] = None,
) -> None:
    directory = root / "packages" / package_id
    directory.mkdir(parents=True)
    write_json(
        directory / "package.yaml",
        {
            "schema_version": "1.0",
            "package_id": package_id,
            "rpm_name": package_id,
            "summary": package_id,
            "description": package_id,
            "license": "MIT",
            "version": version,
            "release_channel": "stable",
            "upstream": {
                "homepage": "https://example.org/%s" % package_id,
                "release_api": release_api,
                "release_regex": release_regex,
                "source_url_template": source_url_template,
            },
            "target": {"os": "openEuler 24.03 LTS SP3", "arch": "riscv64", "isa": "RVA23"},
            "riscv": {"status": "unknown", "needs_native": False},
            "packaging": {"spec": "%s.spec" % package_id, "patch_series": "patches/series", "smoke_test": "tests/smoke.sh", "patches": []},
            "maintenance": {"status": "active", "update_disabled": False},
        },
    )
    write_json(directory / "sources.yaml", {"schema_version": "1.0", "package_id": package_id, "sources": [{"id": "source0", "version": version, "url": "https://example.org/%s-%s.tar.gz" % (package_id, version), "filename": "%s-%s.tar.gz" % (package_id, version), "sha256": "0" * 64}]})
    (directory / ("%s.spec" % package_id)).write_text("Name: %s\nVersion:        %s\nRelease: 2%%{?dist}\nSource0:        %s-%s.tar.gz\n%%prep\n%%build\n%%install\n%%check\n%%files\n%%changelog\n" % (package_id, version, package_id, version), encoding="utf-8")
    (directory / "patches").mkdir()
    (directory / "patches" / "series").write_text("", encoding="utf-8")
    (directory / "tests").mkdir()
    (directory / "tests" / "smoke.sh").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")


class PackageUpdateTests(unittest.TestCase):
    def test_compact_prerelease_feed_keeps_current_final_release(self) -> None:
        # Minimal official PyPI shape from the case-converter failure: release
        # values are file lists. No file/source-selection behavior is changed.
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            releases = root / "releases.json"
            write_json(releases, {"releases": {
                "1.2.0": [], "1.2.0rc1": [], "1.2.0a1": [],
                "1.2.0b1": [], "1.2.0alpha1": [], "1.2.0beta1": [],
            }})
            package(root, "demo", str(releases), version="1.2.0")
            plan = root / "plan.json"
            run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"),
                     "--output", str(plan), "--now", "2026-08-08T00:00:00Z"], root)
            shard = root / "shard.json"
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0",
                     "--output", str(shard), "--now", "2026-08-08T00:01:00Z"], root)
            entry = json.loads(shard.read_text())["entries"][0]
            self.assertEqual(entry["status"], "no-update")
            self.assertEqual(entry["latest_version"], "1.2.0")

    def test_compact_prerelease_filter_preserves_stable_versions_and_flags(self) -> None:
        is_prerelease = runpy.run_path(str(SCRIPTS / "_lib.py"))["is_prerelease"]
        for version in ("1.2.0rc1", "v1.2.0RC2", "1.2.0a1", "1.2.0b1",
                        "1.2.0alpha1", "1.2.0beta1", "1.2.0pre1", "1.2.0preview1",
                        "1.2.0dev1", "1.2.0rc1+build.7", "1.2.0-rc1", "1.2.0.dev1"):
            with self.subTest(prerelease=version):
                self.assertTrue(is_prerelease({"version": version}))
        for version in ("1.2.0", "v1.2.0", "1.2.0.post1", "1.2.0post1", "1.0.2a",
                        "1.2.0+build.7", "1.2.0+build1rc1", "1.2.0+rc1"):
            with self.subTest(stable=version):
                self.assertFalse(is_prerelease({"version": version}))
        self.assertTrue(is_prerelease({"version": "1.2.0", "draft": True}))
        self.assertTrue(is_prerelease({"version": "1.2.0", "prerelease": True}))

    def test_create_package_and_update_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            candidate = root / "candidate.json"
            write_json(candidate, {"component_id": "example-hello", "package_id": "hello", "canonical_name": "hello", "summary": "hello", "description": "hello", "license": "GPL-3.0-or-later", "latest_observed_version": "1.0", "upstream": {"homepage": "https://example.org/hello", "repository_url": "https://example.org/hello.git", "release_api": "https://example.org/releases.json"}, "source": {"url": "https://example.org/hello-1.0.tar.gz", "sha256": "1" * 64}, "lineage": [], "resolution_evidence": [{"type": "official-release-source"}]})
            created = root / "created.json"
            run_tool("create-package", ["--candidate", str(candidate), "--packages-dir", str(root / "created-packages"), "--output", str(created)], root)
            self.assertTrue((root / "created-packages" / "hello" / "hello.spec").is_file())
            self.assertEqual(json.loads(created.read_text())["operation"], "onboard")

            source = root / "upstream-2.tar.gz"
            source.write_bytes(b"stable release 2")
            checksum = hashlib.sha256(source.read_bytes()).hexdigest()
            releases = root / "releases.json"
            write_json(releases, [{"version": "1.0", "source_url": source.as_uri(), "sha256": "0" * 64}, {"version": "2.0", "source_url": source.as_uri(), "sha256": checksum}, {"version": "3.0-rc1", "source_url": source.as_uri(), "sha256": checksum}])
            package(root, "demo", str(releases))
            plan = root / "plan.json"
            run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"), "--output", str(plan), "--shard-size", "1", "--now", "2026-08-08T00:00:00Z"], root)
            self.assertEqual(json.loads(plan.read_text())["eligible_count"], 1)
            shard = root / "shard.json"
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard), "--now", "2026-08-08T00:01:00Z"], root)
            entry = json.loads(shard.read_text())["entries"][0]
            self.assertEqual(entry["status"], "update-available")
            self.assertEqual(entry["version"], "2.0")
            aggregate = root / "aggregate.json"
            state = root / "state.json"
            run_tool("check-update", ["aggregate", "--plan", str(plan), "--result", str(shard), "--output", str(aggregate), "--state-output", str(state), "--now", "2026-08-08T00:02:00Z"], root)
            self.assertTrue(json.loads(aggregate.read_text())["complete"])
            applied = root / "applied.json"
            run_tool("check-update", ["apply", "--result", str(aggregate), "--package", "demo", "--packages-dir", str(root / "packages"), "--output", str(applied)], root)
            self.assertEqual(json.loads((root / "packages" / "demo" / "package.yaml").read_text())["version"], "2.0")
            self.assertIn("Source0:        upstream-2.tar.gz", (root / "packages" / "demo" / "demo.spec").read_text())
            self.assertEqual(json.loads(applied.read_text())["idempotency_key"], "update:demo:2.0")

    def test_duplicate_version_is_suppressed_and_missing_shard_is_visible(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            releases = root / "releases.json"
            write_json(releases, [{"version": "2.0", "source_url": "https://example.org/demo-2.tar.gz", "sha256": "2" * 64}])
            package(root, "a", str(releases))
            package(root, "b", str(releases))
            state = root / "state.json"
            write_json(state, {"open_updates": {"a": ["2.0"]}})
            plan = root / "plan.json"
            run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"), "--state", str(state), "--output", str(plan), "--shard-size", "1", "--now", "2026-08-08T00:00:00Z"], root)
            shard = root / "shard0.json"
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard), "--no-source-digest", "--now", "2026-08-08T00:01:00Z"], root)
            self.assertEqual(json.loads(shard.read_text())["entries"][0]["status"], "duplicate-suppressed")
            aggregate = root / "aggregate.json"
            run_tool("check-update", ["aggregate", "--plan", str(plan), "--result", str(shard), "--output", str(aggregate), "--now", "2026-08-08T00:02:00Z"], root)
            result = json.loads(aggregate.read_text())
            self.assertFalse(result["complete"])
            self.assertEqual(result["failed_shards"], [1])
            self.assertEqual(result["pending_backfill_count"], 1)

    def test_empty_plan_aggregates_without_synthetic_shards(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            packages = root / "packages"
            packages.mkdir()
            plan = root / "plan.json"
            run_tool(
                "check-update",
                [
                    "plan",
                    "--packages-dir",
                    str(packages),
                    "--output",
                    str(plan),
                    "--now",
                    "2026-08-08T00:00:00Z",
                ],
                root,
            )
            self.assertEqual(json.loads(plan.read_text())["expected_shards"], [])
            aggregate = root / "aggregate.json"
            state = root / "state.json"
            run_tool(
                "check-update",
                [
                    "aggregate",
                    "--plan",
                    str(plan),
                    "--output",
                    str(aggregate),
                    "--state-output",
                    str(state),
                    "--now",
                    "2026-08-08T00:01:00Z",
                ],
                root,
            )
            result = json.loads(aggregate.read_text())
            self.assertTrue(result["complete"])
            self.assertEqual(result["expected_count"], 0)
            self.assertEqual(result["checked_count"], 0)
            self.assertEqual(result["coverage"], 1.0)
            self.assertEqual(result["failed_shards"], [])
            self.assertEqual(json.loads(state.read_text())["consecutive_incomplete_runs"], 0)

    def test_html_release_index_uses_reviewed_regex_and_source_template(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            archive = root / "demo-2.0.tar.gz"
            archive.write_bytes(b"official stable archive")
            index = root / "releases.html"
            index.write_text(
                '<a href="demo-1.0.tar.gz">demo-1.0.tar.gz</a>'
                '<a href="demo-2.0.tar.gz">demo-2.0.tar.gz</a>'
                '<a href="demo-3.0-rc1.tar.gz">demo-3.0-rc1.tar.gz</a>',
                encoding="utf-8",
            )
            package(
                root,
                "demo",
                index.as_uri(),
                release_regex=r"demo-([0-9]+(?:\.[0-9]+)+(?:-rc[0-9]+)?)\.tar\.gz",
                source_url_template=root.as_uri() + "/demo-{version}.tar.gz",
            )
            plan = root / "plan.json"
            run_tool(
                "check-update",
                ["plan", "--packages-dir", str(root / "packages"), "--output", str(plan), "--now", "2026-08-08T00:00:00Z"],
                root,
            )
            shard = root / "shard.json"
            run_tool(
                "check-update",
                ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard), "--now", "2026-08-08T00:01:00Z"],
                root,
            )
            entry = json.loads(shard.read_text())["entries"][0]
            self.assertEqual(entry["status"], "update-available")
            self.assertEqual(entry["version"], "2.0")
            self.assertEqual(entry["source_url"], archive.as_uri())
            self.assertEqual(entry["sha256"], hashlib.sha256(archive.read_bytes()).hexdigest())

    def test_anchored_html_filename_keeps_reviewed_source_and_digest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            archive = root / "demo-2.0.tar.gz"
            archive.write_bytes(b"reviewed stable source, not the linked binary")
            index = root / "index.html"
            index.write_text(
                '<html><a href="https://untrusted.invalid/binaries/demo-%32.0.tar.gz?download=1&amp;mode=binary">download</a>'
                '<a href="demo-2.0.tar.gz">duplicate</a>'
                '<a href="demo-9.0-rc1.tar.gz">prerelease</a>'
                '<a href="other-99.0.tar.gz">unrelated</a></html>', encoding="utf-8",
            )
            package(root, "demo", index.as_uri(), release_regex=r"^demo-(?P<version>[0-9]+\.[0-9]+)\.tar\.gz$", source_url_template=root.as_uri() + "/demo-{version}.tar.gz")
            plan, shard = root / "plan.json", root / "shard.json"
            run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"), "--output", str(plan)], root)
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard)], root)
            entry = json.loads(shard.read_bytes())["entries"][0]
            self.assertEqual(entry["status"], "update-available")
            self.assertEqual(entry["version"], "2.0")
            self.assertEqual(entry["source_url"], archive.as_uri())
            self.assertEqual(entry["sha256"], hashlib.sha256(archive.read_bytes()).hexdigest())

    def test_anchored_html_without_source_contract_still_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            index = root / "index.html"
            index.write_text('<a href="https://untrusted.invalid/demo-2.0.tar.gz">download</a>', encoding="utf-8")
            package(root, "demo", index.as_uri(), release_regex=r"^demo-([0-9]+\.[0-9]+)\.tar\.gz$")
            plan, shard = root / "plan.json", root / "shard.json"
            run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"), "--output", str(plan)], root)
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard)], root)
            entry = json.loads(shard.read_bytes())["entries"][0]
            self.assertEqual(entry["status"], "failed")
            self.assertIn("no stable releases", entry["failure"]["message"])

    def test_html_identity_adapter_keeps_prerelease_suffix_visible(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            index = root / "index.html"
            # The selector intentionally captures only the numeric prefix.
            index.write_text('<a href="demo-9.0-rc1.tar.gz">download</a>', encoding="utf-8")
            package(root, "demo", index.as_uri(), release_regex=r"^demo-([0-9]+\.[0-9]+)", source_url_template=root.as_uri() + "/demo-{version}.tar.gz")
            plan, shard = root / "plan.json", root / "shard.json"
            run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"), "--output", str(plan)], root)
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard)], root)
            entry = json.loads(shard.read_bytes())["entries"][0]
            self.assertEqual(entry["status"], "failed")
            self.assertIn("no stable releases", entry["failure"]["message"])

    def test_anchored_json_tag_regex_keeps_official_source_and_digest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            archive = root / "demo-2.0.tar.gz"
            archive.write_bytes(b"official stable JSON tag archive")
            releases = root / "tags.json"
            write_json(releases, [{"name": "v2.0"}, {"name": "v3.0-rc1"}, {"name": "other-project-99.0"}])
            package(root, "demo", releases.as_uri(), release_regex=r"^v?(?P<version>[0-9]+(?:\.[0-9]+)+)$", source_url_template=root.as_uri() + "/demo-{version}.tar.gz")
            plan = root / "plan.json"
            shard = root / "shard.json"
            run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"), "--output", str(plan)], root)
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard)], root)
            entry = json.loads(shard.read_text())["entries"][0]
            self.assertEqual(entry["status"], "update-available")
            self.assertEqual(entry["version"], "2.0")
            self.assertEqual(entry["tag"], "v2.0")
            self.assertEqual(entry["source_url"], archive.as_uri())
            self.assertEqual(entry["sha256"], hashlib.sha256(archive.read_bytes()).hexdigest())

    def test_json_release_regex_preserves_draft_prerelease_and_asset_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            archive = root / "reviewed-source.tar.gz"
            archive.write_bytes(b"stable source asset")
            checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
            releases = root / "releases.json"
            write_json(releases, [
                {"tag_name": "v2.0", "name": "Stable release", "source_url": archive.as_uri(), "sha256": checksum, "assets": [{"name": "demo-2.0.tar.gz", "browser_download_url": archive.as_uri()}]},
                {"tag_name": "v9.0", "draft": True},
                {"tag_name": "v8.0", "prerelease": True},
            ])
            package(root, "demo", releases.as_uri(), release_regex=r"^v?(?P<version>[0-9]+(?:\.[0-9]+)+)$", source_url_template=archive.as_uri())
            plan = root / "plan.json"
            shard = root / "shard.json"
            run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"), "--output", str(plan)], root)
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard)], root)
            entry = json.loads(shard.read_text())["entries"][0]
            self.assertEqual(entry["status"], "update-available")
            self.assertEqual(entry["version"], "2.0")
            self.assertEqual(entry["tag"], "v2.0")
            self.assertEqual(entry["source_url"], archive.as_uri())
            self.assertEqual(entry["sha256"], hashlib.sha256(archive.read_bytes()).hexdigest())

            # Without digest fetching, the upstream checksum must still survive
            # the identity-regex adapter rather than being recomputed locally.
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard), "--no-source-digest"], root)
            preserved = json.loads(shard.read_text())["entries"][0]
            self.assertEqual(preserved["sha256"], checksum)

    def test_json_regex_mismatch_and_invalid_json_remain_visible_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            mismatch = root / "mismatch.json"
            malformed = root / "malformed.json"
            write_json(mismatch, [{"name": "unrelated-2.0"}, {"name": "v3.0-rc1"}])
            malformed.write_text('[{"tag_name": "v2.0"}', encoding="utf-8")
            for identifier, feed in (("mismatch", mismatch), ("malformed", malformed)):
                package(root, identifier, feed.as_uri(), release_regex=r"^v?(?P<version>[0-9]+(?:\.[0-9]+)+)$", source_url_template="https://example.org/{version}.tar.gz")
            plan = root / "plan.json"
            shard = root / "shard.json"
            run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"), "--output", str(plan)], root)
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard)], root)
            entries = {row["package_id"]: row for row in json.loads(shard.read_text())["entries"]}
            self.assertEqual(entries["mismatch"]["status"], "failed")
            self.assertIn("no stable releases", entries["mismatch"]["failure"]["message"])
            self.assertEqual(entries["malformed"]["status"], "failed")
            self.assertIn("invalid JSON", entries["malformed"]["failure"]["message"])

    def test_json_numeric_capture_does_not_hide_original_prerelease_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            archive = root / "demo-v2.0.tar.gz"
            archive.write_bytes(b"official archive uses original tag identity")
            releases = root / "tags.json"
            write_json(releases, [{"name": "v2.0"}, {"name": "v9.0-rc1"}])
            package(root, "demo", releases.as_uri(), release_regex=r"^v?(?P<version>[0-9]+(?:\.[0-9]+)+)", source_url_template=root.as_uri() + "/demo-{tag}.tar.gz")
            plan = root / "plan.json"
            shard = root / "shard.json"
            run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"), "--output", str(plan)], root)
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard)], root)
            entry = json.loads(shard.read_text())["entries"][0]
            self.assertEqual(entry["status"], "update-available")
            self.assertEqual(entry["version"], "2.0")
            self.assertEqual(entry["tag"], "v2.0")
            self.assertEqual(entry["source_url"], archive.as_uri())
            self.assertEqual(entry["sha256"], hashlib.sha256(archive.read_bytes()).hexdigest())

    def test_typed_tag_refs_retain_tag_and_hash_reviewed_source(self) -> None:
        for kind in ("tag", "commit"):
            for singleton in (False, True):
                with self.subTest(kind=kind, singleton=singleton), tempfile.TemporaryDirectory() as temporary:
                    root = pathlib.Path(temporary)
                    source = root / "source-v2.0.tar.gz"
                    source.write_bytes(b"fixed local source bytes, never executed")
                    record = dict(ref="refs/tags/v2.0", object=dict(type=kind, sha="a" * 40))
                    result = self.scan_source_contract(root, record if singleton else [record], root.as_uri() + "/source-{tag}.tar.gz")
                    self.assertEqual(result["status"], "update-available")
                    self.assertEqual((result["version"], result["tag"]), ("2.0", "v2.0"))
                    self.assertEqual(result["source_url"], source.as_uri())
                    self.assertEqual(result["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())

    def test_typed_tag_refs_reject_wrong_namespace_shape_and_hidden_prereleases(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            source = root / "source-v2.0.tar.gz"
            source.write_bytes(b"stable local fixture")
            def ref(name, kind="tag", sha="a" * 40, **metadata):
                return dict(ref=name, object=dict(type=kind, sha=sha), **metadata)
            records = [ref("refs/tags/v2.0"), ref("refs/heads/v99.0"), ref("refs/pull/99/head"),
                       ref("refs/tags/"), ref("refs/tags/v99.0", kind="blob"), ref("refs/tags/v99.1", sha="a" * 12),
                       dict(ref="refs/tags/v99.2"), ref("refs/tags/v99.3", draft=True),
                       ref("refs/tags/v99.4", prerelease=True), ref("refs/tags/v99.5-rc1"), ref("refs/tags/v99.6rc1"),
                       ref("refs/tags/v99.7\n"), ref("refs/tags/v99.8 bad"), ref("refs/tags/x/../v99.9"),
                       ref("refs/tags/.hidden/v99.10"), ref("refs/tags/x.lock/v99.11"),
                       dict(date="2099.1", id=36575835, body="v999.0", assets=[dict(name="v999.1.tar.gz")])]
            releases = root / "refs.json"
            write_json(releases, records)
            # The numeric-only selector intentionally cannot conceal a suffix.
            package(root, "demo", releases.as_uri(), release_regex=r"v?(?P<version>[0-9]+(?:\.[0-9]+)+)", source_url_template=root.as_uri() + "/source-{tag}.tar.gz")
            plan, shard = root / "plan.json", root / "shard.json"
            run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"), "--output", str(plan)], root)
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard)], root)
            result = json.loads(shard.read_bytes())["entries"][0]
            self.assertEqual((result["status"], result["version"], result["tag"]), ("update-available", "2.0", "v2.0"))
            self.assertEqual(result["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())

    def test_typed_tag_ref_template_does_not_trust_asset_checksum(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            source, binary = root / "source-2.0.tar.gz", root / "binary.tar.gz"
            source.write_bytes(b"reviewed source bytes")
            binary.write_bytes(b"wrong platform binary")
            record = dict(ref="refs/tags/v2.0", object=dict(type="tag", sha="a" * 40),
                          sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),
                          assets=[dict(name="v99.0.tar.gz", browser_download_url=binary.as_uri())])
            result = self.scan_source_contract(root, [record], root.as_uri() + "/source-{version}.tar.gz")
            self.assertEqual(result["source_url"], source.as_uri())
            self.assertEqual(result["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())

    def test_typed_tag_ref_without_source_contract_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            record = dict(ref="refs/tags/v2.0", object=dict(type="commit", sha="b" * 40),
                          assets=[dict(name="source-looking.tar.gz", browser_download_url="https://example.invalid/binary.tar.gz")])
            result = self.scan_source_contract(root, [record], None)
            self.assertEqual(result["status"], "failed")
            self.assertIn("no official source URL", result["failure"]["message"])

    def test_typed_ref_does_not_override_existing_release_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            source = root / "source-2.0.tar.gz"
            source.write_bytes(b"existing explicit release")
            record = dict(tag_name="v2.0", ref="refs/heads/v999.0", object=dict(type="blob", sha="x"), draft=False)
            result = self.scan_source_contract(root, [record], root.as_uri() + "/source-{version}.tar.gz")
            self.assertEqual((result["status"], result["version"], result["tag"]), ("update-available", "2.0", "v2.0"))
            self.assertEqual(result["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())

    def test_malformed_tag_refs_keep_failure_and_coverage_visible(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            refs = root / "refs.json"
            write_json(refs, [dict(ref="refs/heads/v999.0", object=dict(type="commit", sha="a" * 40))])
            package(root, "demo", refs.as_uri(), release_regex=r"(?P<version>[0-9]+(?:\.[0-9]+)+)", source_url_template=root.as_uri() + "/source-{version}.tar.gz")
            plan, shard, aggregate = root / "plan.json", root / "shard.json", root / "aggregate.json"
            run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"), "--output", str(plan)], root)
            run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(shard)], root)
            entry = json.loads(shard.read_bytes())["entries"][0]
            self.assertEqual(entry["status"], "failed")
            self.assertIn("no stable releases", entry["failure"]["message"])
            run_tool("check-update", ["aggregate", "--plan", str(plan), "--result", str(shard), "--output", str(aggregate)], root)
            summary = json.loads(aggregate.read_bytes())
            self.assertEqual(summary["coverage"], 1.0)
            self.assertEqual(summary["counts"]["failed"], 1)
            self.assertFalse(summary["complete"])

    @staticmethod
    def pypi_sdist(**changes):
        return {"packagetype": "sdist", "python_version": "source", "yanked": False,
                "url": "https://files.pythonhosted.org/source-2.0.tar.gz",
                "digests": {"sha256": "e" * 64}, **changes}

    @staticmethod
    def pypi_document(releases):
        return {"info": {"name": "demo", "version": "2.0"}, "urls": [], "releases": releases}

    def test_pypi_typed_sdist_metadata_ignores_first_wheel(self) -> None:
        # Reduced from official pytimeparse JSON captured 2026-10-22. This
        # verifies metadata selection, not the referenced archive's bytes.
        url = "https://files.pythonhosted.org/packages/92/bf/87bd96fd60abf241cae10e6f7fc3882c8a81ebdbe76f49f9c3116b5b38ab/pytimeparse-1.1.10.tar.gz"
        digest = "ecf0ee613a72cb0b1d3d5404bd398a64266576fc36ccf3149178af6f2ec6f736"
        wheel = self.pypi_sdist(packagetype="bdist_wheel", python_version="py3", url="https://example.invalid/wheel.whl")
        with tempfile.TemporaryDirectory() as temporary:
            result = self.scan_source_contract(pathlib.Path(temporary), self.pypi_document({
                "1.1.9": [], "1.1.10": [wheel, self.pypi_sdist(url=url, digests={"sha256": digest})]}), None)
            self.assertEqual((result["status"], result["version"], result["source_url"], result["sha256"]),
                             ("update-available", "1.1.10", url, digest))

    def test_pypi_rejects_ambiguous_sdists_before_validating_fields(self) -> None:
        for second in (self.pypi_sdist(), self.pypi_sdist(url="http://bad.invalid/source", digests={})):
            with self.subTest(second=second), tempfile.TemporaryDirectory() as temporary:
                result = self.scan_source_contract(pathlib.Path(temporary), self.pypi_document({
                    "2.0": [self.pypi_sdist(), second]}), None)
                self.assertEqual((result["status"], result["latest_version"]), ("failed", "2.0"))
                self.assertIn("exactly one", result["failure"]["message"])

    def test_pypi_rejects_invalid_source_contracts(self) -> None:
        bad = [dict(url="http://example.invalid/source"), dict(url="https://user:secret@example.invalid/source"),
               dict(url="https://@example.invalid/source"), dict(url="https://example.invalid/source#fragment"),
               dict(url="https://example.invalid:444/source"), dict(url="https://example.invalid:bad/source"),
               dict(url="https://example.invalid/source\n"), dict(url=None), dict(digests={}),
               dict(digests={"sha256": "a" * 63}), dict(digests={"sha256": "g" * 64}),
               dict(python_version="py3"), dict(yanked="false"), dict(yanked=0)]
        for changes in bad:
            with self.subTest(changes=changes), tempfile.TemporaryDirectory() as temporary:
                result = self.scan_source_contract(pathlib.Path(temporary), self.pypi_document({
                    "2.0": [self.pypi_sdist(**changes)]}), None)
                self.assertEqual((result["status"], result["latest_version"]), ("failed", "2.0"))
                self.assertEqual(result["failure"]["category"], "source")

    def test_pypi_newest_invalid_release_never_falls_back_to_older_source(self) -> None:
        for newest in ([], [self.pypi_sdist(packagetype="bdist_wheel")], None, {}, [None],
                       [self.pypi_sdist(url="http://bad.invalid/source")]):
            with self.subTest(newest=newest), tempfile.TemporaryDirectory() as temporary:
                result = self.scan_source_contract(pathlib.Path(temporary), self.pypi_document({
                    "1.1": [self.pypi_sdist()], "2.0": newest}), None)
                self.assertEqual((result["status"], result["latest_version"]), ("failed", "2.0"))
                self.assertNotIn("source_url", result)

    def test_pypi_yanked_declarations_are_not_source_candidates(self) -> None:
        for only_yanked in (False, True):
            with self.subTest(only_yanked=only_yanked), tempfile.TemporaryDirectory() as temporary:
                files = [self.pypi_sdist(yanked=True, url="http://ignored.invalid/source")]
                if not only_yanked:
                    files.append(self.pypi_sdist())
                result = self.scan_source_contract(pathlib.Path(temporary), self.pypi_document({"2.0": files}), None)
                self.assertEqual(result["status"], "failed" if only_yanked else "update-available")

    def test_pypi_keeps_existing_stable_version_and_prerelease_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = self.scan_source_contract(pathlib.Path(temporary), self.pypi_document({
                "2.0": [self.pypi_sdist()], "3.0rc1": [], "4.0dev1": []}), None)
            self.assertEqual((result["status"], result["version"]), ("update-available", "2.0"))

    def test_pypi_invalid_newest_cannot_be_overridden_by_a_template(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            source = root / "source-2.0.tar.gz"
            source.write_bytes(b"must not be selected for ambiguous PyPI metadata")
            result = self.scan_source_contract(root, self.pypi_document({"2.0": []}), root.as_uri()+"/source-{version}.tar.gz")
            self.assertEqual((result["status"], result["latest_version"]), ("failed", "2.0"))
            self.assertEqual(result["failure"]["category"], "source")

    def test_pypi_failure_retains_aggregate_coverage_without_recovery_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            result = self.scan_source_contract(root, self.pypi_document({"2.0": []}), None)
            self.assertEqual(result["status"], "failed")
            summary = root / "summary.json"
            run_tool("check-update", ["aggregate", "--plan", str(root/"plan.json"), "--result", str(root/"result.json"), "--output", str(summary)], root)
            aggregate = json.loads(summary.read_bytes())
            self.assertEqual(aggregate["coverage"], 1.0)
            self.assertEqual(aggregate["counts"]["failed"], 1)
            self.assertFalse(aggregate["complete"])

    def scan_source_contract(self, root, records, template):
        feed = root / "release.json"
        write_json(feed, records)
        package(root, "demo", feed.as_uri(), release_regex=r"^v?(?P<version>[0-9]+(?:\.[0-9]+)+)$", source_url_template=template)
        plan = root / "plan.json"
        result = root / "result.json"
        run_tool("check-update", ["plan", "--packages-dir", str(root / "packages"), "--output", str(plan)], root)
        run_tool("check-update", ["scan", "--plan", str(plan), "--shard-index", "0", "--output", str(result)], root)
        return json.loads(result.read_bytes())["entries"][0]

    def test_reviewed_template_beats_binary_asset_and_rehashes_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            source = root / "source-2.0.tar.gz"
            source.write_bytes(b"correct source fixture")
            binary = root / "demo-2.0-darwin-amd64.tar.gz"
            binary.write_bytes(b"wrong platform fixture")
            result = self.scan_source_contract(root, [dict(tag_name="v2.0", sha256=hashlib.sha256(binary.read_bytes()).hexdigest(), assets=[dict(name=binary.name, browser_download_url=binary.as_uri())])], root.as_uri() + "/source-{version}.tar.gz")
            self.assertEqual(result["source_url"], source.as_uri())
            self.assertEqual(result["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())

    def test_canonical_tarball_beats_unreviewed_asset(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            source = root / "source.tar.gz"
            source.write_bytes(b"official forge source fixture")
            binary = root / "demo-android_arm64.tar.gz"
            binary.write_bytes(b"wrong binary fixture")
            result = self.scan_source_contract(root, [dict(tag_name="v2.0", tarball_url=source.as_uri(), sha256=hashlib.sha256(binary.read_bytes()).hexdigest(), assets=[dict(name=binary.name, browser_download_url=binary.as_uri())])], None)
            self.assertEqual(result["source_url"], source.as_uri())
            self.assertEqual(result["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())

    def test_assets_without_source_contract_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            binary = root / "demo-linux.tar.gz"
            binary.write_bytes(b"not proven source")
            result = self.scan_source_contract(root, [dict(tag_name="v2.0", assets=[dict(name=binary.name, browser_download_url=binary.as_uri())])], None)
            self.assertEqual(result["status"], "failed")
            self.assertIn("no official source URL", result["failure"]["message"])

    def test_invalid_template_does_not_fall_back_to_asset(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            binary = root / "demo.tar.gz"
            binary.write_bytes(b"not chosen")
            result = self.scan_source_contract(root, [dict(tag_name="v2.0", assets=[dict(name=binary.name, browser_download_url=binary.as_uri())])], root.as_uri() + "/{unknown}.tar.gz")
            self.assertEqual(result["status"], "failed")
            self.assertIn("invalid source_url_template", result["failure"]["message"])


if __name__ == "__main__":
    unittest.main()
