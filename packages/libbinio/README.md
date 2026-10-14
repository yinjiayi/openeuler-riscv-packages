<!-- SPDX-License-Identifier: Apache-2.0 -->
# libbinio

This directory packages upstream `https://github.com/adplug/libbinio` version `1.5` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The official stable tag `libbinio-1.5` pins commit
`020a4c2b7612863600428e0e9f2491b923e54ac2`. Source0's full SHA-256 is
`d4454ee76a6c711e1e46b4b61da5cc168c520c145902719e00f1261fe657164f`.
All 40 original Git files match the fixed official archive. No source patch
or substituted external recipe is used. The historical AUR `libbinio 1.5-1`
row is discovery lineage, not source or license authority.

The library is LGPL-2.1-or-later. `LicenseRef-Ken-Turkowski` denotes the
literal permission and warranty notice in `src/binio.cpp` lines 451–470,
preserved verbatim as `COPYING-KEN-TURKOWSKI`. The manual is GFDL-1.1-or-later
with no Invariant Sections but with its original Front-Cover and Back-Cover
Texts. Full license, authorship, unchanged manual, FDL and generated version
source accompany the compiled Info manual; no claim of the GFDL
no-cover-text variant is made. The stale discovery GPL label is not copied.

Default string, iostream, ISO-library and math detection are preserved;
shared/static libraries, headers, pkg-config and Info documentation ship.
`autoreconf --force --install`, upstream configure with maintainer mode,
`make`, `make install`, and original `make check` run in target CI. Upstream
defines no unit `TESTS`, so its empty default check is not claimed as a
functional suite. The separately labeled packaging-owned C++ checks cover
wire endian values, peeking, IEEE single conversion, C/std strings, bounded
memory and error state, iostream wrappers, and file access. The identical
source is compiled against source, staged, and RPM-installed libraries.
Installed checks require RPM ownership/integrity and linkage to the exact
installed SONAME; there is no upstream source fallback.

Build dependencies are supplied by the audited target repositories. Devel
requires `gcc-c++` and `pkgconf` for its installed verification. Supplier
and namespace metadata review does not prove a DNF transaction; actual
build/install/default/downstream execution and physical RPM/SRPM validation
remain target CI gates. No local RPM/QEMU build, native hardware validation,
timing/performance, merge or public publication result is asserted here.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
