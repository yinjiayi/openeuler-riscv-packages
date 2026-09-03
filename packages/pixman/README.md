<!-- SPDX-License-Identifier: Apache-2.0 -->
# pixman

This directory packages pixman `0.46.4` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Fedora 44 GA supplied the reviewed `0.46.2-3.fc44` packaging
baseline; the selected source is the newer official stable release already
observed in Arch stable, openSUSE Tumbleweed, and Ubuntu 26.04 LTS GA.

The official release archive is pinned by independently calculated SHA-256,
and its bytes also match the upstream SHA-512 file. Archive inspection found
one expected root, no absolute or parent-traversal path, no special entry, and
only safe relative symlinks. The committed discovery snapshot's AUR match was
the stale `pixman-git` VCS package, so it was excluded; a later AUR RPC query
was metadata-only. No AUR recipe or distribution spec was read or executed.

The network-free build explicitly enables the complete upstream Meson test
suite and libpng-backed test support. The installed smoke test links against
the public pixman API and verifies a real image fill operation. The package's
RISC-V status remains `unknown` until CI runs it in the pinned openEuler
RVA23/QEMU environment.

Exact-head run `33723149338` completed the long RISC-V/QEMU build, passed all
35 upstream Meson tests, and produced four binary RPMs plus one SRPM. Package
installation then succeeded, but the public-API smoke source failed to compile
because it used `NULL` without including its standard definition. Release 2
adds `<stddef.h>` to that smoke source; package code and upstream test coverage
are unchanged, and installed-smoke status awaits the next exact-head run.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, and documentation.
