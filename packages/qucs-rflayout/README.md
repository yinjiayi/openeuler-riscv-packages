<!-- SPDX-License-Identifier: Apache-2.0 -->
# qucs-rflayout

This directory packages upstream `https://github.com/thomaslepoix/Qucs-RFlayout` version `2.1.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `2` matches the pinned archive's exact `Qucs-RFlayout-2.1.2` source root, declares the fixed-repository Qt 6 and OpenGL development providers, and uses upstream's `check` target so its excluded unit-test executable is built before CTest. GUI and test functionality remain enabled, the source SHA-256 is unchanged, and the RISC-V build status remains `unknown` pending fresh CI evidence.

Release `4` keeps the complete GUI and Catch test targets enabled while fixing
upstream's optional XeLaTeX handling: generated diagram files become a product
dependency only when CMake actually finds XeLaTeX. The normal documentation and
installation targets remain intact.

Release `5` runs CMake installation from its generated build directory.
Upstream's `Gzip.cmake` install hook invokes `make gzip` in the current
directory; calling it from the source directory failed to generate the
compressed manual and changelog after compilation completed. The build
directory contains that target, so the hook can create both documentation
files before CMake installs them. The existing GUI, Catch checks, and optional
LaTeX patch are retained; fresh target CI must verify the repair.

Release `6` addresses the next failure in the bundled Catch2 test framework:
modern glibc obtains signal-stack sizes at runtime, whereas this older header
uses one as a constant array size. A small adaptation of
[Catch2's upstream fix](https://github.com/catchorg/Catch2/commit/8f277a54c0b9c1d1024dedcb2dec1d206971e745)
allocates the alternate stack once with owned storage and retains fatal-signal
reporting. The complete `check` target remains enabled; the prior run completed
installation but could not compile its unit-test executable.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
