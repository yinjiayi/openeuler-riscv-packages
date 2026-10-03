<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-number-delta-perl

The frozen inventory's exact `libtest-number-delta-perl` row maps to
[Debian's source package 1.06-4](https://packages.debian.org/source/sid/libtest-number-delta-perl)
and the official [CPAN Test-Number-Delta 1.06 release](https://metacpan.org/dist/Test-Number-Delta).
The publisher's `D/DA/DAGOLDEN/CHECKSUMS` and downloaded HTTPS source archive
both give SHA-256
`535430919e6fdf6ce55ff76e9892afccba3b7d4160db45f3ac43b0f92ffcd049`.
The 43 archive entries stay under one top-level directory, without traversal
paths, links or special files. The distribution-wide `LICENSE`, `README`,
and `lib/Test/Number/Delta.pm` explicitly grant Apache-2.0 rights. No
third-party or vendored executable code was found in the archive.

The official openEuler 24.03 LTS SP3 RVA23 `everything` `repomd.xml` pins
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
That metadata has neither `perl-Test-Number-Delta` nor
`perl(Test::Number::Delta)`, but does provide the required
`perl(Test::Builder)`, `perl(Test::Builder::Tester)`, `perl(Test::More)`,
and core dependencies. This is a repository snapshot, not proof of public
availability at a later time.

`%check` retains all 12 default upstream test files. The original source
passed 72 assertions with zero skips on the local Perl 5.34.1 host. The
target CI must independently prove the full test and installed-RPM smoke.
The installed smoke checks RPM ownership, module version, passing absolute
tolerance and inequality behavior. PR CI success does not prove publication.
