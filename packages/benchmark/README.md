<!-- SPDX-License-Identifier: Apache-2.0 -->
# benchmark

This directory packages Google Benchmark 1.9.5 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The SPEC disables all dependency downloads, uses the target's `gtest-devel`, and retains the complete upstream test suite.

The immutable discovery record corroborates the component across Arch stable, AUR metadata, Debian stable, Fedora GA, openSUSE Tumbleweed, and Ubuntu GA. Only the inspected official stable archive and pinned SHA-256 are trusted; no AUR recipe is executed.

The official Fedora 44 `google-benchmark` dist-git SPEC was retrieved as read-only reference evidence on 2026-08-11 (SHA-256 `a6b6118bf5603b5099f4f5fc45d6c1e0fd8bae518a01a1b9f29d36f5ee8f2bad`). It corroborates upstream version `1.9.5`, system GoogleTest, disabled dependency downloads, disabled assembly tests, and explicit `GIT_VERSION`. The Fedora SPEC and its patches were not executed or treated as trusted commands.

The official upstream archive `benchmark-1.9.5.tar.gz` independently verifies as SHA-256 `9631341c82bac4a288bef951f8b26b41f69021794184ece969f8473977eaa340`. The installed-package smoke test compiles, links, and runs one minimal benchmark through the public API; it does not assert a performance number.

Meaningful acceptance depends on timing and performance behavior. The package is therefore routed as `needs-native-riscv` and must remain unmerged until a separately approved native RISC-V runner can build and run its tests. QEMU results must not be presented as native benchmark validation.

The upstream Apache-2.0 license governs fetched source and this repository's original packaging material.
