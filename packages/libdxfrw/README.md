<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdxfrw

This directory packages upstream `https://github.com/LibreCAD/libdxfrw` version `1.0.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Source, identity and dependencies

The official stable tag `1.0.1` resolves to
`945f2161a13ee521f66f9c52dcfff998e8ccae99`, tree
`53f8fceec4dbe974ccb8d29f6e30be0fc3c72cfe`. All 90 regular archive files
match the authenticated Git blob inventory. Source SHA-256:
`34a89ea5946be0fdd5b0e9499cea4210b73921fb6f48b0fbcec0178939ee1e7b`.
Discovery retains Fedora `1.1.0-0.11.rc1.fc43`; the official `1.1.0-rc1`
tag is not a stable release, so it is not repackaged as stable 1.1.0.
The old Autotools `AC_INIT` says 0.6.3; this package uses the official tag's
CMake project version 1.0.1, not that stale embedded version.

Fresh complete official (18,503 packages) and supplemental (1,244) primary
and filelists inventories found no runtime/devel name, ABI, public header,
static library, CMake export, converter/man-page or pkg-config collision.
BuildRequires resolve in the metadata capability walk; this is not a DNF
SAT or completed dependency-install claim. Actual resolution is a CI gate.
No network is required by upstream build or test logic. No source archive
or generated build output is committed.

## Build and patch contract

The original default static library and `dwg2dxf` are built unchanged in
`build-static`. An additional shared build supplies `libdxfrw.so.1` and
its CMake exports. Shared exports are installed once; the original static
archive is added without overwriting the shared target configuration.
No library feature, converter, warning or original test is disabled.
Explicit `CMAKE_INSTALL_INCLUDEDIR=include` handles upstream's use of that
variable before `GNUInstallDirs`; this is configuration, not a source patch.

`0001-correct-installed-pkgconfig-paths.patch` fixes only the erroneous
literal `|` in `libdir` and nonexistent `include/libdxfrw1` directory.
It is original downstream packaging code (Apache-2.0), not a RISC-V defect.
It is SPEC-applied and checksum-bound in package metadata. Remove it when
an adopted official stable release emits correct pkg-config paths. No
upstream issue, PR or other write was made.

The initial CI failed in `%prep`, before compilation: GNU patch with
`--fuzz=0` rejected the asymmetric short context of the first hunk, whereas
Apple patch accepted it. The repair represents the same two replacements
as exact one-line hunks. Both GNU and Apple patch must apply with zero fuzz
and zero offset to the fixed, checksum-verified source; patched bytes must
equal precisely those two replacements. This is patch-format portability,
not permission to weaken patch application, original builds or tests.

## Tests and evidence boundary

This release registers zero upstream CTest/Automake semantic tests. A
**downstream DXF contract** is the committed packaging fixture that checks
three drawing entities and exact coordinates/layer after real API reads;
it is not an upstream test suite or general DWG-conformance claim.
The original `dx_iface.cpp`, `dx_iface.h` and `dx_data.h` are copied without
changes and SHA-256-bound for installed replay. A fresh installed-header
consumer reads ASCII input, binary CLI output and ASCII CLI round-trip
output. Independent CMake imported-target and static-library consumers
also read those outputs (five semantic replays per runner invocation).
The binary DXF magic is compared byte-for-byte. Missing input and invalid
CLI usage must fail. `%check` additionally checks outputs from both
original default-static and shared converter builds (seven replays total).
No batch-mode exit-status shortcut is used. No sleeps, native devices,
network, permissive `|| true` or suppressed test failures are introduced.

`%check` runs against the staged install; RPM smoke first verifies installed
runtime/devel files with `rpm -V`, then repeats the installed consumers.
Test compilation links the packaged API, not source-tree API headers.
The fixture checks DXF LINE/CIRCLE/POINT only: it does not prove the full
DWG parser, all entities/code pages, malformed-file security, native
hardware behavior, timing or performance. Local work is limited to inert
source/patch review, source verification, Bash syntax and trusted tooling
tests. RISC-V build/install and physical RPM/SRPM proof must come from CI.

## License review

The library and converter notices allow GPL version 2 or later; complete
upstream `COPYING` is installed. `src/intern/rscodec.cpp` also contains
Simon Rockliff's complete June 26, 1991 permission to modify/distribute,
conditional on retaining his named contribution and with a disclaimer.
`LicenseRef-Rockliff-1991` refers to that exact embedded notice, not an
invented SPDX identifier. The entire unchanged file is installed as a
license record, preserving attribution and conditions in runtime and SRPM.
The source-only Autotools helpers' original notices and distribution
exceptions are retained and installed, including X Consortium `install-sh`.
Complete official GPLv3 text is separately SHA-256-pinned in `sources.yaml`
for helpers declaring GPLv3-or-later; the archive's generated Autotools
material remains in the SRPM. Those helpers are not substituted or executed
locally. Original upstream example/interface notices remain in the replay
sources. New packaging fixtures are Apache-2.0; combining the fixture with
the upstream interface for tests does not relicense upstream code.

No signature is supplied for these source inputs; HTTPS, authenticated Git
identity and SHA-256 checks are not a GPG-signature claim. Submission does
not claim successful target builds, Auto-merge, a merge or a public release.
