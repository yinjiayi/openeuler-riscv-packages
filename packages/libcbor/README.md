<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcbor

This directory packages upstream libcbor 0.14.0 for openEuler 24.03 LTS SP3
on `riscv64`/RVA23. CI downloads the official release tag over HTTPS and
verifies its pinned SHA-256 before the network-enabled target build.

The package builds a versioned shared library and a development subpackage.
`%check` runs every registered upstream CMocka test plus the C++ linkage
executable. The installed-RPM smoke test compiles, links, serializes, and
parses a CBOR value through the public API.

External source licenses remain those of upstream. The repository license only
covers original packaging metadata, scripts, and documentation.
