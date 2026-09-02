<!-- SPDX-License-Identifier: Apache-2.0 -->
# xde-session

This directory packages upstream `https://github.com/bbidulock/xde-session` version `1.14` release `6` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## CI repair history

Exact-head Package CI run `33671434719` for commit `e5bbca16ecd6bff5fbc8be2a7756b65293cd592b` completed the audited BuildRequires installation, then failed in `%build` because `pkg-config` could not resolve the mandatory `x11` module. Release 2 adds openEuler's `libX11-devel` build dependency; the target `riscv64` repository metadata records that package as the provider of `pkgconfig(x11)`.

Exact-head Package CI run `33673288095` for commit
`f6d368fbb6990fdf49f9070026325a37bad7bf28` passed the mandatory `x11`
check, then stopped at the next effective error because `pkg-config` could not
resolve mandatory module `xext`. Release 3 adds openEuler's `libXext-devel`,
whose target repository metadata provides `pkgconfig(xext)`. The source,
patch set, and `%check` execution remain unchanged.

Exact-head Package CI run `33674836307` for commit
`0cf30b59dd429a510dfd91a90127120eecb4a4d0` passed the mandatory `x11`,
`xext`, and `xau` checks, then stopped because `pkg-config` could not resolve
the next mandatory module, `xscrnsaver`. Release 4 adds openEuler's
`libXScrnSaver-devel`, whose target repository metadata provides
`pkgconfig(xscrnsaver)`. The source, patch set, and complete `%make_build
check` execution remain unchanged; the RISC-V build status remains unknown
pending fresh exact-head CI evidence.

Exact-head Package CI run `33676559117` for commit
`f06fd3b9b863405a83852868cbccdfd46e209901` passed the mandatory `x11`,
`xext`, `xau`, and `xscrnsaver` checks, then stopped because `pkg-config`
could not resolve the next mandatory module, `xdmcp`. Release 5 adds
openEuler's `libXdmcp-devel`; the checksum-verified official openEuler 24.03
LTS SP3 `riscv64` repository metadata records version
`1.1.4-2.oe2403sp3` as the provider of `pkgconfig(xdmcp)`. The source, patch
set, and complete `%make_build check` execution remain unchanged; the RISC-V
build status remains unknown pending fresh exact-head CI evidence.

Exact-head Package CI run `33678893917` for commit
`d541f7f070a0e0c9999878a9902520212f9ea552` passed the mandatory `x11`,
`xext`, `xau`, `xscrnsaver`, and `xdmcp` checks, then stopped because
`pkg-config` could not resolve the next mandatory module, `ice`. Release 6
adds openEuler's `libICE-devel`; the checksum-verified official openEuler
24.03 LTS SP3 `riscv64` repository metadata records version
`1.1.1-1.oe2403sp3` as the provider of `pkgconfig(ice)`. The source, patch
set, and complete `%make_build check` execution remain unchanged; the RISC-V
build status remains unknown pending fresh exact-head CI evidence.
