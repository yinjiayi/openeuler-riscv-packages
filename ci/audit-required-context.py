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
      nodes { number headRefOid }
    }
  }
  rateLimit { cost remaining resetAt }
}
"""


REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


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
    context_name: str,
    expected_workflow: str,
    expected_app: str,
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
            if not isinstance(exact_head, str) or not exact_head or exact_head != commit_oid:
                violations.append("exact-head-mismatch")
            if overflow:
                violations.append("context-pagination-overflow")
            if not matching:
                violations.append("missing-context")
            for item in matching:
                if item.get("type") != "check-run":
                    violations.append("status-context-not-allowed")
                elif item.get("workflow") != expected_workflow or item.get("app") != expected_app:
                    violations.append("unexpected-provenance")
            records.append({
                "number": pr.get("number"),
                "url": pr.get("url"),
                "head_sha": exact_head,
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


def collect_heads(owner: str, name: str) -> Tuple[Dict[int, Optional[str]], int, List[Dict[str, Any]], int]:
    cursor: Optional[str] = None
    heads: Dict[int, Optional[str]] = {}
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
            heads[number] = pr.get("headRefOid")
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
        owner, name, args.context, args.expected_workflow, args.expected_app
    )
    heads, second_total, second_rates, second_pages = collect_heads(owner, name)
    first_heads: Dict[int, Optional[str]] = {}
    for record in records:
        number = record.get("number")
        if not isinstance(number, int):
            raise AuditError("context scan PR number is invalid")
        if number in first_heads:
            raise AuditError("duplicate pull request in context scan")
        first_heads[number] = record.get("head_sha")
    changed_heads = sorted(
        number for number in set(first_heads) | set(heads)
        if first_heads.get(number) != heads.get(number)
    )
    stable = (
        first_total == second_total == len(records) == len(heads)
        and not changed_heads
    )
    if not stable:
        result["errors"].append("open-pr-exact-head-snapshot-changed")
    for record in records:
        if record["violations"]:
            result["errors"].append("pr-%s:%s" % (record["number"], ",".join(record["violations"])))
    missing = [record for record in records if "missing-context" in record["violations"]]
    status_contexts = [record for record in records if "status-context-not-allowed" in record["violations"]]
    bad_provenance = [record for record in records if "unexpected-provenance" in record["violations"]]
    overflow = [record for record in records if "context-pagination-overflow" in record["violations"]]
    head_mismatch = [record for record in records if "exact-head-mismatch" in record["violations"]]
    duplicates = [record for record in records if record["matching_context_count"] > 1]
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
            "duplicate_context_pr_count": len(duplicates),
            "changed_head_pr_count": len(changed_heads),
            "context_scan_page_count": first_pages,
            "head_verification_page_count": second_pages,
        },
        "changed_heads": changed_heads,
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
