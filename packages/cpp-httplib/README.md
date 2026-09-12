<!-- SPDX-License-Identifier: Apache-2.0 -->
# cpp-httplib

This directory packages cpp-httplib 0.56.0 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. It installs the deterministic dependency-free header-only variant and CMake metadata. `%check` compiles and runs the upstream in-process server/client example over loopback; no external network is used. Installed smoke verifies that the header version matches the installed RPM version and that the CMake metadata exists.

The immutable discovery record corroborates the component across Arch stable, AUR metadata, Debian stable, Fedora GA, openSUSE Tumbleweed, and Ubuntu GA. Official upstream 0.56.0 supersedes the older distribution observations. No AUR content is trusted or executed.

The upstream MIT license governs fetched source. Apache-2.0 covers only this repository's original packaging material.
