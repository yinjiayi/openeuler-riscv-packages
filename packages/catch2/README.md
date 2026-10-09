<!-- SPDX-License-Identifier: Apache-2.0 -->
# catch2

This directory packages upstream `https://github.com/catchorg/Catch2` version `3.16.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The earlier 3.16.1 CI run invoked CTest in the source directory and reported
`No tests were found!!!`; that exit status did not prove the upstream suite passed.
The SPEC now runs the complete, unfiltered suite serially in the CMake build
directory and uses `--no-tests=error` to reject an empty suite. Validation of this
repair requires fresh CI for its exact commit; the installed smoke test alone
does not satisfy the upstream test gate.

The first corrected-directory run, at commit
`1a6794e2f3705da1b6958915dd48e8ea368f3f3f` (Package CI `37936210975`),
registered 82 CTest cases and completed 56 cases successfully. After starting
case 57, `ErrorHandling::InvalidTestSpecExitsEarly`, the shell reported that the
CTest process received an illegal-instruction signal. Case 57 has no terminal
result, and 26 cases have no completion record; this is not evidence that a
Catch2 assertion failed or that the whole suite passed.

The SPEC adds failure-preserving diagnostics for one fresh CI run: CTest's
version, CTest and SelfTest file SHA-256/ELF identification bytes, generated
CTest registration, the full unfiltered serial suite's verbose output, and
`LastTest.log` when a suite failure leaves it available. The original CTest
nonzero exit status remains the package check's exit status even if that log
cannot be read. This is diagnostic instrumentation, not a source fix, test
bypass, or established QEMU defect. No source, default test, feature flag,
dependency or shared CI setting changes; the existing CI log cap stays in place.
Fresh full-suite, installed-smoke and physical-product evidence remains required.

The immutable discovery snapshot cross-checks Arch stable, Debian stable, Fedora GA, and openSUSE Tumbleweed records. Only the official stable tag archive and independently calculated SHA-256 are build inputs; no AUR recipe or distribution build hook is read or executed.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
