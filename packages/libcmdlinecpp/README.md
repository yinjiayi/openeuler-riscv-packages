<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcmdlinecpp

Official nullptrT/libcmdlinecpp v1.0.0, immutable commit
`db5417e4853aa5d0a07b8e8c1fb697375dde1188`. Source archive SHA-256:
`3a420bf657470a6e8e996b6d90eaf8cf9fa4b35f659c2de597631bbd26712f14`.
All 28 archive files match official Git blobs. No detached signature is supplied.
Discovery lineage is the existing August 8 catalog entry, revalidated against
the official stable tag; no AUR recipe is executed or borrowed.

The LGPL-3.0-or-later source notices and complete upstream LICENSE.txt remain
unchanged. Full official GNU GPL3 accompanies the LGPL text incorporating it,
in SRPM and installed license payload. Packaging itself remains Apache-2.0.

Retain upstream's default static library, all public headers, optional consumer
metadata and all four original example programs. There is no upstream registered
CTest/assertive test suite: enabling BUILD_CMDLINECPP_TESTS builds demonstrations,
not a passing test count. Doxygen's optional documentation target is not a default
build target. No shared-library ABI is claimed for this default-static package.

One scoped metadata patch exports the selected filename to the parent CMake
directory (otherwise the generated .pc Libs points only at a directory) and uses
the complete static filename in find_library. The installed config reads the
existing LIBLOGCPP_DOTTED_VERSION macro (the source header's actual spelling).
It changes no parser logic, headers,
examples or compiler options. It is an upstream-generic packaging correction,
not a RISC-V source defect. Not submitted upstream; remove when fixed upstream.

Target run38981536885 at packaging head d60fbc8ddcf4 built all examples and
passed their help/rejection checks, but original main -n 3 fixture aborted in
the library with CmdLineArguments::NotFound. is_specified("iterations") and
typed conversion use unprefixed logical keys; lookup_option rejected every
unprefixed key before searching registered options. A second minimal patch
normalizes that form into the existing search. Long/short CLI forms and missing
key exceptions remain. All original headers, examples and test commands are
unchanged. The downstream consumer additionally verifies three equivalent key
forms and one missing-key exception, against both staged and installed products.
This is a generic source repair, not a RISC-V workaround or a passing build
claim. Remove when upstream supports these existing public-API callers.

Target CI must build all original examples. Explicitly downstream checks exercise
help/rejection for all four, valid options/actions/trailing-list vectors and two
semantic consumers against staged then installed static library/header bytes.
The original main2.cpp lowercase path lookup remains unchanged; help/rejection
checks do not assert that unused illustrative lookup is correct. Every installed
example source and every installed public header are hash checked. The original source provides no additional
default test runner to omit. Installed compiler/CMake/pkgconf dependencies support
the installed replay. Target is openEuler 24.03 LTS SP3 riscv64/RVA23; no local
upstream/RPM/QEMU execution or native/performance/security claim. Metadata/source
validation does not establish build/install/physical-product success: fresh hosted
CI and independent RPM/SRPM/ELF acceptance remain required before merging.
