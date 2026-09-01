<!-- SPDX-License-Identifier: Apache-2.0 -->
# vncmanager

This directory packages upstream `https://github.com/openSUSE/vncmanager` version `1.0.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The SPEC configures an explicit out-of-source CMake directory and reuses it for build, install, and the retained CTest check. Upstream 1.0.2 defines the executable and install rules but does not define test cases.

The downstream MIT patch adds the standard `<cstdint>` include required for
the source's direct `uint8_t` use with GCC 14. It changes no runtime behavior.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
