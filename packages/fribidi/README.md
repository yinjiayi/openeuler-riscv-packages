<!-- SPDX-License-Identifier: Apache-2.0 -->
# fribidi

This directory packages FriBidi `1.0.16` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official versioned release asset is independently
SHA-256 pinned and passed single-root, path, link, and special-entry safety
inspection. Arch stable, Fedora 44 GA, openSUSE Tumbleweed, Debian stable, and
Ubuntu 26.04 LTS GA all confirm the 1.0.16 stable release line.

AUR was queried through RPC only. Its matching `fribidi-git` row is VCS-only
and older than 730 days, so it was excluded as a source; no PKGBUILD or
distribution spec was executed. The official tarball contains the generated
Unicode tables and API manual pages, so the build needs no network access or
documentation generator. The complete upstream Meson suite remains enabled.
Installed smoke exercises both the CLI and public FriBidi API.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
