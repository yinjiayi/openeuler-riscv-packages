<!-- SPDX-License-Identifier: Apache-2.0 -->
# stow

This directory packages GNU Stow 2.4.1 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. GNU's current stable release page and FTP index identify
2.4.1 as the latest stable release. The immutable official archive has
SHA-256 `2a671e75fc207303bfe86a9a7223169c7669df0a8108ebdf1a7fe8cd2b88780b`.
It contains one source root, 87 regular files and 10 directories, with no
absolute or parent-traversing paths, links, or special entries.

Frozen discovery snapshot `discovery-20260812T174200Z-b34-stow` records Arch
`2.4.1-1`, Debian stable `2.4.1-2`, Fedora 44 `2.4.1-4.fc44`, openSUSE
Tumbleweed `2.4.1`, and Ubuntu Resolute `2.4.1-2`. Distribution metadata was
used only as untrusted lineage evidence; no distribution recipe was executed.

The target repository snapshot contains Perl `4:5.38.0-10.oe2403sp3`, GNU
Make `1:4.4.1-2.oe2403sp3`, perl-generators `1.10-11.oe2403sp3`,
perl-Test-Simple `2:1.302198-1.oe2403sp3`, and perl-Test-Output
`1.034-1.oe2403sp3`. It contains no `stow` package, `/usr/bin/stow` provider,
or `perl(Stow)` provider. Stow is architecture-independent and exposes no
shared-library SONAME, so it cannot replace a target shared ABI.

`%check` runs the complete official upstream harness: all 16 test files and
478 assertions pass under the locked RVA23 image, with no skips or weakened
tests. The installed smoke verifies the packaged Perl module and performs a
real stow/unstow cycle, including executing the created target symlink and
proving it is removed by the delete operation.

GNU Stow is GPL-3.0-or-later. Apache-2.0 covers only this repository's
original packaging metadata and smoke script.
