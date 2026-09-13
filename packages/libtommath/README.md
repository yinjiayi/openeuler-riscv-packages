<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtommath

This directory packages LibTomMath `1.3.0` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official versioned release asset is SHA-256 pinned, its
digest is corroborated by GitHub's release metadata, and the archive passed
single-root, path, link, and special-entry safety inspection. Arch stable,
openSUSE Tumbleweed, Debian stable, and Ubuntu 26.04 LTS GA confirm 1.3.0.

Fedora 44's frozen row was `1.3.1~rc1`, which is a prerelease and therefore
was recorded for lineage but excluded as a stable version authority. AUR was
queried through RPC only; its `libtommath-git` row is VCS-only, out of date,
and older than 730 days. No PKGBUILD or distribution spec was executed. The
build keeps the complete upstream `test-ltm` suite, and installed smoke
compiles and runs a public multiple-precision arithmetic API consumer without
network access.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
