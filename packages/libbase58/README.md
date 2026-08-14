<!-- SPDX-License-Identifier: Apache-2.0 -->
# libbase58

This directory packages libbase58 `0.1.4` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official annotated `v0.1.4` tag resolves to immutable
commit `16c2527608053d2cc2fa05b2e3b5ae96065d1410`; its SHA-256-pinned archive is
single-rooted and contains no unsafe paths, links, or special members. It
contains the MIT license and all 12 tests registered by upstream.

Frozen AUR metadata supplies component discovery lineage. It was used only as
read-only catalog evidence; no AUR recipe was read or executed. A full target
metadata and alias scan found no libbase58 package, provider, or consumer, and
the current ABI is `libbase58.so.0` (full library version 0.0.2). The target
primary repository contains the complete build/test closure, including
`libgcrypt-devel` for the tested Base58Check command-line implementation and
`vim-common` for the upstream tests' `xxd` fixture conversion.

`%check` runs all 12 upstream-registered raw and checksum encoding/decoding
tests, including expected invalid-input cases. Installed smoke verifies the
SONAME, exercises a binary command-line round trip, then compiles and runs a
public-library API round trip through the installed pkg-config metadata.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
