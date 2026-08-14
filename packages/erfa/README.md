<!-- SPDX-License-Identifier: Apache-2.0 -->
# erfa

This directory packages ERFA `2.0.1` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The publisher's current stable release asset is SHA-256
pinned, has one archive root, and contains no unsafe path, link, or special
member. Its license text is BSD-3-Clause.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` records the
same stable component in Arch extra, Fedora 44 GA, Debian stable, openSUSE
Tumbleweed, and Ubuntu 26.04 LTS GA. Read-only AUR RPC found no exact `erfa`
package. No AUR or distribution packaging recipe was read or executed.

The openEuler 24.03 LTS SP3 RVA23 repository has no existing ERFA package or
`liberfa.so.1` provider, so version `2.0.1-1` introduces no lower-EVR or
SONAME replacement. `%check` runs both maintained upstream executables:
the full ERFA numerical conformance suite and the extra version/date suite.
Installed smoke compiles and runs a calendar-to-Julian-date call through the
public pkg-config interface.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
