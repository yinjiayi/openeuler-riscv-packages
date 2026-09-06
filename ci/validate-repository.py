#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Static, dependency-free validation for CI policy and workflow wiring."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ACTION_REF = re.compile(r"(?m)^\s*uses:\s*([^#\s]+)")
PINNED_ACTION = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
GITHUB_TOKEN_LITERALS = (
    re.compile(rb"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
)


def contains_github_token_literal(content: bytes) -> bool:
    return any(pattern.search(content) for pattern in GITHUB_TOKEN_LITERALS)


def tracked_paths(root: Path) -> list[Path]:
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode == 0:
        return [root / value.decode("utf-8", "surrogateescape") for value in completed.stdout.split(b"\0") if value]
    return [path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts]


def committed_token_paths(root: Path) -> list[str]:
    result: list[str] = []
    for path in tracked_paths(root):
        if not path.is_file():
            continue
        try:
            content = path.read_bytes()
        except OSError:
            continue
        if contains_github_token_literal(content):
            result.append(str(path.relative_to(root)))
    return sorted(result)


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

    for path in committed_token_paths(root):
        errors.append(f"{path}: GitHub token-like credential is forbidden in repository content")

    expected = {
        "package-ci.yml",
        "daily-update-check.yml",
        "build-ci-image.yml",
        "catalog-discovery.yml",
        "dashboard.yml",
        "auto-merge.yml",
        "golden-evaluation.yml",
        "update-schedule-monitor.yml",
        "rpm-repo-backfill.yml",
    }
    workflows = root / ".github" / "workflows"
    present = {path.name for path in workflows.glob("*.yml")}
    missing = sorted(expected - present)
    if missing:
        errors.append("missing workflow(s): " + ", ".join(missing))

    manifest_helper_path = root / "ci" / "rpm-manifest.sh"
    finalizer_path = root / "ci" / "finalize-target-rpmdb.sh"
    bootstrap_path = root / "ci" / "bootstrap-rootfs.sh"
    verify_target_path = root / "ci" / "verify-target.sh"
    containerfile_path = root / "ci" / "Containerfile.riscv64"
    image_workflow_path = workflows / "build-ci-image.yml"
    baseline_files = (
        manifest_helper_path,
        finalizer_path,
        bootstrap_path,
        verify_target_path,
        containerfile_path,
        image_workflow_path,
    )
    if any(not path.is_file() for path in baseline_files):
        errors.append("trusted RPM baseline implementation is incomplete")
    else:
        manifest_helper = manifest_helper_path.read_text(encoding="utf-8")
        finalizer = finalizer_path.read_text(encoding="utf-8")
        bootstrap = bootstrap_path.read_text(encoding="utf-8")
        verify_target = verify_target_path.read_text(encoding="utf-8")
        containerfile = containerfile_path.read_text(encoding="utf-8")
        image_workflow = image_workflow_path.read_text(encoding="utf-8")
        bootstrap_repository = (root / "ci" / "openeuler-rva23.repo").read_text(
            encoding="utf-8"
        )
        if (
            not manifest_helper_path.stat().st_mode & 0o111
            or "%{SHA1HEADER}" not in manifest_helper
            or "%{SHA256HEADER}" not in manifest_helper
            or "NF != 5" not in manifest_helper
            or "length($4) != 40" not in manifest_helper
            or "length($5) != 64" not in manifest_helper
        ):
            errors.append("shared target RPM manifest helper is missing its executable exact query contract")
        if "rpm --root \"$rootfs\" --eval '%{_dbpath}'" not in bootstrap:
            errors.append("bootstrap rootfs does not record its RPM-evaluated database path")
        for marker in (
            'rpmdb --root "$rootfs" --verifydb',
            'rpmdb --root "$rootfs" --exportdb',
            'rpmdb --dbpath "$roundtrip_db" --importdb',
            'rpmdb --dbpath "$roundtrip_db" --exportdb',
            'cmp -s /evidence/rpmdb-header-list.bin /evidence/rpmdb-header-list-roundtrip.bin',
        ):
            if marker not in bootstrap:
                errors.append(f"bootstrap RPM database transport is missing: {marker}")
        transaction_marker = "dnf -y"
        export_marker = 'rpmdb --root "$rootfs" --exportdb'
        if (
            "gpgcheck=1" not in bootstrap_repository
            or "gpgkey=file://" not in bootstrap_repository
            or transaction_marker not in bootstrap
            or export_marker not in bootstrap
            or (
                transaction_marker in bootstrap
                and export_marker in bootstrap
                and bootstrap.index(transaction_marker) > bootstrap.index(export_marker)
            )
        ):
            errors.append(
                "portable RPM database export must follow the gpgchecked dependency-resolved DNF transaction"
            )
        for marker in (
            "rpm --eval '%{_dbpath}'",
            'sha256sum --check',
            'rpmdb --dbpath "$staging_db" --importdb',
            'rpmdb --dbpath "$staging_db" --verifydb',
            "the target runtime rpmdb path is unexpectedly nonempty",
            'stat -c \'%d\' -- "$staging_db"',
            'rmdir "$runtime_db"',
            'mv -- "$staging_db" "$runtime_db"',
            'cmp -s -- "$baseline_root/rpm-manifest.tsv" "$runtime_manifest"',
            "rpmdb --verifydb",
            "validate_db_path 'bootstrap rpmdb path'",
            "validate_db_path 'target runtime rpmdb path'",
            "validate_db_path 'target staging rpmdb path'",
        ):
            if marker not in finalizer:
                errors.append(f"target RPM database finalizer is missing: {marker}")
        if 'cmp -s -- "$transport" "$target_export"' in finalizer:
            errors.append("target finalizer requires non-canonical cross-version header-stream bytes")
        for forbidden_marker in (
            "ln -s",
            "/var/lib/rpm",
            "/usr/lib/sysimage/rpm",
            "--initdb",
            "--justdb",
            "--nodeps",
            "--nosignature",
            'find "$runtime_db" -mindepth 1 -delete',
            'cp -a -- "$staging_db/." "$runtime_db/"',
        ):
            if forbidden_marker in finalizer:
                errors.append(
                    "target RPM database finalizer guesses a path or bypasses the transport contract: "
                    + forbidden_marker
                )
        for marker in (
            '[[ -s $live_manifest ]]',
            "bash rpm rpm-build gcc gcc-c++ make python3",
            'cmp -s -- "$manifest" "$live_manifest"',
        ):
            if marker not in verify_target:
                errors.append(f"target verification is missing the live RPM baseline gate: {marker}")
        finalizer_run = "&& /usr/local/libexec/openeuler-riscv-ci/finalize-target-rpmdb.sh"
        target_verify_run = "&& /usr/local/bin/verify-target"
        if (
            finalizer_run not in containerfile
            or target_verify_run not in containerfile
            or containerfile.index(finalizer_run) > containerfile.index(target_verify_run)
        ):
            errors.append("target RPM database finalization must precede target verification")
        for name in ("ci/finalize-target-rpmdb.sh", "ci/rpm-manifest.sh"):
            if image_workflow.count(f"- {name}") < 2 or f"sha256sum {name}" not in image_workflow:
                errors.append(f"CI image workflow does not trigger on and record {name}")
        if (
            "artifacts/image/rpm-manifest-live.tsv" not in image_workflow
            or "cmp -s artifacts/image/rpm-manifest.tsv artifacts/image/rpm-manifest-live.tsv"
            not in image_workflow
        ):
            errors.append("CI image workflow does not retain and compare the live target RPM manifest")

    forbidden = {
        "OPENAI_API_KEY": "Actions must not hold OpenAI credentials",
        "pull_request_target": "write-capable pull_request_target is forbidden",
        "ubuntu-latest": "runner images must use an explicit version",
    }
    for workflow in sorted(workflows.glob("*.yml")):
        text = workflow.read_text(encoding="utf-8")
        for needle, reason in forbidden.items():
            if needle in text:
                errors.append(f"{workflow.name}: {reason} ({needle})")
        for secret_name in re.findall(r"secrets\.([A-Za-z_][A-Za-z0-9_]*)", text):
            if secret_name != "RPM_REPO_SSH_PRIVATE_KEY":
                errors.append(f"{workflow.name}: unapproved Actions secret {secret_name}")
            elif workflow.name not in {"package-ci.yml", "rpm-repo-backfill.yml"}:
                errors.append(f"{workflow.name}: RPM repository deploy key is outside its approved workflows")
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
    auto_merge = (workflows / "auto-merge.yml").read_text(encoding="utf-8") if (workflows / "auto-merge.yml").exists() else ""
    ruleset_path = root / ".github" / "rulesets" / "main.json"
    ruleset = json.loads(ruleset_path.read_text(encoding="utf-8")) if ruleset_path.exists() else {}
    auto_merge_policy_path = root / "ci" / "evaluate-auto-merge.py"
    auto_merge_state_proof_path = root / "ci" / "prove-auto-merge-state.py"
    default_branch_head_proof_path = root / "ci" / "prove-default-branch-head.py"
    required_context_activation_path = root / "ci" / "prove-required-context-active.py"
    auto_merge_events = (
        "types: [opened, reopened, synchronize, ready_for_review, "
        "converted_to_draft, edited, labeled, unlabeled]"
    )
    if auto_merge_events not in auto_merge:
        errors.append("auto-merge workflow does not re-evaluate converted_to_draft and edited events")
    if "branches: [main]" in auto_merge:
        errors.append("auto-merge workflow must receive retarget events so it can disarm non-default-branch PRs")
    if not re.search(r"(?m)^  configure:\s*\n    if:", auto_merge):
        errors.append("auto-merge workflow does not preserve the established configure job context")
    required_contexts: list[str] = []
    for rule in ruleset.get("rules", []):
        if rule.get("type") == "required_status_checks":
            required_contexts.extend(
                check.get("context", "")
                for check in rule.get("parameters", {}).get("required_status_checks", [])
            )
    if required_contexts.count("configure") != 1:
        errors.append("main ruleset must require exactly one established Auto Merge Policy configure context")
    required_integrations = [
        check.get("integration_id")
        for rule in ruleset.get("rules", [])
        if rule.get("type") == "required_status_checks"
        for check in rule.get("parameters", {}).get("required_status_checks", [])
    ]
    if required_integrations != [15368] * len(required_contexts):
        errors.append("every required status check must be pinned to the GitHub Actions integration")
    required_rules = [rule for rule in ruleset.get("rules", []) if rule.get("type") == "required_status_checks"]
    if len(required_rules) != 1 or required_rules[0].get("parameters", {}).get(
        "strict_required_status_checks_policy"
    ) is not True:
        errors.append("required status checks must keep every pull request up to date with main")
    if not auto_merge_policy_path.is_file() or not auto_merge_policy_path.stat().st_mode & 0o111:
        errors.append("fail-closed auto-merge scope policy is missing or not executable")
    else:
        auto_merge_policy = auto_merge_policy_path.read_text(encoding="utf-8")
        for marker in (
            'BLOCKING_LABELS = {',
            'changed file is outside a package directory',
            'automatic merge requires exactly one package directory',
            'pull request file list is incomplete',
            'pull request head changed after the workflow event',
        ):
            if marker not in auto_merge_policy:
                errors.append(f"auto-merge scope policy is missing fail-closed marker: {marker}")
    if (
        not auto_merge_state_proof_path.is_file()
        or not auto_merge_state_proof_path.stat().st_mode & 0o111
    ):
        errors.append("fail-closed Auto-merge state proof is missing or not executable")
    else:
        auto_merge_state_proof = auto_merge_state_proof_path.read_text(encoding="utf-8")
        for marker in (
            'pull_request.get("state") != "open"',
            'pull_request.get("merged") is not False',
            'pull_request.get("merged_at") is not None',
            'nested(pull_request, "head", "repo", "full_name") != repository',
            'nested(pull_request, "base", "repo", "full_name") != repository',
            'nested(pull_request, "head", "sha") != event_head',
            'nested(pull_request, "base", "sha") != event_base',
            'nested(pull_request, "base", "ref") != event_base_ref',
            'expected_auto_merge == "disabled" and auto_merge is not None',
            'enabled = mapping(auto_merge, "pull request auto_merge")',
            'enabled.get("merge_method") != "squash"',
        ):
            if marker not in auto_merge_state_proof:
                errors.append(f"Auto-merge state proof is missing fail-closed marker: {marker}")
    if (
        not default_branch_head_proof_path.is_file()
        or not default_branch_head_proof_path.stat().st_mode & 0o111
    ):
        errors.append("fail-closed default-branch freshness proof is missing or not executable")
    else:
        default_branch_head_proof = default_branch_head_proof_path.read_text(encoding="utf-8")
        for marker in (
            'repository_document.get("default_branch")',
            'ref_object.get("type") != "commit"',
            'event_base_ref != default_branch',
            'event_base != default_head',
            'return 0 if result["fresh"] else 3',
        ):
            if marker not in default_branch_head_proof:
                errors.append(f"default-branch freshness proof is missing marker: {marker}")
    if (
        not required_context_activation_path.is_file()
        or not required_context_activation_path.stat().st_mode & 0o111
    ):
        errors.append("live required-context activation proof is missing or not executable")
    else:
        required_context_activation = required_context_activation_path.read_text(encoding="utf-8")
        for marker in (
            'live.get("enforcement") != "active"',
            'live.get("target") != "branch"',
            'live.get("source") != repository',
            'live.get("source_type") != "Repository"',
            'live.get("current_user_can_bypass")',
            'current_user_can_bypass != "never"',
            'live_contexts[0].get("integration_id") != expected_integration_id',
            '"bypass_actors" in live',
            'live_bypass != []',
            'includes != ["~DEFAULT_BRANCH"] or excludes != []',
            'item.get("type") == "required_status_checks"',
            'return 0 if result["activated"] else 3',
        ):
            if marker not in required_context_activation:
                errors.append(f"live required-context activation proof is missing marker: {marker}")
    for marker in (
        "Disarm GitHub Auto-merge before evaluating the current head",
        "Bind the current base to the repository default branch",
        "steps.protected_base.outputs.protected == 'true'",
        "ref: ${{ github.event.pull_request.base.sha }}",
        "if [[ ! -x ci/evaluate-auto-merge.py ]]; then",
        'reasons: ["protected-base policy predates evaluator"]',
        "printf 'eligible=false\\npackage_id=\\n' >>\"$GITHUB_OUTPUT\"",
        "gh api --paginate --slurp",
        "ci/evaluate-auto-merge.py",
        "ci/prove-auto-merge-state.py",
        "POLICY_ELIGIBLE: ${{ steps.policy.outputs.eligible }}",
        "Auto-merge remains disabled; explicit maintainer squash merge is required",
        ".auto_merge == null",
        ".state == \"open\"",
        ".merged == false",
        ".merged_at == null",
        ".head.sha == $head",
        ".base.sha == $base",
        ".head.repo.full_name == $repo",
        ".base.repo.full_name == $repo",
        "Unable to prove the mandatory Auto-merge disarm state",
    ):
        if marker not in auto_merge:
            errors.append(f"auto-merge workflow is missing fail-closed scope gate: {marker}")
    if auto_merge.count("ci/prove-auto-merge-state.py") != 1:
        errors.append("post-checkout policy evaluation must prove the leased PR remains disarmed exactly once")
    if auto_merge.count("--expected-auto-merge disabled") != 1:
        errors.append("post-checkout policy evaluation must prove exactly one disabled state")
    for forbidden in (
        "--auto --squash",
        "--expected-auto-merge enabled",
        "Arm GitHub Auto-merge",
        "trap 'rollback_unverified_auto_merge $?' EXIT",
        "ci/prove-default-branch-head.py",
        "ci/prove-required-context-active.py",
    ):
        if forbidden in auto_merge:
            errors.append(f"evaluation-only Auto Merge Policy must not arm or prepare to arm: {forbidden}")
    if "contents: write" in auto_merge:
        errors.append("evaluation-only Auto Merge Policy must not retain contents write permission")
    auto_merge_command = re.compile(r"gh\s+pr\s+merge[^\n]*--auto[^\n]*--squash")
    for automation_root in (workflows, root / "ci", root / "scripts"):
        if not automation_root.is_dir():
            continue
        for automation_path in sorted(automation_root.rglob("*")):
            if not automation_path.is_file() or "tests" in automation_path.parts:
                continue
            try:
                automation_text = automation_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if auto_merge_command.search(automation_text):
                relative_path = automation_path.relative_to(root)
                errors.append(f"{relative_path}: repository automation must not arm GitHub Auto-merge")
    for marker in (
        'repository=$(gh api "repos/$GITHUB_REPOSITORY")',
        '.default_branch == "main"',
        'default_ref=$(gh api "repos/$GITHUB_REPOSITORY/git/ref/heads/main")',
        '.object.type == "commit"',
        '"$EVENT_BASE_SHA" == "$default_head"',
    ):
        if marker not in auto_merge:
            errors.append(f"pre-checkout default-branch freshness gate is missing marker: {marker}")
    evaluator_command = "          ci/evaluate-auto-merge.py \\\n"
    auto_merge_order = (
        "--disable-auto",
        "ref: ${{ github.event.pull_request.base.sha }}",
        "if [[ ! -x ci/evaluate-auto-merge.py ]]; then",
        evaluator_command,
        "ci/prove-auto-merge-state.py",
    )
    auto_merge_positions = [auto_merge.find(marker) for marker in auto_merge_order]
    if -1 not in auto_merge_positions and auto_merge_positions != sorted(auto_merge_positions):
        errors.append("auto-merge workflow does not preserve disarm/base/fallback/evaluate/final-proof order")
    disarm_step = auto_merge.find("Disarm GitHub Auto-merge before evaluating the current head")
    base_gate_step = auto_merge.find("Bind the current base to the repository default branch")
    checkout_step = auto_merge.find("Check out the immutable protected-base policy")
    if not 0 <= disarm_step < base_gate_step < checkout_step:
        errors.append("auto-merge workflow must disarm before default-branch gating and checkout")
    if "github.event.pull_request.head.ref" in auto_merge:
        errors.append("auto-merge workflow must never fall back to pull-request-head policy code")
    rsync_retry_path = root / "ci" / "rsync-with-lock-retry.sh"
    rsync_retry = rsync_retry_path.read_text(encoding="utf-8") if rsync_retry_path.exists() else ""
    for event in ("opened", "synchronize", "reopened", "merge_group", "workflow_dispatch", "workflow_call", "push"):
        if event not in package_ci:
            errors.append(f"package-ci.yml does not visibly support {event}")
    if "inputs.base_sha" not in package_ci or "github.sha" not in package_ci:
        errors.append("package-ci.yml cannot validate a trusted bot-created PR head via workflow_dispatch")
    if "commit_sha:" not in package_ci or "pr_number:" not in package_ci or "run-name: Package CI ${{ inputs.commit_sha" not in package_ci:
        errors.append("package-ci.yml cannot bind a protected-main trusted dispatch to its exact input commit")
    for marker in (
        "ci/rsync-with-lock-retry.sh -- rsync",
        "RRSYNC_LOCK_JITTER_KEY: ${{ format('{0}:{1}', github.run_id, needs.prepare.outputs.package_id) }}",
    ):
        if marker not in package_ci:
            errors.append(f"package CI repository publication is missing: {marker}")
    for marker in (
        "result != 12",
        "rrsync error: Another instance of rrsync is already accessing this directory.",
        "attempt >= max_attempts",
    ):
        if marker not in rsync_retry:
            errors.append(f"rrsync lock retry is missing fail-closed marker: {marker}")
    for check in ("metadata-validate", "source-verify", "rpmbuild-riscv64", "rpm-install-smoke", "patch-policy", "merge-policy"):
        if not re.search(rf"(?m)^  {re.escape(check)}:\s*$", package_ci):
            errors.append(f"package-ci.yml is missing required check job {check}")
    if "ci/compose-build-result.py" not in package_ci:
        errors.append("package-ci.yml does not compose a final commit-bound build result")
    if "repository-snapshot:" not in package_ci or "ci/rpm-repo-client.py resolve" not in package_ci:
        errors.append("package-ci.yml does not resolve one immutable supplemental repository generation")
    if "--allow-unavailable" not in package_ci:
        errors.append("package-ci.yml does not record the official-repository-only outage fallback")
    if "artifacts/repository/resolution.json" not in package_ci:
        errors.append("package-ci.yml does not pass repository resolution evidence to installed smoke")
    if "publish-rpm-repository:" not in package_ci or "ci/stage-rpm-repository-upload.py" not in package_ci:
        errors.append("package-ci.yml does not publish passing main-branch RPM/SRPM batches")
    if "github.event_name == 'push'" not in package_ci or "github.ref == 'refs/heads/main'" not in package_ci:
        errors.append("package-ci.yml does not restrict automatic RPM publication to protected main pushes")
    if "RPM_REPO_SSH_PRIVATE_KEY: ${{ secrets.RPM_REPO_SSH_PRIVATE_KEY }}" not in package_ci:
        errors.append("package-ci.yml is missing the single approved restricted deployment key")
    if "ci/rpm-repo-known-hosts" not in package_ci or "StrictHostKeyChecking=yes" not in package_ci:
        errors.append("package-ci.yml does not pin and enforce the RPM repository SSH host key")
    if "issues: write\n      pull-requests: write" not in package_ci:
        errors.append("record-ci-state cannot label trusted PRs with its job-scoped token")
    if re.search(r"--result\s+[^\n]*build-result\.json", package_ci):
        errors.append("package-ci.yml writes a phase result directly to build-result.json")
    if "rpmbuild-internal.log" not in package_ci:
        errors.append("package-ci.yml does not retain the RPM tool's internal log for repair evidence")
    if 'result=$?' not in package_ci or 'exit "$result"' not in package_ci:
        errors.append("package-ci.yml does not preserve the exact rpmbuild exit code")
    if package_ci.count('--commit-sha "$BUILD_COMMIT_SHA"') < 2 or "GITHUB_SHA:" in package_ci:
        errors.append("package-ci.yml does not pass the exact head explicitly to source and rpmbuild results")
    build_artifact_marker = "name: package-ci-build-${{ needs.prepare.outputs.package_id }}-${{ github.run_id }}"
    if build_artifact_marker not in package_ci:
        errors.append("package-ci.yml is missing the build artifact upload")
    else:
        build_artifact_block = package_ci.split(build_artifact_marker, 1)[1].split("if-no-files-found:", 1)[0]
        if "${{ runner.temp }}/package-ci-build-upload/" not in build_artifact_block:
            errors.append("package-ci.yml does not upload the sanitized build staging tree")
        for unsafe_tree in ("/BUILD/", "/BUILDROOT/", "/SOURCES/", "/SPECS/"):
            if unsafe_tree in build_artifact_block:
                errors.append(f"package-ci.yml build artifact includes unsafe raw tree {unsafe_tree}")
    stager = root / "ci" / "stage-build-artifacts.py"
    if not stager.is_file() or "regular .json/.log evidence and regular .rpm products only" not in stager.read_text(encoding="utf-8"):
        errors.append("build artifact stager does not enforce the regular evidence/RPM allowlist")

    build_rpm = (root / "scripts" / "build-rpm").read_text(encoding="utf-8")
    if "GITHUB_SHA" in build_rpm or '"commit_sha": args.commit_sha' not in build_rpm:
        errors.append("build-rpm must use only the explicit --commit-sha provenance input")
    package_policy = (root / "ci" / "package-policy.py").read_text(encoding="utf-8")
    package_schema = (root / "schemas" / "package.schema.json").read_text(encoding="utf-8")
    if 'build.get("user", "root")' not in package_policy:
        errors.append("package build-user policy must preserve the compatible root default")
    if '"user": {"enum": ["root", "unprivileged"]}' not in package_schema:
        errors.append("package schema does not fail closed on build.user")
    if "build_user: ${{ steps.policy.outputs.build_user }}" not in package_ci:
        errors.append("package-ci.yml does not propagate the validated build-user policy")
    build_timeout = (
        "timeout-minutes: ${{ fromJSON(needs.prepare.outputs.timeout_minutes || '120') }}"
    )
    if package_ci.count(build_timeout) != 1:
        errors.append(
            "package-ci.yml must bind the heavy RPM job to the validated package timeout"
        )
    timeout_budget_path = root / "ci" / "rpmbuild-timeout-budget.py"
    if not timeout_budget_path.is_file() or not timeout_budget_path.stat().st_mode & 0o111:
        errors.append("rpmbuild timeout-budget helper is missing or not executable")
    for marker in (
        "- name: Establish the validated package deadline\n        if: needs.prepare.outputs.mode == 'package'",
        "ci/rpmbuild-timeout-budget.py start",
        "rpmbuild_timeout_seconds=$(ci/rpmbuild-timeout-budget.py remaining",
        '[[ "$rpmbuild_timeout_seconds" =~ ^[1-9][0-9]*$ ]]',
        'rpmbuild_outer_timeout_seconds=$((rpmbuild_timeout_seconds + 60))',
        '[[ "$rpmbuild_outer_timeout_seconds" =~ ^[1-9][0-9]*$ ]]',
        '--timeout-seconds "$rpmbuild_outer_timeout_seconds"',
        '--build-timeout-seconds "$rpmbuild_timeout_seconds"',
    ):
        if marker not in package_ci:
            errors.append(f"package-ci.yml is missing the evidence-preserving build budget marker: {marker}")
    if "--timeout-seconds 6900" in package_ci:
        errors.append("package-ci.yml still truncates validated package budgets at 6900 seconds")
    if '--timeout-seconds "$rpmbuild_timeout_seconds"' in package_ci:
        errors.append("package-ci.yml gives the outer cap no timeout-evidence grace period")
    reserve_matches = re.findall(r"--reserve-seconds ([0-9]+)", package_ci)
    grace_matches = re.findall(
        r"rpmbuild_outer_timeout_seconds=\$\(\(rpmbuild_timeout_seconds \+ ([0-9]+)\)\)",
        package_ci,
    )
    if len(reserve_matches) != 1 or len(grace_matches) != 1:
        errors.append("package-ci.yml must declare one evidence reserve and one outer-cap grace")
    elif int(reserve_matches[0]) - int(grace_matches[0]) < 240:
        errors.append("package-ci.yml must retain at least 240 seconds for timeout evidence")
    if package_ci.count('--build-user "$BUILD_USER"') < 2:
        errors.append("package-ci.yml does not bind dependency and rpmbuild stages to build.user")
    runner_expression = (
        "needs.prepare.outputs.mode == 'package' && "
        "needs.prepare.outputs.needs_native != 'true' && "
        "(github.event_name == 'push' || github.event_name == 'workflow_dispatch') && "
        "github.ref == 'refs/heads/main'"
    )
    runner_labels = '["self-hosted","linux","x64","oe-rva23-qemu"]'
    if package_ci.count(runner_expression) != 2:
        errors.append(
            "package-ci.yml must route exactly the two heavy QEMU jobs only from protected-main trusted events"
        )
    if package_ci.count(runner_labels) != 2:
        errors.append(
            "package-ci.yml must bind exactly two heavy jobs to the approved QEMU runner label set"
        )
    qemu_policy_path = root / "ci" / "qemu-runner-policy.py"
    qemu_policy = qemu_policy_path.read_text(encoding="utf-8") if qemu_policy_path.exists() else ""
    for marker in (
        'TRUSTED_EVENTS = {"push", "workflow_dispatch"}',
        'PROTECTED_REF = "refs/heads/main"',
        'SELF_HOSTED_LABELS = ["self-hosted", "linux", "x64", "oe-rva23-qemu"]',
    ):
        if marker not in qemu_policy:
            errors.append(f"QEMU runner evidence policy is missing {marker}")
    if "ci/qemu-runner-policy.py" not in package_ci:
        errors.append("package-ci.yml does not emit structured QEMU runner routing evidence")
    authorization = root / "ci" / "authorize-trusted-package-dispatch.py"
    if not authorization.is_file() or not authorization.stat().st_mode & 0o111:
        errors.append("trusted protected-main dispatch authorizer is missing or not executable")
    elif not all(marker in authorization.read_text(encoding="utf-8") for marker in (
        "PROTECTED_REF = \"refs/heads/main\"",
        "TRUSTED_ASSOCIATIONS",
        "PR changes are not confined",
        "PR is not an allowed bot infrastructure shape",
        "IMAGE_LOCK_BRANCH_RE",
        "CATALOG_BRANCH_RE",
        "trusted PR dispatch must disable repository publication",
    )):
        errors.append("trusted protected-main dispatch authorizer is missing required scope or publication guards")
    for marker in (
        "authorize-trusted-dispatch:",
        "needs: authorize-trusted-dispatch",
        "tooling_sha: ${{ steps.tooling.outputs.tooling_sha }}",
        "ci/authorize-trusted-package-dispatch.py",
        "--pr-number \"$PR_NUMBER\"",
        "--publish-to-repo \"$PUBLISH_TO_REPO\"",
        "$GITHUB_REPOSITORY/.github/workflows/rpm-repo-backfill.yml@refs/heads/main",
        "inputs.commit_sha == '' && inputs.publish_to_repo",
    ):
        if marker not in package_ci:
            errors.append("package-ci.yml is missing fixed-main trusted dispatch authorization: %s" % marker)
    if package_ci.count("if: always() && needs.authorize-trusted-dispatch.outputs.authorized == 'true'") < 7:
        errors.append("package-ci.yml can check out a dispatch head before trusted authorization succeeds")
    if "(github.event_name == 'workflow_call' && inputs.publish_to_repo)" in package_ci:
        errors.append("package-ci.yml permits reusable callers other than the protected RPM backfill to publish")
    tooling_resolver = root / "ci" / "resolve-protected-tooling.py"
    if not tooling_resolver.is_file() or not tooling_resolver.stat().st_mode & 0o111:
        errors.append("protected-main tooling resolver is missing or not executable")
    elif not all(marker in tooling_resolver.read_text(encoding="utf-8") for marker in (
        'EVENT_SHA_EVENTS = {"push", "workflow_dispatch", "workflow_call"}',
        'PACKAGE_WORKFLOW = ".github/workflows/package-ci.yml"',
        'BACKFILL_WORKFLOW = ".github/workflows/rpm-repo-backfill.yml"',
        'f"{repository}/{PACKAGE_WORKFLOW}@refs/pull/{number}/merge"',
        'if len(parents) != 3 or parents[0] != merge_sha:',
        'if parents[2] != package_sha:',
        'tooling_sha = require_sha(parents[1], "pull-request merge first parent")',
        'require_ancestor(root, tooling_sha, checked_sha)',
        'require_checked_head(root, checked_sha)',
    )):
        errors.append("protected-main tooling resolver is missing event or immutable-HEAD guards")
    overlay_materializer = root / "ci" / "materialize-package-head.py"
    overlay_selector = root / "ci" / "select-package-scope.py"
    if not overlay_materializer.is_file() or not overlay_materializer.stat().st_mode & 0o111:
        errors.append("protected-main package overlay materializer is missing or not executable")
    elif not all(marker in overlay_materializer.read_text(encoding="utf-8") for marker in (
        '"kind": "protected-main-package-overlay"',
        '"package_tree_sha": tree_sha',
        '"tooling_commit_sha": tooling_sha',
    )):
        errors.append("protected-main package overlay evidence is missing its exact provenance binding")
    if not overlay_selector.is_file() or not overlay_selector.stat().st_mode & 0o111:
        errors.append("protected-main package overlay scope selector is missing or not executable")
    elif not all(marker in overlay_selector.read_text(encoding="utf-8") for marker in (
        'parser.add_argument("--tooling-head")',
        'parser.add_argument("--overlay-evidence", type=Path)',
        'git(root, ["write-tree", f"--prefix={package_path}/"])',
        'git(root, ["ls-files", "--others", "--", package_path])',
    )):
        errors.append("protected-main package selector does not revalidate the exact overlay tree")
    for marker in (
        '--tooling-head "$TOOLING_HEAD_SHA"',
        "--overlay-evidence artifacts/scope/tooling-overlay.json",
    ):
        if marker not in package_ci:
            errors.append(f"package CI scope selection is missing overlay binding: {marker}")
    protected_tooling_checkout = (
        "ref: ${{ needs.authorize-trusted-dispatch.outputs.tooling_sha }}"
    )
    immutable_tooling_candidate = (
        "ref: ${{ (github.event_name == 'pull_request' || "
        "github.event_name == 'merge_group') && github.workflow_sha || github.sha }}"
    )
    untrusted_tooling_checkout = (
        "ref: ${{ inputs.commit_sha != '' && github.sha || "
        "github.event.pull_request.head.sha || github.event.merge_group.head_sha || github.sha }}"
    )
    if package_ci.count(immutable_tooling_candidate) != 1:
        errors.append("package-ci.yml does not select one immutable workflow/event tooling candidate")
    if package_ci.count(protected_tooling_checkout) != 8:
        errors.append(
            "package-ci.yml must use one validated tooling output in seven package jobs and CI state"
        )
    if package_ci.count("github.event.pull_request.base.sha") != 1:
        errors.append("package-ci.yml may pass the pull-request payload base only once for audit evidence")
    if untrusted_tooling_checkout in package_ci:
        errors.append("package-ci.yml must not execute shared tooling from a pull-request head")
    if package_ci.count("ci/materialize-package-head.py --repo-root .") != 7:
        errors.append("package-ci.yml must overlay the exact package tree in all seven package jobs")
    if package_ci.count('--tooling-sha "$TOOLING_COMMIT_SHA"') != 7:
        errors.append("package-ci.yml package overlays are not bound to the checked-out protected tooling")
    if package_ci.count(
        "TOOLING_COMMIT_SHA: ${{ needs.authorize-trusted-dispatch.outputs.tooling_sha }}"
    ) != 7:
        errors.append("package-ci.yml overlay jobs do not share the validated tooling output")
    for marker in (
        "Classify the exact event delta with protected tooling",
        "Materialize only the exact package tree",
        "tooling_sha: ${{ steps.tooling.outputs.tooling_sha }}",
        "ci/resolve-protected-tooling.py",
        "fetch-depth: ${{ github.event_name == 'pull_request' && 2 || 0 }}",
        '--pr-number "$PR_NUMBER"',
        '--package-head "$PACKAGE_HEAD"',
        '--base-sha "$BASE_SHA"',
        "PACKAGE_COMMIT_SHA: ${{ inputs.commit_sha || github.event.pull_request.head.sha || github.event.merge_group.head_sha || github.sha }}",
        "TOOLING_HEAD_SHA: ${{ needs.authorize-trusted-dispatch.outputs.tooling_sha }}",
        "&& needs.authorize-trusted-dispatch.outputs.tooling_sha || github.event.before || inputs.base_sha }}",
        "if: always() && github.event_name == 'pull_request' && needs.authorize-trusted-dispatch.outputs.authorized == 'true'",
    ):
        if marker not in package_ci:
            errors.append(f"package CI protected-tooling overlay contract is missing: {marker}")
    trusted_dispatch = root / "scripts" / "dispatch-trusted-package-ci"
    if not trusted_dispatch.is_file() or not trusted_dispatch.stat().st_mode & 0o111:
        errors.append("trusted protected-main package dispatcher is missing or not executable")
    elif not all(marker in trusted_dispatch.read_text(encoding="utf-8") for marker in (
        '"--ref",\n                "main"',
        '"pr_number=%d" % args.pr',
        '"publish_to_repo=false"',
        "TRUSTED_ASSOCIATIONS",
        "download_build_result",
        "wait_for_terminal_run",
        '"--run-timeout-seconds"',
        '"terminal_observation"',
    )):
        errors.append("trusted protected-main package dispatcher is missing required scope or evidence guards")
    for workflow in sorted(workflows.glob("*.yml")):
        if workflow.name == "package-ci.yml":
            continue
        if "oe-rva23-qemu" in workflow.read_text(encoding="utf-8"):
            errors.append(
                f"{workflow.name}: repository QEMU runner label is outside package-ci.yml"
            )
    build_runner_path = root / "ci" / "run-rpmbuild-container.py"
    build_runner = (
        build_runner_path.read_text(encoding="utf-8") if build_runner_path.exists() else ""
    )
    if not build_runner_path.is_file() or not build_runner_path.stat().st_mode & 0o111:
        errors.append("rpmbuild user orchestrator is missing or not executable")
    for marker in (
        'BUILD_USERS = {"root", "unprivileged"}',
        'TARGET_UID = 10001',
        'docker_limits(network="bridge")',
        'docker_limits(network="none")',
        '"--commit-sha",',
        'verified network source retrieval',
        'OE_BUILD_NETWORK=enabled',
        'EVIDENCE_FILES =',
        'grant_unprivileged_workspace_access(repo_root, args.package_id)',
        'grant_other_access(repo_root, readable=False)',
        'grant_other_access(packages_dir, readable=False)',
        'grant_other_access(work_parent, readable=False)',
        'successful unprivileged build is missing required evidence',
        'require_complete=completed.returncode == 0',
        'type=positive_seconds',
        'str(build_timeout_seconds)',
    ):
        if marker not in build_runner:
            errors.append(
                f"rpmbuild user orchestrator is missing required contract marker {marker}"
            )

    image_workflow = (workflows / "build-ci-image.yml").read_text(encoding="utf-8") if (workflows / "build-ci-image.yml").exists() else ""
    if "--method PATCH" in image_workflow and "/user/packages/container/" in image_workflow:
        errors.append("build-ci-image.yml must verify public GHCR state, not attempt a user-level visibility mutation")
    if "ci/dispatch-required-checks.sh" not in image_workflow or "statuses: write" not in image_workflow:
        errors.append("digest-lock PR creation does not bridge actual required jobs onto the bot-created PR head")
    if "Auto-merge is disabled; an explicit maintainer squash merge is required" not in image_workflow:
        errors.append("digest-lock PR creation does not report the explicit maintainer merge boundary")
    if "git ls-remote --exit-code --heads" not in image_workflow or "test \"$changed\" = ci/image.lock" not in image_workflow:
        errors.append("digest-lock retry does not safely verify and reuse an existing lock branch")
    if "git merge --no-edit origin/main" not in image_workflow:
        errors.append("digest-lock retry does not update the reused branch to the latest protected main")

    settings_path = root / ".github" / "repository-settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8")) if settings_path.exists() else {}
    merge_settings = settings.get("merge", {})
    if merge_settings.get("allow_auto_merge") is not False:
        errors.append("repository settings must disable GitHub Auto-merge")
    actions_settings = settings.get("actions", {})
    if actions_settings.get("default_workflow_permissions") != "read":
        errors.append("default GITHUB_TOKEN permissions must remain read-only")
    if actions_settings.get("can_approve_pull_request_reviews") is not True:
        errors.append("Actions cannot create the reviewed digest-lock PR")
    if actions_settings.get("fork_pull_request_approval_policy") != "first_time_contributors_new_to_github":
        errors.append("established contributors must be allowed to run fork workflows without repeated approval")
    qemu_runner = actions_settings.get("self_hosted_qemu_runner", {})
    if qemu_runner != {
        "enabled": True,
        "trust_boundary": "protected-main-only",
        "labels": ["self-hosted", "linux", "x64", "oe-rva23-qemu"],
    }:
        errors.append("repository settings do not record the protected-main QEMU runner boundary")
    github_configurator = (root / "ci" / "configure-github.sh").read_text(encoding="utf-8")
    for marker in (
        "-F allow_auto_merge=false",
        ".allow_auto_merge == false",
        "repository merge-setting readback mismatch",
    ):
        if marker not in github_configurator:
            errors.append(f"GitHub provisioning does not enforce disabled Auto-merge: {marker}")
    if "actions/permissions/fork-pr-contributor-approval" not in github_configurator:
        errors.append("GitHub provisioning does not enforce the external fork workflow approval policy")
    if github_configurator.count("first_time_contributors_new_to_github") < 1:
        errors.append("GitHub provisioning does not enforce the least restrictive public-repository fork policy")
    context_audit_path = root / "ci" / "audit-required-context.py"
    if not context_audit_path.is_file() or not context_audit_path.stat().st_mode & 0o111:
        errors.append("required-context migration audit is missing or not executable")
    else:
        context_audit = context_audit_path.read_text(encoding="utf-8")
        for marker in (
            "pullRequests(first: 100",
            "contexts(first: 100)",
            "context-pagination-overflow",
            "open-pr-exact-head-snapshot-changed",
            "status-context-not-allowed",
            "unexpected-provenance",
            "configure-bridge-v1",
            "bot-image-lock-v1",
            "bridge_attestation_stable",
            "changed_base_pr_count",
            'return 0 if result["passed"] else 1',
        ):
            if marker not in context_audit:
                errors.append(f"required-context migration audit is missing fail-closed contract: {marker}")
    audit_markers = (
        "ci/audit-required-context.py",
        "--context configure",
        '--expected-workflow "Auto Merge Policy"',
        "--expected-app github-actions",
        "--bridge-policy bot-image-lock-v1",
        '--output "$audit_output"',
    )
    for marker in audit_markers:
        if marker not in github_configurator:
            errors.append(f"GitHub provisioning is missing required-context preflight: {marker}")
    if all(marker in github_configurator for marker in audit_markers):
        dry_run = github_configurator.index("if [[ $mode == dry-run ]]")
        audit_call = github_configurator.index("ci/audit-required-context.py")
        first_write = github_configurator.index('gh api --method PATCH "repos/$repo"')
        second_audit = github_configurator.rindex("run_required_context_audit")
        ruleset_write = github_configurator.index('gh api --method PUT "repos/$repo/rulesets/$ruleset_id"')
        if not dry_run < audit_call < first_write < second_audit < ruleset_write:
            errors.append("required-context preflight must follow dry-run exit and precede every remote write")
    for marker in (
        'if ! applied_full=$(gh api "repos/$repo/rulesets/$ruleset_id")',
        "ruleset readback identity is invalid; attempting exact policy rollback",
        'if ! applied_policy=$(jq -ceS "$ruleset_projection"',
        '[[ $applied_policy == "$desired_policy" ]]',
        'integration_id: .integration_id',
        'has("bypass_actors") and (.bypass_actors | type == "array")',
        "ruleset readback does not exactly match the configured protection policy",
        "rollback_ruleset()",
        "attempting exact policy rollback",
        "ruleset rollback could not be verified; inspect the live policy immediately",
    ):
        if marker not in github_configurator:
            errors.append(f"GitHub provisioning does not prove exact ruleset readback: {marker}")
    if settings.get("allowed_actions_secrets") != ["RPM_REPO_SSH_PRIVATE_KEY"]:
        errors.append("repository settings must allow only the restricted RPM repository deployment key")
    forbidden_secrets = settings.get("forbidden_actions_secrets", [])
    if "OPENAI_API_KEY" not in forbidden_secrets or "CODEX_API_KEY" not in forbidden_secrets:
        errors.append("OpenAI and Codex Actions secrets must remain explicitly forbidden")

    discovery = (workflows / "catalog-discovery.yml").read_text(encoding="utf-8") if (workflows / "catalog-discovery.yml").exists() else ""
    if "scripts/snapshot-catalog" not in discovery or "scripts/discover-packages" not in discovery:
        errors.append("catalog-discovery.yml must normalize live metadata before candidate discovery")
    if re.search(r"discover-packages[\s\S]{0,1500}--input\s+[^\n]*(?:\.db|repomd\.xml|Release|json\.gz)", discovery):
        errors.append("discover-packages must not consume raw distribution databases or indexes directly")
    if "ci/dispatch-required-checks.sh" not in discovery or "statuses: write" not in discovery:
        errors.append("catalog snapshot PRs cannot satisfy protected checks after GITHUB_TOKEN event suppression")
    if "Auto-merge is disabled; an explicit maintainer squash merge is required" not in discovery:
        errors.append("catalog snapshot PR creation does not report the explicit maintainer merge boundary")

    check_bridge = root / "ci" / "dispatch-required-checks.sh"
    if not check_bridge.is_file() or not check_bridge.stat().st_mode & 0o111:
        errors.append("bot-created PR check bridge is missing or not executable")
    else:
        check_bridge_text = check_bridge.read_text(encoding="utf-8")
        for marker in (
            'gh workflow run package-ci.yml --repo "$repo" --ref main',
            'expected_name="Package CI PR $pr_number $head_sha $dispatch_nonce"',
            '.displayTitle == $name and .headSha == $base',
            '-f "dispatch_nonce=$dispatch_nonce"',
            '.conclusion == "success"',
        ):
            if marker not in check_bridge_text:
                errors.append(
                    "bot-created PR check bridge is missing protected-main dispatch binding: %s"
                    % marker
                )
    if "inputs.package_id || inputs.pr_number" not in package_ci:
        errors.append("trusted bot PR dispatches do not have PR-isolated concurrency")
    if "inputs.dispatch_nonce" not in package_ci or "inputs.commit_sha, inputs.dispatch_nonce" not in package_ci:
        errors.append("trusted bot PR dispatch run identity does not include a unique nonce")

    configure_bridge_path = workflows / "configure-context-bridge.yml"
    configure_bridge = configure_bridge_path.read_text(encoding="utf-8") if configure_bridge_path.exists() else ""
    for marker in (
        "workflows: [Auto Merge Policy]",
        "workflow_dispatch:",
        "if: github.ref == 'refs/heads/main'",
        "checks: write",
        "actions: read",
        "ci/bridge-configure-context.py",
        "if: always()",
        "retention-days: 7",
        "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
    ):
        if marker not in configure_bridge:
            errors.append("configure CheckRun bridge is missing protected-main evidence contract: %s" % marker)
    for forbidden in ("pull_request_target", "statuses: write", "github.event.pull_request.head"):
        if forbidden in configure_bridge:
            errors.append("configure CheckRun bridge contains forbidden candidate/status mechanism: %s" % forbidden)
    configure_bridge_helper = root / "ci" / "bridge-configure-context.py"
    if not configure_bridge_helper.is_file() or not configure_bridge_helper.stat().st_mode & 0o111:
        errors.append("configure CheckRun bridge helper is missing or not executable")
    else:
        helper_text = configure_bridge_helper.read_text(encoding="utf-8")
        for marker in (
            'SOURCE_PATH = ".github/workflows/auto-merge.yml"',
            'BRIDGE_PATH = ".github/workflows/configure-context-bridge.yml"',
            'CHECK_APP_ID = 15368',
            'IMAGE_BRANCH = re.compile',
            'published-public-anonymous-verified',
            'image-lock branch does not match the candidate digest prefix',
            'a forbidden configure StatusContext already exists',
            'status": "in_progress"',
            'prove_check(args.repository, check_id, head, eid, details, "completed", "success")',
            'fail_created_check',
        ):
            if marker not in helper_text:
                errors.append("configure CheckRun bridge helper is missing fail-closed attestation: %s" % marker)

    credential_guard = root / "scripts" / "github-credential-guard"
    if not credential_guard.is_file() or not credential_guard.stat().st_mode & 0o111:
        errors.append("local GitHub credential guard is missing or not executable")
    for skill_name in (
        "openeuler-riscv-repair",
        "openeuler-riscv-repo-bootstrap",
        "openeuler-rpm-onboard",
        "openeuler-rpm-update",
        "openeuler-package-dashboard",
    ):
        skill_path = root / "skills" / skill_name / "SKILL.md"
        if not skill_path.is_file() or "github-credential-guard" not in skill_path.read_text(encoding="utf-8"):
            errors.append(f"{skill_name}: Skill does not require the local GitHub credential guard")

    daily = (workflows / "daily-update-check.yml").read_text(encoding="utf-8") if (workflows / "daily-update-check.yml").exists() else ""
    if "--state-output artifacts/state/update-state.json" not in daily:
        errors.append("daily update aggregation does not persist per-package success timestamps")
    update_applier = (root / "ci" / "apply-update-batch.sh").read_text(encoding="utf-8")
    if "--auto --squash" in update_applier:
        errors.append("daily update application must not arm GitHub Auto-merge")
    if "Auto-merge is disabled; an explicit maintainer squash merge is required" not in update_applier:
        errors.append("daily update application does not report the explicit maintainer merge boundary")

    golden = (workflows / "golden-evaluation.yml").read_text(encoding="utf-8") if (workflows / "golden-evaluation.yml").exists() else ""
    for package_id in ("golden-success-hello", "golden-riscv-inline-asm", "golden-needs-native-kmod"):
        if package_id not in golden:
            errors.append(f"golden-evaluation.yml is missing {package_id}")
    if "--stage auto" not in golden:
        errors.append("golden-evaluation.yml does not use stage-aware golden assertions")
    if "rpmbuild-internal.log" not in golden:
        errors.append("golden-evaluation.yml does not retain the RPM tool's internal log")
    if "--allow-unavailable" not in golden or "repository-resolution.json" not in golden:
        errors.append("golden-evaluation.yml does not propagate repository outage evidence")
    if "BUILD_USER: ${{ steps.policy.outputs.build_user }}" not in golden or '--build-user "$BUILD_USER"' not in golden:
        errors.append("golden-evaluation.yml does not pass the package build identity to dependency preparation")

    builddeps_path = root / "ci" / "prepare-build-deps.py"
    builddeps = builddeps_path.read_text(encoding="utf-8") if builddeps_path.exists() else ""
    if ":/workspace:ro" not in builddeps:
        errors.append("BuildRequires planning must mount the reviewed repository read-only")
    if ":/workspace/artifacts/" in builddeps:
        errors.append("BuildRequires evidence cannot be nested beneath the read-only /workspace mount")
    if ":/evidence:rw" not in builddeps or '"/evidence/' not in builddeps:
        errors.append("BuildRequires planning is missing its dedicated writable /evidence mount")
    for marker in (
        "--supplemental-repo-file",
        "--supplemental-evidence",
        "--enablerepo=openeuler-riscv-project",
        "openeuler-riscv-project.repo,readonly",
        "fallback_repository_ids",
    ):
        if marker not in builddeps:
            errors.append(f"BuildRequires preparation is missing supplemental repository control: {marker}")
    for marker in (
        "DNF_TRANSACTION_CONTAINER_PATH",
        '"--budget-seconds", str(DNF_TRANSACTION_BUDGET_SECONDS)',
        '"--attempt-timeouts-seconds", DNF_ATTEMPT_TIMEOUTS_SECONDS',
        '"--kill-after-seconds", str(DNF_KILL_AFTER_SECONDS)',
        'dst=/evidence',
        '"dependency_install_attempts"',
        '"dependency_install_transaction"',
    ):
        if marker not in builddeps:
            errors.append(f"BuildRequires preparation is missing bounded download resilience: {marker}")
    dnf_transaction_path = root / "ci" / "run-dnf-transaction"
    dnf_transaction = (
        dnf_transaction_path.read_text(encoding="utf-8")
        if dnf_transaction_path.exists()
        else ""
    )
    for marker in (
        "--setopt=retries=20",
        "--setopt=timeout=60",
        "--setopt=minrate=1000",
        "--setopt=max_parallel_downloads=1",
        "PROTECTED_NETWORK_OPTIONS",
        "cannot override protected DNF option",
        "start_new_session=True",
        "os.killpg(process.pid, signal.SIGTERM)",
        "os.killpg(process.pid, signal.SIGKILL)",
        '"attempts": []',
        '"elapsed_seconds"',
        '"exit_code"',
        "worst_case_seconds > args.budget_seconds",
    ):
        if marker not in dnf_transaction:
            errors.append(f"bounded DNF transaction runner is missing its fail-closed contract: {marker}")
    if "--setopt=minrate=1\"" in dnf_transaction:
        errors.append("bounded DNF transaction runner must not permit the obsolete 1 B/s low-speed threshold")
    for marker in (
        "BASELINE_ANCHORS",
        "rpm_manifest_from_image",
        '"--platform", "linux/riscv64", "--network", "none", "--read-only"',
        "RUNNER_MANAGED_NETWORK_LABEL",
        "RUNNER_SESSION_LABEL",
        "validate_managed_network",
        "validate_container_networks",
        "recover_created_network_id",
        "recover_created_container_id",
        "baseline = rpm_baseline_evidence",
        'if baseline["status"] != "passed"',
        '"--network", dependency_network',
        '["docker", "network", "disconnect", egress_network_id, container_id]',
        '"classification": "none" if valid else "failure:infrastructure"',
        '"network_install_started": False',
        'baseline["network_install_started"] = True',
        'baseline["network_install_completed"] = True',
        "cleanup_docker_resources",
        'write_json_atomic(baseline_path, baseline)',
    ):
        if marker not in builddeps:
            errors.append(f"BuildRequires preparation is missing the live RPM fail-closed gate: {marker}")
    if '"docker", "network", "connect"' in builddeps:
        errors.append("BuildRequires preparation must not transition a running container's network")
    baseline_order_markers = (
        "before = rpm_manifest_from_image",
        "baseline = rpm_baseline_evidence",
        'if baseline["status"] != "passed"',
        "egress_network_id = run([",
        '"docker", "create"',
        'baseline["network_install_started"] = True',
        "write_json_atomic(baseline_path, baseline)",
        "run(root_exec(",
        'transaction_record.get("status") != "passed"',
        '["docker", "network", "disconnect", egress_network_id, container_id]',
        'baseline["network_install_completed"] = True',
    )
    cursor = 0
    try:
        for marker in baseline_order_markers:
            cursor = builddeps.index(marker, cursor) + len(marker)
    except ValueError:
        errors.append(
            "BuildRequires network lifecycle is not ordered after the live RPM baseline"
        )

    install_smoke = (root / "ci" / "install-smoke.sh").read_text(encoding="utf-8")
    if "--enablerepo=openeuler-riscv-project" not in install_smoke:
        errors.append("installed-RPM smoke does not use the verified supplemental repository")
    for marker in ("repository_evidence", "endpoint-unavailable", "enabled_repositories"):
        if marker not in install_smoke:
            errors.append(f"installed-RPM smoke is missing repository outage control: {marker}")
    for marker in (
        "ci/run-dnf-transaction",
        "--budget-seconds 3300",
        "--attempt-timeouts-seconds 2100,1100",
        "--retry-delay-seconds 5",
        "--kill-after-seconds 10",
        "bounded RPM installation DNF transaction failed",
    ):
        if marker not in install_smoke:
            errors.append(f"installed-RPM smoke is missing bounded download resilience: {marker}")

    rpm_client = root / "ci" / "rpm-repo-client.py"
    if not rpm_client.is_file() or "http://2.27.148.101:38080" not in rpm_client.read_text(encoding="utf-8"):
        errors.append("supplemental RPM repository client is missing or does not pin the operator endpoint")
    elif "RepositoryUnavailable" not in rpm_client.read_text(encoding="utf-8"):
        errors.append("supplemental RPM repository client cannot distinguish outages from integrity failures")
    known_hosts = root / "ci" / "rpm-repo-known-hosts"
    if not known_hosts.is_file() or "[2.27.148.101]:38022 ssh-ed25519 " not in known_hosts.read_text(encoding="utf-8"):
        errors.append("RPM repository SSH host key is not pinned")

    server_dir = root / "ops" / "rpm-repo-server"
    required_server_files = {
        "README.md",
        "deploy-key.pub",
        "install.sh",
        "nginx.conf",
        "openeuler-rpmrepo.default",
        "openeuler-rpmrepo.path",
        "openeuler-rpmrepo.service",
        "openeuler-rpmrepo.timer",
        "rpmrepo_publish.py",
    }
    if not server_dir.is_dir() or not required_server_files.issubset({path.name for path in server_dir.iterdir()}):
        errors.append("reproducible RPM repository server deployment assets are incomplete")
    else:
        server_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in server_dir.iterdir()
            if path.is_file() and path.suffix not in {".pub"}
        )
        if "/srv/openeuler-riscv-rpm-repo" in server_text:
            errors.append("RPM repository data must not use the retired /srv path")
        for marker in (
            "/opt/openeuler-riscv-rpm-repo",
            "rrsync -wo -no-del -no-overwrite",
            "createrepo_c",
            "PathChanged=/opt/openeuler-riscv-rpm-repo/incoming",
            "%{SOURCEPACKAGE}",
            'identity["sourcepackage"] == "1"',
        ):
            if marker not in server_text:
                errors.append(f"RPM repository server definition is missing: {marker}")

    backfill = (workflows / "rpm-repo-backfill.yml").read_text(encoding="utf-8") if (workflows / "rpm-repo-backfill.yml").exists() else ""
    for marker in (
        "ci/list-rpm-repo-packages.py",
        "uses: ./.github/workflows/package-ci.yml",
        "--max-concurrency \"${{ vars.RPM_BACKFILL_MAX_CONCURRENCY || '50' }}\"",
        "packages_0: ${{ steps.plan.outputs.packages_0 }}",
        "packages_1: ${{ steps.plan.outputs.packages_1 }}",
        "max-parallel: ${{ fromJSON(needs.plan.outputs.max_parallel_per_shard) }}",
        "publish_to_repo: true",
        "retention-days: 7",
    ):
        if marker not in backfill:
            errors.append(f"RPM repository backfill is missing: {marker}")

    if 'def root_exec(' not in builddeps or '"--user", "0:0"' not in builddeps:
        errors.append("BuildRequires installation does not explicitly retain root identity")
    if (
        'TARGET_BUILD_UID = 10001' not in builddeps
        or 'args.build_user == "unprivileged"' not in builddeps
    ):
        errors.append("BuildRequires image does not provision the fixed opt-in build identity")

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
