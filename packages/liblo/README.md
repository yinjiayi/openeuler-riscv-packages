<!-- SPDX-License-Identifier: Apache-2.0 -->
# liblo

This directory packages liblo 0.36 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The immutable source is the official asset attached to
upstream's current stable `0.36` release (tag commit
`025f277275e6b81032a72dfb0b131adab80363e6`). Its locally verified SHA-256
agrees with the digest published by the GitHub release API and is pinned in
`sources.yaml`. The archive contains one source root and no unsafe paths,
special files, or escaping links.

Frozen discovery snapshot `discovery-20260812T161000Z-b34-liblo` records Arch
`1:0.36-1`, Debian stable `0.32-2`, Fedora 44 `0.34-3.fc44`, openSUSE
Tumbleweed `0.36-1.3`, and Ubuntu Resolute `0.34-1`. Distribution metadata was
used only as lineage evidence; no distribution recipe was read or executed.

The target repository snapshot contains Doxygen `1:1.9.6-2.oe2403sp3`, GCC
and G++ `14.3.1-10.oe2403sp3`, GNU Make `1:4.4.1-2.oe2403sp3`, and pkgconf
`1.9.5-2.oe2403sp3`; it contains neither liblo, its command-line tools, nor
`liblo.so.7`. The built library declares SONAME `liblo.so.7` and does not
replace any target ABI. `%check` runs the complete registered upstream suite:
the core UDP/TCP/UNIX/SLIP test, the bidirectional TCP scenario, and both C++
binding variants (4/4, zero skips). The exact official archive also passed
upstream's full `make distcheck`. The installed smoke compiles through
`liblo.pc`, links the public ABI, and validates a real address object's
protocol and port without sending network traffic.

liblo is LGPL-2.1-or-later. Apache-2.0 covers only this repository's original
packaging metadata and scripts.
