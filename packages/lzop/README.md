<!-- SPDX-License-Identifier: Apache-2.0 -->
# lzop

This directory packages lzop `1.04` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official publisher archive is SHA-256 pinned,
single-rooted, and free of unsafe paths, links, or special members. It contains
the upstream GPL-2.0-or-later license and maintained CMake test definition.

Arch stable, Debian, Fedora 44 GA, openSUSE Tumbleweed, and Ubuntu provide
frozen cross-distribution lineage. Read-only AUR RPC had no canonical package
row; no AUR PKGBUILD or distribution recipe was read or executed. Release `4`
deliberately supersedes the fixed target's `1.04-3` command package and retains
the target `lzo-devel` dependency without taking ownership of liblzo2's ABI.

`%check` uses CTest to run the complete upstream automated test, which invokes
the freshly built lzop against the shipped license input and fails on any
compression error. Installed smoke verifies a deterministic compress, test,
decompress, and byte-for-byte round trip without network access.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
