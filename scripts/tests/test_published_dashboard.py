# SPDX-License-Identifier: Apache-2.0
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("collect_published_state", ROOT / "ci/collect-published-state.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Response(io.BytesIO):
    status = 200

    def __init__(self, payload, url, size=None):
        super().__init__(payload)
        self.url = url
        self.headers = {"Content-Length": str(len(payload) if size is None else size)}

    def geturl(self):
        return self.url


class PublishedDashboardTests(unittest.TestCase):
    def record(self, payload=b"inert fixture, never executed"):
        return {"url": MODULE.PUBLIC_ROOT + "/generations/bootstrap-20260808T000000Z/source/Packages/a-1-1.src.rpm",
                "filename": "a-1-1.src.rpm", "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest(), "arch": "src"}

    def test_full_payload_hash_and_size(self):
        payload = b"inert fixture, never executed"
        record = self.record(payload)
        with patch.object(MODULE.urllib.request, "build_opener") as opener:
            opener.return_value.open.return_value = Response(payload, record["url"])
            verified = MODULE.verify_file(record)
        self.assertEqual(verified["sha256"], record["sha256"])
        self.assertIn("verified_at", verified)

    def test_same_size_tampered_payload_rejected(self):
        record = self.record(b"abc")
        with patch.object(MODULE.urllib.request, "build_opener") as opener:
            opener.return_value.open.return_value = Response(b"xyz", record["url"])
            with self.assertRaisesRegex(ValueError, "checksum"):
                MODULE.verify_file(record)

    def test_size_mismatch_rejected(self):
        record = self.record(b"abc")
        with patch.object(MODULE.urllib.request, "build_opener") as opener:
            opener.return_value.open.return_value = Response(b"abcd", record["url"], size=3)
            with self.assertRaisesRegex(ValueError, "exceeds"):
                MODULE.verify_file(record)

    def test_redirect_rejected(self):
        record = self.record(b"abc")
        with patch.object(MODULE.urllib.request, "build_opener") as opener:
            opener.return_value.open.return_value = Response(b"abc", "http://example.org/a.rpm")
            with self.assertRaisesRegex(ValueError, "immutable URL"):
                MODULE.verify_file(record)

    def test_other_origin_rejected_before_network(self):
        record = self.record()
        record["url"] = "https://example.org/a.rpm"
        with patch.object(MODULE.urllib.request, "build_opener") as opener:
            with self.assertRaisesRegex(ValueError, "fixed endpoint"):
                MODULE.verify_file(record)
            opener.assert_not_called()

    def test_unsafe_relative_locations_rejected(self):
        for relative in ["../a.rpm", "/a.rpm", "Packages/../a.rpm", "https://example.org/a.rpm",
                         "Packages/a.rpm?x=1", "Packages/a.rpm#x", "Packages/nested/a.rpm", "Packages/a%2Frpm",
                         "Packages/a%2Fb.rpm", "Packages/a%2F..%2Fb.rpm", "Packages/a%252Fb.rpm"]:
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                MODULE.relative_url(MODULE.PUBLIC_ROOT + "/", relative, rpm=True)

    def test_rpm_name_association_is_exact_and_ambiguity_is_not_guessed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for package_id, name in [("which", "which"), ("debianutils", "debianutils"), ("alias-a", "duplicate"), ("alias-b", "duplicate")]:
                path = root / "packages" / package_id
                path.mkdir(parents=True)
                (path / "package.yaml").write_text(json.dumps({"package_id": package_id, "rpm": {"name": name}, "discovery": {"lineage": [{"package_name": "debianutils"}]}}))
            names, gaps = MODULE.canonical_names(root)
        self.assertEqual(names["which"], "which")
        self.assertEqual(names["debianutils"], "debianutils")
        self.assertNotIn("duplicate", names)
        self.assertEqual(len(gaps), 1)

    def test_schema_validates_definition(self):
        import jsonschema
        schema = json.loads((ROOT / "schemas/dashboard-published-state.schema.json").read_text())
        jsonschema.Draft202012Validator.check_schema(schema)

    def test_primary_metadata_has_no_custom_rpm_artifact_size_budget(self):
        # Metadata is tiny; no large file is allocated, downloaded or executed.
        size = 600 * 1024 * 1024
        raw = ('<metadata xmlns="http://linux.duke.edu/metadata/common" packages="1">'
               '<package><name>demo</name><arch>src</arch><version epoch="0" ver="1" rel="1"/>'
               '<checksum type="sha256">' + 'a' * 64 + '</checksum><size package="' + str(size) + '"/>'
               '<location href="Packages/demo-1-1.src.rpm"/></package></metadata>').encode()
        compressed = gzip.compress(raw)
        repomd = ('<repomd xmlns="http://linux.duke.edu/metadata/repo"><data type="primary">'
                  '<checksum type="sha256">' + MODULE.digest(compressed) + '</checksum>'
                  '<open-checksum type="sha256">' + MODULE.digest(raw) + '</open-checksum>'
                  '<size>' + str(len(compressed)) + '</size><open-size>' + str(len(raw)) + '</open-size>'
                  '<location href="repodata/primary.xml.gz"/></data></repomd>').encode()
        base = MODULE.PUBLIC_ROOT + '/generations/demo/source/'
        repository = {'baseurl': base, 'repomd_sha256': MODULE.digest(repomd), 'rpm_count': 1}
        responses = {base + 'repodata/repomd.xml': repomd, base + 'repodata/primary.xml.gz': compressed}
        with patch.object(MODULE.CLIENT, 'fetch', side_effect=lambda url, limit: responses[url]):
            rows, proof = MODULE.primary_entries(repository, 'source')
        self.assertEqual(rows[0]['size'], size)
        self.assertEqual(proof['package_count'], 1)

    def test_repository_template_is_not_a_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "packages" / "_template"
            path.mkdir(parents=True)
            (path / "package.yaml").write_text(json.dumps({"package_id": "replace-me", "rpm": {"name": "replace-me"}}))
            self.assertEqual(MODULE.canonical_names(root), ({}, []))

    def test_partial_snapshot_retains_verified_orphan_artifacts(self):
        state = {"generation": "demo-" + "a" * 40 + "-1-1", "published_at": "2026-10-09T00:00:00Z",
                 "repositories": {"source": {}, "riscv64": {}}}
        source = self.record(b"abc") | {"name": "demo", "epoch": "0", "version": "1", "release": "1"}
        binary = source | {"filename": "demo-1-1.riscv64.rpm", "url": source["url"].replace("/source/", "/riscv64/").replace("a-1-1.src.rpm", "demo-1-1.riscv64.rpm"),
                           "arch": "riscv64", "sourcerpm": source["filename"]}
        def entries(repository, category):
            return [source if category == "source" else binary], {"repomd_sha256": "a" * 64}
        def verify(record):
            if record["arch"] == "riscv64":
                raise ValueError("fixture checksum failure")
            return {key: record[key] for key in ("filename", "url", "sha256", "size", "arch")} | {"verified_at": "2026-10-09T00:01:00Z"}
        with patch.object(MODULE.CLIENT, "fetch", return_value=b"{}"), patch.object(MODULE.CLIENT, "validate_state", return_value=state), \
             patch.object(MODULE, "primary_entries", side_effect=entries), patch.object(MODULE, "canonical_names", return_value=({"demo": "demo"}, [])), \
             patch.object(MODULE, "verify_file", side_effect=verify), patch.object(MODULE.subprocess, "check_output", return_value="a" * 40):
            result = MODULE.collect(ROOT, 1)
        self.assertEqual(result["coverage"]["status"], "partial")
        self.assertEqual(result["coverage"]["verified_files"], 1)
        self.assertEqual(result["coverage"]["verified_bytes"], 3)
        self.assertEqual(result["coverage"]["verified_packages"], 0)
        self.assertEqual(result["packages"], [])
        self.assertEqual(len(result["verified_artifacts"]), 1)


if __name__ == "__main__":
    unittest.main()
