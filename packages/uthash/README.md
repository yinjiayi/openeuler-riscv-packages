<!-- SPDX-License-Identifier: Apache-2.0 -->
# uthash

This directory packages uthash `2.3.0` headers for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source; Arch stable, Debian stable, openSUSE Tumbleweed, and Ubuntu GA corroborated the same official release. The official tag archive is pinned by SHA-256 and its sole archive symlink was verified to be a safe internal `include -> src` link.

No external distribution recipe or AUR content was executed. All 96 upstream C test programs are compiled and run before an installed-header hash-table smoke test; no build-time network access is used.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
