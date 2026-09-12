# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import re
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
PACKAGE_WORKFLOW = REPO / ".github" / "workflows" / "package-ci.yml"
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
    def test_rpmbuild_job_uses_validated_package_timeout(self) -> None:
        workflow = PACKAGE_WORKFLOW.read_text(encoding="utf-8")
        marker = "  rpmbuild-riscv64:\n"
        self.assertIn(marker, workflow)
        job = workflow.split(marker, 1)[1].split("\n  rpm-install-smoke:\n", 1)[0]
        self.assertIn(
            "timeout-minutes: ${{ fromJSON(needs.prepare.outputs.timeout_minutes || '120') }}",
            job,
        )
        self.assertNotIn("timeout-minutes: 120", job)
        self.assertIn(
            "PACKAGE_TIMEOUT_MINUTES: ${{ needs.prepare.outputs.timeout_minutes || '120' }}",
            job,
        )
        self.assertIn(
            "ci/rpmbuild-timeout-budget.py start",
            job,
        )
        deadline_step = job.split(
            "- name: Establish the validated package deadline", 1
        )[1].split("- name: Materialize only the exact package tree", 1)[0]
        self.assertIn("if: needs.prepare.outputs.mode == 'package'", deadline_step)
        self.assertIn(
            "rpmbuild_timeout_seconds=$(ci/rpmbuild-timeout-budget.py remaining",
            job,
        )
        self.assertIn('[[ "$rpmbuild_timeout_seconds" =~ ^[1-9][0-9]*$ ]]', job)
        self.assertIn(
            '[[ "$rpmbuild_outer_timeout_seconds" =~ ^[1-9][0-9]*$ ]]', job
        )
        self.assertIn(
            '--max-bytes 52428800 --timeout-seconds "$rpmbuild_outer_timeout_seconds" --',
            job,
        )
        self.assertNotIn(
            '--max-bytes 52428800 --timeout-seconds "$rpmbuild_timeout_seconds" --',
            job,
        )
        self.assertIn(
            '--build-timeout-seconds "$rpmbuild_timeout_seconds"',
            job,
        )
        reserve = re.search(r"--reserve-seconds ([0-9]+)", job)
        grace = re.search(
            r"rpmbuild_outer_timeout_seconds=\$\(\(rpmbuild_timeout_seconds \+ ([0-9]+)\)\)",
            job,
        )
        self.assertIsNotNone(reserve)
        self.assertIsNotNone(grace)
        reserve_seconds = int(reserve.group(1))
        grace_seconds = int(grace.group(1))
        self.assertEqual(9981 + grace_seconds, 10041)
        self.assertGreaterEqual(reserve_seconds - grace_seconds, 240)
        self.assertNotIn("--timeout-seconds 6900", job)

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
            9981,
        )
        self.assertEqual(option(command, "--user"), "0:0")
        self.assertEqual(option(command, "--build-user"), "root")
        self.assertEqual(option(command, "--commit-sha"), self.commit)
        self.assertEqual(option(command, "--result"), "/evidence/rpmbuild-phase-result.json")
        self.assertEqual(option(command, "--timeout"), "9981")
        self.assertGreater(command.index("--timeout"), command.index("scripts/build-rpm"))
        self.assertIn(f"{self.artifacts}:/evidence:rw", command)
        self.assertNotIn("--offline", command)
        self.assertEqual(option(command, "--network"), "bridge")
        self.assertIn("OE_BUILD_NETWORK=enabled", command)

    def test_unprivileged_policy_uses_fixed_identity_and_generated_work_tree(self) -> None:
        command = RUNNER_MODULE.build_command(
            self.image,
            self.repo,
            self.work,
            self.artifacts,
            "demo",
            self.commit,
            "unprivileged",
            9981,
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
        self.assertNotIn("--offline", command)
        self.assertEqual(option(command, "--network"), "bridge")
        self.assertIn("OE_BUILD_NETWORK=enabled", command)

    def test_build_timeout_is_positive_and_preserved_above_7200_seconds(self) -> None:
        command = RUNNER_MODULE.build_command(
            self.image,
            self.repo,
            self.work,
            self.artifacts,
            "demo",
            self.commit,
            "root",
            9981,
        )
        self.assertEqual(option(command, "--timeout"), "9981")

        for invalid in (0, -1, True, "9981"):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(
                RUNNER_MODULE.ContractError, "positive integer"
            ):
                RUNNER_MODULE.build_command(
                    self.image,
                    self.repo,
                    self.work,
                    self.artifacts,
                    "demo",
                    self.commit,
                    "root",
                    invalid,
                )

    def test_run_cli_rejects_noncanonical_timeout_values(self) -> None:
        base = [
            "run",
            "--image",
            self.image,
            "--package-id",
            "demo",
            "--repo-root",
            str(self.repo),
            "--work-dir",
            str(self.work),
            "--artifact-dir",
            str(self.artifacts),
            "--commit-sha",
            self.commit,
            "--build-user",
            "root",
            "--build-timeout-seconds",
        ]
        self.assertEqual(
            RUNNER_MODULE.parser().parse_args([*base, "9981"]).build_timeout_seconds,
            9981,
        )
        for invalid in ("0", "-1", "+9981", "9.5", "ten"):
            with self.subTest(invalid=invalid), self.assertRaises(SystemExit):
                RUNNER_MODULE.parser().parse_args([*base, invalid])

    def test_ownership_handoff_is_root_only_and_network_isolated(self) -> None:
        command = RUNNER_MODULE.unprivileged_prepare_command(
            self.image, self.repo, self.work, "demo"
        )
        self.assertEqual(option(command, "--user"), "0:0")
        self.assertEqual(option(command, "--network"), "none")
        self.assertIn("prepare", command)
        self.assertIn("/workspace/work/demo/.ci-result", command)

    def test_unprivileged_workspace_access_exposes_only_selected_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = pathlib.Path(temporary) / "repo"
            selected_package = repo / "packages" / "demo"
            unselected_package = repo / "packages" / "other"
            for directory in (
                repo / "ci",
                repo / "scripts",
                selected_package,
                unselected_package,
                repo / ".git",
                repo / "_state",
                repo / "work",
            ):
                directory.mkdir(parents=True, exist_ok=True)
                directory.chmod(0o700)
            repo.chmod(0o755)
            (repo / "packages").chmod(0o755)
            executable = repo / "scripts" / "build-rpm"
            executable.write_text("#!/bin/sh\n")
            executable.chmod(0o700)
            for path in (
                repo / "ci" / "run-rpmbuild-container.py",
                selected_package / "package.yaml",
                selected_package / "sources.yaml",
                unselected_package / "package.yaml",
                repo / ".git" / "config",
                repo / "_state" / "docker-config.json",
            ):
                path.write_text("{}\n")
                path.chmod(0o600)

            RUNNER_MODULE.grant_unprivileged_workspace_access(repo, "demo")

            self.assertEqual(repo.stat().st_mode & 0o007, 0o001)
            self.assertEqual((repo / "packages").stat().st_mode & 0o007, 0o001)
            self.assertEqual((repo / "work").stat().st_mode & 0o007, 0o001)
            for directory in (repo / "ci", repo / "scripts", selected_package):
                self.assertEqual(directory.stat().st_mode & 0o007, 0o005, directory)
            for path in (
                repo / "ci" / "run-rpmbuild-container.py",
                selected_package / "package.yaml",
                selected_package / "sources.yaml",
            ):
                self.assertEqual(path.stat().st_mode & 0o007, 0o004, path)
            self.assertEqual(executable.stat().st_mode & 0o007, 0o005)
            for path in (
                unselected_package,
                unselected_package / "package.yaml",
                repo / ".git",
                repo / ".git" / "config",
                repo / "_state",
                repo / "_state" / "docker-config.json",
            ):
                self.assertEqual(path.stat().st_mode & 0o007, 0, path)

    def test_unprivileged_workspace_access_rejects_symlinked_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = pathlib.Path(temporary) / "repo"
            (repo / "ci").mkdir(parents=True)
            (repo / "scripts").mkdir()
            (repo / "packages" / "demo").mkdir(parents=True)
            (repo / "work").mkdir()
            protected_directories = (
                repo,
                repo / "ci",
                repo / "scripts",
                repo / "packages",
                repo / "packages" / "demo",
                repo / "work",
            )
            for directory in protected_directories:
                directory.chmod(0o700)
            (repo / "packages" / "demo" / "package.yaml").symlink_to("../demo")

            with self.assertRaisesRegex(RUNNER_MODULE.ContractError, "must not be a symlink"):
                RUNNER_MODULE.grant_unprivileged_workspace_access(repo, "demo")
            for directory in protected_directories:
                self.assertEqual(directory.stat().st_mode & 0o007, 0, directory)

    def test_root_build_exposes_only_workspace_parent_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = pathlib.Path(temporary) / "repo"
            work = repo / "work" / "demo"
            artifacts = repo / "artifacts" / "build"
            package = repo / "packages" / "demo"
            for directory in (
                repo,
                repo / "work",
                work,
                repo / "artifacts",
                artifacts,
                repo / "packages",
                package,
            ):
                directory.mkdir(parents=True, exist_ok=True)
                directory.chmod(0o700)
            (package / "package.yaml").write_text("{}\n")

            arguments = Namespace(
                image=self.image,
                package_id="demo",
                repo_root=str(repo),
                work_dir=str(work),
                artifact_dir=str(artifacts),
                commit_sha=self.commit,
                build_user="root",
                build_timeout_seconds=9981,
            )
            with mock.patch.object(
                RUNNER_MODULE.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 1),
            ):
                self.assertEqual(RUNNER_MODULE.run_mode(arguments), 1)

            self.assertEqual(repo.stat().st_mode & 0o007, 0o001)
            self.assertEqual((repo / "work").stat().st_mode & 0o007, 0o001)
            for directory in (repo / "packages", package, work, artifacts):
                self.assertEqual(directory.stat().st_mode & 0o007, 0, directory)

    def test_handoff_targets_fixed_uid_gid_and_rejects_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary) / "work"
            (root / "SOURCES").mkdir(parents=True)
            (root / "SOURCES" / "source.tar.xz").write_bytes(b"source")
            executable = root / "run-check"
            executable.write_text("#!/bin/sh\n")
            root.chmod(0o700)
            (root / "SOURCES").chmod(0o700)
            (root / "SOURCES" / "source.tar.xz").chmod(0o600)
            executable.chmod(0o700)
            with mock.patch.object(RUNNER_MODULE.os, "chown") as chown:
                count = RUNNER_MODULE.handoff_ownership(root)
            self.assertEqual(count, 4)
            self.assertEqual(chown.call_count, 4)
            for call in chown.call_args_list:
                self.assertEqual(call.args[1:3], (10001, 10001))
                self.assertFalse(call.kwargs["follow_symlinks"])
            self.assertEqual(root.stat().st_mode & 0o007, 0o005)
            self.assertEqual((root / "SOURCES").stat().st_mode & 0o007, 0o005)
            self.assertEqual(
                (root / "SOURCES" / "source.tar.xz").stat().st_mode & 0o007,
                0o004,
            )
            self.assertEqual(executable.stat().st_mode & 0o007, 0o005)

            (root / "unsafe").symlink_to("SOURCES")
            with self.assertRaises(RUNNER_MODULE.ContractError):
                RUNNER_MODULE.ownership_entries(root)

    def test_exec_identity_checks_reject_policy_user_mismatches(self) -> None:
        arguments = Namespace(
            build_user="unprivileged",
            work_dir="/work",
            result_dir="/result",
            identity_output="/result/identity.json",
            command=["scripts/build-rpm"],
        )
        with mock.patch.dict(RUNNER_MODULE.os.environ, {"OE_BUILD_NETWORK": "enabled"}), mock.patch.object(
            RUNNER_MODULE,
            "target_identity",
            return_value=(Namespace(pw_name="rpmbuild"), Namespace()),
        ), mock.patch.object(RUNNER_MODULE.os, "geteuid", return_value=0), mock.patch.object(
            RUNNER_MODULE.os, "getegid", return_value=0
        ):
            with self.assertRaisesRegex(RUNNER_MODULE.ContractError, "must never run as root"):
                RUNNER_MODULE.exec_mode(arguments)

        arguments.build_user = "root"
        with mock.patch.dict(RUNNER_MODULE.os.environ, {"OE_BUILD_NETWORK": "enabled"}), mock.patch.object(RUNNER_MODULE.os, "geteuid", return_value=10001), mock.patch.object(
            RUNNER_MODULE.os, "getegid", return_value=10001
        ):
            with self.assertRaisesRegex(RUNNER_MODULE.ContractError, "UID/GID 0:0"):
                RUNNER_MODULE.exec_mode(arguments)

    def test_exec_identity_rejects_missing_network_policy_marker(self) -> None:
        arguments = Namespace(
            build_user="root",
            work_dir="/work",
            result_dir="/result",
            identity_output="/result/identity.json",
            command=["scripts/build-rpm"],
        )
        with mock.patch.dict(RUNNER_MODULE.os.environ, {}, clear=True), mock.patch.object(
            RUNNER_MODULE.os, "geteuid", return_value=0
        ), mock.patch.object(RUNNER_MODULE.os, "getegid", return_value=0), mock.patch.object(
            RUNNER_MODULE.pwd,
            "getpwuid",
            return_value=Namespace(pw_name="root"),
        ):
            with self.assertRaisesRegex(
                RUNNER_MODULE.ContractError, "network-enabled build policy"
            ):
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
            (repo / "ci").mkdir()
            (repo / "scripts").mkdir()
            (repo / "ci" / "run-rpmbuild-container.py").write_text("#!/usr/bin/env python3\n")
            (repo / "scripts" / "build-rpm").write_text("#!/usr/bin/env python3\n")
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
                build_timeout_seconds=9981,
            )
            with mock.patch.object(
                RUNNER_MODULE.subprocess, "run", side_effect=fake_run
            ):
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

    def test_successful_unprivileged_run_requires_complete_readback_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = pathlib.Path(temporary) / "repo"
            work = repo / "work" / "demo"
            artifacts = repo / "artifacts" / "build"
            package = repo / "packages" / "demo"
            for directory in (
                work,
                artifacts,
                package,
                repo / "ci",
                repo / "scripts",
            ):
                directory.mkdir(parents=True, exist_ok=True)
            (repo / "ci" / "run-rpmbuild-container.py").write_text(
                "#!/usr/bin/env python3\n"
            )
            (repo / "scripts" / "build-rpm").write_text("#!/usr/bin/env python3\n")
            (package / "package.yaml").write_text("{}\n")

            calls = 0

            def fake_run(command, *, check):
                nonlocal calls
                calls += 1
                if calls == 1:
                    (work / ".ci-result" / "ownership-handoff.json").write_text(
                        '{"kind":"rpmbuild-ownership-handoff"}\n'
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
                build_timeout_seconds=9981,
            )
            with mock.patch.object(RUNNER_MODULE.subprocess, "run", side_effect=fake_run):
                with self.assertRaisesRegex(
                    RUNNER_MODULE.ContractError,
                    "successful unprivileged build is missing required evidence",
                ):
                    RUNNER_MODULE.run_mode(arguments)
            self.assertEqual(calls, 2)

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
