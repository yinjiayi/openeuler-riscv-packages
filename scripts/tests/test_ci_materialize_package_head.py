# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "ci" / "materialize-package-head.py"
WORKFLOW = REPO / ".github" / "workflows" / "package-ci.yml"


class MaterializePackageHeadTests(unittest.TestCase):
    def git(self, root: Path, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", *arguments],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return completed.stdout.strip()

    def test_exact_package_tree_is_overlaid_without_replacing_tooling(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.git(root, "init")
            self.git(root, "config", "user.name", "CI Test")
            self.git(root, "config", "user.email", "ci@example.invalid")
            (root / "packages" / "example").mkdir(parents=True)
            (root / "packages" / "example" / "package.yaml").write_text(
                "package-version-one\n", encoding="utf-8"
            )
            (root / "ci").mkdir()
            (root / "ci" / "tool.py").write_text("old-tool\n", encoding="utf-8")
            self.git(root, "add", ".")
            self.git(root, "commit", "-m", "old package head")
            package_commit = self.git(root, "rev-parse", "HEAD")

            (root / "packages" / "example" / "package.yaml").write_text(
                "main-version\n", encoding="utf-8"
            )
            (root / "ci" / "tool.py").write_text("protected-main-tool\n", encoding="utf-8")
            self.git(root, "add", ".")
            self.git(root, "commit", "-m", "protected main tooling")
            tooling_commit = self.git(root, "rev-parse", "HEAD")

            output = root / "artifacts" / "overlay.json"
            completed = subprocess.run(
                [
                    str(SCRIPT),
                    "--repo-root",
                    str(root),
                    "--package-id",
                    "example",
                    "--commit-sha",
                    package_commit,
                    "--tooling-sha",
                    tooling_commit,
                    "--output",
                    str(output),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                (root / "packages" / "example" / "package.yaml").read_text(encoding="utf-8"),
                "package-version-one\n",
            )
            self.assertEqual(
                (root / "ci" / "tool.py").read_text(encoding="utf-8"),
                "protected-main-tool\n",
            )
            evidence = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(evidence["status"], "passed")
            self.assertEqual(evidence["package_commit_sha"], package_commit)
            self.assertEqual(evidence["tooling_commit_sha"], tooling_commit)

    def test_tooling_head_mismatch_fails_before_package_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.git(root, "init")
            self.git(root, "config", "user.name", "CI Test")
            self.git(root, "config", "user.email", "ci@example.invalid")
            (root / "packages" / "example").mkdir(parents=True)
            package = root / "packages" / "example" / "package.yaml"
            package.write_text("untouched\n", encoding="utf-8")
            self.git(root, "add", ".")
            self.git(root, "commit", "-m", "fixture")
            commit = self.git(root, "rev-parse", "HEAD")
            wrong = "0" * 40
            completed = subprocess.run(
                [
                    str(SCRIPT),
                    "--repo-root",
                    str(root),
                    "--package-id",
                    "example",
                    "--commit-sha",
                    commit,
                    "--tooling-sha",
                    wrong,
                    "--output",
                    str(root / "result.json"),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertEqual(package.read_text(encoding="utf-8"), "untouched\n")

    def test_trusted_dispatch_jobs_use_protected_tooling_and_exact_overlay(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        checkout = (
            "ref: ${{ inputs.commit_sha != '' && github.sha || "
            "github.event.pull_request.head.sha || github.event.merge_group.head_sha || github.sha }}"
        )
        self.assertEqual(workflow.count(checkout), 7)
        self.assertEqual(workflow.count("ci/materialize-package-head.py --repo-root ."), 7)
        self.assertEqual(workflow.count("if: inputs.commit_sha != ''"), 7)


if __name__ == "__main__":
    unittest.main()
