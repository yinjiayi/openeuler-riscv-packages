<!-- SPDX-License-Identifier: Apache-2.0 -->
# xed

This directory packages upstream `https://github.com/linuxmint/xed` version `3.8.9` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Package CI run `33671388772` for exact head `74c43e4ac76f0717d585a29d541d346ea7bbd644` completed the audited dependency transaction and then failed during Meson configuration because `libxml-2.0` pkg-config metadata was unavailable. Release 2 declares `libxml2-devel`, which provides that build-time interface; no upstream source or tests are changed.

Package CI run `33672386241` for exact head
`b56ded625b8aa88afd83ba52367e4232f5460f2a` passed the audited dependency
transaction and the `libxml-2.0` check, then stopped at the next effective
error because `glib-2.0` pkg-config metadata was unavailable. Release 3 adds
openEuler's `glib2-devel`, the verified provider of that interface. The source,
patch set, and test execution remain unchanged.

Package CI run `33673849283` for exact head
`15596e8e97646b6d2c6947e116a691ab2b39f13a` resolved the earlier XML and GLib
interfaces, then stopped at the next effective Meson error because
`gtk+-3.0` was unavailable. Release 4 adds openEuler's `gtk3-devel`, whose
SHA-256-bound target repository metadata provides `pkgconfig(gtk+-3.0)`.
