#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compose the final, commit-bound CI build-result envelope.

The package tools deliberately emit phase results while work is in progress.
This helper is called only after the required package checks have concluded. It
does not turn a skipped phase into success and it fails closed if the exact
commit SHA is unavailable. An immutable OCI digest is mandatory whenever QEMU
was used; a native-only routing result truthfully records that no image ran.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
import tempfile
from typing import Any, Dict, Iterable, Mapping, Optional


PACKAGE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA_RE = re.compile(r"^[a-f0-9]{40}$")
DIGEST_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
WORKFLOW_RESULTS = {"success", "failure", "cancelled", "skipped"}
CLASSIFICATION_MAP = {
    "needs-native-riscv": "needs-native-riscv",
    "qemu-limitation": "qemu-limitation",
    "infrastructure": "infrastructure",
    "dependency": "dependency",
    "spec-packaging": "packaging",
    "riscv-specific": "riscv-source",
    "upstream-build": "test",
    "source-verification": "source-verification",
    "metadata": "metadata",
    "packaging": "packaging",
    "riscv-source": "riscv-source",
    "test": "test",
    "unknown": "unknown",
}
CHECK_NAMES = (
    "metadata-validate",
    "source-verify",
    "rpmbuild-riscv64",
    "rpm-install-smoke",
    "patch-policy",
)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--package-id", required=True)
    result.add_argument("--commit-sha", required=True)
    result.add_argument("--job-id", required=True)
    result.add_argument("--image-lock", default="ci/image.lock")
    result.add_argument("--qemu-version", default="qemu-v9.2.0")
    result.add_argument("--pr-number")
    result.add_argument("--trusted-internal-pr", choices=("true", "false"))
    result.add_argument("--metadata-result", required=True, choices=sorted(WORKFLOW_RESULTS))
    result.add_argument("--source-result", required=True, choices=sorted(WORKFLOW_RESULTS))
    result.add_argument("--patch-result", required=True, choices=sorted(WORKFLOW_RESULTS))
    result.add_argument("--rpmbuild-result", required=True, choices=sorted(WORKFLOW_RESULTS))
    result.add_argument("--smoke-result", required=True, choices=sorted(WORKFLOW_RESULTS))
    result.add_argument("--rpmbuild-phase")
    result.add_argument("--smoke-phase")
    result.add_argument("--failure-classification")
    result.add_argument("--needs-native", action="store_true")
    result.add_argument("--artifact-reference", action="append", default=[])
    result.add_argument("--output", required=True)
    return result


def read_object(path_value: Optional[str]) -> Mapping[str, Any]:
    if not path_value:
        return {}
    path = pathlib.Path(path_value)
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, Mapping) else {}


def image_digest(path: pathlib.Path) -> str:
    if not path.is_file():
        raise ValueError("image lock does not exist: %s" % path)
    value = ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r'^\s*digest:\s*["\']?([^"\'\s#]*)', raw)
        if match:
            value = match.group(1)
            break
    if not DIGEST_RE.fullmatch(value):
        raise ValueError("ci/image.lock has no published immutable sha256 digest")
    return value


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def date_time(value: Any, fallback: str) -> str:
    if not isinstance(value, str) or not value:
        return fallback
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return fallback
    if parsed.tzinfo is None:
        return fallback
    return value


def workflow_check(result: str, evidence: str) -> Dict[str, str]:
    return {
        "status": "passed" if result == "success" else "skipped" if result == "skipped" else "failed",
        "evidence": evidence,
    }


def classification_category(document: Mapping[str, Any]) -> Optional[str]:
    classification = document.get("classification")
    if isinstance(classification, Mapping):
        category = classification.get("category")
        return str(category) if category else None
    if isinstance(classification, str):
        return classification
    return None


def first_failure_message(*documents: Mapping[str, Any]) -> Optional[str]:
    for document in documents:
        failure = document.get("failure")
        if isinstance(failure, Mapping):
            for key in ("first_effective_error", "message"):
                value = failure.get(key)
                if value:
                    return str(value)[:4000]
        for key in ("message", "remediation"):
            value = document.get(key)
            if value:
                return str(value)[:4000]
    return None


def unique_strings(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        item = str(value).strip()
        if item and item not in result:
            result.append(item)
    return result


def validate_final(document: Mapping[str, Any]) -> None:
    """Enforce the final-envelope subset of build-result.schema.json."""
    required = {
        "schema_version",
        "job_id",
        "package_id",
        "commit_sha",
        "status",
        "classification",
        "environment",
        "checks",
        "artifacts",
        "started_at",
        "finished_at",
    }
    allowed = required | {"pr_number", "trusted_internal_pr", "failure_summary", "reproducer"}
    if set(document) - allowed or not required.issubset(document):
        raise ValueError("final build result has missing or unexpected top-level fields")
    if document["schema_version"] != 1 or not str(document["job_id"]):
        raise ValueError("invalid schema version or job id")
    if not PACKAGE_RE.fullmatch(str(document["package_id"])):
        raise ValueError("invalid package id")
    if not SHA_RE.fullmatch(str(document["commit_sha"])):
        raise ValueError("commit SHA must be exactly 40 lowercase hexadecimal characters")
    if document["status"] not in {"passed", "failed", "needs-native-riscv", "qemu-limitation", "cancelled"}:
        raise ValueError("invalid final status")
    if document["classification"] not in {"none", "source-verification", "metadata", "packaging", "riscv-source", "dependency", "infrastructure", "qemu-limitation", "needs-native-riscv", "test", "unknown"}:
        raise ValueError("invalid final classification")
    environment = document["environment"]
    expected_environment = {
        "os": "openEuler",
        "release": "24.03-LTS-SP3",
        "arch": "riscv64",
        "isa": "RVA23",
        "repo_url": "https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/",
    }
    if not isinstance(environment, Mapping) or any(environment.get(key) != value for key, value in expected_environment.items()):
        raise ValueError("target environment does not match the fixed openEuler RVA23 contract")
    if set(environment) != set(expected_environment) | {"image_digest", "qemu_version"}:
        raise ValueError("environment has missing or unexpected fields")
    image = environment.get("image_digest")
    qemu = environment.get("qemu_version")
    if document["status"] == "needs-native-riscv":
        if document["classification"] != "needs-native-riscv":
            raise ValueError("native-only status must use the native-only classification")
        if image is not None or qemu != "not-run-native-policy":
            raise ValueError("native-only routing must not claim a QEMU image execution")
    elif not DIGEST_RE.fullmatch(str(image or "")) or not str(qemu or "") or qemu == "not-run-native-policy":
        raise ValueError("QEMU result is missing the immutable image digest or QEMU version")
    checks = document["checks"]
    if not isinstance(checks, Mapping) or set(checks) != set(CHECK_NAMES):
        raise ValueError("final result must contain exactly the five required package checks")
    for name, check in checks.items():
        if not isinstance(check, Mapping) or set(check) != {"status", "evidence"}:
            raise ValueError("invalid check envelope for %s" % name)
        if check.get("status") not in {"passed", "failed", "skipped", "not-applicable"} or not isinstance(check.get("evidence"), str):
            raise ValueError("invalid check status or evidence for %s" % name)
    if not isinstance(document["artifacts"], list) or len(document["artifacts"]) != len(set(document["artifacts"])):
        raise ValueError("artifacts must be a unique string array")


def atomic_json(path: pathlib.Path, document: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=".%s." % path.name, dir=str(path.parent))
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(document, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    args = parser().parse_args()
    if not PACKAGE_RE.fullmatch(args.package_id):
        raise ValueError("invalid package id")
    if not SHA_RE.fullmatch(args.commit_sha):
        raise ValueError("invalid exact commit SHA")

    phase = read_object(args.rpmbuild_phase)
    smoke = read_object(args.smoke_phase)
    failure = read_object(args.failure_classification)
    now = utc_now()

    checks = {
        "metadata-validate": workflow_check(args.metadata_result, "package-ci metadata artifact"),
        "source-verify": workflow_check(args.source_result, "package-ci verified-source artifact"),
        "patch-policy": workflow_check(args.patch_result, "package-ci patch-policy artifact"),
        "rpmbuild-riscv64": workflow_check(args.rpmbuild_result, "package-ci rpmbuild phase artifact"),
        "rpm-install-smoke": workflow_check(args.smoke_result, "package-ci installation/smoke artifact"),
    }

    category = classification_category(failure)
    if args.needs_native:
        status = "needs-native-riscv"
        classification = "needs-native-riscv"
        checks["rpmbuild-riscv64"] = {"status": "skipped", "evidence": "package metadata requires a native RISC-V runner; QEMU build was not executed"}
        checks["rpm-install-smoke"] = {"status": "skipped", "evidence": "native kernel/hardware validation is unavailable; no synthetic smoke success was recorded"}
    else:
        phase_status = str(phase.get("status") or "")
        smoke_status = str(smoke.get("status") or "")
        if phase_status == "passed":
            checks["rpmbuild-riscv64"]["status"] = "passed"
        elif phase_status:
            checks["rpmbuild-riscv64"]["status"] = "failed"
        if phase_status != "passed":
            checks["rpm-install-smoke"] = {"status": "skipped", "evidence": "install/smoke was not run because rpmbuild did not pass"}
        elif smoke_status == "passed":
            checks["rpm-install-smoke"]["status"] = "passed"
        else:
            checks["rpm-install-smoke"]["status"] = "failed"

        if "cancelled" in {args.metadata_result, args.source_result, args.patch_result, args.rpmbuild_result, args.smoke_result}:
            status = "cancelled"
            classification = "infrastructure"
        elif category == "qemu-limitation":
            status = "qemu-limitation"
            classification = "qemu-limitation"
        elif all(check["status"] == "passed" for check in checks.values()):
            status = "passed"
            classification = "none"
        else:
            status = "failed"
            classification = CLASSIFICATION_MAP.get(category or "", "unknown")
            if classification == "unknown":
                if checks["metadata-validate"]["status"] == "failed":
                    classification = "metadata"
                elif checks["source-verify"]["status"] == "failed":
                    classification = "source-verification"
                elif checks["patch-policy"]["status"] == "failed":
                    classification = "packaging"
                elif not phase:
                    classification = "infrastructure"
                elif not smoke and checks["rpm-install-smoke"]["status"] == "failed":
                    classification = "infrastructure"
                elif checks["rpm-install-smoke"]["status"] == "failed":
                    classification = "test"

    document: Dict[str, Any] = {
        "schema_version": 1,
        "job_id": args.job_id,
        "package_id": args.package_id,
        "commit_sha": args.commit_sha,
        "status": status,
        "classification": classification,
        "environment": {
            "os": "openEuler",
            "release": "24.03-LTS-SP3",
            "arch": "riscv64",
            "isa": "RVA23",
            "repo_url": "https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/",
            "image_digest": None if args.needs_native else image_digest(pathlib.Path(args.image_lock)),
            "qemu_version": "not-run-native-policy" if args.needs_native else args.qemu_version,
        },
        "checks": checks,
        "artifacts": unique_strings(args.artifact_reference),
        "failure_summary": (
            None
            if status == "passed"
            else "Native RISC-V validation is required; no QEMU build was executed."
            if status == "needs-native-riscv"
            else first_failure_message(failure, phase, smoke) or "Required package validation did not pass."
        ),
        "reproducer": None,
        "started_at": date_time(phase.get("started_at"), now),
        "finished_at": now,
    }
    if args.pr_number:
        number = int(args.pr_number)
        if number < 1:
            raise ValueError("PR number must be positive")
        document["pr_number"] = number
    if args.trusted_internal_pr is not None:
        document["trusted_internal_pr"] = args.trusted_internal_pr == "true"

    validate_final(document)
    atomic_json(pathlib.Path(args.output), document)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("compose-build-result: %s" % exc, file=sys.stderr)
        raise SystemExit(2)
