# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import runpy
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from unittest import mock


REPO = pathlib.Path(__file__).resolve().parents[2]
RUNNER = REPO / "ci" / "run-rpmbuild-container.py"
PREPARE_DEPS = REPO / "ci" / "prepare-build-deps.py"
PACKAGE_POLICY = REPO / "ci" / "package-policy.py"
QEMU_RUNNER_POLICY = REPO / "ci" / "qemu-runner-policy.py"
sys.path.insert(0, str(REPO / "scripts"))


def load_module(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RUNNER_MODULE = load_module(RUNNER, "ci_run_rpmbuild_container")
DEPS_MODULE = load_module(PREPARE_DEPS, "ci_prepare_build_deps")
QEMU_POLICY_MODULE = load_module(QEMU_RUNNER_POLICY, "ci_qemu_runner_policy")


def option(command: list[str], name: str) -> str:
    return command[command.index(name) + 1]


class BuildUserPolicyTests(unittest.TestCase):
    def test_host_build_entrypoints_are_executable(self) -> None:
        for path in (PREPARE_DEPS, RUNNER):
            self.assertTrue(path.is_file(), path)
            self.assertTrue(path.stat().st_mode & 0o111, f"not executable: {path}")

    def test_package_schema_accepts_only_the_two_build_user_policies(self) -> None:
        schema = json.loads((REPO / "schemas" / "package.schema.json").read_text())
        package = json.loads(
            (REPO / "packages" / "golden-success-hello" / "package.yaml").read_text()
        )
        schema_errors = runpy.run_path(str(REPO / "scripts" / "validate-metadata"))[
            "schema_errors"
        ]

        for value in ("root", "unprivileged"):
            candidate = copy.deepcopy(package)
            candidate["build"]["user"] = value
            self.assertEqual(schema_errors(candidate, schema, schema), [], value)

        invalid = copy.deepcopy(package)
        invalid["build"]["user"] = "automatic"
        self.assertTrue(
            any(
                "$.build.user is not in enum" in error
                for error in schema_errors(invalid, schema, schema)
            )
        )

    def test_package_policy_defaults_to_root_and_emits_explicit_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package_dir = pathlib.Path(temporary) / "demo"
            package_dir.mkdir()
            output = pathlib.Path(temporary) / "policy.json"
            github_output = pathlib.Path(temporary) / "github-output"
            document = {
                "package_id": "demo",
                "build": {"profile": "qemu-user", "timeout_minutes": 30},
            }
            (package_dir / "package.yaml").write_text(json.dumps(document) + "\n")
            subprocess.run(
                [
                    sys.executable,
                    str(PACKAGE_POLICY),
                    "--package-dir",
                    str(package_dir),
                    "--output",
                    str(output),
                    "--github-output",
                    str(github_output),
                ],
                check=True,
            )
            self.assertEqual(json.loads(output.read_text())["build_user"], "root")
            self.assertIn("build_user=root\n", github_output.read_text())

            document["build"]["user"] = "unprivileged"
            (package_dir / "package.yaml").write_text(json.dumps(document) + "\n")
            output.unlink()
            github_output.unlink()
            subprocess.run(
                [
                    sys.executable,
                    str(PACKAGE_POLICY),
                    "--package-dir",
                    str(package_dir),
                    "--output",
                    str(output),
                    "--github-output",
                    str(github_output),
                ],
                check=True,
            )
            self.assertEqual(json.loads(output.read_text())["build_user"], "unprivileged")
            self.assertIn("build_user=unprivileged\n", github_output.read_text())

    def test_package_policy_rejects_unknown_value(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package_dir = pathlib.Path(temporary) / "demo"
            package_dir.mkdir()
            (package_dir / "package.yaml").write_text(
                json.dumps(
                    {
                        "package_id": "demo",
                        "build": {
                            "profile": "qemu-user",
                            "timeout_minutes": 30,
                            "user": "automatic",
                        },
                    }
                )
                + "\n"
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(PACKAGE_POLICY),
                    "--package-dir",
                    str(package_dir),
                    "--output",
                    str(pathlib.Path(temporary) / "policy.json"),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("unknown build.user", completed.stderr)


class BuildContainerCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = pathlib.Path("/runner/work/repository")
        self.work = self.repo / "work" / "demo"
        self.artifacts = self.repo / "artifacts" / "build"
        self.image = "openeuler-builddeps:123-1"
        self.commit = "a" * 40

    def test_root_policy_preserves_root_rpmbuild_and_exact_provenance(self) -> None:
        command = RUNNER_MODULE.build_command(
            self.image,
            self.repo,
            self.work,
            self.artifacts,
            "demo",
            self.commit,
            "root",
        )
        self.assertEqual(option(command, "--user"), "0:0")
        self.assertEqual(option(command, "--build-user"), "root")
        self.assertEqual(option(command, "--commit-sha"), self.commit)
        self.assertEqual(option(command, "--result"), "/evidence/rpmbuild-phase-result.json")
        self.assertIn(f"{self.artifacts}:/evidence:rw", command)
        self.assertIn("--offline", command)
        self.assertEqual(option(command, "--network"), "none")

    def test_unprivileged_policy_uses_fixed_identity_and_generated_work_tree(self) -> None:
        command = RUNNER_MODULE.build_command(
            self.image,
            self.repo,
            self.work,
            self.artifacts,
            "demo",
            self.commit,
            "unprivileged",
        )
        self.assertEqual(option(command, "--user"), "10001:10001")
        self.assertEqual(option(command, "--build-user"), "unprivileged")
        self.assertEqual(
            option(command, "--result"),
            "/workspace/work/demo/.ci-result/rpmbuild-phase-result.json",
        )
        self.assertNotIn(f"{self.artifacts}:/evidence:rw", command)
        self.assertIn(f"{self.work}:/workspace/work/demo:rw", command)
        self.assertIn(f"{self.repo}:/workspace:ro", command)
        self.assertIn("--offline", command)
        self.assertEqual(option(command, "--network"), "none")

    def test_ownership_handoff_is_root_only_and_network_isolated(self) -> None:
        command = RUNNER_MODULE.unprivileged_prepare_command(
            self.image, self.repo, self.work, "demo"
        )
        self.assertEqual(option(command, "--user"), "0:0")
        self.assertEqual(option(command, "--network"), "none")
        self.assertIn("prepare", command)
        self.assertIn("/workspace/work/demo/.ci-result", command)

    def test_handoff_targets_fixed_uid_gid_and_rejects_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary) / "work"
            (root / "SOURCES").mkdir(parents=True)
            (root / "SOURCES" / "source.tar.xz").write_bytes(b"source")
            with mock.patch.object(RUNNER_MODULE.os, "chown") as chown:
                count = RUNNER_MODULE.handoff_ownership(root)
            self.assertEqual(count, 3)
            self.assertEqual(chown.call_count, 3)
            for call in chown.call_args_list:
                self.assertEqual(call.args[1:3], (10001, 10001))
                self.assertFalse(call.kwargs["follow_symlinks"])

            (root / "unsafe").symlink_to("SOURCES")
            with self.assertRaises(RUNNER_MODULE.ContractError):
                RUNNER_MODULE.ownership_entries(root)

    def test_exec_identity_checks_reject_policy_user_mismatches(self) -> None:
        arguments = Namespace(
            build_user="unprivileged",
            work_dir="/work",
            result_dir="/result",
            identity_output="/result/identity.json",
            command=["scripts/build-rpm", "--offline"],
        )
        with mock.patch.object(
            RUNNER_MODULE,
            "target_identity",
            return_value=(Namespace(pw_name="rpmbuild"), Namespace()),
        ), mock.patch.object(RUNNER_MODULE.os, "geteuid", return_value=0), mock.patch.object(
            RUNNER_MODULE.os, "getegid", return_value=0
        ):
            with self.assertRaisesRegex(RUNNER_MODULE.ContractError, "must never run as root"):
                RUNNER_MODULE.exec_mode(arguments)

        arguments.build_user = "root"
        with mock.patch.object(RUNNER_MODULE.os, "geteuid", return_value=10001), mock.patch.object(
            RUNNER_MODULE.os, "getegid", return_value=10001
        ):
            with self.assertRaisesRegex(RUNNER_MODULE.ContractError, "UID/GID 0:0"):
                RUNNER_MODULE.exec_mode(arguments)

    def test_unprivileged_run_copies_only_regular_structured_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = pathlib.Path(temporary) / "repo"
            work = repo / "work" / "demo"
            artifacts = repo / "artifacts" / "build"
            package = repo / "packages" / "demo"
            work.mkdir(parents=True)
            artifacts.mkdir(parents=True)
            package.mkdir(parents=True)
            (package / "package.yaml").write_text("{}\n")

            calls = 0

            def fake_run(command, *, check):
                nonlocal calls
                calls += 1
                result_dir = work / ".ci-result"
                if calls == 1:
                    (result_dir / "ownership-handoff.json").write_text(
                        '{"kind":"rpmbuild-ownership-handoff"}\n'
                    )
                else:
                    (result_dir / "build-identity.json").write_text(
                        '{"uid":10001,"gid":10001}\n'
                    )
                    (result_dir / "rpmbuild-phase-result.json").write_text(
                        json.dumps({"commit_sha": self.commit}) + "\n"
                    )
                return subprocess.CompletedProcess(command, 0)

            arguments = Namespace(
                image=self.image,
                package_id="demo",
                repo_root=str(repo),
                work_dir=str(work),
                artifact_dir=str(artifacts),
                commit_sha=self.commit,
                build_user="unprivileged",
            )
            with mock.patch.object(RUNNER_MODULE.subprocess, "run", side_effect=fake_run):
                self.assertEqual(RUNNER_MODULE.run_mode(arguments), 0)
            self.assertEqual(calls, 2)
            for name in RUNNER_MODULE.EVIDENCE_FILES:
                self.assertTrue((artifacts / name).is_file(), name)
            self.assertEqual(
                json.loads((artifacts / "rpmbuild-phase-result.json").read_text())[
                    "commit_sha"
                ],
                self.commit,
            )

    def test_dependency_install_and_user_provisioning_are_explicitly_root(self) -> None:
        self.assertEqual(
            DEPS_MODULE.root_exec("container", "dnf", "install"),
            ["docker", "exec", "--user", "0:0", "container", "dnf", "install"],
        )
        commands = DEPS_MODULE.build_user_provision_commands("container")
        self.assertEqual(len(commands), 2)
        for command in commands:
            self.assertEqual(command[:5], ["docker", "exec", "--user", "0:0", "container"])
            self.assertIn(command[5], {"groupadd", "useradd"})
        self.assertIn("10001", commands[0])
        self.assertIn("10001", commands[1])

    def test_workflow_keeps_native_routing_outside_both_build_user_paths(self) -> None:
        workflow = (REPO / ".github" / "workflows" / "package-ci.yml").read_text()
        condition = (
            "needs.prepare.outputs.mode == 'package' && "
            "needs.prepare.outputs.needs_native != 'true'"
        )
        self.assertGreaterEqual(workflow.count(condition), 4)
        self.assertIn(
            "if: needs.prepare.outputs.mode == 'package' && "
            "needs.prepare.outputs.needs_native == 'true'",
            workflow,
        )
        self.assertIn('ci/run-rpmbuild-container.py run', workflow)
        self.assertIn('--build-user "$BUILD_USER"', workflow)

    def test_self_hosted_qemu_pool_is_protected_main_only(self) -> None:
        workflow = (REPO / ".github" / "workflows" / "package-ci.yml").read_text()
        trusted = (
            "needs.prepare.outputs.mode == 'package' && "
            "needs.prepare.outputs.needs_native != 'true' && "
            "(github.event_name == 'push' || github.event_name == 'workflow_dispatch') && "
            "github.ref == 'refs/heads/main'"
        )
        labels = '["self-hosted","linux","x64","oe-rva23-qemu"]'
        self.assertEqual(workflow.count(trusted), 2)
        self.assertEqual(workflow.count(labels), 2)
        self.assertNotIn("github.event_name == 'pull_request'", trusted)
        self.assertNotIn("github.event_name == 'merge_group'", trusted)
        self.assertIn("needs.prepare.outputs.needs_native != 'true'", trusted)

    def test_runner_policy_routes_only_non_native_protected_main_work(self) -> None:
        for event in ("pull_request", "merge_group", "workflow_run", "schedule"):
            decision = QEMU_POLICY_MODULE.decide(
                "package", False, event, "refs/heads/main"
            )
            self.assertEqual(decision["runner_kind"], "github-hosted", event)
        for ref in ("refs/pull/1/merge", "refs/heads/topic", "refs/tags/v1"):
            decision = QEMU_POLICY_MODULE.decide("package", False, "push", ref)
            self.assertEqual(decision["runner_kind"], "github-hosted", ref)
        self.assertEqual(
            QEMU_POLICY_MODULE.decide(
                "infrastructure", False, "push", "refs/heads/main"
            )["runner_kind"],
            "github-hosted",
        )
        self.assertEqual(
            QEMU_POLICY_MODULE.decide(
                "package", True, "push", "refs/heads/main"
            )["runner_kind"],
            "github-hosted",
        )
        for event in ("push", "workflow_dispatch"):
            decision = QEMU_POLICY_MODULE.decide(
                "package", False, event, "refs/heads/main"
            )
            self.assertEqual(decision["runner_kind"], "self-hosted-qemu", event)
            self.assertEqual(
                decision["labels"],
                ["self-hosted", "linux", "x64", "oe-rva23-qemu"],
            )


if __name__ == "__main__":
    unittest.main()
