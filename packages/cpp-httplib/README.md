<!-- SPDX-License-Identifier: Apache-2.0 -->
# cpp-httplib

This directory packages cpp-httplib 0.59.0-1 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. It retains the deterministic dependency-free header-only variant and CMake metadata. `%check` compiles and runs the upstream in-process server/client example over loopback; no external network is used. The installed smoke test checks the exact 0.59.0 header version and presence of the CMake configuration.

The immutable discovery record corroborates the component across Arch stable, AUR metadata, Debian stable, Fedora GA, openSUSE Tumbleweed, and Ubuntu GA. The checksum-pinned official upstream 0.59.0 archive supersedes the older distribution observations. No AUR content is trusted or executed.

The existing recipe keeps `HTTPLIB_TEST`, compiled-library mode, TLS backends and compression variants disabled. The retained loopback example is a functional package check, not execution of the comprehensive upstream test suite or validation of those optional features. This version-consistency repair does not change those selections or claim native RISC-V, timing, performance or production-network acceptance. Target build and installed-product results still require current-head CI evidence.

The upstream MIT license governs the installed header and example code. The unchanged fetched archive also retains third-party Google BSD test notices and a Mozilla-origin certificate fixture; it is not asserted to contain exclusively MIT material. Apache-2.0 covers only this repository's original packaging material.
