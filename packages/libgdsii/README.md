<!-- SPDX-License-Identifier: Apache-2.0 -->
# libgdsii

This directory packages upstream `https://github.com/HomerReid/libGDSII` version `0.21` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Official stable `v0.21` is fixed at `a6f6f2de4894075ed1bcf70d0542122781856c4e`.
The original source archive SHA-256 is
`0f0d9aacb5d3860dcecb2d04516d4044d9e3f35229c598560893a8d7634070bb`.
All 24 official Git blobs, including three symlink targets, match the archive.
Complete GPL2 LICENSE, COPYRIGHT and all five C++ implementation/header notices
grant GPL-2.0-or-later; this resolves the catalog's earlier unknown-license triage.
Debian/Ubuntu versions remain discovery lineage, not upstream source evidence.
No detached source signature or signed tag was observed.

Default static library, libtool `.la`, header, GDSIIConvert and unchanged
bend-flux example data are retained. No source or RISC-V algorithm patch is added.
Before autoreconf, `%prep` verifies the exact absolute COPYING/INSTALL symlink
targets, unlinks only those links without dereferencing them, copies the original
LICENSE into COPYING, and regenerates a regular INSTALL using target Automake.
The relative README link remains. One normal autoreconf/configure sequence
replaces the repeated symlink-mode autogen wrapper; source/build declarations
remain unchanged. The original generated metadata is additionally installed as
`libGDSII.pc`. Its Version deliberately stays `0.1` from AC_INIT, whereas the
official tag and RPM version are `0.21`. Automatic CLI debuginfo is retained.

Target GCC C++, Autoconf, Automake, Libtool, Make, pkgconf and normal RPM tools
provide build dependencies. No meep, scuff, GMSH execution or build-time network
is needed. Full official/published supplemental primary/filelists scans review
names, casefolded namespaces, all 13 non-debug installed paths and provider
closure. Non-EQ version constraints remain a target DNF/CI gate, not locally
solved or represented as a successful target build.

No TESTS/check_PROGRAMS/custom check target exists in the five original
Makefile.am files; default `make check` is nevertheless retained. Additional,
explicitly downstream checks verify the original 604-byte example (60 records),
original installed-header hash, seven layers, three boundaries, four zero-width
paths, one label, finite expected coordinates, cached APIs and point-in-polygon.
Two consumers use pkg-config and direct archive linking. CLI checks missing-input
rejection, raw/analyze output and GMSH's 22 points, 18 lines and three surfaces.
The same runner repeats after RPM installation and `rpm -V`. Logs and outputs
are private temporary files. These small functional checks are not security,
performance, memory, native-hardware or electromagnetic-simulation evidence.

Local validation is metadata, trusted-tooling tests/golden and source-only
verification. No local upstream/RPM/QEMU build is run. Hosted locked openEuler
24.03 LTS SP3 riscv64/RVA23 build/install plus independent physical RPM/SRPM
verification are still required before merge; pending CI is not success.
