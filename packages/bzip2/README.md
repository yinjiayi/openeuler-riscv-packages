<!-- SPDX-License-Identifier: Apache-2.0 -->
# bzip2

This directory packages upstream bzip2 `1.0.8` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source; Arch stable, Debian stable, openSUSE Tumbleweed, and Ubuntu GA independently corroborated the same upstream release. The official Sourceware archive is pinned by SHA-256.

No external distribution recipe or AUR content was executed. The build is network-free after source verification and runs upstream's compression test suite plus an installed-library smoke test.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
