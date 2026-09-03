# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
HELPER = REPO / "ci" / "bridge-configure-context.py"
WORKFLOW = REPO / ".github" / "workflows" / "configure-context-bridge.yml"
REPOSITORY = "yinjiayi/openeuler-riscv-packages"
HEAD = "a" * 40
BASE = "b" * 40
SOURCE_RUN = 101
BRIDGE_RUN = 202


FAKE_GH = r'''#!/usr/bin/env python3
import base64 as b64
import json
import os
from pathlib import Path
import sys

args = sys.argv[1:]
scenario = os.environ.get("FAKE_GH_SCENARIO", "success")
state_path = Path(os.environ["FAKE_GH_STATE"])
log_path = Path(os.environ["FAKE_GH_LOG"])
try:
    state = json.loads(state_path.read_text(encoding="utf-8"))
except FileNotFoundError:
    state = {"pr_reads": 0, "check_status": "in_progress", "check_conclusion": None}
stdin = sys.stdin.read() if "--input" in args else ""
with log_path.open("a", encoding="utf-8") as stream:
    stream.write(json.dumps({"args": args, "stdin": stdin}) + "\n")

repo = "yinjiayi/openeuler-riscv-packages"
head = "a" * 40
base = "b" * 40

def save():
    state_path.write_text(json.dumps(state), encoding="utf-8")

def emit(value):
    save()
    print(json.dumps(value))
    raise SystemExit(0)

if args[:2] == ["pr", "merge"]:
    save()
    raise SystemExit(19 if scenario == "disable-nonzero" else 0)
if not args or args[0] != "api":
    print("unexpected fake gh command", file=sys.stderr)
    raise SystemExit(90)

method = "GET"
endpoint = None
i = 1
while i < len(args):
    item = args[i]
    if item in ("-H", "--header", "-X", "--method", "--input"):
        if item in ("-X", "--method"):
            method = args[i + 1]
        i += 2
    elif item in ("--paginate", "--slurp"):
        i += 1
    else:
        endpoint = item
        i += 1
if endpoint is None:
    raise SystemExit(91)
if scenario == "invalid-json" and endpoint.endswith("/actions/runs/202"):
    print("not-json")
    raise SystemExit(0)

source = {
    "id": 101,
    "name": "Auto Merge Policy",
    "path": ".github/workflows/auto-merge.yml",
    "event": "pull_request",
    "status": "completed",
    "conclusion": "action_required",
    "repository": {"full_name": repo},
    "head_repository": {"full_name": repo},
    "actor": {"login": "github-actions[bot]"},
    "triggering_actor": {"login": "github-actions[bot]"},
    "head_sha": head,
    "pull_requests": [{"number": 2011, "head": {"sha": head}, "base": {"sha": base}}],
}
if scenario == "ordinary":
    source["conclusion"] = "success"
    source["actor"] = {"login": "a-normal-contributor"}
    source["triggering_actor"] = {"login": "a-normal-contributor"}
if scenario == "wrong-actor":
    source["actor"] = {"login": "attacker"}
if scenario == "wrong-path":
    source["path"] = ".github/workflows/other.yml"

def image_lock(digest, built_at, status="published-public-anonymous-verified"):
    return """# SPDX-License-Identifier: Apache-2.0
schema_version: 1
image: ghcr.io/yinjiayi/openeuler-riscv64-rpmbuild
tag: 24.03-lts-sp3-rva23
digest: \"%s\"
status: %s
source_repository: https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/
repomd_sha256: \"%s\"
rpm_manifest_sha256: \"%s\"
containerfile_sha256: \"%s\"
built_at: \"%s\"
qemu_version: \"tonistiigi/binfmt:qemu-v9.2.0\"
self_test: passed
""" % (digest, status, "1" * 64, "2" * 64, "3" * 64, built_at)

bridge = {
    "id": 202,
    "name": "Configure Context Bridge",
    "path": ".github/workflows/configure-context-bridge.yml",
    "event": "workflow_run",
    "head_sha": base,
    "head_branch": "main",
    "repository": {"full_name": repo},
}
pull = {
    "number": 2011,
    "state": "open",
    "merged": False,
    "merged_at": None,
    "auto_merge": None,
    "draft": False,
    "user": {"login": "github-actions[bot]"},
    "head": {"sha": head, "ref": "infra/ci-image-123456abcdef", "repo": {"full_name": repo}},
    "base": {"sha": base, "ref": "main", "repo": {"full_name": repo}},
    "changed_files": 1,
}
if scenario == "branch-prefix":
    pull["head"]["ref"] = "infra/ci-image-deadbeefcafe"

if endpoint == f"repos/{repo}":
    emit({"full_name": repo, "default_branch": "main"})
if endpoint == f"repos/{repo}/git/ref/heads/main":
    emit({"ref": "refs/heads/main", "object": {"type": "commit", "sha": base}})
if endpoint == f"repos/{repo}/actions/runs/101":
    emit(source)
if endpoint == f"repos/{repo}/actions/runs/202":
    emit(bridge)
if endpoint == f"repos/{repo}/pulls/2011":
    state["pr_reads"] += 1
    if scenario == "auto-merge":
        pull["auto_merge"] = {"merge_method": "SQUASH"}
    if scenario == "post-race" and state["pr_reads"] >= 4:
        pull["head"]["sha"] = "c" * 40
    emit(pull)
if endpoint == f"repos/{repo}/pulls/2011/files?per_page=100":
    filename = "README.md" if scenario == "wrong-file" else "ci/image.lock"
    emit([[{"filename": filename, "status": "modified"}]])
if endpoint in (
    f"repos/{repo}/contents/ci/image.lock?ref={head}",
    f"repos/{repo}/contents/ci/image.lock?ref={base}",
):
    candidate = endpoint.endswith(head)
    digest = "sha256:" + (("123456abcdef" + "0" * 52) if candidate else "f" * 64)
    built_at = "2026-09-03T01:02:03Z" if candidate else "2026-09-02T01:02:03Z"
    status = "published-but-unverified" if scenario == "tampered-lock" and candidate else "published-public-anonymous-verified"
    raw = image_lock(digest, built_at, status).encode("utf-8")
    emit({
        "type": "file", "path": "ci/image.lock", "name": "image.lock",
        "encoding": "base64", "sha": "d" * 40, "size": len(raw),
        "content": b64.b64encode(raw).decode("ascii"),
    })
if endpoint == f"repos/{repo}/commits/{head}/statuses?per_page=100":
    statuses = [{"context": "configure", "state": "success"}] if scenario == "status-context" else []
    emit([statuses])
if endpoint == f"repos/{repo}/check-runs" and method == "POST":
    if scenario == "post-error":
        save()
        raise SystemExit(23)
    payload = json.loads(stdin)
    state.update({"external_id": payload["external_id"], "details_url": payload["details_url"]})
    emit({
        "id": 303, "name": payload["name"], "head_sha": payload["head_sha"],
        "external_id": payload["external_id"], "status": "in_progress",
    })
if endpoint == f"repos/{repo}/check-runs/303" and method == "PATCH":
    payload = json.loads(stdin)
    state["check_status"] = payload["status"]
    state["check_conclusion"] = payload["conclusion"]
    emit({"id": 303, **payload})
if endpoint == f"repos/{repo}/check-runs/303" and method == "GET":
    app = {"id": 999, "slug": "evil"} if scenario == "wrong-app" else {"id": 15368, "slug": "github-actions"}
    emit({
        "id": 303, "name": "configure", "head_sha": head,
        "status": state["check_status"], "conclusion": state["check_conclusion"],
        "external_id": state.get("external_id"), "details_url": state.get("details_url"),
        "app": app,
    })
if endpoint == f"repos/{repo}/commits/{head}/check-runs?check_name=configure&per_page=100":
    checks = [{"id": 404, "name": "configure"}] if scenario == "existing-check" else []
    page = {"total_count": len(checks), "check_runs": checks}
    emit([page] if "--slurp" in args else page)

print("unexpected fake gh API: %s %s" % (method, endpoint), file=sys.stderr)
save()
raise SystemExit(92)
'''


class ConfigureContextBridgeTests(unittest.TestCase):
    def run_helper(self, scenario: str, expected: int) -> tuple[dict, list[dict]]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            binary = root / "bin"
            binary.mkdir()
            fake = binary / "gh"
            fake.write_text(FAKE_GH, encoding="utf-8")
            fake.chmod(0o755)
            output = root / "evidence.json"
            log = root / "calls.jsonl"
            env = dict(os.environ)
            env.update({
                "PATH": str(binary) + os.pathsep + env.get("PATH", ""),
                "FAKE_GH_SCENARIO": scenario,
                "FAKE_GH_STATE": str(root / "state.json"),
                "FAKE_GH_LOG": str(log),
                "PYTHONDONTWRITEBYTECODE": "1",
            })
            completed = subprocess.run(
                [
                    str(HELPER),
                    "--repository", REPOSITORY,
                    "--source-run-id", str(SOURCE_RUN),
                    "--bridge-run-id", str(BRIDGE_RUN),
                    "--trusted-main-sha", BASE,
                    "--output", str(output),
                ],
                cwd=REPO,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(completed.returncode, expected, completed.stderr)
            self.assertTrue(output.is_file())
            self.assertFalse(output.with_name(output.name + ".tmp").exists())
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(json.loads(completed.stdout), result)
            calls = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
            return result, calls

    @staticmethod
    def api_calls(calls: list[dict], needle: str) -> list[dict]:
        return [call for call in calls if any(needle in arg for arg in call["args"])]

    def test_exact_bot_image_lock_pr_gets_one_checks_api_success(self) -> None:
        result, calls = self.run_helper("success", 0)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["check_run_id"], 303)
        self.assertEqual(result["image_digest"], "sha256:" + "123456abcdef" + "0" * 52)
        self.assertEqual(result["image_built_at"], "2026-09-03T01:02:03Z")
        posts = [call for call in calls if "-X" in call["args"] and "POST" in call["args"]]
        self.assertEqual(len(posts), 1)
        payload = json.loads(posts[0]["stdin"])
        self.assertEqual(payload["name"], "configure")
        self.assertEqual(payload["head_sha"], HEAD)
        self.assertEqual(payload["status"], "in_progress")
        self.assertIn(f":2011:{HEAD}:{BASE}:101:202", payload["external_id"])
        patches = [json.loads(call["stdin"]) for call in calls if "PATCH" in call["args"]]
        self.assertEqual([item["conclusion"] for item in patches], ["success"])
        self.assertFalse(any("/statuses/" in arg for call in calls for arg in call["args"]))
        self.assertFalse(any(call["args"] and call["args"][0] == "git" for call in calls))

    def test_non_action_required_source_is_safe_noop(self) -> None:
        result, calls = self.run_helper("ordinary", 0)
        self.assertEqual(result["status"], "not-applicable")
        self.assertFalse(any("check-runs" in arg for call in calls for arg in call["args"]))
        self.assertFalse(any(call["args"][:2] == ["pr", "merge"] for call in calls))

    def test_prewrite_attestation_failures_create_no_context(self) -> None:
        for scenario, fragment in (
            ("wrong-actor", "not initiated"),
            ("wrong-path", "provenance"),
            ("wrong-file", "unexpected path"),
            ("auto-merge", "auto-merge is armed"),
            ("status-context", "forbidden configure StatusContext"),
            ("existing-check", "configure CheckRun already exists"),
            ("tampered-lock", "publication status is not verified"),
            ("branch-prefix", "does not match the candidate digest prefix"),
            ("invalid-json", "not valid JSON"),
        ):
            with self.subTest(scenario=scenario):
                result, calls = self.run_helper(scenario, 1)
                self.assertEqual(result["status"], "failed")
                self.assertTrue(any(fragment in error for error in result["errors"]))
                self.assertFalse(any("POST" in call["args"] for call in calls))

    def test_post_create_race_marks_check_failed(self) -> None:
        result, calls = self.run_helper("post-race", 1)
        self.assertEqual(result["status"], "failed")
        patches = [json.loads(call["stdin"]) for call in calls if "PATCH" in call["args"]]
        self.assertEqual([item["conclusion"] for item in patches], ["failure"])

    def test_wrong_check_app_cannot_leave_successful_attestation(self) -> None:
        result, calls = self.run_helper("wrong-app", 1)
        self.assertEqual(result["status"], "failed")
        patches = [json.loads(call["stdin"]) for call in calls if "PATCH" in call["args"]]
        self.assertEqual([item["conclusion"] for item in patches], ["failure"])
        self.assertIn("GitHub Actions Checks app", result["errors"][0])

    def test_ambiguous_post_never_infers_success(self) -> None:
        result, calls = self.run_helper("post-error", 1)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["check_run_id"], None)
        self.assertTrue(self.api_calls(calls, "/commits/" + HEAD + "/check-runs"))
        self.assertFalse(any("success" in call["stdin"] for call in calls))

    def test_workflow_is_default_branch_only_and_never_checks_out_candidate(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("workflow_run:", workflow)
        self.assertIn("workflows: [Auto Merge Policy]", workflow)
        self.assertIn("workflow_dispatch:", workflow)
        self.assertNotIn("pull_request_target", workflow)
        self.assertIn("if: github.ref == 'refs/heads/main'", workflow)
        self.assertIn("ref: ${{ github.sha }}", workflow)
        self.assertNotIn("github.event.workflow_run.head_sha }}", workflow)
        self.assertNotIn("github.event.pull_request.head", workflow)
        self.assertIn("checks: write", workflow)
        self.assertIn("pull-requests: write", workflow)
        self.assertNotIn("statuses: write", workflow)
        self.assertIn("if: always()", workflow)
        self.assertIn("retention-days: 7", workflow)
        self.assertIn("actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a", workflow)


if __name__ == "__main__":
    unittest.main()
