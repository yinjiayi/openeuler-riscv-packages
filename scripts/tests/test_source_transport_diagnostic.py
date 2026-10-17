# SPDX-License-Identifier: Apache-2.0
"""Guard the narrowly scoped hosted source probe, never execute target code."""
import ast
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/source-transport-diagnostic.yml"


class SourceTransportDiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.text = WORKFLOW.read_text()

    def test_hosted_read_only_and_immutable(self):
        self.assertIn("permissions:\n  contents: read\n", self.text)
        self.assertIn("runs-on: ubuntu-24.04", self.text)
        self.assertIn("timeout-minutes: 10", self.text)
        self.assertIn("ref: a59220b2321f5db3dc0b4520e4c72170e6cc498b", self.text)
        self.assertIn("persist-credentials: false", self.text)
        for forbidden in ("secrets.", "token:", "self-hosted", "workflow_dispatch:", "pull_request_target:"):
            self.assertNotIn(forbidden, self.text)
        uses = re.findall(r"uses: (\S+)", self.text)
        self.assertEqual(len(uses), 2)
        self.assertTrue(all(re.fullmatch(r"actions/[a-z-]+@[0-9a-f]{40}", item) for item in uses))

    def test_only_diagnostic_changes_trigger_probe(self):
        trigger = self.text.split("permissions:", 1)[0]
        paths = re.findall(r"^      - (.+)$", trigger, re.M)
        self.assertEqual(paths, [".github/workflows/source-transport-diagnostic.yml",
                                "scripts/tests/test_source_transport_diagnostic.py"])
        self.assertIn("  pull_request:", trigger)
        self.assertNotIn("  push:", trigger)

    def test_real_supported_verify_only_options(self):
        cli = (ROOT / "scripts/build-rpm").read_text()
        for option in ("--verify-only", "--download-timeout", "--retries"):
            self.assertIn('add_argument("' + option + '"', cli)
            self.assertIn(option, self.text)
        self.assertIn("--download-timeout 25 --retries 0", self.text)
        self.assertIn("! command -v rpmspec", self.text)
        self.assertIn("test ! -e work/source-transport-diagnostic", self.text)
        self.assertEqual(self.text.count("scripts/build-rpm --package-dir"), 1)
        self.assertNotIn("--offline", self.text)
        self.assertNotIn("curl ", self.text)
        self.assertNotIn("pip install", self.text)

    def test_three_fresh_physical_sources_and_schema_are_required(self):
        self.assertIn('validator["schema_errors"](result, schema, schema)', self.text)
        self.assertIn('fetch["cached"] is False', self.text)
        self.assertIn('fetch["status"] == 200', self.text)
        self.assertIn('hashlib.sha256(source.read_bytes()).hexdigest() == digest', self.text)
        for filename in ("libinjection-4.0.0.tar.gz", "COPYING.GPL2", "COPYING.GPL3"):
            self.assertIn('"' + filename + '": (', self.text)
        script = self.text.split("          python3 - <<'PY'\n", 1)[1].split("          PY\n", 1)[0]
        import textwrap
        ast.parse(textwrap.dedent(script))

    def test_actual_failure_evidence_is_retained_without_aliasing_attempts(self):
        self.assertIn("if: always()", self.text)
        self.assertIn("${{ github.run_id }}-${{ github.run_attempt }}", self.text)
        self.assertIn("retention-days: 7", self.text)
        self.assertIn("if-no-files-found: error", self.text)
        self.assertNotIn("continue-on-error", self.text)
        self.assertNotIn("actions/download-artifact", self.text)


if __name__ == "__main__":
    unittest.main()
