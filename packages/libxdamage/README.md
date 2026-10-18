<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXdamage

This package maps the inventory's exact `libxdamage` key to X.Org's official
stable `libXdamage` 1.1.7 release for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The [release announcement](https://www.mail-archive.com/xorg-announce%40lists.x.org/msg01868.html)
publishes SHA-256 `127067f521d3ee467b97bcb145aeba1078e2454d448e8748eb984d5b397bde24`
for the HTTPS tarball, matching the independently downloaded source. The
archive has one top-level source tree without traversal paths, links, or
special files. CI fetches and verifies the pinned hash before building.

The official release includes both Autotools and Meson; this package uses the
upstream Meson build. That project registers no test cases. `%check` retains
`%meson_test` without claiming functional upstream tests. The installed-RPM
smoke checks the package version and compiles, links, loads, and runs a client
referencing the public `XDamageQueryExtension` symbol. It does not call X
server-dependent protocol functions; those remain untested under QEMU user
mode without an X server. No core feature is disabled.

The upstream `COPYING` notice is HPND-sell-variant; the Meson build definition
also carries MIT, so the RPM conservatively records both. The devel package
contains the public header and pkg-config metadata. CI build artifacts are
not evidence of publication to the public RPM repository.
