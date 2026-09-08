<!-- SPDX-License-Identifier: Apache-2.0 -->
# libbsd

This directory packages libbsd `0.12.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source, with Arch stable, Debian stable, openSUSE Tumbleweed, and Ubuntu GA corroborating the same official stable component. The freedesktop.org release archive is pinned by SHA-256.

No external distribution recipe or AUR content was executed. The package retains upstream tests and validates an installed BSD string API against the separately packaged `libmd` dependency, all without build-time network access.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
