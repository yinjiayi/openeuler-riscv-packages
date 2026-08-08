# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import pathlib
import tempfile
import unittest

from helpers import run_tool, write_json


class DiscoveryTests(unittest.TestCase):
    def test_filters_and_deduplicates_without_executing_aur(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            arch = root / "arch.json"
            aur = root / "aur.json"
            fedora = root / "fedora.json"
            write_json(
                arch,
                {
                    "snapshot": {"resolved_release": "rolling", "components": ["core", "extra"], "snapshot_at": "2026-08-08T00:00:00Z"},
                    "packages": [
                        {
                            "name": "foo",
                            "package_base": "foo",
                            "version": "1.2.3-1",
                            "repository": "core",
                            "license": "MIT",
                            "upstream_url": "https://github.com/example/foo",
                            "source_url": "https://github.com/example/foo/archive/refs/tags/v1.2.3.tar.gz",
                            "sha256": "a" * 64,
                        },
                        {
                            "name": "testing-only",
                            "version": "1",
                            "repository": "core-testing",
                            "license": "MIT",
                            "upstream_url": "https://example.org/testing-only",
                            "source_url": "https://example.org/testing-only-1.tar.gz",
                        },
                        {
                            "name": "future-release",
                            "version": "2.0rc1-1",
                            "repository": "extra",
                            "license": "MIT",
                            "upstream_url": "https://example.org/future-release",
                            "source_url": "https://example.org/future-release-2.0rc1.tar.gz",
                            "sha256": "c" * 64,
                        },
                    ],
                },
            )
            write_json(
                aur,
                {
                    "snapshot": {"resolved_release": "AUR", "components": ["RPC"], "snapshot_at": "2026-08-08T00:00:00Z"},
                    "results": [
                        {"Name": "foo", "PackageBase": "foo", "Version": "9.9.9-2", "License": ["MIT"], "URL": "https://github.com/example/foo", "LastModified": 1786000000},
                        {"Name": "foo-bin", "PackageBase": "foo-bin", "Version": "1.2.0", "License": ["MIT"], "URL": "https://github.com/example/foo", "LastModified": 1786000000},
                        {"Name": "foo-git", "PackageBase": "foo-git", "Version": "r10", "License": ["MIT"], "URL": "https://github.com/example/foo", "LastModified": 1786000000},
                        {"Name": "stale", "Version": "1", "License": ["MIT"], "URL": "https://example.org/stale", "LastModified": 1500000000},
                    ],
                },
            )
            write_json(
                fedora,
                {
                    "snapshot": {"resolved_release": "44", "components": ["Everything-source"], "snapshot_at": "2026-08-08T00:00:00Z"},
                    "packages": [
                        {"name": "supplement-only", "version": "3.0", "repository": "everything", "license": "Apache-2.0", "upstream_url": "https://codeberg.org/example/supplement", "source_url": "https://codeberg.org/example/supplement/archive/v3.0.tar.gz", "sha256": "b" * 64}
                    ],
                },
            )
            snapshot = root / "snapshot.json"
            summary = root / "summary.json"
            run_tool(
                "discover-packages",
                [
                    "--input", "arch=%s" % arch,
                    "--input", "aur=%s" % aur,
                    "--input", "fedora=%s" % fedora,
                    "--output", str(snapshot),
                    "--summary", str(summary),
                    "--as-of", "2026-08-08T00:00:00Z",
                ],
                root,
            )
            result = json.loads(snapshot.read_text())
            self.assertEqual({item["name"] for item in result["candidates"]}, {"foo", "supplement-only"})
            foo_candidates = [item for item in result["candidates"] if item["component_id"] == "github.com-example-foo"]
            self.assertEqual(len(foo_candidates), 1)
            self.assertEqual(foo_candidates[0]["stable_version"], "1.2.3")
            self.assertEqual({item["source"] for item in foo_candidates[0]["lineage"]}, {"arch", "aur"})
            reasons = {item["name"]: item["decision"] for item in result["rejections"]}
            self.assertEqual(reasons["foo-bin"], "binary-only")
            self.assertEqual(reasons["foo-git"], "vcs-only")
            self.assertEqual(reasons["stale"], "stale")
            self.assertEqual(reasons["testing-only"], "excluded-repository")
            self.assertEqual(reasons["future-release"], "pre-release")
            self.assertFalse(result["policy"]["execute_external_packaging"])
            self.assertTrue(result["policy"]["verified_source_required"])

            resolved = root / "resolved.json"
            run_tool("resolve-upstream", ["--input", str(snapshot), "--output", str(resolved), "--as-of", "2026-08-08T00:00:00Z"], root)
            components = json.loads(resolved.read_text())["components"]
            self.assertEqual({item["package_id"] for item in components}, {"foo", "supplement-only"})
            foo = next(item for item in components if item["package_id"] == "foo")
            self.assertEqual(foo["source"]["sha256"], "a" * 64)
            self.assertEqual({item["name"] for item in foo["excluded_variant_lineage"]}, {"foo-bin", "foo-git"})

    def test_config_can_supply_metadata_urls(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            metadata = root / "arch.json"
            write_json(metadata, {"packages": [{"name": "x", "version": "1", "repository": "extra", "license": "MIT", "upstream_url": "https://example.org/x", "source_url": "https://example.org/x-1.tar.gz"}]})
            config = root / "sources.yaml"
            write_json(config, {"policy": {"aur_stale_days": 730}, "sources": {"arch": {"enabled": True, "metadata_urls": [str(metadata)]}}})
            output = root / "out.json"
            run_tool("discover-packages", ["--config", str(config), "--output", str(output), "--as-of", "2026-08-08T00:00:00Z"], root)
            result = json.loads(output.read_text())
            self.assertEqual(result["candidates"], [])
            self.assertEqual(len(result["rejections"]), 1)
            self.assertEqual(result["rejections"][0]["decision"], "unverified-upstream")

    def test_resolver_rejects_source_without_checksum(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            snapshot = root / "snapshot.json"
            write_json(
                snapshot,
                {
                    "snapshot_id": "discovery-test",
                    "candidates": [
                        {
                            "name": "unchecked",
                            "package_base": "unchecked",
                            "version": "1.0",
                            "component_id": "example.org-unchecked",
                            "decision": "eligible",
                            "license": "MIT",
                            "upstream_url": "https://example.org/unchecked",
                            "source_url": "https://example.org/unchecked-1.0.tar.gz",
                            "sha256": None,
                            "lineage": [{"source": "arch", "original_name": "unchecked"}],
                        }
                    ],
                    "rejections": [],
                },
            )
            output = root / "resolved.json"
            run_tool("resolve-upstream", ["--input", str(snapshot), "--output", str(output), "--as-of", "2026-08-08T00:00:00Z"], root)
            result = json.loads(output.read_text())
            self.assertEqual(result["components"], [])
            self.assertEqual(result["rejections"][0]["reason"], "no-verifiable-stable-source")


if __name__ == "__main__":
    unittest.main()
