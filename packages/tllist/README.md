<!-- SPDX-License-Identifier: Apache-2.0 -->
# tllist

This directory packages tllist 1.1.0 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. A header-only library is source included by applications and
does not ship a runtime shared object; its installed behavior is therefore
verified by compiling and running consumers. The immutable discovery snapshot
`discovery-20260808T165000Z-9a89920c269462cd` records the same 1.1.0 line in
Arch stable, Debian stable, Fedora 44 GA, openSUSE Tumbleweed, and Ubuntu GA.
An exact-name read-only AUR RPC query on 2026-08-12 returned no result. No AUR
or distribution packaging recipe was read or executed.

The official Codeberg 1.1.0 tag resolves to commit
`8dcb0725c73eee9e350f41a921faf0bcd2ab9920`. Its archive is SHA-256 pinned;
pre-extraction inspection found one root and no link, special entry, absolute
path, or parent traversal. Upstream declares the source and header under MIT.

The complete Meson unit target compiles and executes the upstream macro API.
Installed smoke independently compiles a public-header consumer and validates
front, back, length, and cleanup operations. The library has no architecture-
specific payload; its pkg-config file is therefore installed in the shared
pkg-config directory so the noarch RPM remains portable. tllist is absent from
the fixed target repository and every BuildRequires is present. Target RPM,
install, and smoke status remains unknown until exact-head QEMU CI completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
