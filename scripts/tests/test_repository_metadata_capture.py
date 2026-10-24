# SPDX-License-Identifier: Apache-2.0
"""Offline fixtures only: no endpoint, package source, RPM, or target execution."""
from __future__ import annotations

import bz2
import copy
import gzip
import hashlib
import importlib.util
import json
import lzma
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock
import zlib

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("metadata_capture", ROOT / "ci/capture-repository-metadata.py")
capture = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(capture)
client = capture.CLIENT
P = capture.COMMON_NS
F = capture.FILES_NS
R = capture.REPO_NS
GENERATION = "fixture-" + "a" * 40 + "-123-2"
PKGID = "b" * 64


def primary(arch: str = "riscv64", packages: str | None = None, count: int = 1) -> bytes:
    package = f'''<package type="rpm"><name>fixture</name><arch>{arch}</arch>
      <version epoch="0" ver="1.0" rel="1"/><checksum type="sha256" pkgid="YES">{PKGID}</checksum>
      <size package="100" installed="200" archive="200"/><location href="Packages/fixture-1.0-1.{arch}.rpm"/>
      <format xmlns:rpm="http://linux.duke.edu/metadata/rpm"><rpm:sourcerpm>fixture-1.0-1.src.rpm</rpm:sourcerpm></format></package>'''
    return f'<metadata xmlns="{P}" packages="{count}">{package if packages is None else packages}</metadata>'.encode()


def filelists(arch: str = "riscv64", packages: str | None = None, count: int = 1) -> bytes:
    paths = ('<file>fixture-1.0.tar.gz</file><file>fixture.spec</file>' if arch in {"src", "nosrc"} else
             '<file>/usr/bin/fixture</file><file type="dir">/usr/share/fixture</file>')
    package = f'''<package pkgid="{PKGID}" name="fixture" arch="{arch}">
      <version epoch="0" ver="1.0" rel="1"/>{paths}</package>'''
    return f'<filelists xmlns="{F}" packages="{count}">{package if packages is None else packages}</filelists>'.encode()


class MetadataCaptureTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.transport = {}
        self.state = {"schema_version": 1, "generation": GENERATION, "published_at": "2026-10-24T00:00:00Z",
                      "package_id": "fixture", "commit_sha": "a" * 40, "run_id": 123, "run_attempt": 2,
                      "repositories": {}}
        for category, arch in (("riscv64", "riscv64"), ("source", "src")):
            base = client.PUBLIC_ROOT + "/generations/" + GENERATION + "/" + category + "/"
            entries = []
            for kind, raw in (("primary", primary(arch)), ("filelists", filelists(arch))):
                compressed = gzip.compress(raw, mtime=0)
                href = f"repodata/{kind}.xml.gz"
                self.transport[base + href] = compressed
                entries.append(f'''<data type="{kind}"><checksum type="sha256">{capture.sha(compressed)}</checksum>
                  <open-checksum type="sha256">{capture.sha(raw)}</open-checksum><location href="{href}"/>
                  <size>{len(compressed)}</size><open-size>{len(raw)}</open-size></data>''')
            repomd = f'<repomd xmlns="{R}">{"".join(entries)}</repomd>'.encode()
            self.transport[base + "repodata/repomd.xml"] = repomd
            self.state["repositories"][category] = {"baseurl": base, "repomd_sha256": capture.sha(repomd), "rpm_count": 1}
        self.state_url = client.PUBLIC_ROOT + "/generations/" + GENERATION + "/state.json"
        self.transport[self.state_url] = json.dumps(self.state).encode()
        self.resolution = {"schema_version": 1, "kind": "supplemental-repository-resolution", "status": "passed",
                           "resolved_at": "2026-10-24T00:00:00Z", "state_url": client.STATE_URL,
                           "state_sha256": capture.sha(self.transport[self.state_url]), "generation": GENERATION,
                           "repositories": copy.deepcopy(self.state["repositories"]),
                           "verified_repomd_sha256": {k: v["repomd_sha256"] for k, v in self.state["repositories"].items()},
                           "trust": {"transport": "operator-provided HTTP endpoint", "rpm_gpgcheck": False,
                                     "controls": ["fixed endpoint", "no redirects", "immutable generation URL", "state-bound repomd SHA-256"]}}
        self.overlay = {"schema_version": 1, "kind": "protected-main-package-overlay", "status": "passed",
                        "package_id": "fixture", "package_commit_sha": "c" * 40, "package_tree_sha": "d" * 40,
                        "tooling_commit_sha": "e" * 40}
        self.args = SimpleNamespace(resolution=self.root / "resolution.json", repo_file=self.root / "project.repo",
                                    overlay=self.root / "overlay.json", output_dir=self.root / "metadata", package_id="fixture",
                                    package_commit="c" * 40, tooling_commit="e" * 40, run_id="500", run_attempt="3")
        self.repo = "\n".join(["[openeuler-riscv-project]", "name=openEuler RISC-V project packages (immutable generation)",
                               "baseurl=" + self.state["repositories"]["riscv64"]["baseurl"], "enabled=1", "gpgcheck=0",
                               "repo_gpgcheck=0", "metadata_expire=never", "skip_if_unavailable=0", "module_hotfixes=1", ""])

    def write_inputs(self):
        self.args.resolution.write_text(json.dumps(self.resolution))
        self.args.overlay.write_text(json.dumps(self.overlay))
        self.args.repo_file.write_text(self.repo)

    def fetch(self, url, maximum):
        self.assertNotEqual(url, client.STATE_URL, "capture must never re-resolve mutable global state")
        self.assertIn(url, self.transport)
        raw = self.transport[url]
        self.assertLessEqual(len(raw), maximum)
        return raw

    def run_capture(self):
        self.write_inputs()
        with mock.patch.object(client, "fetch", side_effect=self.fetch):
            return capture.capture(self.args)

    def rejected(self):
        with self.assertRaises((ValueError, client.RepositoryUnavailable)):
            self.run_capture()
        self.assertFalse((self.args.output_dir / "receipt.json").exists())

    def rebind_repomd(self, category, changed):
        repository = self.state["repositories"][category]
        url = repository["baseurl"] + "repodata/repomd.xml"
        self.transport[url] = changed(self.transport[url])
        repository["repomd_sha256"] = capture.sha(self.transport[url])
        self.transport[self.state_url] = json.dumps(self.state).encode()
        self.resolution["state_sha256"] = capture.sha(self.transport[self.state_url])
        self.resolution["repositories"] = copy.deepcopy(self.state["repositories"])
        self.resolution["verified_repomd_sha256"] = {k: v["repomd_sha256"] for k, v in self.state["repositories"].items()}

    def test_complete_raw_bytes_full_join_and_exact_attempt_context(self):
        result = self.run_capture()
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["context"]["run_id"], 500)
        self.assertEqual(result["context"]["run_attempt"], 3)
        self.assertEqual(result["context"]["package_commit_sha"], "c" * 40)
        self.assertEqual(result["context"]["tooling_commit_sha"], "e" * 40)
        self.assertEqual(result["repositories"]["riscv64"]["package_count"], 1)
        self.assertEqual(result["repositories"]["source"]["file_count"], 2)
        metadata = [name for name in result["files"] if name.startswith(("riscv64-", "source-"))]
        self.assertEqual(len(metadata), 10)
        for name, row in result["files"].items():
            raw = (self.args.output_dir / name).read_bytes()
            self.assertEqual(capture.sha(raw), row["sha256"])
            self.assertEqual(len(raw), row["bytes"])
        self.assertEqual((self.args.output_dir / "state.json").read_bytes(), self.transport[self.state_url])
        self.assertIn("no RPM payload", result["claim_boundary"])

    def test_disabled_official_only_is_not_applicable_and_never_fetches(self):
        self.write_inputs()
        client.write_unavailable_resolution(SimpleNamespace(repo_file=self.args.repo_file, output=self.args.resolution,
                                                           state_url=client.STATE_URL))
        with mock.patch.object(client, "fetch", side_effect=AssertionError("disabled must not fetch")):
            result = capture.capture(self.args)
        self.assertEqual(result["status"], "not-applicable")
        self.assertIsNone(result["generation"])
        self.assertEqual(result["repositories"], {})
        self.assertNotIn("state.json", result["files"])

    def test_disabled_tampered_repo_or_fallback_is_rejected(self):
        for case in ("enabled", "fallback"):
            with self.subTest(case=case):
                self.write_inputs()
                client.write_unavailable_resolution(SimpleNamespace(repo_file=self.args.repo_file, output=self.args.resolution,
                                                                   state_url=client.STATE_URL))
                if case == "enabled":
                    self.args.repo_file.write_text(self.args.repo_file.read_text().replace("enabled=0", "enabled=1"))
                else:
                    value = json.loads(self.args.resolution.read_text())
                    value["fallback"]["supplemental_repository_enabled"] = True
                    self.args.resolution.write_text(json.dumps(value))
                with mock.patch.object(client, "fetch", side_effect=AssertionError("must not fetch")):
                    with self.assertRaises(ValueError):
                        capture.capture(self.args)

    def test_stale_output_directory_not_reused(self):
        self.args.output_dir.mkdir()
        self.rejected()

    def test_overlay_tooling_and_package_must_match_context(self):
        self.overlay["tooling_commit_sha"] = "f" * 40
        self.rejected()

    def test_state_byte_checksum_not_semantic_json_equality(self):
        self.transport[self.state_url] += b"\n"
        self.rejected()

    def test_state_repository_mapping_cannot_change_after_resolve(self):
        self.resolution["repositories"]["riscv64"]["rpm_count"] = 2
        self.rejected()

    def test_repomd_tamper_rejected(self):
        url = self.state["repositories"]["riscv64"]["baseurl"] + "repodata/repomd.xml"
        self.transport[url] += b"\n"
        self.rejected()

    def test_compressed_checksum_tamper_rejected(self):
        url = self.state["repositories"]["riscv64"]["baseurl"] + "repodata/primary.xml.gz"
        self.transport[url] = b"x" * len(self.transport[url])
        self.rejected()

    def test_open_checksum_tamper_rejected(self):
        self.rebind_repomd("source", lambda raw: raw.replace(capture.sha(primary("src")).encode(), b"0" * 64))
        self.rejected()

    def test_missing_or_duplicate_required_type_rejected(self):
        self.rebind_repomd("riscv64", lambda raw: raw.replace(b'type="filelists"', b'type="primary"'))
        self.rejected()

    def test_endpoint_failure_during_enabled_capture_is_not_fallback(self):
        self.write_inputs()
        with mock.patch.object(client, "fetch", side_effect=client.RepositoryUnavailable("offline")):
            with self.assertRaises(client.RepositoryUnavailable):
                capture.capture(self.args)
        self.assertFalse((self.args.output_dir / "receipt.json").exists())
        self.assertEqual(json.loads(self.args.resolution.read_text())["status"], "passed")

    def test_metadata_locations_reject_redirect_target_traversal_encoding_and_queries(self):
        for href in ("https://example.test/x.gz", "//example.test/x.gz", "repodata/../x.gz", "repodata/%2e.gz",
                     "repodata/x.gz?x=1", "repodata/x.gz#x", "repodata/dir/x.gz", "repodata/\\x.gz"):
            with self.subTest(href=href), self.assertRaises(ValueError):
                capture.metadata_url(client.PUBLIC_ROOT + "/", href)

    def test_xml_rejects_dtd_entities_alternate_encoding_and_wrong_namespace(self):
        for raw in (b'<!DOCTYPE x [<!ENTITY a "x">]><x/>', b'<!ENTITY a SYSTEM "file:///etc/passwd"><x/>',
                    '<x/>'.encode("utf-16"), b'<x xmlns="wrong"/>'):
            with self.subTest(raw=raw), self.assertRaises((ValueError, UnicodeError)):
                capture.xml_root(raw, "x")

    def test_full_join_rejects_orphans_duplicates_identity_mismatch_and_counts(self):
        cases = [(primary(), filelists().replace(PKGID.encode(), b"f" * 64), 1),
                 (primary(), filelists().replace(b'ver="1.0"', b'ver="2.0"'), 1),
                 (primary(), filelists().replace(b'packages="1"', b'packages="2"'), 1),
                 (primary("x86_64"), filelists("x86_64"), 1),
                 (primary(), filelists(), 2)]
        for p, f, count in cases:
            with self.subTest(primary=p, files=f), self.assertRaises(ValueError):
                capture.joined_namespace(p, f, "riscv64", count)
        p = primary().decode().split('packages="1">')[1].split('</metadata>')[0]
        f = filelists().decode().split('packages="1">')[1].split('</filelists>')[0]
        for p1, f1 in ((primary(packages=p+p, count=2), filelists(packages=f+f, count=2)),
                       (primary(), filelists(packages=f+f, count=2))):
            with self.assertRaises(ValueError):
                capture.joined_namespace(p1, f1, "riscv64", 2)

    def test_filelists_unsafe_or_duplicate_paths_rejected(self):
        for path in (b"relative/file", b"/usr/../file", b"/usr/./file", b"/usr/\\file", b"/usr//bin/file", b"/usr/bin/file/"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                capture.joined_namespace(primary(), filelists().replace(b"/usr/bin/fixture", path), "riscv64", 1)
        with self.assertRaises(ValueError):
            capture.joined_namespace(primary(), filelists().replace(b'<file type="dir">/usr/share/fixture</file>',
                                       b'<file>/usr/bin/fixture</file>'), "riscv64", 1)
        self.assertEqual(capture.joined_namespace(primary(), filelists().replace(b"/usr/share/fixture", b"/"),
                                                 "riscv64", 1)["file_count"], 2)

    def test_source_relative_payload_members_and_safe_subdirectories(self):
        # Regression for actual enabled metadata: 6tunnel's SRPM contains
        # 6tunnel-0.14.tar.gz and 6tunnel.spec, not absolute installed paths.
        for arch in ("src", "nosrc"):
            for member in (b"6tunnel-0.14.tar.gz", b"6tunnel.spec", b"patches/fix.patch",
                           b"sources/nested/fixture.tar.xz"):
                with self.subTest(arch=arch, member=member):
                    files = filelists(arch).replace(b"fixture-1.0.tar.gz", member)
                    self.assertEqual(capture.joined_namespace(primary(arch), files, "source", 1)["file_count"], 2)

    def test_source_rejects_absolute_traversal_empty_control_and_ambiguous_members(self):
        for member in (b"", b"/", b"/usr/src/fixture", b"//server/fixture", b".", b"..",
                       b"./fixture", b"../fixture", b"patches/../fixture", b"patches/./fixture",
                       b"patches//fixture", b"patches/", b"patches/\\fixture", b"C:/fixture",
                       b"file:fixture", b"https://example.test/fixture", b"bad\x7fname", b"bad&#9;name"):
            with self.subTest(member=member), self.assertRaises(ValueError):
                capture.joined_namespace(primary("src"),
                                         filelists("src").replace(b"fixture-1.0.tar.gz", member), "source", 1)
        with self.assertRaises(ValueError):
            capture.joined_namespace(primary("src"),
                                     filelists("src").replace(b"fixture.spec", b"fixture-1.0.tar.gz"), "source", 1)

    def test_binary_relative_source_members_still_rejected(self):
        for member in (b"6tunnel.spec", b"patches/fix.patch", b"fixture-1.0.tar.gz"):
            with self.subTest(member=member), self.assertRaises(ValueError):
                capture.joined_namespace(primary(), filelists().replace(b"/usr/bin/fixture", member), "riscv64", 1)

    def test_source_path_acceptance_preserves_full_identity_join(self):
        for files in (filelists("src").replace(PKGID.encode(), b"f" * 64),
                      filelists("src").replace(b'ver="1.0"', b'ver="2.0"'),
                      filelists("src").replace(b'packages="1"', b'packages="2"')):
            with self.subTest(files=files), self.assertRaises(ValueError):
                capture.joined_namespace(primary("src"), files, "source", 1)

    def test_standard_decoders_bound_open_bytes_and_reject_truncation(self):
        raw = b"metadata" * 100
        for suffix, encoder in (("gz", gzip.compress), ("bz2", bz2.compress), ("xz", lzma.compress)):
            encoded = encoder(raw)
            with self.subTest(suffix=suffix):
                self.assertEqual(capture.decompress(encoded, "repodata/m.xml." + suffix, len(raw)), raw)
                with self.assertRaises(ValueError):
                    capture.decompress(encoded, "repodata/m.xml." + suffix, len(raw) - 1)
                with self.assertRaises((ValueError, EOFError, OSError, zlib.error, lzma.LZMAError)):
                    capture.decompress(encoded[:-5], "repodata/m.xml." + suffix, len(raw))
                for trailing in (b"trailing", encoded):
                    with self.assertRaises(ValueError):
                        capture.decompress(encoded + trailing, "repodata/m.xml." + suffix, len(raw))

    def test_xz_decoder_has_memory_limit_and_rejects_excessive_dictionary(self):
        # Inert LZMA-alone header advertises 256 MiB; constructing this fixture
        # needs only a tiny 4 KiB encoder, not a large experimental allocation.
        encoded = lzma.compress(b"x", format=lzma.FORMAT_ALONE,
                                filters=[{"id": lzma.FILTER_LZMA1, "dict_size": 4096}])
        encoded = encoded[:1] + (256 * 1024 * 1024).to_bytes(4, "little") + encoded[5:]
        with self.assertRaises(lzma.LZMAError):
            capture.decompress(encoded, "repodata/m.xml.xz", 1)

    def test_zstd_uses_fixed_argv_memory_limit_and_output_bound(self):
        process = mock.Mock()
        process.stdout.read.return_value = b"x"
        process.wait.return_value = 0
        process.poll.return_value = 0
        with mock.patch.object(Path, "is_file", return_value=True), mock.patch.object(capture.os, "access", return_value=True), \
                mock.patch.object(capture.subprocess, "Popen", return_value=process) as popen, \
                mock.patch.object(capture.threading, "Timer") as timer:
            self.assertEqual(capture.decompress(b"compressed", "repodata/m.xml.zst", 1), b"x")
            self.assertEqual(popen.call_args.args[0], ["/usr/bin/zstd", "-dc", "--memory=128MB"])
            process.stdout.read.assert_called_once_with(2)
            self.assertEqual(timer.call_args.args[0], 30)
            timer.return_value.start.assert_called_once()
            timer.return_value.cancel.assert_called_once()

    def test_unsupported_compression_and_missing_zstd_are_not_skipped(self):
        with self.assertRaises(ValueError):
            capture.decompress(b"x", "repodata/m.xml.zip", 1)
        with mock.patch.object(Path, "is_file", return_value=False):
            with self.assertRaisesRegex(ValueError, "preinstalled"):
                capture.decompress(b"x", "repodata/m.xml.zst", 1)

    def test_existing_fetch_transport_rejects_redirect_and_foreign_endpoint(self):
        self.assertIsNone(client.NoRedirect().redirect_request(None, None, 302, "x", {}, "http://example.test"))
        for url in ("https://example.test/a", client.PUBLIC_ROOT + "/x?q=1", client.PUBLIC_ROOT + "/x#f"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                client.fetch(url, 100)

    def test_duplicate_json_keys_and_repo_proxy_rejected(self):
        with self.assertRaises(ValueError):
            capture.json_bytes(b'{"generation":"a", "generation":"b"}')
        self.repo += "proxy=http://example.test\n"
        self.rejected()

    def test_workflow_keeps_resolve_and_existing_seven_day_artifact(self):
        workflow = (ROOT / ".github/workflows/package-ci.yml").read_text()
        job = workflow.split("  repository-snapshot:\n", 1)[1].split("  merge-policy:\n", 1)[0]
        self.assertIn("--allow-unavailable", job)
        self.assertLess(job.index("ci/rpm-repo-client.py resolve"), job.index("ci/capture-repository-metadata.py"))
        self.assertIn("--run-attempt \"$SNAPSHOT_RUN_ATTEMPT\"", job)
        self.assertIn("path: artifacts/repository/", job)
        self.assertIn("retention-days: 7", job)
        self.assertNotIn("apt-get", job)
        self.assertNotIn("pip install", job)


if __name__ == "__main__":
    unittest.main()
