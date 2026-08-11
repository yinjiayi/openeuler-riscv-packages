<!-- SPDX-License-Identifier: Apache-2.0 -->
# range-v3

This directory packages upstream `https://github.com/ericniebler/range-v3` version `0.12.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The immutable discovery snapshot cross-checks Arch stable, AUR metadata, Debian stable, Fedora GA, and openSUSE Tumbleweed records. Only the official stable tag archive and independently calculated SHA-256 are build inputs; no AUR recipe or distribution build hook is read or executed.

The official Fedora 44 `range-v3` dist-git SPEC was retrieved as read-only reference evidence on 2026-08-11 (SHA-256 `e336938e92768b85895549a77c16132de0969f8111283b7333d4513bd15efda3`). It corroborates version `0.12.0`, the header-only payload, disabled CPU-native tuning/modules/examples/performance targets, and the installed `std/` header tree. The Fedora SPEC was not executed or copied as a trusted instruction source; this package retains the full upstream unit-test build and `%ctest` gate.

The official upstream archive `range-v3-0.12.0.tar.gz` independently verifies as SHA-256 `015adb2300a98edfceaf0725beec3337f542af4915cec4d0b89fa0886f4ba9cb`. The committed manifest pins that exact digest and the build runs without network after source acquisition.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
