# SPDX-License-Identifier: Apache-2.0
"""Architecture authorization must come from diagnostics, never installed names."""
from __future__ import annotations

import runpy
import sys
import unittest

from helpers import SCRIPTS

sys.path.insert(0, str(SCRIPTS))


class ClassifierArchitectureEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.classify = staticmethod(runpy.run_path(str(SCRIPTS / "classify-failure"))["classify"])

    def assert_unknown_no_patch(self, text: str) -> None:
        result = self.classify(text, False, None)
        self.assertEqual(result["category"], "unknown")
        self.assertFalse(result["source_patch_allowed"])
        self.assertFalse(result["repairable_locally"])

    def assert_riscv_diagnostic(self, text: str) -> None:
        result = self.classify(text, False, None)
        self.assertEqual(result["category"], "riscv-specific")
        self.assertTrue(result["source_patch_allowed"])
        self.assertTrue(result["evidence"])

    def test_actual_hdr_install_path_is_not_architecture_failure(self) -> None:
        self.assert_unknown_no_patch(
            "-- Installing: /workspace/work/hdrhistogram-c/BUILDROOT/"
            "hdrhistogram-c-0.12.1-1.riscv64/usr/bin/hdr_histogram_atomic_test\n"
        )

    def test_path_cannot_override_generic_rpm_wrapper(self) -> None:
        result = self.classify(
            "-- Installing: /workspace/work/hdrhistogram-c/BUILDROOT/"
            "hdrhistogram-c-0.12.1-1.riscv64/usr/bin/hdr_histogram_atomic_test\n"
            "CTest process return code -4 (SIGILL), before its first result\n"
            "error: Bad exit status from /var/tmp/rpm-tmp.example (%check)\n",
            False,
            None,
        )
        # Existing wrapper fallback only, not proof of a SPEC cause.
        self.assertEqual(result["category"], "spec-packaging")
        self.assertFalse(result["source_patch_allowed"])

    def test_standalone_atomic_executable_path_is_not_diagnostic(self) -> None:
        self.assert_unknown_no_patch("-- Installing: /BUILDROOT/demo.riscv64/usr/bin/atomic\n")

    def test_riscv_macro_header_path_is_not_diagnostic(self) -> None:
        self.assert_unknown_no_patch("Copying /usr/include/__riscv/atomic.h\n")

    def test_hyphenated_test_name_does_not_authorize_source_patch(self) -> None:
        self.assert_unknown_no_patch("Built target riscv-atomic-error-test\n")

    def test_atomic_support_information_is_not_a_failure(self) -> None:
        self.assert_unknown_no_patch("riscv64 atomic operations enabled\n")

    def test_sigill_alone_is_not_source_or_native_diagnosis(self) -> None:
        self.assert_unknown_no_patch("CTest process exited with SIGILL (-4) before first test result\n")

    def test_riscv_atomic_not_supported_diagnostic_is_retained(self) -> None:
        self.assert_riscv_diagnostic("source.c:4: error: RISC-V atomic operations are not supported\n")

    def test_riscv_atomic_extension_requirement_is_retained(self) -> None:
        self.assert_riscv_diagnostic("riscv64: error: atomic instructions require extension A\n")

    def test_reverse_atomic_riscv_diagnostic_is_retained(self) -> None:
        self.assert_riscv_diagnostic("source.c:4: error: atomic operations unsupported on RISC-V\n")

    def test_unsupported_isa_diagnostic_is_retained(self) -> None:
        self.assert_riscv_diagnostic("cc1: error: unsupported ISA string 'rv64bad'\n")

    def test_unrecognized_riscv_opcode_diagnostic_is_retained(self) -> None:
        self.assert_riscv_diagnostic("assembler: error: unrecognized opcode for riscv64 target\n")

    def test_riscv_macro_in_explicit_error_is_retained(self) -> None:
        self.assert_riscv_diagnostic('#error "__riscv must be defined for this implementation"\n')

    def test_generic_build_failure_stays_generic(self) -> None:
        result = self.classify("ninja: error: subcommand failed\n", False, None)
        self.assertEqual(result["category"], "upstream-build")
        self.assertNotEqual(result["category"], "riscv-specific")


if __name__ == "__main__":
    unittest.main()
