# libccd 2.1

The package follows the first build path in the official README: plain Make,
default double precision and static library, with every public header installed
under `/usr/include/ccd` and `/usr/lib64/libccd.a`. It is a static development
package, not a claim about the optional shared CMake/autotools builds or their
different single-precision defaults. No core target is disabled.

Release 2 omits the automatic debuginfo subpackage: this original static-only
installation has no executable/shared ELF for the debug-file collector.
Exact-head CI for release 1 completed both source and staged default checks
but failed on the empty debuginfo `%files` list; it did not produce accepted
RPMs or run installed checks. Source, patch, default build/test commands and
installed content are unchanged. Replacement-head CI remains an acceptance
gate, not an asserted success.

## Source and rights

Official `danfis/libccd` stable lightweight tag `v2.1` resolves to commit
`7931e764a19ef6b21b443376c699bbc9c6d4fba8`. The commit archive has SHA-256
`479994a86d32e2effcaad64204142000ee6b6b291fd1859ac6710aee8d00a482`.
The complete Git tree and all 103 original blobs were independently checked.
No signature is asserted. Historical AUR `libccd 2.1-1` lineage comes from
`discovery-20260808T165000Z-9a89920c269462cd`; no AUR recipe was executed.

The library is BSD-3-Clause; bundled CU and its checker are LGPL-3.0-or-later.
The aggregate license therefore records both. Full BSD/GPL/LGPL notices and
pristine corresponding source archive plus all original file hashes accompany
the RPM. CU is test support, not part of the installed collision library.
The Python 3 checker port retains the copyright/license notice and adds a dated
modification notice. Only print/range/filter compatibility and textual diff
streams change; EPS 0.6 and non-exact comparison are unchanged.
The patch is not submitted upstream; remove it when an official fixed release
supplies equivalent Python 3 support.

## Tests and provenance

`%check` runs the original `make -C src check PYTHON=python3`: all nine suites,
42 test entries (including setup/teardown), and 18 out/err regression pairs.
Because upstream test/checker exit statuses alone can miss failures, the wrapper
requires complete zero-failure summaries, positive assertion counts, every DONE
marker, all generated fixtures and 18 successful original comparisons. No suite
filter, epsilon override, fixture rewriting or ignored failure is used.

Staged and installed checks repeat the original Make test target against the
actual RPM archive and public headers. Only fresh temporary copies of upstream
runtime sources/public headers are removed to rule out fallback; pristine
source0 remains unchanged. Absolute archive links, before/after SHA-256 checks,
RPM ownership, header hashes and default double config checks bind the results
to physical installed content. Original bench binaries are built by this target
but are not executed by upstream plain-Make `check`; no timing/performance or
native RISC-V claim follows. Optional CU framework self-tests and alternative
CTest/autotools routes are not represented as having run.

Build support is `gcc make m4 glibc-devel python3 diffutils bash coreutils rpm
patch gzip tar`. Installed test support uses a separately evidenced, bounded,
official-only DNF transaction through the pinned repository helper, never a
consumer dependency or candidate replacement. Fresh complete supplier metadata
and all open PR identities found no name/header/library conflict; static
dependency closure is a preflight only, not an actual target solver result.

Target: locked openEuler 24.03 LTS SP3, riscv64/RVA23 QEMU user mode. No local
RPM/QEMU or upstream test execution. Source-only verification and trusted
repository tests do not imply target build success: exact-head CI, installation
and physical artifacts remain required before serial explicit squash merging.
