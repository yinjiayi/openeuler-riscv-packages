<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-sharedir-dist-perl

The frozen inventory key `libfile-sharedir-dist-perl` records Ubuntu source
0.07-1. This package uses the official [File-ShareDir-Dist 0.07](https://metacpan.org/dist/File-ShareDir-Dist)
CPAN release. Its HTTPS archive SHA-256
`8d7fe5d0ee22351f41ef95adc22dbd56c31ffa2a9b2c1984300e92ff7e9fe86d`
matches publisher `CHECKSUMS`. The archive has one root, only regular files
and directories, and no traversal paths or links.

The archive's `LICENSE` grants GPL version 1 or later, or Artistic License
1.0, as Perl 5 terms. `README` and all four shipped modules repeat the Perl 5
grant; the small corpus files are test fixtures under that distribution grant.
No conflicting notice was found. The RPM metadata uses
`GPL-1.0-or-later OR Artistic-1.0-Perl`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-ShareDir-Dist` nor Provides for the four shipped
modules. It does provide File::Copy and Test::More. This is a snapshot check,
not a guarantee about future repository contents.

All six unmodified default upstream test files passed 19 assertions on a
fresh local Perl 5.34 build. A staged vendor install contained four modules
and four manpages. The target build, tests, installed smoke and physical
RPM/SRPM products remain unverified until exact-head CI. PR artifacts do not
constitute public publication.
