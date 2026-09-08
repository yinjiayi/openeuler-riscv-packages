<!-- SPDX-License-Identifier: Apache-2.0 -->
# gperf

This directory packages GNU gperf `3.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority distribution lineage and still carried `3.2.1`; Arch stable, openSUSE Tumbleweed, and Ubuntu 26.04 LTS GA corroborated upstream `3.3`, while Debian stable also retained `3.2.1`. The official GNU stable archive is pinned by SHA-256.

Arch stable and AUR RPC metadata were recorded. The AUR result is a VCS package and is not trusted as source. No AUR recipe, Fedora spec, or other distribution build script is executed. Unlike the Fedora 44 spec, this package keeps the complete upstream `make check` target mandatory; the installed smoke test generates C lookup code, compiles it, and exercises the generated lookup function.

External source licenses remain those of the upstream project. The repository license covers only original packaging metadata, scripts, and documentation.
