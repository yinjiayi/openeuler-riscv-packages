<!-- SPDX-License-Identifier: Apache-2.0 -->
# mpdecimal

This directory packages mpdecimal 4.0.1 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The upstream HTTPS release archive is SHA-256 pinned. Its
single root, member paths, links, and file types were inspected before use.
The upstream source is BSD-2-Clause licensed.

The frozen discovery snapshot records Arch core `mpdecimal` 4.0.1-3 as
lineage only; no distribution recipe was read or executed. The runtime ships
both `libmpdec.so.4` and `libmpdec++.so.4` with development headers and
pkg-config metadata in the devel package.

Upstream `make check` runs its complete C and C++ suites against both static
and shared libraries. The official decimal test vectors are copyrighted and
not redistributed here. During `%check`, CI fetches them from the official
HTTPS endpoint, verifies the pinned SHA-256, and places them where upstream's
test runner expects them. The installed smoke compiles and executes C and C++
decimal arithmetic through the installed pkg-config files. Build-time network
access is required for the official vectors; a fetch failure fails `%check`.

External source licenses remain upstream's. Apache-2.0 covers only original
packaging metadata, scripts, tests, and documentation in this repository.
