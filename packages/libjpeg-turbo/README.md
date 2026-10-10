<!-- SPDX-License-Identifier: Apache-2.0 -->
# libjpeg-turbo

This directory packages libjpeg-turbo `3.2.0` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official release asset is SHA-256 pinned, its digest is
corroborated by GitHub's release metadata, and the archive passed single-root,
path, link, and special-entry safety inspection. Arch stable confirms 3.2.0;
Fedora 44, openSUSE Tumbleweed, Debian stable, and Ubuntu 26.04 LTS GA carried
older stable lines, making this an intentional official-stable forward release.

AUR was queried through RPC only. The matching `libjpeg-turbo-git` row is
VCS-only and was excluded as source evidence; no PKGBUILD or distribution spec
was executed. The build enables shared libjpeg, TurboJPEG, RISC-V SIMD, tools,
and the complete upstream regression suite. The Fedora-proven `fp-contract`
floating-point mode is selected for RISC-V while every check still runs.
Installed smoke performs a PPM-to-JPEG round trip and compiles a public
TurboJPEG API consumer without network access.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
