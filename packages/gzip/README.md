<!-- SPDX-License-Identifier: Apache-2.0 -->
# gzip

This directory packages upstream GNU gzip `1.14` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44, Arch stable, openSUSE Tumbleweed, and Ubuntu GA carry the same upstream stable release; Debian stable corroborates the component at `1.13`. The official GNU stable-release archive is pinned by SHA-256.

The frozen AUR metadata contained no exact-name `gzip` entry. No AUR recipe or external distribution build script was read or executed. The build is network-free after source verification, runs the complete upstream `make check` suite, and verifies installed compression, integrity checking, decompression, and `zgrep` behavior.

External source licenses remain those of the upstream project. The repository license covers only original packaging metadata, scripts, and documentation.
