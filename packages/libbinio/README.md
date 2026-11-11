<!-- SPDX-License-Identifier: Apache-2.0 -->
# libbinio

This directory packages upstream `https://github.com/adplug/libbinio` version `1.5` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The official stable tag `libbinio-1.5` pins commit
`020a4c2b7612863600428e0e9f2491b923e54ac2`. Source0's full SHA-256 is
`d4454ee76a6c711e1e46b4b61da5cc168c520c145902719e00f1261fe657164f`.
All 40 original Git files match the fixed official archive. One documented
downstream lifetime patch is applied; no external recipe is substituted.
The historical AUR `libbinio 1.5-1`
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

Repair provenance: exact head `6a384f55e0c42e80cbeebed31f24c23a9501ff24`,
Package CI run `38646644683` attempt 1, failed `%check` at
`FAIL: ieee-single-bytes`. The source declares float conversion storage
inside a branch but dereferences its pointer after that scope ends. Patch
`0001-keep-float-storage-alive-until-byte-write.patch` moves the float,
double and manual-byte storage into the enclosing IEEE block. This is a
generic upstream C++ lifetime defect, not a demonstrated RISC-V-specific
or QEMU fault. It preserves normal optimization, all 35 downstream checks,
original empty `make check`, features and license text. Source line count
is unchanged, preserving exact Ken Turkowski notice extraction. The same
real build log proves original installed headers use `/usr/include/libbinio`;
the staged compiler, payload manifest and installed smoke now match it.
Applicable source is fixed upstream 1.5; remove the patch once a verified
official release contains the equivalent fix. No upstream submission or
acceptance is claimed. Replacement target CI, RPM/SRPM and install proof
are required before calling this repaired head successful.

The replacement head `3bb5a819474a29cc5adfd9fc6b10e2a888633094`
passed the build phase in run `38650705469` attempt 1, but its installed
smoke stopped after the loader reported `/lib64/lp64d/libbinio.so.1`.
The old assertion compared that spelling to a literal `/usr/lib64` path.
Installed smoke now resolves both the loader path and expected SONAME to
the same canonical file, and rechecks that file's libbinio RPM ownership.
It still rejects any other library, retains RPM integrity and all 35 checks,
and does not claim the observed alias was already proved equivalent.
Only new-head target smoke can establish that equivalence and execute the
installed functional suite; old-head build success is not full acceptance.

Build dependencies are supplied by the audited target repositories. Devel
requires `gcc-c++` and `pkgconf` for its installed verification. Supplier
and namespace metadata review does not prove a DNF transaction; actual
build/install/default/downstream execution and physical RPM/SRPM validation
remain target CI gates. No local RPM/QEMU build, native hardware validation,
timing/performance, merge or public publication result is asserted here.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
