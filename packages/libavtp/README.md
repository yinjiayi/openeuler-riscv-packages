<!-- SPDX-License-Identifier: Apache-2.0 -->
# libavtp

This directory packages libavtp `0.2.0` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The immutable official stable tag archive is SHA-256
pinned, single-rooted, and free of unsafe paths, links, and special members.
The source and public headers carry the BSD-3-Clause license.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` corroborates
the same version across Arch extra, Fedora 44 GA, Debian stable, openSUSE
Tumbleweed, and Ubuntu 26.04 LTS GA. Read-only AUR RPC found no exact
`libavtp` package. No AUR PKGBUILD or distribution recipe was read or
executed.

The fixed openEuler RVA23 metadata has no existing `libavtp` package or
`libavtp.so.0` provider. `%check` forces tests on and executes all seven
maintained CMocka programs covering the common, stream, AAF, CRF, CVF, RVF,
and IEC61883/IIDC APIs without exclusions. Installed smoke compiles and runs
a public PDU field round trip through pkg-config.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
