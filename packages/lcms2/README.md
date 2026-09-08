<!-- SPDX-License-Identifier: Apache-2.0 -->
# lcms2

This directory packages Little CMS `2.19.1` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official GitHub release asset is SHA-256 pinned, matches
the digest published in upstream asset metadata, and passed archive-safety
inspection. Arch stable and openSUSE Tumbleweed confirm 2.19.1; Fedora 44,
Debian stable, and Ubuntu 26.04 LTS GA carried older stable releases. This is
an intentional official-stable forward release.

AUR was queried through RPC only. Its matching `lcms2-git` row is both
VCS-only and older than 730 days, so it was excluded as a source; no PKGBUILD
or distribution spec was executed. The GPL-3.0-or-later plugin source remains
in the official archive but the fast-float and threaded plugins are not built
or shipped; the conservative RPM license expression records both MIT and GPL
material. JPEG, TIFF, utilities, and the complete upstream Meson testbed are
enabled. Installed smoke links and runs a public-API consumer without network.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
