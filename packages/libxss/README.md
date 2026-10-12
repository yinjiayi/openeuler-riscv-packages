<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXss

This package tracks X.Org's stable `libXScrnSaver` 1.2.5 release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The [official release announcement](https://www.mail-archive.com/xorg@lists.x.org/msg08196.html)
publishes SHA-256 `5057365f847253e0e275871441e10ff7846c8322a5d88e1e187d326de1cd8d00`
for the HTTPS `.tar.xz` archive; an independent download matched it. The
archive has one top-level tree without links, special files, or path traversal.
CI verifies the pinned digest before building.

The 1.2.5 source registers no automated Autotools or Meson test programs.
`%check` retains upstream `make check` without describing it as a functional
suite. Installed-RPM smoke compiles and runs a consumer of `xscrnsaver.pc` and
the allocation/free API without an X server. It does not validate
display-dependent Screen Saver requests.

The source `COPYING` corresponds to SPDX `X11`. The frozen inventory key is
`libxss`, while the upstream source is `libXScrnSaver` and the shared library
and RPM use `libXss`. PR CI artifacts do not establish public repository
publication.
