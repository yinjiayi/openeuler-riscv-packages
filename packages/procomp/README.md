<!-- SPDX-License-Identifier: Apache-2.0 -->
# procomp

This directory packages upstream `https://github.com/yusufprompt/procomp` version `0.2.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Packaging release 2 passes the RPM macro build directory explicitly to CMake so the configure, build, install, and test phases share the same out-of-tree build.
