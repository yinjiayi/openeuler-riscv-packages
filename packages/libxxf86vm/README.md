<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXxf86vm

This package tracks X.Org's stable `libXxf86vm` 1.1.7 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The [official release announcement](https://www.mail-archive.com/xorg@lists.x.org/msg08245.html)
publishes SHA-256 `ae50c0f669e0af5a67cc4cd0f54f21d64a64d2660af883e80e95d3fe51b945d8`
for the HTTPS `.tar.xz` archive; an independent download matched it. The
archive has one top-level tree without links, special files, or path traversal.
CI verifies the pinned digest before building.

The 1.1.7 source registers no upstream automated test programs. `%check`
retains the upstream `make check` target without describing it as a functional
suite. Installed-RPM smoke checks the public header, pkg-config metadata,
shared-library loading and exported ABI symbols. It does not validate
display-dependent mode-setting behavior.

The library source, header and `COPYING` match the SPDX `X11` license's
no-advertising variant of MIT; the Meson and manual-page build metadata use
MIT terms. The frozen inventory key is lowercase `libxxf86vm`, while upstream
and RPM names are `libXxf86vm`. PR CI artifacts do not establish public
repository publication.
