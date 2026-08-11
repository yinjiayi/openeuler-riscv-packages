<!-- SPDX-License-Identifier: Apache-2.0 -->
# lzo

This directory packages LZO `2.10` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source; Arch stable, Debian stable, openSUSE Tumbleweed, Ubuntu GA, and metadata-only AUR lineage corroborated the same official release. The upstream archive is pinned by SHA-256.

No Fedora spec, PKGBUILD, or AUR content was executed. The shared-library build retains upstream checks and validates a full installed compression/decompression round trip without network access.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
