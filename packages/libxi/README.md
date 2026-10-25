<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXi

This package maps the inventory's exact `libxi` key to X.Org's official
stable `libXi` 1.8.3 release for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.
The [release announcement](https://www.mail-archive.com/xorg%40lists.x.org/msg08293.html)
publishes SHA-256 `7ad60056f01af4f786cfe93b3a7707447711626fc8da2637bec71a90409babe5`
for the HTTPS tarball, matching the independently downloaded source. The
archive has one top-level tree and no traversal paths, links, or special
files. CI fetches and verifies the pinned hash before building.

The official release contains a pre-generated Autotools build and manual
pages. Its Automake files register no test programs or `TESTS`, so `%check`
runs the unmodified upstream `make check` without claiming functional test
coverage. Installed-RPM smoke checks package metadata, both public headers,
library loading, and public API symbol linking. X-server-dependent protocol
calls remain untested under QEMU user mode without an X server.

The pre-generated manual pages are retained. Building extra DocBook specs is
disabled because it is a separate XML toolchain; this does not disable the
library, headers, pkg-config metadata, or upstream `make check`. `COPYING`
contains MIT-style, Open Group, and historical permission notices, represented
by the RPM's SPDX expression. CI artifacts do not establish public RPM
repository publication.
