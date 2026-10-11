#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Current all-PR state with canonical identity from actual changed paths.

A snapshot drift is an observed change to the live PR population, main, or
paginated PR identity while a complete snapshot is being read. Only explicitly
typed drift may restart the entire collection, at most once. Attempts never
share pages or immutable-recipe caches. Authentication, schema and identity
failures remain fatal. A public attempt receipt contains fixed reason codes,
not private queries, response bodies, tokens, exception text or raw paths.
"""
from __future__ import annotations
import argparse, datetime, hashlib, json, os, pathlib, re, runpy, subprocess, tempfile, time

HERE = pathlib.Path(__file__).resolve().parent
H = runpy.run_path(str(HERE / "collect-build-history.py"))
QUERY = '''query($owner:String!,$name:String!,$cursor:String){repository(owner:$owner,name:$name){
 nameWithOwner defaultBranchRef{name target{oid}} pullRequests(first:25,after:$cursor,orderBy:{field:UPDATED_AT,direction:DESC}){
 totalCount pageInfo{hasNextPage endCursor} nodes{number title url state isDraft createdAt updatedAt mergedAt
 headRefName headRefOid baseRefName baseRefOid author{login} autoMergeRequest{enabledAt}
 labels(first:100){totalCount nodes{name}}
 headRef{target{... on Commit{oid statusCheckRollup{state contexts(first:30){totalCount pageInfo{hasNextPage endCursor}
 nodes{... on CheckRun{databaseId name status conclusion startedAt completedAt detailsUrl
 checkSuite{databaseId createdAt app{databaseId} commit{oid} workflowRun{databaseId runAttempt}}}
 ... on StatusContext{id context state targetUrl createdAt updatedAt commit{oid} creator{login}}}}}}}}
 headRepository{nameWithOwner} files(first:100){totalCount pageInfo{hasNextPage endCursor} nodes{path}}}}}}'''

MAX_SNAPSHOT_ATTEMPTS = 2


class SnapshotDrift(ValueError):
    """A specific changed-input fence, not arbitrary API or schema failure."""
    REASONS = {"main-during-pages", "pr-population-during-pages", "pr-head-during-files",
               "pr-files-population", "main-after-recipes", "pr-population-at-frontier",
               "pr-frontier-reordered"}

    def __init__(self, reason: str):
        if reason not in self.REASONS:
            raise ValueError("unknown snapshot drift reason")
        self.reason = reason
        super().__init__(reason)


def collect(repository: str, root: pathlib.Path, raw: pathlib.Path) -> dict:
    owner, name = repository.split("/"); raw.mkdir(parents=True, exist_ok=True)
    snapshot_started = H["iso"](datetime.datetime.now(datetime.timezone.utc))
    nodes = []; receipts = []; errors = []; cursor = None; main = None; expected = None; page = 0
    def graphql(query: str, variables: dict, label: str) -> dict:
        body = json.dumps({"query": query, "variables": variables}).encode()
        # GraphQL POST is a read query, not a mutation; token remains process env.
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
        for attempt in range(1, 4):
            result = subprocess.run(["gh", "api", "graphql", "--input", "-"], input=body,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90, check=False)
            if token and token.encode() in result.stdout + result.stderr:
                raise ValueError("credential response rejected")
            (raw / (label + ".attempt-%d.stderr" % attempt)).write_bytes(result.stderr[:16*1024*1024])
            (raw / (label + ".attempt-%d.json" % attempt)).write_bytes(result.stdout[:16*1024*1024])
            transient = any(code in result.stderr for code in (b"HTTP 502", b"HTTP 503", b"HTTP 504")) or not result.stdout
            if not result.returncode or not transient:
                break
            if attempt < 3: time.sleep(attempt)
        if len(result.stdout) > 16 * 1024 * 1024:
            raise ValueError("GraphQL response too large")
        p = raw / (label + ".json"); p.write_bytes(result.stdout)
        q = raw / (label + ".query.json"); q.write_bytes(body)
        receipts.append({"path": str(p), "sha256": hashlib.sha256(result.stdout).hexdigest(),
                         "query_path": str(q), "query_sha256": hashlib.sha256(body).hexdigest(), "exit": result.returncode})
        if result.returncode:
            raise ValueError("GraphQL read failed")
        document = json.loads(result.stdout)
        if document.get("errors"):
            raise ValueError("GraphQL returned errors; incomplete current snapshot")
        return document["data"]["repository"]

    while True:
        page += 1
        response = graphql(QUERY, {"owner": owner, "name": name, "cursor": cursor}, "pr-page-%03d" % page)
        head = response["defaultBranchRef"]["target"]["oid"]
        if main is not None and head != main:
            raise SnapshotDrift("main-during-pages")
        main = head; connection = response["pullRequests"]
        if expected is not None and expected != connection["totalCount"]:
            raise SnapshotDrift("pr-population-during-pages")
        expected = connection["totalCount"]; nodes.extend(connection["nodes"])
        for node in connection["nodes"]:
            node["checks_observed_at"] = H["iso"](datetime.datetime.now(datetime.timezone.utc))
        if not connection["pageInfo"]["hasNextPage"]:
            break
        newer = connection["pageInfo"]["endCursor"]
        if not newer or newer == cursor:
            raise ValueError("PR pagination cursor did not advance")
        cursor = newer
    if len(nodes) != expected or len({n["number"] for n in nodes}) != expected:
        raise ValueError("PR pages missing or duplicated entries")
    prs = []
    missing_metadata = []
    for node in nodes:
        files = node["files"]; paths = [f["path"] for f in files["nodes"]]
        complete = files["totalCount"] == len(paths) and not files["pageInfo"]["hasNextPage"]
        if not complete:
            file_cursor = files["pageInfo"]["endCursor"]
            while files["pageInfo"]["hasNextPage"]:
                query = '''query($owner:String!,$name:String!,$number:Int!,$cursor:String!){repository(owner:$owner,name:$name){
                  pullRequest(number:$number){headRefOid files(first:100,after:$cursor){totalCount pageInfo{hasNextPage endCursor} nodes{path}}}}}'''
                reply = graphql(query, {"owner": owner, "name": name, "number": node["number"], "cursor": file_cursor},
                                "pr-%d-files-%d" % (node["number"], len(paths)))
                current = reply["pullRequest"]
                if current["headRefOid"] != node["headRefOid"]:
                    raise SnapshotDrift("pr-head-during-files")
                files = current["files"]
                if files["totalCount"] != node["files"]["totalCount"]:
                    raise SnapshotDrift("pr-files-population")
                paths.extend(f["path"] for f in files["nodes"])
                newer = files["pageInfo"]["endCursor"]
                if files["pageInfo"]["hasNextPage"] and (not newer or newer == file_cursor):
                    raise ValueError("PR files cursor did not advance")
                file_cursor = newer
            complete = files["totalCount"] == len(paths) == len(set(paths))
        row = {"number": node["number"], "title": node["title"], "html_url": node["url"],
            "state": "closed" if node["state"] in ("CLOSED", "MERGED") else "open", "draft": node["isDraft"],
            "merged_at": node["mergedAt"], "created_at": node["createdAt"], "updated_at": node["updatedAt"],
            "head": {"sha": node["headRefOid"], "ref": node["headRefName"]}, "base": {"sha": node["baseRefOid"], "ref": node["baseRefName"]},
            "user": {"login": node["author"]["login"] if node["author"] else None}, "auto_merge": node["autoMergeRequest"],
            "changed_files": files["totalCount"], "actual_files": paths, "actual_files_complete": complete,
            "checks_observed_at": node["checks_observed_at"],
            "canonical_package_id": None, "recipe_tree_sha": None, "recipe_blob_sha": None, "recipe": None}
        row["files"] = [{"filename": path} for path in paths]
        row["labels"] = [{"name": item["name"]} for item in node["labels"]["nodes"]]
        row["labels_complete"] = node["labels"]["totalCount"] == len(row["labels"])
        target = (node.get("headRef") or {}).get("target") or {}
        rollup = target.get("statusCheckRollup") or {}
        contexts = rollup.get("contexts") or {"totalCount": 0, "nodes": [], "pageInfo": {"hasNextPage": False}}
        row["checks_complete"] = target.get("oid") == node["headRefOid"] and contexts["totalCount"] == len(contexts["nodes"]) and not contexts["pageInfo"]["hasNextPage"]
        row["check_selection_version"] = 1
        row["check_runs"] = [{"name": c["name"], "status": c["status"].lower(),
            "conclusion": c["conclusion"].lower() if c.get("conclusion") else None,
            "head_sha": c["checkSuite"]["commit"]["oid"], "html_url": c["detailsUrl"],
            "check_run_id": c.get("databaseId"), "app_id": (c["checkSuite"].get("app") or {}).get("databaseId"),
            "check_suite_id": c["checkSuite"].get("databaseId"), "check_suite_created_at": c["checkSuite"].get("createdAt"),
            "started_at": c.get("startedAt"), "completed_at": c.get("completedAt"),
            "workflow_run_id": (c["checkSuite"].get("workflowRun") or {}).get("databaseId"),
            "workflow_run_attempt": (c["checkSuite"].get("workflowRun") or {}).get("runAttempt")}
            for c in contexts["nodes"] if "name" in c]
        if any(c["head_sha"] != node["headRefOid"] for c in row["check_runs"]):
            row["checks_complete"] = False
        row["status_contexts"] = [{"context": c["context"], "state": c["state"].lower(), "target_url": c["targetUrl"],
            "id": c.get("id"), "head_sha": (c.get("commit") or {}).get("oid"),
            "creator_login": (c.get("creator") or {}).get("login"),
            "created_at": c.get("createdAt"), "updated_at": c.get("updatedAt")}
                                    for c in contexts["nodes"] if "context" in c]
        if any(c["head_sha"] != node["headRefOid"] for c in row["status_contexts"]):
            row["checks_complete"] = False
        row["check_selection_metadata_complete"] = row["checks_complete"] and all(
            all(type(c.get(key)) is int and c[key] > 0 for key in ("check_run_id", "app_id", "check_suite_id"))
            and isinstance(c.get("check_suite_created_at"), str) and bool(c["check_suite_created_at"])
            for c in row["check_runs"]
        ) and all(all(isinstance(c.get(key), str) and c[key] for key in ("id", "head_sha", "creator_login", "created_at", "updated_at")) for c in row["status_contexts"])
        row["check_rollup_state"] = rollup.get("state")
        if complete:
            try: row["canonical_package_id"] = H["canonical_package"](paths)
            except ValueError: pass  # Infrastructure/multi-package is not a guessed alias.
        else:
            errors.append({"pr": node["number"], "reason": "PR changed-files connection incomplete; canonical identity withheld"})
        pid = row["canonical_package_id"]; head = node["headRefOid"]
        row["package_id"] = pid
        row["canonical_identity_verified"] = bool(pid and complete)
        if node["state"] == "OPEN" and pid and (not row["checks_complete"] or not row["check_selection_metadata_complete"] or not row["labels_complete"]):
            errors.append({"pr": node["number"], "reason": "current canonical PR check/label connection incomplete; current status is a lower bound"})
        if pid and H["SHA"].fullmatch(head):
            tree = H["git_read"](root, ["rev-parse", head + ":packages/" + pid])
            blob = H["git_read"](root, ["rev-parse", head + ":packages/" + pid + "/package.yaml"])
            payload = H["git_read"](root, ["show", head + ":packages/" + pid + "/package.yaml"])
            if tree and blob and payload:
                metadata = json.loads(payload)
                if metadata.get("package_id") != pid: raise ValueError("PR metadata disagrees with actual canonical path")
                row.update(recipe_tree_sha=tree.decode().strip(), recipe_blob_sha=blob.decode().strip(), recipe=H["recipe_metadata"](metadata, head))
            elif node["state"] == "OPEN":
                missing_metadata.append(row)
        prs.append(row)
    # Exact immutable expressions in batches, only OPEN PR recipes not locally
    # available. GraphQL tree/blob oids avoid thousands of REST requests.
    for start in range(0, len(missing_metadata), 25):
        batch = missing_metadata[start:start+25]; fields = []
        for i, row in enumerate(batch):
            expression = row["head"]["sha"] + ":packages/" + row["canonical_package_id"]
            fields.append('t%d:object(expression:%s){oid ... on Tree{entries{name oid type}}}' % (i, json.dumps(expression)))
            fields.append('b%d:object(expression:%s){oid ... on Blob{text}}' % (i, json.dumps(expression + "/package.yaml")))
        query = 'query($owner:String!,$name:String!){repository(owner:$owner,name:$name){' + ' '.join(fields) + '}}'
        response = graphql(query, {"owner": owner, "name": name}, "open-recipes-%03d" % (start//25+1))
        for i, row in enumerate(batch):
            tree, blob = response.get("t%d" % i), response.get("b%d" % i)
            if not tree or not blob or blob.get("text") is None:
                errors.append({"pr": row["number"], "reason": "immutable PR recipe unavailable"}); continue
            metadata = json.loads(blob["text"])
            if metadata.get("package_id") != row["canonical_package_id"]:
                raise ValueError("remote PR recipe/path identity mismatch")
            entries = [e for e in tree["entries"] if e["name"] == "package.yaml" and e["oid"] == blob["oid"]]
            if len(entries) != 1: raise ValueError("PR tree/blob identity mismatch")
            row.update(recipe_tree_sha=tree["oid"], recipe_blob_sha=blob["oid"], recipe=H["recipe_metadata"](metadata, row["head"]["sha"]))
    final = graphql('query($owner:String!,$name:String!){repository(owner:$owner,name:$name){defaultBranchRef{name target{oid}}}}',
                    {"owner": owner, "name": name}, "main-after")
    if final["defaultBranchRef"]["target"]["oid"] != main:
        raise SnapshotDrift("main-after-recipes")
    # Updated-at fence: any PR mutation since that PR's first read puts its
    # current-head/check association on hold; do not backfill from old success.
    by_number = {row["number"]: row for row in prs}
    fence_cursor = None; fence_page = 0; fence_ids = set()
    while True:
        fence_page += 1
        frontier = graphql('''query($owner:String!,$name:String!,$cursor:String){repository(owner:$owner,name:$name){
           pullRequests(first:100,after:$cursor,orderBy:{field:UPDATED_AT,direction:DESC}){
             totalCount pageInfo{hasNextPage endCursor} nodes{number updatedAt headRefOid}}}}''',
           {"owner": owner, "name": name, "cursor": fence_cursor}, "pr-freshness-after-%03d" % fence_page)
        connection = frontier["pullRequests"]
        if connection["totalCount"] != expected:
            raise SnapshotDrift("pr-population-at-frontier")
        for item in connection["nodes"]:
            if item["number"] in fence_ids:
                raise SnapshotDrift("pr-frontier-reordered")
            fence_ids.add(item["number"])
            row = by_number[item["number"]]
            if row["head"]["sha"] != item["headRefOid"] or row["updated_at"] != item["updatedAt"]:
                row["snapshot_head_current"] = False; row["checks_complete"] = False
                errors.append({"pr": row["number"], "reason": "PR changed during current snapshot; current status withheld"})
        # Because the frontier is update-time descending, every mutation after
        # our first read appears before the first entry older than that read.
        if not connection["pageInfo"]["hasNextPage"] or (connection["nodes"] and connection["nodes"][-1]["updatedAt"] < snapshot_started):
            break
        newer = connection["pageInfo"]["endCursor"]
        if not newer or newer == fence_cursor: raise ValueError("PR freshness cursor did not advance")
        fence_cursor = newer
    for row in prs:
        row.setdefault("snapshot_head_current", True)
    # Current recent Actions facts are deliberately bounded, separate from the
    # exhaustive historical Package CI ledger. Never label this subset as full.
    api = H["API"](repository, raw / "recent-actions", 2)
    recent = api.get("actions/runs?per_page=100&page=1")
    return {"schema_version": 1, "generated_at": H["iso"](datetime.datetime.now(datetime.timezone.utc)),
            "repository": {"full_name": repository, "default_branch": "main"}, "main_sha": main,
            "pull_requests": prs, "workflow_runs": recent["workflow_runs"],
            "coverage": {"pull_request_total": expected, "pull_request_scanned": len(prs), "complete": not errors,
                         "snapshot_started_at": snapshot_started, "freshness_frontier_pages": fence_page,
                         "pages": page, "errors": errors, "workflow_runs_complete": recent["total_count"] <= 100,
                         "workflow_runs_returned": len(recent["workflow_runs"]), "workflow_runs_total_available": recent["total_count"]},
            "raw_receipts": receipts + api.receipts}


def collect_snapshot(repository: str, root: pathlib.Path, raw: pathlib.Path,
                     receipt_path: pathlib.Path) -> dict:
    """Two whole attempts at most, inside the existing 30-minute Pages timeout.

    A newly created private run directory also isolates repeated CLI invocations;
    never reuse partial pages from an earlier attempt or overwrite private proof.
    The safe receipt is written before each attempt so cancellation still leaves
    a truthful collecting state rather than missing evidence or claimed success.
    """
    raw.mkdir(parents=True, exist_ok=True)
    run_raw = pathlib.Path(tempfile.mkdtemp(prefix="snapshot-", dir=raw))
    receipt = {"schema_version": 1, "repository": repository, "status": "collecting",
               "maximum_attempts": MAX_SNAPSHOT_ATTEMPTS, "attempts": []}
    for number in range(1, MAX_SNAPSHOT_ATTEMPTS + 1):
        attempt = {"attempt": number, "status": "collecting",
                   "started_at": H["iso"](datetime.datetime.now(datetime.timezone.utc))}
        receipt["attempts"].append(attempt)
        H["save"](receipt_path, receipt)
        try:
            result = collect(repository, root, run_raw / ("attempt-%02d" % number))
        except SnapshotDrift as error:
            attempt.update(status="snapshot-drift", reason=error.reason,
                           completed_at=H["iso"](datetime.datetime.now(datetime.timezone.utc)))
            receipt["status"] = "collecting" if number < MAX_SNAPSHOT_ATTEMPTS else "failed"
            H["save"](receipt_path, receipt)
            if number == MAX_SNAPSHOT_ATTEMPTS:
                raise
        except Exception:
            # Do not copy arbitrary API/schema exception text to a public artifact.
            attempt.update(status="fatal", reason="fatal-input-or-api-error",
                           completed_at=H["iso"](datetime.datetime.now(datetime.timezone.utc)))
            receipt["status"] = "failed"
            H["save"](receipt_path, receipt)
            raise
        else:
            H["save"](run_raw / ("attempt-%02d" % number) / "receipt.json", result)
            attempt.update(status="collected",
                           completed_at=H["iso"](datetime.datetime.now(datetime.timezone.utc)))
            receipt["status"] = "collected"
            receipt["accepted_attempt"] = number
            H["save"](receipt_path, receipt)
            return result
    raise AssertionError("unreachable snapshot attempt limit")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY") or os.environ.get("GH_REPOSITORY"))
    p.add_argument("--repo-root", type=pathlib.Path, default=HERE.parent)
    p.add_argument("--raw-dir", type=pathlib.Path, required=True)
    p.add_argument("--output", type=pathlib.Path, required=True)
    p.add_argument("--receipt", type=pathlib.Path, required=True,
                   help="secret-safe collection attempt evidence; never raw API data")
    args = p.parse_args()
    if not args.repository or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repository): p.error("invalid repository")
    if args.output.exists() or args.receipt.exists():
        p.error("output and receipt must be fresh paths")
    if args.output.resolve() == args.receipt.resolve():
        p.error("output and receipt must be distinct paths")
    try:
        result = collect_snapshot(args.repository, args.repo_root, args.raw_dir, args.receipt)
    except Exception:
        # The safe summary survives for always-upload evidence; private attempts
        # retain the exact raw bodies for an authorized operator, not Pages.
        p.exit(1, "Current snapshot failed; see secret-safe collection receipt.\n")
    # Raw paths/queries and accepted raw receipt stay in the private attempt.
    result.pop("raw_receipts")
    H["save"](args.output, result)
    return 0


if __name__ == "__main__": raise SystemExit(main())
