# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "ci" / "evaluate-auto-merge.py"
WORKFLOW = REPO / ".github" / "workflows" / "auto-merge.yml"
STATE_PROOF = REPO / "ci" / "prove-auto-merge-state.py"
BASE_HEAD_PROOF = REPO / "ci" / "prove-default-branch-head.py"
ACTIVATION_PROOF = REPO / "ci" / "prove-required-context-active.py"
RULESET = REPO / ".github" / "rulesets" / "main.json"
CONFIGURATOR = REPO / "ci" / "configure-github.sh"
HEAD = "1" * 40
BASE = "2" * 40
REPOSITORY = "yinjiayi/openeuler-riscv-packages"


def pull_request(*, paths: list[str], draft: bool = False, labels: list[str] | None = None) -> dict:
    return {
        "state": "open",
        "draft": draft,
        "author_association": "OWNER",
        "user": {"login": "yinjiayi"},
        "head": {"sha": HEAD, "repo": {"full_name": REPOSITORY}},
        "base": {"sha": BASE, "repo": {"full_name": REPOSITORY}},
        "labels": [{"name": label} for label in labels or []],
        "changed_files": len(paths),
    }


def file_entries(paths: list[str]) -> list[dict[str, str]]:
    return [{"filename": path, "status": "modified"} for path in paths]


class AutoMergePolicyTests(unittest.TestCase):
    def evaluate(
        self,
        pr: dict,
        files: object,
        *,
        expected: int = 0,
        event_head: str = HEAD,
        event_base: str = BASE,
    ) -> dict:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            pr_path = root / "pr.json"
            files_path = root / "files.json"
            output = root / "result.json"
            pr_path.write_text(json.dumps(pr) + "\n", encoding="utf-8")
            files_path.write_text(json.dumps(files) + "\n", encoding="utf-8")
            completed = subprocess.run(
                [
                    str(POLICY),
                    "--pr-json",
                    str(pr_path),
                    "--files-json",
                    str(files_path),
                    "--repo",
                    REPOSITORY,
                    "--event-head",
                    event_head,
                    "--event-base",
                    event_base,
                    "--output",
                    str(output),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(completed.returncode, expected, completed.stderr)
            return json.loads(output.read_text(encoding="utf-8"))

    def test_exact_single_package_change_is_eligible(self) -> None:
        paths = [
            "packages/acl/README.md",
            "packages/acl/acl.spec",
            "packages/acl/tests/smoke.sh",
        ]
        result = self.evaluate(pull_request(paths=paths), file_entries(paths))
        self.assertTrue(result["eligible"])
        self.assertEqual(result["package_id"], "acl")
        self.assertEqual(result["reasons"], [])

    def test_paginated_single_package_file_response_is_eligible(self) -> None:
        paths = ["packages/acl/README.md", "packages/acl/acl.spec"]
        pages = [[file_entries(paths)[0]], [file_entries(paths)[1]]]
        result = self.evaluate(pull_request(paths=paths), pages)
        self.assertTrue(result["eligible"])

    def test_package_plus_any_shared_file_is_blocked(self) -> None:
        for shared in (
            ".github/workflows/package-ci.yml",
            "ci/prepare-build-deps.py",
            "scripts/build-rpm",
            "schemas/package.schema.json",
            "dashboard/app.js",
            "catalog/package-index.json",
            "track.md",
        ):
            with self.subTest(shared=shared):
                paths = ["packages/acl/README.md", shared]
                result = self.evaluate(pull_request(paths=paths), file_entries(paths))
                self.assertFalse(result["eligible"])
                self.assertTrue(any("outside a package directory" in item for item in result["reasons"]))

    def test_two_package_directories_are_blocked(self) -> None:
        paths = ["packages/acl/README.md", "packages/attr/README.md"]
        result = self.evaluate(pull_request(paths=paths), file_entries(paths))
        self.assertFalse(result["eligible"])
        self.assertIn("automatic merge requires exactly one package directory", result["reasons"])

    def test_renaming_infrastructure_into_package_scope_is_blocked(self) -> None:
        paths = ["packages/acl/helper.py"]
        files = [
            {
                "filename": paths[0],
                "previous_filename": "ci/helper.py",
                "status": "renamed",
            }
        ]
        result = self.evaluate(pull_request(paths=paths), files)
        self.assertFalse(result["eligible"])
        self.assertTrue(any("renamed source is outside" in item for item in result["reasons"]))

    def test_incomplete_file_pagination_fails_closed(self) -> None:
        paths = ["packages/acl/README.md", "packages/acl/acl.spec"]
        result = self.evaluate(pull_request(paths=paths), file_entries(paths[:1]))
        self.assertFalse(result["eligible"])
        self.assertTrue(any("file list is incomplete" in item for item in result["reasons"]))

    def test_draft_blocking_label_and_changed_head_each_block(self) -> None:
        paths = ["packages/acl/README.md"]
        cases = (
            (pull_request(paths=paths, draft=True), HEAD, "draft"),
            (pull_request(paths=paths, labels=["needs-human"]), HEAD, "blocking label"),
            (pull_request(paths=paths), "3" * 40, "head changed"),
        )
        for pr, event_head, reason in cases:
            with self.subTest(reason=reason):
                result = self.evaluate(pr, file_entries(paths), event_head=event_head)
                self.assertFalse(result["eligible"])

    def test_pr_1996_shape_is_blocked_even_when_six_package_contexts_succeeded(self) -> None:
        # Ruleset 20579949 did not require the failing Build CI Image or Golden
        # Evaluation checks. Scope must therefore block the infrastructure PR
        # independently of those six successful package contexts.
        paths = [
            ".github/workflows/build-ci-image.yml",
            "ci/Containerfile.riscv64",
            "ci/bootstrap-rootfs.sh",
            "ci/finalize-target-rpmdb.sh",
            "ci/prepare-build-deps.py",
            "ci/rpm-manifest.sh",
            "ci/validate-repository.py",
            "ci/verify-target.sh",
            "scripts/classify-failure",
            "scripts/tests/test_build_and_classify.py",
            "scripts/tests/test_rpm_baseline.py",
            "track.md",
        ]
        required_contexts = {
            name: "success"
            for name in (
                "metadata-validate",
                "source-verify",
                "rpmbuild-riscv64",
                "rpm-install-smoke",
                "patch-policy",
                "merge-policy",
            )
        }
        self.assertEqual(set(required_contexts.values()), {"success"})
        result = self.evaluate(pull_request(paths=paths), file_entries(paths))
        self.assertFalse(result["eligible"])
        self.assertEqual(result["package_id"], "")

    def test_pr_1997_shape_is_blocked_when_six_required_contexts_are_skipped(self) -> None:
        # GitHub accepted the skipped required job conclusions after trusted
        # dispatch failed. Infrastructure scope must still keep auto-merge off.
        paths = [
            ".github/workflows/package-ci.yml",
            "ci/resolve-protected-tooling.py",
            "ci/validate-repository.py",
            "scripts/tests/test_ci_materialize_package_head.py",
            "scripts/tests/test_ci_resolve_protected_tooling.py",
            "track.md",
        ]
        required_contexts = {
            name: "skipped"
            for name in (
                "metadata-validate",
                "source-verify",
                "rpmbuild-riscv64",
                "rpm-install-smoke",
                "patch-policy",
                "merge-policy",
            )
        }
        self.assertEqual(set(required_contexts.values()), {"skipped"})
        result = self.evaluate(pull_request(paths=paths), file_entries(paths))
        self.assertFalse(result["eligible"])
        self.assertEqual(result["package_id"], "")

    def test_workflow_disarms_before_policy_and_arms_only_eligible_scope(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(
            "types: [opened, reopened, synchronize, ready_for_review, converted_to_draft, edited, labeled, unlabeled]",
            workflow,
        )
        self.assertIn("Disarm GitHub Auto-merge before evaluating the current head", workflow)
        self.assertNotIn("branches: [main]", workflow)
        self.assertIn("Bind the current base to the repository default branch", workflow)
        self.assertGreaterEqual(
            workflow.count("steps.protected_base.outputs.protected == 'true'"), 3
        )
        self.assertIn("  configure:\n    if:", workflow)
        self.assertNotIn("    name: auto-merge-policy\n", workflow)
        self.assertIn("ref: ${{ github.event.pull_request.base.sha }}", workflow)
        self.assertIn("ci/evaluate-auto-merge.py", workflow)
        self.assertIn("--paginate --slurp", workflow)
        self.assertIn("steps.policy.outputs.eligible == 'true'", workflow)
        self.assertIn("trap 'rollback_unverified_auto_merge $?' EXIT", workflow)
        self.assertIn(
            "Unable to prove that the leased open PR remained unmerged and Auto-merge was disarmed",
            workflow,
        )
        self.assertEqual(workflow.count("ci/prove-auto-merge-state.py"), 3)
        self.assertEqual(workflow.count("--expected-auto-merge disabled"), 2)
        self.assertEqual(workflow.count("--expected-auto-merge enabled"), 1)
        self.assertTrue(STATE_PROOF.stat().st_mode & 0o111)
        self.assertTrue(BASE_HEAD_PROOF.stat().st_mode & 0o111)
        self.assertTrue(ACTIVATION_PROOF.stat().st_mode & 0o111)
        self.assertEqual(workflow.count("ci/prove-default-branch-head.py"), 2)
        self.assertIn("default-branch-freshness.json", workflow)
        self.assertIn("auto-merge-pre-arm-base-freshness.json", workflow)
        self.assertIn("ci/prove-required-context-active.py", workflow)
        self.assertEqual(workflow.count("ci/prove-required-context-active.py"), 2)
        self.assertIn("auto-merge-pre-arm-activation.json", workflow)
        self.assertIn("steps.activation.outputs.activated == 'true'", workflow)
        self.assertLess(
            workflow.index("Disarm GitHub Auto-merge before evaluating the current head"),
            workflow.index("Bind the current base to the repository default branch"),
        )
        self.assertLess(
            workflow.index("Bind the current base to the repository default branch"),
            workflow.index("Check out the immutable protected-base policy"),
        )
        first_freshness = workflow.index("ci/prove-default-branch-head.py")
        second_freshness = workflow.rindex("ci/prove-default-branch-head.py")
        self.assertLess(first_freshness, workflow.index("Check out the immutable protected-base policy"))
        self.assertLess(second_freshness, workflow.index("--auto --squash"))
        self.assertLess(workflow.index("--disable-auto"), workflow.index("ci/evaluate-auto-merge.py"))
        self.assertLess(workflow.index("ci/evaluate-auto-merge.py"), workflow.index("--auto --squash"))

    def test_first_deployment_bootstrap_can_only_emit_blocked_policy(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        checkout = "ref: ${{ github.event.pull_request.base.sha }}"
        fallback = "if [[ ! -x ci/evaluate-auto-merge.py ]]; then"
        blocked = 'reasons: ["protected-base policy predates evaluator"]'
        false_outputs = "printf 'eligible=false\\npackage_id=\\n' >>\"$GITHUB_OUTPUT\""
        evaluator = "          ci/evaluate-auto-merge.py \\\n"
        disarm = "--disable-auto"
        arm = "--auto --squash"
        self.assertIn(fallback, workflow)
        self.assertIn(blocked, workflow)
        self.assertIn(false_outputs, workflow)
        self.assertNotIn("github.event.pull_request.head.ref", workflow)
        ordered = [disarm, checkout, fallback, evaluator, arm]
        self.assertEqual([workflow.index(item) for item in ordered], sorted(workflow.index(item) for item in ordered))

    def test_stable_auto_merge_context_is_required_and_exactly_read_back(self) -> None:
        ruleset = json.loads(RULESET.read_text(encoding="utf-8"))
        required_rule = next(rule for rule in ruleset["rules"] if rule["type"] == "required_status_checks")
        self.assertTrue(required_rule["parameters"]["strict_required_status_checks_policy"])
        contexts = [
            check["context"]
            for check in required_rule["parameters"]["required_status_checks"]
        ]
        self.assertEqual(
            contexts,
            [
                "metadata-validate",
                "source-verify",
                "rpmbuild-riscv64",
                "rpm-install-smoke",
                "patch-policy",
                "merge-policy",
                "configure",
            ],
        )
        self.assertEqual(
            [check["integration_id"] for check in required_rule["parameters"]["required_status_checks"]],
            [15368] * 7,
        )
        configurator = CONFIGURATOR.read_text(encoding="utf-8")
        self.assertIn('if ! applied_full=$(gh api "repos/$repo/rulesets/$ruleset_id")', configurator)
        self.assertIn('[[ $applied_policy == "$desired_policy" ]]', configurator)
        self.assertIn(
            "ruleset readback does not exactly match the configured protection policy",
            configurator,
        )
        self.assertIn("rollback_ruleset()", configurator)
        self.assertIn("attempting exact policy rollback", configurator)

    def test_mandatory_disarm_has_a_complete_inline_state_proof(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        start = workflow.index("Disarm GitHub Auto-merge before evaluating the current head")
        end = workflow.index("Check out the immutable protected-base policy")
        mandatory = workflow[start:end]
        for marker in (
            'current=$(gh api "repos/$GITHUB_REPOSITORY/pulls/$PR_NUMBER")',
            '.state == "open"',
            ".merged == false",
            ".merged_at == null",
            ".head.sha == $head",
            ".base.sha == $base",
            ".head.repo.full_name == $repo",
            ".base.repo.full_name == $repo",
            ".auto_merge == null",
            "Unable to prove the mandatory Auto-merge disarm state",
        ):
            self.assertIn(marker, mandatory)
        self.assertNotIn("ci/prove-auto-merge-state.py", mandatory)

    def test_post_checkout_transaction_phases_use_the_common_state_proof(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        rollback = workflow.index("rollback-auto-merge-proof.log")
        pre_arm = workflow.index("--auto --squash")
        post_arm = workflow.rindex("--expected-auto-merge enabled")
        proof_positions = []
        start = 0
        while True:
            position = workflow.find("ci/prove-auto-merge-state.py", start)
            if position == -1:
                break
            proof_positions.append(position)
            start = position + 1
        self.assertEqual(len(proof_positions), 3)
        self.assertLess(proof_positions[0], rollback)
        self.assertLess(proof_positions[1], pre_arm)
        self.assertLess(pre_arm, proof_positions[2])
        self.assertLess(proof_positions[2], post_arm)

    def test_pre_arm_revalidation_order_is_inside_the_rollback_transaction(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        arm_block = workflow[workflow.index("      - name: Arm GitHub Auto-merge only after"):]
        merge = arm_block.index("--auto --squash")
        positions = (
            arm_block.index("trap 'rollback_unverified_auto_merge $?' EXIT"),
            arm_block.rindex("--expected-auto-merge disabled", 0, merge),
            arm_block.rindex("ci/prove-default-branch-head.py", 0, merge),
            arm_block.rindex("ci/prove-required-context-active.py", 0, merge),
            merge,
            arm_block.index("--expected-auto-merge enabled", merge),
        )
        self.assertEqual(positions, tuple(sorted(positions)))


if __name__ == "__main__":
    unittest.main()
