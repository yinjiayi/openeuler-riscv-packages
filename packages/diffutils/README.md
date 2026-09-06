<!-- SPDX-License-Identifier: Apache-2.0 -->
# diffutils

This directory packages upstream GNU diffutils `3.12` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44, Arch stable, openSUSE Tumbleweed, and Ubuntu GA carry `3.12`; Debian stable corroborates the same component at `3.10`. The official GNU stable-release archive is pinned by SHA-256.

The frozen AUR metadata contained no exact-name `diffutils` entry. No AUR recipe or external distribution build script was read or executed. The build is network-free after source verification, runs the complete upstream `make check` suite, and verifies the installed `cmp` and `diff` behavior.

External source licenses remain those of the upstream project. The repository license covers only original packaging metadata, scripts, and documentation.
