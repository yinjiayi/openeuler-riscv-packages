# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "ci" / "stage-golden-products.py"
PACKAGE = "golden-success-hello"
COMMIT = "a" * 40


class GoldenPhysicalProductTests(unittest.TestCase):
    def setup_workspace(self, workspace: Path) -> tuple[dict, Path]:
        products = []
        for tree, filename, data, kind in (
            ("RPMS/riscv64", "hello.rpm", b"inert-mock-binary-product", "rpm"),
            ("SRPMS", "hello.src.rpm", b"inert-mock-source-product", "srpm"),
        ):
            relative = f"work/{PACKAGE}/{tree}/{filename}"
            path = workspace / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            products.append({"path": "/workspace/" + relative, "sha256": hashlib.sha256(data).hexdigest(),
                             "size": len(data), "kind": kind})
        phase = {"schema_version": 1, "kind": "build-result",
                 "started_at": "2026-10-10T00:00:00Z", "completed_at": "2026-10-10T00:00:01Z",
                 "status": "passed", "phase": "complete", "exit_code": 0,
                 "package_id": PACKAGE, "commit_sha": COMMIT,
                 "target": {"os": "openEuler 24.03 LTS SP3", "arch": "riscv64", "isa": "RVA23"},
                 "source_verification": [], "commands": [["private-command-canary"]],
                 "artifacts": products, "failure": None}
        phase_path = workspace / "artifacts" / "golden" / PACKAGE / "rpmbuild-phase-result.json"
        phase_path.parent.mkdir(parents=True)
        phase_path.write_text(json.dumps(phase))
        return phase, phase_path

    def run_stage(self, workspace: Path, expected: int = 0, native: bool = False) -> tuple[dict, Path]:
        completed = subprocess.run([sys.executable, str(TOOL), "--workspace", str(workspace),
                                    "--package-id", PACKAGE, "--commit-sha", COMMIT,
                                    "--needs-native", "true" if native else "false"],
                                   capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, expected, completed.stderr)
        output = workspace / "artifacts" / "golden-products" / PACKAGE
        manifest = json.loads((output / "physical-products.json").read_text())
        self.assertNotIn("private-command-canary", json.dumps(manifest))
        return manifest, output

    def test_exact_passed_products_are_separate_from_logs_and_config(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            _, phase_path = self.setup_workspace(workspace)
            for relative in (f"work/{PACKAGE}/BUILD/unwanted.rpm", f"work/{PACKAGE}/SOURCES/secret.rpm",
                             f"artifacts/golden/{PACKAGE}/private.log", f"work/{PACKAGE}/RPMS/private.repo"):
                path = workspace / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("private-command-canary")
            manifest, output = self.run_stage(workspace)
            self.assertEqual(manifest["phase_sha256"], hashlib.sha256(phase_path.read_bytes()).hexdigest())
            self.assertEqual(manifest["product_evidence"], "phase-matched-physical-products")
            self.assertEqual(len(manifest["products"]), 2)
            files = {path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()}
            self.assertEqual(files, {"physical-products.json", f"work/{PACKAGE}/RPMS/riscv64/hello.rpm",
                                     f"work/{PACKAGE}/SRPMS/hello.src.rpm"})
            for product in manifest["products"]:
                path = output / product["path"]
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), product["sha256"])

    def test_success_rejects_missing_corrupt_extra_and_false_claims(self) -> None:
        for change in ("missing", "corrupt", "extra", "duplicate", "sha", "size", "kind", "path", "head", "package", "schema"):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temporary:
                workspace = Path(temporary)
                phase, path = self.setup_workspace(workspace)
                rpm = workspace / f"work/{PACKAGE}/RPMS/riscv64/hello.rpm"
                if change == "missing": rpm.unlink()
                elif change == "corrupt": rpm.write_bytes(b"corrupt")
                elif change == "extra": (rpm.parent / "extra.rpm").write_bytes(b"extra")
                elif change == "duplicate": phase["artifacts"].append(dict(phase["artifacts"][0]))
                elif change == "sha": phase["artifacts"][0]["sha256"] = "f" * 64
                elif change == "size": phase["artifacts"][0]["size"] += 1
                elif change == "kind": phase["artifacts"][0]["kind"] = "srpm"
                elif change == "path": phase["artifacts"][0]["path"] = f"/workspace/work/{PACKAGE}/RPMS/../secret.rpm"
                elif change == "head": phase["commit_sha"] = "b" * 40
                elif change == "package": phase["package_id"] = "other"
                elif change == "schema": phase["unknown"] = "private-command-canary"
                path.write_text(json.dumps(phase))
                manifest, output = self.run_stage(workspace, expected=1)
                self.assertEqual(manifest["status"], "failed")
                self.assertEqual(manifest["products"], [])
                self.assertEqual(list(output.rglob("*.rpm")), [])

    def test_failed_phase_preserves_partial_bytes_without_success_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            phase, path = self.setup_workspace(workspace)
            phase.update(status="failed", phase="rpmbuild", exit_code=1, artifacts=[])
            path.write_text(json.dumps(phase))
            manifest, _ = self.run_stage(workspace)
            self.assertEqual(manifest["phase_status"], "failed")
            self.assertEqual(manifest["product_evidence"], "unverified-partial-or-no-build")
            self.assertEqual(len(manifest["products"]), 2)

    def test_native_and_early_failure_do_not_fabricate_products(self) -> None:
        for native in (True, False):
            with self.subTest(native=native), tempfile.TemporaryDirectory() as temporary:
                manifest, output = self.run_stage(Path(temporary), native=native)
                self.assertEqual(manifest["products"], [])
                self.assertEqual(list(output.rglob("*.rpm")), [])
                self.assertEqual(manifest["product_evidence"], "not-built-native-route" if native else "unverified-partial-or-no-build")

    def test_native_rejects_unexpected_products(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            self.setup_workspace(workspace)
            manifest, _ = self.run_stage(workspace, expected=1, native=True)
            self.assertEqual(manifest["products"], [])

    def test_symlinks_and_fifo_rpms_fail_closed(self) -> None:
        for change in ("work", "tree", "directory", "file", "phase", "fifo"):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temporary:
                workspace = Path(temporary)
                _, phase = self.setup_workspace(workspace)
                rpm = workspace / f"work/{PACKAGE}/RPMS/riscv64/hello.rpm"
                target = {"work": workspace / "work", "tree": rpm.parent.parent,
                          "directory": rpm.parent, "file": rpm, "phase": phase, "fifo": rpm}[change]
                parked = target.with_name(target.name + "-parked")
                target.rename(parked)
                if change == "fifo": os.mkfifo(target)
                else: target.symlink_to(parked, target_is_directory=parked.is_dir())
                manifest, _ = self.run_stage(workspace, expected=1)
                self.assertEqual(manifest["products"], [])

    def test_stale_output_is_not_deleted_or_reused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            self.setup_workspace(workspace)
            _, output = self.run_stage(workspace)
            before = {p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob("*") if p.is_file()}
            result = subprocess.run([sys.executable, str(TOOL), "--workspace", str(workspace),
                                     "--package-id", PACKAGE, "--commit-sha", COMMIT,
                                     "--needs-native", "false"], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            after = {p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_parser_resource_overflow_fails_without_copying_products(self) -> None:
        for limit, value in (("MAX_PHASE_BYTES", 1), ("MAX_TREE_DEPTH", 1)):
            with self.subTest(limit=limit), tempfile.TemporaryDirectory() as temporary:
                workspace = Path(temporary)
                self.setup_workspace(workspace)
                spec = importlib.util.spec_from_file_location("golden_product_limit_test", TOOL)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                with mock.patch.object(module, limit, value), mock.patch.object(
                        sys, "argv", [str(TOOL), "--workspace", str(workspace),
                                      "--package-id", PACKAGE, "--commit-sha", COMMIT,
                                      "--needs-native", "false"]):
                    self.assertEqual(module.main(), 1)
                output = workspace / "artifacts" / "golden-products" / PACKAGE
                manifest = json.loads((output / "physical-products.json").read_text())
                self.assertEqual(manifest["status"], "failed")
                self.assertEqual(manifest["products"], [])
                self.assertEqual(list(output.rglob("*.rpm")), [])

    def test_workflow_keeps_products_outside_text_ingestion(self) -> None:
        text = (REPO / ".github/workflows/golden-evaluation.yml").read_text()
        exercise, evaluate = text.split("  evaluate:\n", 1)
        self.assertIn("python3 ci/stage-golden-products.py --workspace .", exercise)
        self.assertIn("name: golden-products-${{ matrix.package_id }}-${{ github.run_id }}", exercise)
        self.assertIn("path: artifacts/golden-products/${{ matrix.package_id }}/", exercise)
        self.assertIn("pattern: golden-result-*-${{ github.run_id }}", evaluate)
        self.assertNotIn("golden-products", evaluate)
        self.assertEqual(exercise.count("retention-days: 7"), 3)


if __name__ == "__main__":
    unittest.main()
