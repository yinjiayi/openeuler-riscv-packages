<!-- SPDX-License-Identifier: Apache-2.0 -->
# semver-cpp

This directory packages upstream `https://github.com/Neargye/semver` version `1.0.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Packaging release 3 selects the verified `semver-1.0.0` top-level directory, uses an explicit CMake build directory, enables the bundled doctest suite for CTest, and disables the automatic debuginfo subpackage because the installed payload is header-only.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
