<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXxf86dga

This package maps the inventory's exact `libxxf86dga` key to X.Org's
official stable `libXxf86dga` 1.1.7 release for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The [release announcement](https://www.mail-archive.com/xorg-announce%40lists.x.org/msg01875.html)
publishes SHA-256 `b3be5b444d324cb6e0f4b5019a4972c99ea336ccb8ab7968eccefecd917ffde6`
for the HTTPS tarball, matching the independently downloaded source. The
archive has one top-level tree without traversal paths, links, or special
files. CI fetches and verifies the pinned hash before building.

Upstream 1.1.7 includes Autotools and Meson and asks downstreams to test the
new Meson path; this package uses that unmodified path. Meson registers no
tests, so `%check` retains `%meson_test` without claiming functional upstream
coverage. Installed-RPM smoke checks the package/pkg-config version and
compiles, links, and runs a client referencing both public DGA API families.
X-server-dependent protocol calls remain untested under QEMU user mode
without a server. The two public headers and generated manual pages are
retained.

Upstream `COPYING` and Meson identify the X11 license, recorded in the RPM.
CI build artifacts do not establish public RPM repository publication.
