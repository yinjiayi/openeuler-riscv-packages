<!-- SPDX-License-Identifier: Apache-2.0 -->
# libpipeline

This directory packages upstream libpipeline `1.5.8` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source; Arch stable, Debian stable, openSUSE Tumbleweed, and Ubuntu GA corroborated the same upstream component. The official Savannah release archive is pinned by SHA-256.

The frozen AUR metadata contained no exact-name `libpipeline` entry. No AUR recipe or external distribution build script was read or executed. The build is network-free after source verification and runs the upstream Check-based test suite plus an installed-library compile-and-run smoke test.

External source licenses remain those of the upstream project. The repository license covers only original packaging metadata, scripts, and documentation.
