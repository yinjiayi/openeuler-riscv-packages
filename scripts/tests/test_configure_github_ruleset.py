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
CONFIGURATOR = REPO / "ci" / "configure-github.sh"


FAKE_GH = textwrap.dedent(r'''
    #!/usr/bin/env python3
    import json
    import os
    from pathlib import Path
    import sys

    args = sys.argv[1:]
    state_path = Path(os.environ["FAKE_STATE"])
    state = json.loads(state_path.read_text())

    def save():
        state_path.write_text(json.dumps(state))

    def input_document():
        index = args.index("--input")
        source = args[index + 1]
        if source == "-":
            return json.load(sys.stdin)
        return json.loads((Path.cwd() / source).read_text())

    if args[:2] == ["auth", "status"]:
        raise SystemExit(0)
    if args[:2] == ["api", "graphql"]:
        print(json.dumps({"data": {"repository": {"pullRequests": {
            "totalCount": 0,
            "pageInfo": {"hasNextPage": False, "endCursor": None},
            "nodes": [],
        }}, "rateLimit": {"cost": 1, "remaining": 4999, "resetAt": "2026-09-03T00:00:00Z"}}}))
        raise SystemExit(0)
    if not args or args[0] != "api":
        raise SystemExit(90)

    method = "GET"
    if "--method" in args:
        method = args[args.index("--method") + 1]
    endpoint = next((item for item in args[1:] if item.startswith("repos/")), "")
    repo = "repos/yinjiayi/openeuler-riscv-packages"

    if endpoint == repo and method == "GET":
        print(json.dumps(state["repository"]))
    elif endpoint == repo and method == "PATCH":
        for index, argument in enumerate(args):
            if argument != "-F" or index + 1 >= len(args):
                continue
            key, value = args[index + 1].split("=", 1)
            if key in {
                "allow_auto_merge",
                "allow_squash_merge",
                "allow_merge_commit",
                "allow_rebase_merge",
                "delete_branch_on_merge",
            }:
                state["repository"][key] = value == "true"
        save()
    elif endpoint == repo + "/rulesets" and method == "GET":
        if os.environ["FAKE_SCENARIO"] == "create-unverified" and state.get("deleted"):
            raise SystemExit(19)
        print(json.dumps([[{"id": item["id"], "name": item["name"]} for item in state["rulesets"]]]))
    elif endpoint.startswith(repo + "/rulesets/") and method == "GET":
        wanted = int(endpoint.rsplit("/", 1)[1])
        item = next((item for item in state["rulesets"] if item["id"] == wanted), None)
        if item is None:
            raise SystemExit(4)
        if os.environ["FAKE_SCENARIO"] == "readback-invalid" and state["put_count"] == 1:
            print('"malformed-policy-shape"')
            raise SystemExit(0)
        if os.environ["FAKE_SCENARIO"] == "readback-missing-bypass" and state["put_count"] == 1:
            item = dict(item)
            item.pop("bypass_actors", None)
        print(json.dumps(item))
    elif endpoint.startswith(repo + "/rulesets/") and method == "PUT":
        wanted = int(endpoint.rsplit("/", 1)[1])
        document = input_document()
        state["put_count"] += 1
        document["id"] = wanted
        document["source"] = repo.split("/", 1)[1]
        document["source_type"] = "Repository"
        if os.environ["FAKE_SCENARIO"] == "update-mismatch" and state["put_count"] == 1:
            document["enforcement"] = "evaluate"
        if os.environ["FAKE_SCENARIO"] == "update-wrong-integration" and state["put_count"] == 1:
            document["rules"][-1]["parameters"]["required_status_checks"][0]["integration_id"] = 1
        state["rulesets"] = [document if item["id"] == wanted else item for item in state["rulesets"]]
        save()
    elif endpoint == repo + "/rulesets" and method == "POST":
        document = input_document()
        document["id"] = 777
        document["source"] = repo.split("/", 1)[1]
        document["source_type"] = "Repository"
        state["rulesets"].append(document)
        save()
        scenario = os.environ["FAKE_SCENARIO"]
        if scenario in ("create-invalid", "create-unverified"):
            print("{}")
        elif scenario == "create-raw":
            print("{")
        elif scenario == "create-scalar":
            print('"invalid"')
        else:
            print(json.dumps(document))
    elif endpoint.startswith(repo + "/rulesets/") and method == "DELETE":
        wanted = int(endpoint.rsplit("/", 1)[1])
        state["rulesets"] = [item for item in state["rulesets"] if item["id"] != wanted]
        state["deleted"] = True
        save()
    elif endpoint == repo + "/actions/permissions/fork-pr-contributor-approval" and method == "GET" and "--jq" in args:
        print("first_time_contributors_new_to_github")
    elif method == "GET":
        print("{}")
    else:
        pass
''').lstrip()


class ConfigureGithubRulesetTests(unittest.TestCase):
    def run_apply(self, scenario: str, *, existing: bool, expected: int) -> tuple[subprocess.CompletedProcess[str], dict]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake_gh = root / "gh"
            fake_gh.write_text(FAKE_GH, encoding="utf-8")
            fake_gh.chmod(0o755)
            desired = json.loads((REPO / ".github/rulesets/main.json").read_text())
            previous = json.loads(json.dumps(desired))
            previous["id"] = 20579949
            previous["source"] = "yinjiayi/openeuler-riscv-packages"
            previous["source_type"] = "Repository"
            previous["rules"][-1]["parameters"]["required_status_checks"] = previous["rules"][-1]["parameters"]["required_status_checks"][:-1]
            if scenario == "previous-missing-bypass":
                previous.pop("bypass_actors")
            if scenario == "previous-wrong-source":
                previous["source_type"] = "Organization"
            state_path = root / "state.json"
            state_path.write_text(json.dumps({
                "repository": {
                    "visibility": "public",
                    "default_branch": "main",
                    "allow_auto_merge": True,
                    "allow_squash_merge": True,
                    "allow_merge_commit": False,
                    "allow_rebase_merge": False,
                    "delete_branch_on_merge": True,
                },
                "rulesets": [previous] if existing else [],
                "put_count": 0,
            }))
            env = os.environ.copy()
            env.update({
                "PATH": str(root) + os.pathsep + env["PATH"],
                "FAKE_STATE": str(state_path),
                "FAKE_SCENARIO": scenario,
                "REQUIRED_CONTEXT_AUDIT_OUTPUT": str(root / "audit.json"),
                "PYTHONDONTWRITEBYTECODE": "1",
            })
            completed = subprocess.run(
                [str(CONFIGURATOR), "--apply"],
                cwd=REPO,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(completed.returncode, expected, completed.stderr)
            return completed, json.loads(state_path.read_text())

    def test_successful_update_exactly_applies_desired_ruleset(self) -> None:
        completed, state = self.run_apply("success", existing=True, expected=0)
        self.assertTrue(json.loads(completed.stdout)["writes_performed"])
        self.assertIs(state["repository"]["allow_auto_merge"], False)
        self.assertEqual(state["rulesets"][0]["enforcement"], "active")
        checks = state["rulesets"][0]["rules"][-1]["parameters"]["required_status_checks"]
        self.assertEqual(checks[-1]["context"], "configure")

    def test_readback_mismatch_restores_the_previous_policy(self) -> None:
        for scenario in ("update-mismatch", "update-wrong-integration"):
            with self.subTest(scenario=scenario):
                completed, state = self.run_apply(scenario, existing=True, expected=1)
                self.assertIn("readback does not exactly match", completed.stderr)
                checks = state["rulesets"][0]["rules"][-1]["parameters"]["required_status_checks"]
                self.assertNotIn("configure", [item["context"] for item in checks])
                self.assertEqual(state["put_count"], 2)

    def test_malformed_create_response_discovers_deletes_and_lists_absence(self) -> None:
        for scenario in ("create-invalid", "create-raw", "create-scalar"):
            with self.subTest(scenario=scenario):
                completed, state = self.run_apply(scenario, existing=False, expected=1)
                self.assertIn("attempting discovered-rule rollback", completed.stderr)
                self.assertEqual(state["rulesets"], [])

    def test_malformed_exact_readback_restores_the_previous_policy(self) -> None:
        for scenario in ("readback-invalid", "readback-missing-bypass"):
            with self.subTest(scenario=scenario):
                completed, state = self.run_apply(scenario, existing=True, expected=1)
                self.assertIn("readback identity is invalid", completed.stderr)
                checks = state["rulesets"][0]["rules"][-1]["parameters"]["required_status_checks"]
                self.assertNotIn("configure", [item["context"] for item in checks])
                self.assertEqual(state["put_count"], 2)

    def test_missing_previous_bypass_stops_before_ruleset_mutation(self) -> None:
        for scenario in ("previous-missing-bypass", "previous-wrong-source"):
            with self.subTest(scenario=scenario):
                completed, state = self.run_apply(scenario, existing=True, expected=1)
                self.assertIn("existing ruleset readback identity or policy shape is invalid", completed.stderr)
                self.assertEqual(state["put_count"], 0)

    def test_delete_without_successful_absence_listing_is_unverified(self) -> None:
        completed, state = self.run_apply("create-unverified", existing=False, expected=1)
        self.assertIn("rollback could not be verified", completed.stderr)
        self.assertEqual(state["rulesets"], [])


if __name__ == "__main__":
    unittest.main()
