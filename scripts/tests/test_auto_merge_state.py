# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest


REPO = Path(__file__).resolve().parents[2]
PROOF = REPO / "ci" / "prove-auto-merge-state.py"
HEAD = "1" * 40
BASE = "2" * 40
BASE_REF = "main"
REPOSITORY = "yinjiayi/openeuler-riscv-packages"


def pull_request(*, auto_merge: object = None) -> dict[str, object]:
    return {
        "state": "open",
        "merged": False,
        "merged_at": None,
        "head": {"sha": HEAD, "repo": {"full_name": REPOSITORY}},
        "base": {"sha": BASE, "ref": BASE_REF, "repo": {"full_name": REPOSITORY}},
        "auto_merge": auto_merge,
    }


class AutoMergeStateProofTests(unittest.TestCase):
    def run_proof(
        self,
        document: object,
        *,
        expected_auto_merge: str = "disabled",
        api_exit: int = 0,
        expected: int = 0,
        event_head: str = HEAD,
        event_base: str = BASE,
        event_base_ref: str = BASE_REF,
        repository: str = REPOSITORY,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            response = root / "response.json"
            response.write_text(json.dumps(document) + "\n", encoding="utf-8")
            fake_gh = root / "gh"
            fake_gh.write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env python3
                    import os
                    from pathlib import Path
                    import sys

                    expected = ["api", os.environ["EXPECTED_API_PATH"]]
                    if sys.argv[1:] != expected:
                        print("unexpected gh arguments", file=sys.stderr)
                        raise SystemExit(97)
                    exit_code = int(os.environ.get("FAKE_GH_EXIT", "0"))
                    if exit_code:
                        print("simulated API failure", file=sys.stderr)
                        raise SystemExit(exit_code)
                    sys.stdout.write(Path(os.environ["FAKE_GH_RESPONSE"]).read_text())
                    """
                ),
                encoding="utf-8",
            )
            fake_gh.chmod(0o755)
            environment = os.environ.copy()
            environment.update(
                {
                    "PATH": f"{root}{os.pathsep}{environment['PATH']}",
                    "EXPECTED_API_PATH": f"repos/{REPOSITORY}/pulls/2006",
                    "FAKE_GH_RESPONSE": str(response),
                    "FAKE_GH_EXIT": str(api_exit),
                }
            )
            completed = subprocess.run(
                [
                    str(PROOF),
                    "--repo",
                    repository,
                    "--pr-number",
                    "2006",
                    "--event-head",
                    event_head,
                    "--event-base",
                    event_base,
                    "--event-base-ref",
                    event_base_ref,
                    "--expected-auto-merge",
                    expected_auto_merge,
                ],
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(completed.returncode, expected, completed.stderr)
            return completed

    def test_open_unmerged_exact_lease_with_auto_merge_disabled_passes(self) -> None:
        completed = self.run_proof(pull_request())
        self.assertIn("state proof passed", completed.stdout)
        self.assertIn("Auto-merge is disabled", completed.stdout)

    def test_open_unmerged_exact_lease_with_auto_merge_enabled_passes(self) -> None:
        completed = self.run_proof(
            pull_request(auto_merge={"merge_method": "squash"}),
            expected_auto_merge="enabled",
        )
        self.assertIn("Auto-merge is enabled", completed.stdout)

    def test_closed_merged_or_merge_timestamp_each_fails_closed(self) -> None:
        cases = (
            ({"state": "closed"}, "not open"),
            ({"merged": True}, "not proven unmerged"),
            ({"merged_at": "2026-09-03T00:00:00Z"}, "merge timestamp"),
        )
        for changes, message in cases:
            with self.subTest(changes=changes):
                document = pull_request()
                document.update(changes)
                completed = self.run_proof(document, expected=2)
                self.assertIn(message, completed.stderr)

    def test_head_and_base_sha_changes_each_fail_closed(self) -> None:
        for key, message in (("head", "head changed"), ("base", "base changed")):
            with self.subTest(key=key):
                document = pull_request()
                document[key]["sha"] = "3" * 40  # type: ignore[index]
                completed = self.run_proof(document, expected=2)
                self.assertIn(message, completed.stderr)

    def test_base_ref_change_fails_closed(self) -> None:
        document = pull_request()
        document["base"]["ref"] = "release"  # type: ignore[index]
        completed = self.run_proof(document, expected=2)
        self.assertIn("base ref changed", completed.stderr)

    def test_head_and_base_repository_changes_each_fail_closed(self) -> None:
        for key, message in (
            ("head", "head repository changed"),
            ("base", "base repository changed"),
        ):
            with self.subTest(key=key):
                document = pull_request()
                document[key]["repo"]["full_name"] = "someone/fork"  # type: ignore[index]
                completed = self.run_proof(document, expected=2)
                self.assertIn(message, completed.stderr)

    def test_auto_merge_null_and_non_null_expectations_are_exact(self) -> None:
        disabled = self.run_proof(
            pull_request(auto_merge={"merge_method": "squash"}), expected=2
        )
        self.assertIn("Auto-merge is not disabled", disabled.stderr)
        enabled = self.run_proof(
            pull_request(), expected_auto_merge="enabled", expected=2
        )
        self.assertIn("auto_merge must be a JSON object", enabled.stderr)

    def test_enabled_requires_an_object_with_the_squash_method(self) -> None:
        for value in ({}, {"merge_method": "merge"}, "enabled", False):
            with self.subTest(value=value):
                completed = self.run_proof(
                    pull_request(auto_merge=value),
                    expected_auto_merge="enabled",
                    expected=2,
                )
                self.assertTrue(
                    "squash" in completed.stderr or "must be a JSON object" in completed.stderr
                )

    def test_api_error_and_invalid_json_each_fail_closed(self) -> None:
        api_error = self.run_proof(pull_request(), api_exit=1, expected=2)
        self.assertIn("API request failed", api_error.stderr)
        invalid = self.run_proof("not an object", expected=2)
        self.assertIn("must be a JSON object", invalid.stderr)

    def test_missing_required_api_fields_each_fail_closed(self) -> None:
        for field in ("state", "merged", "merged_at", "head", "base", "auto_merge"):
            with self.subTest(field=field):
                document = pull_request()
                del document[field]
                completed = self.run_proof(document, expected=2)
                self.assertIn("state proof failed", completed.stderr)

    def test_invalid_cli_identity_is_rejected_before_api_acceptance(self) -> None:
        for arguments, message in (
            ({"repository": "invalid"}, "owner/name"),
            ({"event_head": "main"}, "event head"),
            ({"event_base": "main"}, "event base"),
            ({"event_base_ref": "../unsafe"}, "event base ref"),
        ):
            with self.subTest(arguments=arguments):
                completed = self.run_proof(pull_request(), expected=2, **arguments)
                self.assertIn(message, completed.stderr)


if __name__ == "__main__":
    unittest.main()
