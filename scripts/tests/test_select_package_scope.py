# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
from typing import Optional
import unittest


REPO = Path(__file__).resolve().parents[2]
MATERIALIZER = REPO / "ci" / "materialize-package-head.py"
SELECTOR = REPO / "ci" / "select-package-scope.py"
SCHEMA = REPO / "schemas" / "tooling-overlay.schema.json"
sys.path.insert(0, str(REPO / "scripts"))


class SelectPackageScopeTests(unittest.TestCase):
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

    def repository(self, root: Path) -> tuple[str, str]:
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
        self.git(root, "commit", "-m", "historical package head")
        package_commit = self.git(root, "rev-parse", "HEAD")
        (root / "packages" / "example" / "package.yaml").write_text(
            "protected-main-version\n", encoding="utf-8"
        )
        (root / "ci" / "tool.py").write_text("protected-main-tool\n", encoding="utf-8")
        self.git(root, "add", ".")
        self.git(root, "commit", "-m", "protected main tooling")
        return package_commit, self.git(root, "rev-parse", "HEAD")

    def materialize(
        self, root: Path, package_commit: str, tooling_commit: str
    ) -> Path:
        evidence = root / "artifacts" / "scope" / "tooling-overlay.json"
        completed = subprocess.run(
            [
                str(MATERIALIZER),
                "--repo-root",
                str(root),
                "--package-id",
                "example",
                "--commit-sha",
                package_commit,
                "--tooling-sha",
                tooling_commit,
                "--output",
                str(evidence),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return evidence

    def select(
        self,
        root: Path,
        package_commit: str,
        *,
        tooling_commit: Optional[str] = None,
        evidence: Optional[Path] = None,
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
        output = root / "scope-result.json"
        arguments = [
            str(SELECTOR),
            "--repo-root",
            str(root),
            "--package-id",
            "example",
            "--head",
            package_commit,
            "--output",
            str(output),
        ]
        if tooling_commit is not None:
            arguments.extend(["--tooling-head", tooling_commit])
        if evidence is not None:
            arguments.extend(["--overlay-evidence", str(evidence)])
        completed = subprocess.run(
            arguments,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        return completed, json.loads(output.read_text(encoding="utf-8"))

    def test_ordinary_exact_checkout_retains_the_existing_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, tooling_commit = self.repository(root)
            completed, result = self.select(root, tooling_commit)
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertEqual(result["mode"], "package")
            self.assertEqual(result["head_sha"], tooling_commit)
            self.assertEqual(result["changed_files"], ["packages/example/package.yaml"])

    def test_overlay_binds_separate_package_tooling_and_tree_commits(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package_commit, tooling_commit = self.repository(root)
            evidence = self.materialize(root, package_commit, tooling_commit)
            self.assertEqual(self.git(root, "rev-parse", "HEAD"), tooling_commit)
            completed, result = self.select(
                root,
                package_commit,
                tooling_commit=tooling_commit,
                evidence=evidence,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertEqual(result["mode"], "package")
            self.assertEqual(result["head_sha"], package_commit)
            self.assertEqual(result["selection"], "trusted-explicit-package")

    def test_overlay_arguments_are_required_as_a_pair(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package_commit, tooling_commit = self.repository(root)
            completed, result = self.select(
                root, package_commit, tooling_commit=tooling_commit
            )
            self.assertEqual(completed.returncode, 2)
            self.assertEqual(result["mode"], "invalid")
            self.assertIn(
                "tooling head and overlay evidence must be supplied together",
                result["errors"],
            )

    def test_overlay_evidence_must_match_every_explicit_identity(self) -> None:
        for field, replacement in (
            ("package_commit_sha", "1" * 40),
            ("tooling_commit_sha", "2" * 40),
            ("package_tree_sha", "3" * 40),
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                package_commit, tooling_commit = self.repository(root)
                evidence = self.materialize(root, package_commit, tooling_commit)
                document = json.loads(evidence.read_text(encoding="utf-8"))
                document[field] = replacement
                evidence.write_text(json.dumps(document) + "\n", encoding="utf-8")
                completed, result = self.select(
                    root,
                    package_commit,
                    tooling_commit=tooling_commit,
                    evidence=evidence,
                )
                self.assertEqual(completed.returncode, 2)
                self.assertEqual(result["mode"], "invalid")

    def test_overlay_rejects_tracked_or_untracked_worktree_changes(self) -> None:
        for untracked in (False, True):
            with self.subTest(untracked=untracked), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                package_commit, tooling_commit = self.repository(root)
                evidence = self.materialize(root, package_commit, tooling_commit)
                if untracked:
                    (root / "packages" / "example" / "injected.txt").write_text(
                        "untrusted\n", encoding="utf-8"
                    )
                else:
                    (root / "packages" / "example" / "package.yaml").write_text(
                        "tampered\n", encoding="utf-8"
                    )
                completed, result = self.select(
                    root,
                    package_commit,
                    tooling_commit=tooling_commit,
                    evidence=evidence,
                )
                self.assertEqual(completed.returncode, 2)
                self.assertEqual(result["mode"], "invalid")

    def test_overlay_document_has_a_strict_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package_commit, tooling_commit = self.repository(root)
            evidence = self.materialize(root, package_commit, tooling_commit)
            document = json.loads(evidence.read_text(encoding="utf-8"))
            schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
            schema_errors = runpy.run_path(str(REPO / "scripts" / "validate-metadata"))[
                "schema_errors"
            ]
            self.assertEqual(schema_errors(document, schema, schema), [])
            document["unexpected"] = True
            self.assertNotEqual(schema_errors(document, schema, schema), [])


if __name__ == "__main__":
    unittest.main()
