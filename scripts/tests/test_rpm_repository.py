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


REPO = Path(__file__).resolve().parents[2]
CLIENT_PATH = REPO / "ci" / "rpm-repo-client.py"
STAGER = REPO / "ci" / "stage-rpm-repository-upload.py"
LIST_PACKAGES = REPO / "ci" / "list-rpm-repo-packages.py"
PUBLISHER_PATH = REPO / "ops" / "rpm-repo-server" / "rpmrepo_publish.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


client = load_module("rpm_repo_client", CLIENT_PATH)
publisher = load_module("rpm_repo_publisher", PUBLISHER_PATH)


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


if __name__ == "__main__":
    unittest.main()
