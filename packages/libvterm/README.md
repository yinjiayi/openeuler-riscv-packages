<!-- SPDX-License-Identifier: Apache-2.0 -->
# libvterm

This directory packages libvterm `0.3.3` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official upstream `v0.3.3` tag resolves to immutable
commit `9d6d2112335080312ef8c36667fa717ded4f7daf`; that commit archive is SHA-256 pinned,
single-rooted, and free of unsafe paths, links, or special members. It contains
the upstream MIT license and the complete maintained test corpus.

Arch stable, Debian, Fedora 44 GA, openSUSE Tumbleweed, and Ubuntu provide
frozen cross-distribution lineage. Read-only AUR RPC had no canonical package
row; no AUR PKGBUILD or distribution recipe was read or executed. This is new
to the fixed target repository and introduces only upstream's stable
`libvterm.so.0` ABI plus the three diagnostic command-line tools.

`%check` runs upstream `make test`, whose strict Perl harness executes all 43
shipped parser, encoding, state, screen, reflow, selection, regression, and
vttest cases and exits on the first failure. Installed smoke verifies the
SONAME, exercises the dump tool, and compiles against the public screen API
without network access.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
