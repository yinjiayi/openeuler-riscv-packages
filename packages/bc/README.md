<!-- SPDX-License-Identifier: Apache-2.0 -->
# bc

This directory packages upstream GNU bc `1.08.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44, Arch stable, and openSUSE Tumbleweed carry `1.08.2`; Debian stable and Ubuntu GA corroborate the same component at `1.07.1`. The official GNU stable-release archive is pinned by SHA-256.

The frozen AUR metadata contained no exact-name `bc` entry. No AUR recipe or external distribution build script was read or executed. The build is network-free after source verification, preserves upstream's check target, and exercises the freshly built and installed `bc` and `dc` calculators with deterministic arithmetic inputs.

External source licenses remain those of the upstream project. The repository license covers only original packaging metadata, scripts, and documentation.
