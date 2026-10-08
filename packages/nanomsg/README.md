<!-- SPDX-License-Identifier: Apache-2.0 -->
# nanomsg

This directory packages nanomsg `1.3.0` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official `1.3.0` tag archive is pinned by SHA-256
`acf65c0ef312f431aa3c4cb114326781c999ec0c977067f3a1f0c81b5ec8710f`; it is
single-rooted and contains no unsafe paths, links, or special members. It
includes the upstream MIT license and maintained portable CTest suite.

Arch stable, Debian, Fedora 44 GA, openSUSE Tumbleweed, and Ubuntu provide
frozen component lineage at earlier stable releases. The SHA-256-pinned
official archive establishes the reviewed 1.3.0 source bytes. Read-only AUR RPC metadata was
considered; no AUR PKGBUILD or distribution recipe was read or executed. A
target metadata and alias scan was recorded for the earlier 1.2.5/ABI 6
admission; it is not fresh coverage evidence for this update. The 1.3.0
`src/nn.h` and CMake shared-library properties specify `libnanomsg.so.7`
(full ABI 7.0.2), which the RPM file manifest must match.

`%check` runs the upstream transport, protocol, poll, statistics, stress,
and regression CTests without omissions (44 default Linux tests in 1.3.0).
Installed smoke verifies the SONAME,
then compiles and runs a bounded in-process pair round trip through the public
pkg-config and socket APIs, requiring neither network nor privileged access.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
