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
PROOF = REPO / "ci" / "prove-required-context-active.py"
REPOSITORY = "yinjiayi/openeuler-riscv-packages"
RULESET_ID = 20579949


def live_ruleset(*, enforcement: str = "active", context: str = "configure") -> dict:
    document = json.loads((REPO / ".github/rulesets/main.json").read_text(encoding="utf-8"))
    document["id"] = RULESET_ID
    document["updated_at"] = "2026-09-03T08:00:00Z"
    document["current_user_can_bypass"] = "never"
    document["node_id"] = "RRS_test_ruleset_node"
    document["source"] = REPOSITORY
    document["source_type"] = "Repository"
    document["enforcement"] = enforcement
    required = next(rule for rule in document["rules"] if rule["type"] == "required_status_checks")
    for check in required["parameters"]["required_status_checks"]:
        if check["context"] == "configure":
            check["context"] = context
    return document


class RequiredContextActivationTests(unittest.TestCase):
    def run_proof(
        self,
        *,
        listing: object | None = None,
        exact: object | None = None,
        api_failure: str = "",
        expected: int,
    ) -> dict:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = root / "ruleset.json"
            config.write_text(
                (REPO / ".github/rulesets/main.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            listing_path = root / "listing.json"
            listing_path.write_text(json.dumps(listing if listing is not None else [[{
                "id": RULESET_ID,
                "name": "protect-main-zero-review-auto-merge",
            }]]), encoding="utf-8")
            exact_path = root / "exact.json"
            exact_path.write_text(json.dumps(exact if exact is not None else live_ruleset()), encoding="utf-8")
            fake_gh = root / "gh"
            fake_gh.write_text(textwrap.dedent("""\
                #!/usr/bin/env python3
                import os
                from pathlib import Path
                import sys

                args = sys.argv[1:]
                failure = os.environ.get("FAKE_FAILURE", "")
                if args == ["api", os.environ["LIST_PATH"], "--paginate", "--slurp"]:
                    if failure == "list":
                        raise SystemExit(17)
                    sys.stdout.write(Path(os.environ["LIST_RESPONSE"]).read_text())
                    raise SystemExit(0)
                if args == ["api", os.environ["EXACT_PATH"]]:
                    if failure == "exact":
                        raise SystemExit(18)
                    sys.stdout.write(Path(os.environ["EXACT_RESPONSE"]).read_text())
                    raise SystemExit(0)
                raise SystemExit(97)
            """), encoding="utf-8")
            fake_gh.chmod(0o755)
            env = os.environ.copy()
            env.update({
                "PATH": str(root) + os.pathsep + env["PATH"],
                "LIST_PATH": f"repos/{REPOSITORY}/rulesets",
                "EXACT_PATH": f"repos/{REPOSITORY}/rulesets/{RULESET_ID}",
                "LIST_RESPONSE": str(listing_path),
                "EXACT_RESPONSE": str(exact_path),
                "FAKE_FAILURE": api_failure,
            })
            completed = subprocess.run([
                str(PROOF),
                "--repository", REPOSITORY,
                "--context", "configure",
                "--ruleset-config", str(config),
            ], env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            self.assertEqual(completed.returncode, expected, completed.stderr)
            return json.loads(completed.stdout)

    def test_active_exact_ruleset_context_passes(self) -> None:
        self.assertTrue(self.run_proof(expected=0)["activated"])

    def test_absent_inactive_or_missing_context_is_safe_noop(self) -> None:
        cases = (
            {"listing": [[]]},
            {"exact": live_ruleset(enforcement="evaluate")},
            {"exact": live_ruleset(context="another-context")},
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                self.assertFalse(self.run_proof(expected=3, **arguments)["activated"])

    def test_ambiguous_identity_malformed_shape_and_api_failure_fail_closed(self) -> None:
        duplicate = [[
            {"id": RULESET_ID, "name": "protect-main-zero-review-auto-merge"},
            {"id": RULESET_ID + 1, "name": "protect-main-zero-review-auto-merge"},
        ]]
        wrong_integration = live_ruleset()
        required = next(
            rule for rule in wrong_integration["rules"]
            if rule["type"] == "required_status_checks"
        )
        next(
            check for check in required["parameters"]["required_status_checks"]
            if check["context"] == "configure"
        )["integration_id"] = 1
        duplicate_context = live_ruleset()
        duplicate_required = next(
            rule for rule in duplicate_context["rules"]
            if rule["type"] == "required_status_checks"
        )
        duplicate_required["parameters"]["required_status_checks"].append({
            "context": "configure", "integration_id": 15368,
        })
        cases = (
            {"listing": duplicate},
            {"listing": {"not": "pages"}},
            {"exact": {key: value for key, value in live_ruleset().items() if key != "current_user_can_bypass"}},
            {"exact": {**live_ruleset(), "bypass_actors": [{"actor_id": 1}]}},
            {"exact": {**live_ruleset(), "bypass_actors": None}},
            {"exact": {**live_ruleset(), "bypass_actors": {}}},
            {"exact": {**live_ruleset(), "source": "other/repository"}},
            {"exact": {**live_ruleset(), "source_type": "Organization"}},
            {"exact": {**live_ruleset(), "node_id": ""}},
            {"exact": {**live_ruleset(), "node_id": 123}},
            {"exact": wrong_integration},
            {"exact": duplicate_context},
            {"exact": {**live_ruleset(), "conditions": {"ref_name": {
                "include": ["~DEFAULT_BRANCH"], "exclude": ["~DEFAULT_BRANCH"]
            }}}},
            {"api_failure": "list"},
            {"api_failure": "exact"},
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                result = self.run_proof(expected=2, **arguments)
                self.assertFalse(result["activated"])
                self.assertIn("error", result)

    def test_hidden_bypass_uses_current_workflow_token_bypass_proof(self) -> None:
        full = live_ruleset()
        hidden = {key: value for key, value in full.items() if key != "bypass_actors"}
        result = self.run_proof(exact=hidden, expected=0)
        self.assertEqual(result["current_user_can_bypass"], "never")
        self.assertEqual(result["bypass_actors_visibility"], "not-returned")
        self.assertFalse(result["bypass_actors_verified_empty"])

    def test_non_never_or_missing_current_user_bypass_fails_closed(self) -> None:
        cases = (
            {"exact": {**live_ruleset(), "current_user_can_bypass": "always"}},
            {"exact": {**live_ruleset(), "current_user_can_bypass": "pull_requests_only"}},
            {"exact": {**live_ruleset(), "current_user_can_bypass": "exempt"}},
            {"exact": {**live_ruleset(), "current_user_can_bypass": "unknown"}},
            {"exact": {**live_ruleset(), "current_user_can_bypass": None}},
            {"exact": {**live_ruleset(), "current_user_can_bypass": []}},
            {"exact": {key: value for key, value in live_ruleset().items()
                       if key != "current_user_can_bypass"}},
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                result = self.run_proof(expected=2, **arguments)
                self.assertFalse(result["activated"])
                self.assertIn("error", result)

    def test_missing_context_is_inactive_before_hidden_bypass_is_relevant(self) -> None:
        hidden = {
            key: value
            for key, value in live_ruleset(context="another-context").items()
            if key != "bypass_actors"
        }
        result = self.run_proof(exact=hidden, expected=3)
        self.assertFalse(result["activated"])
        self.assertEqual(result["occurrences"], 0)


if __name__ == "__main__":
    unittest.main()
