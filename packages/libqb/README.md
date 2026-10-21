<!-- SPDX-License-Identifier: Apache-2.0 -->
# libqb

This directory packages libqb `2.0.10` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The publisher's current stable release asset is SHA-256
pinned, single-rooted, and free of unsafe paths, links, and special members.
The library is LGPL-2.1-or-later.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` cross-checks
Arch extra, Fedora 44 GA, Debian stable, openSUSE Tumbleweed, and Ubuntu
26.04 LTS GA. Read-only AUR RPC found no exact `libqb` package. No AUR
PKGBUILD or distribution recipe was read or executed.

Version `2.0.10-1` exceeds openEuler's existing `2.0.8-6` while preserving
`libqb.so.100` for all target consumers and retaining the `libqb`,
`libqb-devel`, `libqb-help`, and `doxygen2man` package topology.
`%check` enables the slow checks and runs all 12 canonical Automake tests;
the observed summary was 12 pass with no skip, XFAIL, failure, XPASS, or
error. Installed smoke compiles and runs array allocation through the public
pkg-config API and verifies the library version object.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
