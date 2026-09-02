<!-- SPDX-License-Identifier: Apache-2.0 -->
# parlatype

This directory packages upstream `https://github.com/gkarsay/parlatype` version `4.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Package CI run `33671468530` for exact head `e6fdf4134c1e0bed41c9166a14e9cb562ed782ee` completed the audited dependency transaction and then failed during Meson configuration because `gtk4` pkg-config metadata was unavailable. Release 2 declares `gtk4-devel`, which provides that build-time interface; no upstream source or tests are changed.
