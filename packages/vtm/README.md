<!-- SPDX-License-Identifier: Apache-2.0 -->
# vtm

This directory packages upstream `https://github.com/directvt/vtm` version `2026.07.30` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The 240-minute package budget covers the large single-translation-unit C++ build under qemu-user while preserving upstream CTest discovery. Because upstream currently registers no CTest cases, both `%check` and the installed-RPM smoke test also execute `vtm --version` and require the packaged version.
