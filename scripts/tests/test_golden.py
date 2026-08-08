# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import pathlib
import tempfile
import unittest

from helpers import SCRIPTS, run_tool


class GoldenTests(unittest.TestCase):
    def test_repository_manifests_validate_and_sources_materialize(self) -> None:
        repo = SCRIPTS.parent
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            validation = root / "validation.json"
            run_tool(
                "validate-metadata",
                ["--repo-root", str(repo), "--schemas-dir", str(repo / "schemas"), "--output", str(validation), "--now", "2026-08-08T00:00:00Z"],
                repo,
            )
            validated = json.loads(validation.read_text())
            self.assertTrue(validated["valid"])
            self.assertEqual(validated["summary"]["golden_checked"], 3)
            materialization = root / "materialization.json"
            run_tool(
                "golden-eval",
                ["materialize", "--repo-root", str(repo), "--manifests-dir", str(repo / "tests" / "golden"), "--output-dir", str(root / "archives"), "--output", str(materialization), "--now", "2026-08-08T00:00:00Z"],
                repo,
            )
            result = json.loads(materialization.read_text())
            self.assertTrue(result["valid"])
            self.assertEqual(len(result["fixtures"]), 3)
            hello = next(item for item in result["fixtures"] if item["package_id"] == "golden-success-hello")
            self.assertFalse(hello["materialized"])

    def test_evaluate_selects_baseline_or_repaired_from_target_patch(self) -> None:
        source = {
            "kind": "official-stable-release",
            "url": "https://example.org/source-1.tar.gz",
            "sha256": "a" * 64,
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            manifests = root / "manifests"
            results = root / "results"
            manifests.mkdir()
            results.mkdir()
            for package_id in (
                "golden-success-hello",
                "golden-riscv-inline-asm",
                "golden-needs-native-kmod",
            ):
                (root / "packages" / package_id / "patches").mkdir(parents=True)

            default_manifests = {
                "golden-success-hello": {
                    "expected": {"states": ["passed"], "build_statuses": ["passed"]},
                },
                "golden-needs-native-kmod": {
                    "expected": {
                        "states": ["needs-native-riscv"],
                        "build_statuses": ["needs-native-riscv"],
                        "classifications": ["needs-native-riscv"],
                    },
                },
            }
            for package_id, extra in default_manifests.items():
                manifest = {
                    "schema_version": 1,
                    "package_id": package_id,
                    "source": source,
                    "phases": [{"name": "single"}],
                    **extra,
                }
                (manifests / (package_id + ".yaml")).write_text(json.dumps(manifest), encoding="utf-8")

            target_patch = "packages/golden-riscv-inline-asm/patches/0001-fix.patch"
            staged = {
                "schema_version": 1,
                "package_id": "golden-riscv-inline-asm",
                "source": source,
                "phases": [
                    {"name": "baseline", "expected_status": "failed"},
                    {"name": "repair", "target_patch": target_patch},
                    {"name": "repaired", "expected_status": "passed"},
                ],
                "expected_baseline": {
                    "states": ["repair-queued"],
                    "build_statuses": ["failed"],
                    "classifications": ["riscv-specific"],
                    "no_patch": True,
                    "log_patterns": ["inline asm failure"],
                },
                "expected_repaired": {
                    "states": ["passed"],
                    "build_statuses": ["passed"],
                    "patch_paths": ["patches/0001-fix.patch"],
                    "log_patterns": ["rebuild passed"],
                },
            }
            (manifests / "golden-riscv-inline-asm.yaml").write_text(json.dumps(staged), encoding="utf-8")

            def final_envelope(package_id: str, status: str) -> dict:
                return {
                    "package_id": package_id,
                    "job_id": "123:1:golden:" + package_id,
                    "checks": {
                        "metadata-validate": {"status": "passed", "evidence": "test"},
                        "source-verify": {"status": "passed", "evidence": "test"},
                        "rpmbuild-riscv64": {"status": status, "evidence": "test"},
                        "rpm-install-smoke": {"status": status, "evidence": "test"},
                        "patch-policy": {"status": "passed", "evidence": "test"},
                    },
                    "status": status,
                }

            def source_evidence(package_id: str) -> dict:
                return {
                    "package_id": package_id,
                    "source_verification": [
                        {
                            "url": source["url"],
                            "sha256": source["sha256"],
                            "verified": True,
                        }
                    ],
                }

            def evaluate(documents: list, log_text: str, output_name: str, expect_success: bool = True) -> dict:
                for old in results.rglob("*"):
                    if old.is_file():
                        old.unlink()
                (results / "results.json").write_text(json.dumps(documents), encoding="utf-8")
                log_dir = results / "golden-result-golden-riscv-inline-asm-123"
                log_dir.mkdir(exist_ok=True)
                (log_dir / "rpmbuild.log").write_text(log_text, encoding="utf-8")
                output = root / output_name
                completed = run_tool(
                    "golden-eval",
                    [
                        "evaluate",
                        "--repo-root",
                        str(root),
                        "--manifests-dir",
                        str(manifests),
                        "--results-dir",
                        str(results),
                        "--stage",
                        "auto",
                        "--output",
                        str(output),
                        "--now",
                        "2026-08-08T00:00:00Z",
                    ],
                    root,
                    expected=0 if expect_success else 1,
                )
                self.assertEqual(completed.returncode == 0, expect_success)
                return json.loads(output.read_text())

            common = [
                final_envelope("golden-success-hello", "passed"),
                source_evidence("golden-success-hello"),
                {
                    "package_id": "golden-needs-native-kmod",
                    "recommended_state": "needs-native-riscv",
                    "classification": {"category": "needs-native-riscv"},
                },
                final_envelope("golden-needs-native-kmod", "needs-native-riscv"),
                source_evidence("golden-needs-native-kmod"),
            ]
            baseline = evaluate(
                common
                + [
                    {
                        "package_id": "golden-riscv-inline-asm",
                        "recommended_state": "repair-queued",
                        "status": "failed",
                        "classification": {"category": "riscv-specific"},
                    },
                    final_envelope("golden-riscv-inline-asm", "failed"),
                    source_evidence("golden-riscv-inline-asm"),
                ],
                "compiler reported an inline asm failure",
                "baseline.json",
            )
            inline = next(item for item in baseline["goldens"] if item["package_id"] == "golden-riscv-inline-asm")
            self.assertEqual(inline["stage"], "baseline")
            self.assertTrue(inline["passed"])

            patch_path = root / target_patch
            patch_path.write_text("test patch\n", encoding="utf-8")
            repaired = evaluate(
                common
                + [
                    {
                        "package_id": "golden-riscv-inline-asm",
                        "recommended_state": "passed",
                    },
                    final_envelope("golden-riscv-inline-asm", "passed"),
                    source_evidence("golden-riscv-inline-asm"),
                ],
                "latest-head rebuild passed",
                "repaired.json",
            )
            inline = next(item for item in repaired["goldens"] if item["package_id"] == "golden-riscv-inline-asm")
            self.assertEqual(inline["stage"], "repaired")
            self.assertTrue(inline["passed"])

            # An unrelated report that says "passed" must not overrule the
            # single authoritative final build envelope.
            failed_hello = evaluate(
                [
                    {"package_id": "golden-success-hello", "status": "passed"},
                    final_envelope("golden-success-hello", "failed"),
                    source_evidence("golden-success-hello"),
                    {
                        "package_id": "golden-needs-native-kmod",
                        "recommended_state": "needs-native-riscv",
                        "classification": {"category": "needs-native-riscv"},
                    },
                    final_envelope("golden-needs-native-kmod", "needs-native-riscv"),
                    source_evidence("golden-needs-native-kmod"),
                    {
                        "package_id": "golden-riscv-inline-asm",
                        "recommended_state": "passed",
                    },
                    final_envelope("golden-riscv-inline-asm", "passed"),
                    source_evidence("golden-riscv-inline-asm"),
                ],
                "latest-head rebuild passed",
                "failed-hello.json",
                expect_success=False,
            )
            hello = next(item for item in failed_hello["goldens"] if item["package_id"] == "golden-success-hello")
            build_assertion = next(item for item in hello["assertions"] if item["name"] == "build-status")
            self.assertFalse(build_assertion["passed"])
            self.assertEqual(build_assertion["observed"], ["failed"])


if __name__ == "__main__":
    unittest.main()
