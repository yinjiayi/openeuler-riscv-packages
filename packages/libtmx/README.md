<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtmx

Portable Tiled TMX map loader, official stable `tmx_1.10.1` from
`baylej/tmx`, fixed commit `b671187d51a5616b80774c94650a360ce48a872f`.
The codeload source SHA-256 is
`498732f076a344387c04946a9da2542e532547526d633d08bd2d289dfe2a0578`;
all 49 Git blobs were compared with the archive. The lightweight official tag
has no signature; no detached signature asset is published for this release.
The complete BSD-2-Clause `COPYING` and original copyright notices are retained.
AUR discovery lineage (`libtmx` 1.10.0-2) is discovery evidence only; no external
packaging script is executed or copied. The repository license covers original
packaging, not the upstream BSD-2-Clause files.

The recipe keeps upstream CMake defaults: static library, required libxml2,
zlib enabled, zstd and Sphinx documentation disabled by their original defaults.
It does not introduce feature switches or source patches. The literal upstream
`/usr/lib/cmake/tmx` export location is preserved, with the archive in
`/usr/lib64` and `tmx.h` in `/usr/include`. GNUInstallDirs receives relative
`lib64` so generated imported targets remain relocatable for staged consumers.
The pure-static package does not
produce a separate debuginfo subpackage; distribution optimization/debug
compiler flags are retained.

Upstream defines no CTest test cases. Its actual CI checks are the unchanged
example dumper's two full command lines (compressed map plus resource-manager,
file-descriptor, callback and buffer arguments) and a C++ header compilation.
These checks run in `%check` against staged installation and again after RPM
installation. All original dumper/CMake and eleven example data files are
installed byte-for-byte and checked with SHA-256. The original dumper is a smoke
consumer, not an assertion suite or a leak-free guarantee; its diagnostic
allocation counts and resource-preload behavior are not promoted to such claims.

A separate downstream assertion consumer is added, without altering upstream:
four map input APIs, equality of 504 GIDs across five map loads, dimensions,
typed properties, tilesets/text objects, two correctly loaded object templates,
color conversion, and invalid-input rejection. The installed runner rebuilds
the original CMake consumer, compiles the unchanged upstream C++ check, and
links the downstream consumer with the installed static archive and target
libxml2/zlib. It must exit nonzero on a failed assertion; checks are compiled
with `-UNDEBUG`. These are compatibility checks, not a new upstream test suite.

Target is only openEuler 24.03 LTS SP3 riscv64/RVA23 using `ci/image.lock`.
No source, RPM or QEMU build runs on the local host. Local metadata, trusted
tooling, golden evaluation and fixed source-only verification do not establish
target build/install/test success. Hosted target CI and physical RPM/SRPM
acceptance remain required before merge. Dependency provider inventory uses
full official and supplementary primary/filelists with version bounds retained;
only target DNF resolution can establish installability. No auto-merge is enabled.
