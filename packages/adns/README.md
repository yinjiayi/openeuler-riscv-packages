<!-- SPDX-License-Identifier: Apache-2.0 -->
# adns

This directory packages adns 1.6.2 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official upstream FTP index exposes 1.6.2 as the highest
stable release, and the exact archive is pinned by SHA-256 in `sources.yaml`.

The source archive contains 407 members under one top-level directory. It has
no absolute or parent-traversal paths, links, or special files. Upstream's
`COPYING` and source headers identify GPL-3.0-or-later licensing.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` records Arch
stable `1.6.1-1`, Debian stable `1.6.1-1`, Fedora 44 GA `1.6.1-6.fc44`,
openSUSE Tumbleweed `1.6.2-1.3`, and Ubuntu Resolute GA `1.6.1-1build1`.
Read-only AUR RPC metadata contains only a stale VCS entry; no AUR or
distribution recipe was read or executed.

The openEuler 24.03 LTS SP3 RVA23 repository supplies every declared
BuildRequires. It has no package or provider named `adns` or `libadns`, no
`libadns.so.1` provider, and no reverse consumer requiring that SONAME. Version
`1.6.2-1` therefore introduces no lower-EVR replacement. The built shared
object has SONAME `libadns.so.1`.

Upstream's top-level `make check` intentionally treats exit code 5 as a skip,
so the hard gate also ran every regression case directly: all 102 returned
zero on native openEuler `riscv64`, with zero skips or failures. The installed
smoke test checks the CLI version, compiles against `adns.h`, links the shared
library, and initializes and closes a resolver state without issuing a query.

Upstream's recursive install rules apply `DESTDIR` twice. The SPEC keeps the
official source unchanged and stages through explicit absolute install
directories with an empty `DESTDIR`; this layout was verified in an isolated
destination.

The packaging metadata and smoke test in this directory are Apache-2.0.
