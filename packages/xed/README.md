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

Package CI run `33674636862` for exact head
`28f03c9bf41266cf03e10b8c50bbeac4acd74363` resolved XML, GLib, GTK 3 and
then stopped at the next effective Meson error because `gtksourceview-4` was
unavailable. Release 5 adds openEuler's `gtksourceview4-devel`, whose fixed
target metadata provides `pkgconfig(gtksourceview-4)`.

Package CI run `33675528070` for exact head
`64219f349f579106306b963df38de05113261264` resolved all earlier interfaces,
then stopped at the mandatory Meson dependency `libpeas-1.0`. Release 6 adds
`libpeas-devel`; checksum-verified openEuler 24.03 LTS SP3 EPOL RVA23 metadata
identifies `libpeas-devel-1.36.0-1.oe2403sp3.riscv64` as the provider of
`pkgconfig(libpeas-1.0)`. The source, patch set, and complete `%meson_test`
execution remain unchanged.

The current CI buildroot enables Everything RVA23 and the fixed supplemental
generation, neither of which contains `libpeas-devel`. This package metadata
repair is therefore not evidence of a successful RISC-V build: CI must first
make the official provider visible, then obtain fresh exact-head build and
smoke evidence. The RISC-V status remains `unknown`.
