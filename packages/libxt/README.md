<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXt

This package maps the frozen inventory's exact `libxt` key to X.Org's
stable `libXt` 1.3.1 release for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.
The [official release announcement](https://lists.x.org/archives/xorg-announce/2024-November/003560.html)
publishes SHA-256 `e0a774b33324f4d4c05b199ea45050f87206586d81655f8bef4dba434d931288`
for the HTTPS tarball, matching the independently downloaded file. Its 431
archive members stay under one top-level directory, with no traversal paths,
symlinks, or special files. CI verifies the pinned digest before building.

The upstream Autotools release registers three GLib unit-test executables:
`Alloc`, `Converters`, and `Event`. `glib2-devel` and `--enable-unit-tests`
keep the complete suite active in `%check`; none of these tests needs an X
server. Installed-RPM smoke additionally compiles against the public
`Intrinsic.h` header, links `libXt`, and exercises display-free allocation.
It does not establish X-server protocol coverage.

Optional DocBook specifications are disabled, while the shared library,
public headers, pkg-config interface, and manual pages remain enabled. The
RPM SPDX expression reflects the MIT, historical X11/HPND, and Open Group
notices in upstream `COPYING`. CI artifacts alone do not establish public
RPM repository publication.
