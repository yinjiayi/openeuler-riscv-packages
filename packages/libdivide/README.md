<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdivide 5.4.0

Header-only integer division for C/C++ is not a native hardware speed claim.
The official https://libdivide.com site links ridiculousfish/libdivide.
Official stable v5.4.0 is pinned to commit
`ea0fb1ad79a116cd561595c930bcaf33147b3e6c`, tree
`ad653b11989148a72273994a415c8509ef05018f`; all 62 regular Git blobs match
the safe archive. SHA-256:
`6aa730b24dabb10c350d74363f94fcb0f750fe6fde65355278410aeb5bacd7fe`.
No detached signature is supplied. Frozen AUR/Fedora 5.3.0 discovery metadata
is lineage, not executable recipe or a claimed upstream latest version.

Retain the complete dual BSL-1.0 OR Zlib LICENSE.txt. Original doc/divlu.c
has a public-domain/CC0-1.0 notice, so the combined installed tests declare
`(BSL-1.0 OR Zlib) AND CC0-1.0`. Install that unmodified notice-bearing file
and the full official SPDX v3.27.0 CC0 text, fixed to
`d46e94e2c78ceede1cfc63cfa0396472d2798d4c`, Git blob
`0e259d42c996742e9e3cba14c677129b2c1b6311`, SHA-256
`a2010f343487d3f7618affe54f789f5487602331c0a8d03f49e9a7c547cf0499`.
SRPM retains the original source and both legal sources. No source patches.

The RPM installs headers, CMake metadata and source fixtures, not ELF binaries;
omit the inapplicable implicit debug subpackage, not any build/test target.

Keep all seven original Release build programs and all eight default CTest
entries (four original programs and their four build dependencies). Do not
reduce tester's six integer types, random iterations, divlu corpus, or the
finite branchfree benchmark's default algorithms/arguments. Architecture
probes remain AUTO; no forced x86/ARM vector flags, missing-test skips,
warning suppression, failure-ignore or shortened loops are added. Preserve
upstream strict diagnostics; its existing benchmark_divlu-only warning flag
is upstream, not a downstream workaround. Keep -O3 and add enabled assertions.

Full verbose CTest rejects C99 `Division fail:` diagnostics in addition to
exit status because the original C99 test prints failures without exiting
nonzero. Recompile/replay all four original programs unchanged against the
seven installed headers in staged and installed RPM environments; SHA-256
binds the distributed original test inputs. The separate downstream CMake
consumer verifies find_package(libdivide 5.4.0 EXACT), libdivide::libdivide,
and constant-divider headers. These checks do not add upstream case counts.
The unregistered benchmark/benchmark_divlu infinite loops are built, not
executed, exactly as default CTest specifies.

QEMU can check arithmetic results/benchmark checksums. Its printed timings
are explicitly not accepted as performance, native RISC-V, vector-ISA
coverage, or hardware evidence; those claims need a native runner. Metadata's
qemu-user profile applies only to functional build/install validation. A
timeout or failure is not a pass and must not be fixed by reducing the suite.

Fresh official/supplemental primary and filelists scans found no name/header/
CMake-provider collisions and a metadata build-root provider closure. That
does not replace actual DNF resolution. Target acceptance still requires
locked openEuler 24.03 LTS SP3/riscv64/RVA23 remote CI, real installation and
independent physical RPM/SRPM verification. Source-only verification and
trusted repository tests are not target execution. No local upstream/RPM/
QEMU execution, Auto-merge, upstream write, merge or publication claim.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
