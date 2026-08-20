<!-- SPDX-License-Identifier: Apache-2.0 -->
# gf2x

This directory packages gf2x 1.3.0 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Upstream's current stable `gf2x-1.3.0` tag resolves to commit
`27ba588f03bf6e1e74763903bab25e6e8bb6d0f0`. The official release upload is
pinned by SHA-256 in `sources.yaml`.

The source archive contains 248 members under one top-level directory, has no
absolute or parent-traversal paths, and uses only contained regular-file hard
links. Its distribution license evidence is GPL-3.0-or-later together with
LGPL-2.1-or-later; the default build includes the GPL Toom implementation, so
the binary package retains both notices.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` records Arch
stable `1.3.0-3`, Debian stable `1.3.0-3`, Fedora 44 GA `1.3.0-18.fc44`,
openSUSE Tumbleweed `1.3.0-3.7`, and Ubuntu Resolute GA `1.3.0-3build1`.
The read-only AUR metadata contains only an old MinGW variant and was not used
as native package evidence. No distribution or AUR recipe was read or run.

The openEuler 24.03 LTS SP3 RVA23 repository supplies every BuildRequires and
has no package or provider named `gf2x`, no `libgf2x.so.3` provider, and no
reverse consumer requiring that SONAME. Version `1.3.0-1` therefore introduces
no lower-EVR replacement. The built shared object has SONAME `libgf2x.so.3`.

`%check` runs upstream's complete top-level `make check`: 15 low-level
multiplication cases and 45 general/FFT cases passed on native openEuler
`riscv64`, with zero failures, skips, XFAILs, or errors. The installed smoke
test compiles through `gf2x.pc`, links the packaged shared library, and checks
an exact polynomial multiplication result.

The packaging metadata and smoke test in this directory are Apache-2.0.
