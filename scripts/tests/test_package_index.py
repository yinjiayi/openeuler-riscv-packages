#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import gzip
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "scripts" / "generate-package-index"
VALIDATOR = ROOT / "scripts" / "validate-package-index"


class PackageIndexTests(unittest.TestCase):
    def test_generation_and_validation_preserve_overlay_and_snapshot_counts(self) -> None:
        with tempfile.TemporaryDirectory(prefix="package-index-test-") as directory:
            root = pathlib.Path(directory)
            package_dir = root / "packages" / "demo"
            package_dir.mkdir(parents=True)
            (package_dir / "package.yaml").write_text(
                json.dumps(
                    {
                        "package_id": "demo",
                        "version": {"current": "1.0", "release": "1"},
                        "rpm": {"summary": "Demo", "license": "MIT"},
                        "upstream": {"component": "example-demo", "homepage": "https://example.invalid/demo"},
                        "target": {"os": "openEuler", "release": "24.03-LTS-SP3", "arch": "riscv64", "isa": "RVA23", "riscv_status": "unknown"},
                        "build": {"profile": "qemu-user", "network_during_build": True},
                    }
                ),
                encoding="utf-8",
            )
            (package_dir / "sources.yaml").write_text(
                json.dumps({"sources": [{"url": "https://example.invalid/demo.tar.gz", "digests": {"sha256": "a" * 64}}]}),
                encoding="utf-8",
            )
            catalog_dir = root / "catalog" / "snapshots"
            catalog_dir.mkdir(parents=True)
            snapshot = {
                "schema_version": 1,
                "snapshot_id": "fixture-snapshot",
                "policy": {"verified_source_required": True},
                "candidates": [],
                "rejections": [
                    {
                        "component_id": "example-foo",
                        "package_base": "foo",
                        "name": "foo",
                        "decision": "unverified-upstream",
                        "lineage": [{"source": "arch"}],
                    }
                ],
            }
            snapshot_path = catalog_dir / "fixture.json"
            snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
            reviewed_path = root / "catalog" / "upstream-releases.yaml"
            reviewed_path.write_text(
                json.dumps({"schema_version": 1, "kind": "reviewed-upstream-releases", "source_snapshot_id": "fixture-snapshot", "releases": []}),
                encoding="utf-8",
            )
            prs_path = root / "prs.json"
            prs_path.write_text(
                json.dumps(
                    [
                        {
                            "number": 7,
                            "title": "Update demo to 1.1",
                            "state": "OPEN",
                            "mergedAt": None,
                            "closedAt": None,
                            "headRefName": "update/demo/1.1",
                            "headRefOid": "b" * 40,
                            "baseRefName": "main",
                            "labels": [{"name": "package:demo"}],
                            "updatedAt": "2026-08-21T00:00:00Z",
                            "url": "https://github.com/example/demo/pull/7",
                        }
                    ]
                ),
                encoding="utf-8",
            )
            output = root / "catalog" / "package-index.json.gz"
            summary = root / "catalog" / "package-index-summary.json"
            command = [
                sys.executable,
                str(GENERATOR),
                "--repo-root",
                str(root),
                "--snapshot",
                "catalog/snapshots/fixture.json",
                "--reviewed-evidence",
                "catalog/upstream-releases.yaml",
                "--pull-requests",
                str(prs_path),
                "--main-ref",
                "c" * 40,
                "--generated-at",
                "2026-08-21T00:00:00Z",
                "--output",
                str(output),
                "--summary-output",
                str(summary),
            ]
            subprocess.run(command, cwd=ROOT, check=True, stdout=subprocess.PIPE, text=True)
            index = json.load(gzip.open(output, "rt", encoding="utf-8"))
            self.assertEqual(index["source_snapshot"]["record_count"], 1)
            self.assertEqual(index["pull_request_count"], 1)
            self.assertEqual({entry["discovery_key"] for entry in index["entries"]}, {"demo", "foo"})
            validation = root / "validation.json"
            subprocess.run(
                [sys.executable, str(VALIDATOR), "--repo-root", str(root), "--output", str(validation)],
                cwd=ROOT,
                check=True,
            )
            self.assertTrue(json.loads(validation.read_text(encoding="utf-8"))["valid"])


if __name__ == "__main__":
    unittest.main()
