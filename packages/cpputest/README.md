<!-- SPDX-License-Identifier: Apache-2.0 -->
# cpputest

This directory packages CppUTest 4.0 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Version 4.0 is the highest numeric stable upstream tag;
upstream's moving `latest-passing-build` release is deliberately not treated
as a stable versioned release. The immutable `v4.0` archive is pinned by its
locally calculated SHA-256 in `sources.yaml`.

Frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
records Arch Extra `4.0-6`, Debian stable `4.0-3`, Fedora 44
`4.0-15.fc44`, and Ubuntu Resolute `4.0-3build1`. Distribution metadata was
used only as lineage evidence; no distribution recipe was read or executed.

`%check` enables the complete upstream CMake test gate and runs every
platform-selected test group serially. Grouped mode is upstream's default and
still executes every self-test; serial execution isolates the deliberate
signal/crash checks under RISC-V user-mode emulation. The installed smoke test
compiles and runs a real CppUTest test against the installed library.

External source licenses remain upstream's BSD-3-Clause terms. Apache-2.0
covers only this repository's original packaging metadata and scripts.
