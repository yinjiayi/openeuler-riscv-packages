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


if __name__ == "__main__":
    unittest.main()
