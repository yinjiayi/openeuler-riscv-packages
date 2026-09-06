#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Fail closed unless every open PR exact head has one trusted check context."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


CONTEXT_QUERY = r"""
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(first: 100, after: $cursor, states: OPEN,
                 orderBy: {field: CREATED_AT, direction: ASC}) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        number
        url
        headRefOid
        baseRefOid
        commits(last: 1) {
          nodes {
            commit {
              oid
              statusCheckRollup {
                contexts(first: 100) {
                  totalCount
                  pageInfo { hasNextPage endCursor }
                  nodes {
                    __typename
                    ... on CheckRun {
                      databaseId
                      name
                      externalId
                      status
                      conclusion
                      detailsUrl
                      checkSuite {
                        app { slug }
                        workflowRun {
                          databaseId
                          workflow { name }
                        }
                      }
                    }
                    ... on StatusContext {
                      context
                      state
                      targetUrl
                      creator { login }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  rateLimit { cost remaining resetAt }
}
"""


HEAD_QUERY = r"""
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(first: 100, after: $cursor, states: OPEN,
                 orderBy: {field: CREATED_AT, direction: ASC}) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes { number headRefOid baseRefOid }
    }
  }
  rateLimit { cost remaining resetAt }
}
"""


REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA = re.compile(r"^[0-9a-f]{40}$")
BRIDGE_EXTERNAL_ID = re.compile(
    r"^configure-bridge-v1:([^:]+/[^:]+):([1-9][0-9]*):"
    r"([0-9a-f]{40}):([0-9a-f]{40}):([1-9][0-9]*):([1-9][0-9]*)$"
)
IMAGE_BRANCH = re.compile(r"^infra/ci-image-[0-9a-f]{12}$")
BRIDGE_POLICY = "bot-image-lock-v1"
CHECKS_APP_ID = 15368


class AuditError(RuntimeError):
    """A safe, user-facing audit failure."""


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, value: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def graphql(query: str, owner: str, name: str, cursor: Optional[str]) -> Dict[str, Any]:
    command = [
        "gh", "api", "graphql", "-f", "query=" + query,
        "-F", "owner=" + owner, "-F", "name=" + name,
    ]
    if cursor is not None:
        command.extend(["-F", "cursor=" + cursor])
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AuditError("gh api graphql failed with exit status %d" % completed.returncode)
    try:
        document = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise AuditError("gh api graphql returned invalid JSON") from error
    if not isinstance(document, dict):
        raise AuditError("gh api graphql returned a non-object response")
    if document.get("errors"):
        raise AuditError("GitHub GraphQL returned one or more errors")
    return document


def rest_json(arguments: List[str]) -> Any:
    completed = subprocess.run(
        ["gh", "api", *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AuditError("gh api REST failed with exit status %d" % completed.returncode)
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise AuditError("gh api REST returned invalid JSON") from error


def require_dict(value: Any, description: str) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise AuditError(description + " is not an object")
    return value


def verify_bridge_context(
    repository: str,
    pr_number: int,
    graph_head: str,
    graph_base: str,
    item: Dict[str, Any],
) -> Dict[str, Any]:
    check_id = item.get("check_run_id")
    if type(check_id) is not int or check_id <= 0:
        raise AuditError("bridge CheckRun id is invalid")
    check = require_dict(
        rest_json([f"repos/{repository}/check-runs/{check_id}"]),
        "bridge CheckRun readback",
    )
    app = require_dict(check.get("app"), "bridge CheckRun app")
    external = check.get("external_id")
    match = BRIDGE_EXTERNAL_ID.fullmatch(external) if isinstance(external, str) else None
    if match is None:
        raise AuditError("bridge CheckRun external_id is invalid")
    bound_repo, bound_pr, bound_head, bound_base, source_id, bridge_id = match.groups()
    if (
        bound_repo != repository
        or int(bound_pr) != pr_number
        or bound_head != graph_head
        or bound_base != graph_base
    ):
        raise AuditError("bridge CheckRun external_id does not bind the exact PR snapshot")
    details_url = f"https://github.com/{repository}/runs/{check_id}"
    if (
        check.get("id") != check_id
        or check.get("name") != "configure"
        or check.get("head_sha") != graph_head
        or check.get("status") != "completed"
        or check.get("conclusion") != "success"
        or check.get("details_url") != details_url
        or app.get("id") != CHECKS_APP_ID
        or app.get("slug") != "github-actions"
    ):
        raise AuditError("bridge CheckRun identity, conclusion, or app provenance is invalid")

    source = require_dict(
        rest_json([f"repos/{repository}/actions/runs/{source_id}"]),
        "bridge source workflow run",
    )
    source_pulls = source.get("pull_requests")
    source_pull = (
        require_dict(source_pulls[0], "bridge source pull request")
        if isinstance(source_pulls, list) and len(source_pulls) == 1
        else None
    )
    if source_pull is None:
        raise AuditError("bridge source workflow does not bind exactly one PR")
    source_head = require_dict(source_pull.get("head"), "bridge source pull head")
    source_base = require_dict(source_pull.get("base"), "bridge source pull base")
    if (
        source.get("id") != int(source_id)
        or source.get("name") != "Auto Merge Policy"
        or source.get("path") != ".github/workflows/auto-merge.yml"
        or source.get("event") != "pull_request"
        or source.get("status") != "completed"
        or source.get("conclusion") != "action_required"
        or require_dict(source.get("repository"), "source repository").get("full_name") != repository
        or require_dict(source.get("head_repository"), "source head repository").get("full_name") != repository
        or require_dict(source.get("actor"), "source actor").get("login") != "github-actions[bot]"
        or require_dict(source.get("triggering_actor"), "source triggering actor").get("login") != "github-actions[bot]"
        or source.get("head_sha") != graph_head
        or source_pull.get("number") != pr_number
        or source_head.get("sha") != graph_head
        or source_base.get("sha") != graph_base
    ):
        raise AuditError("bridge source workflow provenance or exact lease is invalid")

    bridge = require_dict(
        rest_json([f"repos/{repository}/actions/runs/{bridge_id}"]),
        "bridge workflow run",
    )
    if (
        bridge.get("id") != int(bridge_id)
        or bridge.get("name") != "Configure Context Bridge"
        or bridge.get("path") != ".github/workflows/configure-context-bridge.yml"
        or bridge.get("event") not in ("workflow_run", "workflow_dispatch")
        or bridge.get("status") != "completed"
        or bridge.get("conclusion") != "success"
        or bridge.get("head_sha") != graph_base
        or bridge.get("head_branch") != "main"
        or require_dict(bridge.get("repository"), "bridge repository").get("full_name") != repository
    ):
        raise AuditError("bridge workflow protected-main provenance is invalid")

    pull = require_dict(rest_json([f"repos/{repository}/pulls/{pr_number}"]), "bridge pull request")
    pull_head = require_dict(pull.get("head"), "bridge pull-request head")
    pull_base = require_dict(pull.get("base"), "bridge pull-request base")
    if (
        pull.get("number") != pr_number
        or pull.get("state") != "open"
        or pull.get("merged") is not False
        or pull.get("merged_at") is not None
        or pull.get("auto_merge") is not None
        or pull.get("draft") is not False
        or require_dict(pull.get("user"), "bridge pull-request author").get("login") != "github-actions[bot]"
        or pull_head.get("sha") != graph_head
        or pull_base.get("sha") != graph_base
        or pull_base.get("ref") != "main"
        or not isinstance(pull_head.get("ref"), str)
        or IMAGE_BRANCH.fullmatch(pull_head["ref"]) is None
        or require_dict(pull_head.get("repo"), "bridge head repository").get("full_name") != repository
        or require_dict(pull_base.get("repo"), "bridge base repository").get("full_name") != repository
        or pull.get("changed_files") != 1
    ):
        raise AuditError("bridge pull-request identity, state, or exact lease is invalid")
    pages = rest_json([
        "--paginate", "--slurp", f"repos/{repository}/pulls/{pr_number}/files?per_page=100"
    ])
    if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
        raise AuditError("bridge pull-request files are not fully paginated arrays")
    files = [entry for page in pages for entry in page]
    if (
        len(files) != 1
        or not isinstance(files[0], dict)
        or files[0].get("filename") != "ci/image.lock"
        or files[0].get("status") != "modified"
        or files[0].get("previous_filename") is not None
    ):
        raise AuditError("bridge pull request is not one modified ci/image.lock")
    repo = require_dict(rest_json([f"repos/{repository}"]), "bridge repository readback")
    ref = require_dict(rest_json([f"repos/{repository}/git/ref/heads/main"]), "bridge main ref")
    ref_object = require_dict(ref.get("object"), "bridge main ref object")
    if (
        repo.get("full_name") != repository
        or repo.get("default_branch") != "main"
        or ref.get("ref") != "refs/heads/main"
        or ref_object.get("type") != "commit"
        or ref_object.get("sha") != graph_base
    ):
        raise AuditError("bridge base is not the current repository main head")
    return {
        "policy": BRIDGE_POLICY,
        "check_run_id": check_id,
        "source_run_id": int(source_id),
        "bridge_run_id": int(bridge_id),
        "head_sha": graph_head,
        "base_sha": graph_base,
    }


def connection_from(document: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    try:
        connection = document["data"]["repository"]["pullRequests"]
        rate = document["data"]["rateLimit"]
    except (KeyError, TypeError) as error:
        raise AuditError("GitHub GraphQL response is missing required fields") from error
    if not isinstance(connection, dict) or not isinstance(rate, dict):
        raise AuditError("GitHub GraphQL response has invalid connection fields")
    return connection, rate


def normalized_context(node: Dict[str, Any]) -> Dict[str, Any]:
    if node.get("__typename") == "CheckRun":
        suite = node.get("checkSuite") or {}
        workflow_run = suite.get("workflowRun") or {}
        workflow = workflow_run.get("workflow") or {}
        app = suite.get("app") or {}
        return {
            "type": "check-run",
            "name": node.get("name"),
            "check_run_id": node.get("databaseId"),
            "external_id": node.get("externalId"),
            "workflow_run_id": workflow_run.get("databaseId"),
            "workflow": workflow.get("name"),
            "app": app.get("slug"),
            "status": node.get("status"),
            "conclusion": node.get("conclusion"),
            "details_url": node.get("detailsUrl"),
        }
    if node.get("__typename") == "StatusContext":
        return {
            "type": "status-context",
            "name": node.get("context"),
            "creator": (node.get("creator") or {}).get("login"),
            "state": node.get("state"),
            "target_url": node.get("targetUrl"),
        }
    return {"type": str(node.get("__typename") or "unknown"), "name": None}


def collect_contexts(
    owner: str,
    name: str,
    repository: str,
    context_name: str,
    expected_workflow: str,
    expected_app: str,
    bridge_policy: Optional[str],
) -> Tuple[List[Dict[str, Any]], int, List[Dict[str, Any]], int]:
    cursor: Optional[str] = None
    records: List[Dict[str, Any]] = []
    total: Optional[int] = None
    rates: List[Dict[str, Any]] = []
    pages = 0
    seen_cursors = set()
    while True:
        pages += 1
        connection, rate = connection_from(graphql(CONTEXT_QUERY, owner, name, cursor))
        rates.append(rate)
        page_total = connection.get("totalCount")
        if not isinstance(page_total, int):
            raise AuditError("pull request totalCount is not an integer")
        if total is None:
            total = page_total
        elif page_total != total:
            raise AuditError("open pull request total changed during context pagination")
        nodes = connection.get("nodes")
        if not isinstance(nodes, list):
            raise AuditError("pull request page nodes is not a list")
        for pr in nodes:
            try:
                commit_nodes = pr["commits"]["nodes"]
            except (KeyError, TypeError) as error:
                raise AuditError("pull request commit connection is missing") from error
            commit = commit_nodes[0].get("commit") if isinstance(commit_nodes, list) and commit_nodes else None
            commit_oid = commit.get("oid") if isinstance(commit, dict) else None
            rollup = commit.get("statusCheckRollup") if isinstance(commit, dict) else None
            contexts_connection = rollup.get("contexts") if isinstance(rollup, dict) else None
            raw_contexts = contexts_connection.get("nodes", []) if isinstance(contexts_connection, dict) else []
            if not isinstance(raw_contexts, list):
                raise AuditError("status context nodes is not a list")
            contexts = [normalized_context(item) for item in raw_contexts if isinstance(item, dict)]
            matching = [item for item in contexts if item.get("name") == context_name]
            context_total = contexts_connection.get("totalCount", 0) if isinstance(contexts_connection, dict) else 0
            page_info = contexts_connection.get("pageInfo", {}) if isinstance(contexts_connection, dict) else {}
            overflow = (
                bool(page_info.get("hasNextPage"))
                or not isinstance(context_total, int)
                or context_total > 100
                or context_total != len(raw_contexts)
            )
            violations: List[str] = []
            exact_head = pr.get("headRefOid")
            exact_base = pr.get("baseRefOid")
            if not isinstance(exact_head, str) or SHA.fullmatch(exact_head) is None or exact_head != commit_oid:
                violations.append("exact-head-mismatch")
            if not isinstance(exact_base, str) or SHA.fullmatch(exact_base) is None:
                violations.append("exact-base-invalid")
            if overflow:
                violations.append("context-pagination-overflow")
            if not matching:
                violations.append("missing-context")
            for item in matching:
                if item.get("type") != "check-run":
                    violations.append("status-context-not-allowed")
                elif (
                    item.get("workflow") == expected_workflow
                    and item.get("app") == expected_app
                    and not str(item.get("external_id") or "").startswith("configure-bridge-v1:")
                ):
                    continue
                elif (
                    bridge_policy == BRIDGE_POLICY
                    and isinstance(pr.get("number"), int)
                    and isinstance(exact_head, str)
                    and isinstance(exact_base, str)
                ):
                    try:
                        item["bridge_attestation"] = verify_bridge_context(
                            repository, pr["number"], exact_head, exact_base, item
                        )
                    except AuditError as error:
                        item["bridge_error"] = str(error)
                        violations.append("unexpected-provenance")
                else:
                    violations.append("unexpected-provenance")
            records.append({
                "number": pr.get("number"),
                "url": pr.get("url"),
                "head_sha": exact_head,
                "base_sha": exact_base,
                "commit_oid": commit_oid,
                "context_total_count": context_total,
                "context_page_overflow": overflow,
                "matching_context_count": len(matching),
                "matching_contexts": matching,
                "violations": sorted(set(violations)),
            })
        page_info = connection.get("pageInfo")
        if not isinstance(page_info, dict):
            raise AuditError("pull request pageInfo is missing")
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")
        if not isinstance(cursor, str) or not cursor:
            raise AuditError("pull request pagination has no end cursor")
        if not nodes or cursor in seen_cursors:
            raise AuditError("pull request pagination made no forward progress")
        seen_cursors.add(cursor)
    if total is None:
        raise AuditError("pull request pagination produced no total")
    return records, total, rates, pages


def collect_heads(owner: str, name: str) -> Tuple[Dict[int, Tuple[Optional[str], Optional[str]]], int, List[Dict[str, Any]], int]:
    cursor: Optional[str] = None
    heads: Dict[int, Tuple[Optional[str], Optional[str]]] = {}
    total: Optional[int] = None
    rates: List[Dict[str, Any]] = []
    pages = 0
    seen_cursors = set()
    while True:
        pages += 1
        connection, rate = connection_from(graphql(HEAD_QUERY, owner, name, cursor))
        rates.append(rate)
        page_total = connection.get("totalCount")
        if not isinstance(page_total, int):
            raise AuditError("pull request totalCount is not an integer")
        if total is None:
            total = page_total
        elif page_total != total:
            raise AuditError("open pull request total changed during head verification pagination")
        nodes = connection.get("nodes")
        if not isinstance(nodes, list):
            raise AuditError("head verification page nodes is not a list")
        for pr in nodes:
            number = pr.get("number") if isinstance(pr, dict) else None
            if not isinstance(number, int):
                raise AuditError("head verification PR number is invalid")
            if number in heads:
                raise AuditError("duplicate pull request in head verification")
            heads[number] = (pr.get("headRefOid"), pr.get("baseRefOid"))
        page_info = connection.get("pageInfo")
        if not isinstance(page_info, dict):
            raise AuditError("head verification pageInfo is missing")
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")
        if not isinstance(cursor, str) or not cursor:
            raise AuditError("head verification pagination has no end cursor")
        if not nodes or cursor in seen_cursors:
            raise AuditError("head verification pagination made no forward progress")
        seen_cursors.add(cursor)
    if total is None:
        raise AuditError("head verification pagination produced no total")
    return heads, total, rates, pages


def initial_result(args: argparse.Namespace) -> Dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": "required-context-audit",
        "repository": args.repository,
        "context": args.context,
        "expected_workflow": args.expected_workflow,
        "expected_app": args.expected_app,
        "bridge_policy": args.bridge_policy,
        "started_at": utc_now(),
        "completed_at": None,
        "passed": False,
        "snapshot_stable": False,
        "errors": [],
        "summary": {},
        "records": [],
    }


def audit(args: argparse.Namespace, result: Dict[str, Any]) -> None:
    owner, name = args.repository.split("/", 1)
    records, first_total, first_rates, first_pages = collect_contexts(
        owner,
        name,
        args.repository,
        args.context,
        args.expected_workflow,
        args.expected_app,
        args.bridge_policy,
    )
    heads, second_total, second_rates, second_pages = collect_heads(owner, name)
    first_heads: Dict[int, Tuple[Optional[str], Optional[str]]] = {}
    for record in records:
        number = record.get("number")
        if not isinstance(number, int):
            raise AuditError("context scan PR number is invalid")
        if number in first_heads:
            raise AuditError("duplicate pull request in context scan")
        first_heads[number] = (record.get("head_sha"), record.get("base_sha"))
    changed_heads = sorted(
        number for number in set(first_heads) | set(heads)
        if (first_heads.get(number) or (None, None))[0] != (heads.get(number) or (None, None))[0]
    )
    changed_bases = sorted(
        number for number in set(first_heads) | set(heads)
        if (first_heads.get(number) or (None, None))[1] != (heads.get(number) or (None, None))[1]
    )
    stable = (
        first_total == second_total == len(records) == len(heads)
        and not changed_heads
        and not changed_bases
    )
    if not stable:
        result["errors"].append("open-pr-exact-head-snapshot-changed")
    # Revalidate every exceptional bridge after the second GraphQL snapshot.
    # This closes the REST/main-ref race window; ordinary workflow CheckRuns do
    # not use this exception and therefore incur no additional REST traffic.
    for record in records:
        for item in record["matching_contexts"]:
            first_proof = item.get("bridge_attestation")
            if not isinstance(first_proof, dict):
                continue
            try:
                final_proof = verify_bridge_context(
                    args.repository,
                    record["number"],
                    record["head_sha"],
                    record["base_sha"],
                    item,
                )
                if final_proof != first_proof:
                    raise AuditError("bridge attestation changed between REST snapshots")
                item["bridge_attestation_stable"] = True
            except AuditError as error:
                item["bridge_error"] = str(error)
                record["violations"] = sorted(set(record["violations"] + ["unexpected-provenance"]))
    for record in records:
        if record["violations"]:
            result["errors"].append("pr-%s:%s" % (record["number"], ",".join(record["violations"])))
    missing = [record for record in records if "missing-context" in record["violations"]]
    status_contexts = [record for record in records if "status-context-not-allowed" in record["violations"]]
    bad_provenance = [record for record in records if "unexpected-provenance" in record["violations"]]
    overflow = [record for record in records if "context-pagination-overflow" in record["violations"]]
    head_mismatch = [record for record in records if "exact-head-mismatch" in record["violations"]]
    base_invalid = [record for record in records if "exact-base-invalid" in record["violations"]]
    duplicates = [record for record in records if record["matching_context_count"] > 1]
    bridged = [
        record for record in records
        if any(
            isinstance(item.get("bridge_attestation"), dict)
            and item.get("bridge_attestation_stable") is True
            for item in record["matching_contexts"]
        )
    ]
    result.update({
        "completed_at": utc_now(),
        "passed": stable and not result["errors"],
        "snapshot_stable": stable,
        "summary": {
            "first_open_pr_total": first_total,
            "second_open_pr_total": second_total,
            "audited_pr_count": len(records),
            "verified_head_count": len(heads),
            "context_present_pr_count": len(records) - len(missing),
            "missing_pr_count": len(missing),
            "status_context_pr_count": len(status_contexts),
            "unexpected_provenance_pr_count": len(bad_provenance),
            "context_overflow_pr_count": len(overflow),
            "head_mismatch_pr_count": len(head_mismatch),
            "base_invalid_pr_count": len(base_invalid),
            "duplicate_context_pr_count": len(duplicates),
            "bridge_context_pr_count": len(bridged),
            "changed_head_pr_count": len(changed_heads),
            "changed_base_pr_count": len(changed_bases),
            "context_scan_page_count": first_pages,
            "head_verification_page_count": second_pages,
        },
        "changed_heads": changed_heads,
        "changed_bases": changed_bases,
        "missing": [{"number": item["number"], "head_sha": item["head_sha"], "url": item["url"]} for item in missing],
        "status_contexts": [{"number": item["number"], "head_sha": item["head_sha"]} for item in status_contexts],
        "unexpected_provenance": [{"number": item["number"], "head_sha": item["head_sha"]} for item in bad_provenance],
        "context_overflow": [
            {
                "number": item["number"],
                "head_sha": item["head_sha"],
                "context_total_count": item["context_total_count"],
            }
            for item in overflow
        ],
        "head_mismatches": [
            {"number": item["number"], "head_sha": item["head_sha"], "commit_oid": item["commit_oid"]}
            for item in head_mismatch
        ],
        "duplicates": [
            {"number": item["number"], "head_sha": item["head_sha"], "count": item["matching_context_count"]}
            for item in duplicates
        ],
        "graphql_rate_samples": first_rates + second_rates,
        "records": records,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--context", required=True)
    parser.add_argument("--expected-workflow", required=True)
    parser.add_argument("--expected-app", required=True)
    parser.add_argument("--bridge-policy", choices=[BRIDGE_POLICY])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not REPOSITORY.fullmatch(args.repository):
        parser.error("--repository must be OWNER/NAME")
    for option, value in (
        ("--context", args.context),
        ("--expected-workflow", args.expected_workflow),
        ("--expected-app", args.expected_app),
    ):
        if not value.strip():
            parser.error(option + " must not be empty")
    result = initial_result(args)
    try:
        audit(args, result)
    except AuditError as error:
        result["completed_at"] = utc_now()
        result["errors"].append(str(error))
    except Exception as error:  # pragma: no cover - last-resort fail-closed evidence
        result["completed_at"] = utc_now()
        result["errors"].append("unexpected audit failure: " + type(error).__name__)
    write_json(args.output.resolve(), result)
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
