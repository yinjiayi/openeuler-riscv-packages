<!-- SPDX-License-Identifier: Apache-2.0 -->
# argparse

This directory packages upstream argparse 3.2 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. It installs the C++17 header, CMake metadata, and pkg-config metadata, and runs the bundled doctest-based upstream suite during `%check`.

The immutable discovery record corroborates the component across Arch stable, AUR metadata, Debian stable, Fedora GA, openSUSE Tumbleweed, and Ubuntu GA. Only the inspected official release archive and pinned SHA-256 are build inputs; AUR remains untrusted metadata lineage.

The upstream MIT license governs fetched source. Apache-2.0 covers only this repository's original packaging material.
