<!-- SPDX-License-Identifier: Apache-2.0 -->
# libpng

This directory packages libpng `1.6.58` (RPM epoch `2`) for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44, Arch stable, and openSUSE Tumbleweed corroborated the same release; Debian stable and Ubuntu 26.04 LTS GA retained older `1.6.x` releases when frozen. Upstream describes `1.6.58` as a production release, and the official SourceForge archive is pinned by SHA-256.

Only AUR RPC metadata was inspected; no PKGBUILD, Fedora spec, or other distribution build script is executed. The build is network-free and does not disable upstream RISC-V Vector detection: on the fixed `riscv64`/RVA23 toolchain, supported RVV code is built and exercised by the complete serial upstream check target. The installed smoke test compiles and runs a consumer against the packaged libpng and zlib interfaces.

External source licenses remain those of the upstream project. The repository license covers only original packaging metadata, scripts, and documentation.
