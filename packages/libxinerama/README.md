<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXinerama

This package maps the inventory's exact `libxinerama` key to X.Org's official
stable `libXinerama` 1.1.6 release for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The [release announcement](https://www.mail-archive.com/xorg%40lists.x.org/msg08239.html)
publishes SHA-256 `d00fc1599c303dc5cbc122b8068bdc7405d6fcb19060f4597fc51bd3a8be51d7`
for the HTTPS tarball, matching the independently downloaded source. The
archive contains one top-level source tree and has no traversal paths, links,
or special files. CI fetches and verifies the pinned hash before building.

Upstream 1.1.6 includes both Autotools and Meson and asks downstreams to test
the new Meson path; this package uses that unmodified path. The Meson project
registers no tests, so `%check` retains `%meson_test` without claiming
functional upstream coverage. Installed-RPM smoke checks the installed RPM,
pkg-config version, public headers, dynamic library loading, and two public
symbols. The API requires an X server for protocol calls; the smoke does not
claim to exercise those calls under QEMU user mode without a server. Upstream's
five manual pages and both public headers are retained.

Upstream `COPYING` and the Meson project identify MIT, MIT-open-group, and X11
notices, all recorded in the RPM. CI build artifacts do not establish public
RPM repository publication.
