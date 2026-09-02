<!-- SPDX-License-Identifier: Apache-2.0 -->
# xde-session

This directory packages upstream `https://github.com/bbidulock/xde-session` version `1.14` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## CI repair history

Exact-head Package CI run `33671434719` for commit `e5bbca16ecd6bff5fbc8be2a7756b65293cd592b` completed the audited BuildRequires installation, then failed in `%build` because `pkg-config` could not resolve the mandatory `x11` module. Release 2 adds openEuler's `libX11-devel` build dependency; the target `riscv64` repository metadata records that package as the provider of `pkgconfig(x11)`.
