<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmpc

This directory packages GNU MPC `1.4.1` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official GNU release archive is SHA-256 pinned and passed
single-root, path, link, and special-entry safety inspection. The immutable
discovery snapshot records Arch `1.4.1-1`, AUR MinGW `1.4.0-1`, Debian
`1.3.1-1`, Fedora 44 GA `1.4.0-1.fc44`, openSUSE Tumbleweed `1.4.1-1.4`, and
Ubuntu GA `1.3.1-3`.

The AUR record is cross-target metadata only; no PKGBUILD or distribution spec
was read or executed. The complete upstream arithmetic suite remains enabled
against openEuler's GMP and MPFR development libraries. Installed smoke links
the public API and verifies an exact complex value.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
