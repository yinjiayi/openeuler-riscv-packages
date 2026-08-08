# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import os
import pathlib
import runpy
import subprocess
import sys
import tempfile
import unittest


REPO = pathlib.Path(__file__).resolve().parents[2]
COMPOSER = REPO / "ci" / "compose-build-result.py"


def compose(root: pathlib.Path, native: bool) -> subprocess.CompletedProcess[str]:
    output = root / "build-result.json"
    arguments = [
        str(COMPOSER),
        "--package-id",
        "golden-needs-native-kmod" if native else "golden-success-hello",
        "--commit-sha",
        "a" * 40,
        "--job-id",
        "unit-test:compose",
        "--image-lock",
        str(root / "missing-image.lock"),
        "--metadata-result",
        "success",
        "--source-result",
        "success",
        "--patch-result",
        "success",
        "--rpmbuild-result",
        "success",
        "--smoke-result",
        "success",
        "--output",
        str(output),
    ]
    if native:
        arguments.append("--needs-native")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        arguments,
        cwd=str(REPO),
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


class ComposeBuildResultTests(unittest.TestCase):
    def test_smoke_phase_result_has_a_schema_branch(self) -> None:
        schema = json.loads((REPO / "schemas" / "build-result.schema.json").read_text(encoding="utf-8"))
        scripts_path = str(REPO / "scripts")
        sys.path.insert(0, scripts_path)
        try:
            schema_errors = runpy.run_path(str(REPO / "scripts" / "validate-metadata"))["schema_errors"]
        finally:
            sys.path.remove(scripts_path)
        document = {
            "schema_version": 1,
            "package_id": "golden-success-hello",
            "phase": "rpm-install-smoke",
            "status": "passed",
            "message": "RPM installation and package smoke test passed",
            "started_at": "2026-08-08T00:00:00Z",
            "finished_at": "2026-08-08T00:01:00Z",
        }
        self.assertEqual(schema_errors(document, schema, schema), [])
        document.pop("message")
        self.assertNotEqual(schema_errors(document, schema, schema), [])

    def test_native_route_does_not_claim_a_qemu_image(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            completed = compose(root, native=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            document = json.loads((root / "build-result.json").read_text(encoding="utf-8"))
            self.assertEqual(document["status"], "needs-native-riscv")
            self.assertEqual(document["classification"], "needs-native-riscv")
            self.assertIsNone(document["environment"]["image_digest"])
            self.assertEqual(document["environment"]["qemu_version"], "not-run-native-policy")
            self.assertEqual(document["checks"]["rpmbuild-riscv64"]["status"], "skipped")
            self.assertEqual(document["checks"]["rpm-install-smoke"]["status"], "skipped")

    def test_qemu_route_still_fails_closed_without_a_digest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            completed = compose(root, native=False)
            self.assertEqual(completed.returncode, 2)
            self.assertIn("image lock", completed.stderr)
            self.assertFalse((root / "build-result.json").exists())


if __name__ == "__main__":
    unittest.main()
