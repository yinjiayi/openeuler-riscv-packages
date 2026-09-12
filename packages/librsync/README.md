<!-- SPDX-License-Identifier: Apache-2.0 -->
# librsync

This directory packages librsync 2.3.4 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The source is the immutable asset attached to upstream's
current stable `v2.3.4` release and is pinned by a locally calculated
SHA-256 in `sources.yaml`. Archive paths and links were audited before use.

Frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
records Arch Extra `1:2.3.4-2`, Debian stable `2.3.4-1.1`, Fedora 44
`2.3.4-8.fc44`, openSUSE Tumbleweed `2.3.4-1.11`, and Ubuntu Resolute
`2.3.4-1.1ubuntu3`. Distribution metadata was used only as lineage evidence;
no distribution recipe was read or executed.

The package builds shared ABI `librsync.so.2` and the `rdiff` client against
the target repository's `popt-devel`. `%check` runs all 15 registered
upstream CTest cases, including the command-line round-trip tests. The installed
smoke test independently performs an `rdiff` signature/delta/patch round trip.

librsync is LGPL-2.1-or-later. Its compiled-in BLAKE2 reference implementation
is used under its CC0-1.0 option. Apache-2.0 covers only this repository's
original packaging metadata and scripts.
