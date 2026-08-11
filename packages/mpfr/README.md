<!-- SPDX-License-Identifier: Apache-2.0 -->
# mpfr

This directory packages MPFR `4.2.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source; Arch stable, Debian stable, openSUSE Tumbleweed, and metadata-only AUR lineage corroborated the same official stable release. The official MPFR archive is pinned by SHA-256.

No Fedora spec, PKGBUILD, or AUR content was executed. The network-free build retains the complete upstream arithmetic test suite and an installed correctly-rounded square-root smoke test. The package license records both the LGPL-covered library and GFDL-covered reference manual.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
