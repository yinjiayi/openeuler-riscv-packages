# SPDX-License-Identifier: Apache-2.0
"""Inert signature-contract tests; subprocess/GPG and network are mocked."""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import runpy
import sys
import tempfile
import unittest
from unittest import mock

from helpers import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
from _lib import ToolError  # noqa: E402


class SignaturePolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = pathlib.Path(temporary.name).resolve()
        self.sources = self.root / "SOURCES"
        self.sources.mkdir()
        self.data = b"inert source bytes, never executed\n"
        self.source = self.sources / "demo.tar.gz"
        self.source.write_bytes(self.data)
        self.fingerprint = "A" * 40
        self.signature = {"url": "https://example.org/demo.tar.gz.asc", "policy": "required",
                          "path": "packages/demo/signature.asc", "keyring": "packages/demo/keyring.gpg",
                          "key_fingerprint": self.fingerprint}
        for key in ("path", "keyring"):
            path = self.root / self.signature[key]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"inert fixture; not a signature or key")
        self.entry = {"id": "source0", "kind": "upstream-release", "filename": self.source.name,
                      "url": "https://example.org/demo.tar.gz", "version": "1.0",
                      "digests": {"sha256": hashlib.sha256(self.data).hexdigest()},
                      "signature": self.signature, "redistribution": {"allowed": True, "reason": "test"}}
        self.module = runpy.run_path(str(SCRIPTS / "build-rpm"))
        self.globals = self.module["materialize_source"].__globals__
        self.fetch = mock.Mock(side_effect=AssertionError("signature/cache must not fetch"))
        patch = mock.patch.dict(self.globals, {"fetch_url": self.fetch})
        patch.start()
        self.addCleanup(patch.stop)
        self.schema = json.loads((SCRIPTS.parent / "schemas/sources.schema.json").read_text())
        self.schema_errors = runpy.run_path(str(SCRIPTS / "validate-metadata"))["schema_errors"]

    def document(self, entry=None):
        return {"schema_version": 1, "package_id": "demo", "sources": [entry or self.entry]}

    def errors(self, entry=None):
        return self.schema_errors(self.document(entry), self.schema, self.schema)

    def status(self, signer=None, primary=None):
        return "[GNUPG:] VALIDSIG %s 2026-10-20 1792497600 0 4 0 1 10 00%s\n" % (
            signer or self.fingerprint, " " + primary if primary else "")

    def materialize(self, entry=None):
        return self.module["materialize_source"](
            entry or self.entry, package_id="demo", repo_root=self.root, sources_dir=self.sources,
            cache_dir=None, timeout=1, retries=0, offline=True)

    def verifier(self, stdout=None, stderr="", returncode=0):
        return mock.patch.object(self.globals["subprocess"], "run", return_value=mock.Mock(
            returncode=returncode, stdout=self.status() if stdout is None else stdout, stderr=stderr))

    def test_null_and_existing_advisory_metadata_remain_compatible(self):
        for signature in (None, {"policy": "checksum-required-signature-advisory",
                                "url": "https://example.org/source.asc", "key_fingerprint": "ABCD " * 8}):
            entry = dict(self.entry, signature=signature)
            self.assertEqual(self.errors(entry), [])
            with self.verifier() as gpg:
                self.assertNotEqual(self.materialize(entry)["signature"]["status"], "verified")
                gpg.assert_not_called()
        self.fetch.assert_not_called()

    def test_generator_schema_and_cached_runtime_share_required_contract(self):
        creator = runpy.run_path(str(SCRIPTS / "create-package"))
        candidate = {"canonical_name": "demo", "latest_observed_version": "1.0", "license": "MIT",
                     "upstream": {"homepage": "https://example.org/demo"}, "source": {
                         "url": self.entry["url"], "sha256": self.entry["digests"]["sha256"],
                         "signature": self.signature}}
        files = creator["build_files"](candidate, "demo", False)
        generated = json.loads(files["sources.yaml"][0])
        self.assertEqual(self.schema_errors(generated, self.schema, self.schema), [])
        self.assertEqual(generated["sources"][0]["signature"], self.signature)
        with self.verifier(), mock.patch.dict(self.globals, {"shutil": mock.Mock(which=lambda _: "gpgv")}):
            self.assertEqual(self.materialize(generated["sources"][0])["signature"]["status"], "verified")
            self.assertEqual(self.materialize(generated["sources"][0])["signature"]["status"], "verified")
        self.fetch.assert_not_called()

    def test_required_schema_rejects_missing_unknown_and_legacy_alias_fields(self):
        for field in ("path", "keyring", "key_fingerprint", "url", "policy"):
            entry = copy.deepcopy(self.entry)
            del entry["signature"][field]
            self.assertTrue(self.errors(entry), field)
        for field in ("fingerprint", "unexpected"):
            entry = copy.deepcopy(self.entry)
            entry["signature"][field] = self.fingerprint
            self.assertTrue(self.errors(entry), field)

    def test_required_fingerprint_is_canonical_full_40_or_64_hex(self):
        for fingerprint in ("A" * 40, "B" * 64):
            entry = copy.deepcopy(self.entry)
            entry["signature"]["key_fingerprint"] = fingerprint
            self.assertEqual(self.errors(entry), [])
        for fingerprint in ("A" * 16, "A" * 39, "A" * 41, "A" * 63, "A" * 65,
                            "a" * 40, " A" * 40, "G" * 40, "A" * 40 + "\n"):
            entry = copy.deepcopy(self.entry)
            entry["signature"]["key_fingerprint"] = fingerprint
            self.assertTrue(self.errors(entry), repr(fingerprint))
            with self.assertRaisesRegex(ToolError, "canonical 40- or 64-hex"):
                self.materialize(entry)

    def test_required_paths_fail_schema_and_runtime_before_gpg(self):
        for field in ("path", "keyring"):
            for path in ("", ".", "..", "../key", "keys/../key", "keys/./key", "/key", "keys//key",
                         "keys/", "keys\\key", "key\n", 123):
                entry = copy.deepcopy(self.entry)
                entry["signature"][field] = path
                self.assertTrue(self.errors(entry), repr(path))
                with self.verifier() as gpg, self.assertRaises(ToolError):
                    self.materialize(entry)
                gpg.assert_not_called()

    def test_keyring_linked_ancestor_nonregular_and_missing_rejected(self):
        keyring = self.root / self.signature["keyring"]
        keyring.unlink()
        with self.assertRaisesRegex(ToolError, "missing or unreadable"):
            self.materialize()
        keyring.mkdir()
        with self.assertRaisesRegex(ToolError, "without symlinks"):
            self.materialize()
        keyring.rmdir()
        keyring.symlink_to(self.source)
        with self.assertRaisesRegex(ToolError, "without symlinks"):
            self.materialize()
        entry = copy.deepcopy(self.entry)
        (self.root / "linked").symlink_to(keyring.parent, target_is_directory=True)
        entry["signature"]["keyring"] = "linked/keyring.gpg"
        with self.assertRaisesRegex(ToolError, "without symlinks"):
            self.materialize(entry)

    def test_gpg_uses_private_home_explicit_keyring_and_separate_status(self):
        observed = []
        def run(argv, **kwargs):
            home = pathlib.Path(argv[2])
            observed.append(home)
            self.assertEqual(argv[:2], ["gpgv", "--homedir"])
            self.assertTrue(home.is_dir())
            self.assertEqual(home.stat().st_mode & 0o777, 0o700)
            self.assertEqual(list(home.iterdir()), [])
            self.assertEqual(argv[3:], ["--keyring", str(self.root / self.signature["keyring"]),
                                      "--status-fd", "1", str(self.root / self.signature["path"]), str(self.source)])
            self.assertEqual(kwargs["stdout"], self.globals["subprocess"].PIPE)
            self.assertEqual(kwargs["stderr"], self.globals["subprocess"].PIPE)
            return mock.Mock(returncode=0, stdout=self.status(), stderr="ordinary diagnostics")
        with mock.patch.dict(self.globals, {"shutil": mock.Mock(which=lambda _: "gpgv")}), mock.patch.object(
                self.globals["subprocess"], "run", side_effect=run):
            self.assertEqual(self.materialize()["signature"]["status"], "verified")
        self.assertEqual(len(observed), 1)
        self.assertFalse(observed[0].exists())

    def test_exact_status_accepts_complete_signer_but_not_primary_fallback(self):
        parse = self.module["exact_signature_status"]
        self.assertTrue(parse(self.status(), self.fingerprint))
        self.assertTrue(parse(self.status(primary="B" * 40), self.fingerprint))
        self.assertTrue(parse(self.status("C" * 64), "C" * 64))
        self.assertFalse(parse(self.status("B" * 40, self.fingerprint), self.fingerprint))

    def test_forged_prefixed_truncated_and_malformed_status_rejected(self):
        parse = self.module["exact_signature_status"]
        for status in ("diagnostic " + self.status(), "VALIDSIG " + self.fingerprint,
                       self.status(self.fingerprint + "B"), self.status() + self.status(),
                       self.status().replace("2026-10-20", "not-date"),
                       self.status().replace("1792497600", "not-time"),
                       self.status().replace(" 00\n", " 000\n"),
                       self.status().replace(" 4 0 1 10 00", ""),
                       self.status()[:-1] + " arbitrary-suffix\n"):
            self.assertFalse(parse(status, self.fingerprint), repr(status))

    def test_diagnostic_validsig_and_nonzero_exit_cannot_verify(self):
        with mock.patch.dict(self.globals, {"shutil": mock.Mock(which=lambda _: "gpgv")}):
            for stdout, stderr, code in (("", self.status(), 0), (self.status(), "", 1),
                                         (self.status("B" * 40), self.status(), 0)):
                with self.verifier(stdout, stderr, code), self.assertRaisesRegex(ToolError, "verification failed"):
                    self.materialize()

    def test_no_gpg_and_bad_checksum_cannot_use_signature_or_network_fallback(self):
        with mock.patch.dict(self.globals, {"shutil": mock.Mock(which=lambda _: None)}):
            with self.assertRaisesRegex(ToolError, "gpgv is required"):
                self.materialize()
        self.source.write_bytes(b"wrong bytes")
        with self.verifier() as gpg, self.assertRaisesRegex(ToolError, "checksum mismatch"):
            self.materialize()
        gpg.assert_not_called()
        self.fetch.assert_not_called()
