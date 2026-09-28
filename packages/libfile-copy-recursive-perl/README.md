<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-copy-recursive-perl

This package maps the frozen inventory's exact `libfile-copy-recursive-perl`
key to the official [File-Copy-Recursive 0.45](https://metacpan.org/dist/File-Copy-Recursive)
CPAN release. Its HTTPS archive was independently downloaded and pinned to
SHA-256 `d3971cf78a8345e38042b208bb7b39cb695080386af629f4a04ffd6549df1157`,
matching the official CPAN `CHECKSUMS` index. The 19-entry archive has a
single top-level directory and contains no traversal paths, links, or special
files. CI verifies the digest before the openEuler 24.03 LTS SP3 `riscv64`/
RVA23 build.

`%check` runs all five default upstream test files, including symlink and
read-only directory cases where applicable. Upstream OS-specific and
permission-specific SKIP branches are not counted as passes. The installed-
RPM smoke checks the module provider and copies a small directory tree. The
source POD and CPAN metadata declare the same GPL/Artistic choice as Perl;
there is no standalone license file. CI artifacts do not prove public RPM
repository publication.
