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

    def test_all_package_jobs_use_protected_tooling_and_exact_overlay(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        protected_checkout = (
            "ref: ${{ needs.authorize-trusted-dispatch.outputs.tooling_sha }}"
        )
        immutable_candidate = (
            "ref: ${{ (github.event_name == 'pull_request' || "
            "github.event_name == 'merge_group') && github.workflow_sha || github.sha }}"
        )
        untrusted_checkout = (
            "ref: ${{ inputs.commit_sha != '' && github.sha || "
            "github.event.pull_request.head.sha || "
            "github.event.merge_group.head_sha || github.sha }}"
        )
        exact_package_head = (
            "${{ inputs.commit_sha || github.event.pull_request.head.sha || "
            "github.event.merge_group.head_sha || github.sha }}"
        )
        self.assertEqual(workflow.count(immutable_candidate), 1)
        self.assertEqual(workflow.count(protected_checkout), 8)
        self.assertNotIn(untrusted_checkout, workflow)
        self.assertEqual(workflow.count("github.event.pull_request.base.sha"), 1)
        self.assertIn(
            "fetch-depth: ${{ github.event_name == 'pull_request' && 2 || 0 }}",
            workflow,
        )
        self.assertIn('--pr-number "$PR_NUMBER"', workflow)
        self.assertIn('--package-head "$PACKAGE_HEAD"', workflow)
        self.assertIn('--base-sha "$BASE_SHA"', workflow)
        self.assertEqual(workflow.count("ci/materialize-package-head.py --repo-root ."), 7)
        downstream_overlay = (
            "- name: Materialize only the exact package tree\n"
            "        if: needs.prepare.outputs.mode == 'package'"
        )
        self.assertEqual(workflow.count(downstream_overlay), 6)
        self.assertGreaterEqual(workflow.count(exact_package_head), 7)
        self.assertEqual(workflow.count('--tooling-sha "$TOOLING_COMMIT_SHA"'), 7)
        self.assertEqual(
            workflow.count(
                "TOOLING_COMMIT_SHA: "
                "${{ needs.authorize-trusted-dispatch.outputs.tooling_sha }}"
            ),
            7,
        )
        self.assertIn("Classify the exact event delta with protected tooling", workflow)
        self.assertIn("Materialize only the exact package tree", workflow)
        self.assertIn('--tooling-head "$TOOLING_HEAD_SHA"', workflow)
        self.assertIn(
            "TOOLING_HEAD_SHA: "
            "${{ needs.authorize-trusted-dispatch.outputs.tooling_sha }}",
            workflow,
        )
        self.assertIn(
            "&& needs.authorize-trusted-dispatch.outputs.tooling_sha || "
            "github.event.before || inputs.base_sha }}",
            workflow,
        )
        self.assertIn(
            "--overlay-evidence artifacts/scope/tooling-overlay.json", workflow
        )
        self.assertIn(
            "tooling_sha: ${{ steps.tooling.outputs.tooling_sha }}", workflow
        )
        self.assertIn("ci/resolve-protected-tooling.py", workflow)
        self.assertIn(
            "if: always() && github.event_name == 'pull_request' && "
            "needs.authorize-trusted-dispatch.outputs.authorized == 'true'",
            workflow,
        )


if __name__ == "__main__":
    unittest.main()
