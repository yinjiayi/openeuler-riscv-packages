<!-- SPDX-License-Identifier: Apache-2.0 -->
# sysinfoviewer

This directory packages upstream `https://github.com/Magpiny/sysinfoviewer` version `0.3.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Packaging release 2 accepts the CMake 3.27 version shipped by the target repository and declares the wxWidgets, libcurl, ALSA, libdrm, and pkg-config development dependencies required by upstream. Upstream registers no CTest tests; the package therefore does not claim functional test coverage from its empty CTest invocation.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
