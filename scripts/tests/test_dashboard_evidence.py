# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import io
import json
import pathlib
import runpy
import stat
import subprocess
import tempfile
import unittest
from unittest import mock
import zipfile


ROOT = pathlib.Path(__file__).resolve().parents[2]
COLLECTOR = ROOT / "ci" / "collect-dashboard-evidence.py"


class DashboardEvidenceTests(unittest.TestCase):
    def test_artifact_listing_retries_truncated_page_without_slurping(self) -> None:
        module = runpy.run_path(str(COLLECTOR))
        fetch = module["list_artifacts"]
        calls: list[str] = []

        def fake_gh(*arguments: str, **kwargs: object) -> str:
            self.assertEqual(arguments[0], "api")
            self.assertEqual(kwargs, {"timeout_seconds": 30})
            calls.append(arguments[1])
            if len(calls) == 1:
                return '{"artifacts": ['
            if arguments[1].endswith("&page=1"):
                return json.dumps({"artifacts": [{"id": index} for index in range(1, 26)]})
            return json.dumps({"artifacts": [{"id": 25}, {"id": 26}]})

        with mock.patch.dict(fetch.__globals__, {"gh": fake_gh}):
            with mock.patch.object(fetch.__globals__["time"], "sleep") as sleep:
                artifacts, pages, retries = fetch("example/repository")
        self.assertEqual([item["id"] for item in artifacts], list(range(1, 27)))
        self.assertEqual((pages, retries), (2, 1))
        self.assertEqual(len(calls), 3)
        self.assertTrue(all("per_page=25" in item for item in calls))
        self.assertTrue(all("--paginate" not in item for item in calls))
        sleep.assert_called_once_with(1)

    def test_artifact_listing_fails_closed_after_repeated_truncation(self) -> None:
        module = runpy.run_path(str(COLLECTOR))
        fetch = module["list_artifacts"]
        with mock.patch.dict(fetch.__globals__, {"gh": lambda *args, **kwargs: '{"artifacts": ['}):
            with mock.patch.object(fetch.__globals__["time"], "sleep"):
                with self.assertRaisesRegex(RuntimeError, "page 1 failed after 6 attempts"):
                    fetch("example/repository")

    def test_artifact_listing_retries_subprocess_timeout(self) -> None:
        module = runpy.run_path(str(COLLECTOR))
        fetch = module["list_artifacts"]
        calls = 0

        def fake_gh(*arguments: str, **kwargs: object) -> str:
            nonlocal calls
            calls += 1
            if calls == 1:
                raise subprocess.TimeoutExpired("gh api", 30)
            return json.dumps({"artifacts": [{"id": 1}]})

        with mock.patch.dict(fetch.__globals__, {"gh": fake_gh}):
            with mock.patch.object(fetch.__globals__["time"], "sleep") as sleep:
                artifacts, pages, retries = fetch("example/repository")
        self.assertEqual(([item["id"] for item in artifacts], pages, retries), ([1], 1, 1))
        sleep.assert_called_once_with(1)

    def test_artifact_listing_rejects_invalid_page_shape(self) -> None:
        module = runpy.run_path(str(COLLECTOR))
        fetch = module["list_artifacts"]
        with mock.patch.dict(fetch.__globals__, {"gh": lambda *args, **kwargs: '{"artifacts": {}}'}):
            with self.assertRaisesRegex(ValueError, "invalid shape"):
                fetch("example/repository")

    def test_selects_latest_per_package_kind_with_publications_first(self) -> None:
        module = runpy.run_path(str(COLLECTOR))
        artifacts = [
            {
                "id": 1,
                "name": "package-ci-smoke-demo-100",
                "created_at": "2026-08-08T00:00:00Z",
                "expired": False,
            },
            {
                "id": 2,
                "name": "package-ci-smoke-demo-101",
                "created_at": "2026-08-08T01:00:00Z",
                "expired": False,
            },
            {
                "id": 3,
                "name": "rpm-repository-publish-demo-102",
                "created_at": "2026-08-08T02:00:00Z",
                "expired": False,
            },
            {
                "id": 4,
                "name": "rpm-repository-publish-other-package-103",
                "created_at": "2026-08-08T03:00:00Z",
                "expired": False,
            },
            {
                "id": 5,
                "name": "package-ci-smoke-expired-104",
                "created_at": "2026-08-08T04:00:00Z",
                "expired": True,
            },
            {
                "id": 6,
                "name": "package-ci-smoke-malformed",
                "created_at": "2026-08-08T05:00:00Z",
                "expired": False,
            },
        ]
        selected, eligible_count = module["select_artifacts"](artifacts)
        self.assertEqual(eligible_count, 4)
        self.assertEqual(
            [artifact["name"] for artifact in selected],
            [
                "rpm-repository-publish-other-package-103",
                "rpm-repository-publish-demo-102",
                "package-ci-smoke-demo-101",
            ],
        )

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
