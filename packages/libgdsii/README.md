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

Configured shared and static libraries, libtool `.la`, header, GDSIIConvert and unchanged
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
names, casefolded namespaces, shared SONAME/link/static/header/CLI/data paths and provider
closure. Non-EQ version constraints remain a target DNF/CI gate, not locally
solved or represented as a successful target build.

No TESTS/check_PROGRAMS/custom check target exists in the five original
Makefile.am files; default `make check` is nevertheless retained. Additional,
explicitly downstream checks verify the original 604-byte example (60 records),
original installed-header hash, seven layers, three boundaries, four zero-width
paths, one label, finite expected coordinates, cached APIs and point-in-polygon.
Two consumers use pkg-config/shared and direct archive linking. CLI checks missing-input
rejection, raw/analyze output and GMSH's 22 points, 18 lines and three surfaces.
The same runner repeats after RPM installation and `rpm -V`. Logs and outputs
are private temporary files. These small functional checks are not security,
performance, memory, native-hardware or electromagnetic-simulation evidence.

Local validation is metadata, trusted-tooling tests/golden and source-only
verification. No local upstream/RPM/QEMU build is run. Hosted locked openEuler
24.03 LTS SP3 riscv64/RVA23 build/install plus independent physical RPM/SRPM
verification are still required before merge; pending CI is not success.

Repair of exact head `5b83f8a083eaa80db21794120504e8623af15652`, failed
Package CI `38999421752`: the target's standard configure macro selected both
shared and static libraries, but the staged pkg-config consumer could not load
`libGDSII.so.0` from the uninstalled buildroot. This is a package recipe/loader
error, not a RISC-V source defect. Keep the configure command, original default
`make check`, static consumer, full fixture assertions and CLI checks unchanged.
Package the real `libGDSII.so.0.0.0` plus both upstream-generated symlinks and run
normal RPM post-install/post-uninstall `ldconfig` scriptlets. The runner clears
inherited loader overrides, uses a buildroot-only library path only when given
a nonempty staging root, and checks `ldd` resolution. After actual RPM installation
it uses the normal system loader without `LD_LIBRARY_PATH` or `LD_PRELOAD`, so a
missing installed shared library remains a hard failure. `glibc-common` supplies
the target `ldd` check. No upstream source, legal bytes, fixture or source manifest
changes are needed; replacement-head target CI and physical acceptance remain
pending, not asserted successful by this repair.

Diagnostic follow-up for exact head `8a1ac257cca6fab30d8a23b26954249cf902de45`,
Package CI `39001404659`: real rpmbuild and every staged API/static/CLI check
passed, DNF installation and `rpm -V` passed, but the installed runner exited 1
after the fixture hash with no failing-command trace. Independent inert RPM/SRPM
inspection verified the packaged files, both exact shared-link targets and the
installed runner; a missing packaged shared library is therefore not established.
The precise installed predicate remains unresolved. Add named checkpoints, an
ERR trap preserving the original nonzero status and captured `ldd` output only;
do not change any predicate, source, default feature, consumer or test. This is a
diagnostic-only change, not a claimed cause repair or successful installation.
Fresh exact-head hosted target evidence must identify the failure before a
causal recipe change or merge can be accepted.
