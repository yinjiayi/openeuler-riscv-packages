# sfsexp 1.4.1

This is an inert package proposal, not evidence of a target build or a submitted PR.
Canonical package ID sfsexp follows the five retained distribution lineages;
libsexp is the actual library/ABI name and must also be checked for collisions.

The official release asset is fixed by SHA256
15e9a18bb0d5c3c5093444a9003471c2d25ab611b4219ef1064f598668723681.
It is bound to commit b7d3bea0effb6663a6d69897bc1c4ea3cc08b682 and tree
98f2786c124cdb5be8d031d9bbe47722af8788df. The captured release contains
62 exact main-Git files plus 19 generated extras, not an all-Git-identical archive.
All 42 omitted repository paths are classified in the local source contract.
The lightweight tag and commit offered no signatures; the selected release has
one archive asset and no detached signature/checksum asset. This is a statement
about captured metadata, not a global absence or independent archive authentication.

Production remains the original configure/make/install flow: default shared and
static libraries; default upstream _NO_MEMORY_MANAGEMENT_ policy; original
-O3 -Wall and NODEBUG append; eight examples and eight test programs built.
No --enable-thread-unsafe-memory-management or debug option is forced.
No source patch, native ISA flag, SIMD option, or CMake replacement is applied.
The public seven-header directory is /usr/include/sfsexp; sfsexp.pc links -lsexp.
The single SDK RPM retains original .so/.a/.la installation, with normal debug
generation left enabled. No example or upstream test CLI is installed.

Original make check is preserved but registers zero functional tests. The added
build check invokes six original deterministic programs against the exact release
fixture: readtests (18 records in each of two passes), ctest (all chunk lengths),
error_codes, partial, bug and read_and_dump. The readtests counter oracle rejects
its otherwise-successful exit when FAIL is nonzero. Partial output is checked by
status, exact leading diagnostic and output shape, not claimed fully byte-exact.
ctorture elapsed-time and vis_test's one-second watchdog programs remain built
and unchanged but are not executed. The nondefault four-profile Valgrind matrix,
random stress generator, optional UTF-8 fixture and legacy language bindings are
not claimed tested or redistributed as supplemental source.

Six owned public-C API groups run at build and installed stages, using a fresh
consumer and negative no-library link control. Installed compilation uses actual
pkg-config flags; link trace, full map and six loader symbols must resolve to the
same installed shared file, with complete raw records and SDK before/after hashes.
No ambient LD_LIBRARY_PATH/RPATH is allowed for installed checks. This is bounded
API and SDK evidence, not whole-library safety, concurrency or performance proof.

Core grant: LGPL-2.1-or-later, with the UC/LANL notice intact. Complete COPYING and
LICENSE_LGPL and every one of the 81 raw original files are retained as notices.
GNU source-helper exceptions remain distinct; LicenseRef-SFSEXP-GNU-Helpers elects
the permitted later GPL3 branch, including the nested Bootstrap GPL branch, with
all original Autoconf/Libtool exceptions and full GPL3 text. It does not convert
the compiled library to GPL. X Consortium and FSF unlimited notices remain raw.
Owned packaging and QA use Apache-2.0 with its full text. The recovered optional
Markus Kuhn UTF-8 fixture has unversioned CC BY attribution, is absent from the
release/default workload and is not inserted; its own grant/version must be
resolved before a future additive redistribution. No blanket LGPL claim covers it.

Fresh complete official/supplemental provider and namespace joins (including
sfsexp, libsfsexp, libsexp and source identity), current declaration fences,
root source/rights approval, trusted repository gates and actual target CI remain
required. No source, rights, provider, target, physical, merge, publication or full
Daily acceptance follows merely from this draft. The parent records actual work
in the existing README/track only after execution.

Explicit build prerequisites include gawk and sed for the original generated
configure/Libtool commands. Their exact command owners must be in the build-role
closure; an ambient image tool or incidental provider is not assumed. The runtime
QA requirements and all source/default/API behavior are unchanged by this revision.
