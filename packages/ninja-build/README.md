<!-- SPDX-License-Identifier: Apache-2.0 -->
# ninja-build

This directory packages Ninja `1.13.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source; Arch stable, Debian stable, openSUSE Tumbleweed, and metadata-only AUR lineage corroborated the same stable component. The official tag archive is pinned by SHA-256.

No Fedora spec, PKGBUILD, or AUR content was executed. Tests link against the openEuler `gtest-devel` package so CMake cannot fall back to its networked FetchContent path. The upstream test binary and an installed end-to-end Ninja build remain mandatory.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
