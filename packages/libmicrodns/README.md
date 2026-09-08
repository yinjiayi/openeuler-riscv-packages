<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmicrodns

This directory packages libmicrodns 0.2.0 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The immutable source is upstream's current stable `0.2.0`
tag (commit `deb7ed7bf05dc26802a0ca1987049b31405b8930`) and is pinned by the
locally calculated SHA-256 in `sources.yaml`. The archive contains one source
root and no unsafe paths, special files, or escaping links.

Frozen discovery snapshot `discovery-20260812T140000Z-b34-libmicrodns`
records Arch `0.2.0-2`, Debian stable `0.2.0-1`, Fedora 44
`0.2.0-15.fc44`, openSUSE Tumbleweed `0.2.0+6-2.11`, and Ubuntu Resolute
`0.2.0-1build1`. Distribution metadata was used only as lineage evidence; no
distribution recipe was read or executed.

The target repository snapshot contains GCC `14.3.1-10.oe2403sp3`, Meson
`1.3.1-1.oe2403sp3`, Ninja `1.11.1-1.oe2403sp3`, and pkgconf
`1.9.5-2.oe2403sp3`; it contains neither libmicrodns nor `libmicrodns.so.1`.
`%check` runs the complete maintained Meson test suite (the single registered
`microdns:unittest` executable) without exclusions. The installed smoke test
compiles a public-header consumer through `microdns.pc`, links the shared ABI,
and calls `mdns_strerror` without requiring multicast network access.

libmicrodns is LGPL-2.1-or-later. Apache-2.0 covers only this repository's
original packaging metadata and scripts.
