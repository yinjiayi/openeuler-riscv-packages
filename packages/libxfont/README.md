<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXfont2

This package maps the inventory's exact `libxfont` key to X.Org's official
stable `libXfont2` 2.0.9 release for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The [release announcement](https://www.mail-archive.com/xorg%40lists.x.org/msg08332.html)
publishes SHA-256 `f042a370666815e7b941e9b7019024755bd1c6c2954afbfa515af378251799e2`
for the HTTPS tarball, matching the independently downloaded source. The
archive has one top-level source tree and no traversal paths, links, or
special files. CI fetches and verifies the pinned hash before building.

The default build retains built-in fonts, FreeType, BDF and PCF formats,
and gzip compression. Upstream disabled the deprecated X fontserver backend
by default in 2.0.9; this spec does not override that upstream decision.
Python is an explicit build dependency so `%check` runs the upstream five
malformed-PCF parser security tests with their generated fixtures. The
fontserver-specific test is not applicable when that backend is absent.
The installed-RPM smoke checks the version and compiles, links, loads, and
runs a client exercising public font-name record allocation and disposal.
It does not assert live X-server behavior.

The RPM license expression follows the notices in upstream `COPYING` and
the current Fedora packaging review. The devel package contains the public
header, pkg-config metadata, and developer DocBook source. CI build
artifacts are not evidence of publication to the public RPM repository.
