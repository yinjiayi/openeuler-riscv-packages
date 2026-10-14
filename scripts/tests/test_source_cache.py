# SPDX-License-Identifier: Apache-2.0
"""Source cache regression tests: no target commands or upstream code executed."""
from __future__ import annotations

import copy
import hashlib
import pathlib
import runpy
import sys
import tempfile
import unittest
from unittest import mock

from helpers import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
from _lib import ToolError  # noqa: E402


class SourceCacheTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = pathlib.Path(self.temporary.name).resolve()
        self.work = self.root / "work" / "demo"
        self.sources = self.work / "SOURCES"
        self.sources.mkdir(parents=True)
        self.data = b"inert exact source fixture; never execute\n"
        self.entry = {"id": "source0", "filename": "demo.tar.gz", "url": "https://example.org/demo.tar.gz",
                      "digests": {"sha256": hashlib.sha256(self.data).hexdigest()}, "signature": None}
        self.source = self.sources / self.entry["filename"]
        self.source.write_bytes(self.data)
        self.module = runpy.run_path(str(SCRIPTS / "build-rpm"))
        self.globals = self.module["materialize_source"].__globals__
        self.fetch = mock.Mock(side_effect=AssertionError("cache-only must not fetch"))
        patch = mock.patch.dict(self.globals, {"fetch_url": self.fetch})
        patch.start()
        self.addCleanup(patch.stop)

    def materialize(self, entry=None, package="demo"):
        return self.module["materialize_source"](
            entry or self.entry, package_id=package, repo_root=self.root,
            sources_dir=self.sources, cache_dir=None, timeout=1, retries=0, offline=True,
        )

    def test_exact_bytes_rehashed_without_network_or_artifact_digest(self) -> None:
        result = self.materialize()
        self.assertTrue(result["verified"])
        self.assertEqual(result["sha256"], self.entry["digests"]["sha256"])
        self.assertTrue(result["materialization"]["cache_reverified"])
        self.fetch.assert_not_called()

    def test_missing_and_corrupt_cache_fail_without_fallback(self) -> None:
        self.source.unlink()
        with self.assertRaisesRegex(ToolError, "missing or unreadable"):
            self.materialize()
        self.source.write_bytes(b"corrupt")
        with self.assertRaisesRegex(ToolError, "checksum mismatch"):
            self.materialize()
        self.assertFalse(self.source.exists())
        self.fetch.assert_not_called()

    def test_cache_file_symlink_and_nonregular_entry_fail(self) -> None:
        other = self.root / "outside-source"
        other.write_bytes(self.data)
        self.source.unlink()
        self.source.symlink_to(other)
        with self.assertRaisesRegex(ToolError, "without symlinks"):
            self.materialize()
        self.source.unlink()
        self.source.mkdir()
        with self.assertRaisesRegex(ToolError, "regular file/directory"):
            self.materialize()
        self.fetch.assert_not_called()

    def test_cache_directory_symlink_and_workspace_ancestor_fail(self) -> None:
        self.source.unlink()
        self.sources.rmdir()
        external = self.root / "external"
        external.mkdir()
        (external / self.entry["filename"]).write_bytes(self.data)
        self.sources.symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(ToolError, "without symlinks"):
            self.materialize()
        with self.assertRaisesRegex(ToolError, "symlink"):
            self.module["prepare_dirs"](self.work)
        self.sources.unlink()
        self.work.rmdir()
        self.work.symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(ToolError, "symlink ancestors"):
            self.module["work_path"](self.work / "nested", self.root)

    def test_offline_still_enforces_https_aur_and_fixture_provenance(self) -> None:
        for url in ("http://example.org/demo.tar.gz", "https://aur.archlinux.org/demo.tar.gz", "fixture://tests/demo"):
            with self.subTest(url=url):
                entry = dict(self.entry, url=url)
                with self.assertRaises(ToolError):
                    self.materialize(entry)
        entry = dict(self.entry, url="fixture://tests/demo")
        self.assertTrue(self.materialize(entry, "golden-demo")["verified"])
        self.fetch.assert_not_called()

    def test_full_filename_and_sha_are_not_silently_normalized(self) -> None:
        for name in ("../demo.tar.gz", "/demo.tar.gz", "sub/demo.tar.gz", ".", "..", ""):
            with self.subTest(name=name), self.assertRaisesRegex(ToolError, "filename"):
                self.materialize(dict(self.entry, filename=name))
        entry = dict(self.entry, digests={"sha256": "not-a-digest"})
        with self.assertRaisesRegex(ToolError, "SHA-256"):
            self.materialize(entry)
        self.fetch.assert_not_called()

    def test_manifest_identity_shape_and_unique_names_fail_closed(self) -> None:
        entries = self.module["source_entries"]
        self.assertEqual(entries({"package_id": "demo", "sources": [self.entry]}, "demo"), [self.entry])
        invalid = [None, [], {"package_id": "other", "sources": [self.entry]},
                   {"package_id": "demo", "sources": []},
                   {"package_id": "demo", "sources": [None]},
                   {"package_id": "demo", "sources": [self.entry, dict(self.entry, id="source1")]},
                   {"package_id": "demo", "sources": [self.entry, dict(self.entry, filename="other.tar.gz")]},
                   {"package_id": "demo", "sources": [dict(self.entry, filename="../demo.tar.gz")]}]
        for document in invalid:
            with self.subTest(document=document), self.assertRaises(ToolError):
                entries(document, "demo")

    def test_required_signature_is_rechecked_on_cached_source(self) -> None:
        sig = self.root / "signature.asc"
        key = self.root / "keyring.gpg"
        sig.write_bytes(b"inert signature")
        key.write_bytes(b"inert key")
        fingerprint = "A" * 40
        entry = copy.deepcopy(self.entry)
        entry["signature"] = {"policy": "required", "path": sig.name, "keyring": key.name, "fingerprint": fingerprint}
        with mock.patch.dict(self.globals, {"shutil": mock.Mock(which=mock.Mock(return_value="gpgv"))}), mock.patch.object(
            self.globals["subprocess"], "run", return_value=mock.Mock(returncode=0, stdout="[GNUPG:] VALIDSIG " + fingerprint)
        ) as verify:
            self.assertEqual(self.materialize(entry)["signature"]["status"], "verified")
            self.assertEqual(verify.call_args.args[0], ["gpgv", "--keyring", str(key), "--status-fd", "1", str(sig), str(self.source)])
            verify.return_value = mock.Mock(returncode=1, stdout="bad signature")
            with self.assertRaisesRegex(ToolError, "signature verification failed"):
                self.materialize(entry)
        self.fetch.assert_not_called()

    def test_required_signature_missing_symlink_and_malformed_fail(self) -> None:
        entry = copy.deepcopy(self.entry)
        entry["signature"] = {"policy": "required", "path": "signature.asc", "keyring": "keyring.gpg", "fingerprint": "A" * 40}
        with self.assertRaisesRegex(ToolError, "missing or unreadable"):
            self.materialize(entry)
        (self.root / "real-signature").write_bytes(b"inert")
        (self.root / "signature.asc").symlink_to("real-signature")
        with self.assertRaisesRegex(ToolError, "without symlinks"):
            self.materialize(entry)
        (self.root / "linked-signatures").symlink_to(self.root, target_is_directory=True)
        entry["signature"]["path"] = "linked-signatures/real-signature"
        with self.assertRaisesRegex(ToolError, "without symlinks"):
            self.materialize(entry)
        entry["signature"]["path"] = "../outside-signature"
        with self.assertRaisesRegex(ToolError, "escapes"):
            self.materialize(entry)
        with self.assertRaisesRegex(ToolError, "object or null"):
            self.materialize(dict(self.entry, signature="required"))
        self.fetch.assert_not_called()
