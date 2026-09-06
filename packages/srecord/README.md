<!-- SPDX-License-Identifier: Apache-2.0 -->
# srecord

This directory packages SRecord 1.65.0 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. `Source0` is the immutable, versioned official SourceForge
release archive. Its SHA-256 was calculated locally, and all 800 archive
members were audited as one safe `srecord-1.65.0-Source/` tree with no links,
special files, absolute paths, or parent-directory escapes.

Frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
records AUR `1.65.0-2`, Fedora 44 GA `1.65.0-7.fc44`, openSUSE Tumbleweed
`1.65.0-2.6`, Debian stable `1.64-4.1`, and Ubuntu 26.04 LTS GA
`1.64-4.1build2`. No Arch official-repository entry was present in the
snapshot; the AUR evidence was obtained through its read-only RPC endpoint.
No AUR recipe or distribution build script was fetched or executed.

The build runs upstream's complete 208-case CTest regression suite serially
and builds all upstream-generated manuals and documentation. The upstream
CMake project installs its library as a static archive, so the devel package
uses the conventional `libsrecord.a` filename and introduces no shared
SONAME. The installed smoke exercises all three command-line tools, converts
the same data between Motorola S-Record and Intel HEX, compares the results,
and compiles a C++ consumer against the installed static library.

Command-line sources are GPL-3.0-or-later, while the reusable library sources
are LGPL-3.0-or-later. Apache-2.0 covers only this repository's original
packaging metadata and smoke script.
