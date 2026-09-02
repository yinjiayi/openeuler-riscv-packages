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
    for field in ("target", "enforcement"):
        if live.get(field) != expected.get(field):
            return {"activated": False, "reason": f"ruleset {field} differs from protected configuration", "ruleset_id": ruleset_id}
    if live.get("target") != "branch" or live.get("enforcement") != "active":
        return {"activated": False, "reason": "configured ruleset is not an active branch ruleset", "ruleset_id": ruleset_id}
    if "bypass_actors" not in live or "bypass_actors" not in expected:
        raise ActivationError("ruleset bypass actors field is missing")
    live_bypass = live["bypass_actors"]
    expected_bypass = expected["bypass_actors"]
    if not isinstance(live_bypass, list) or not isinstance(expected_bypass, list):
        raise ActivationError("ruleset bypass actors field is not a list")
    if live_bypass != expected_bypass or live_bypass != []:
        return {"activated": False, "reason": "ruleset bypass actors differ or are nonempty", "ruleset_id": ruleset_id}
    live_conditions = live.get("conditions")
    expected_conditions = expected.get("conditions")
    if live_conditions != expected_conditions:
        return {"activated": False, "reason": "ruleset branch conditions differ from protected configuration", "ruleset_id": ruleset_id}
    ref_name = live_conditions.get("ref_name") if isinstance(live_conditions, Mapping) else None
    includes = ref_name.get("include") if isinstance(ref_name, Mapping) else None
    excludes = ref_name.get("exclude") if isinstance(ref_name, Mapping) else None
    if includes != ["~DEFAULT_BRANCH"] or excludes != []:
        return {"activated": False, "reason": "ruleset does not exclusively include the default branch", "ruleset_id": ruleset_id}
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
        return {
            "activated": False,
            "reason": "required context is not present exactly once",
            "ruleset_id": ruleset_id,
            "occurrences": occurrences,
        }
    return {"activated": True, "reason": "live ruleset requires the context", "ruleset_id": ruleset_id}


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
