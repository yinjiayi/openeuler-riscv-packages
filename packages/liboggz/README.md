<!-- SPDX-License-Identifier: Apache-2.0 -->
# liboggz

This directory packages liboggz 1.1.3 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The source is the current stable archive published in
Xiph.org's official release index and is pinned by the locally calculated
SHA-256 in `sources.yaml`. The archive contains one source root and no unsafe
paths, special files, or escaping links.

Frozen discovery snapshot `discovery-20260812T140000Z-b34-liboggz` records
Arch `1.1.3-1`, Debian stable `1.1.3-1`, Fedora 44 `1.1.3-1.fc44`, openSUSE
Tumbleweed `1.1.3-2.5`, and Ubuntu Resolute `1.1.3-3`. Distribution metadata
was used only as lineage evidence; no distribution recipe was read or
executed.

The target repository snapshot contains GCC `14.3.1-10.oe2403sp3`, GNU Make
`1:4.4.1-2.oe2403sp3`, pkgconf `1.9.5-2.oe2403sp3`, and libogg-devel
`2:1.3.5-4.oe2403sp3`; it contains neither liboggz nor `liboggz.so.2`.
`%check` runs the complete registered Automake suite: the oggz-chop HTTP date
test plus all 23 library comment, write, read, and I/O tests (24/24 total,
zero skips). The installed smoke compiles through `oggz.pc`, creates and
closes a real write context, and thereby checks headers, link metadata, and
the installed `liboggz.so.2` ABI.

liboggz is BSD-3-Clause. Apache-2.0 covers only this repository's original
packaging metadata and scripts.
