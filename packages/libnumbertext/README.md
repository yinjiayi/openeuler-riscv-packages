<!-- SPDX-License-Identifier: Apache-2.0 -->
# libnumbertext

This directory packages libnumbertext 1.0.11 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. `Source0` is the immutable C++ archive attached to upstream's
official latest release. Its SHA-256 was calculated locally, and all 102 archive
members were audited as one safe `libnumbertext-1.0.11/` tree with no links,
special files, absolute paths, or parent-directory escapes.

Frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
records Arch Extra `1.0.11-3`, Fedora 44 GA `1.0.11-10.fc44`, openSUSE
Tumbleweed `1.0.11-1.12`, Debian 13.6 stable `1.0.11-4`, and Ubuntu 26.04 LTS
GA `1.0.11-4build2`. A read-only AUR RPC name search found only the obsolete,
orphaned MinGW cross-build `mingw-w64-libnumbertext` (`1.0.7-1`); no AUR
recipe or distribution build script was fetched or executed.

The build preserves upstream's warnings-as-errors policy and runs the complete
Automake suite. The release has one maintained Spanish language regression
test, which passed on both a native RISC-V supplemental host and an independent
GCC 15 host with zero failures, skips, XFAILs, or XPASSes. The installed smoke
checks the `spellout` CLI, pkg-config metadata, shared-library SONAME, and a
compiled C++ consumer using an installed language module.

The library and most language modules are dual-licensed under
LGPL-3.0-or-later or BSD-3-Clause; the Serbian module is available under
LGPL-3.0-or-later or CC-BY-SA-3.0. Apache-2.0 covers only this repository's
original packaging metadata and smoke script.
