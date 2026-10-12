<!-- SPDX-License-Identifier: Apache-2.0 -->
# gflags

This directory packages gflags 2.2.2 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The requested release matches the frozen distribution cohort;
upstream 2.3.1 is recorded separately as the latest detected stable release.

The source is GitHub's archive of the official annotated `v2.2.2` tag, whose
peeled commit is `e171aa2d15ed9eb17054558e0b3a6a413bb01067`. Its SHA-256 and
BSD-3-Clause license were independently verified. The discovery lineage covers
Arch, AUR metadata, Debian, Fedora 44, openSUSE Tumbleweed, and Ubuntu. No
external distribution recipe was read or executed.

A **selective CMake initializer** is a temporary `%check`-only file inherited
by upstream's nested CMake test projects. It enables the release's documented
`GFLAGS_USE_TARGET_NAMESPACE` option only for the `cmake_config` consumer,
whose own test links `gflags::gflags`. It does not modify or install upstream
source and leaves the negative-compilation consumers on their intended
non-namespaced targets.

All 57 upstream CTest cases remain enabled, including configuration and
negative-compilation tests. The installed smoke test compiles and runs a real
consumer through the installed header, shared library, and pkg-config metadata.
Apache-2.0 covers only this repository's original packaging files.
