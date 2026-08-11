<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmd

This directory packages libmd `1.2.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 supplied the priority component identity at `1.1.0`; Arch stable, openSUSE Tumbleweed, and the official upstream release index established `1.2.0`, so the resolver selected the newer stable release instead of regressing. Debian stable, Ubuntu GA, and metadata-only AUR lineage were retained for traceability.

No Fedora spec, PKGBUILD, or AUR content was executed. The official archive is pinned by SHA-256, upstream tests remain mandatory, and an installed MD5 API smoke test runs without network access.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
