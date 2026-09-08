<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtsm

This directory packages libtsm `4.7.0` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. GitHub marks `v4.7.0` as the publisher's current stable
release. Its immutable tag archive is SHA-256 pinned, has one archive root,
and contains no unsafe path, link, or special member. `COPYING` and
`LICENSE_htable` establish the MIT and LGPL-2.1-or-later terms.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` records this
component in Arch extra, Fedora 44 GA, and openSUSE Tumbleweed. Debian stable
records the earlier Aetf lineage, while Ubuntu 26.04 LTS GA records the same
source name without an upstream URL; both are retained as frozen lineage and
not treated as release-source proof. Read-only AUR RPC found no exact package.
No AUR or distribution recipe was read or executed.

The openEuler 24.03 LTS SP3 RVA23 repository has no existing `libtsm` package
or `libtsm.so.4` provider, so `4.7.0-1` introduces no lower EVR or SONAME
replacement. Its fixed dependency closure includes the Check framework and
libxkbcommon used by the complete upstream suite. `%check` runs all seven
declared Meson tests with no downstream exclusion. Installed smoke compiles
and runs a public screen-API consumer through pkg-config.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
