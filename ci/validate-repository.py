#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Static, dependency-free validation for CI policy and workflow wiring."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ACTION_REF = re.compile(r"(?m)^\s*uses:\s*([^#\s]+)")
PINNED_ACTION = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def lock_value(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*\"?([^\"\n]*)\"?\s*$", text)
    return match.group(1).strip() if match else ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output")
    parser.add_argument("--require-published-image", action="store_true")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    expected = {
        "package-ci.yml",
        "daily-update-check.yml",
        "build-ci-image.yml",
        "catalog-discovery.yml",
        "dashboard.yml",
        "auto-merge.yml",
        "golden-evaluation.yml",
        "update-schedule-monitor.yml",
    }
    workflows = root / ".github" / "workflows"
    present = {path.name for path in workflows.glob("*.yml")}
    missing = sorted(expected - present)
    if missing:
        errors.append("missing workflow(s): " + ", ".join(missing))

    forbidden = {
        "OPENAI_API_KEY": "Actions must not hold OpenAI credentials",
        "pull_request_target": "write-capable pull_request_target is forbidden",
        "runs-on: self-hosted": "self-hosted RISC-V runners are not enabled in M0/M1",
        "ubuntu-latest": "runner images must use an explicit version",
        "secrets.": "custom Actions secrets are outside this repository's CI design",
    }
    for workflow in sorted(workflows.glob("*.yml")):
        text = workflow.read_text(encoding="utf-8")
        for needle, reason in forbidden.items():
            if needle in text:
                errors.append(f"{workflow.name}: {reason} ({needle})")
        for action in ACTION_REF.findall(text):
            if action.startswith("./"):
                continue
            if not PINNED_ACTION.fullmatch(action):
                errors.append(f"{workflow.name}: action is not pinned to a full commit: {action}")
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if "actions/upload-artifact@" in line or "actions/upload-pages-artifact@" in line:
                block = "\n".join(lines[index : index + 14])
                if not re.search(r"retention-days:\s*7\b", block):
                    errors.append(f"{workflow.name}:{index + 1}: artifact retention is not explicitly 7 days")

    package_ci = (workflows / "package-ci.yml").read_text(encoding="utf-8") if (workflows / "package-ci.yml").exists() else ""
    for event in ("opened", "synchronize", "reopened", "merge_group", "workflow_dispatch"):
        if event not in package_ci:
            errors.append(f"package-ci.yml does not visibly support {event}")
    if "inputs.base_sha" not in package_ci or "github.sha" not in package_ci:
        errors.append("package-ci.yml cannot validate a trusted bot-created PR head via workflow_dispatch")
    for check in ("metadata-validate", "source-verify", "rpmbuild-riscv64", "rpm-install-smoke", "patch-policy", "merge-policy"):
        if not re.search(rf"(?m)^  {re.escape(check)}:\s*$", package_ci):
            errors.append(f"package-ci.yml is missing required check job {check}")
    if "ci/compose-build-result.py" not in package_ci:
        errors.append("package-ci.yml does not compose a final commit-bound build result")
    if "issues: write\n      pull-requests: write" not in package_ci:
        errors.append("record-ci-state cannot label trusted PRs with its job-scoped token")
    if re.search(r"--result\s+[^\n]*build-result\.json", package_ci):
        errors.append("package-ci.yml writes a phase result directly to build-result.json")

    image_workflow = (workflows / "build-ci-image.yml").read_text(encoding="utf-8") if (workflows / "build-ci-image.yml").exists() else ""
    if "--method PATCH" in image_workflow and "/user/packages/container/" in image_workflow:
        errors.append("build-ci-image.yml must verify public GHCR state, not attempt a user-level visibility mutation")
    if "ci/dispatch-required-checks.sh" not in image_workflow or "statuses: write" not in image_workflow:
        errors.append("digest-lock PR creation does not bridge actual required jobs onto the bot-created PR head")
    if "git ls-remote --exit-code --heads" not in image_workflow or "test \"$changed\" = ci/image.lock" not in image_workflow:
        errors.append("digest-lock retry does not safely verify and reuse an existing lock branch")
    if "git merge --no-edit origin/main" not in image_workflow:
        errors.append("digest-lock retry does not update the reused branch to the latest protected main")

    settings_path = root / ".github" / "repository-settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8")) if settings_path.exists() else {}
    actions_settings = settings.get("actions", {})
    if actions_settings.get("default_workflow_permissions") != "read":
        errors.append("default GITHUB_TOKEN permissions must remain read-only")
    if actions_settings.get("can_approve_pull_request_reviews") is not True:
        errors.append("Actions cannot create the reviewed digest-lock PR")

    discovery = (workflows / "catalog-discovery.yml").read_text(encoding="utf-8") if (workflows / "catalog-discovery.yml").exists() else ""
    if "scripts/snapshot-catalog" not in discovery or "scripts/discover-packages" not in discovery:
        errors.append("catalog-discovery.yml must normalize live metadata before candidate discovery")
    if re.search(r"discover-packages[\s\S]{0,1500}--input\s+[^\n]*(?:\.db|repomd\.xml|Release|json\.gz)", discovery):
        errors.append("discover-packages must not consume raw distribution databases or indexes directly")
    if "ci/dispatch-required-checks.sh" not in discovery or "statuses: write" not in discovery:
        errors.append("catalog snapshot PRs cannot satisfy protected checks after GITHUB_TOKEN event suppression")

    check_bridge = root / "ci" / "dispatch-required-checks.sh"
    if not check_bridge.is_file() or not check_bridge.stat().st_mode & 0o111:
        errors.append("bot-created PR check bridge is missing or not executable")

    daily = (workflows / "daily-update-check.yml").read_text(encoding="utf-8") if (workflows / "daily-update-check.yml").exists() else ""
    if "--state-output artifacts/state/update-state.json" not in daily:
        errors.append("daily update aggregation does not persist per-package success timestamps")

    golden = (workflows / "golden-evaluation.yml").read_text(encoding="utf-8") if (workflows / "golden-evaluation.yml").exists() else ""
    for package_id in ("golden-success-hello", "golden-riscv-inline-asm", "golden-needs-native-kmod"):
        if package_id not in golden:
            errors.append(f"golden-evaluation.yml is missing {package_id}")
    if "--stage auto" not in golden:
        errors.append("golden-evaluation.yml does not use stage-aware golden assertions")

    builddeps_path = root / "ci" / "prepare-build-deps.py"
    builddeps = builddeps_path.read_text(encoding="utf-8") if builddeps_path.exists() else ""
    if ":/workspace:ro" not in builddeps:
        errors.append("BuildRequires planning must mount the reviewed repository read-only")
    if ":/workspace/artifacts/" in builddeps:
        errors.append("BuildRequires evidence cannot be nested beneath the read-only /workspace mount")
    if ":/evidence:rw" not in builddeps or '"/evidence/' not in builddeps:
        errors.append("BuildRequires planning is missing its dedicated writable /evidence mount")

    all_workflow_text = "\n".join(path.read_text(encoding="utf-8") for path in workflows.glob("*.yml"))
    exact_repo = "https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/"
    if exact_repo not in (root / "ci" / "openeuler-rva23.repo").read_text(encoding="utf-8"):
        errors.append("approved openEuler RVA23 repository is not fixed in ci/openeuler-rva23.repo")
    if "17 18 * * *" not in all_workflow_text:
        errors.append("daily 02:17 Asia/Shanghai schedule (18:17 UTC) is missing")

    lock = (root / "ci" / "image.lock").read_text(encoding="utf-8")
    digest = lock_value(lock, "digest")
    if not DIGEST.fullmatch(digest):
        message = "ci/image.lock has no verified published-image digest; package builds fail closed until build-ci-image completes"
        if args.require_published_image:
            errors.append(message)
        else:
            warnings.append(message)

    result = {
        "schema_version": 1,
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "warnings": warnings,
        "workflow_count": len(present),
        "published_image_locked": bool(DIGEST.fullmatch(digest)),
    }
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
