<!-- SPDX-License-Identifier: Apache-2.0 -->
# muparser

This directory packages muparser `2.3.5` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official `v2.3.5` tag resolves to immutable commit
`fbafd7f8774af2b53f4d2de07c57353fcfc09216`; its SHA-256-pinned archive is
single-rooted and has no unsafe paths, links, or special members. It contains
the BSD-2-Clause license and the complete maintained parser test program.

Arch stable, Debian, Fedora 44 GA, and Ubuntu provide frozen package lineage;
Ubuntu's frozen snapshot remains at 2.3.4 while upstream and the other current
channels corroborate 2.3.5. Read-only AUR RPC metadata was considered, and no
AUR PKGBUILD or distribution recipe was read or executed. The target has no
muparser package, provider, consumer, or `libmuparser.so.2` alias collision.

`%check` runs the complete upstream ParserTest registration with OpenMP and
samples enabled. Installed smoke verifies the SONAME, then compiles and runs a
C++ client through pkg-config that parses and evaluates a public expression.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
