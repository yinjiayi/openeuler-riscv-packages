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
PROOF = REPO / "ci" / "prove-default-branch-head.py"
REPOSITORY = "yinjiayi/openeuler-riscv-packages"
HEAD = "a" * 40
STALE = "b" * 40


class DefaultBranchHeadProofTests(unittest.TestCase):
    def run_proof(
        self,
        *,
        event_base: str = HEAD,
        event_base_ref: str = "main",
        repository_response: object | None = None,
        ref_response: object | None = None,
        failure: str = "",
        expected: int,
    ) -> dict:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository_path = root / "repository.json"
            repository_path.write_text(json.dumps(
                repository_response if repository_response is not None else {"default_branch": "main"}
            ), encoding="utf-8")
            ref_path = root / "ref.json"
            ref_path.write_text(json.dumps(
                ref_response if ref_response is not None else {
                    "ref": "refs/heads/main",
                    "object": {"type": "commit", "sha": HEAD},
                }
            ), encoding="utf-8")
            fake_gh = root / "gh"
            fake_gh.write_text(textwrap.dedent("""\
                #!/usr/bin/env python3
                import os
                from pathlib import Path
                import sys

                args = sys.argv[1:]
                if args == ["api", os.environ["REPOSITORY_ENDPOINT"]]:
                    if os.environ["FAILURE"] == "repository":
                        raise SystemExit(17)
                    sys.stdout.write(Path(os.environ["REPOSITORY_RESPONSE"]).read_text())
                    raise SystemExit(0)
                if args == ["api", os.environ["REF_ENDPOINT"]]:
                    if os.environ["FAILURE"] == "ref":
                        raise SystemExit(18)
                    sys.stdout.write(Path(os.environ["REF_RESPONSE"]).read_text())
                    raise SystemExit(0)
                raise SystemExit(97)
            """), encoding="utf-8")
            fake_gh.chmod(0o755)
            env = os.environ.copy()
            env.update({
                "PATH": str(root) + os.pathsep + env["PATH"],
                "REPOSITORY_ENDPOINT": f"repos/{REPOSITORY}",
                "REF_ENDPOINT": f"repos/{REPOSITORY}/git/ref/heads/main",
                "REPOSITORY_RESPONSE": str(repository_path),
                "REF_RESPONSE": str(ref_path),
                "FAILURE": failure,
            })
            completed = subprocess.run([
                str(PROOF),
                "--repository", REPOSITORY,
                "--event-base", event_base,
                "--event-base-ref", event_base_ref,
            ], env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            self.assertEqual(completed.returncode, expected, completed.stderr)
            return json.loads(completed.stdout)

    def test_current_default_branch_head_passes(self) -> None:
        result = self.run_proof(expected=0)
        self.assertTrue(result["fresh"])
        self.assertEqual(result["default_head"], HEAD)

    def test_stale_head_or_nondefault_target_is_a_safe_noop(self) -> None:
        for arguments in (
            {"event_base": STALE},
            {"event_base_ref": "release"},
        ):
            with self.subTest(arguments=arguments):
                self.assertFalse(self.run_proof(expected=3, **arguments)["fresh"])

    def test_api_and_shape_failures_fail_closed(self) -> None:
        cases = (
            {"failure": "repository"},
            {"failure": "ref"},
            {"repository_response": []},
            {"repository_response": {}},
            {"ref_response": []},
            {"ref_response": {"object": {"type": "tag", "sha": HEAD}}},
            {"ref_response": {"object": {"type": "commit", "sha": "short"}}},
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                result = self.run_proof(expected=2, **arguments)
                self.assertFalse(result["fresh"])
                self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
