#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate uploaded RPM batches and publish immutable repository generations."""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
from typing import Any


DEFAULT_ROOT = Path("/opt/openeuler-riscv-rpm-repo")
DEFAULT_PUBLIC_BASE_URL = "http://2.27.148.101:38080"
PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
GENERATION = re.compile(
    r"^(?P<package>[a-z0-9]+(?:-[a-z0-9]+)*)-"
    r"(?P<commit>[0-9a-f]{40})-(?P<run>[1-9][0-9]{0,19})-"
    r"(?P<attempt>[1-9][0-9]{0,9})$"
)
RPM_FILENAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9+_.~%-]*\.rpm$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class PublishError(RuntimeError):
    """A batch is invalid and must not become repository content."""


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "LC_ALL": "C"},
    )


def load_ready(batch: Path) -> dict[str, Any]:
    marker = batch / ".ready"
    try:
        marker_mode = marker.lstat().st_mode
    except FileNotFoundError as error:
        raise PublishError("ready marker is missing") from error
    if not stat.S_ISREG(marker_mode) or marker.is_symlink():
        raise PublishError("ready marker must be a regular non-symlink file")
    if marker.stat().st_size > 4 * 1024 * 1024:
        raise PublishError("ready marker exceeds 4 MiB")
    try:
        value = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise PublishError(f"ready marker is not valid UTF-8 JSON: {error}") from error
    if not isinstance(value, dict):
        raise PublishError("ready marker must contain an object")
    return value


def validate_ready(batch: Path, ready: dict[str, Any]) -> list[dict[str, Any]]:
    match = GENERATION.fullmatch(batch.name)
    if not match:
        raise PublishError("batch directory is not a canonical generation id")
    expected_keys = {
        "schema_version",
        "generation",
        "package_id",
        "commit_sha",
        "run_id",
        "run_attempt",
        "artifacts",
    }
    if set(ready) != expected_keys or ready.get("schema_version") != 1:
        raise PublishError("ready marker has missing or unexpected fields")
    package_id = ready.get("package_id")
    commit_sha = ready.get("commit_sha")
    run_id = ready.get("run_id")
    run_attempt = ready.get("run_attempt")
    if not isinstance(package_id, str) or not PACKAGE_ID.fullmatch(package_id):
        raise PublishError("ready marker package_id is invalid")
    if not isinstance(commit_sha, str) or not COMMIT_SHA.fullmatch(commit_sha):
        raise PublishError("ready marker commit_sha is invalid")
    if not isinstance(run_id, int) or isinstance(run_id, bool) or run_id < 1:
        raise PublishError("ready marker run_id is invalid")
    if not isinstance(run_attempt, int) or isinstance(run_attempt, bool) or run_attempt < 1:
        raise PublishError("ready marker run_attempt is invalid")
    if (
        ready.get("generation") != batch.name
        or package_id != match.group("package")
        or commit_sha != match.group("commit")
        or str(run_id) != match.group("run")
        or str(run_attempt) != match.group("attempt")
    ):
        raise PublishError("ready marker does not match its generation directory")
    artifacts = ready.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise PublishError("ready marker has no RPM artifacts")
    names: set[str] = set()
    binary_count = 0
    source_count = 0
    for artifact in artifacts:
        if not isinstance(artifact, dict) or set(artifact) != {"filename", "kind", "sha256", "size"}:
            raise PublishError("artifact record has missing or unexpected fields")
        filename = artifact.get("filename")
        kind = artifact.get("kind")
        checksum = artifact.get("sha256")
        size = artifact.get("size")
        if not isinstance(filename, str) or not RPM_FILENAME.fullmatch(filename) or filename in names:
            raise PublishError("artifact filename is invalid or duplicated")
        if kind not in {"binary", "source"}:
            raise PublishError("artifact kind must be binary or source")
        if not isinstance(checksum, str) or not SHA256.fullmatch(checksum):
            raise PublishError("artifact SHA-256 is invalid")
        if not isinstance(size, int) or isinstance(size, bool) or size < 1:
            raise PublishError("artifact size is invalid")
        names.add(filename)
        binary_count += kind == "binary"
        source_count += kind == "source"
    if binary_count < 1 or source_count < 1:
        raise PublishError("each batch must contain at least one binary RPM and one source RPM")
    actual_entries = {entry.name for entry in batch.iterdir()}
    if actual_entries != names | {".ready"}:
        raise PublishError("batch contents do not exactly match the ready marker")
    return artifacts


def query_rpm(path: Path) -> dict[str, str]:
    if path.is_symlink() or not stat.S_ISREG(path.lstat().st_mode):
        raise PublishError(f"{path.name}: RPM must be a regular non-symlink file")
    try:
        completed = run(
            [
                "rpm",
                "--query",
                "--package",
                "--queryformat",
                "%{NAME}\t%{EPOCHNUM}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{SOURCEPACKAGE}\n",
                str(path),
            ]
        )
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "RPM query failed").strip()
        raise PublishError(f"{path.name}: {detail[:1000]}") from error
    fields = completed.stdout.rstrip("\n").split("\t")
    if len(fields) != 6 or not all(fields):
        raise PublishError(f"{path.name}: RPM query returned an invalid identity")
    name, epoch, version, release, arch, sourcepackage = fields
    if arch not in {"riscv64", "noarch", "src", "nosrc"}:
        raise PublishError(f"{path.name}: unsupported RPM architecture {arch!r}")
    if sourcepackage not in {"1", "(none)"}:
        raise PublishError(f"{path.name}: invalid SOURCEPACKAGE marker {sourcepackage!r}")
    return {
        "name": name,
        "epoch": epoch,
        "version": version,
        "release": release,
        "arch": arch,
        "sourcepackage": sourcepackage,
    }


def validate_artifacts(batch: Path, artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    validated: list[dict[str, Any]] = []
    for artifact in artifacts:
        path = batch / str(artifact["filename"])
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError as error:
            raise PublishError(f"{path.name}: RPM is missing") from error
        if not stat.S_ISREG(mode) or path.is_symlink():
            raise PublishError(f"{path.name}: RPM must be a regular non-symlink file")
        if path.stat().st_size != artifact["size"] or sha256_file(path) != artifact["sha256"]:
            raise PublishError(f"{path.name}: size or SHA-256 does not match the ready marker")
        identity = query_rpm(path)
        # SRPM headers retain the package's build architecture (often noarch or
        # riscv64); SOURCEPACKAGE is RPM's authoritative source-package tag.
        actual_kind = "source" if identity["sourcepackage"] == "1" else "binary"
        if actual_kind != artifact["kind"]:
            raise PublishError(f"{path.name}: ready-marker kind does not match RPM architecture")
        validated.append({**artifact, "path": path, "identity": identity})
    return validated


def install_rpms(root: Path, artifacts: list[dict[str, Any]]) -> None:
    public = root / "public"
    for artifact in artifacts:
        repository = "source" if artifact["kind"] == "source" else "riscv64"
        destination = public / repository / "Packages" / artifact["filename"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if destination.is_symlink() or not destination.is_file():
                raise PublishError(f"{artifact['filename']}: canonical destination is not a regular file")
            if sha256_file(destination) != artifact["sha256"]:
                raise PublishError(
                    f"{artifact['filename']}: immutable filename already exists with different bytes; bump Release"
                )
            continue
        temporary = destination.with_name(f".{destination.name}.{uuid.uuid4().hex}.tmp")
        try:
            shutil.copyfile(artifact["path"], temporary, follow_symlinks=False)
            os.chmod(temporary, 0o644)
            with temporary.open("rb") as stream:
                os.fsync(stream.fileno())
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)


def update_metadata(root: Path, repository: str) -> None:
    repo = root / "public" / repository
    metadata_store = repo / ".metadata"
    metadata_store.mkdir(parents=True, exist_ok=True)
    work = root / "tmp" / f"createrepo-{repository}-{uuid.uuid4().hex}"
    work.mkdir(parents=True)
    try:
        run(["createrepo_c", "--database", "--update", "--outputdir", str(work), str(repo)])
        generated = work / "repodata"
        if not (generated / "repomd.xml").is_file():
            raise PublishError(f"createrepo_c did not generate {repository}/repodata/repomd.xml")
        stored = metadata_store / uuid.uuid4().hex
        os.replace(generated, stored)
        link = repo / f".repodata-{uuid.uuid4().hex}"
        link.symlink_to(Path(".metadata") / stored.name)
        os.replace(link, repo / "repodata")
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "createrepo_c failed").strip()
        raise PublishError(f"{repository}: {detail[-2000:]}") from error
    finally:
        shutil.rmtree(work, ignore_errors=True)


def snapshot_repository(source: Path, destination: Path) -> tuple[int, str]:
    packages = destination / "Packages"
    packages.mkdir(parents=True)
    count = 0
    for rpm_path in sorted((source / "Packages").glob("*.rpm")):
        if rpm_path.is_symlink() or not rpm_path.is_file():
            raise PublishError(f"canonical package is not a regular file: {rpm_path}")
        os.link(rpm_path, packages / rpm_path.name)
        count += 1
    repodata_link = source / "repodata"
    if not repodata_link.is_symlink():
        raise PublishError(f"canonical {source.name}/repodata is not an atomic symlink")
    metadata = repodata_link.resolve(strict=True)
    shutil.copytree(metadata, destination / "repodata", copy_function=shutil.copy2)
    repomd = destination / "repodata" / "repomd.xml"
    return count, sha256_file(repomd)


def build_state(
    generation: str,
    ready: dict[str, Any] | None,
    public_base_url: str,
    repository_evidence: dict[str, tuple[int, str]],
) -> dict[str, Any]:
    base = public_base_url.rstrip("/")
    repositories: dict[str, Any] = {}
    for repository, (count, checksum) in repository_evidence.items():
        repositories[repository] = {
            "baseurl": f"{base}/generations/{generation}/{repository}/",
            "repomd_sha256": checksum,
            "rpm_count": count,
        }
    return {
        "schema_version": 1,
        "generation": generation,
        "published_at": utc_now(),
        "package_id": ready.get("package_id") if ready else None,
        "commit_sha": ready.get("commit_sha") if ready else None,
        "run_id": ready.get("run_id") if ready else None,
        "run_attempt": ready.get("run_attempt") if ready else None,
        "repositories": repositories,
    }


def create_generation(
    root: Path,
    generation: str,
    ready: dict[str, Any] | None,
    public_base_url: str,
) -> dict[str, Any]:
    generations = root / "public" / "generations"
    final = generations / generation
    if final.exists():
        existing = final / "state.json"
        if existing.is_file():
            state = json.loads(existing.read_text(encoding="utf-8"))
            if state.get("generation") == generation:
                return state
        raise PublishError("generation directory already exists without matching state")
    temporary = generations / f".{generation}.{uuid.uuid4().hex}.tmp"
    temporary.mkdir(parents=True)
    try:
        evidence = {
            repository: snapshot_repository(root / "public" / repository, temporary / repository)
            for repository in ("riscv64", "source")
        }
        state = build_state(generation, ready, public_base_url, evidence)
        atomic_json(temporary / "state.json", state)
        os.replace(temporary, final)
        atomic_json(root / "public" / "state.json", state)
        return state
    finally:
        if temporary.exists():
            shutil.rmtree(temporary, ignore_errors=True)


def quarantine(root: Path, batch: Path, reason: str) -> None:
    failed = root / "failed"
    failed.mkdir(parents=True, exist_ok=True)
    destination = failed / f"{batch.name}-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    if destination.exists():
        destination = failed / f"{destination.name}-{uuid.uuid4().hex[:8]}"
    os.replace(batch, destination)
    atomic_json(destination / "failure.json", {"schema_version": 1, "failed_at": utc_now(), "reason": reason})


def ensure_layout(root: Path) -> None:
    for path, mode in (
        (root / "incoming", 0o750),
        (root / "failed", 0o700),
        (root / "tmp", 0o700),
        (root / "public", 0o755),
        (root / "public" / "generations", 0o755),
        (root / "public" / "riscv64" / "Packages", 0o755),
        (root / "public" / "source" / "Packages", 0o755),
    ):
        path.mkdir(parents=True, exist_ok=True)
        os.chmod(path, mode)


def bootstrap(root: Path, public_base_url: str) -> None:
    ensure_layout(root)
    state_path = root / "public" / "state.json"
    if state_path.is_file():
        return
    for repository in ("riscv64", "source"):
        update_metadata(root, repository)
    generation = f"bootstrap-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    create_generation(root, generation, None, public_base_url)


def publish_ready_batches(root: Path, public_base_url: str) -> int:
    ensure_layout(root)
    failures = 0
    for batch in sorted((root / "incoming").iterdir(), key=lambda path: path.name):
        if batch.is_symlink() or not batch.is_dir() or not (batch / ".ready").exists():
            continue
        try:
            ready = load_ready(batch)
            artifacts = validate_ready(batch, ready)
            validated = validate_artifacts(batch, artifacts)
            install_rpms(root, validated)
            for repository in ("riscv64", "source"):
                update_metadata(root, repository)
            create_generation(root, batch.name, ready, public_base_url)
            shutil.rmtree(batch)
            print(f"published {batch.name}")
        except Exception as error:  # Keep the service processing independent ready batches.
            failures += 1
            message = f"{type(error).__name__}: {error}"
            print(f"rejected {batch.name}: {message}", file=sys.stderr)
            try:
                quarantine(root, batch, message)
            except Exception as quarantine_error:
                print(f"failed to quarantine {batch}: {quarantine_error}", file=sys.stderr)
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--public-base-url", default=os.environ.get("RPM_REPO_PUBLIC_BASE_URL", DEFAULT_PUBLIC_BASE_URL))
    parser.add_argument("--bootstrap", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if root == Path("/") or not args.public_base_url.startswith("http://"):
        parser.error("unsafe repository root or public base URL")
    lock_path = Path("/run/lock/openeuler-rpmrepo.lock") if root == DEFAULT_ROOT else root / ".publish.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        if args.bootstrap:
            bootstrap(root, args.public_base_url)
            return 0
        return publish_ready_batches(root, args.public_base_url)


if __name__ == "__main__":
    raise SystemExit(main())
