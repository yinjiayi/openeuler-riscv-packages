<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-iconv-perl

The frozen inventory's `libtext-iconv-perl` key records Ubuntu source
1.7-8.1. This package uses the official [Text-Iconv 1.7](https://metacpan.org/dist/Text-Iconv)
CPAN release. Its HTTPS archive SHA-256
`5b80b7d5e709d34393bcba88971864a17b44a5bf0f9e4bcee383d029e7d2d5c3`
matches the publisher's `CHECKSUMS` entry. The archive contains one root,
regular files and directories only, without links or path traversal.

The archive README grants redistribution under the same terms as Perl itself;
the module and XS files name the same copyright holder and contain no
conflicting notice. The RPM uses the repository's Perl 5 dual-license SPDX
mapping, `GPL-1.0-or-later OR Artistic-1.0-Perl`. CPAN metadata's `unknown`
license field is not treated as the grant.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-Iconv` nor `perl(Text::Iconv)`. It contains the
glibc, compiler, Perl development and MakeMaker build providers needed for
this XS module. This is a repository snapshot, not a future-state guarantee.

Upstream's unmodified default `make test` runs two files and 14 assertions.
They passed locally with macOS Perl 5.34.1; the platform selected `-liconv`,
which does not establish the target glibc link mode. Upstream explicitly
permits conversion-pair-specific skips when a platform lacks a codeset, but
none occurred locally. Target RPM build, full default test outcome and
installed smoke require exact-head CI evidence. PR artifacts alone do not
prove public RPM repository publication.
