<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXvMC

This package tracks X.Org's stable `libXvMC` 1.0.15 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The [official release announcement](https://www.mail-archive.com/xorg@lists.x.org/msg08243.html)
publishes SHA-256 `4f518afde3d7fd435346af7b368d2f73517f3d5f82647c962caf3f7bb8ff7078`
for the HTTPS `.tar.xz` archive; an independent download matched it. The
archive has one top-level tree without links, special files, or path traversal.
CI verifies the pinned digest before building.

The 1.0.15 source registers no upstream automated test programs. `%check`
retains the upstream `make check` target without describing it as a functional
suite. Installed-RPM smoke checks both the client and wrapper shared libraries,
their public symbols, headers and pkg-config files. It does not validate
display-dependent motion-compensation behavior.

The source `COPYING` and wrapper/header permission notices use MIT terms;
the source build metadata includes the historical X.Org permission notice
represented by `HPND-sell-variant`. The frozen inventory key is lowercase
`libxvmc`, while upstream and RPM names are `libXvMC`. PR CI artifacts do not
establish public repository publication.
