<!-- SPDX-License-Identifier: Apache-2.0 -->
# libpsl

This directory packages libpsl `0.23.1` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official versioned release asset is independently
SHA-256 pinned and passed single-root, path, link, and special-entry safety
inspection. openSUSE Tumbleweed confirms 0.23.1; Arch stable, Fedora 44 GA,
Debian stable, and Ubuntu 26.04 LTS GA retained older stable releases. This is
an intentional official-stable forward release.

AUR was queried through RPC only. Its matching `libpsl-git` row is VCS-only
and older than 730 days, so it was excluded as a source; no PKGBUILD or
distribution spec was executed. The official archive includes the Public
Suffix List used to generate built-in DAFSA data offline. The build binds to
the fixed target's libidn2 and libunistring and keeps the complete upstream
Meson test suite. Installed smoke exercises the CLI, built-in list, and public
libpsl API without network access.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
