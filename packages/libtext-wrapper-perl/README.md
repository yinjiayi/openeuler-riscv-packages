<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-wrapper-perl

The frozen inventory's exact `libtext-wrapper-perl` key maps to official
[Text-Wrapper 1.05](https://metacpan.org/dist/Text-Wrapper). The CPAN HTTPS
archive and its official `CHECKSUMS` entry both have SHA-256
`64268e15983a9df47e1d9199a491f394e89f542e54afb33f4b78f3f318e09ab9`.
Archive entries are under one top-level tree, without traversal paths,
links or special files. The bundled `LICENSE` explicitly grants either
GPL version 1 or later, or the generic nine-clause Artistic License 1.0.
Its text matches [Artistic-1.0](https://spdx.org/licenses/Artistic-1.0.html),
not the distinct Perl-kit Artistic-1.0-Perl variant. Release 2 corrects the
SPEC/package metadata identifier to `GPL-1.0-or-later OR Artistic-1.0`.
The original bundled LICENSE bytes and module copyright/disclaimers remain
unchanged; this correction does not relicense or modify the upstream source.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-Wrapper` nor a `perl(Text::Wrapper)` provider.
It provides Test::Differences, which the SPEC requires to use upstream's
stronger comparison path in its Unicode test. This snapshot check does
not guarantee future repository contents.

`%check` retains all four default upstream `t` files. Local Perl 5.34.1
ran 32 assertions with no skips. The archive also has two `xt/release`
POD author tests outside default MakeMaker `TESTS`; they were not run and
are not counted as passed. One requires Pod::Coverage::TrustPod, absent in
the reviewed target primary. Installed-RPM smoke tests exact line wrapping
and the module provider. Target CI must prove the RPM build and smoke; PR
artifacts alone do not establish public RPM repository publication.

The release-2 correction changes only license accounting and the RPM release.
Source pins, patches, all default tests, `%check` and installed smoke remain
unchanged. The earlier local-test statement above is historical evidence, not
a release-2 local rerun. Fresh exact-head target CI and physical RPM/SRPM
verification are required before claiming release-2 build acceptance; no
author-only tests, native RISC-V validation or public publication are claimed.
