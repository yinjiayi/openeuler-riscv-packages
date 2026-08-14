<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmpack

This directory packages libmpack `1.0.5` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official `1.0.5` tag resolves to immutable commit
`e9047afe4c02cd47c510f701deda6f502d7d94a2`; its SHA-256-pinned archive is
single-rooted and contains no unsafe paths or special members. Its only link is
the relative in-tree `test/tap.h -> deps/tap/tap.h` test header. It includes the
upstream MIT license and the complete self-contained TAP suite.

Frozen Arch, Debian, and Ubuntu metadata supplies component discovery lineage.
It was used only as read-only catalog evidence; no distribution recipe was
read or executed. A full target metadata and alias scan found no libmpack
package, provider, or consumer, and the current ABI is `libmpack.so.0`. The
target primary repository contains the complete build and test closure.

The upstream tag leaves its internal Makefile patch version at 1.0.3. The RPM
passes the public tag version as existing Makefile variables, so the installed
pkg-config version is 1.0.5 without modifying source or ABI. `%check` runs the
complete upstream TAP executable covering token conversion, incremental
parsing, object walking, serialization, and MessagePack-RPC state handling.
Installed smoke verifies the SONAME and compiles a public API encode/decode
round trip through the installed pkg-config metadata.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
