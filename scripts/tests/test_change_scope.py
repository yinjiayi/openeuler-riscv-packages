# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import tempfile
import unittest


REPO = pathlib.Path(__file__).resolve().parents[2]
DETECTOR = REPO / "ci" / "detect-change-scope.py"
PACKAGE_POLICY = REPO / "ci" / "package-policy.py"


def run(arguments: list[str], root: pathlib.Path, expected: int = 0) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        arguments,
        cwd=str(root),
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != expected:
        raise AssertionError(
            "command returned %s, expected %s\nstdout:\n%s\nstderr:\n%s"
            % (completed.returncode, expected, completed.stdout, completed.stderr)
        )
    return completed


def git(root: pathlib.Path, *arguments: str) -> str:
    completed = run(["git", *arguments], root)
    return completed.stdout.strip()


def write(root: pathlib.Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def commit(root: pathlib.Path, relative: str, content: str, message: str) -> str:
    write(root, relative, content)
    git(root, "add", "--", relative)
    git(root, "commit", "-m", message)
    return git(root, "rev-parse", "HEAD")


def repository(root: pathlib.Path) -> str:
    git(root, "init", "--initial-branch=main")
    git(root, "config", "user.name", "Scope Test")
    git(root, "config", "user.email", "scope-test@example.invalid")
    return commit(root, "README.md", "fixture\n", "initial")


def detect(root: pathlib.Path, base: str, head: str, expected: int = 0) -> dict[str, object]:
    output = root / "scope.json"
    run(
        [str(DETECTOR), "--base", base, "--head", head, "--output", str(output)],
        root,
        expected,
    )
    return json.loads(output.read_text(encoding="utf-8"))


class ChangeScopeTests(unittest.TestCase):
    def test_base_advances_multiple_times_without_polluting_package_delta(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            common = repository(root)
            git(root, "switch", "-c", "acl-head")
            head = commit(root, "packages/acl/README.md", "acl\n", "package acl")
            git(root, "switch", "main")
            commit(root, "packages/fmt/README.md", "fmt\n", "package fmt")
            commit(root, "ci/shared.py", "# shared\n", "shared infrastructure")
            base = commit(root, "packages/ed/README.md", "ed\n", "package ed")

            document = detect(root, base, head)

            self.assertEqual(document["mode"], "package")
            self.assertEqual(document["package_id"], "acl")
            self.assertEqual(document["changed_files"], ["packages/acl/README.md"])
            self.assertEqual(document["base_sha"], base)
            self.assertEqual(document["head_sha"], head)
            self.assertEqual(document["merge_base_sha"], common)
            self.assertEqual(document["errors"], [])

    def test_true_two_package_delta_remains_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            base = repository(root)
            write(root, "packages/acl/README.md", "acl\n")
            write(root, "packages/attr/README.md", "attr\n")
            git(root, "add", "--", "packages/acl/README.md", "packages/attr/README.md")
            git(root, "commit", "-m", "two packages")
            head = git(root, "rev-parse", "HEAD")

            document = detect(root, base, head, expected=2)

            self.assertEqual(document["mode"], "invalid")
            self.assertEqual(document["package_id"], "")
            self.assertEqual(
                document["changed_files"],
                ["packages/acl/README.md", "packages/attr/README.md"],
            )
            self.assertIn("exactly one package directory", document["errors"][0])

    def test_infrastructure_delta_remains_infrastructure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            base = repository(root)
            head = commit(root, "ci/shared.py", "# shared\n", "shared infrastructure")

            document = detect(root, base, head)

            self.assertEqual(document["mode"], "infrastructure")
            self.assertEqual(document["package_id"], "")
            self.assertEqual(document["changed_files"], ["ci/shared.py"])
            self.assertEqual(document["merge_base_sha"], base)

    def test_native_package_scope_preserves_native_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            repository(root)
            package_dir = root / "packages" / "golden-needs-native-kmod"
            write(
                root,
                "packages/golden-needs-native-kmod/package.yaml",
                json.dumps(
                    {
                        "package_id": "golden-needs-native-kmod",
                        "build": {
                            "profile": "needs-native-riscv",
                            "native_reason": "kernel module load required",
                            "timeout_minutes": 30,
                        },
                    }
                )
                + "\n",
            )
            git(root, "add", "--", "packages/golden-needs-native-kmod/package.yaml")
            git(root, "commit", "-m", "native policy")
            base = git(root, "rev-parse", "HEAD")
            head = commit(
                root,
                "packages/golden-needs-native-kmod/README.md",
                "native fixture\n",
                "update native package",
            )

            scope = detect(root, base, head)
            self.assertEqual(scope["mode"], "package")
            self.assertEqual(scope["package_id"], "golden-needs-native-kmod")

            policy_output = root / "policy.json"
            run(
                [
                    str(PACKAGE_POLICY),
                    "--package-dir",
                    str(package_dir),
                    "--output",
                    str(policy_output),
                ],
                root,
            )
            policy = json.loads(policy_output.read_text(encoding="utf-8"))
            self.assertTrue(policy["needs_native"])
            self.assertEqual(policy["build_profile"], "needs-native-riscv")

    def test_ref_name_is_rejected_instead_of_resolved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            head = repository(root)

            document = detect(root, "main", head, expected=2)

            self.assertEqual(document["mode"], "invalid")
            self.assertIsNone(document["base_sha"])
            self.assertEqual(document["head_sha"], head)
            self.assertIsNone(document["merge_base_sha"])
            self.assertEqual(document["changed_files"], [])
            self.assertIn("full 40-character commit SHA", document["errors"][0])

    def test_head_that_is_already_in_base_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            head = repository(root)
            base = commit(root, "packages/ed/README.md", "ed\n", "package ed")

            document = detect(root, base, head, expected=2)

            self.assertEqual(document["mode"], "invalid")
            self.assertEqual(document["changed_files"], [])
            self.assertIsNone(document["merge_base_sha"])
            self.assertIn("already an ancestor", document["errors"][0])

    def test_unrelated_histories_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            base = repository(root)
            git(root, "switch", "--orphan", "unrelated")
            head = commit(root, "packages/acl/README.md", "acl\n", "unrelated package")

            document = detect(root, base, head, expected=2)

            self.assertEqual(document["mode"], "invalid")
            self.assertEqual(document["changed_files"], [])
            self.assertIn("common ancestor", document["errors"][0])


if __name__ == "__main__":
    unittest.main()
