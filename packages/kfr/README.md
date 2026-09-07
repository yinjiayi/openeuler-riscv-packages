<!-- SPDX-License-Identifier: Apache-2.0 -->
# kfr

This directory packages upstream `https://github.com/kfrlib/kfr` version `7.0.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 2 follows upstream's supported RISC-V build path: Clang compiles the RVV backend with `-march=rv64gcv` and `KFR_ARCH=rvv`. The package uses upstream's `ENABLE_TESTS` option, so `%check` executes the registered KFR CTest suite rather than an empty test discovery pass.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
