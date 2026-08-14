<!-- SPDX-License-Identifier: Apache-2.0 -->
# nanomsg

This directory packages nanomsg `1.2.4` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official `1.2.4` tag resolves to immutable commit
`e6d0b8ddfc780eb89f8f6ef305e92c19e76bed6b`; its SHA-256-pinned archive is
single-rooted and contains no unsafe paths, links, or special members. It
includes the upstream MIT license and all 43 maintained portable CTests.

Arch stable, Debian, Fedora 44 GA, openSUSE Tumbleweed, and Ubuntu provide
frozen component lineage at earlier stable releases, while the immutable
official tag establishes current 1.2.4. Read-only AUR RPC metadata was
considered; no AUR PKGBUILD or distribution recipe was read or executed. A
full target metadata and alias scan found no nanomsg package, provider, or
consumer; upstream 1.2.4 introduces `libnanomsg.so.6` (full ABI 6.0.1).

`%check` runs all 43 upstream transport, protocol, poll, statistics, stress,
and regression CTests without omissions. Installed smoke verifies the SONAME,
then compiles and runs a bounded in-process pair round trip through the public
pkg-config and socket APIs, requiring neither network nor privileged access.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
