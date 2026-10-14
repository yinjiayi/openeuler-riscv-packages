# SPDX-License-Identifier: Apache-2.0
"""Run the actual smoke shell control flow with inert local transaction mocks."""
from __future__ import annotations

import json
import os
from pathlib import Path
import runpy
import shlex
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "ci" / "install-smoke.sh"


class InstallSmokeResultTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads((REPO / "schemas" / "build-result.schema.json").read_text())
        sys.path.insert(0, str(REPO / "scripts"))
        try:
            cls.schema_errors = staticmethod(runpy.run_path(str(REPO / "scripts" / "validate-metadata"))["schema_errors"])
        finally:
            sys.path.remove(str(REPO / "scripts"))

    def run_case(self, *, smoke_status=0, dnf_status=0, repository_status=0,
                 native=False, missing_work=False, missing_rpms=False,
                 write_status=0):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "demo"
            (package / "tests").mkdir(parents=True)
            (package / "package.yaml").write_text(json.dumps({"build": {"profile": "needs-native-riscv" if native else "qemu"}}))
            (package / "tests" / "smoke.sh").write_text(f"#!/bin/bash\nexit {smoke_status}\n")
            work = root / "work"
            if not missing_work:
                work.mkdir()
                if not missing_rpms:
                    (work / "RPMS").mkdir()
                    # Inert bytes: the mock transaction never reads or installs this file.
                    (work / "RPMS" / "demo.rpm").write_bytes(b"not an RPM")
            repository = root / "project.repo"
            repository.write_text("""[openeuler-riscv-project]
name=Local inert test
baseurl=http://2.27.148.101:38080/
enabled=0
gpgcheck=0
repo_gpgcheck=0
metadata_expire=never
skip_if_unavailable=1
module_hotfixes=1
""")
            evidence = root / "resolution.json"
            evidence.write_text(json.dumps({
                "kind": "supplemental-repository-resolution",
                "state_url": "http://2.27.148.101:38080/state.json",
                "status": "unavailable", "reason": "endpoint-unavailable",
                "generation": None, "state_sha256": None, "repositories": {},
                "fallback": {"active_repository_ids": ["openeuler-rva23"], "supplemental_repository_enabled": False},
            }))
            source = SCRIPT.read_text()
            marker = "supplemental_repo=/etc/yum.repos.d/openeuler-riscv-project.repo"
            self.assertEqual(source.count(marker), 1)
            # Relocate only the fixed system repository path in a disposable copy;
            # the real parser, traps, status branches and smoke invocation are unchanged.
            sandbox_script = root / "install-smoke.sh"
            sandbox_script.write_text(source.replace(marker, "supplemental_repo=" + shlex.quote(str(repository))))
            mocks = root / "bin"
            mocks.mkdir()
            python_mock = mocks / "python3"
            python_mock.write_text(f"""#!{sys.executable}
import os, sys
if os.environ.get('RESULT_STATUS'):
    code = int(os.environ['MOCK_WRITE_STATUS'])
    if code:
        raise SystemExit(code)
elif sys.argv[1:] and sys.argv[1] == 'ci/run-dnf-transaction':
    # Never invoke the supplied dnf argv or any target/backend command.
    raise SystemExit(int(os.environ['MOCK_DNF_STATUS']))
elif len(sys.argv) > 2 and sys.argv[2].endswith('project.repo'):
    code = int(os.environ['MOCK_REPOSITORY_STATUS'])
    if code:
        raise SystemExit(code)
os.execv(sys.executable, [sys.executable] + sys.argv[1:])
""")
            python_mock.chmod(0o755)
            bash_env = root / "bash-env"
            # Bash 3.2 on macOS lacks mapfile. This mock preserves the target's
            # exact NUL-delimited RPM-list semantics without installing a shell.
            bash_env.write_text("""mapfile() {
  [[ $# = 3 && $1 = -d && -z $2 && $3 = rpms ]] || return 99
  rpms=()
  local item
  while IFS= read -r -d '' item; do rpms+=("$item"); done
}
""")
            result = root / "result.json"
            env = dict(os.environ, PATH=str(mocks) + os.pathsep + os.environ["PATH"],
                       BASH_ENV=str(bash_env), MOCK_DNF_STATUS=str(dnf_status),
                       MOCK_REPOSITORY_STATUS=str(repository_status),
                       MOCK_WRITE_STATUS=str(write_status),
                       PRIVATE_COMMAND_CANARY="secret-not-for-result")
            for key in ("RESULT_STATUS", "RESULT_MESSAGE", "RESULT_PACKAGE", "RESULT_STARTED"):
                env.pop(key, None)
            completed = subprocess.run(["/bin/bash", str(sandbox_script), str(package), str(work), str(result), str(evidence)],
                                       cwd=REPO, env=env, capture_output=True, text=True, timeout=15)
            document = json.loads(result.read_text()) if result.exists() else None
            if document is not None:
                self.assertEqual(self.schema_errors(document, self.schema, self.schema), [], document)
                self.assertNotIn("secret-not-for-result", json.dumps(document))
                self.assertNotIn(str(root), document["message"])
                self.assertEqual(document["package_id"], "demo")
                self.assertEqual(document["phase"], "rpm-install-smoke")
            return completed, document

    def test_failing_smoke_has_message_and_original_exit_status(self):
        completed, result = self.run_case(smoke_status=42)
        self.assertEqual(completed.returncode, 42, completed.stderr)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["message"], "RPM installation or package smoke test failed (exit status 42); see smoke.log")

    def test_early_unassigned_command_failure_is_schema_valid(self):
        completed, result = self.run_case(repository_status=53)
        self.assertEqual(completed.returncode, 53, completed.stderr)
        self.assertEqual(result["status"], "failed")
        self.assertIn("exit status 53", result["message"])

    def test_existing_installation_message_is_preserved(self):
        completed, result = self.run_case(dnf_status=37)
        self.assertEqual(completed.returncode, 37, completed.stderr)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["message"], "bounded RPM installation DNF transaction failed; see dnf-transaction.json")

    def test_missing_work_directory_message_is_preserved(self):
        completed, result = self.run_case(missing_work=True)
        self.assertEqual(completed.returncode, 2, completed.stderr)
        self.assertEqual(result["message"], "package or work directory is missing")

    def test_missing_binary_rpm_message_is_preserved(self):
        completed, result = self.run_case(missing_rpms=True)
        self.assertEqual(completed.returncode, 1, completed.stderr)
        self.assertEqual(result["message"], "binary RPM output directory is missing")

    def test_native_policy_status_and_message_are_preserved(self):
        completed, result = self.run_case(native=True)
        self.assertEqual(completed.returncode, 1, completed.stderr)
        self.assertEqual(result["status"], "needs-native-riscv")
        self.assertEqual(result["message"], "package policy requires native RISC-V validation; no self-hosted runner is configured")

    def test_success_status_and_message_are_preserved(self):
        completed, result = self.run_case()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["message"], "RPM installation and package smoke test passed")

    def test_result_write_failure_does_not_mask_original_failure(self):
        completed, result = self.run_case(smoke_status=42, write_status=37)
        self.assertEqual(completed.returncode, 42, completed.stderr)
        self.assertIsNone(result)

    def test_result_write_failure_cannot_make_success_pass(self):
        completed, result = self.run_case(write_status=37)
        self.assertEqual(completed.returncode, 37, completed.stderr)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
