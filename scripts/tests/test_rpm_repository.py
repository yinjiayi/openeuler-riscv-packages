# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock


REPO = Path(__file__).resolve().parents[2]
CLIENT_PATH = REPO / "ci" / "rpm-repo-client.py"
STAGER = REPO / "ci" / "stage-rpm-repository-upload.py"
LIST_PACKAGES = REPO / "ci" / "list-rpm-repo-packages.py"
BUILDDEPS_PATH = REPO / "ci" / "prepare-build-deps.py"
RSYNC_RETRY = REPO / "ci" / "rsync-with-lock-retry.sh"
PUBLISHER_PATH = REPO / "ops" / "rpm-repo-server" / "rpmrepo_publish.py"
BACKFILL_WORKFLOW = REPO / ".github" / "workflows" / "rpm-repo-backfill.yml"
PACKAGE_WORKFLOW = REPO / ".github" / "workflows" / "package-ci.yml"
GOLDEN_WORKFLOW = REPO / ".github" / "workflows" / "golden-evaluation.yml"
PERMISSION_LEVEL = {"none": 0, "read": 1, "write": 2}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


client = load_module("rpm_repo_client", CLIENT_PATH)
publisher = load_module("rpm_repo_publisher", PUBLISHER_PATH)
builddeps = load_module("prepare_build_deps", BUILDDEPS_PATH)


def run(argv: list[str], expected: int = 0) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        argv,
        cwd=REPO,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != expected:
        raise AssertionError(
            f"expected {expected}, got {completed.returncode}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed


def permission_blocks(path: Path) -> list[tuple[int, dict[str, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks: list[tuple[int, dict[str, str]]] = []
    for index, line in enumerate(lines):
        stripped = line.lstrip(" ")
        if stripped != "permissions:":
            continue
        indent = len(line) - len(stripped)
        block: dict[str, str] = {}
        for candidate in lines[index + 1:]:
            candidate_stripped = candidate.lstrip(" ")
            candidate_indent = len(candidate) - len(candidate_stripped)
            if candidate_stripped and candidate_indent <= indent:
                break
            if candidate_indent != indent + 2 or ":" not in candidate_stripped:
                continue
            key, value = candidate_stripped.split(":", 1)
            value = value.strip()
            if value in PERMISSION_LEVEL:
                block[key] = value
        blocks.append((indent, block))
    return blocks


class RepositoryClientTests(unittest.TestCase):
    def state(self, generation: str) -> dict[str, object]:
        bootstrap = generation.startswith("bootstrap-")
        return {
            "schema_version": 1,
            "generation": generation,
            "published_at": "2026-08-12T03:00:00Z",
            "package_id": None if bootstrap else "hello",
            "commit_sha": None if bootstrap else "a" * 40,
            "run_id": None if bootstrap else 123,
            "run_attempt": None if bootstrap else 1,
            "repositories": {
                name: {
                    "baseurl": f"{client.PUBLIC_ROOT}/generations/{generation}/{name}/",
                    "repomd_sha256": "b" * 64,
                    "rpm_count": 0 if bootstrap else 2,
                }
                for name in ("riscv64", "source")
            },
        }

    def test_bootstrap_and_package_generations_are_exact(self) -> None:
        bootstrap = self.state("bootstrap-20260812T030000Z")
        normal = self.state(f"hello-{'a' * 40}-123-1")
        self.assertEqual(client.validate_state(bootstrap)["package_id"], None)
        self.assertEqual(client.validate_state(normal)["package_id"], "hello")

    def test_mutable_or_redirected_baseurl_is_rejected(self) -> None:
        state = self.state(f"hello-{'a' * 40}-123-1")
        state["repositories"]["riscv64"]["baseurl"] = f"{client.PUBLIC_ROOT}/riscv64/"
        with self.assertRaisesRegex(ValueError, "immutable expected generation"):
            client.validate_state(state)

    def resolve_args(self, root: Path, allow_unavailable: bool) -> SimpleNamespace:
        return SimpleNamespace(
            state_url=client.STATE_URL,
            repo_file=str(root / "project.repo"),
            output=str(root / "resolution.json"),
            allow_unavailable=allow_unavailable,
        )

    def test_connection_failure_requires_explicit_official_only_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with mock.patch.object(
                client,
                "load_and_verify_state",
                side_effect=client.RepositoryUnavailable("unavailable"),
            ):
                with self.assertRaises(client.RepositoryUnavailable):
                    client.resolve(self.resolve_args(root, False))
                self.assertEqual(client.resolve(self.resolve_args(root, True)), 0)
            resolution = json.loads((root / "resolution.json").read_text(encoding="utf-8"))
            repository = (root / "project.repo").read_text(encoding="utf-8")
            self.assertEqual(resolution["status"], "unavailable")
            self.assertEqual(resolution["reason"], "endpoint-unavailable")
            self.assertEqual(resolution["fallback"]["active_repository_ids"], ["openeuler-rva23"])
            self.assertIsNone(resolution["state_sha256"])
            self.assertIn("enabled=0", repository)
            self.assertIn("skip_if_unavailable=1", repository)

    def test_invalid_or_untrusted_content_never_falls_back(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with mock.patch.object(
                client,
                "load_and_verify_state",
                side_effect=ValueError("repomd.xml does not match state.json"),
            ):
                with self.assertRaisesRegex(ValueError, "does not match"):
                    client.resolve(self.resolve_args(root, True))
            self.assertFalse((root / "resolution.json").exists())
            self.assertFalse((root / "project.repo").exists())

    def test_transient_http_service_errors_are_unavailable_but_client_errors_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transient = client.urllib.error.HTTPError(
                client.STATE_URL, 503, "service unavailable", {}, None
            )
            with mock.patch.object(client, "load_and_verify_state", side_effect=client.RepositoryUnavailable()):
                self.assertEqual(client.resolve(self.resolve_args(root, True)), 0)
            with mock.patch.object(client, "load_and_verify_state", side_effect=ValueError("HTTP 404")):
                with self.assertRaisesRegex(ValueError, "HTTP 404"):
                    client.resolve(self.resolve_args(root, True))
            self.assertIsInstance(transient, client.urllib.error.HTTPError)

    def test_available_generation_remains_checksum_and_url_bound(self) -> None:
        generation = f"hello-{'a' * 40}-123-1"
        state = self.state(generation)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with mock.patch.object(
                client,
                "load_and_verify_state",
                return_value=(state, "c" * 64, {"riscv64": "b" * 64, "source": "b" * 64}),
            ):
                self.assertEqual(client.resolve(self.resolve_args(root, True)), 0)
            resolution = json.loads((root / "resolution.json").read_text(encoding="utf-8"))
            repository = (root / "project.repo").read_text(encoding="utf-8")
            self.assertEqual(resolution["status"], "passed")
            self.assertEqual(resolution["generation"], generation)
            self.assertEqual(resolution["state_sha256"], "c" * 64)
            self.assertIn(state["repositories"]["riscv64"]["baseurl"], repository)
            self.assertIn("enabled=1", repository)


class SupplementalRepositorySelectionTests(unittest.TestCase):
    def test_official_only_fallback_disables_the_supplemental_repository(self) -> None:
        evidence = {
            "kind": "supplemental-repository-resolution",
            "status": "unavailable",
            "state_url": client.STATE_URL,
            "state_sha256": None,
            "generation": None,
            "repositories": {},
            "reason": "endpoint-unavailable",
            "fallback": {
                "active_repository_ids": ["openeuler-rva23"],
                "supplemental_repository_enabled": False,
            },
        }
        available, record = builddeps.validate_supplemental_repository(
            evidence, client.unavailable_repo_text()
        )
        self.assertFalse(available)
        self.assertEqual(record["status"], "unavailable")
        self.assertEqual(record["fallback_repository_ids"], ["openeuler-rva23"])

    def test_tampered_fallback_configuration_is_rejected(self) -> None:
        evidence = {
            "kind": "supplemental-repository-resolution",
            "status": "unavailable",
            "state_url": client.STATE_URL,
            "state_sha256": None,
            "generation": None,
            "repositories": {},
            "reason": "endpoint-unavailable",
            "fallback": {
                "active_repository_ids": ["openeuler-rva23"],
                "supplemental_repository_enabled": False,
            },
        }
        repository = client.unavailable_repo_text().replace("enabled=0", "enabled=1")
        with self.assertRaisesRegex(ValueError, "fallback is invalid"):
            builddeps.validate_supplemental_repository(evidence, repository)

    def test_extra_dnf_repository_setting_is_rejected(self) -> None:
        evidence = {
            "kind": "supplemental-repository-resolution",
            "status": "unavailable",
            "state_url": client.STATE_URL,
            "state_sha256": None,
            "generation": None,
            "repositories": {},
            "reason": "endpoint-unavailable",
            "fallback": {
                "active_repository_ids": ["openeuler-rva23"],
                "supplemental_repository_enabled": False,
            },
        }
        repository = client.unavailable_repo_text() + "proxy=http://example.invalid/\n"
        with self.assertRaisesRegex(ValueError, "unexpected settings"):
            builddeps.validate_supplemental_repository(evidence, repository)

    def test_verified_generation_remains_enabled(self) -> None:
        generation = f"hello-{'a' * 40}-123-1"
        baseurl = f"{client.PUBLIC_ROOT}/generations/{generation}/riscv64/"
        evidence = {
            "kind": "supplemental-repository-resolution",
            "status": "passed",
            "state_url": client.STATE_URL,
            "state_sha256": "c" * 64,
            "generation": generation,
            "repositories": {
                "riscv64": {"baseurl": baseurl, "repomd_sha256": "b" * 64, "rpm_count": 2}
            },
        }
        repository = "\n".join(
            [
                "[openeuler-riscv-project]",
                f"baseurl={baseurl}",
                "enabled=1",
                "gpgcheck=0",
                "repo_gpgcheck=0",
                "name=openEuler RISC-V project packages (immutable generation)",
                "metadata_expire=never",
                "skip_if_unavailable=0",
                "module_hotfixes=1",
                "",
            ]
        )
        available, record = builddeps.validate_supplemental_repository(evidence, repository)
        self.assertTrue(available)
        self.assertEqual(record["repomd_sha256"], "b" * 64)


class UploadStagingTests(unittest.TestCase):
    def test_binary_and_source_rpms_are_flattened_and_checksum_bound(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact = root / "artifact"
            (artifact / "work" / "hello" / "RPMS" / "riscv64").mkdir(parents=True)
            (artifact / "work" / "hello" / "SRPMS").mkdir(parents=True)
            binary = artifact / "work" / "hello" / "RPMS" / "riscv64" / "hello-1-1.riscv64.rpm"
            source = artifact / "work" / "hello" / "SRPMS" / "hello-1-1.src.rpm"
            binary.write_bytes(b"binary-rpm-fixture")
            source.write_bytes(b"source-rpm-fixture")
            output = root / "output"
            commit = "c" * 40
            completed = run(
                [
                    str(STAGER),
                    "--artifact-root", str(artifact),
                    "--output-dir", str(output),
                    "--package-id", "hello",
                    "--commit-sha", commit,
                    "--run-id", "456",
                    "--run-attempt", "2",
                ]
            )
            generation = f"hello-{commit}-456-2"
            self.assertEqual(completed.stdout.strip(), generation)
            ready = json.loads((output / ".ready").read_text(encoding="utf-8"))
            self.assertEqual(ready["generation"], generation)
            self.assertEqual({item["kind"] for item in ready["artifacts"]}, {"binary", "source"})
            expected = hashlib.sha256(b"binary-rpm-fixture").hexdigest()
            binary_record = next(item for item in ready["artifacts"] if item["kind"] == "binary")
            self.assertEqual(binary_record["sha256"], expected)
            self.assertEqual(sorted(path.name for path in (output / "payload").iterdir()), [binary.name, source.name])

    def test_publisher_ready_contract_rejects_unlisted_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            generation = f"hello-{'d' * 40}-789-1"
            batch = root / generation
            batch.mkdir()
            rpm = batch / "hello-1-1.noarch.rpm"
            rpm.write_bytes(b"rpm")
            ready = {
                "schema_version": 1,
                "generation": generation,
                "package_id": "hello",
                "commit_sha": "d" * 40,
                "run_id": 789,
                "run_attempt": 1,
                "artifacts": [
                    {
                        "filename": rpm.name,
                        "kind": "binary",
                        "sha256": hashlib.sha256(b"rpm").hexdigest(),
                        "size": 3,
                    },
                    {
                        "filename": "hello-1-1.src.rpm",
                        "kind": "source",
                        "sha256": hashlib.sha256(b"src").hexdigest(),
                        "size": 3,
                    },
                ],
            }
            (batch / "hello-1-1.src.rpm").write_bytes(b"src")
            (batch / ".ready").write_text(json.dumps(ready), encoding="utf-8")
            self.assertEqual(len(publisher.validate_ready(batch, ready)), 2)
            (batch / "extra.txt").write_text("extra", encoding="utf-8")
            with self.assertRaisesRegex(publisher.PublishError, "exactly match"):
                publisher.validate_ready(batch, ready)

    def test_source_rpm_uses_sourcepackage_tag_instead_of_build_arch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "hello-1-1.src.rpm"
            source.write_bytes(b"source-rpm-fixture")
            completed = subprocess.CompletedProcess(
                ["rpm"],
                0,
                stdout="hello\t0\t1\t1\tnoarch\t1\n",
                stderr="",
            )
            with mock.patch.object(publisher, "run", return_value=completed):
                identity = publisher.query_rpm(source)
            self.assertEqual(identity["arch"], "noarch")
            self.assertEqual(identity["sourcepackage"], "1")

    def test_binary_noarch_rpm_is_not_mistaken_for_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            binary = Path(temporary) / "hello-1-1.noarch.rpm"
            binary.write_bytes(b"binary-rpm-fixture")
            completed = subprocess.CompletedProcess(
                ["rpm"],
                0,
                stdout="hello\t0\t1\t1\tnoarch\t(none)\n",
                stderr="",
            )
            with mock.patch.object(publisher, "run", return_value=completed):
                identity = publisher.query_rpm(binary)
            self.assertEqual(identity["arch"], "noarch")
            self.assertEqual(identity["sourcepackage"], "(none)")


class BackfillPlanTests(unittest.TestCase):
    def test_native_retired_and_golden_packages_are_recorded_as_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packages = root / "packages"
            fixtures = {
                "active": {"build": {"profile": "qemu-user"}, "maintenance": {"status": "active"}},
                "native": {"build": {"profile": "needs-native-riscv"}, "maintenance": {"status": "active"}},
                "retired": {"build": {"profile": "qemu-user"}, "maintenance": {"status": "retired"}},
                "golden-success-hello": {"build": {"profile": "qemu-user"}, "maintenance": {"status": "active"}},
            }
            for package_id, value in fixtures.items():
                directory = packages / package_id
                directory.mkdir(parents=True)
                (directory / "package.yaml").write_text(json.dumps(value), encoding="utf-8")
            output = root / "plan.json"
            run([str(LIST_PACKAGES), "--packages-dir", str(packages), "--output", str(output)])
            plan = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(plan["packages"], ["active"])
            self.assertEqual(plan["shards"], [
                {"index": 0, "package_count": 1, "packages": ["active"]},
                {"index": 1, "package_count": 0, "packages": []},
            ])
            self.assertEqual(plan["max_parallel_per_shard"], 25)
            self.assertEqual({item["package_id"] for item in plan["skipped"]}, {"native", "retired", "golden-success-hello"})

    def test_more_than_one_matrix_is_split_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packages = root / "packages"
            expected = [f"pkg-{index:03d}" for index in range(257)]
            for package_id in expected:
                directory = packages / package_id
                directory.mkdir(parents=True)
                (directory / "package.yaml").write_text(
                    json.dumps({"build": {"profile": "qemu-user"}, "maintenance": {"status": "active"}}),
                    encoding="utf-8",
                )
            output = root / "plan.json"
            github_output = root / "github-output"
            run([
                str(LIST_PACKAGES),
                "--packages-dir", str(packages),
                "--output", str(output),
                "--github-output", str(github_output),
                "--max-concurrency", "50",
            ])
            plan = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual([shard["package_count"] for shard in plan["shards"]], [129, 128])
            self.assertEqual(plan["shards"][0]["packages"], expected[0::2])
            self.assertEqual(plan["shards"][1]["packages"], expected[1::2])
            self.assertEqual(plan["max_parallel_per_shard"], 25)
            values = dict(line.split("=", 1) for line in github_output.read_text(encoding="utf-8").splitlines())
            self.assertEqual(json.loads(values["packages_0"]), expected[0::2])
            self.assertEqual(json.loads(values["packages_1"]), expected[1::2])
            self.assertEqual(values["package_count"], "257")
            self.assertEqual(values["max_parallel_per_shard"], "25")


class BackfillWorkflowContractTests(unittest.TestCase):
    def test_backfill_splits_fifty_self_hosted_workers_across_two_matrices(self) -> None:
        workflow = BACKFILL_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(
            "--max-concurrency \"${{ vars.RPM_BACKFILL_MAX_CONCURRENCY || '50' }}\"",
            workflow,
        )
        self.assertEqual(
            workflow.count("max-parallel: ${{ fromJSON(needs.plan.outputs.max_parallel_per_shard) }}"),
            2,
        )
        self.assertIn("package_id: ${{ fromJSON(needs.plan.outputs.packages_0) }}", workflow)
        self.assertIn("package_id: ${{ fromJSON(needs.plan.outputs.packages_1) }}", workflow)
        package_workflow = PACKAGE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(
            "$GITHUB_REPOSITORY/.github/workflows/rpm-repo-backfill.yml@refs/heads/main",
            package_workflow,
        )

    def test_caller_permission_ceiling_covers_reusable_workflow_jobs(self) -> None:
        caller_blocks = permission_blocks(BACKFILL_WORKFLOW)
        caller = next(block for indent, block in caller_blocks if indent == 0)
        required: dict[str, str] = {}
        for _, block in permission_blocks(PACKAGE_WORKFLOW):
            for key, value in block.items():
                current = required.get(key, "none")
                if PERMISSION_LEVEL[value] > PERMISSION_LEVEL[current]:
                    required[key] = value
        insufficient = {
            key: {"caller": caller.get(key, "none"), "required": value}
            for key, value in required.items()
            if PERMISSION_LEVEL[caller.get(key, "none")] < PERMISSION_LEVEL[value]
        }
        self.assertEqual(insufficient, {})

    def test_package_and_golden_workflows_propagate_official_only_evidence(self) -> None:
        for path in (PACKAGE_WORKFLOW, GOLDEN_WORKFLOW):
            workflow = path.read_text(encoding="utf-8")
            self.assertIn("--allow-unavailable", workflow)
            self.assertTrue(
                "artifacts/repository/resolution.json" in workflow
                or "repository-resolution.json" in workflow
            )
            self.assertIn("ci/install-smoke.sh", workflow)

    def test_golden_dependency_preparation_uses_the_package_build_identity(self) -> None:
        workflow = GOLDEN_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("BUILD_USER: ${{ steps.policy.outputs.build_user }}", workflow)
        self.assertIn('--build-user "$BUILD_USER"', workflow)

    def test_heavy_dependency_preparation_has_a_bounded_one_hour_window(self) -> None:
        for path in (PACKAGE_WORKFLOW, GOLDEN_WORKFLOW):
            workflow = path.read_text(encoding="utf-8")
            self.assertIn(
                "--max-bytes 52428800 --timeout-seconds 3600 --",
                workflow,
            )
            self.assertNotIn(
                "--max-bytes 52428800 --timeout-seconds 1800 --",
                workflow,
            )


class RrsyncLockRetryTests(unittest.TestCase):
    def fake_command(self, root: Path) -> tuple[Path, Path]:
        counter = root / "counter"
        counter.write_text("0\n", encoding="utf-8")
        command = root / "fake-rrsync"
        command.write_text(
            "#!/bin/sh\n"
            'count=$(cat "$COUNT_FILE")\n'
            'count=$((count + 1))\n'
            'printf "%s\\n" "$count" >"$COUNT_FILE"\n'
            'if [ "$count" -le "$FAILURES" ]; then\n'
            '  printf "%s\\n" "$FAILURE_MESSAGE" >&2\n'
            '  exit "$FAILURE_RESULT"\n'
            "fi\n"
            "exit 0\n",
            encoding="utf-8",
        )
        command.chmod(0o755)
        return command, counter

    def invoke(
        self,
        command: Path,
        counter: Path,
        failures: int,
        result: int,
        message: str,
    ) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment.update(
            {
                "COUNT_FILE": str(counter),
                "FAILURES": str(failures),
                "FAILURE_RESULT": str(result),
                "FAILURE_MESSAGE": message,
                "RRSYNC_LOCK_MAX_ATTEMPTS": "4",
                "RRSYNC_LOCK_BASE_DELAY_SECONDS": "0",
                "RRSYNC_LOCK_JITTER_MAX_SECONDS": "0",
                "RRSYNC_LOCK_JITTER_KEY": "123:demo",
            }
        )
        return subprocess.run(
            [str(RSYNC_RETRY), "--", str(command)],
            cwd=REPO,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def test_exact_rrsync_lock_code_retries_then_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            command, counter = self.fake_command(Path(temporary))
            completed = self.invoke(
                command,
                counter,
                2,
                12,
                "rrsync error: Another instance of rrsync is already accessing this directory.",
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(counter.read_text(encoding="utf-8").strip(), "3")

    def test_other_code_12_failure_is_not_retried(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            command, counter = self.fake_command(Path(temporary))
            completed = self.invoke(command, counter, 3, 12, "rsync authentication failed")
            self.assertEqual(completed.returncode, 12)
            self.assertEqual(counter.read_text(encoding="utf-8").strip(), "1")

    def test_lock_text_with_other_exit_code_is_not_retried(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            command, counter = self.fake_command(Path(temporary))
            completed = self.invoke(
                command,
                counter,
                3,
                23,
                "rrsync error: Another instance of rrsync is already accessing this directory.",
            )
            self.assertEqual(completed.returncode, 23)
            self.assertEqual(counter.read_text(encoding="utf-8").strip(), "1")

    def test_workflow_jitter_key_is_distinct_for_each_package(self) -> None:
        workflow = PACKAGE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(
            "RRSYNC_LOCK_JITTER_KEY: ${{ format('{0}:{1}', github.run_id, needs.prepare.outputs.package_id) }}",
            workflow,
        )
        self.assertNotIn("RRSYNC_LOCK_JITTER_SEED: ${{ github.run_id }}", workflow)


class BuildRequiresRetryTests(unittest.TestCase):
    def test_buildrequires_uses_the_container_local_bounded_runner(self) -> None:
        source = BUILDDEPS_PATH.read_text(encoding="utf-8")
        self.assertIn('DNF_ATTEMPT_TIMEOUTS_SECONDS = "2100,1100"', source)
        self.assertIn("DNF_TRANSACTION_BUDGET_SECONDS = 3300", source)
        self.assertIn("DNF_KILL_AFTER_SECONDS = 10", source)
        self.assertIn("dst={DNF_TRANSACTION_CONTAINER_PATH},readonly", source)
        self.assertIn('"dependency_install_transaction"', source)
        self.assertNotIn("run_with_retries", source)


if __name__ == "__main__":
    unittest.main()
