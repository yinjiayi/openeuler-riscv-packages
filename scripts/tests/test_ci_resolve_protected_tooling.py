# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
from typing import Optional
import unittest


REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "ci" / "resolve-protected-tooling.py"
SCOPE = REPO / "ci" / "detect-change-scope.py"
MATERIALIZER = REPO / "ci" / "materialize-package-head.py"
REPOSITORY = "yinjiayi/openeuler-riscv-packages"
PROTECTED_REF = "refs/heads/main"
PACKAGE_WORKFLOW_REF = (
    f"{REPOSITORY}/.github/workflows/package-ci.yml@{PROTECTED_REF}"
)
BACKFILL_WORKFLOW_REF = (
    f"{REPOSITORY}/.github/workflows/rpm-repo-backfill.yml@{PROTECTED_REF}"
)


class ResolveProtectedToolingTests(unittest.TestCase):
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
        (root / "README.md").write_text("old tooling\n", encoding="utf-8")
        self.git(root, "add", ".")
        self.git(root, "commit", "-m", "old protected tooling")
        old = self.git(root, "rev-parse", "HEAD")
        (root / "README.md").write_text("new workflow and wrapper\n", encoding="utf-8")
        self.git(root, "add", ".")
        self.git(root, "commit", "-m", "new protected tooling")
        new = self.git(root, "rev-parse", "HEAD")
        return old, new

    def run_resolver(
        self,
        root: Path,
        *,
        event_name: str = "pull_request",
        workflow_ref: str = PACKAGE_WORKFLOW_REF,
        workflow_sha: str,
        event_sha: str,
        event_ref: str = "refs/pull/7/merge",
        base_repository: str = REPOSITORY,
        base_ref: str = "main",
        expected: int = 0,
    ) -> tuple[subprocess.CompletedProcess[str], Optional[dict[str, object]], str]:
        output = root / "tooling-binding.json"
        github_output = root / "github-output.txt"
        completed = subprocess.run(
            [
                str(SCRIPT),
                "--repo-root",
                str(root),
                "--event-name",
                event_name,
                "--repository",
                REPOSITORY,
                "--workflow-ref",
                workflow_ref,
                "--workflow-sha",
                workflow_sha,
                "--event-sha",
                event_sha,
                "--event-ref",
                event_ref,
                "--base-repository",
                base_repository,
                "--base-ref",
                base_ref,
                "--output",
                str(output),
                "--github-output",
                str(github_output),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(completed.returncode, expected, completed.stderr)
        document = json.loads(output.read_text(encoding="utf-8")) if output.exists() else None
        github_text = github_output.read_text(encoding="utf-8") if github_output.exists() else ""
        return completed, document, github_text

    def test_stale_pull_request_base_and_merge_sha_cannot_replace_workflow_sha(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            stale_base, workflow_sha = self.repository(root)
            merge_sha = "f" * 40

            _, document, github_output = self.run_resolver(
                root,
                workflow_sha=workflow_sha,
                event_sha=merge_sha,
            )

            self.assertNotEqual(stale_base, workflow_sha)
            self.assertEqual(document["tooling_commit_sha"], workflow_sha)
            self.assertNotEqual(document["tooling_commit_sha"], merge_sha)
            self.assertEqual(github_output, f"tooling_sha={workflow_sha}\n")

    def test_stale_package_branch_retains_new_tooling_and_package_only_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.git(root, "init")
            self.git(root, "config", "user.name", "CI Test")
            self.git(root, "config", "user.email", "ci@example.invalid")
            (root / "packages" / "demo").mkdir(parents=True)
            (root / "packages" / "demo" / "package.yaml").write_text(
                "old package\n", encoding="utf-8"
            )
            (root / "ci").mkdir()
            (root / "ci" / "wrapper.py").write_text("old wrapper\n", encoding="utf-8")
            self.git(root, "add", ".")
            self.git(root, "commit", "-m", "shared stale base")
            protected_branch = self.git(root, "branch", "--show-current")

            self.git(root, "switch", "-c", "package-head")
            (root / "packages" / "demo" / "package.yaml").write_text(
                "new package\n", encoding="utf-8"
            )
            self.git(root, "add", ".")
            self.git(root, "commit", "-m", "package update")
            package_head = self.git(root, "rev-parse", "HEAD")

            self.git(root, "switch", protected_branch)
            (root / "ci" / "wrapper.py").write_text(
                "parser.add_argument('--build-timeout-seconds')\n", encoding="utf-8"
            )
            self.git(root, "add", ".")
            self.git(root, "commit", "-m", "advance protected workflow and wrapper")
            workflow_sha = self.git(root, "rev-parse", "HEAD")

            _, binding, _ = self.run_resolver(
                root,
                workflow_sha=workflow_sha,
                event_sha="f" * 40,
            )
            scope_path = root / "scope.json"
            scope = subprocess.run(
                [
                    str(SCOPE),
                    "--base",
                    workflow_sha,
                    "--head",
                    package_head,
                    "--output",
                    str(scope_path),
                ],
                cwd=root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(scope.returncode, 0, scope.stderr)
            scope_document = json.loads(scope_path.read_text(encoding="utf-8"))
            self.assertEqual(scope_document["mode"], "package")
            self.assertEqual(scope_document["package_id"], "demo")
            self.assertEqual(
                scope_document["changed_files"], ["packages/demo/package.yaml"]
            )

            overlay_path = root / "overlay.json"
            overlay = subprocess.run(
                [
                    str(MATERIALIZER),
                    "--repo-root",
                    str(root),
                    "--package-id",
                    "demo",
                    "--commit-sha",
                    package_head,
                    "--tooling-sha",
                    workflow_sha,
                    "--output",
                    str(overlay_path),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(overlay.returncode, 0, overlay.stderr)
            overlay_document = json.loads(overlay_path.read_text(encoding="utf-8"))
            self.assertEqual(binding["tooling_commit_sha"], workflow_sha)
            self.assertEqual(overlay_document["tooling_commit_sha"], workflow_sha)
            self.assertEqual(overlay_document["package_commit_sha"], package_head)
            self.assertEqual(
                (root / "ci" / "wrapper.py").read_text(encoding="utf-8"),
                "parser.add_argument('--build-timeout-seconds')\n",
            )
            self.assertEqual(
                (root / "packages" / "demo" / "package.yaml").read_text(encoding="utf-8"),
                "new package\n",
            )

    def test_merge_group_uses_workflow_sha(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, workflow_sha = self.repository(root)

            _, document, _ = self.run_resolver(
                root,
                event_name="merge_group",
                workflow_sha=workflow_sha,
                event_sha="e" * 40,
                event_ref="refs/heads/gh-readonly-queue/main/pr-7-deadbeef",
                base_ref=PROTECTED_REF,
            )

            self.assertEqual(document["tooling_commit_sha"], workflow_sha)

    def test_mutable_or_malformed_workflow_sha_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, head = self.repository(root)

            completed, document, github_output = self.run_resolver(
                root,
                workflow_sha="refs/heads/main",
                event_sha=head,
                expected=2,
            )

            self.assertIn("full lowercase commit SHA", completed.stderr)
            self.assertIsNone(document)
            self.assertEqual(github_output, "")

    def test_pull_request_identity_guards_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, head = self.repository(root)
            cases = (
                {"workflow_ref": f"{REPOSITORY}/.github/workflows/package-ci.yml@refs/heads/topic"},
                {"base_repository": "attacker/openeuler-riscv-packages"},
                {"base_ref": "topic"},
            )
            for overrides in cases:
                with self.subTest(overrides=overrides):
                    completed, document, _ = self.run_resolver(
                        root,
                        workflow_sha=head,
                        event_sha="e" * 40,
                        expected=2,
                        **overrides,
                    )
                    self.assertTrue(completed.stderr)
                    self.assertIsNone(document)

    def test_checked_out_head_must_equal_workflow_sha(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            old, new = self.repository(root)
            self.git(root, "checkout", "--detach", old)

            completed, document, _ = self.run_resolver(
                root,
                workflow_sha=new,
                event_sha="e" * 40,
                expected=2,
            )

            self.assertIn("checked-out tooling commit", completed.stderr)
            self.assertIsNone(document)

    def test_protected_main_events_use_exact_event_sha(self) -> None:
        cases = (
            ("push", PACKAGE_WORKFLOW_REF),
            ("workflow_dispatch", PACKAGE_WORKFLOW_REF),
            ("workflow_call", BACKFILL_WORKFLOW_REF),
        )
        for event_name, workflow_ref in cases:
            with self.subTest(event_name=event_name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                old, event_sha = self.repository(root)
                _, document, _ = self.run_resolver(
                    root,
                    event_name=event_name,
                    workflow_ref=workflow_ref,
                    workflow_sha=old,
                    event_sha=event_sha,
                    event_ref=PROTECTED_REF,
                    base_ref="",
                )
                self.assertEqual(document["tooling_commit_sha"], event_sha)

    def test_protected_main_event_rejects_mutable_event_sha_or_ref(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, head = self.repository(root)
            mutable, document, _ = self.run_resolver(
                root,
                event_name="workflow_dispatch",
                workflow_sha=head,
                event_sha="main",
                event_ref=PROTECTED_REF,
                base_ref="",
                expected=2,
            )
            self.assertIn("full lowercase commit SHA", mutable.stderr)
            self.assertIsNone(document)

            wrong_ref, document, _ = self.run_resolver(
                root,
                event_name="workflow_dispatch",
                workflow_sha=head,
                event_sha=head,
                event_ref="refs/heads/topic",
                base_ref="",
                expected=2,
            )
            self.assertIn("event ref is unexpected", wrong_ref.stderr)
            self.assertIsNone(document)


if __name__ == "__main__":
    unittest.main()
