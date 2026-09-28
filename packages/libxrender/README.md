<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXrender

This package tracks X.Org's official stable `libXrender` 0.9.12 release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The
[X.Org announcement](https://lists.x.org/archives/xorg-announce/2024-December/003567.html)
publishes SHA-256 `b832128da48b39c8d608224481743403ad1691bf4e554e4be9c174df171d1b97`
for the HTTPS tarball; the independently downloaded archive matched it. Its
single top-level source tree contains no links, special files, or traversal
paths. CI verifies the pinned hash before building.

The release registers no upstream test programs. `%check` retains its
Automake `make check` target without claiming an upstream functional suite.
The installed-RPM smoke compiles, links, and runs a consumer of `xrender.pc`
and `XRenderParseColor`, testing a valid RGBA value and an invalid value. This
path does not require an X server; it does not validate display-dependent
Render requests.

The upstream `COPYING` and source notices use the X.Org permission-to-sell
license variant, recorded as `HPND-sell-variant`. The frozen inventory key is
`libxrender` while the upstream and RPM names are `libXrender`; this exact
mapping avoids a duplicate Dashboard entry. PR build artifacts do not prove
public RPM publication.
