<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXv

This package tracks X.Org's stable `libXv` 1.0.13 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The [official release announcement](https://www.mail-archive.com/xorg-announce@lists.x.org/msg01782.html)
publishes SHA-256 `7d34910958e1c1f8d193d828fea1b7da192297280a35437af0692f003ba03755`
for the HTTPS `.tar.xz` archive; an independent download matched it. The
archive has one top-level tree without links, special files, or path traversal.
CI verifies the pinned digest before building.

The 1.0.13 source registers no upstream automated test programs. `%check`
retains the upstream `make check` target without describing it as a
functional suite. Installed-RPM smoke compiles and runs a consumer of
`xv.pc` and the adaptor/encoding release APIs using locally allocated
structures. It does not validate display-dependent X Video requests.

The source `COPYING` and source headers cover the historical permission
notice variants represented by `SMLNJ AND HPND-sell-variant`. The frozen
inventory key is lowercase `libxv`, while the upstream and RPM names are
`libXv`. PR CI artifacts do not establish public repository publication.
