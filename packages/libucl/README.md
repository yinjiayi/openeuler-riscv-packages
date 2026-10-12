<!-- SPDX-License-Identifier: Apache-2.0 -->
# libucl

This directory packages libucl `0.9.4` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. GitHub marks `0.9.4` as the publisher's current stable
release. Its immutable tag archive is SHA-256 pinned, has one archive root,
and contains no unsafe path, link, or special member. `COPYING` establishes
the BSD-2-Clause license.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` records the
same component in AUR metadata and Fedora 44 GA. The same frozen Arch extra,
Debian stable, openSUSE Tumbleweed, and Ubuntu 26.04 LTS GA indexes have no
matching Vsevolod Stakhov libucl source package. Read-only AUR RPC reports
`libucl` `0.9.2-1`; no AUR or distribution recipe was read or executed.

The openEuler 24.03 LTS SP3 RVA23 repository has no existing `libucl` package
or `libucl.so.0` provider, so `0.9.4-1` introduces no lower EVR or SONAME
replacement. The dependency closure uses only fixed-target `cmake`, GCC C/C++,
and `make`. `%check` runs all five upstream CTest entries with no downstream
exclusion. Installed smoke parses UCL through both the utility and public C
API.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
