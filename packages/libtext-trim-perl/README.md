<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-trim-perl

The frozen inventory's exact `libtext-trim-perl` key maps to official
[Text-Trim 1.04](https://metacpan.org/dist/Text-Trim). The CPAN HTTPS
archive and its official `CHECKSUMS` entry both have SHA-256
`d5878a9079d33cd1766cf6abc44cd625bd00a0213d2ce8e3143fe6944abaaa11`.
All archive entries stay under one top-level tree and none is a traversal
path, link or special file. The bundled `LICENSE` explicitly grants
GNU GPL version 1 or later or the Perl Artistic License, resolving the
frozen inventory's historical `unverified-upstream` marker by direct
release review.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-Trim` nor a `perl(Text::Trim)` provider. It
provides Perl Encode, Test::Pod and Test::Pod::Coverage, which the SPEC
requires for the complete target test suite. This snapshot check does not
guarantee future repository contents.

`%check` retains all seven default upstream `t` files, including Unicode
and POD checks. Local Perl 5.34.1 reported 64 planned assertions: 63 passed,
one POD coverage assertion skipped because Test::Pod::Coverage is absent
locally. The target SPEC declares the official module so exact-head CI must
prove the unskipped suite; the local skip is not a pass. Installed-RPM smoke
checks trim, ltrim and rtrim behavior plus the RPM module provider. PR
artifacts alone do not establish public RPM repository publication.
