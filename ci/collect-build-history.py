#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Checkpoint all available Package CI attempts, not retained artifacts.

Success means BOTH real build and install/smoke jobs AND their execution steps
passed. This API evidence is not RPM integrity, trusted acceptance or publication.
Run/head identity is separate from an entire package Git-tree recipe identity.
Deleted runs/logs cannot be recovered; failures always produce a lower bound.
"""
from __future__ import annotations

import argparse
import base64
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import subprocess
import threading
import time
import urllib.parse
import urllib.request
import urllib.error
from typing import Any

SHA = re.compile(r"^[0-9a-f]{40}$")
PACKAGE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BUILD_STEPS = {"Build SRPM and RPM with verified source networking", "Build SRPM and RPM without network"}
SMOKE_STEPS = {"Install RPM and run smoke test"}
INDEX_PATHS = {"catalog/package-index.json.gz", "catalog/package-index-summary.json", "catalog/package-index.json", "dashboard/data/index.json"}
MAX_RESPONSE = 8 * 1024 * 1024
# Three byte-identical historical workflow contracts span the 14 recorded
# protected workflow heads independently reviewed for legacy explicit dispatch.
# This is NOT a generic log/env fallback or a fabricated protected overlay.
LEGACY_DISPATCH_WORKFLOWS = {
    "729eb4d5b19325b09ab3f675c0725e54f18eb424d9a880a7df9910c49b9f9e75",
    "c240903907a69bb7b9de2bdb27ef991fef6b891c53113628823046bcb86b4747",
    "c25f7293303280b72e5f9c34d11279662bc0614600be4dd90f43878949f8ce30",
}


def timestamp(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(dt.timezone.utc)


def iso(value: dt.datetime) -> str:
    return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def save(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


class API:
    """Read-only gh; private immutable response cache, bounded calls and concurrency."""
    def __init__(self, repository: str, raw: pathlib.Path, budget: int = 4000,
                 recorded_jobs: pathlib.Path | None = None, wait_rate_limit: bool = False):
        self.repository, self.raw, self.budget = repository, raw, budget
        raw.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.calls = 0
        self.transport_calls = 0
        self.receipts: list[dict[str, Any]] = []
        self.thread = threading.local()
        self.recorded = json.loads(recorded_jobs.read_text()) if recorded_jobs else {}
        self.wait_rate_limit = wait_rate_limit
        self.rate_lock = threading.Lock()

    def get(self, endpoint: str, immutable: bool = False) -> Any:
        if endpoint in self.recorded:
            item = self.recorded[endpoint]
            payload = pathlib.Path(item["path"]).read_bytes()
            if digest(payload) != item["sha256"] or len(payload) > MAX_RESPONSE:
                raise ValueError("recorded historical jobs checksum mismatch")
            document = json.loads(payload)
            expected = re.fullmatch(r"actions/runs/([0-9]+)/attempts/([0-9]+)/jobs\?per_page=100&page=1", endpoint)
            if not expected or document.get("total_count") != len(document.get("jobs", [])) or not document["jobs"]:
                raise ValueError("recorded jobs incomplete or ambiguous empty run identity")
            if any(j.get("run_id") != int(expected[1]) or j.get("run_attempt") != int(expected[2])
                   or j.get("status") != "completed" for j in document["jobs"]):
                raise ValueError("recorded jobs run/attempt/terminal identity mismatch")
            receipt = {"endpoint": endpoint, "observed_at": None, "sha256": item["sha256"], "bytes": len(payload),
                       "path": item["path"], "reused": True, "purpose": "recorded-historical-terminal-API-evidence-not-fresh"}
            with self.lock:
                self.receipts.append(receipt)
            self.thread.receipts = getattr(self.thread, "receipts", []) + [receipt["sha256"]]
            return document
        key = digest(endpoint.encode())
        path, meta = self.raw / (key + ".json"), self.raw / (key + ".receipt.json")
        if immutable and path.exists() and meta.exists():
            receipt = json.loads(meta.read_text())
            payload = pathlib.Path(receipt["path"]).read_bytes()
            if receipt["endpoint"] != endpoint or receipt["sha256"] != digest(payload):
                raise ValueError("immutable raw checkpoint checksum mismatch")
            with self.lock:
                self.receipts.append(dict(receipt, reused=True))
            self.thread.receipts = getattr(self.thread, "receipts", []) + [receipt["sha256"]]
            return json.loads(payload)
        with self.lock:
            if self.calls >= self.budget:
                raise RuntimeError("API request budget exhausted; resume from checkpoint")
            self.calls += 1
        began = iso(dt.datetime.now(dt.timezone.utc))
        def request() -> subprocess.CompletedProcess:
            with self.lock: self.transport_calls += 1
            return subprocess.run(
            ["gh", "api", "--method", "GET", "-H", "Cache-Control: no-cache",
             "repos/" + self.repository + ("/" + endpoint if endpoint else "")],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, check=False,
            )
        result = request()
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
        if token and token.encode() in result.stdout + result.stderr:
            raise ValueError("credential in API response rejected without saving")
        if result.returncode and self.wait_rate_limit and b"rate limit exceeded" in result.stderr.lower():
            failed = self.raw / (key + ".primary-failure-" + str(time.time_ns()))
            failed.with_suffix(failed.suffix + ".stdout").write_bytes(result.stdout[:MAX_RESPONSE])
            failed.with_suffix(failed.suffix + ".stderr").write_bytes(result.stderr[:MAX_RESPONSE])
            with self.rate_lock:
                # rate_limit itself can return an inconsistent cached quota.
                # The failed actual endpoint's own signed-TLS HTTP headers are
                # authoritative for this request, not a second resource guess.
                with self.lock: self.transport_calls += 1
                quota = subprocess.run(["gh", "api", "--include", "--method", "GET", "-H", "Cache-Control: no-cache",
                         "repos/" + self.repository + "/" + endpoint], capture_output=True, timeout=60, check=False)
                if token and token.encode() in quota.stdout + quota.stderr:
                    raise ValueError("credential in quota response rejected")
                proof = self.raw / (key + ".quota-proof-" + str(time.time_ns()))
                proof.write_bytes(quota.stdout[:MAX_RESPONSE])
                proof.with_suffix(proof.suffix + ".stderr").write_bytes(quota.stderr[:MAX_RESPONSE])
                headers = dict((k.lower(), v.strip()) for k, v in re.findall(r"^(X-Ratelimit-[^:]+): ([^\r\n]+)", quota.stdout.decode("utf-8", "replace"), re.M | re.I))
                if quota.returncode == 0:
                    result = request()
                else:
                    if headers.get("x-ratelimit-resource") != "core" or headers.get("x-ratelimit-remaining") != "0" or not headers.get("x-ratelimit-reset", "").isdigit():
                        raise RuntimeError("secondary or unsupported rate limit; explicit resume required")
                    reset = int(headers["x-ratelimit-reset"])
                    wait = max(0, reset - time.time() + 2)
                    if wait > 3700: raise RuntimeError("primary reset exceeds approved bounded wait")
                    save(self.raw / "rate-wait.json", {"reset": reset, "remaining": 0, "seconds": wait,
                     "proof_path": str(proof), "proof_sha256": digest(quota.stdout[:MAX_RESPONSE]),
                     "reason": "primary quota exhausted; approved full backfill will resume after reset"})
                    while wait > 0:
                        time.sleep(min(wait, 30)); wait = max(0, reset - time.time() + 2)
                    result = request()
        payload = result.stdout
        if token and token.encode() in payload + result.stderr:
            raise ValueError("credential in API response rejected without saving")
        if len(payload) > MAX_RESPONSE:
            raise ValueError("API response exceeds bound")
        if result.returncode:
            # Never copy arbitrary transport stderr into public ledger.
            failed = self.raw / (key + ".failure-" + str(time.time_ns()))
            failed.with_suffix(failed.suffix + ".stdout").write_bytes(payload)
            failed.with_suffix(failed.suffix + ".stderr").write_bytes(result.stderr[:MAX_RESPONSE])
            raise RuntimeError("read-only API failed (exit %d)" % result.returncode)
        document = json.loads(payload)
        if isinstance(document, dict) and document.get("message"):
            raise RuntimeError("API error response")
        path = self.raw / (key + "-" + digest(payload) + ".json")
        receipt = {"endpoint": endpoint, "observed_at": began, "sha256": digest(payload),
                   "bytes": len(payload), "path": str(path), "reused": False}
        path.write_bytes(payload)
        # The mutable index points to an immutable, content-addressed response;
        # keep all prior bodies so recorded hashes remain physically rebindable.
        (self.raw / (key + ".json")).write_bytes(payload)
        save(meta, receipt)
        with self.lock:
            self.receipts.append(receipt)
        self.thread.receipts = getattr(self.thread, "receipts", []) + [receipt["sha256"]]
        return document

    def job_log(self, job_id: int) -> str:
        endpoint = "actions/jobs/%d/logs" % job_id
        key = digest(endpoint.encode()); meta = self.raw / (key + ".log.receipt.json")
        if meta.exists():
            receipt = json.loads(meta.read_text()); payload = pathlib.Path(receipt["path"]).read_bytes()
            if receipt["endpoint"] != endpoint or digest(payload) != receipt["sha256"]:
                raise ValueError("job log cache checksum mismatch")
        else:
            with self.lock:
                if self.calls >= self.budget: raise RuntimeError("API request budget exhausted; resume from checkpoint")
                self.calls += 1
                self.transport_calls += 1
            result = subprocess.run(["gh", "api", "--allow-escape-sequences", "--method", "GET", "repos/" + self.repository + "/" + endpoint],
                    capture_output=True, timeout=90, check=False)
            token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
            if token and token.encode() in result.stdout + result.stderr:
                raise ValueError("credential in job log rejected")
            if len(result.stdout) > 2 * 1024 * 1024: raise ValueError("scope job log exceeds 2MiB bound")
            if result.returncode:
                failure = self.raw / (key + ".log.failure-" + str(time.time_ns()))
                failure.write_bytes(result.stderr[:MAX_RESPONSE])
                raise ValueError("historical scope job log unavailable (exit %d)" % result.returncode)
            payload = result.stdout
            path = self.raw / (key + "-" + digest(payload) + ".log"); path.write_bytes(payload)
            receipt = {"endpoint": endpoint, "path": str(path), "sha256": digest(payload), "bytes": len(payload),
                       "observed_at": iso(dt.datetime.now(dt.timezone.utc)), "purpose": "inert-scope-log-identity-not-target-execution"}
            save(meta, receipt)
        with self.lock: self.receipts.append(receipt)
        self.thread.receipts = getattr(self.thread, "receipts", []) + [receipt["sha256"]]
        return payload.decode("utf-8", "strict")


def list_runs(api: API, start: dt.datetime, cutoff: dt.datetime) -> tuple[list[dict], list[dict]]:
    """Split inclusive second windows BEFORE pagination crosses GitHub's 1,000 cap."""
    found: dict[int, dict] = {}
    windows: list[dict] = []

    def visit(lo: dt.datetime, hi: dt.datetime) -> None:
        prefix = "actions/workflows/package-ci.yml/runs?per_page=100&created=" + iso(lo) + ".." + iso(hi)
        first = api.get(prefix + "&page=1")
        count = first.get("total_count")
        if not isinstance(count, int) or count < 0 or not isinstance(first.get("workflow_runs"), list):
            raise ValueError("invalid run listing")
        if count >= 1000:
            seconds = int((hi - lo).total_seconds())
            if seconds <= 1:
                raise ValueError("unsplittable same-second GitHub 1000-run limit")
            middle = lo + dt.timedelta(seconds=seconds // 2)
            visit(lo, middle)
            visit(middle, hi)
            return
        local: dict[int, dict] = {}
        pages = max(1, (count + 99) // 100)
        for number in range(1, pages + 1):
            page = first if number == 1 else api.get(prefix + "&page=" + str(number))
            if page.get("total_count") != count or len(page.get("workflow_runs", [])) > 100:
                raise ValueError("run window mutated or malformed during pagination")
            for run in page["workflow_runs"]:
                if run["path"].split("@")[0] != ".github/workflows/package-ci.yml":
                    raise ValueError("wrong workflow in Package CI listing")
                if not lo <= timestamp(run["created_at"]) <= hi or not SHA.fullmatch(run["head_sha"]):
                    raise ValueError("run outside exact window")
                if run["id"] in local:
                    raise ValueError("duplicate run inside page sequence")
                local[run["id"]] = run
        if len(local) != count:
            raise ValueError("run listing count mismatch or truncated page")
        for rid, run in local.items():
            if rid in found and found[rid]["head_sha"] != run["head_sha"]:
                raise ValueError("overlapping windows disagree on run head")
            found[rid] = run
        windows.append({"start": iso(lo), "end": iso(hi), "expected": count,
                        "observed": len(local), "pages": pages, "complete": True})

    visit(start, cutoff)
    return sorted(found.values(), key=lambda run: run["id"], reverse=True), windows


def successful_jobs(jobs: list[dict], run: dict, attempt: int, cutoff: str) -> dict | None:
    selected = {}
    for kind, name, steps in [("build", "rpmbuild-riscv64", BUILD_STEPS),
                              ("smoke", "rpm-install-smoke", SMOKE_STEPS)]:
        matches = []
        for job in jobs:
            if job.get("name") != name or job.get("head_sha") != run["head_sha"]:
                continue
            if job.get("run_id") != run["id"] or job.get("run_attempt") != attempt:
                raise ValueError("job run/attempt identity mismatch")
            if job.get("status") != "completed" or job.get("conclusion") != "success":
                continue
            # Package PR runs must never use the self-hosted pool. Historical
            # main builds may legitimately do so, but are never native proof.
            labels = job.get("labels", [])
            if run["event"] in ("pull_request", "merge_group") and "self-hosted" in labels:
                raise ValueError("PR build routed to forbidden self-hosted runner")
            actual = [step for step in job.get("steps", []) if step.get("name") in steps
                      and step.get("status") == "completed" and step.get("conclusion") == "success"]
            if len(actual) != 1:
                continue
            ended = actual[0].get("completed_at") or job.get("completed_at")
            if not ended or timestamp(ended) > timestamp(cutoff):
                continue
            matches.append({"id": job["id"], "name": name, "step_name": actual[0]["name"],
                            "step_number": actual[0]["number"], "completed_at": ended,
                            "runner_labels": labels})
        if len(matches) != 1:
            return None
        selected[kind] = matches[0]
    return selected


def canonical_package(paths: list[str]) -> str:
    ids = {path.split("/")[1] for path in paths if path.startswith("packages/") and len(path.split("/")) >= 3}
    if len(ids) != 1:
        raise ValueError("actual changed files do not select exactly one package")
    package = ids.pop()
    if not PACKAGE.fullmatch(package) or not all(path.startswith("packages/" + package + "/") or path in INDEX_PATHS or path == "dashboard/data/packages/" + package + ".json" for path in paths):
        raise ValueError("not package-only actual changed-file scope")
    return package


def git_read(root: pathlib.Path | None, args: list[str]) -> bytes | None:
    if root is None:
        return None
    result = subprocess.run(["git", "-C", str(root), *args], stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, timeout=30, check=False)
    return result.stdout if result.returncode == 0 else None


def recipe_metadata(metadata: dict, head: str) -> dict:
    # Distribution lineage includes functional providers/VCS variants and is
    # not an identity alias registry. Only explicit metadata aliases are used.
    aliases = {value for value in metadata.get("aliases", []) if isinstance(value, str)}
    if metadata.get("rpm", {}).get("name"):
        aliases.add(metadata["rpm"]["name"])
    if metadata.get("upstream", {}).get("component"):
        aliases.add(metadata["upstream"]["component"])
    version = metadata.get("version", {})
    return {"version": str(version.get("current", "")), "release": str(version.get("release", "")),
            "ref": head, "rpm_name": str(metadata.get("rpm", {}).get("name", "")),
            "aliases": sorted(aliases), "discovery_keys": [v for v in metadata.get("discovery_keys", []) if isinstance(v, str)]}


def unique_header_values(header: str, names: str) -> dict:
    values = re.findall(r"^  (" + names + r"): ([^\n]+)$", header, re.M)
    if len(values) != len({k for k, _ in values}):
        raise ValueError("scope header contains duplicate identity fields")
    return dict(values)


def scope_log_identity(text: str, run: dict) -> dict:
    # Only configure/scope job logs are read. Strip ANSI without evaluating it.
    clean = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)
    clean = "\n".join(re.sub(r"^\d{4}-\d\d-\d\dT\S+Z ", "", line) for line in clean.splitlines())
    matches = []
    for group in clean.split("##[group]Run ")[1:]:
        if not group.startswith("ci/materialize-package-head.py --repo-root ."):
            continue
        header, _, following = group.partition("##[endgroup]")
        env = unique_header_values(header, "PACKAGE_ID|PACKAGE_COMMIT_SHA|TOOLING_COMMIT_SHA")
        for line in following.splitlines():
            if not line.startswith('{"kind":"protected-main-package-overlay"'): continue
            overlay = json.loads(line)
            pid, head, tree = overlay.get("package_id"), overlay.get("package_commit_sha"), overlay.get("package_tree_sha")
            if (overlay.get("schema_version") != 1 or overlay.get("status") != "passed"
                or not PACKAGE.fullmatch(str(pid)) or not SHA.fullmatch(str(head)) or not SHA.fullmatch(str(tree))
                or env.get("PACKAGE_ID") != pid or env.get("PACKAGE_COMMIT_SHA") != head
                or env.get("TOOLING_COMMIT_SHA") != overlay.get("tooling_commit_sha")):
                raise ValueError("scope overlay/env identity mismatch")
            if run["event"] != "workflow_dispatch" and head != run["head_sha"]:
                raise ValueError("scope candidate disagrees with PR workflow head")
            if run["event"] == "workflow_dispatch" and overlay["tooling_commit_sha"] != run["head_sha"]:
                raise ValueError("dispatch scope tooling disagrees with workflow head")
            if run["event"] == "pull_request" and "change scope: package " + pid not in clean.splitlines():
                raise ValueError("scope log lacks actual package-only classification")
            matches.append({"package_id": pid, "head_sha": head, "recipe_tree_sha": tree,
                            "base_sha": overlay["tooling_commit_sha"]})
    if not matches and run["event"] != "workflow_dispatch":
        # Original protected/event configure contract before package-overlay
        # introduction: actual detect command env + successful scope output.
        # It remains tied to the exact workflow head, never title or branch.
        for group in clean.split("##[group]Run ")[1:]:
            header, _, following = group.partition("##[endgroup]")
            if "ci/detect-change-scope.py" not in header: continue
            env = unique_header_values(header, "BASE_SHA|HEAD_SHA")
            outputs = re.findall(r"^change scope: package ([a-z0-9]+(?:-[a-z0-9]+)*)$", following.split("##[group]", 1)[0], re.M)
            if len(outputs) == 1 and env.get("HEAD_SHA") == run["head_sha"] and SHA.fullmatch(env.get("BASE_SHA", "")):
                matches.append({"package_id": outputs[0], "head_sha": run["head_sha"], "recipe_tree_sha": None, "base_sha": env["BASE_SHA"]})
    if len(matches) != 1: raise ValueError("scope log lacks unique structured materialization identity")
    return matches[0]


def legacy_dispatch_identity(text: str, run: dict, root: pathlib.Path | None, api: API) -> dict:
    if run["event"] != "workflow_dispatch":
        raise ValueError("legacy explicit contract is dispatch-only")
    workflow = git_read(root, ["show", run["head_sha"] + ":.github/workflows/package-ci.yml"])
    if workflow is None:
        document = api.get("contents/.github/workflows/package-ci.yml?ref=" + run["head_sha"], immutable=True)
        if document.get("encoding") != "base64": raise ValueError("legacy workflow encoding unavailable")
        workflow = base64.b64decode(document["content"])
        if hashlib.sha1(b"blob " + str(len(workflow)).encode() + b"\0" + workflow).hexdigest() != document["sha"]:
            raise ValueError("legacy workflow Git blob mismatch")
    contract = digest(workflow)
    if contract not in LEGACY_DISPATCH_WORKFLOWS:
        raise ValueError("legacy workflow exact reviewed contract unavailable")
    clean = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)
    clean = "\n".join(re.sub(r"^\d{4}-\d\d-\d\dT\S+Z ", "", line) for line in clean.splitlines())
    checkouts, selects, policies = [], [], []
    for group in clean.split("##[group]Run ")[1:]:
        header, _, following = group.partition("##[endgroup]")
        if header.startswith("actions/checkout@"):
            if not header.startswith("actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n"):
                raise ValueError("legacy checkout action differs from exact historical contract")
            checkouts.append(unique_header_values(header, "ref|repository"))
        if 'ci/select-package-scope.py' in header:
            if '--package-id "$EXPLICIT_PACKAGE" --head "$HEAD_SHA"' not in header:
                raise ValueError("legacy explicit selection command contract mismatch")
            selects.append(unique_header_values(header, "BASE_SHA|HEAD_SHA|EXPLICIT_PACKAGE"))
        if 'ci/package-policy.py' in header:
            if 'ci/package-policy.py --package-dir "packages/$PACKAGE_ID"' not in header:
                raise ValueError("legacy package policy command contract mismatch")
            policies.append(unique_header_values(header, "MODE|PACKAGE_ID"))
    if len(checkouts) != 1 or len(selects) != 1 or len(policies) != 1:
        raise ValueError("legacy checkout/select/policy contract is nonunique")
    selected = selects[0]; head, package = selected.get("HEAD_SHA", ""), selected.get("EXPLICIT_PACKAGE", "")
    if (not SHA.fullmatch(head) or not PACKAGE.fullmatch(package)
        or checkouts[0] != {"ref": head, "repository": api.repository}
        or policies[0] != {"MODE": "package", "PACKAGE_ID": package}):
        raise ValueError("legacy explicit candidate/package/workflow identity mismatch")
    before_select = clean.split("##[group]Run mkdir -p artifacts/scope", 1)[0]
    if (len(re.findall(r"^\[command\]/usr/bin/git checkout --progress --force " + head + r"$", before_select, re.M)) != 1
        or len(re.findall(r"^\[command\]/usr/bin/git log -1 --format=%H\n" + head + r"$", before_select, re.M)) != 1):
        raise ValueError("legacy actual checkout/log does not prove candidate head")
    return {"package_id": package, "head_sha": head, "recipe_tree_sha": None,
            "base_sha": run["head_sha"], "legacy_contract_sha256": contract}


def resolve_recipe(api: API, run: dict, root: pathlib.Path | None, jobs: list[dict] | None = None, attempt: int | None = None) -> dict:
    head = run["head_sha"]
    # Dispatch may materialize a PR input SHA distinct from workflow main. Do
    # NOT guess input SHA/package from run-name, title, branch or artifact name.
    candidates = [p for p in run.get("pull_requests", []) if p.get("head", {}).get("sha") == head]
    scoped = None
    if run["event"] == "workflow_dispatch" or (run["event"] == "pull_request" and not candidates):
        if not jobs or attempt is None:
            raise ValueError("dispatch materialized candidate identity needs structured scope evidence")
        scope_jobs = [j for j in jobs if j.get("name") in ("change-scope", "configure") and j.get("run_id") == run["id"]
                      and j.get("run_attempt") == attempt and j.get("head_sha") == head
                      and j.get("status") == "completed" and j.get("conclusion") == "success"]
        if len(scope_jobs) != 1: raise ValueError("historical exact scope job unavailable or ambiguous")
        scope_text = api.job_log(scope_jobs[0]["id"])
        try:
            scoped = scope_log_identity(scope_text, run)
        except ValueError:
            if run["event"] != "workflow_dispatch": raise
            scoped = legacy_dispatch_identity(scope_text, run, root, api)
        head, base = scoped["head_sha"], scoped["base_sha"]
    elif run["event"] == "pull_request":
        bases = {p["base"]["sha"] for p in candidates if SHA.fullmatch(p.get("base", {}).get("sha", ""))}
        if len(bases) != 1:
            raise ValueError("historical PR base/head linkage unavailable")
        base = bases.pop()
    else:
        parent = git_read(root, ["rev-parse", head + "^1"])
        if parent:
            base = parent.decode().strip()
        else:
            commit = api.get("git/commits/" + head, immutable=True)
            if not commit.get("parents"):
                raise ValueError("root commit cannot resolve one-package delta")
            base = commit["parents"][0]["sha"]
    if scoped and run["event"] == "workflow_dispatch":
        # Rebuilding an existing main package legitimately has no commit delta.
        # Only actual structured protected materialization may name that package;
        # the independent exact entire Git tree + metadata check below is still
        # mandatory. Infrastructure-only jobs cannot satisfy successful_jobs.
        if scoped["recipe_tree_sha"] is None and not scoped.get("legacy_contract_sha256"):
            raise ValueError("dispatch materialization lacks whole recipe tree")
        package, method = scoped["package_id"], "exact-package-tree"
    else:
        merge_base = git_read(root, ["merge-base", "--all", base, head])
        if merge_base:
            ancestors = merge_base.decode().splitlines()
            if len(ancestors) != 1: raise ValueError("ambiguous multiple merge bases")
            base = ancestors[0]
        local_paths = git_read(root, ["diff", "--name-status", "--no-renames", "-z", base, head])
        if local_paths is not None:
            fields = [value.decode("utf-8") for value in local_paths.split(b"\0") if value]
            if len(fields) % 2: raise ValueError("invalid Git name-status response")
            paths = fields[1::2]  # no-renames represents both old and new paths
            method = "exact-local-git-delta"
        else:
            comparison = api.get("compare/" + base + "..." + head + "?per_page=1", immutable=True)
            files = comparison.get("files", [])
            if len(files) >= 300: raise ValueError("GitHub compare files reached unprovable 300-file limit")
            if comparison.get("base_commit", {}).get("sha") != base: raise ValueError("comparison base mismatch")
            ancestor = comparison.get("merge_base_commit", {}).get("sha", "")
            if not SHA.fullmatch(ancestor): raise ValueError("comparison merge-base identity unavailable")
            base = ancestor
            paths = [f["filename"] for f in files]
            if any(f.get("previous_filename") for f in files): raise ValueError("renamed package identity is ambiguous")
            method = "exact-compare-files"
        package = canonical_package(paths)
        if scoped and scoped["package_id"] != package:
            raise ValueError("scope selected package disagrees with exact changed paths")
    local_tree = git_read(root, ["rev-parse", head + ":packages/" + package])
    local_blob = git_read(root, ["rev-parse", head + ":packages/" + package + "/package.yaml"])
    payload = git_read(root, ["show", head + ":packages/" + package + "/package.yaml"])
    if local_tree and local_blob and payload:
        tree_sha, blob_sha = local_tree.decode().strip(), local_blob.decode().strip()
    else:
        tree = api.get("git/trees/" + head + ":packages/" + package, immutable=True)
        if tree.get("truncated"):
            raise ValueError("package Git tree truncated")
        entries = [e for e in tree["tree"] if e["path"] == "package.yaml" and e["type"] == "blob"]
        if len(entries) != 1:
            raise ValueError("canonical metadata blob missing")
        tree_sha, blob_sha = tree["sha"], entries[0]["sha"]
        blob = api.get("git/blobs/" + blob_sha, immutable=True)
        if blob.get("encoding") != "base64":
            raise ValueError("unsupported metadata encoding")
        payload = base64.b64decode(blob["content"], validate=False)
        if hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest() != blob_sha:
            raise ValueError("metadata blob Git hash mismatch")
    if not SHA.fullmatch(tree_sha) or not SHA.fullmatch(blob_sha):
        raise ValueError("invalid recipe Git identity")
    if scoped and scoped["recipe_tree_sha"] is not None and scoped["recipe_tree_sha"] != tree_sha:
        raise ValueError("scope materialized tree disagrees with exact Git recipe")
    metadata = json.loads(payload)
    if metadata.get("package_id") != package:
        raise ValueError("metadata canonical package disagrees with actual path")
    provenance = {"identity_method": "scope-log+" + method if scoped else method, "base_sha": base}
    if scoped and scoped.get("legacy_contract_sha256"):
        provenance.update(identity_method="legacy-workflow-contract+exact-package-tree",
                          workflow_contract_sha256=scoped["legacy_contract_sha256"])
    return {"package_id": package, "head_sha": head, "recipe_tree_sha": tree_sha,
            "recipe_blob_sha": blob_sha, "recipe": recipe_metadata(metadata, head),
            "provenance": provenance}


def valid_observation(row: dict) -> bool:
    basic = (isinstance(row, dict) and PACKAGE.fullmatch(str(row.get("package_id", ""))) is not None
            and all(SHA.fullmatch(str(row.get(k, ""))) for k in ("head_sha", "recipe_tree_sha", "recipe_blob_sha"))
            and row.get("build_status") == row.get("smoke_status") == "passed"
            and row.get("evidence_strength") == "hosted-step"
            and row.get("id") == "%s:%s:%s:%s" % (row.get("run_id"), row.get("run_attempt"), row.get("head_sha"), row.get("package_id"))
            and isinstance(row.get("jobs"), dict) and all(row["jobs"].get(k, {}).get("id") for k in ("build", "smoke")))
    if not basic:
        return False
    return (row.get("recipe", {}).get("ref") == row["head_sha"]
            and row["jobs"]["build"].get("name") == "rpmbuild-riscv64"
            and row["jobs"]["build"].get("step_name") in BUILD_STEPS
            and row["jobs"]["smoke"].get("name") == "rpm-install-smoke"
            and row["jobs"]["smoke"].get("step_name") in SMOKE_STEPS
            and row["jobs"]["build"]["id"] != row["jobs"]["smoke"]["id"]
            and all(isinstance(row["jobs"][k].get("step_number"), int) and row["jobs"][k]["step_number"] > 0 for k in ("build", "smoke")))


def required_format_checker(schema: dict):
    """Fail closed if this schema declares formats without installed handlers."""
    import jsonschema
    formats = set()

    def visit(node):
        if isinstance(node, dict):
            if isinstance(node.get("format"), str):
                formats.add(node["format"])
            for value in node.values():
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)

    visit(schema)
    checker = jsonschema.FormatChecker()
    missing = formats - checker.checkers.keys()
    if missing:
        raise ValueError("history schema format handlers unavailable: " + ", ".join(sorted(missing)))
    return checker


def validate_seed(seed: dict, repository: str) -> None:
    import jsonschema
    schema = json.loads((pathlib.Path(__file__).resolve().parents[1] / "schemas/build-history.schema.json").read_text())
    jsonschema.Draft202012Validator(schema, format_checker=required_format_checker(schema)).validate(seed)
    if seed["repository"] != repository:
        raise ValueError("history repository mismatch")
    cutoff = timestamp(seed["snapshot"]["cutoff"])
    observed_summary = {"distinct_package_count": len({r["package_id"] for r in seed["observations"]}),
        "distinct_recipe_count": len({(r["package_id"], r["recipe_tree_sha"]) for r in seed["observations"]}),
        "success_tuple_count": len(seed["observations"])}
    if seed["summary"] != observed_summary:
        raise ValueError("history summary disagrees with actual observations")
    for row in seed["observations"]:
        expected_url = "https://github.com/" + repository + "/actions/runs/" + str(row["run_id"])
        if not valid_observation(row) or row["run_url"] != expected_url or timestamp(row["completed_at"]) > cutoff:
            raise ValueError("history observation semantic identity mismatch")
        times = [timestamp(row["jobs"][k]["completed_at"]) for k in ("build", "smoke")]
        if timestamp(row["created_at"]) > min(times) or timestamp(row["completed_at"]) != max(times):
            raise ValueError("history job timestamps disagree with observation")
        if row["event"] in ("pull_request", "merge_group") and any("self-hosted" in row["jobs"][k]["runner_labels"] for k in ("build", "smoke")):
            raise ValueError("history PR used forbidden self-hosted runner")
        legacy = row["provenance"]["identity_method"] == "legacy-workflow-contract+exact-package-tree"
        if legacy and (row["event"] != "workflow_dispatch" or row["provenance"].get("workflow_contract_sha256") not in LEGACY_DISPATCH_WORKFLOWS):
            raise ValueError("legacy history lacks reviewed exact dispatch workflow contract")
        if row["event"] == "workflow_dispatch" and (not SHA.fullmatch(row.get("workflow_head_sha", "")) or not (legacy or row["provenance"]["identity_method"].startswith("scope-log+"))):
            raise ValueError("dispatch history lacks distinct workflow/candidate scope identity")
    seen = set()
    for row in seed["attempts"]:
        expected = "%s:%s:%s" % (row["run_id"], row["run_attempt"], row["head_sha"])
        if row["id"] != expected or row["id"] in seen:
            raise ValueError("duplicate or mismatched checkpoint identity")
        seen.add(row["id"])
        if row["status"] == "success" and not any(o["run_id"] == row["run_id"] and o["run_attempt"] == row["run_attempt"]
              and o.get("workflow_head_sha", o["head_sha"]) == row["head_sha"] for o in seed["observations"]):
            raise ValueError("success checkpoint has no bound successful observation")
        if row["status"] == "not-successful" and not row["terminal"]:
            raise ValueError("nonterminal negative checkpoint")
        if row["status"] == "pending" and row["terminal"]:
            raise ValueError("pending checkpoint marked terminal")
        if row["status"] == "unresolved" and (not row["terminal"] or not row.get("reason")):
            raise ValueError("unresolved checkpoint lacks terminal reason")


def merge_seed(seed: dict | None, repository: str) -> tuple[dict, dict]:
    if seed is None:
        return {}, {}
    validate_seed(seed, repository)
    if seed.get("schema_version") != 1 or seed.get("kind") != "package-build-history" or seed.get("repository") != repository:
        raise ValueError("history seed identity/schema invalid")
    rows = seed.get("observations")
    if not isinstance(rows, list) or not all(valid_observation(row) for row in rows):
        raise ValueError("history seed observations invalid")
    observations = {row["id"]: row for row in rows}
    if len(observations) != len(rows):
        raise ValueError("duplicate history seed observations")
    attempts = seed.get("attempts", [])
    if not isinstance(attempts, list) or not all(isinstance(a, dict) and isinstance(a.get("id"), str) for a in attempts):
        raise ValueError("history checkpoint attempts invalid")
    return observations, {row["id"]: row for row in attempts}


def published_seed(url: str, repository: str, raw: pathlib.Path, bootstrap: dict | None) -> dict:
    owner, repo = repository.split("/")
    base = "https://" + owner.lower() + ".github.io/" + repo + "/"
    if url != base + "build-history-ledger.json":
        raise ValueError("published seed must be the repository's exact normal-HTTPS Pages ledger")
    class SameOrigin(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, request, fp, code, msg, headers, newurl):
            if urllib.parse.urlparse(newurl).scheme != "https" or urllib.parse.urlparse(newurl).netloc != urllib.parse.urlparse(base).netloc:
                raise ValueError("published seed redirect changed HTTPS origin")
            return super().redirect_request(request, fp, code, msg, headers, newurl)
    opener = urllib.request.build_opener(SameOrigin())
    def fetch(address: str, filename: str) -> dict:
        request = urllib.request.Request(address, headers={"Cache-Control": "no-cache", "User-Agent": "openeuler-dashboard-history"})
        with opener.open(request, timeout=60) as response:
            payload = response.read(32 * 1024 * 1024 + 1)
            if response.status != 200 or len(payload) > 32 * 1024 * 1024:
                raise ValueError("published seed response exceeds bound or is not HTTP200")
        (raw / filename).write_bytes(payload)
        save(raw / (filename + ".receipt.json"), {"url": address, "sha256": digest(payload), "bytes": len(payload),
             "purpose": "durable-previous-Pages-state-not-seven-day-artifact", "observed_at": iso(dt.datetime.now(dt.timezone.utc))})
        return json.loads(payload)
    try:
        document = fetch(url, "published-seed.json")
    except urllib.error.HTTPError as error:
        if error.code != 404 or bootstrap is None:
            raise ValueError("published history seed unavailable; refusing to erase durable history") from error
        public = fetch(base + "data.json", "bootstrap-prior-dashboard.json")
        # A first deployment can have the original dashboard without any history
        # fields. Once history exists, missing ledger is a hard failure forever.
        if public.get("repository") != repository or "build_history" in public:
            raise ValueError("published ledger missing after history deployment; fail closed")
        document = bootstrap
        save(raw / "bootstrap-receipt.json", {"reason": "verified pre-history Dashboard; checked-in full backfill seed retained",
             "seed_sha256": digest(json.dumps(bootstrap, sort_keys=True).encode())})
    validate_seed(document, repository)
    return document


def union_seed(observations: dict, attempts: dict, seed: dict, repository: str) -> None:
    new_observations, new_attempts = merge_seed(seed, repository)
    for key, row in new_observations.items():
        if key in observations and observations[key] != row:
            left = json.loads(json.dumps(observations[key])); right = json.loads(json.dumps(row))
            left["provenance"].pop("api_raw_sha256"); right["provenance"].pop("api_raw_sha256")
            left.setdefault("workflow_head_sha", left["head_sha"]); right.setdefault("workflow_head_sha", right["head_sha"])
            if left != right: raise ValueError("conflicting durable history observation")
        observations[key] = row
    rank = {"pending": 0, "unresolved": 1, "not-successful": 2, "success": 3}
    for key, row in new_attempts.items():
        prior = attempts.get(key)
        if not prior or rank[row["status"]] >= rank[prior["status"]]: attempts[key] = row


def collect(api: API, runs: list[dict], cutoff: str, root: pathlib.Path | None,
            observations: dict, checkpoints: dict, workers: int, checkpoint_path: pathlib.Path,
            retry_unresolved: bool = False, reinterpret_cached_negative: bool = False) -> list[dict]:
    failures: list[dict] = []
    lock = threading.Lock()
    tasks = [(run, attempt) for run in runs for attempt in range(1, int(run["run_attempt"]) + 1)]
    # Scan successful latest runs first but NEVER truncate the population to it.
    tasks.sort(key=lambda pair: (pair[0].get("conclusion") != "success", -pair[0]["id"], pair[1]))

    completed = 0
    def write_checkpoint() -> None:
        save(checkpoint_path, {"repository": api.repository, "cutoff": cutoff,
             "observations": list(observations.values()), "attempts": list(checkpoints.values()), "failures": failures})

    def one(pair: tuple[dict, int]) -> None:
        nonlocal completed
        run, attempt = pair
        key = "%s:%s:%s" % (run["id"], attempt, run["head_sha"])
        prior = checkpoints.get(key)
        if prior and prior.get("terminal") and prior.get("status") in ("not-successful", "success"):
            endpoint = "actions/runs/%d/attempts/%d/jobs?per_page=100&page=1" % (run["id"], attempt)
            if not (reinterpret_cached_negative and prior["status"] == "not-successful" and endpoint in api.recorded): return
        if prior and prior.get("status") == "unresolved" and not retry_unresolved:
            with lock:
                failures.append({"run_id": run["id"], "run_attempt": attempt, "head_sha": run["head_sha"], "reason": prior["reason"]})
            return
        api.thread.receipts = []
        try:
            endpoint = "actions/runs/%d/attempts/%d/jobs?per_page=100&page=" % (run["id"], attempt)
            page = api.get(endpoint + "1", immutable=bool(prior and prior.get("terminal")) or attempt < int(run["run_attempt"]))
            count = page["total_count"]
            jobs = list(page["jobs"])
            for number in range(2, (count + 99) // 100 + 1):
                jobs.extend(api.get(endpoint + str(number), immutable=bool(prior and prior.get("terminal")) or attempt < int(run["run_attempt"]))["jobs"])
            if count != len(jobs) or len({j["id"] for j in jobs}) != count:
                raise ValueError("incomplete attempt jobs pagination")
            terminal = all(j.get("status") == "completed" for j in jobs) and (
                attempt < int(run["run_attempt"]) or run.get("status") == "completed")
            if any(j.get("completed_at") and timestamp(j["completed_at"]) > timestamp(cutoff) for j in jobs):
                terminal = False
            selected = successful_jobs(jobs, run, attempt, cutoff)
            state = {"id": key, "run_id": run["id"], "run_attempt": attempt,
                     "head_sha": run["head_sha"], "terminal": terminal, "status": "not-successful" if terminal else "pending",
                     "api_raw_sha256": list(api.thread.receipts)}
            if selected:
                identity = resolve_recipe(api, run, root, jobs, attempt)
                identity.update(id="%s:%s:%s:%s" % (run["id"], attempt, identity["head_sha"], identity["package_id"]), run_id=run["id"], run_attempt=attempt,
                                workflow_head_sha=run["head_sha"], event=run["event"], head_branch=run.get("head_branch"), created_at=run["created_at"],
                                completed_at=max(x["completed_at"] for x in selected.values()),
                                run_url="https://github.com/" + api.repository + "/actions/runs/" + str(run["id"]),
                                build_status="passed", smoke_status="passed", evidence_strength="hosted-step", jobs=selected)
                identity["provenance"]["api_raw_sha256"] = list(api.thread.receipts)
                state["status"] = "success"
                with lock:
                    observations[identity["id"]] = identity
            with lock:
                checkpoints[key] = state
        except Exception as error:
            with lock:
                failures.append({"run_id": run["id"], "run_attempt": attempt, "head_sha": run["head_sha"],
                                 "reason": str(error)[:300]})
                if "budget exhausted" not in str(error) and locals().get("terminal", False):
                    checkpoints[key] = {"id": key, "run_id": run["id"], "run_attempt": attempt, "head_sha": run["head_sha"],
                       "terminal": True, "status": "unresolved", "reason": str(error)[:300], "api_raw_sha256": list(api.thread.receipts)}
        finally:
            with lock:
                completed += 1
                if completed % 25 == 0:
                    write_checkpoint()

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        list(executor.map(one, tasks))
    write_checkpoint()
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY") or os.environ.get("GH_REPOSITORY"))
    parser.add_argument("--raw-dir", required=True, help="Private evidence/checkpoint directory, never upload to Pages")
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", help="Prior persistent safe ledger (not a seven-day artifact)")
    parser.add_argument("--published-seed-url", help="Exact repository Pages ledger; missing/degraded seed fails closed")
    parser.add_argument("--repo-root", type=pathlib.Path)
    parser.add_argument("--cutoff", default=iso(dt.datetime.now(dt.timezone.utc)))
    parser.add_argument("--max-requests", type=int, default=4000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--list-only", action="store_true")
    parser.add_argument("--resume-listing", help="Private checksum-bound complete listing checkpoint from same cutoff")
    parser.add_argument("--expected-listing-sha256")
    parser.add_argument("--retry-unresolved", action="store_true")
    parser.add_argument("--reinterpret-cached-negative", action="store_true", help="Maintenance: re-evaluate only checksum-bound cached terminal negative jobsets after verified historical contract upgrade; never refetch negatives")
    parser.add_argument("--recorded-jobs-index", type=pathlib.Path, help="Private checksum-bound complete terminal API job responses")
    parser.add_argument("--wait-rate-limit", action="store_true", help="Approved backfills only: checkpoint and wait for primary quota reset")
    args = parser.parse_args()
    if not args.repository or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repository):
        parser.error("repository must be owner/repository")
    if not 1 <= args.workers <= 6 or args.max_requests < 1:
        parser.error("workers must be 1..6 and request budget positive")
    started = iso(dt.datetime.now(dt.timezone.utc)); api = API(args.repository, pathlib.Path(args.raw_dir), args.max_requests,
                args.recorded_jobs_index, args.wait_rate_limit)
    reasons: list[dict] = []; runs = []; windows = []
    seed = json.loads(pathlib.Path(args.seed).read_text()) if args.seed else None
    observations, attempts = merge_seed(seed, args.repository)
    if args.published_seed_url:
        union_seed(observations, attempts, published_seed(args.published_seed_url, args.repository, pathlib.Path(args.raw_dir), seed), args.repository)
    checkpoint = pathlib.Path(args.raw_dir) / "checkpoint.json"
    if checkpoint.exists():
        cached = json.loads(checkpoint.read_text())
        if cached.get("repository") != args.repository or cached.get("cutoff") != args.cutoff:
            raise ValueError("private checkpoint repository/cutoff mismatch")
        # Private recovery is schema/semantic checked using the same envelope.
        envelope = {"schema_version": 1, "kind": "package-build-history", "repository": args.repository,
          "generated_at": started, "snapshot": {"cutoff": args.cutoff, "started_at": started, "coverage_complete": False,
          "lower_bound": True, "reasons": [], "listed_run_count": 0, "expected_attempt_count": 0, "processed_attempt_count": 0,
          "unresolved_count": 0, "windows": [], "deleted_history_recoverable": False}, "observations": cached.get("observations", []),
          "attempts": cached.get("attempts", []), "summary": {
             "distinct_package_count": len({r["package_id"] for r in cached.get("observations", [])}),
             "distinct_recipe_count": len({(r["package_id"], r["recipe_tree_sha"]) for r in cached.get("observations", [])}),
             "success_tuple_count": len(cached.get("observations", []))}, "limitations": []}
        validate_seed(envelope, args.repository)
        union_seed(observations, attempts, envelope, args.repository)
    try:
        repo = api.get("")
        created = repo["created_at"]
        if args.resume_listing:
            listing_bytes = pathlib.Path(args.resume_listing).read_bytes()
            if not args.expected_listing_sha256 or digest(listing_bytes) != args.expected_listing_sha256:
                raise ValueError("resume listing checksum mismatch or expected hash absent")
            listed = json.loads(listing_bytes)
            if listed["repository"] != args.repository or listed["cutoff"] != args.cutoff or not listed["complete"]:
                raise ValueError("resume listing identity or coverage mismatch")
            runs, windows = listed["runs"], listed["windows"]
            if not windows or windows[0]["start"] != created or windows[-1]["end"] != args.cutoff:
                raise ValueError("listing windows do not cover repository creation through cutoff")
            if len({r["id"] for r in runs}) != len(runs) or any(w["expected"] != w["observed"] or w["expected"] >= 1000 for w in windows):
                raise ValueError("listing duplicate runs or invalid window counts")
            if any(windows[i]["end"] != windows[i+1]["start"] for i in range(len(windows)-1)):
                raise ValueError("listing window coverage gap")
            for window in windows:
                in_window = [r for r in runs if timestamp(window["start"]) <= timestamp(r["created_at"]) <= timestamp(window["end"])]
                if len(in_window) != window["expected"]:
                    raise ValueError("listing run/window population mismatch")
            if any(r["path"].split("@")[0] != ".github/workflows/package-ci.yml" or not SHA.fullmatch(r["head_sha"]) or not timestamp(created) <= timestamp(r["created_at"]) <= timestamp(args.cutoff) for r in runs):
                raise ValueError("listing invalid run identity or timestamp")
        else:
            runs, windows = list_runs(api, timestamp(created), timestamp(args.cutoff))
            save(pathlib.Path(args.raw_dir) / "listing.json", {"repository": args.repository, "cutoff": args.cutoff,
                 "complete": True, "runs": runs, "windows": windows})
        if not args.list_only:
            reasons.extend(collect(api, runs, args.cutoff, args.repo_root, observations, attempts, args.workers, checkpoint, args.retry_unresolved, args.reinterpret_cached_negative))
        else:
            reasons.append({"reason": "listing-only: no historical attempt audit"})
    except Exception as error:
        created = locals().get("created", None)
        reasons.append({"reason": str(error)[:300]})
    expected = {(r["id"], a, r["head_sha"]) for r in runs for a in range(1, int(r["run_attempt"]) + 1)}
    checked = {(a["run_id"], a["run_attempt"], a["head_sha"]) for a in attempts.values()}
    missing = len(expected - checked)
    unresolved = sum(a["status"] == "unresolved" and (a["run_id"], a["run_attempt"], a["head_sha"]) in expected for a in attempts.values())
    pending = sum(a["status"] == "pending" and (a["run_id"], a["run_attempt"], a["head_sha"]) in expected for a in attempts.values())
    if pending:
        reasons.append({"reason": "available attempts pending at cutoff", "count": pending})
    if missing:
        reasons.append({"reason": "unresolved available run attempts", "count": missing})
    result = {"schema_version": 1, "kind": "package-build-history", "repository": args.repository,
              "generated_at": iso(dt.datetime.now(dt.timezone.utc)),
              "snapshot": {"cutoff": args.cutoff, "started_at": started, "repository_created_at": created,
                           "coverage_complete": not reasons, "lower_bound": bool(reasons), "reasons": reasons,
                           "listed_run_count": len(runs), "expected_attempt_count": len(expected),
                           "processed_attempt_count": len(expected & checked), "unresolved_count": missing + unresolved,
                           "windows": windows, "deleted_history_recoverable": False},
              "observations": sorted(observations.values(), key=lambda row: row["id"]),
              "attempts": sorted(attempts.values(), key=lambda row: row["id"]),
              "summary": {"distinct_package_count": len({r["package_id"] for r in observations.values()}),
                          "distinct_recipe_count": len({(r["package_id"], r["recipe_tree_sha"]) for r in observations.values()}),
                          "success_tuple_count": len(observations)},
              "limitations": ["Only GitHub-available runs/attempts can be scanned; deleted history is unknowable.",
                               "Hosted job+actual-step evidence is not physical RPM/SRPM or trusted/public release acceptance.",
                               "Artifact expiry does not remove retained API observations or earlier successful attempts."]}
    save(pathlib.Path(args.output), result)
    validate_seed(result, args.repository)
    save(pathlib.Path(args.raw_dir) / "collection-receipt.json", {"started_at": started,
         "finished_at": result["generated_at"], "api_calls": api.calls, "transport_calls_including_quota_probes_and_primary_retries": api.transport_calls,
         "api_calls_definition": "budgeted logical endpoint reads; immutable cache reads excluded; transport_calls includes primary-limit proof/retry overhead",
         "interpretation_policy": "verified-main-historical-step-names-v2", "reinterpret_cached_negative": args.reinterpret_cached_negative,
         "max_requests": args.max_requests,
         "raw_receipts": api.receipts, "output_sha256": digest(pathlib.Path(args.output).read_bytes())})
    print(json.dumps({"output": args.output, "summary": result["summary"], "snapshot": result["snapshot"], "api_calls": api.calls}))
    return 0 if not reasons else 2


if __name__ == "__main__":
    raise SystemExit(main())
