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
PACKAGE_WORKFLOW_REF = f"{REPOSITORY}/.github/workflows/package-ci.yml@{PROTECTED_REF}"
BACKFILL_WORKFLOW_REF = (
    f"{REPOSITORY}/.github/workflows/rpm-repo-backfill.yml@{PROTECTED_REF}"
)


class ResolveProtectedToolingTests(unittest.TestCase):
    def git(self, root: Path, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", *arguments], cwd=root, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
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
        return old, self.git(root, "rev-parse", "HEAD")

    def pull_request_repository(self, root: Path) -> tuple[str, str, str, str]:
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
        stale_base = self.git(root, "rev-parse", "HEAD")
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
        tooling_sha = self.git(root, "rev-parse", "HEAD")
        self.git(root, "merge", "--no-ff", "--no-edit", "package-head")
        return stale_base, tooling_sha, package_head, self.git(root, "rev-parse", "HEAD")

    def run_resolver(
        self, root: Path, *, event_name: str, workflow_ref: str,
        workflow_sha: str, event_sha: str, event_ref: str,
        base_repository: str = REPOSITORY, base_ref: str = "",
        pr_number: str = "", package_head: str = "", base_sha: str = "",
        expected: int = 0,
    ) -> tuple[subprocess.CompletedProcess[str], Optional[dict[str, object]], str]:
        output = root / "tooling-binding.json"
        github_output = root / "github-output.txt"
        for path in (output, github_output):
            if path.exists():
                path.unlink()
        completed = subprocess.run(
            [
                str(SCRIPT), "--repo-root", str(root),
                "--event-name", event_name, "--repository", REPOSITORY,
                "--workflow-ref", workflow_ref, "--workflow-sha", workflow_sha,
                "--event-sha", event_sha, "--event-ref", event_ref,
                "--base-repository", base_repository, "--base-ref", base_ref,
                "--pr-number", pr_number, "--package-head", package_head,
                "--base-sha", base_sha, "--output", str(output),
                "--github-output", str(github_output),
            ],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(completed.returncode, expected, completed.stderr)
        document = json.loads(output.read_text(encoding="utf-8")) if output.exists() else None
        github_text = github_output.read_text(encoding="utf-8") if github_output.exists() else ""
        return completed, document, github_text

    def pull_request_context(self, stale: str, package: str, merge: str) -> dict[str, str]:
        return {
            "event_name": "pull_request",
            "workflow_ref": (
                f"{REPOSITORY}/.github/workflows/package-ci.yml@refs/pull/1997/merge"
            ),
            "workflow_sha": merge, "event_sha": merge,
            "event_ref": "refs/pull/1997/merge", "base_ref": "main",
            "pr_number": "1997", "package_head": package, "base_sha": stale,
        }

    def test_live_pull_request_context_binds_first_parent_and_allows_stale_payload_base(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            stale, tooling, package, merge = self.pull_request_repository(root)
            _, document, github_output = self.run_resolver(
                root, **self.pull_request_context(stale, package, merge)
            )
            self.assertNotEqual(stale, tooling)
            self.assertEqual(document["workflow_commit_sha"], merge)
            self.assertEqual(document["reported_base_sha"], stale)
            self.assertEqual(document["package_commit_sha"], package)
            self.assertEqual(document["tooling_commit_sha"], tooling)
            self.assertEqual(document["binding_source"], "pull-request-merge-first-parent")
            self.assertEqual(github_output, f"tooling_sha={tooling}\n")

    def test_pull_request_rejects_wrong_ref_number_or_mutable_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            stale, _, package, merge = self.pull_request_repository(root)
            context = self.pull_request_context(stale, package, merge)
            cases = (
                {"workflow_ref": PACKAGE_WORKFLOW_REF}, {"pr_number": "01997"},
                {"event_ref": "refs/pull/1998/merge"},
                {"workflow_sha": "refs/pull/1997/merge"}, {"event_sha": "f" * 40},
                {"base_sha": "main"}, {"package_head": "package-head"},
                {"base_repository": "attacker/openeuler-riscv-packages"},
                {"base_ref": "topic"},
            )
            for override in cases:
                with self.subTest(override=override):
                    candidate = dict(context)
                    candidate.update(override)
                    completed, document, github_output = self.run_resolver(
                        root, expected=2, **candidate
                    )
                    self.assertTrue(completed.stderr)
                    self.assertIsNone(document)
                    self.assertEqual(github_output, "")

    def test_pull_request_rejects_non_merge_or_wrong_second_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            stale, tooling, package, merge = self.pull_request_repository(root)
            context = self.pull_request_context(stale, package, merge)
            wrong_parent = dict(context)
            wrong_parent["package_head"] = stale
            completed, document, _ = self.run_resolver(root, expected=2, **wrong_parent)
            self.assertIn("second parent", completed.stderr)
            self.assertIsNone(document)

            self.git(root, "checkout", "--detach", tooling)
            non_merge = dict(context)
            non_merge["workflow_sha"] = tooling
            non_merge["event_sha"] = tooling
            completed, document, _ = self.run_resolver(root, expected=2, **non_merge)
            self.assertIn("exactly two parents", completed.stderr)
            self.assertIsNone(document)

    def test_pull_request_checkout_head_must_equal_synthetic_merge(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            stale, tooling, package, merge = self.pull_request_repository(root)
            self.git(root, "checkout", "--detach", tooling)
            completed, document, _ = self.run_resolver(
                root, expected=2, **self.pull_request_context(stale, package, merge)
            )
            self.assertIn("checked-out workflow commit", completed.stderr)
            self.assertIsNone(document)

    def test_stale_package_branch_retains_first_parent_tooling_and_package_only_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            stale, tooling, package, merge = self.pull_request_repository(root)
            _, binding, _ = self.run_resolver(
                root, **self.pull_request_context(stale, package, merge)
            )
            scope_path = root / "scope.json"
            scope = subprocess.run(
                [str(SCOPE), "--base", tooling, "--head", package,
                 "--output", str(scope_path)],
                cwd=root, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(scope.returncode, 0, scope.stderr)
            scope_document = json.loads(scope_path.read_text(encoding="utf-8"))
            self.assertEqual(scope_document["mode"], "package")
            self.assertEqual(scope_document["package_id"], "demo")
            self.assertEqual(scope_document["changed_files"], ["packages/demo/package.yaml"])

            # Downstream jobs independently check out the validated output.
            self.git(root, "checkout", "--detach", tooling)
            overlay_path = root / "overlay.json"
            overlay = subprocess.run(
                [str(MATERIALIZER), "--repo-root", str(root), "--package-id", "demo",
                 "--commit-sha", package, "--tooling-sha", tooling,
                 "--output", str(overlay_path)],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(overlay.returncode, 0, overlay.stderr)
            overlay_document = json.loads(overlay_path.read_text(encoding="utf-8"))
            self.assertEqual(binding["tooling_commit_sha"], tooling)
            self.assertEqual(overlay_document["tooling_commit_sha"], tooling)
            self.assertEqual(overlay_document["package_commit_sha"], package)
            self.assertEqual(
                (root / "ci" / "wrapper.py").read_text(encoding="utf-8"),
                "parser.add_argument('--build-timeout-seconds')\n",
            )
            self.assertEqual(
                (root / "packages" / "demo" / "package.yaml").read_text(encoding="utf-8"),
                "new package\n",
            )

    def test_merge_group_binds_explicit_protected_base_ancestor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            base, checked = self.repository(root)
            _, document, github_output = self.run_resolver(
                root, event_name="merge_group", workflow_ref=PACKAGE_WORKFLOW_REF,
                workflow_sha=checked, event_sha=checked,
                event_ref="refs/heads/gh-readonly-queue/main/pr-7-deadbeef",
                base_ref=PROTECTED_REF, package_head=checked, base_sha=base,
            )
            self.assertEqual(document["tooling_commit_sha"], base)
            self.assertEqual(document["binding_source"], "merge-group-protected-base")
            self.assertEqual(github_output, f"tooling_sha={base}\n")

    def test_merge_group_rejects_wrong_base_identity_or_nonancestor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            base, checked = self.repository(root)
            context = {
                "event_name": "merge_group", "workflow_ref": PACKAGE_WORKFLOW_REF,
                "workflow_sha": checked, "event_sha": checked,
                "event_ref": "refs/heads/gh-readonly-queue/main/pr-7-deadbeef",
                "base_ref": PROTECTED_REF, "package_head": checked, "base_sha": base,
            }
            for override in (
                {"base_ref": "main"},
                {"base_repository": "attacker/openeuler-riscv-packages"},
                {"base_sha": "main"}, {"event_sha": "f" * 40},
            ):
                with self.subTest(override=override):
                    candidate = dict(context)
                    candidate.update(override)
                    completed, document, _ = self.run_resolver(root, expected=2, **candidate)
                    self.assertTrue(completed.stderr)
                    self.assertIsNone(document)

            self.git(root, "checkout", "--orphan", "unrelated")
            self.git(root, "rm", "-f", "README.md")
            (root / "unrelated.txt").write_text("unrelated\n", encoding="utf-8")
            self.git(root, "add", ".")
            self.git(root, "commit", "-m", "unrelated base")
            unrelated = self.git(root, "rev-parse", "HEAD")
            self.git(root, "checkout", "--detach", checked)
            context["base_sha"] = unrelated
            completed, document, _ = self.run_resolver(root, expected=2, **context)
            self.assertIn("not an ancestor", completed.stderr)
            self.assertIsNone(document)

    def test_protected_main_events_use_exact_event_sha(self) -> None:
        cases = (("push", PACKAGE_WORKFLOW_REF),
                 ("workflow_dispatch", PACKAGE_WORKFLOW_REF),
                 ("workflow_call", BACKFILL_WORKFLOW_REF))
        for event_name, workflow_ref in cases:
            with self.subTest(event_name=event_name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                old, event_sha = self.repository(root)
                _, document, _ = self.run_resolver(
                    root, event_name=event_name, workflow_ref=workflow_ref,
                    workflow_sha=old, event_sha=event_sha, event_ref=PROTECTED_REF,
                )
                self.assertEqual(document["tooling_commit_sha"], event_sha)

    def test_protected_main_event_rejects_mutable_event_sha_or_ref(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, head = self.repository(root)
            completed, document, _ = self.run_resolver(
                root, event_name="workflow_dispatch", workflow_ref=PACKAGE_WORKFLOW_REF,
                workflow_sha=head, event_sha="main", event_ref=PROTECTED_REF, expected=2,
            )
            self.assertIn("full lowercase commit SHA", completed.stderr)
            self.assertIsNone(document)
            completed, document, _ = self.run_resolver(
                root, event_name="workflow_dispatch", workflow_ref=PACKAGE_WORKFLOW_REF,
                workflow_sha=head, event_sha=head, event_ref="refs/heads/topic", expected=2,
            )
            self.assertIn("event ref is unexpected", completed.stderr)
            self.assertIsNone(document)


if __name__ == "__main__":
    unittest.main()
