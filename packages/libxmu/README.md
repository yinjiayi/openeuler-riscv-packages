<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXmu

This package maps the inventory's exact `libxmu` key to X.Org's official
stable `libXmu` 1.3.1 release for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.
The [release announcement](https://www.mail-archive.com/xorg-announce%40lists.x.org/msg01877.html)
publishes SHA-256 `81a99e94c4501e81c427cbaa4a11748b584933e94b7a156830c3621256857bc4`
for the HTTPS tarball, matching the independently downloaded source. The
archive has one top-level tree without traversal paths, links, or special
files. CI fetches and verifies the pinned hash before building.

The official release includes the pre-generated Autotools build and 11
registered GLib unit-test executables. `glib2-devel` is required and
`--enable-unit-tests` explicitly retains the whole upstream suite in
`%check`; none of the tests call an X server. The CursorName test may report
an upstream skip only if the target's `/usr/include/X11/cursorfont.h` is
missing; the build requires `libX11-devel` so that header should be present.
Installed-RPM smoke additionally checks both library/pkg-config versions,
runs a display-free public charset function, and verifies linkage of the
full libXmu API. It does not claim X-server protocol coverage.

The optional DocBook documentation generator is disabled; both libraries,
public headers, and pkg-config interfaces remain enabled. Upstream `COPYING`
contains Open Group, Digital, XFree86, and ISC notices, recorded in the RPM's
SPDX expression. CI artifacts do not establish public RPM repository
publication.
