# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import hashlib
import json
import pathlib
import tempfile
import unittest
from typing import Optional

from helpers import run_tool, write_json


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
