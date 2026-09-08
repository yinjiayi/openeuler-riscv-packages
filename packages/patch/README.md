<!-- SPDX-License-Identifier: Apache-2.0 -->
# patch

This directory packages GNU patch `2.8` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority distribution lineage, and Arch stable, Debian stable, openSUSE Tumbleweed, and Ubuntu 26.04 LTS GA corroborated the same stable component. The official GNU archive is pinned by SHA-256.

Arch stable and AUR RPC metadata were recorded. The AUR result was a stale VCS entry and was excluded as source. No AUR recipe, Fedora spec, or other distribution build script is executed. The build is network-free, retains upstream extended-attribute support, runs the complete upstream test suite, and then applies a real unified diff in the installed smoke test.

External source licenses remain those of the upstream project. The repository license covers only original packaging metadata, scripts, and documentation.
