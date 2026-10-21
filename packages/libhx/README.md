<!-- SPDX-License-Identifier: Apache-2.0 -->
# libHX

This directory packages the real RPM component `libHX` `5.4` for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The lower-case directory ID `libhx` follows
the repository schema; it does not rename the case-sensitive RPM, pkg-config
module, shared library, or upstream project.

The upstream project page identifies `5.4` (2026-03-25) as the latest stable
release and links both the official immutable archive and the Codeberg source
repository. The release archive is SHA-256 pinned here. It has one archive
root, no links or special members, and no unsafe or escaping paths. Upstream
`COPYING` licenses libHX under LGPL-2.1-or-later; the source release also
contains GPL-licensed generated build helpers reflected in the source license
expression.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` corroborates the
component through Arch extra, Fedora 44 GA, Debian stable, openSUSE Tumbleweed,
and Ubuntu 26.04 LTS GA metadata. Read-only AUR RPC returned no exact `libhx`
package. No AUR or distribution build recipe was read or executed.

The complete upstream `make check` build compiles all 38 declared C and C++
check programs and runs all seven registered tests: seven pass with zero skip,
XFAIL, fail, XPASS, or error. Packaging removes no test and adds no weak pass.
Installed smoke checks both RPMs and pkg-config version `5.4`, then compiles
and runs a public `HX_strdup` C API consumer.

The fixed openEuler 24.03 LTS SP3 RVA23 repository contains every declared
BuildRequires. It has no existing `libHX` package or `libHX.so.43` provider, so
`5.4-1` introduces neither a lower EVR nor a SONAME replacement. The official
build reports pkg-config version `5.4` and SONAME `libHX.so.43`.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test script, and documentation in this directory.
