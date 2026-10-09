<!-- SPDX-License-Identifier: Apache-2.0 -->
# catch2

This directory packages upstream `https://github.com/catchorg/Catch2` version `3.16.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The earlier 3.16.1 CI run invoked CTest in the source directory and reported
`No tests were found!!!`; that exit status did not prove the upstream suite passed.
The SPEC now runs the complete, unfiltered suite serially in the CMake build
directory and uses `--no-tests=error` to reject an empty suite. Validation of this
repair requires fresh CI for its exact commit; the installed smoke test alone
does not satisfy the upstream test gate.

The immutable discovery snapshot cross-checks Arch stable, Debian stable, Fedora GA, and openSUSE Tumbleweed records. Only the official stable tag archive and independently calculated SHA-256 are build inputs; no AUR recipe or distribution build hook is read or executed.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
