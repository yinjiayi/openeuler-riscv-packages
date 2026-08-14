<!-- SPDX-License-Identifier: Apache-2.0 -->
# libogg

This directory packages libogg `1.3.6` (RPM epoch `2`) for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority distribution lineage; Arch stable, AUR RPC metadata, openSUSE Tumbleweed, and Ubuntu 26.04 LTS GA corroborated the same component, while Debian stable retained `1.3.5`. The official Xiph.org stable archive is pinned by SHA-256.

Only AUR RPC metadata was inspected; no PKGBUILD, Fedora spec, or other distribution build script is executed. The network-free build keeps the upstream bitwise and framing self-tests mandatory, and the installed smoke test compiles and runs a consumer against the packaged headers and shared library.

External source licenses remain those of the upstream project. The repository license covers only original packaging metadata, scripts, and documentation.
