# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import os
import pathlib
import runpy
import sys
import tempfile
import unittest
from unittest import mock

from helpers import SCRIPTS, run_tool, write_json

sys.path.insert(0, str(SCRIPTS))
from _lib import canonical_tar_gz  # noqa: E402


def golden_package(root: pathlib.Path, package_id: str, digest: str, profile: str = "qemu-user") -> pathlib.Path:
    directory = root / "packages" / package_id
    (directory / "patches").mkdir(parents=True)
    (directory / "tests").mkdir()
    write_json(
        directory / "package.yaml",
        {
            "schema_version": 1,
            "package_id": package_id,
            "rpm": {"name": package_id, "summary": "fixture", "license": "MIT"},
            "upstream": {"component": package_id, "homepage": "https://example.org", "source_repository": "https://example.org/repo.git", "release_channel": "fixture", "release_api": None, "release_regex": None},
            "version": {"current": "1.0", "release": "1", "latest_detected": "1.0"},
            "discovery": {"snapshot_id": "golden", "lineage": [{"source": "golden-fixture", "package_name": package_id, "package_base": package_id, "source_version": "1.0", "evidence_url": "https://example.org", "observed_at": None}]},
            "target": {"os": "openEuler", "release": "24.03-LTS-SP3", "arch": "riscv64", "isa": "RVA23", "riscv_status": "unknown"},
            "build": {"profile": profile, "network_during_build": False, "timeout_minutes": 30, "native_reason": "kernel module load required" if profile != "qemu-user" else None},
            "files": {"spec": "%s.spec" % package_id, "sources": "sources.yaml", "patches": [], "smoke_test": "tests/smoke.sh"},
            "maintenance": {"status": "golden", "maintainers": [], "notes": None},
            "updates": {"enabled": False, "last_checked_at": None, "last_successful_check_at": None, "release_provider": None},
        },
    )
    write_json(
        directory / "sources.yaml",
        {"schema_version": 1, "package_id": package_id, "sources": [{"id": "source0", "kind": "golden-fixture", "url": "fixture://tests/golden/fixtures/%s-1.0" % package_id, "filename": "%s-1.0.tar.gz" % package_id, "version": "1.0", "digests": {"sha256": digest}, "signature": None, "redistribution": {"allowed": True, "reason": "test fixture"}}]},
    )
    (directory / ("%s.spec" % package_id)).write_text("# SPDX-License-Identifier: Apache-2.0\nName: %s\nVersion: 1.0\nRelease: 1\nBuildRequires: gcc\n%%prep\n%%build\n%%install\n%%check\n%%files\n%%changelog\n" % package_id, encoding="utf-8")
    (directory / "patches" / "series").write_text("", encoding="utf-8")
    (directory / "tests" / "smoke.sh").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    return directory


class BuildAndClassifyTests(unittest.TestCase):
    def test_explicit_source_denial_blocks_every_mode_before_side_effects(self) -> None:
        namespace = runpy.run_path(str(SCRIPTS / "build-rpm"))
        main = namespace["main"]
        schema = json.loads((SCRIPTS.parent / "schemas" / "build-result.schema.json").read_text())
        schema_errors = runpy.run_path(str(SCRIPTS / "validate-metadata"))["schema_errors"]
        for mode in ([], ["--verify-only"], ["--plan"], ["--verify-only", "--offline"]):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temporary:
                root = pathlib.Path(temporary)
                package = golden_package(root, "golden-denied", "a" * 64)
                sources = json.loads((package / "sources.yaml").read_text())
                # A later denial must prevent even the first permitted fetch.
                denied = dict(sources["sources"][0])
                denied.update({"id": "source1", "url": "https://example.org/denied.tar.gz", "redistribution": {"allowed": False, "reason": "untrusted reason must not be echoed"}})
                sources["sources"].append(denied)
                write_json(package / "sources.yaml", sources)
                result = root / "result.json"
                argv = ["--package-dir", str(package), "--repo-root", str(root), "--work-dir", str(root / "work"), "--cache-dir", str(root / "cache"), "--result", str(result), "--commit-sha", "a" * 40] + mode
                operations = {name: mock.Mock(side_effect=AssertionError(name + " must not run")) for name in ("prepare_dirs", "materialize_source", "stage_package", "build_requires", "environment_check", "run_logged")}
                with mock.patch.dict(main.__globals__, operations), mock.patch.object(sys, "argv", ["build-rpm"] + argv):
                    self.assertEqual(main(), 1)
                for operation in operations.values():
                    operation.assert_not_called()
                document = json.loads(result.read_text())
                self.assertEqual(document["status"], "failed")
                self.assertEqual(document["phase"], "source-verify")
                self.assertEqual(document["commit_sha"], "a" * 40)
                self.assertEqual(document["source_verification"], [])
                self.assertEqual(document["commands"], [])
                self.assertEqual(document["artifacts"], [])
                self.assertEqual(schema_errors(document, schema, schema), [])
                self.assertIn("explicitly disallowed", document["failure"]["message"])
                self.assertNotIn("untrusted reason", result.read_text())
                self.assertFalse((root / "work").exists())
                self.assertFalse((root / "cache").exists())
                # Exercise the real CLI failure envelope as well, including the
                # nullable provenance field when no exact commit is provided.
                cli_result = root / "cli-result.json"
                run_tool("build-rpm", ["--package-dir", str(package), "--repo-root", str(root), "--work-dir", str(root / "cli-work"), "--result", str(cli_result)] + mode, root, expected=1)
                cli_document = json.loads(cli_result.read_text())
                self.assertIsNone(cli_document["commit_sha"])
                self.assertEqual(cli_document["phase"], "source-verify")
                self.assertEqual(schema_errors(cli_document, schema, schema), [])
                self.assertFalse((root / "cli-work").exists())

    def test_direct_materialization_denial_blocks_download_fixture_and_offline_reuse(self) -> None:
        namespace = runpy.run_path(str(SCRIPTS / "build-rpm"))
        materialize = namespace["materialize_source"]
        from _lib import SourceRedistributionError
        for url, offline in (("https://example.org/source.tar.gz", False), ("fixture://fixture", False), ("https://example.org/source.tar.gz", True)):
            with self.subTest(url=url, offline=offline), tempfile.TemporaryDirectory() as temporary:
                root = pathlib.Path(temporary)
                (root / "source.tar.gz").write_bytes(b"stale source must remain untouched")
                operations = {name: mock.Mock(side_effect=AssertionError(name + " must not run")) for name in ("fetch_url", "canonical_tar_gz", "fixture_path", "sha256_file", "verify_signature")}
                with mock.patch.dict(materialize.__globals__, operations):
                    with self.assertRaises(SourceRedistributionError):
                        materialize({"url": url, "filename": "source.tar.gz", "digests": {"sha256": "a" * 64}, "redistribution": {"allowed": False}}, package_id="golden-denied", repo_root=root, sources_dir=root, cache_dir=root / "cache", timeout=1, retries=1, offline=offline)
                for operation in operations.values():
                    operation.assert_not_called()
                self.assertEqual((root / "source.tar.gz").read_bytes(), b"stale source must remain untouched")
                self.assertFalse((root / "cache").exists())

    def test_allowed_source_download_retains_checksum_and_cache_contract(self) -> None:
        namespace = runpy.run_path(str(SCRIPTS / "build-rpm"))
        materialize = namespace["materialize_source"]
        from _lib import sha256_bytes
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            url = "https://example.org/source.tar.gz"
            content = b"verified permitted source"
            fetch = mock.Mock(return_value=(content, {"url": url}))
            entry = {"id": "source0", "url": url, "filename": "source.tar.gz", "digests": {"sha256": sha256_bytes(content)}, "redistribution": {"allowed": True}}
            with mock.patch.dict(materialize.__globals__, {"fetch_url": fetch}):
                result = materialize(entry, package_id="demo", repo_root=root, sources_dir=root, cache_dir=root / "cache", timeout=7, retries=2, offline=False)
            fetch.assert_called_once_with(url, timeout=7, retries=2, cache_dir=root / "cache", max_bytes=2 * 1024 * 1024 * 1024)
            self.assertTrue(result["verified"])
            self.assertEqual(result["sha256"], sha256_bytes(content))
            self.assertEqual((root / "source.tar.gz").read_bytes(), content)

    def test_first_error_ignores_zero_automake_counter(self) -> None:
        namespace = runpy.run_path(str(SCRIPTS / "build-rpm"))
        first_error = namespace["first_error"]
        log = "\n".join(
            [
                "PASS: tests/hello-1",
                "FAIL: tests/atexit-1",
                "# FAIL: 1",
                "# ERROR: 0",
            ]
        )
        self.assertEqual(first_error(log), "FAIL: tests/atexit-1")

    def test_first_error_ignores_zero_test_summaries_and_uses_log_order(self) -> None:
        namespace = runpy.run_path(str(SCRIPTS / "build-rpm"))
        first_error = namespace["first_error"]
        timeout = "lock-test-multiple-monitors time out (After 120 seconds)"
        log = "\n".join(
            [
                timeout,
                "59/59 lock-test-multiple-monitors TIMEOUT 120.11s killed by signal 15 SIGTERM",
                "Fail: 0",
                "# ERROR: 0",
                "Timeout: 1",
                "100% tests passed, 0 tests failed out of 59",
                "error: Bad exit status from /var/tmp/rpm-tmp.abc (%check)",
            ]
        )
        self.assertEqual(first_error(log), timeout)

    def test_first_error_returns_none_for_only_zero_test_summaries(self) -> None:
        namespace = runpy.run_path(str(SCRIPTS / "build-rpm"))
        first_error = namespace["first_error"]
        log = "\n".join(
            [
                "Fail: 0",
                "Error: 0",
                "Timeout: 0",
                "100% tests passed, 0 tests failed out of 59",
            ]
        )
        self.assertIsNone(first_error(log))

    def test_first_error_keeps_rpm_wrapper_as_zero_summary_fallback(self) -> None:
        namespace = runpy.run_path(str(SCRIPTS / "build-rpm"))
        first_error = namespace["first_error"]
        wrapper = "error: Bad exit status from /var/tmp/rpm-tmp.abc (%check)"
        log = "\n".join(["Fail: 0", "# FAIL: 0", "Error: 0", "# ERROR: 0", wrapper])
        self.assertEqual(first_error(log), wrapper)

    def test_first_error_ignores_timeout_configuration(self) -> None:
        namespace = runpy.run_path(str(SCRIPTS / "build-rpm"))
        first_error = namespace["first_error"]
        wrapper = "error: Bad exit status from /var/tmp/rpm-tmp.abc (%check)"
        log = "\n".join(
            [
                "GTKLS_TEST_TIMEOUT_MULTIPLIER=10",
                "meson test --timeout-multiplier 10",
                "runner --timeout 120s",
                wrapper,
            ]
        )
        self.assertEqual(first_error(log), wrapper)

    def test_first_error_preserves_real_failure_before_timeout(self) -> None:
        namespace = runpy.run_path(str(SCRIPTS / "build-rpm"))
        first_error = namespace["first_error"]
        log = "\n".join(
            [
                "FAIL: tests/atexit-1",
                "1/2 tests/slow TIMEOUT 120.00s killed by signal 15 SIGTERM",
            ]
        )
        self.assertEqual(first_error(log), "FAIL: tests/atexit-1")

    def test_first_error_ignores_benign_asterisk_banner(self) -> None:
        namespace = runpy.run_path(str(SCRIPTS / "build-rpm"))
        first_error = namespace["first_error"]
        log = "\n".join(
            [
                "*** Configuration summary ***",
                "FAIL: tests/atexit-1",
                "make[1]: *** [Makefile:42: check] Error 1",
            ]
        )
        self.assertEqual(first_error(log), "FAIL: tests/atexit-1")

    def test_first_error_keeps_gnu_make_failure(self) -> None:
        namespace = runpy.run_path(str(SCRIPTS / "build-rpm"))
        first_error = namespace["first_error"]
        make_error = "gmake[2]: *** [Makefile:17: all] Error 2"
        self.assertEqual(first_error("*** Build summary ***\n" + make_error), make_error)

    def test_fixture_source_is_canonical_and_offline_reusable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            fixture = root / "tests" / "golden" / "fixtures" / "golden-demo-1.0"
            fixture.mkdir(parents=True)
            (fixture / "hello.c").write_text("int main(void){return 0;}\n", encoding="utf-8")
            archive = root / "expected.tar.gz"
            digest = canonical_tar_gz(fixture, archive, "golden-demo-1.0")["sha256"]
            package_dir = golden_package(root, "golden-demo", digest)
            result = root / "result.json"
            exact_head = "a" * 40
            with mock.patch.dict(os.environ, {"GITHUB_SHA": "b" * 40}):
                run_tool("build-rpm", ["--package-dir", str(package_dir), "--repo-root", str(root), "--work-dir", str(root / "work"), "--result", str(result), "--commit-sha", exact_head, "--verify-only", "--now", "2026-08-08T00:00:00Z"], root)
            document = json.loads(result.read_text())
            self.assertEqual(document["status"], "source-verified")
            self.assertEqual(document["commit_sha"], exact_head)
            self.assertEqual(document["source_verification"][0]["sha256"], digest)
            self.assertEqual(document["dependency_plan"]["build_requires"], ["gcc"])
            offline = root / "offline.json"
            run_tool("build-rpm", ["--package-dir", str(package_dir), "--repo-root", str(root), "--work-dir", str(root / "work"), "--result", str(offline), "--verify-only", "--offline", "--now", "2026-08-08T00:01:00Z"], root)
            self.assertEqual(json.loads(offline.read_text())["status"], "source-verified")

    def test_failure_classification_and_native_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            inline = root / "inline.log"
            inline.write_text("error: unknown register name 'eax' in inline asm\n", encoding="utf-8")
            output = root / "inline.json"
            run_tool("classify-failure", ["--input", str(inline), "--output", str(output), "--now", "2026-08-08T00:00:00Z"], root)
            document = json.loads(output.read_text())
            self.assertEqual(document["classification"]["category"], "riscv-specific")
            self.assertEqual(document["recommended_state"], "repair-queued")

            fixture = root / "tests" / "golden" / "fixtures" / "golden-kmod-1.0"
            fixture.mkdir(parents=True)
            (fixture / "x").write_text("x")
            digest = canonical_tar_gz(fixture, root / "k.tar.gz", "golden-kmod-1.0")["sha256"]
            package_dir = golden_package(root, "golden-kmod", digest, "needs-native-riscv")
            native = root / "native.json"
            run_tool("classify-failure", ["--input", str(inline), "--package-dir", str(package_dir), "--output", str(native), "--now", "2026-08-08T00:00:00Z"], root)
            self.assertEqual(json.loads(native.read_text())["recommended_state"], "needs-native-riscv")

    def test_specific_riscv_evidence_beats_generic_rpmbuild_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            result = root / "build-result.json"
            write_json(
                result,
                {
                    "package_id": "golden-riscv-inline-asm",
                    "status": "failed",
                    "phase": "rpmbuild",
                    "failure": {
                        "message": "error: Bad exit status from /var/tmp/rpm-tmp.abc (%build)",
                    },
                },
            )
            internal_log = root / "rpmbuild-internal.log"
            internal_log.write_text(
                'golden_inline.c:12:2: error: #error "golden failure: x86-only counter lacks a RISC-V implementation"\n',
                encoding="utf-8",
            )
            output = root / "classification.json"
            run_tool(
                "classify-failure",
                [
                    "--input",
                    str(result),
                    "--log",
                    str(internal_log),
                    "--output",
                    str(output),
                    "--now",
                    "2026-08-08T00:00:00Z",
                ],
                root,
            )
            document = json.loads(output.read_text())
            self.assertEqual(document["classification"]["category"], "riscv-specific")
            self.assertTrue(document["classification"]["source_patch_allowed"])

    def test_envelope_image_digest_is_not_failure_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            result = root / "final-build-result.json"
            write_json(
                result,
                {
                    "package_id": "golden-riscv-inline-asm",
                    "status": "failed",
                    "failure_summary": "rpmbuild failed with exit code 1: error: Bad exit status from /var/tmp/rpm-tmp.abc (%build)",
                    "environment": {
                        "image_digest": "sha256:" + "d" * 64,
                        "arch": "riscv64",
                        "isa": "RVA23",
                    },
                },
            )
            internal_log = root / "rpmbuild-internal.log"
            internal_log.write_text(
                'golden_inline.c:12:2: error: #error "golden failure: x86-only counter lacks a RISC-V implementation"\n',
                encoding="utf-8",
            )
            output = root / "classification.json"
            run_tool(
                "classify-failure",
                [
                    "--input",
                    str(result),
                    "--log",
                    str(internal_log),
                    "--output",
                    str(output),
                    "--now",
                    "2026-08-08T00:00:00Z",
                ],
                root,
            )
            document = json.loads(output.read_text())
            self.assertEqual(document["classification"]["category"], "riscv-specific")
            self.assertNotIn("failure:infrastructure", document["labels"])

    def test_single_test_timeout_beats_generic_rpmbuild_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            result = root / "build-result.json"
            write_json(
                result,
                {
                    "package_id": "gtk4-layer-shell",
                    "status": "failed",
                    "phase": "rpmbuild",
                    "failure_summary": "rpmbuild failed with exit code 1: error: Bad exit status from /var/tmp/rpm-tmp.abc (%check)",
                    "failure": {
                        "first_effective_error": "rpmbuild failed with exit code 1: Fail: 0",
                        "message": "rpmbuild failed with exit code 1: Fail: 0",
                    },
                },
            )
            internal_log = root / "rpmbuild-internal.log"
            internal_log.write_text(
                "[1/2] cc -o test meson-generated.c.o -Werror\n"
                "lock-test-multiple-monitors time out (After 120 seconds)\n"
                "59/59 lock-test-multiple-monitors TIMEOUT 120.11s killed by signal 15 SIGTERM\n"
                "Ok: 58\n"
                "Expected Fail: 0\n"
                "Fail: 0\n"
                "Timeout: 1\n",
                encoding="utf-8",
            )
            output = root / "classification.json"
            run_tool(
                "classify-failure",
                [
                    "--input",
                    str(result),
                    "--log",
                    str(internal_log),
                    "--output",
                    str(output),
                    "--now",
                    "2026-09-03T00:00:00Z",
                ],
                root,
            )
            document = json.loads(output.read_text())
            classification = document["classification"]
            self.assertEqual(classification["category"], "upstream-build")
            self.assertEqual(classification["confidence"], "high")
            self.assertFalse(classification["repairable_locally"])
            self.assertFalse(classification["source_patch_allowed"])
            self.assertEqual(document["recommended_state"], "failed")
            self.assertNotIn("failure:spec-packaging", document["labels"])
            self.assertNotIn("failure:qemu-limitation", document["labels"])
            self.assertIn("time out", classification["evidence"][0]["excerpt"])

    def test_earlier_test_failure_beats_later_test_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            log = root / "parallel-test-failure.log"
            log.write_text(
                "FAIL: tests/assertion-first\n"
                "59/59 lock-test-multiple-monitors TIMEOUT 120.11s killed by signal 15 SIGTERM\n"
                "error: Bad exit status from /var/tmp/rpm-tmp.abc (%check)\n",
                encoding="utf-8",
            )
            output = root / "classification.json"
            run_tool(
                "classify-failure",
                ["--input", str(log), "--output", str(output), "--now", "2026-09-03T00:00:00Z"],
                root,
            )
            document = json.loads(output.read_text())
            classification = document["classification"]
            self.assertEqual(classification["category"], "upstream-build")
            self.assertEqual(classification["confidence"], "medium")
            self.assertTrue(classification["repairable_locally"])
            self.assertTrue(classification["source_patch_allowed"])
            self.assertEqual(document["recommended_state"], "repair-queued")
            self.assertIn("FAIL: tests/assertion-first", classification["evidence"][0]["excerpt"])
            self.assertIn("FAIL:", classification["evidence"][0]["pattern"])

    def test_zero_meson_and_ctest_counts_are_not_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            log = root / "successful-test-summary.log"
            log.write_text(
                "Ok: 59\n"
                "Fail: 0\n"
                "Error: 0\n"
                "Timeout: 0\n"
                "100% tests passed, 0 tests failed out of 59\n",
                encoding="utf-8",
            )
            output = root / "classification.json"
            run_tool(
                "classify-failure",
                ["--input", str(log), "--output", str(output), "--now", "2026-09-03T00:00:00Z"],
                root,
            )
            classification = json.loads(output.read_text())["classification"]
            self.assertEqual(classification["category"], "unknown")
            self.assertEqual(classification["confidence"], "low")

    def test_dependency_timeout_does_not_treat_kmod_package_as_native(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            result = root / "dependency-failure.json"
            write_json(
                result,
                {
                    "package_id": "gui-demo",
                    "status": "failed",
                    "phase": "dependency-prepare",
                    "exit_code": 124,
                    "message": "Audited BuildRequires preparation failed; see install.log.",
                },
            )
            install_log = root / "install.log"
            install_log.write_text(
                "Install 418 Packages\n"
                "kmod-libs riscv64 30-11.oe2403sp3 openeuler-rva23 56 k\n"
                "context canceled\n",
                encoding="utf-8",
            )
            output = root / "classification.json"
            run_tool(
                "classify-failure",
                [
                    "--input",
                    str(result),
                    "--log",
                    str(install_log),
                    "--output",
                    str(output),
                    "--now",
                    "2026-08-31T00:00:00Z",
                ],
                root,
            )
            document = json.loads(output.read_text())
            self.assertEqual(document["classification"]["category"], "infrastructure")
            self.assertEqual(document["recommended_state"], "failed")
            self.assertNotIn("needs-native-riscv", document["labels"])

    def test_invalid_locked_image_rpm_baseline_is_infrastructure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            result = root / "dependency-failure.json"
            write_json(
                result,
                {
                    "package_id": "demo",
                    "status": "failed",
                    "phase": "dependency-prepare",
                    "exit_code": 1,
                    "message": "Audited BuildRequires preparation failed; see install.log.",
                },
            )
            install_log = root / "install.log"
            install_log.write_text(
                "base-image-rpm-baseline-invalid: dependency networking and installation were refused.\n",
                encoding="utf-8",
            )
            output = root / "classification.json"
            run_tool(
                "classify-failure",
                [
                    "--input",
                    str(result),
                    "--log",
                    str(install_log),
                    "--output",
                    str(output),
                    "--now",
                    "2026-09-02T00:00:00Z",
                ],
                root,
            )
            document = json.loads(output.read_text())
            self.assertEqual(document["classification"]["category"], "infrastructure")
            self.assertFalse(document["classification"]["repairable_locally"])
            self.assertFalse(document["classification"]["source_patch_allowed"])


if __name__ == "__main__":
    unittest.main()
