<!-- SPDX-License-Identifier: Apache-2.0 -->
# kfr

This directory packages upstream `https://github.com/kfrlib/kfr` version `7.0.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 2 follows upstream's supported RISC-V build path: Clang compiles the RVV backend with `-march=rv64gcv` and `KFR_ARCH=rvv`. The package uses upstream's `ENABLE_TESTS` option, so `%check` executes the registered KFR CTest suite rather than an empty test discovery pass. The runtime output directory is absolute because upstream declares test executables from a CMake subdirectory while its CTest registrations refer to the project-level `bin` directory.

Release 6 retains both registered upstream CTest executables, including KFR's
performance coverage, and gives the QEMU-user build 90 minutes. A trusted
Release 5 run compiled and installed the package successfully but reached the
60-minute package deadline only after the first test executable had started.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
