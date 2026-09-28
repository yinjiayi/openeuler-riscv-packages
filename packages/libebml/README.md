<!-- SPDX-License-Identifier: Apache-2.0 -->
# LibEBML

This directory packages the official LibEBML 1.4.6 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. Matroska's HTTPS tarball is pinned by
SHA-256, and its byte stream also matched the publisher's SHA-512 manifest.
The official release index lists 1.4.6 as newer than the inventory snapshot's
1.4.5. Archive inspection found no absolute or parent-traversal paths.

Upstream CMake requires utf8cpp 3.2.5 and otherwise fetches its Git tag.
`Source1` pins the publisher's exact archive by SHA-256, and CMake reads that
verified tree. The library is built shared with upstream SONAME 5. Upstream
provides no executable test target; `%check` and installed smoke compile and
run a public C++ API check with EBML ID serialization and library ABI access.

LibEBML is LGPL-2.1-or-later; the utf8cpp build dependency is BSL-1.0.
The Apache-2.0 header covers only this repository's original packaging
files. The discovery record is Ubuntu metadata, not an executable recipe.
QEMU-user CI can verify functional behavior but not native RISC-V performance;
successful PR checks do not establish RPM repository publication.
