<!-- SPDX-License-Identifier: Apache-2.0 -->
# utf8proc

This directory packages utf8proc `2.11.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source; Arch stable, Debian stable, openSUSE Tumbleweed, and metadata-only AUR lineage corroborated the same official stable component. The upstream tag archive is pinned by SHA-256.

No Fedora spec, PKGBUILD, or AUR content was executed. Unicode `17.0.0` normalization and grapheme-break conformance files are separately pinned as official test dependencies. The downstream-only patch replaces upstream CMake downloads with explicit verified file paths, keeping the full test suite while enforcing a network-free build.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
