<!-- SPDX-License-Identifier: Apache-2.0 -->
# cpp-httplib

This directory packages cpp-httplib 0.60.1-1 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. It installs the deterministic dependency-free header-only variant and CMake metadata. `%check` compiles and runs the upstream in-process server/client example over loopback; no external network is used. This example check is not the complete upstream test suite. The installed smoke check requires the package query, the literal 0.60.1 header version, and installed CMake configuration to succeed.

The immutable discovery record corroborates the component across Arch stable, AUR metadata, Debian stable, Fedora GA, openSUSE Tumbleweed, and Ubuntu GA. Official upstream 0.60.1 supersedes the older distribution observations. No AUR content is trusted or executed.

PR #2489's hosted run 37926843504 at commit f97819a6ca18afcb427991a09d2579554f03e31e built the pinned 0.60.1-1 RPM and passed the existing example check. DNF installation succeeded, but the smoke check still required the old 0.54.1 header version and exited 1. The repair updates that literal assertion, synchronizes this description, and aligns metadata release 1 with the unchanged SPEC. Source pins, SPEC checks, package/CMake checks, and feature selection remain unchanged. Successful validation of the repair requires new exact-commit hosted CI and actual installation evidence; the old failed run is not evidence of repaired success or publication.

The upstream MIT license governs fetched source. Apache-2.0 covers only this repository's original packaging material.
