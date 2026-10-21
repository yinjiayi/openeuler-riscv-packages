<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmobi

This directory packages libmobi `0.12` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official `v0.12` tag resolves to immutable commit
`85dcfe803fc2a21020ddcf15c3eb66b93d388add`; its SHA-256-pinned archive is
single-rooted and contains no unsafe paths, links, or special members. It
includes the upstream LGPL-3.0-or-later license, 12 document samples, and all
32 shipped checksum fixtures.

Frozen AUR, Debian, and Ubuntu metadata supplies component discovery lineage.
It was used only as read-only catalog evidence; no distribution recipe was
read or executed. A full target metadata and alias scan found no libmobi
package, provider, or consumer, and the current ABI is `libmobi.so.0`. The
target primary repository contains the complete build/test closure, including
system libxml2 and zlib development files.

`%check` runs all 12 upstream sample-driven tests with encryption support and
checksum validation enabled. This includes the maintained invalid sample as an
expected failure rather than dropping it. Installed smoke verifies the SONAME,
tool version, and a compiled public-library version query through the installed
pkg-config metadata.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
