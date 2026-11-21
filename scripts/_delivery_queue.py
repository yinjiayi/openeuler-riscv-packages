# SPDX-License-Identifier: Apache-2.0
"""Shared-snapshot scheduling, not a package/merge/publication acceptance gate."""
from __future__ import annotations

import argparse
from concurrent.futures import Future, ThreadPoolExecutor
import contextlib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sqlite3
import subprocess
import sys
import threading
import uuid

from _lib import ToolError, emit_json, isoformat, load_json, parse_now, parse_time, stable_json

SHA = re.compile(r"^[0-9a-f]{40}$")
PACKAGE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
REQUIRED = ("metadata-validate", "source-verify", "rpmbuild-riscv64", "rpm-install-smoke", "patch-policy", "merge-policy")
HOLDS = {"needs-human", "needs-native-riscv", "qemu-limitation", "source-blocked", "license-blocked", "checksum-blocked", "security-blocked", "tests-disabled", "codex-repairing"}
QUEUES = ("repair", "intake", "merge-review")
POLICY_WORKFLOW = ".github/workflows/auto-merge.yml"
ACTIONS_APP = 15368


def require(condition, message):
    if not condition:
        raise ToolError(message, 1)


def reject_credential_response(value):
    for name in ("GH_TOKEN", "GITHUB_TOKEN"):
        token = os.environ.get(name)
        require(not token or token not in value, "credential appeared in API response; refused to retain it")


def api(path):
    """Only GET; suppress untrusted stderr so credentials never enter a receipt."""
    try:
        result = subprocess.run(["gh", "api", "--method", "GET", path], capture_output=True, text=True, timeout=90)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ToolError("GitHub read failed or timed out", 1) from exc
    require(result.returncode == 0, "GitHub GET failed; no complete snapshot was produced")
    reject_credential_response(result.stdout)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ToolError("GitHub returned invalid JSON", 1) from exc


def graphql_api(query, variables):
    try:
        result = subprocess.run(["gh", "api", "graphql", "--input", "-"],
                                input=json.dumps({"query": query, "variables": variables}),
                                capture_output=True, text=True, timeout=90)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ToolError("GitHub GraphQL read failed or timed out", 1) from exc
    require(result.returncode == 0 and len(result.stdout) <= 16 * 1024 * 1024, "GraphQL read failed or exceeded response bound")
    reject_credential_response(result.stdout)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ToolError("invalid GraphQL response", 1) from exc
    require(not data.get("errors") and isinstance(data.get("data"), dict), "incomplete GraphQL read")
    return data["data"]


def batch_details(repo, prs, read, workers):
    """Batch common heads; overflow alone falls back to full REST pagination.

    At ~2,000 PRs this avoids ~6,000 individual files/check/status REST calls. This
    remains a full census, not cached or incremental CI reuse.
    """
    batches = [prs[start:start + 25] for start in range(0, len(prs), 25)]
    fields = """number headRefOid changedFiles files(first:100){totalCount pageInfo{hasNextPage} nodes{path changeType}}
      commits(last:1){nodes{commit{oid statusCheckRollup{
      contexts(first:100){totalCount pageInfo{hasNextPage} nodes{
        ... on CheckRun{databaseId name status conclusion detailsUrl startedAt completedAt
          checkSuite{databaseId app{databaseId} commit{oid} workflowRun{databaseId runAttempt}}}
        ... on StatusContext{id context state targetUrl createdAt updatedAt commit{oid}}
      }}}}}}"""
    def collect(batch):
        query = 'query($owner:String!,$name:String!){repository(owner:$owner,name:$name){' + " ".join(
            f"p{i}:pullRequest(number:{pr['number']}){{{fields}}}" for i, pr in enumerate(batch)) + "}}"
        owner, name = repo.split("/")
        response = read(query, {"owner": owner, "name": name})["repository"]
        output = {}
        for i, pr in enumerate(batch):
            node = response.get(f"p{i}")
            require(node and node["number"] == pr["number"] and node["headRefOid"] == pr["head"]["sha"], "PR head changed during check batch")
            files = node["files"]
            require(files["totalCount"] == node["changedFiles"], "file count changed during batch")
            if files["pageInfo"]["hasNextPage"] or any(item["changeType"] == "RENAMED" for item in files["nodes"]):
                # GraphQL exposes no previousFilename (verified against the
                # live schema). Renames require REST for their original scope.
                changed = None
            else:
                require(len(files["nodes"]) == files["totalCount"], "incomplete files batch")
                changed = [{"filename": item["path"], "status": item["changeType"].lower()} for item in files["nodes"]]
            output[pr["number"]] = {"files": changed, "file_count": node["changedFiles"], "checks": None}
            commits = node["commits"]["nodes"]
            require(len(commits) == 1 and commits[0]["commit"]["oid"] == pr["head"]["sha"], "check batch commit identity mismatch")
            rollup = commits[0]["commit"].get("statusCheckRollup")
            contexts = rollup.get("contexts") if rollup else {"nodes": [], "totalCount": 0, "pageInfo": {"hasNextPage": False}}
            if contexts["pageInfo"]["hasNextPage"]:
                continue
            require(len(contexts["nodes"]) == contexts["totalCount"], "incomplete check batch")
            observed_checks = []
            latest_statuses = {}
            check_ids = set()
            for context in contexts["nodes"]:
                if "name" in context:
                    suite = context["checkSuite"]
                    require(suite["commit"]["oid"] == pr["head"]["sha"], "check batch contains another SHA")
                    item = {"name": context["name"], "kind": "check", "id": context["databaseId"],
                            "app_id": (suite.get("app") or {}).get("databaseId"), "url": context.get("detailsUrl"),
                            "suite_id": suite.get("databaseId"), "workflow_run_id": (suite.get("workflowRun") or {}).get("databaseId"),
                            "run_attempt": (suite.get("workflowRun") or {}).get("runAttempt"), "started_at": context.get("startedAt"),
                            "state": (context.get("conclusion") or "").lower() if context["status"] == "COMPLETED" else "pending"}
                    require(isinstance(item["id"], int) and item["id"] > 0 and item["id"] not in check_ids, "check batch lacks unique check identity")
                    check_ids.add(item["id"])
                    observed_checks.append(item)
                else:
                    require(context["commit"]["oid"] == pr["head"]["sha"], "status batch contains another SHA")
                    item = {"name": context["context"], "kind": "status", "id": context["id"], "url": context.get("targetUrl"), "state": context["state"].lower()}
                    key, order = item["name"], (context.get("updatedAt") or context["createdAt"], context["id"])
                    if key not in latest_statuses or order > latest_statuses[key][0]:
                        latest_statuses[key] = (order, item)
            output[pr["number"]]["checks"] = observed_checks + [value[1] for value in latest_statuses.values()]
        return output
    output = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for result in executor.map(collect, batches):
            output.update(result)
    require(len(output) == len(prs), "check batch coverage incomplete")
    return output


def pages(get, path, field=None):
    collected = []
    expected = None
    for page in range(1, 10001):
        data = get(path + ("&" if "?" in path else "?") + f"per_page=100&page={page}")
        values = data.get(field) if field and isinstance(data, dict) else data
        require(isinstance(values, list), "invalid paginated API response")
        if field:
            total = data.get("total_count")
            require(isinstance(total, int) and total >= 0, "missing pagination total_count")
            require(expected is None or expected == total, "pagination changed during collection")
            expected = total
        collected.extend(values)
        if len(values) < 100:
            require(expected is None or len(collected) == expected, "incomplete paginated response")
            return collected
    raise ToolError("pagination safety bound exceeded", 1)


def package_paths(files):
    packages = set()
    scoped = bool(files)
    seen = set()
    for entry in files:
        name = entry.get("filename")
        require(isinstance(name, str) and name not in seen, "invalid or duplicate PR filename")
        seen.add(name)
        paths = [name]
        if entry.get("status") == "renamed":
            require(isinstance(entry.get("previous_filename"), str), "rename lacks original filename")
            paths.append(entry["previous_filename"])
        for raw in paths:
            path = PurePosixPath(raw)
            require(not path.is_absolute() and ".." not in path.parts and path.as_posix() == raw and "\\" not in raw, "unsafe PR path")
            if len(path.parts) >= 3 and path.parts[0] == "packages" and PACKAGE.fullmatch(path.parts[1]):
                packages.add(path.parts[1])
            else:
                scoped = False
    return sorted(packages), scoped and len(packages) == 1


def membership(prs):
    result = {}
    for pr in prs:
        number = pr.get("number")
        require(isinstance(number, int) and number > 0 and number not in result, "duplicate or invalid PR membership")
        metadata = {"updated_at": pr.get("updated_at"), "labels": sorted(label["name"] for label in pr.get("labels", [])),
                    "draft": pr.get("draft"), "author": (pr.get("user") or {}).get("login"),
                    "association": pr.get("author_association"), "head_ref": pr["head"].get("ref"),
                    "base_ref": pr["base"].get("ref"), "head_repo": (pr["head"].get("repo") or {}).get("full_name"),
                    "base_repo": (pr["base"].get("repo") or {}).get("full_name")}
        result[number] = (pr["head"]["sha"], pr["base"]["sha"], stable_json(metadata))
    return result


def duplicate_checks(checks):
    groups = {}
    for check in checks:
        if check.get("kind") == "check":
            groups.setdefault(check["name"], []).append(check)
    return [group for group in groups.values() if len(group) > 1]


def policy_provenance_reader(repo, get):
    """Snapshot-local, GET-only corroboration for the one allowlisted context.

    A details URL is only a locator. Authenticated workflow/run/suite and
    attempt-jobs responses must join back to every observed check. Neither
    increasing IDs nor a later successful event supersedes another result.
    """
    cache, lock = {}, threading.Lock()

    def cached(path, paginated=False):
        with lock:
            owner = path not in cache
            if owner:
                cache[path] = Future()
            future = cache[path]
        if owner:
            try:
                value = pages(get, path, "jobs") if paginated else get(path)
            except ToolError:
                # A failed corroborating read holds only this ambiguity;
                # never invent provenance or fail unrelated package work.
                value = None
            except BaseException as exc:
                future.set_exception(exc)
                raise
            future.set_result(value)
        # Different endpoints proceed in the existing collector worker pool;
        # only readers of this same endpoint share/wait for one GET result.
        return future.result()

    def state(value):
        return value.get("conclusion") if value.get("status") == "completed" else "pending"

    def positive(value):
        return type(value) is int and value > 0

    def augment(pr):
        # codex-repairing is an ownership routing label, not a semantic hold:
        # retain the same inputs for owned_repair_routing's exact comparison.
        # classify still holds it, so this never admits another worker.
        if not pr["trusted"] or pr["draft"] or not pr["package_only"] or set(pr["labels"]) & (HOLDS - {"codex-repairing"}):
            return
        groups = duplicate_checks(pr["checks"])
        if any(c["name"] != "configure" or c.get("app_id") != ACTIONS_APP or
               not positive(c.get("suite_id")) or not positive(c.get("id")) for group in groups for c in group):
            return  # Another ambiguity already holds this PR; do not fetch.
        for group in groups:
            workflow = cached(f"repos/{repo}/actions/workflows/auto-merge.yml")
            if not isinstance(workflow, dict) or workflow.get("path") != POLICY_WORKFLOW or workflow.get("state") != "active" or not positive(workflow.get("id")):
                continue
            for check in group:
                check.pop("workflow_provenance", None)
                # REST fallback has no workflowRun/runAttempt fields. Resolve
                # its URL, then bind the actual attempt through the jobs API.
                locator = re.fullmatch(r"https://github\.com/" + re.escape(repo) + r"/actions/runs/([1-9][0-9]*)/job/([1-9][0-9]*)", check.get("url") or "")
                run_id = check.get("workflow_run_id")
                if run_id is None and locator:
                    run_id = int(locator[1])
                if not positive(run_id) or (locator and int(locator[1]) != run_id):
                    continue
                run = cached(f"repos/{repo}/actions/runs/{run_id}")
                suite = cached(f"repos/{repo}/check-suites/{check['suite_id']}")
                if not isinstance(run, dict) or not isinstance(suite, dict):
                    continue
                attempt, repository = run.get("run_attempt"), run.get("repository") or {}
                repo_id = repository.get("id")
                associated = [p for p in run.get("pull_requests", []) if p.get("number") == pr["number"]]
                if (run.get("id") != run_id or run.get("workflow_id") != workflow["id"] or
                    run.get("path") != POLICY_WORKFLOW or run.get("event") != "pull_request" or
                    run.get("head_sha") != pr["head_sha"] or run.get("head_branch") != pr["head_ref"] or
                    run.get("check_suite_id") != check["suite_id"] or not positive(attempt) or
                    (check.get("run_attempt") is not None and check["run_attempt"] != attempt) or
                    repository.get("full_name", "").lower() != repo or not positive(repo_id) or
                    (run.get("head_repository") or {}).get("id") != repo_id or
                    (run.get("head_repository") or {}).get("full_name", "").lower() != repo or
                    suite.get("id") != check["suite_id"] or suite.get("head_sha") != pr["head_sha"] or
                    (suite.get("app") or {}).get("id") != ACTIONS_APP or
                    (suite.get("repository") or {}).get("id") != repo_id or
                    (suite.get("repository") or {}).get("full_name", "").lower() != repo or len(associated) != 1):
                    continue
                association = associated[0]
                if (association.get("url") != f"https://api.github.com/repos/{repo}/pulls/{pr['number']}" or
                    any((association.get(side) or {}).get("sha") != sha or
                        ((association.get(side) or {}).get("repo") or {}).get("id") != repo_id
                        for side, sha in (("head", pr["head_sha"]), ("base", pr["base_sha"])))):
                    continue
                jobs = cached(f"repos/{repo}/actions/runs/{run_id}/attempts/{attempt}/jobs", True)
                if not isinstance(jobs, list):
                    continue
                matching = [j for j in jobs if j.get("check_run_url") == f"https://api.github.com/repos/{repo}/check-runs/{check['id']}"]
                if len(matching) != 1:
                    continue
                job = matching[0]
                if (job.get("name") != "configure" or job.get("run_id") != run_id or job.get("run_attempt") != attempt or
                    job.get("head_sha") != pr["head_sha"] or state(job) != check["state"] or
                    (locator and job.get("id") != int(locator[2]))):
                    continue
                check["workflow_provenance"] = {
                    "repo": repo, "repository_id": repo_id, "pr_number": pr["number"],
                    "head_sha": pr["head_sha"], "base_sha": pr["base_sha"], "head_ref": pr["head_ref"],
                    "check_id": check["id"], "suite_id": check["suite_id"], "app_id": ACTIONS_APP,
                    "workflow_id": workflow["id"], "workflow_path": POLICY_WORKFLOW, "workflow_state": "active",
                    "run_id": run_id, "run_attempt": attempt, "event": "pull_request",
                    "check_state": check["state"], "run_state": state(run), "suite_state": state(suite)}
    return augment


def proven_policy_duplicates(pr, group):
    """Validate retained cross-links again; old/missing evidence stays held."""
    workflow_ids, check_ids = set(), set()
    for check in group:
        proof = check.get("workflow_provenance")
        if not isinstance(proof, dict):
            return False
        repo = proof.get("repo")
        if (check["name"] != "configure" or check.get("app_id") != ACTIONS_APP or
            not isinstance(repo, str) or not REPO.fullmatch(repo) or
            pr["url"] != f"https://github.com/{repo}/pull/{pr['number']}" or
            any(proof.get(key) != value for key, value in {
                "pr_number": pr["number"], "head_sha": pr["head_sha"], "base_sha": pr["base_sha"],
                "head_ref": pr["head_ref"], "check_id": check.get("id"), "suite_id": check.get("suite_id"),
                "app_id": ACTIONS_APP, "workflow_path": POLICY_WORKFLOW, "workflow_state": "active",
                "event": "pull_request", "check_state": check["state"]}.items()) or
            any(type(proof.get(key)) is not int or proof[key] <= 0 for key in
                ("repository_id", "check_id", "suite_id", "workflow_id", "run_id", "run_attempt")) or
            any(check.get(key) is not None and check[key] != proof[target]
                for key, target in (("workflow_run_id", "run_id"), ("run_attempt", "run_attempt"))) or
            any(proof.get(key) not in {"success", "pending", "failure", "error", "cancelled", "timed_out", "action_required", "startup_failure"}
                for key in ("check_state", "run_state", "suite_state"))):
            return False
        workflow_ids.add(proof["workflow_id"])
        check_ids.add(check["id"])
    return len(workflow_ids) == 1 and len(check_ids) == len(group)


def collect_snapshot(repo, workers=4, get=api, now=None, read_graphql=None):
    require(bool(REPO.fullmatch(repo)), "repo must be OWNER/REPO")
    require(1 <= workers <= 16, "workers must be between 1 and 16")
    repo = repo.lower()
    prefix = f"repos/{repo}"
    started = isoformat(parse_now(now))
    main = get(prefix + "/branches/main")["commit"]["sha"]
    require(bool(SHA.fullmatch(main)), "main is not an exact SHA")
    prs = pages(get, prefix + "/pulls?state=open&sort=created&direction=asc")
    before = membership(prs)
    tree = get(prefix + f"/git/trees/{main}?recursive=1")
    require(tree.get("truncated") is False, "main tree is incomplete")
    managed = sorted({entry["path"].split("/")[1] for entry in tree["tree"]
                      if re.fullmatch(r"packages/([a-z0-9]+(?:-[a-z0-9]+)*)/package.yaml", entry["path"])})
    batched = batch_details(repo, prs, read_graphql, workers) if read_graphql else {}
    augment_policy = policy_provenance_reader(repo, get)

    def collect(pr):
        number, head = pr["number"], pr["head"]["sha"]
        require(bool(SHA.fullmatch(head)), "invalid PR head")
        detail = batched.get(number, {})
        files = detail.get("files")
        if files is None:
            files = pages(get, prefix + f"/pulls/{number}/files")
        # GitHub caps PR files at 3,000. Never silently accept a capped response.
        require(len(files) < 3000, "PR file API cap reached; scope cannot be certified")
        if "file_count" in detail:
            require(detail["file_count"] == len(files), "incomplete fallback PR files")
        if "changed_files" in pr:
            require(pr["changed_files"] == len(files), "incomplete PR files")
        package_ids, scoped = package_paths(files)
        # Retain scope evidence, not untrusted patches, blob bodies or API URLs
        # that no scheduler needs. Mutation admission must read its own diff.
        files = [{key: entry[key] for key in ("filename", "status", "previous_filename") if key in entry} for entry in files]
        runs = pages(get, prefix + f"/commits/{head}/check-runs?filter=latest", "check_runs") if detail.get("checks") is None else []
        statuses = pages(get, prefix + f"/commits/{head}/statuses") if detail.get("checks") is None else []
        checks = list(detail.get("checks") or [])
        check_ids = set()
        for run in runs:
            require(run.get("head_sha") == head, "check-run belongs to another SHA")
            require(run["id"] not in check_ids, "duplicate check-run page entry")
            check_ids.add(run["id"])
            checks.append({"name": run["name"], "state": run.get("conclusion") if run.get("status") == "completed" else "pending",
                           "kind": "check", "id": run["id"], "app_id": (run.get("app") or {}).get("id"),
                           "suite_id": (run.get("check_suite") or {}).get("id"), "started_at": run.get("started_at"),
                           "url": run.get("details_url")})
        # Commit statuses contain history; only newest ID per context is current.
        latest = {}
        for status in statuses:
            name = status["context"]
            if name not in latest or status["id"] > latest[name]["id"]:
                latest[name] = status
        checks.extend({"name": value["context"], "state": value["state"], "kind": "status", "id": value["id"], "url": value.get("target_url")}
                      for value in latest.values())
        author = (pr.get("user") or {}).get("login")
        trusted = pr.get("author_association") in {"OWNER", "MEMBER", "COLLABORATOR"} or author in {repo.split("/")[0], "github-actions[bot]"}
        same_repo = ((pr["head"].get("repo") or {}).get("full_name", "").lower() == repo
                     and ((pr["base"].get("repo") or {}).get("full_name", "").lower() == repo))
        record = {"number": number, "head_sha": head, "base_sha": pr["base"]["sha"], "head_ref": pr["head"]["ref"],
                "url": pr["html_url"], "created_at": pr["created_at"], "updated_at": pr["updated_at"],
                "draft": pr.get("draft", True), "trusted": bool(trusted and same_repo), "package_ids": package_ids,
                "package_only": scoped, "labels": sorted(label["name"] for label in pr.get("labels", [])),
                "checks": checks, "files": files, "checks_collected_at": isoformat(parse_now(now))}
        augment_policy(record)
        return record

    with ThreadPoolExecutor(max_workers=workers) as executor:
        records = list(executor.map(collect, prs))
    by_number = {record["number"]: record for record in records}
    refreshes = []
    refreshed_ids = set()
    for attempt in range(3):
        current_prs = pages(get, prefix + "/pulls?state=open&sort=created&direction=asc")
        after = membership(current_prs)
        final_main = get(prefix + "/branches/main")["commit"]["sha"]
        require(main == final_main, "main changed; discard and recollect snapshot")
        require(set(before) == set(after), "PR membership changed; discard and recollect snapshot")
        require(all(before[number][:2] == after[number][:2] for number in before), "PR head/base changed; discard and recollect snapshot")
        changed = sorted(number for number in before if before[number] != after[number])
        if not changed:
            break
        require(attempt < 2, "same-head metadata still changing after two refresh rounds; snapshot refused")
        refreshed_ids.update(changed)
        require(len(refreshed_ids) <= 100, "more than 100 PRs changed metadata; bounded refresh refused")
        refresh_prs = [pr for pr in current_prs if pr["number"] in changed]
        # Same SHA is not permission to reuse old success: replace files, all
        # checks and trust/labels together, then bracket the WHOLE population
        # and main again. Head/base/population drift never takes this shortcut.
        if read_graphql:
            batched.update(batch_details(repo, refresh_prs, read_graphql, workers))
        # Mutable run/job state must be read again for a refreshed record;
        # snapshot-local caching never substitutes stale success on a retry.
        augment_policy = policy_provenance_reader(repo, get)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for record in executor.map(collect, refresh_prs):
                by_number[record["number"]] = record
        refreshes.append({"round": attempt + 1, "pr_numbers": changed, "reason": "same-head-metadata-changed-full-record-refreshed"})
        before = after
    records = [by_number[pr["number"]] for pr in prs]
    document = {"schema_version": 1, "kind": "delivery-queue-snapshot", "repo": repo, "main_sha": main,
                "started_at": started, "collected_at": isoformat(parse_now(now)), "complete": True,
                "mode": "full", "check_selection_version": 2, "managed_packages": managed, "pull_requests": records,
                "coverage": {"open_prs": len(prs), "heads_with_complete_checks": len(records)},
                "refresh_rounds": len(refreshes), "refreshes": refreshes,
                "remote_mutations": False}
    document["snapshot_id"] = hashlib.sha256(stable_json(document).encode()).hexdigest()
    return document


def classify(pr, main):
    if not pr["trusted"] or pr["draft"] or not pr["package_only"]:
        return "held", "untrusted-draft-or-multi-package"
    holds = sorted(set(pr["labels"]) & HOLDS)
    if holds:
        return "held", ",".join(holds)
    checks = pr["checks"]
    duplicates = duplicate_checks(checks)
    if any(not proven_policy_duplicates(pr, group) for group in duplicates):
        # An increasing check ID does not prove one workflow/suite supersedes
        # another. Preserve pending/failure evidence until admission resolves it.
        return "held", "ci-evidence-ambiguous"
    states = [check["state"] for check in checks]
    states += [check["workflow_provenance"][key] for group in duplicates for check in group
               for key in ("run_state", "suite_state")]
    if any(state in {"pending", "queued", "in_progress", "waiting", None} for state in states):
        return "waiting", "ci-pending"
    if pr["base_sha"] != main:
        return "repair", "base-changed"
    if any(state in {"failure", "error", "cancelled", "timed_out", "action_required", "startup_failure"} for state in states):
        return "repair", "ci-failed"
    if not all(any(check["name"] == name and check["state"] == "success" for check in checks) for name in REQUIRED):
        return "repair", "missing-or-incomplete-checks"
    return "merge-review", "requires-live-admission-and-physical-artifacts"


def task_fingerprint(payload, held=False):
    if "number" in payload:
        keys = ["number", "package_ids", "head_sha", "head_ref", "files", "labels", "draft", "trusted", "package_only"]
        if not held:
            keys += ["base_sha", "checks"]
        value = {key: payload.get(key) for key in keys}
        # Check order is transport trivia, not a changed test input/result.
        if "checks" in value:
            value["checks"] = sorted(value["checks"] or [], key=lambda item: stable_json(item, pretty=False))
    else:
        value = payload
    return hashlib.sha256(stable_json(value).encode()).hexdigest()


@contextlib.contextmanager
def database(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=30, isolation_level=None)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout=30000")
    connection.execute("BEGIN IMMEDIATE")
    try:
        connection.execute("CREATE TABLE IF NOT EXISTS snapshots(repo TEXT PRIMARY KEY, snapshot_id TEXT, main_sha TEXT, collected_at TEXT)")
        connection.execute("CREATE TABLE IF NOT EXISTS items(repo TEXT, item_key TEXT, package_id TEXT, queue TEXT, reason TEXT, head_sha TEXT, main_sha TEXT, payload TEXT, priority TEXT, PRIMARY KEY(repo,item_key))")
        connection.execute("CREATE TABLE IF NOT EXISTS leases(repo TEXT, package_id TEXT, lease_id TEXT UNIQUE, owner TEXT, item_key TEXT, head_sha TEXT, main_sha TEXT, expires REAL, PRIMARY KEY(repo,package_id))")
        connection.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, at TEXT, repo TEXT, lease_id TEXT, action TEXT, reason TEXT)")
        connection.execute("CREATE TABLE IF NOT EXISTS parks(repo TEXT, item_key TEXT, fingerprint TEXT, queue TEXT, reason TEXT, PRIMARY KEY(repo,item_key))")
        if "fingerprint" not in {row[1] for row in connection.execute("PRAGMA table_info(leases)")}:
            connection.execute("ALTER TABLE leases ADD COLUMN fingerprint TEXT NOT NULL DEFAULT ''")
        if "check_selection_version" not in {row[1] for row in connection.execute("PRAGMA table_info(snapshots)")}:
            connection.execute("ALTER TABLE snapshots ADD COLUMN check_selection_version INTEGER NOT NULL DEFAULT 0")
        yield connection
        connection.commit()
    except BaseException:
        connection.rollback()
        raise
    finally:
        connection.close()


def event(db, repo, lease_id, action, reason, now):
    db.execute("INSERT INTO events(at,repo,lease_id,action,reason) VALUES(?,?,?,?,?)", (isoformat(now), repo, lease_id, action, reason))


def repair_routing_policy_additions(before, after):
    """Return newly observed successful configure IDs, or None on any other change."""
    def configure(checks):
        return [c for c in checks if c.get("kind") == "check" and c.get("name") == "configure"]

    old_group, new_group = configure(before["checks"]), configure(after["checks"])
    if not old_group or len(new_group) <= len(old_group) or not proven_policy_duplicates(after, new_group):
        return None
    attempts = {(c["workflow_provenance"]["run_id"], c["workflow_provenance"]["run_attempt"]) for c in new_group}
    if len(attempts) != len(new_group):
        return None
    old = {c.get("id"): c for c in old_group}
    new = {c.get("id"): c for c in new_group}
    if len(old) != len(old_group) or not old.keys() <= new.keys():
        return None
    for ident, previous in old.items():
        observed = new[ident]
        # A former singleton gains provenance only as part of a now fully
        # authenticated group; its original core evidence must not change.
        if "workflow_provenance" not in previous and len(old_group) == 1:
            observed = {k: v for k, v in observed.items() if k != "workflow_provenance"}
        if observed != previous:
            return None
    added = sorted(new.keys() - old.keys())
    if any(new[ident]["workflow_provenance"][key] != "success" for ident in added
           for key in ("check_state", "run_state", "suite_state")):
        return None
    non_policy = [c for c in after["checks"] if c not in new_group]
    normalized = dict(after, checks=non_policy + old_group)
    if task_fingerprint(normalized) != task_fingerprint(before):
        return None
    return added


def owned_repair_routing(db, previous, current, lease, now):
    """Return added check IDs (possibly empty) only for this exact repair owner.

    The item stays held, including after lease expiry: no other dispatch worker
    can claim codex-repairing. Only routing labels and positively attested
    completed policy successes may be appended; this is not merge admission
    and does not verify or replace claim-repair's separate remote lease.
    """
    if not previous or not current or lease["expires"] <= now.timestamp():
        return None
    if current["queue"] != "held" or current["reason"] != "codex-repairing":
        return None
    if any(row["head_sha"] != lease["head_sha"] or row["main_sha"] != lease["main_sha"]
           or row["package_id"] != lease["package_id"] for row in (previous, current)):
        return None
    if not db.execute("SELECT 1 FROM events WHERE repo=? AND lease_id=? AND action='claimed' AND reason='repair'",
                      (lease["repo"], lease["lease_id"])).fetchone():
        return None
    before, after = json.loads(previous["payload"]), json.loads(current["payload"])
    old_labels, new_labels = set(before["labels"]), set(after["labels"])
    if previous["queue"] == "repair":
        if "repair-queued" not in old_labels or "codex-repairing" in old_labels:
            return None
        if new_labels != (old_labels - {"repair-queued"}) | {"codex-repairing"}:
            return None
    elif not (previous["queue"] == "held" and previous["reason"] == "codex-repairing" and old_labels == new_labels):
        return None
    after["labels"] = before["labels"]
    if lease["fingerprint"] != task_fingerprint(before):
        return None
    if task_fingerprint(after) == lease["fingerprint"]:
        return []
    return repair_routing_policy_additions(before, after)


def sync(db_path, document, candidates=None, now=None):
    timestamp = parse_now(now)
    require(document.get("kind") == "delivery-queue-snapshot" and document.get("schema_version") == 1 and document.get("complete") is True and document.get("mode") == "full", "a complete full delivery snapshot is required")
    require(document.get("check_selection_version") == 2, "snapshot uses superseded check selection; collect a fresh full snapshot")
    repo, main = document["repo"].lower(), document["main_sha"]
    require(bool(REPO.fullmatch(repo)) and bool(SHA.fullmatch(main)), "invalid snapshot identity")
    prs = document["pull_requests"]
    require(document["coverage"]["open_prs"] == len(prs) == document["coverage"]["heads_with_complete_checks"], "snapshot coverage mismatch")
    require(len({pr["number"] for pr in prs}) == len(prs), "duplicate PR number")
    original = dict(document)
    snapshot_id = original.pop("snapshot_id", None)
    require(snapshot_id == hashlib.sha256(stable_json(original).encode()).hexdigest(), "snapshot checksum mismatch")
    observed = parse_time(document["collected_at"])
    require(observed is not None and observed <= timestamp, "snapshot timestamp is in the future")
    occupied = set(document["managed_packages"])
    rows = []
    for pr in prs:
        occupied.update(pr["package_ids"])
        queue, reason = classify(pr, main)
        package = pr["package_ids"][0] if len(pr["package_ids"]) == 1 else ""
        rows.append((repo, f"pr:{pr['number']}", package, queue, reason, pr["head_sha"], main, stable_json(pr), pr["created_at"]))
    excluded = []
    for candidate in candidates or []:
        package = candidate.get("package_id")
        require(isinstance(package, str) and PACKAGE.fullmatch(package), "candidate needs a canonical package_id")
        if package in occupied:
            excluded.append({"package_id": package, "reason": "managed-or-open-pr-or-duplicate"})
            continue
        occupied.add(package)
        # Intake claim means audit/prepare; source, license, provider and tests
        # must still be validated by onboarding before any external mutation.
        queue = "held" if candidate.get("blocker") else "intake"
        reason = str(candidate.get("blocker") or "requires-onboarding-validation")
        rows.append((repo, f"intake:{package}", package, queue, reason, "", main, stable_json(candidate), "9999-" + package))
    with database(db_path) as db:
        previous = db.execute("SELECT * FROM snapshots WHERE repo=?", (repo,)).fetchone()
        require(previous is None or previous["collected_at"] <= document["collected_at"], "refusing to roll queue back to an older snapshot")
        expire(db, repo, timestamp)
        leased_items = {row["item_key"]: row for row in db.execute(
            "SELECT i.* FROM items i JOIN leases l ON i.repo=l.repo AND i.item_key=l.item_key WHERE i.repo=?", (repo,))}
        parks = {row["item_key"]: row for row in db.execute("SELECT * FROM parks WHERE repo=?", (repo,))}
        reconciled = []
        for row in rows:
            park = parks.get(row[1])
            if park and task_fingerprint(json.loads(row[7]), held=park["queue"] == "held") == park["fingerprint"]:
                row = row[:3] + (park["queue"], park["reason"]) + row[5:]
            elif park:
                db.execute("DELETE FROM parks WHERE repo=? AND item_key=?", (repo, row[1]))
            reconciled.append(row)
        rows = reconciled
        db.execute("DELETE FROM items WHERE repo=?", (repo,))
        db.executemany("INSERT INTO items VALUES(?,?,?,?,?,?,?,?,?)", rows)
        db.execute("INSERT OR REPLACE INTO snapshots VALUES(?,?,?,?,?)", (repo, snapshot_id, main, document["collected_at"], 2))
        for lease in db.execute("SELECT * FROM leases WHERE repo=?", (repo,)).fetchall():
            item = db.execute("SELECT * FROM items WHERE repo=? AND item_key=?", (repo, lease["item_key"])).fetchone()
            added = owned_repair_routing(db, leased_items.get(lease["item_key"]), item, lease, timestamp)
            if added is not None:
                fingerprint = task_fingerprint(json.loads(item["payload"]))
                if fingerprint != lease["fingerprint"]:
                    db.execute("UPDATE leases SET fingerprint=? WHERE lease_id=?", (fingerprint, lease["lease_id"]))
                    event(db, repo, lease["lease_id"], "repair-routing-preserved",
                          "same owner; item remains held; appended proven configure check IDs: "
                          + (",".join(map(str, added)) or "none"), timestamp)
                continue
            if lease["main_sha"] != main or not item or item["head_sha"] != lease["head_sha"] or item["queue"] not in QUEUES or lease["fingerprint"] != task_fingerprint(json.loads(item["payload"])):
                event(db, repo, lease["lease_id"], "invalidated", "main/head/task-input/eligibility changed", timestamp)
                db.execute("DELETE FROM leases WHERE lease_id=?", (lease["lease_id"],))
    return {"status": "synced", "repo": repo, "snapshot_id": snapshot_id, "items": len(rows), "excluded_candidates": excluded,
            "coordination_scope": "same-host-same-local-sqlite-file", "authorizes_remote_mutation": False}


def freshness(db, args, now):
    snapshot = db.execute("SELECT * FROM snapshots WHERE repo=?", (args.repo,)).fetchone()
    require(snapshot is not None, "no shared snapshot for repository")
    require(snapshot["check_selection_version"] == 2, "shared snapshot uses superseded check selection; refresh first")
    require(snapshot["main_sha"] == args.expected_main, "expected main differs from current shared snapshot")
    age = (now - parse_time(snapshot["collected_at"])).total_seconds()
    require(0 <= age <= args.max_age_seconds, "snapshot is stale; coordinator must refresh before more work")
    return snapshot


def expire(db, repo, now):
    for lease in db.execute("SELECT * FROM leases WHERE repo=? AND expires<=?", (repo, now.timestamp())).fetchall():
        event(db, repo, lease["lease_id"], "expired", "lease TTL elapsed", now)
    db.execute("DELETE FROM leases WHERE repo=? AND expires<=?", (repo, now.timestamp()))


def lease_action(args):
    now = parse_now(args.now)
    with database(args.db) as db:
        expire(db, args.repo, now)
        if args.command == "requeue":
            freshness(db, args, now)
            require(bool(args.reason.strip()), "requeue needs a verified changed-input/recovery reason")
            row = db.execute("SELECT * FROM items WHERE repo=? AND item_key=?", (args.repo, args.item_key)).fetchone()
            require(row is not None, "unknown queue item")
            require(db.execute("SELECT 1 FROM leases WHERE repo=? AND package_id=?", (args.repo, row["package_id"])).fetchone() is None, "cannot requeue a leased package")
            payload = json.loads(row["payload"])
            if args.item_key.startswith("pr:"):
                state, reason = classify(payload, row["main_sha"])
            else:
                state, reason = ("held", str(payload["blocker"])) if payload.get("blocker") else ("intake", "requires-onboarding-validation")
            # Explicit local requeue does not remove remote needs-human/native
            # labels or candidate blockers, and never resets claim-repair.
            db.execute("DELETE FROM parks WHERE repo=? AND item_key=?", (args.repo, args.item_key))
            db.execute("UPDATE items SET queue=?,reason=? WHERE repo=? AND item_key=?", (state, reason, args.repo, args.item_key))
            event(db, args.repo, "", "requeued", args.owner + ": " + args.item_key + ": " + args.reason, now)
            return {"status": "requeued", "queue": state, "item_key": args.item_key, "authorizes_remote_mutation": False}
        if args.command == "claim":
            snapshot = freshness(db, args, now)
            target = getattr(args, "item_key", None)
            row = db.execute("SELECT i.* FROM items i WHERE i.repo=? AND i.queue=? AND i.package_id<>'' AND (? IS NULL OR i.item_key=?) AND NOT EXISTS(SELECT 1 FROM leases l WHERE l.repo=i.repo AND l.package_id=i.package_id) ORDER BY priority,item_key LIMIT 1", (args.repo, args.queue, target, target)).fetchone()
            if row is None:
                require(not target, "requested item is absent, ineligible, in another queue or already leased")
                return {"status": "empty", "queue": args.queue, "authorizes_remote_mutation": False}
            lease_id = uuid.uuid4().hex
            expires = now.timestamp() + args.lease_seconds
            fingerprint = task_fingerprint(json.loads(row["payload"]))
            db.execute("INSERT INTO leases VALUES(?,?,?,?,?,?,?,?,?)", (args.repo, row["package_id"], lease_id, args.owner, row["item_key"], row["head_sha"], row["main_sha"], expires, fingerprint))
            event(db, args.repo, lease_id, "claimed", args.queue, now)
            return {"status": "claimed", "lease_id": lease_id, "owner": args.owner, "repo": args.repo,
                    "package_id": row["package_id"], "item_key": row["item_key"], "head_sha": row["head_sha"], "main_sha": row["main_sha"],
                    "snapshot_id": snapshot["snapshot_id"], "task_fingerprint": fingerprint, "expires_at": isoformat(parse_time(expires)), "item": json.loads(row["payload"]),
                    "authorizes_remote_mutation": False}
        lease = db.execute("SELECT * FROM leases WHERE repo=? AND lease_id=?", (args.repo, args.lease_id)).fetchone()
        require(lease is not None and lease["owner"] == args.owner, "lease expired, invalidated or owned by another worker")
        current = db.execute("SELECT payload FROM items WHERE repo=? AND item_key=?", (args.repo, lease["item_key"])).fetchone()
        require(current and lease["fingerprint"] == task_fingerprint(json.loads(current["payload"])), "lease task input changed; stale work cannot modify the new task")
        if args.command == "renew":
            snapshot = freshness(db, args, now)
            require(lease["main_sha"] == args.expected_main, "lease main is stale")
            expires = now.timestamp() + args.lease_seconds
            db.execute("UPDATE leases SET expires=? WHERE lease_id=?", (expires, args.lease_id))
            event(db, args.repo, args.lease_id, "renewed", "", now)
            routing = db.execute("SELECT at,reason FROM events WHERE repo=? AND lease_id=? AND action='repair-routing-preserved' ORDER BY rowid",
                                 (args.repo, args.lease_id)).fetchall()
            # An existing owner can bind a fresh local receipt after a
            # permitted append. The separate exact remote repair lease and
            # all live push fences remain mandatory.
            return {"status": "renewed", "lease_id": args.lease_id, "owner": args.owner, "repo": args.repo,
                    "package_id": lease["package_id"], "item_key": lease["item_key"], "head_sha": lease["head_sha"],
                    "main_sha": lease["main_sha"], "snapshot_id": snapshot["snapshot_id"],
                    "task_fingerprint": lease["fingerprint"], "expires_at": isoformat(parse_time(expires)),
                    "repair_routing_events": [dict(row) for row in routing], "authorizes_remote_mutation": False}
        else:
            state = {"complete": "completed", "waiting": "waiting", "blocked": "held"}.get(args.outcome)
            if state:
                row = db.execute("SELECT payload FROM items WHERE repo=? AND item_key=?", (args.repo, lease["item_key"])).fetchone()
                fingerprint = task_fingerprint(json.loads(row["payload"]), held=state == "held")
                db.execute("INSERT OR REPLACE INTO parks VALUES(?,?,?,?,?)", (args.repo, lease["item_key"], fingerprint, state, args.reason or args.outcome))
                db.execute("UPDATE items SET queue=?,reason=? WHERE repo=? AND item_key=?", (state, args.reason or args.outcome, args.repo, lease["item_key"]))
            event(db, args.repo, args.lease_id, "released", args.outcome + ": " + args.reason, now)
            db.execute("DELETE FROM leases WHERE lease_id=?", (args.lease_id,))
    return {"status": "released", "lease_id": args.lease_id, "authorizes_remote_mutation": False}


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    snapshot = commands.add_parser("snapshot", help="read-only full census; run once per coordinator round")
    snapshot.add_argument("--repo", required=True)
    snapshot.add_argument("--repo-root", default=".")
    snapshot.add_argument("--workers", type=int, default=4)
    snapshot.add_argument("--output", required=True)
    sync_parser = commands.add_parser("sync", help="import one shared snapshot and optional canonical candidate list")
    sync_parser.add_argument("--db", required=True)
    sync_parser.add_argument("--snapshot", required=True)
    sync_parser.add_argument("--candidates", help="JSON array of candidate objects with canonical package_id; optional blocker")
    for name in ("claim", "renew", "release", "requeue", "summary"):
        command = commands.add_parser(name)
        command.add_argument("--db", required=True)
        command.add_argument("--repo", required=True)
        if name != "summary":
            command.add_argument("--owner", required=True)
        if name in {"claim", "renew", "requeue"}:
            command.add_argument("--expected-main", required=True)
            command.add_argument("--lease-seconds", type=int, default=1800)
            command.add_argument("--max-age-seconds", type=int, default=900)
        if name == "claim":
            command.add_argument("--queue", choices=QUEUES, required=True)
            command.add_argument("--item-key", help="select one eligible unleased item in this queue; default is oldest eligible")
        elif name in {"renew", "release"}:
            command.add_argument("--lease-id", required=True)
        if name == "release":
            command.add_argument("--outcome", choices=("complete", "waiting", "blocked", "requeue"), required=True)
            command.add_argument("--reason", default="")
        elif name == "requeue":
            command.add_argument("--item-key", required=True)
            command.add_argument("--reason", required=True, help="verified input change or fulfilled recovery condition, not an unchanged retry")
    for command in commands.choices.values():
        if command is not snapshot:
            command.add_argument("--output")
        command.add_argument("--now")
    return result


def main():
    args = parser().parse_args()
    if hasattr(args, "repo"):
        require(bool(REPO.fullmatch(args.repo)), "repo must be OWNER/REPO")
        args.repo = args.repo.lower()
    if hasattr(args, "lease_seconds"):
        require(60 <= args.lease_seconds <= 86400 and 1 <= args.max_age_seconds <= 86400, "invalid lease/freshness bounds")
        require(bool(SHA.fullmatch(args.expected_main)), "expected-main must be an exact SHA")
    if args.command == "snapshot":
        require(os.environ.get("GITHUB_ACTIONS", "").lower() != "true", "snapshot is a local authenticated-gh operation")
        guard = subprocess.run([sys.executable, str(Path(args.repo_root) / "scripts/github-credential-guard"), "--repo-root", args.repo_root, "--require-auth", "--local-only"], capture_output=True, text=True)
        require(guard.returncode == 0, "credential guard failed")
        output = collect_snapshot(args.repo, args.workers, now=args.now, read_graphql=graphql_api)
    elif args.command == "sync":
        candidates = load_json(args.candidates) if args.candidates else []
        require(isinstance(candidates, list) and all(isinstance(item, dict) for item in candidates), "candidates must be a JSON array of canonical objects")
        output = sync(args.db, load_json(args.snapshot), candidates, args.now)
    elif args.command == "summary":
        with database(args.db) as db:
            snapshot = db.execute("SELECT * FROM snapshots WHERE repo=?", (args.repo,)).fetchone()
            output = {"repo": args.repo, "snapshot": dict(snapshot) if snapshot else None,
                      "queues": {row["queue"]: row["n"] for row in db.execute("SELECT queue,COUNT(*) n FROM items WHERE repo=? GROUP BY queue", (args.repo,))},
                      "active_leases": [dict(row) for row in db.execute("SELECT * FROM leases WHERE repo=? AND expires>?", (args.repo, parse_now(args.now).timestamp()))],
                      "coordination_scope": "same-host-same-local-sqlite-file", "authorizes_remote_mutation": False}
    else:
        output = lease_action(args)
    emit_json(output, args.output)
    return 0
