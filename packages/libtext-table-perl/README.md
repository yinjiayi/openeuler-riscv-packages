<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-table-perl

The frozen inventory's exact `libtext-table-perl` key maps to Ubuntu source
1.135-1 and the official [Text-Table 1.135](https://metacpan.org/dist/Text-Table)
CPAN release. Ubuntu orig tarball MD5 `6bea3ce614b6c28460f1af96114709a6`
matches the CPAN archive byte for byte. The publisher's `CHECKSUMS` entry
and HTTPS archive both have SHA-256
`fca3c16e83127f7c44dde3d3f7e3c73ea50d109a1054445de8082fea794ca5d2`.
The archive's 37 entries have one root without traversal, links or special
files. The included LICENSE grants ISC terms; the generic `open_source`
metadata value is not used as a substitute for the license text.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-Table` nor a `perl(Text::Table)` provider. It
contains upstream runtime dependency `perl(Text::Aligner)` 0.16. This is a
snapshot check, not a guarantee about future repository contents.

`%check` retains all seven default upstream `t/` files. All 175 assertions
passed with local Perl 5.34.1 using the separate official Text-Aligner 0.16
source tree in `PERL5LIB` (its CPAN SHA-256 is
`5c857dbce586f57fa3d7c4ebd320023ab3b2963b2049428ae01bd3bc4f215725`).
The separate `xt/author` and `xt/release` suites are upstream author/release
checks, not default functional tests, and are not claimed as passing. A
source-level staging install yielded the module and man page, both listed in
the SPEC; examples are retained as documentation. Installed-RPM smoke checks
rendered table cells. Target CI must prove RPM build and installation.

Successful PR CI artifacts alone do not prove public RPM repository publication.
