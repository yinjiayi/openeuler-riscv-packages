<!-- SPDX-License-Identifier: Apache-2.0 -->
# ed

This directory packages upstream GNU ed `1.22.5` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44, Arch stable, and openSUSE Tumbleweed carry `1.22.5`; Debian stable and Ubuntu GA corroborate the same component at earlier stable releases. The official GNU lzip archive is pinned by SHA-256.

The frozen AUR metadata contained no exact-name `ed` entry. No AUR recipe or external distribution build script was read or executed. The build is network-free after source verification, runs upstream's `make check`, and edits and verifies a file with the installed binary.

External source licenses remain those of the upstream project. The repository license covers only original packaging metadata, scripts, and documentation.
