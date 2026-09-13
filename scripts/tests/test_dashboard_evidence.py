# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import io
import json
import pathlib
import runpy
import stat
import tempfile
import unittest
import zipfile


ROOT = pathlib.Path(__file__).resolve().parents[2]
COLLECTOR = ROOT / "ci" / "collect-dashboard-evidence.py"


class DashboardEvidenceTests(unittest.TestCase):
    def test_extracts_only_bounded_regular_json_into_artifact_directory(self) -> None:
        module = runpy.run_path(str(COLLECTOR))
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, "w") as bundle:
            bundle.writestr("nested/build-result.json", json.dumps({"package_id": "demo", "status": "passed"}))
            bundle.writestr("../ignored.txt", "not json")
            symlink = zipfile.ZipInfo("link.json")
            symlink.create_system = 3
            symlink.external_attr = (stat.S_IFLNK | 0o777) << 16
            bundle.writestr(symlink, "target")
        with tempfile.TemporaryDirectory() as temporary:
            output = pathlib.Path(temporary)
            extracted = module["extract_json"](archive.getvalue(), output, 123)
            self.assertEqual(len(extracted), 1)
            destination = pathlib.Path(extracted[0])
            self.assertEqual(destination.parent, output / "123")
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8"))["package_id"], "demo")


if __name__ == "__main__":
    unittest.main()
