<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXrandr

This package tracks X.Org's stable `libXrandr` 1.5.5 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The [official release announcement](https://www.mail-archive.com/xorg-announce@lists.x.org/msg01873.html)
publishes SHA-256 `72b922c2e765434e9e9f0960148070bd4504b288263e2868a4ccce1b7cf2767a`
for the HTTPS `.tar.xz` archive; an independent download matched that digest.
The archive has one top-level source tree, with no links, special files, or
traversal paths. CI verifies the pinned digest before building.

The 1.5.5 source has no registered Autotools or Meson test programs. `%check`
retains the upstream `make check` target; it is not described as a functional
upstream suite. Installed-RPM smoke compiles and runs a consumer of
`xrandr.pc`, covering mode-info, gamma, and monitor allocation/free APIs
without an X server. It does not validate display-dependent RandR requests.

The source license is `HPND-sell-variant`; the independently licensed Meson
build script is not part of the installed library. The frozen inventory key
is lowercase `libxrandr`, while the upstream and RPM names are `libXrandr`.
Passing PR CI would provide a build artifact, not proof of public RPM
repository publication.
