<!-- SPDX-License-Identifier: Apache-2.0 -->
# libomemo

This directory packages upstream `https://github.com/gkdr/libomemo` version `0.8.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `2` declares the CMocka, GLib, libgcrypt, Mini-XML, and SQLite pkg-config providers, keeps all three upstream CMocka executables enabled, and configures in the out-of-tree directory expected by the openEuler CMake macros. The package-local patch ports the private implementation from Mini-XML 3 callbacks to the parallel-installable Mini-XML 4 API supplied by the immutable project repository; the public libomemo API is unchanged. The source SHA-256 remains unchanged, and RISC-V build status remains `unknown` pending fresh exact-head CI evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Downstream release `3` records both source-license scopes: `LICENSE` grants
MIT terms to the independent library sources, public headers and tests;
upstream `CMakeLists.txt` separately states copyright 2022 Sebastian Pipping
and GPL v2 or later. Neither notice overrides or relicenses the other work.
The RPM license expression records this combination, and both the SRPM and
installed license directory carry the complete official GNU GPL version2
document (a separately checksum-locked `Source1`) alongside the original MIT
license. The GPL document's own verbatim-copy permission is retained.
All18 original source files, the Mini-XML 4 patch, the three default CMocka
tests and the smoke script are unchanged. Exact-head target CI and physical
RPM/SRPM review are required again for release `3`; earlier green builds of
release `2` do not establish acceptance of this repair.
