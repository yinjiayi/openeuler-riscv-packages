#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Prove that one live active ruleset requires a context on the default branch."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class ActivationError(RuntimeError):
    """The live ruleset state is malformed, ambiguous, or unavailable."""


def api_json(arguments: list[str]) -> Any:
    try:
        completed = subprocess.run(
            ["gh", "api", *arguments],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise ActivationError("cannot execute the GitHub CLI") from error
    if completed.returncode != 0:
        raise ActivationError("GitHub ruleset API request failed")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise ActivationError("GitHub ruleset API response is not valid JSON") from error


def load_expected(path: Path) -> Mapping[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ActivationError("committed ruleset configuration is unreadable") from error
    if not isinstance(document, Mapping):
        raise ActivationError("committed ruleset configuration is not an object")
    if not isinstance(document.get("name"), str) or not document.get("name"):
        raise ActivationError("committed ruleset name is missing")
    return document


def require_mapping(value: Any, description: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ActivationError(f"{description} is not an object")
    return value


def policy_projection(document: Mapping[str, Any]) -> dict[str, Any]:
    conditions = require_mapping(document.get("conditions"), "ruleset conditions")
    ref_name = require_mapping(conditions.get("ref_name"), "ruleset ref-name conditions")
    includes = ref_name.get("include")
    excludes = ref_name.get("exclude")
    if not isinstance(includes, list) or not isinstance(excludes, list):
        raise ActivationError("ruleset ref-name include/exclude fields are not lists")
    raw_rules = document.get("rules")
    if not isinstance(raw_rules, list):
        raise ActivationError("ruleset rules are not a list")
    rules: list[dict[str, Any]] = []
    for raw_rule in raw_rules:
        rule = require_mapping(raw_rule, "ruleset rule")
        rule_type = rule.get("type")
        if not isinstance(rule_type, str) or not rule_type:
            raise ActivationError("ruleset rule type is missing")
        if rule_type == "pull_request":
            parameters = require_mapping(rule.get("parameters"), "pull-request rule parameters")
            rules.append({
                "type": rule_type,
                "parameters": {
                    "allowed_merge_methods": parameters.get("allowed_merge_methods"),
                    "dismiss_stale_reviews_on_push": parameters.get("dismiss_stale_reviews_on_push"),
                    "require_code_owner_review": parameters.get("require_code_owner_review"),
                    "require_last_push_approval": parameters.get("require_last_push_approval"),
                    "required_approving_review_count": parameters.get("required_approving_review_count"),
                    "required_review_thread_resolution": parameters.get("required_review_thread_resolution"),
                },
            })
        elif rule_type == "required_status_checks":
            parameters = require_mapping(rule.get("parameters"), "required-status-check rule parameters")
            raw_checks = parameters.get("required_status_checks")
            if not isinstance(raw_checks, list):
                raise ActivationError("required status checks are not a list")
            checks = []
            for raw_check in raw_checks:
                check = require_mapping(raw_check, "required status check")
                checks.append({
                    "context": check.get("context"),
                    "integration_id": check.get("integration_id"),
                })
            rules.append({
                "type": rule_type,
                "parameters": {
                    "strict_required_status_checks_policy": parameters.get(
                        "strict_required_status_checks_policy"
                    ),
                    "do_not_enforce_on_create": parameters.get("do_not_enforce_on_create"),
                    "required_status_checks": checks,
                },
            })
        else:
            rules.append({"type": rule_type})
    return {
        "name": document.get("name"),
        "target": document.get("target"),
        "enforcement": document.get("enforcement"),
        "conditions": {"ref_name": {"include": includes, "exclude": excludes}},
        "rules": rules,
    }


def prove(repository: str, context: str, config: Path) -> dict[str, Any]:
    expected = load_expected(config)
    expected_name = str(expected["name"])
    pages = api_json([f"repos/{repository}/rulesets", "--paginate", "--slurp"])
    if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
        raise ActivationError("ruleset listing is not a paginated array")
    matches = [
        item for page in pages for item in page
        if isinstance(item, Mapping) and item.get("name") == expected_name
    ]
    if not matches:
        return {"activated": False, "reason": "configured ruleset is absent", "ruleset": expected_name}
    if len(matches) != 1:
        raise ActivationError("configured ruleset name is not unique")
    ruleset_id = matches[0].get("id")
    if not isinstance(ruleset_id, int) or ruleset_id <= 0:
        raise ActivationError("configured ruleset id is not a positive integer")
    live = api_json([f"repos/{repository}/rulesets/{ruleset_id}"])
    if not isinstance(live, Mapping):
        raise ActivationError("exact ruleset response is not an object")
    if live.get("id") != ruleset_id or live.get("name") != expected_name:
        raise ActivationError("exact ruleset identity changed")
    rules = live.get("rules")
    if not isinstance(rules, list):
        raise ActivationError("exact ruleset rules are missing")
    required_rules = [item for item in rules if isinstance(item, Mapping) and item.get("type") == "required_status_checks"]
    if len(required_rules) != 1:
        raise ActivationError("ruleset does not have exactly one required-status-checks rule")
    parameters = required_rules[0].get("parameters")
    checks = parameters.get("required_status_checks") if isinstance(parameters, Mapping) else None
    if not isinstance(checks, list):
        raise ActivationError("required status checks are missing")
    occurrences = sum(
        1 for check in checks
        if isinstance(check, Mapping) and check.get("context") == context
    )
    if occurrences != 1:
        if occurrences > 1:
            raise ActivationError("required context appears more than once")
        return {
            "activated": False,
            "reason": "required context is not present exactly once",
            "ruleset_id": ruleset_id,
            "occurrences": occurrences,
        }
    expected_rules = expected.get("rules")
    if not isinstance(expected_rules, list):
        raise ActivationError("committed ruleset rules are missing")
    expected_required = [
        item for item in expected_rules
        if isinstance(item, Mapping) and item.get("type") == "required_status_checks"
    ]
    if len(expected_required) != 1:
        raise ActivationError("committed ruleset does not have exactly one required-status-checks rule")
    expected_parameters = expected_required[0].get("parameters")
    expected_checks = (
        expected_parameters.get("required_status_checks")
        if isinstance(expected_parameters, Mapping) else None
    )
    if not isinstance(expected_checks, list):
        raise ActivationError("committed required status checks are missing")
    expected_contexts = [
        check for check in expected_checks
        if isinstance(check, Mapping) and check.get("context") == context
    ]
    if len(expected_contexts) != 1:
        raise ActivationError("committed required context is not unique")
    expected_integration_id = expected_contexts[0].get("integration_id")
    if not isinstance(expected_integration_id, int) or expected_integration_id <= 0:
        raise ActivationError("committed required context integration id is invalid")
    live_contexts = [
        check for check in checks
        if isinstance(check, Mapping) and check.get("context") == context
    ]
    if live_contexts[0].get("integration_id") != expected_integration_id:
        raise ActivationError("live required context integration id differs from configuration")
    if live.get("enforcement") != "active":
        return {
            "activated": False,
            "reason": "configured ruleset is not active",
            "ruleset_id": ruleset_id,
        }
    if live.get("target") != "branch":
        raise ActivationError("configured ruleset is not a branch ruleset")
    if live.get("source") != repository or live.get("source_type") != "Repository":
        raise ActivationError("live ruleset is not owned by the target repository")
    if not isinstance(live.get("node_id"), str) or not live.get("node_id"):
        raise ActivationError("live ruleset node id is missing")
    current_user_can_bypass = live.get("current_user_can_bypass")
    if not isinstance(current_user_can_bypass, str):
        raise ActivationError("live ruleset current-user bypass state is missing")
    if current_user_can_bypass != "never":
        raise ActivationError("workflow token may bypass the live ruleset")
    live_visible = policy_projection(live)
    expected_visible = policy_projection(expected)
    if live_visible != expected_visible:
        raise ActivationError("ruleset visible policy differs from protected configuration")
    live_conditions = live.get("conditions")
    ref_name = live_conditions.get("ref_name") if isinstance(live_conditions, Mapping) else None
    includes = ref_name.get("include") if isinstance(ref_name, Mapping) else None
    excludes = ref_name.get("exclude") if isinstance(ref_name, Mapping) else None
    if includes != ["~DEFAULT_BRANCH"] or excludes != []:
        raise ActivationError("ruleset does not exclusively include the default branch")
    if "bypass_actors" not in expected:
        raise ActivationError("committed ruleset bypass actors field is missing")
    expected_bypass = expected["bypass_actors"]
    if not isinstance(expected_bypass, list):
        raise ActivationError("committed ruleset bypass actors field is not a list")
    if expected_bypass != []:
        raise ActivationError("committed ruleset bypass actors are nonempty")
    if "bypass_actors" in live:
        live_bypass = live["bypass_actors"]
        if not isinstance(live_bypass, list):
            raise ActivationError("live ruleset bypass actors field is not a list")
        if live_bypass != []:
            raise ActivationError("live ruleset bypass actors are nonempty")
        bypass_visibility = "visible"
        bypass_verified_empty = True
    else:
        bypass_visibility = "not-returned"
        bypass_verified_empty = False
    return {
        "schema_version": 1,
        "activated": True,
        "reason": "live ruleset requires the pinned context and the workflow token cannot bypass it",
        "repository": repository,
        "context": context,
        "ruleset_id": ruleset_id,
        "node_id": live["node_id"],
        "current_user_can_bypass": current_user_can_bypass,
        "bypass_actors_visibility": bypass_visibility,
        "bypass_actors_verified_empty": bypass_verified_empty,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--context", required=True)
    parser.add_argument("--ruleset-config", required=True, type=Path)
    args = parser.parse_args()
    if REPOSITORY.fullmatch(args.repository) is None:
        parser.error("--repository must be OWNER/NAME")
    if not args.context.strip():
        parser.error("--context must not be empty")
    try:
        result = prove(args.repository, args.context, args.ruleset_config)
    except ActivationError as error:
        json.dump({"activated": False, "error": str(error)}, sys.stdout, sort_keys=True)
        sys.stdout.write("\n")
        return 2
    json.dump(result, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if result["activated"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
