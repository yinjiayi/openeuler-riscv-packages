<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdeflate

This directory packages libdeflate 1.25 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. It builds the shared library and gzip-compatible tools, compares behavior with target `zlib-devel` in the upstream tests, and performs an installed CLI round trip.

The immutable discovery record corroborates the component across Arch stable, AUR metadata, Debian stable, Fedora GA, openSUSE Tumbleweed, and Ubuntu GA. The exact official release asset is pinned by SHA-256, which also matched GitHub's publisher digest; no AUR recipe is used.

The upstream MIT license governs fetched source. Apache-2.0 covers only this repository's original packaging material.
