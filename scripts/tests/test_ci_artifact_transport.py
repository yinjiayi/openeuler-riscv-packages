# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import pathlib
import json
import os
import re
import runpy
import textwrap
import unittest
from unittest import mock


REPO = pathlib.Path(__file__).resolve().parents[2]
WORKFLOW = REPO / ".github/workflows/package-ci.yml"
VALIDATE = runpy.run_path(str(REPO / "ci/validate-repository.py"))["artifact_transport_errors"]


def action_id_selection(artifacts: list[tuple[str, int]], selected: list[int]) -> list[int]:
    """Model the pinned download action: per-name max-ID filter, then exact IDs."""
    latest: dict[str, int] = {}
    for name, artifact_id in sorted(artifacts, key=lambda row: row[1], reverse=True):
        latest.setdefault(name, artifact_id)
    return [artifact_id for artifact_id in latest.values() if artifact_id in selected]


class ArtifactTransportTests(unittest.TestCase):
    def test_workflow_exposes_all_producers_and_consumes_only_exact_ids(self) -> None:
        self.assertEqual(VALIDATE(WORKFLOW.read_text()), [])

    def test_same_name_max_id_regression_with_actual_nonmonotonic_ids(self) -> None:
        old, new = 12085895018, 12085647456
        name = "package-ci-source-libinjection-38991391258"
        self.assertEqual(action_id_selection([(name, old), (name, new)], [new]), [])
        unique = [(name + "-attempt-1", old), (name + "-attempt-2", new)]
        self.assertEqual(action_id_selection(unique, [new]), [new])

    def test_failed_only_rerun_retains_successful_prerequisite_ids(self) -> None:
        # Repository/source succeeded in attempt 1. Only build/smoke rerun in 2.
        artifacts = [("repository-attempt-1", 90), ("source-attempt-1", 80),
                     ("build-attempt-1", 70), ("build-attempt-2", 60)]
        source_output, repository_output, build_output = 80, 90, 60
        self.assertEqual(action_id_selection(artifacts, [source_output]), [80])
        self.assertEqual(action_id_selection(artifacts, [repository_output]), [90])
        self.assertEqual(action_id_selection(artifacts, [build_output]), [60])
        self.assertEqual(action_id_selection(artifacts, [0]), [])

    def test_policy_rejects_same_name_upload_and_current_attempt_download(self) -> None:
        workflow = WORKFLOW.read_text()
        self.assertTrue(VALIDATE(workflow.replace("-attempt-${{ github.run_attempt }}", "")))
        changed = workflow.replace("artifact-ids: ${{ needs.source-verify.outputs.artifact_id || '0' }}",
                                   "name: package-ci-source-demo-${{ github.run_attempt }}")
        self.assertTrue(VALIDATE(changed))

    def test_policy_rejects_missing_producer_and_empty_selector_fallback(self) -> None:
        workflow = WORKFLOW.read_text()
        self.assertTrue(VALIDATE(workflow.replace("steps.upload.outputs.artifact-id", "steps.other.outputs.artifact-id", 1)))
        self.assertTrue(VALIDATE(workflow.replace("needs.source-verify.outputs.artifact_id || '0'", "needs.source-verify.outputs.artifact_id", 1)))
        self.assertTrue(VALIDATE(re.sub(r"artifact-ids:.*", "pattern: package-ci-*", workflow)))
        self.assertTrue(VALIDATE(workflow.replace("merge-multiple: true", "merge-multiple: false", 1)))

    def test_ci_state_rejects_missing_successful_producer_but_allows_absent_failed_output(self) -> None:
        workflow = WORKFLOW.read_text().split("- name: Validate artifact producer outputs before collecting results", 1)[1]
        script = textwrap.dedent(workflow.split("python3 - <<'PY'\n", 1)[1].split("\n          PY", 1)[0])
        producers = ("prepare", "metadata-validate", "patch-policy", "source-verify",
                     "repository-snapshot", "merge-policy", "rpmbuild-riscv64", "rpm-install-smoke")
        needs = {name: {"result": "success", "outputs": {"artifact_id": str(index + 1)}}
                 for index, name in enumerate(producers)}

        def validate() -> None:
            with mock.patch.dict(os.environ, {"PACKAGE_CI_NEEDS": json.dumps(needs)}):
                exec(compile(script, "workflow-artifact-output-validation", "exec"), {})

        validate()
        needs["metadata-validate"]["outputs"]["artifact_id"] = ""
        with self.assertRaisesRegex(SystemExit, "Successful producer has no artifact ID"):
            validate()
        needs["metadata-validate"]["result"] = "failure"
        validate()
        for invalid in ("0", "9,10", "not-an-id", "1"):
            needs["metadata-validate"]["outputs"]["artifact_id"] = invalid
            with self.assertRaisesRegex(SystemExit, "Invalid or duplicate"):
                validate()

    def test_each_requested_ci_state_id_fails_individually_when_missing(self) -> None:
        workflow = WORKFLOW.read_text().split("  ci-state:\n", 1)[1]
        selectors = re.findall(r"artifact-ids: (.+)", workflow)
        self.assertEqual(len(selectors), 8)
        self.assertTrue(all("format(" not in selector and " || '0'" in selector for selector in selectors))
        self.assertEqual(len(set(re.findall(r"path: (artifacts/all-results/[^\n]+)", workflow))), 8)
        self.assertNotIn("continue-on-error", workflow)
        # Pinned action throws none-found for each one-ID download, rather than
        # warning about a missing subset of a multi-ID selector.
        def download_one(artifact_id: int) -> int:
            selected = action_id_selection([("metadata-attempt-1", 100)], [artifact_id])
            if not selected:
                raise ValueError("None of the provided artifact IDs were found")
            return selected[0]
        self.assertEqual(download_one(100), 100)
        with self.assertRaisesRegex(ValueError, "None of the provided"):
            download_one(99)


if __name__ == "__main__":
    unittest.main()
