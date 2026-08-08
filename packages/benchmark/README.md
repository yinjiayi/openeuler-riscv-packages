<!-- SPDX-License-Identifier: Apache-2.0 -->
# benchmark

This directory packages Google Benchmark 1.9.5 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The SPEC disables all dependency downloads, uses the target's `gtest-devel`, and retains the complete upstream test suite.

The immutable discovery record corroborates the component across Arch stable, AUR metadata, Debian stable, Fedora GA, openSUSE Tumbleweed, and Ubuntu GA. Only the inspected official stable archive and pinned SHA-256 are trusted; no AUR recipe is executed.

Meaningful acceptance depends on timing and performance behavior. The package is therefore routed as `needs-native-riscv` and must remain unmerged until a separately approved native RISC-V runner can build and run its tests. QEMU results must not be presented as native benchmark validation.

The upstream Apache-2.0 license governs fetched source and this repository's original packaging material.
