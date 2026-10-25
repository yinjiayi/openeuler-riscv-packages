<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXcomposite

This package maps the inventory's exact `libxcomposite` key to X.Org's
official stable `libXcomposite` 0.4.7 release for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The [release announcement](https://www.mail-archive.com/xorg%40lists.x.org/msg08236.html)
publishes SHA-256 `8bdf310967f484503fa51714cf97bff0723d9b673e0eecbf92b3f97c060c8ccb`
for the HTTPS tarball, matching the independently downloaded source. The
archive has one top-level source tree without traversal paths, links, or
special files. CI fetches and verifies the pinned hash before building.

The official release includes both Autotools and Meson; this package uses the
upstream Meson build. That project registers no test cases. `%check` retains
`%meson_test` without claiming functional upstream tests. The installed-RPM
smoke checks the package version and compiles, links, and runs a client of the
public display-free `XCompositeVersion` API. X-server-dependent protocol
requests remain untested under QEMU user mode without an X server.

XML-to-manpage generation is disabled because it requires a separate xmlto
toolchain; the library, public header, shared linker name, and pkg-config
metadata are retained. Upstream `COPYING` and the Meson project identify
HPND-sell-variant and MIT notices, both recorded in the RPM. CI build
artifacts do not establish public RPM repository publication.
