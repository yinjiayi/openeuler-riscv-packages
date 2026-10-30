# SPDX-License-Identifier: Apache-2.0
"""Image infrastructure routing requires diagnostics, not echoed QA code."""
from __future__ import annotations

import json
import pathlib
import runpy
import sys
import tempfile
import unittest

from helpers import SCRIPTS

sys.path.insert(0, str(SCRIPTS))

# Exact line 375 of retained Plutovg first-failure rpmbuild-internal.log,
# SHA256 cad66537d3b77524c88b350ab1211eb466deeffc87a1a2ac61b5bf7511053ffd.
# It is untrusted source text from a traceback, never executed by these tests.
ACTUAL_PLUTO_QA_SOURCE = "    image=build/'consumer.png';stdout,stderr=run(label+'-run',[str(binary),str(font),str(fontdir),str(image)],timeout=90);assert stdout==expected and stderr==b'';w,h,p=png(image);assert (w,h)==(16,16) and p(8,8)==(255,0,0,255) and p(1,1)==(0,0,255,255) and p(15,15)==(0,0,0,0);proofs.append(dict(layout=layout,standard=standard,route=route,binary_sha256=sha(binary),archive_path=str(archive),archive_sha256=sha(archive),header_sha256=sha(header),map_sha256=sha(mapfile),recorded_map_LOAD_paths=maploads,recorded_link_trace_paths=actual_archives,recorded_GCC_header_paths=actual_headers,target_samefile_archive_and_header=True,PNG_sha256=sha(image),groups=7,stdout_sha256=hashlib.sha256(stdout).hexdigest()))"
RPM_WRAPPER = "error: Bad exit status from /var/tmp/rpm-tmp.example (%check)\n"


class ClassifierImageDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        namespace = runpy.run_path(str(SCRIPTS / "classify-failure"))
        cls.classify = staticmethod(namespace["classify"])
        cls.read_input = staticmethod(namespace["read_input"])

    def assert_unknown(self, text: str) -> None:
        result = self.classify(text, False, None)
        self.assertEqual(result["category"], "unknown")
        self.assertFalse(result["source_patch_allowed"])
        self.assertFalse(result["repairable_locally"])

    def assert_infrastructure(self, text: str) -> None:
        result = self.classify(text, False, None)
        self.assertEqual(result["category"], "infrastructure")
        self.assertFalse(result["source_patch_allowed"])
        self.assertFalse(result["repairable_locally"])
        self.assertTrue(result["evidence"])

    def test_actual_plutovg_source_excerpt_is_not_image_failure(self) -> None:
        self.assert_unknown(ACTUAL_PLUTO_QA_SOURCE + "\n")

    def test_actual_excerpt_does_not_override_rpm_wrapper(self) -> None:
        result = self.classify(
            'Traceback (most recent call last):\n'
            '  File "/build/.packaging-qa/assets/run-qa.py", line 74, in <module>\n'
            + ACTUAL_PLUTO_QA_SOURCE + "\n"
            + "AssertionError: ('installed-c99-pkgconf-run', 1, 0)\n"
            + RPM_WRAPPER,
            False, None,
        )
        # Wrapper fallback remains only a routing classification, not proof
        # that the actual decoded UTF-16 failure was a SPEC or image defect.
        self.assertEqual(result["category"], "spec-packaging")
        self.assertFalse(result["source_patch_allowed"])
        self.assertNotEqual(result["category"], "infrastructure")

    def test_successful_image_digest_is_provenance(self) -> None:
        self.assert_unknown("Using pinned image example digest sha256:" + "a" * 64 + "\n")

    def test_image_digest_key_alone_is_not_failure(self) -> None:
        self.assert_unknown("image_digest: sha256:" + "b" * 64 + "\n")

    def test_quoted_python_failure_statement_is_not_runtime(self) -> None:
        self.assert_unknown('    raise RuntimeError("image digest mismatch")\n')

    def test_echoed_shell_diagnostic_is_not_runtime(self) -> None:
        self.assert_unknown("+ echo 'image digest mismatch'\n")

    def test_unrelated_later_clause_failure_is_not_image_failure(self) -> None:
        result = self.classify(
            "image digest verified; unrelated test failed to start\n", False, None,
        )
        self.assertEqual(result["category"], "upstream-build")
        self.assertEqual(result["evidence"][0]["pattern"], r"tests? failed|FAIL:")

    def test_real_digest_mismatch_is_infrastructure(self) -> None:
        self.assert_infrastructure("RuntimeError: image digest mismatch: expected sha256:a, got sha256:b\n")

    def test_real_invalid_pinned_digest_is_infrastructure(self) -> None:
        self.assert_infrastructure("Error: invalid pinned image digest sha256:broken\n")

    def test_real_digest_verification_failure_is_infrastructure(self) -> None:
        self.assert_infrastructure("image digest verification failed\n")

    def test_real_image_pull_failure_is_preserved(self) -> None:
        self.assert_infrastructure("Error response from daemon: failed to pull OCI image example\n")

    def test_real_image_resolution_failure_is_preserved(self) -> None:
        self.assert_infrastructure("failed to resolve reference for image example@sha256:a\n")

    def test_real_manifest_unknown_is_preserved(self) -> None:
        self.assert_infrastructure("Error response from daemon: manifest unknown\n")

    def test_later_real_image_diagnostic_is_not_dropped_with_excerpt(self) -> None:
        self.assert_infrastructure(
            ACTUAL_PLUTO_QA_SOURCE + "\n"
            "RuntimeError: image digest does not match the locked image\n"
        )

    def test_harmless_image_line_does_not_override_dependency(self) -> None:
        result = self.classify(
            "image digest verified sha256:a\n"
            "fatal error: dependency.h: No such file or directory\n",
            False, None,
        )
        self.assertEqual(result["category"], "dependency")

    def test_failure_bearing_json_image_diagnostic_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "result.json"
            path.write_text(json.dumps({
                "status": "failed",
                "failure": {"message": "image digest mismatch: expected sha256:a got sha256:b"},
                "environment": {"image_digest": "sha256:c"},
            }), encoding="utf-8")
            _, text = self.read_input(path)
            self.assert_infrastructure(text)


if __name__ == "__main__":
    unittest.main()
