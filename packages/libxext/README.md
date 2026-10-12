<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXext

This package tracks X.Org's official stable `libXext` 1.3.7 release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The
[X.Org release announcement](https://lists.x.org/archives/xorg-announce/2026-January/003660.html)
publishes SHA-256 `6c643c7035cdacf67afd68f25d01b90ef889d546c9fcd7c0adf7c2cf91e3a32d`
for the HTTPS tarball, matching the independently downloaded archive. It has
one top-level source tree with no links, special files, or traversal paths.
CI fetches and verifies the pinned hash before building.

The release registers no upstream test programs. `%check` retains Automake's
`make check` target without claiming an upstream functional suite. The
installed-RPM smoke compiles, links, and runs a client of the public
`XextCreateExtension`/`XextDestroyExtension` allocation API without an X
server; display-dependent extension requests remain untested.

The package disables building generated XML/PDF specifications, which need
additional documentation tools but do not affect the library, installed
headers, pkg-config metadata, or man pages. It also omits static and libtool
archives while retaining the shared runtime and linker name. Upstream
`COPYING` contains multiple X.Org permission variants, so the RPM records the
full conservative SPDX conjunction rather than calling the package simply
MIT. The frozen inventory key `libxext` (1.3.4 in that snapshot) maps to this
package ID; the upstream/RPM name is `libXext`. PR artifacts are not public
RPM publication evidence.
