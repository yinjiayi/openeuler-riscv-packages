<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXfixes

This package tracks X.Org's official stable `libXfixes` 6.0.2 release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The
[X.Org release announcement](https://www.mail-archive.com/xorg%40lists.x.org/msg08192.html)
publishes SHA-256 `39f115d72d9c5f8111e4684164d3d68cc1fd21f9b27ff2401b08fddfc0f409ba`
for the HTTPS tarball; the independently downloaded archive matches it. The
archive has one top-level source tree with no links, special files, or
traversal paths. CI fetches and verifies the pinned hash before building.

The release supports both Autoconf and Meson. This package uses the upstream
Meson project and retains `%meson_test` in `%check`; Meson registers no tests,
so this is not described as a passing upstream functional suite. The
installed-RPM smoke compiles, links, and runs a consumer of `xfixes.pc` and
the public `XFixesVersion()` function, checking the library value against the
installed header's `XFIXES_VERSION`. It requires no X server; display-bound
extension operations remain untested by this smoke.

Upstream Meson declares `HPND-sell-variant AND MIT`, matching its `COPYING`
notices. The frozen discovery key `libxfixes` (which saw 6.0.0) maps to this
package ID; upstream/RPM capitalization is `libXfixes`, and official 6.0.2
is used instead of the older frozen version. A PR build artifact is not
evidence of public RPM publication.
