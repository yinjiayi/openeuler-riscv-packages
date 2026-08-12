# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


REPO = Path(__file__).resolve().parents[2]
CLIENT_PATH = REPO / "ci" / "rpm-repo-client.py"
STAGER = REPO / "ci" / "stage-rpm-repository-upload.py"
LIST_PACKAGES = REPO / "ci" / "list-rpm-repo-packages.py"
BUILDDEPS_PATH = REPO / "ci" / "prepare-build-deps.py"
PUBLISHER_PATH = REPO / "ops" / "rpm-repo-server" / "rpmrepo_publish.py"
BACKFILL_WORKFLOW = REPO / ".github" / "workflows" / "rpm-repo-backfill.yml"
PACKAGE_WORKFLOW = REPO / ".github" / "workflows" / "package-ci.yml"
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
            self.assertEqual({item["package_id"] for item in plan["skipped"]}, {"native", "retired", "golden-success-hello"})


class BackfillWorkflowContractTests(unittest.TestCase):
    def test_backfill_keeps_parallelism_without_overloading_the_single_upstream(self) -> None:
        workflow = BACKFILL_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("max-parallel: 8", workflow)

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


class BuildRequiresRetryTests(unittest.TestCase):
    def test_retry_preserves_the_transaction_and_stops_after_success(self) -> None:
        results = [
            subprocess.CompletedProcess(["dnf"], 1),
            subprocess.CompletedProcess(["dnf"], 92),
            subprocess.CompletedProcess(["dnf"], 0),
        ]
        with mock.patch.object(builddeps.subprocess, "run", side_effect=results) as invoked:
            with mock.patch.object(builddeps.time, "sleep") as sleeper:
                used = builddeps.run_with_retries(["dnf", "install", "gcc"], delays=(0, 0))
        self.assertEqual(used, 3)
        self.assertEqual(invoked.call_count, 3)
        self.assertEqual(sleeper.call_count, 2)

    def test_retry_is_bounded_for_deterministic_failures(self) -> None:
        result = subprocess.CompletedProcess(["dnf"], 1)
        with mock.patch.object(builddeps.subprocess, "run", return_value=result) as invoked:
            with mock.patch.object(builddeps.time, "sleep"):
                with self.assertRaises(subprocess.CalledProcessError):
                    builddeps.run_with_retries(["dnf", "install", "missing"], delays=(0, 0))
        self.assertEqual(invoked.call_count, 3)


if __name__ == "__main__":
    unittest.main()
