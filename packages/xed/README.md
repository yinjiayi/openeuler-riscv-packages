<!-- SPDX-License-Identifier: Apache-2.0 -->
# xed

This directory packages upstream `https://github.com/linuxmint/xed` version `3.8.9` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Package CI run `33671388772` for exact head `74c43e4ac76f0717d585a29d541d346ea7bbd644` completed the audited dependency transaction and then failed during Meson configuration because `libxml-2.0` pkg-config metadata was unavailable. Release 2 declares `libxml2-devel`, which provides that build-time interface; no upstream source or tests are changed.
