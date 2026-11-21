# SPDX-License-Identifier: Apache-2.0
"""Publication admission tests use synthetic bytes, never a local RPM build."""
from __future__ import annotations

import copy
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest import mock


REPO = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("publication_client", REPO / "ci/rpm-repo-client.py")
assert SPEC is not None and SPEC.loader is not None
client = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(client)


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class Response(io.BytesIO):
    status = 200

    def __init__(self, url: str, payload: bytes):
        super().__init__(payload)
        self.url = url
        self.headers = {"Content-Length": str(len(payload))}

    def geturl(self) -> str:
        return self.url


class PublicationVerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.generation = "canonical-hello-" + "a" * 40 + "-123-1"
        self.base = client.PUBLIC_ROOT + "/generations/" + self.generation + "/"
        self.state = {
            "schema_version": 1, "generation": self.generation,
            "published_at": "2026-11-06T00:00:00Z", "package_id": "canonical-hello",
            "commit_sha": "a" * 40, "run_id": 123, "run_attempt": 1,
            "repositories": {},
        }
        self.manifest = {key: value for key, value in self.state.items() if key not in {"published_at", "repositories"}}
        self.manifest.update(kind="rpm-repository-upload-batch", status="staged", artifacts=[])
        self.responses: dict[str, bytes] = {}
        self.package_xml: dict[str, str] = {}
        for repository, arch, kind in (("riscv64", "noarch", "binary"), ("source", "src", "source")):
            filename = "hello-1.0-1." + arch + ".rpm"
            # These are deliberately not real RPMs: this gate verifies byte
            # identity, not librpm headers, installation or signatures.
            payload = b"synthetic verified bytes:" + kind.encode()
            self.responses[self.base + repository + "/Packages/" + filename] = payload
            self.manifest["artifacts"].append({"filename": filename, "kind": kind, "sha256": sha(payload), "size": len(payload)})
            source = "hello-1.0-1.src.rpm" if kind == "binary" else ""
            self.package_xml[repository] = (
                '<package type="rpm"><name>hello</name><arch>' + arch + '</arch>'
                '<version epoch="0" ver="1.0" rel="1"/>'
                '<checksum type="sha256">' + sha(payload) + '</checksum>'
                '<size package="' + str(len(payload)) + '"/>'
                '<location href="Packages/' + filename + '"/>'
                '<format><rpm:sourcerpm>' + source + '</rpm:sourcerpm></format></package>'
            )
        self.refresh_metadata()
        self.manifest_path = self.root / "upload.json"
        self.write_manifest()
        self.args = SimpleNamespace(
            state_url=self.base + "state.json", expected_generation=self.generation,
            expected_package="canonical-hello", expected_commit="a" * 40,
            upload_manifest=str(self.manifest_path), output=str(self.root / "result.json"),
        )
        self.requests: list[str] = []
        opener = mock.Mock()
        opener.open.side_effect = self.open_response
        patch = mock.patch.object(client.urllib.request, "build_opener", return_value=opener)
        patch.start()
        self.addCleanup(patch.stop)

    def open_response(self, request, timeout):
        self.assertGreater(timeout, 0)
        self.assertLessEqual(timeout, 20)
        url = request.full_url
        self.requests.append(url)
        if url not in self.responses:
            raise client.urllib.error.HTTPError(url, 404, "missing", {}, None)
        return Response(url, self.responses[url])

    def write_manifest(self) -> None:
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def refresh_metadata(self) -> None:
        for repository in ("riscv64", "source"):
            count = 1 if self.package_xml[repository] else 0
            raw = (
                '<metadata xmlns="http://linux.duke.edu/metadata/common" '
                'xmlns:rpm="http://linux.duke.edu/metadata/rpm" packages="' + str(count) + '">'
                + self.package_xml[repository] + '</metadata>'
            ).encode()
            compressed = gzip.compress(raw, mtime=0)
            repomd = (
                '<repomd xmlns="http://linux.duke.edu/metadata/repo"><data type="primary">'
                '<checksum type="sha256">' + sha(compressed) + '</checksum>'
                '<open-checksum type="sha256">' + sha(raw) + '</open-checksum>'
                '<location href="repodata/primary.xml.gz"/><size>' + str(len(compressed)) + '</size>'
                '<open-size>' + str(len(raw)) + '</open-size></data></repomd>'
            ).encode()
            base = self.base + repository + "/"
            self.responses[base + "repodata/primary.xml.gz"] = compressed
            self.responses[base + "repodata/repomd.xml"] = repomd
            self.state["repositories"][repository] = {"baseurl": base, "repomd_sha256": sha(repomd), "rpm_count": count}
        self.responses[self.base + "state.json"] = json.dumps(self.state).encode()

    def assert_rejected(self, message: str) -> None:
        with self.assertRaisesRegex(ValueError, message):
            client.verify_generation(self.args)
        result = json.loads(Path(self.args.output).read_text())
        self.assertEqual(result["status"], "failed")
        self.assertNotIn("verified_artifacts", result)

    def test_real_bytes_and_binary_source_closure_are_verified(self) -> None:
        self.assertEqual(client.verify_generation(self.args), 0)
        result = json.loads(Path(self.args.output).read_text())
        self.assertEqual(result["status"], "passed")
        self.assertEqual({item["kind"] for item in result["verified_artifacts"]}, {"source", "binary"})
        self.assertEqual(result["upload_manifest_sha256"], sha(self.manifest_path.read_bytes()))
        self.assertTrue(all(item["url"] in self.requests for item in result["verified_artifacts"]))
        self.assertIn("not independently queried", result["identity_source"])
        self.assertIn("not established", result["trust"]["authentication"])
        # Canonical directory identity need not equal RPM NAME.
        self.assertEqual(result["verified_artifacts"][0]["identity"]["name"], "hello")
        self.assertEqual(result["package_id"], "canonical-hello")

    def test_default_upload_path_matches_existing_workflow(self) -> None:
        workflow = (REPO / ".github/workflows/package-ci.yml").read_text()
        self.assertIn("artifacts/repository-publish/upload.json", workflow)
        self.assertIn("ci/rpm-repo-client.py verify-generation", workflow)
        argv = ["rpm-repo-client.py", "verify-generation", "--state-url", self.args.state_url,
                "--expected-generation", self.generation, "--expected-package", "canonical-hello",
                "--expected-commit", "a" * 40, "--output", self.args.output]
        with mock.patch.object(sys, "argv", argv), mock.patch.object(client, "verify_generation", return_value=0) as verify:
            self.assertEqual(client.main(), 0)
        self.assertEqual(verify.call_args.args[0].upload_manifest, "artifacts/repository-publish/upload.json")

    def test_metadata_success_cannot_hide_rpm_404(self) -> None:
        del self.responses[self.base + "riscv64/Packages/hello-1.0-1.noarch.rpm"]
        self.assert_rejected("RPM returned HTTP 404")

    def test_same_size_changed_rpm_bytes_fail(self) -> None:
        url = self.base + "riscv64/Packages/hello-1.0-1.noarch.rpm"
        self.responses[url] = b"x" * len(self.responses[url])
        self.assert_rejected("physical RPM SHA-256 mismatch")

    def test_failed_retry_replaces_prior_passed_receipt(self) -> None:
        self.assertEqual(client.verify_generation(self.args), 0)
        del self.responses[self.base + "source/Packages/hello-1.0-1.src.rpm"]
        self.assert_rejected("RPM returned HTTP 404")

    def test_verification_cannot_overwrite_its_upload_manifest(self) -> None:
        original = self.manifest_path.read_bytes()
        self.args.output = str(self.manifest_path)
        with self.assertRaisesRegex(ValueError, "must not overwrite"):
            client.verify_generation(self.args)
        self.assertEqual(self.manifest_path.read_bytes(), original)

    def test_missing_srpm_is_not_accepted(self) -> None:
        self.package_xml["source"] = ""
        self.refresh_metadata()
        self.assert_rejected("source RPM is missing")
        self.assertFalse(any("/Packages/" in url for url in self.requests))

    def test_srpm_http_404_is_not_hidden_by_valid_metadata(self) -> None:
        del self.responses[self.base + "source/Packages/hello-1.0-1.src.rpm"]
        self.assert_rejected("RPM returned HTTP 404")

    def test_manifest_without_source_is_not_accepted(self) -> None:
        self.manifest["artifacts"] = self.manifest["artifacts"][:1]
        self.write_manifest()
        self.assert_rejected("binary and source RPM batch")

    def test_large_valid_declared_sizes_are_not_an_artifact_budget(self) -> None:
        for artifact in self.manifest["artifacts"]:
            artifact["size"] = 32 * 1024 * 1024 * 1024
        self.write_manifest()
        manifest, _ = client.load_upload_manifest(self.manifest_path, self.state)
        self.assertEqual(manifest["artifacts"], self.manifest["artifacts"])
        self.assertEqual(self.requests, [])  # No giant file is downloaded.

    def test_subpackage_count_has_no_custom_artifact_quota(self) -> None:
        template = self.manifest["artifacts"][0]
        self.manifest["artifacts"].extend(
            {**template, "filename": f"hello-sub-{index}-1.0-1.noarch.rpm"} for index in range(600)
        )
        self.write_manifest()
        manifest, _ = client.load_upload_manifest(self.manifest_path, self.state)
        self.assertEqual(len(manifest["artifacts"]), 602)
        self.assertEqual(self.requests, [])

    def test_upload_manifest_is_required_and_run_bound(self) -> None:
        self.assertEqual(client.verify_generation(self.args), 0)
        self.manifest_path.unlink()
        self.assert_rejected("manifest is missing")
        self.manifest["run_attempt"] = 2
        self.write_manifest()
        self.assert_rejected("run_attempt does not match")

    def test_unreadable_manifest_cannot_leave_prior_success(self) -> None:
        self.assertEqual(client.verify_generation(self.args), 0)
        original_open = Path.open
        manifest_path = self.manifest_path
        def open_with_denied_manifest(path, *args, **kwargs):
            if path == manifest_path:
                raise PermissionError("fixture manifest unreadable")
            return original_open(path, *args, **kwargs)
        with mock.patch.object(Path, "open", open_with_denied_manifest):
            self.assert_rejected("manifest is missing or invalid")

    def test_decompressor_io_and_deflate_errors_replace_prior_success(self) -> None:
        for error in (OSError("fixture decompressor unavailable"), client.zlib.error("fixture corrupt deflate")):
            self.assertEqual(client.verify_generation(self.args), 0)
            with mock.patch.object(client, "load_primary", side_effect=error):
                self.assert_rejected("fixture")

    def test_invalid_manifest_kind_replaces_prior_success(self) -> None:
        for value in ([], {}, None, 1):
            self.manifest["artifacts"][0]["kind"] = "binary"
            self.write_manifest()
            self.assertEqual(client.verify_generation(self.args), 0)
            self.manifest["artifacts"][0]["kind"] = value
            self.write_manifest()
            self.assert_rejected("artifact kind is invalid")

    def test_http_protocol_error_replaces_prior_success(self) -> None:
        self.assertEqual(client.verify_generation(self.args), 0)
        with mock.patch.object(client, "fetch_rpm_digest", side_effect=client.http.client.IncompleteRead(b"partial", 10)):
            self.assert_rejected("IncompleteRead")

    def test_primary_tampering_is_rejected_before_rpm_download(self) -> None:
        self.responses[self.base + "riscv64/repodata/primary.xml.gz"] = b"tampered"
        self.assert_rejected("primary metadata size or SHA-256 mismatch")

    def test_primary_and_upload_must_agree_on_every_artifact_digest(self) -> None:
        self.manifest["artifacts"][0]["sha256"] = "f" * 64
        self.write_manifest()
        self.assert_rejected("primary RPM differs from exact upload manifest")
        self.assertFalse(any("/Packages/" in url for url in self.requests))

    def test_primary_count_cannot_omit_generation_packages(self) -> None:
        self.state["repositories"]["source"]["rpm_count"] = 2
        self.responses[self.base + "state.json"] = json.dumps(self.state).encode()
        self.assert_rejected("primary package count does not match")

    def test_primary_filename_identity_and_source_reference_are_checked(self) -> None:
        original = self.package_xml["riscv64"]
        self.package_xml["riscv64"] = original.replace("<name>hello</name>", "<name>wrong</name>")
        self.refresh_metadata()
        self.assert_rejected("filename does not match")
        self.package_xml["riscv64"] = original.replace("<rpm:sourcerpm>hello", "<rpm:sourcerpm>wrong")
        self.refresh_metadata()
        self.assert_rejected("does not reference an uploaded source RPM")

    def test_manifest_filename_traversal_and_duplicates_fail(self) -> None:
        original = copy.deepcopy(self.manifest)
        for filename in ("../hello.rpm", "/tmp/hello.rpm", "hello\\bad.rpm"):
            self.manifest = copy.deepcopy(original)
            self.manifest["artifacts"][0]["filename"] = filename
            self.write_manifest()
            self.assert_rejected("filename is unsafe")
        self.manifest = copy.deepcopy(original)
        self.manifest["artifacts"].append(copy.deepcopy(self.manifest["artifacts"][0]))
        self.write_manifest()
        self.assert_rejected("filename is unsafe or duplicated")

    def test_primary_traversal_or_absolute_location_is_never_fetched(self) -> None:
        for location in ("../primary.xml.gz", "http://elsewhere/primary.xml.gz", "repodata/%2e%2e/primary.xml.gz"):
            self.refresh_metadata()
            url = self.base + "riscv64/repodata/repomd.xml"
            self.responses[url] = self.responses[url].replace(b"repodata/primary.xml.gz", location.encode())
            self.state["repositories"]["riscv64"]["repomd_sha256"] = sha(self.responses[url])
            self.responses[self.base + "state.json"] = json.dumps(self.state).encode()
            self.assert_rejected("primary location is unsafe")

    def test_xml_entities_and_decompression_bomb_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "DTD or entity"):
            client.xml_root(b'<!DOCTYPE x [<!ENTITY y "z">]><x/>', "x")
        with mock.patch.object(client, "MAX_PRIMARY_OPEN_BYTES", 32):
            self.assert_rejected("expanded primary metadata exceeds")

    def test_current_repository_zstd_primary_format(self) -> None:
        executable = client.shutil.which("zstd")
        self.assertIsNotNone(executable, "the repository's existing zstd dependency is required")
        for repository in ("riscv64", "source"):
            base = self.base + repository + "/"
            old = self.responses[base + "repodata/primary.xml.gz"]
            raw = gzip.decompress(old)
            compressed = subprocess.run([executable, "-q", "-c"], input=raw, capture_output=True, check=True, timeout=20).stdout
            self.responses[base + "repodata/primary.xml.zst"] = compressed
            repomd = self.responses[base + "repodata/repomd.xml"]
            repomd = repomd.replace(b"primary.xml.gz", b"primary.xml.zst").replace(sha(old).encode(), sha(compressed).encode())
            repomd = repomd.replace(f"<size>{len(old)}</size>".encode(), f"<size>{len(compressed)}</size>".encode())
            self.responses[base + "repodata/repomd.xml"] = repomd
            self.state["repositories"][repository]["repomd_sha256"] = sha(repomd)
        self.responses[self.base + "state.json"] = json.dumps(self.state).encode()
        self.assertEqual(client.verify_generation(self.args), 0)

    def test_zstd_missing_invalid_and_expanded_limits(self) -> None:
        with mock.patch.object(client.shutil, "which", return_value=None):
            with self.assertRaisesRegex(ValueError, "zstd is required"):
                client.decompress_zstd(b"anything")
        with self.assertRaisesRegex(ValueError, "invalid zstd"):
            client.decompress_zstd(b"not a zstd frame")
        compressed = subprocess.run([client.shutil.which("zstd"), "-q", "-c"], input=b"a" * 1024, capture_output=True, check=True, timeout=20).stdout
        with mock.patch.object(client, "MAX_PRIMARY_OPEN_BYTES", 32):
            with self.assertRaisesRegex(ValueError, "expanded primary metadata exceeds"):
                client.decompress_zstd(compressed)

    def test_download_size_and_time_limits_are_enforced(self) -> None:
        url = self.base + "riscv64/Packages/hello-1.0-1.noarch.rpm"
        size = len(self.responses[url])
        with self.assertRaisesRegex(ValueError, "Content-Length"):
            client.fetch_rpm_digest(url, size - 1, time.monotonic() + 10)
        with self.assertRaisesRegex(ValueError, "time limit"):
            client.fetch_rpm_digest(url, size, time.monotonic() - 1)

    def test_download_url_cannot_escape_immutable_package_directory(self) -> None:
        for suffix in ("../state.json", "%2e%2e%2fhello.rpm", "hello.rpm?query=1", "hello.rpm#fragment"):
            with self.assertRaises(ValueError):
                client.fetch_rpm_digest(self.base + "riscv64/Packages/" + suffix, 1, time.monotonic() + 10)
        self.assertEqual(self.requests, [])

    def test_download_without_content_length_still_enforces_size(self) -> None:
        url = self.base + "riscv64/Packages/hello-1.0-1.noarch.rpm"
        for payload, size, message in ((b"123", 2, "exceed"), (b"1", 2, "byte count")):
            response = Response(url, payload)
            response.headers = {}
            opener = mock.Mock()
            opener.open.return_value = response
            with mock.patch.object(client.urllib.request, "build_opener", return_value=opener):
                with self.assertRaisesRegex(ValueError, message):
                    client.fetch_rpm_digest(url, size, time.monotonic() + 10)

    def test_download_rejects_redirected_response(self) -> None:
        url = self.base + "riscv64/Packages/hello-1.0-1.noarch.rpm"
        opener = mock.Mock()
        opener.open.return_value = Response("http://elsewhere/package.rpm", b"x")
        with mock.patch.object(client.urllib.request, "build_opener", return_value=opener):
            with self.assertRaisesRegex(ValueError, "redirected"):
                client.fetch_rpm_digest(url, 1, time.monotonic() + 10)


if __name__ == "__main__":
    unittest.main()
