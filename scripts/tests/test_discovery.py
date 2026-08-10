# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import gzip
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
            debian = root / "debian.json"
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
                        {
                            "name": "alias-demo",
                            "version": "4.2-1",
                            "repository": "extra",
                            "license": "MIT",
                            "description": "Small terminal alias demonstration utility",
                            "upstream_url": "https://alias.example.org/project",
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
                        {"name": "supplement-only", "version": "3.0", "repository": "everything", "license": "Apache-2.0", "upstream_url": "https://codeberg.org/example/supplement", "source_url": "https://codeberg.org/example/supplement/archive/v3.0.tar.gz", "sha256": "b" * 64},
                        {"name": "alias-demo", "version": "4.2-7.fc44", "repository": "Everything-source", "license": "MIT", "description": "Terminal utility demonstrating aliases", "upstream_url": "https://github.com/example/alias-demo", "source_url": "https://github.com/example/alias-demo/archive/refs/tags/v4.2.tar.gz", "sha256": "d" * 64},
                    ],
                },
            )
            write_json(
                debian,
                {
                    "snapshot": {
                        "resolved_release": "13.6",
                        "codename": "trixie",
                        "components": ["main"],
                        "snapshot_at": "2026-08-08T00:00:00Z",
                    },
                    "packages": [
                        {
                            "name": "foo",
                            "version": "1.2.3+dfsg-2",
                            "repository": "stable/main",
                            "license": "unknown",
                            "upstream_url": "https://github.com/example/foo",
                        },
                        {
                            "name": "license-gap",
                            "version": "1.0-1",
                            "repository": "stable/main",
                            "license": "unknown",
                            "upstream_url": "https://example.org/license-gap",
                        },
                    ],
                },
            )
            snapshot = root / "snapshot.json.gz"
            summary = root / "summary.json"
            run_tool(
                "discover-packages",
                [
                    "--input", "arch=%s" % arch,
                    "--input", "aur=%s" % aur,
                    "--input", "fedora=%s" % fedora,
                    "--input", "debian=%s" % debian,
                    "--output", str(snapshot),
                    "--summary", str(summary),
                    "--as-of", "2026-08-08T00:00:00Z",
                ],
                root,
            )
            raw = snapshot.read_bytes()
            self.assertEqual(raw[:2], b"\x1f\x8b")
            self.assertEqual(raw[4:8], b"\0\0\0\0", "gzip mtime must be deterministic")
            with gzip.open(snapshot, "rt", encoding="utf-8") as handle:
                result = json.load(handle)
            self.assertEqual({item["name"] for item in result["candidates"]}, {"foo", "supplement-only", "alias-demo"})
            foo_candidates = [item for item in result["candidates"] if item["component_id"] == "github.com-example-foo"]
            self.assertEqual(len(foo_candidates), 1)
            self.assertEqual(foo_candidates[0]["stable_version"], "1.2.3")
            self.assertEqual(
                {item["source"] for item in foo_candidates[0]["lineage"]},
                {"arch", "aur", "debian"},
            )
            reasons = {item["name"]: item["decision"] for item in result["rejections"]}
            self.assertEqual(reasons["foo-bin"], "binary-only")
            self.assertEqual(reasons["foo-git"], "vcs-only")
            self.assertEqual(reasons["stale"], "stale")
            self.assertEqual(reasons["testing-only"], "excluded-repository")
            self.assertEqual(reasons["future-release"], "pre-release")
            self.assertEqual(reasons["license-gap"], "license-blocked")
            license_gap = next(item for item in result["rejections"] if item["name"] == "license-gap")
            self.assertEqual(license_gap["stable_version"], "1.0")
            self.assertEqual(result["policy"]["normalization_version"], 5)
            alias_demo = next(item for item in result["candidates"] if item["name"] == "alias-demo")
            self.assertEqual(alias_demo["component_id"], "github.com-example-alias-demo")
            self.assertEqual({item["source"] for item in alias_demo["lineage"]}, {"arch", "fedora"})
            self.assertEqual(
                alias_demo["deduplication"]["component_aliases"],
                ["alias.example.org-project", "github.com-example-alias-demo"],
            )
            self.assertFalse(result["policy"]["execute_external_packaging"])
            self.assertTrue(result["policy"]["verified_source_required"])

            resolved = root / "resolved.json"
            run_tool("resolve-upstream", ["--input", str(snapshot), "--output", str(resolved), "--as-of", "2026-08-08T00:00:00Z"], root)
            components = json.loads(resolved.read_text())["components"]
            self.assertEqual(
                {item["package_id"] for item in components},
                {"foo", "supplement-only", "alias-demo"},
            )
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

    def test_resolver_layers_reviewed_evidence_without_mutating_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            snapshot = root / "snapshot.json"
            original = {
                "snapshot_id": "discovery-reviewed-fixture",
                "candidates": [],
                "rejections": [
                    {
                        "name": "demo",
                        "package_base": "demo",
                        "component_id": "example.org-demo",
                        "stable_version": "1.0",
                        "decision": "unverified-upstream",
                        "upstream_url": "https://example.org/demo",
                        "lineage": [
                            {
                                "source": "arch",
                                "repository": "extra",
                                "original_name": "demo",
                                "package_base": "demo",
                                "source_version": "1.0-1",
                                "fetched_at": "2026-08-08T00:00:00Z",
                            }
                        ],
                    }
                ],
            }
            write_json(snapshot, original)
            evidence = root / "evidence.json"
            write_json(
                evidence,
                {
                    "schema_version": 1,
                    "kind": "reviewed-upstream-releases",
                    "source_snapshot_id": "discovery-reviewed-fixture",
                    "reviewed_at": "2026-08-08T01:00:00Z",
                    "policy": {
                        "stable_only": True,
                        "official_https_required": True,
                        "source_sha256_required": True,
                        "external_packaging_executed": False,
                    },
                    "releases": [
                        {
                            "component_id": "example.org-demo",
                            "package_id": "demo",
                            "canonical_name": "demo",
                            "summary": "Reviewed demo release",
                            "license": "MIT",
                            "version": "1.1",
                            "upstream": {
                                "homepage": "https://example.org/demo",
                                "repository_url": "https://example.org/demo.git",
                                "release_api": "https://example.org/demo/releases/",
                                "release_regex": "demo-([0-9.]+)\\.tar\\.gz",
                                "source_url_template": "https://example.org/demo-{version}.tar.gz",
                            },
                            "source": {"url": "https://example.org/demo-1.1.tar.gz", "filename": "demo-1.1.tar.gz", "sha256": "d" * 64},
                            "evidence": {
                                "release_page": "https://example.org/demo/releases/",
                                "verified_at": "2026-08-08T01:00:00Z",
                                "method": "downloaded-official-archive-and-calculated-sha256",
                                "license_file": "LICENSE",
                                "archive_inspection": {
                                    "checked": True,
                                    "root_directory": "demo-1.1",
                                    "absolute_paths": False,
                                    "parent_traversal": False,
                                    "symlinks": False,
                                },
                            },
                            "build_requires": ["gcc", "make"],
                            "requires": [],
                        }
                    ],
                },
            )
            output = root / "resolved.json"
            run_tool(
                "resolve-upstream",
                ["--input", str(snapshot), "--reviewed-evidence", str(evidence), "--output", str(output), "--as-of", "2026-08-08T02:00:00Z"],
                root,
            )
            result = json.loads(output.read_text())
            self.assertEqual(len(result["components"]), 1)
            component = result["components"][0]
            self.assertEqual(component["latest_observed_version"], "1.1")
            self.assertEqual(component["source"]["sha256"], "d" * 64)
            self.assertEqual(component["upstream"]["source_url_template"], "https://example.org/demo-{version}.tar.gz")
            self.assertIn("reviewed-official-release", {item["type"] for item in component["resolution_evidence"]})
            self.assertFalse(result["policy"]["external_packaging_executed"])
            self.assertEqual(json.loads(snapshot.read_text()), original)

            reviewed = json.loads(evidence.read_text())
            for method in (
                "downloaded-official-release-archive-and-calculated-sha256",
                "downloaded-official-release-asset-and-calculated-sha256",
                "downloaded-official-tag-archive-and-calculated-sha256",
                "downloaded-official-archive-and-matched-publisher-sha256sum",
            ):
                reviewed["releases"][0]["evidence"]["method"] = method
                write_json(evidence, reviewed)
                run_tool(
                    "resolve-upstream",
                    [
                        "--input",
                        str(snapshot),
                        "--reviewed-evidence",
                        str(evidence),
                        "--output",
                        str(root / ("resolved-" + method + ".json")),
                    ],
                    root,
                )

            unsafe = json.loads(evidence.read_text())
            unsafe["releases"][0]["evidence"]["archive_inspection"]["symlinks"] = True
            write_json(evidence, unsafe)
            rejected = run_tool(
                "resolve-upstream",
                ["--input", str(snapshot), "--reviewed-evidence", str(evidence), "--output", str(root / "unsafe.json")],
                root,
                expected=2,
            )
            self.assertIn("archive safety inspection is incomplete", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
