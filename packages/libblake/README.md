# Libblake

The official 3.0.2.1 archive implements BLAKE-224/256/384/512, BLAKE2s/b and BLAKE2Xs/Xb. Its default configuration enables all eight; optional x86 SIMD source files are not selected in the default object list. No feature or original test is disabled and no source patch is applied.

The recipe runs upstream make all and make check, retaining every original known-answer vector. The tests subpackage retains the complete original archive. Its unchanged test driver is compiled with the same eight SUPPORT macros and run from the original four-file KAT corpus against both staged and normally installed static/shared libraries. Archive SHA-256 and installed-header equality are checked before each replay. Upstream TODO coverage gaps are retained, not represented as newly tested behavior.

The full ISC notice (2022, 2023, 2024, 2026 Mattias Andrée) is shipped in each explicit subpackage. Upstream /usr/lib is relocated only inside the isolated buildroot to openEuler lib64. Full target build, ordinary installation, original test results and physical RPM/SRPM verification remain merge requirements; local repository tooling tests alone are not package acceptance.
