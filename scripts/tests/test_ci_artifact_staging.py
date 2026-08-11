# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import os
import pathlib
import stat
import subprocess
import sys
import tempfile
import unittest


REPO = pathlib.Path(__file__).resolve().parents[2]
STAGER = REPO / "ci" / "stage-build-artifacts.py"


class BuildArtifactStagingTests(unittest.TestCase):
    def test_only_regular_evidence_logs_and_rpms_are_staged(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            artifact_dir = root / "artifacts" / "build"
            work_dir = root / "work" / "demo"
            output_dir = root / "upload"
            (work_dir / "RPMS" / "riscv64").mkdir(parents=True)
            (work_dir / "SRPMS").mkdir(parents=True)
            (work_dir / "BUILD" / "watch_dir").mkdir(parents=True)
            artifact_dir.mkdir(parents=True)

            (artifact_dir / "environment.json").write_text('{"arch":"riscv64"}\n', encoding="utf-8")
            (artifact_dir / "rpmbuild.log").write_text("build failed\n", encoding="utf-8")
            (artifact_dir / "unapproved.txt").write_text("not evidence\n", encoding="utf-8")
            (artifact_dir / "target.json").symlink_to(artifact_dir / "environment.json")
            os.mkfifo(artifact_dir / "runtime.log")

            (work_dir / "RPMS" / "riscv64" / "demo-1.0-1.riscv64.rpm").write_bytes(b"rpm")
            (work_dir / "SRPMS" / "demo-1.0-1.src.rpm").write_bytes(b"srpm")
            (work_dir / "RPMS" / "riscv64" / "linked.rpm").symlink_to(
                work_dir / "RPMS" / "riscv64" / "demo-1.0-1.riscv64.rpm"
            )
            os.mkfifo(work_dir / "RPMS" / "riscv64" / "runtime.rpm")
            os.mkfifo(work_dir / "BUILD" / "watch_dir" / "fsevent-0")
            (output_dir / "stale").mkdir(parents=True)
            (output_dir / "stale" / "old.txt").write_text("stale\n", encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(STAGER),
                    "--package-id",
                    "demo",
                    "--artifact-dir",
                    str(artifact_dir),
                    "--work-dir",
                    str(work_dir),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=str(REPO),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertFalse((output_dir / "stale").exists())
            self.assertFalse((output_dir / "work" / "demo" / "BUILD").exists())

            expected = {
                "artifacts/build/environment.json",
                "artifacts/build/rpmbuild.log",
                "work/demo/RPMS/riscv64/demo-1.0-1.riscv64.rpm",
                "work/demo/SRPMS/demo-1.0-1.src.rpm",
            }
            manifest_path = output_dir / "artifacts" / "build" / "archive-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(set(manifest["included_files"]), expected)
            self.assertEqual(manifest["status"], "passed")
            self.assertIn("non-regular-file", {entry["reason"] for entry in manifest["excluded_entries"]})
            self.assertIn(
                "not-structured-evidence-or-log",
                {entry["reason"] for entry in manifest["excluded_entries"]},
            )
            for path in output_dir.rglob("*"):
                if path.is_dir():
                    continue
                self.assertTrue(stat.S_ISREG(path.lstat().st_mode), str(path))

    def test_infrastructure_scope_still_emits_a_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            output_dir = root / "upload"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(STAGER),
                    "--package-id",
                    "",
                    "--artifact-dir",
                    str(root / "missing-artifacts"),
                    "--work-dir",
                    str(root / "work"),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=str(REPO),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            manifest = json.loads(
                (output_dir / "artifacts" / "build" / "archive-manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertIsNone(manifest["package_id"])
            self.assertEqual(manifest["included_files"], [])


if __name__ == "__main__":
    unittest.main()
