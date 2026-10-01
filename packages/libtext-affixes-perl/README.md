<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-affixes-perl

The frozen inventory's exact `libtext-affixes-perl` key maps to Ubuntu
source 0.09-3 and the official upstream
[Text-Affixes 0.09](https://metacpan.org/dist/Text-Affixes) release. The
official CPAN HTTPS archive SHA-256 is
`7d0808f7194d7a68786fee8fedc36414c69029c460cc41efe608d2bbfb3dcc5e`,
matching the publisher's `CHECKSUMS` entry. Its archive contains only regular
files under one top-level directory, without traversal or links. The included
LICENSE, README and module POD grant the same GPL/Artistic terms as Perl.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary snapshot,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither `perl-Text-Affixes` nor a `perl(Text::Affixes)` provider. It does
provide Module::Build, Test::More, Test::Pod and Test::Pod::Coverage. This
snapshot check does not guarantee future repository contents.

`%check` keeps all five default upstream `t/` files. Local Perl 5.34.1 ran
22 assertions; the POD coverage file skipped locally because
Test::Pod::Coverage is absent here. The target SPEC explicitly installs that
test dependency so target CI must run the complete default suite. A local
source-level install produced the module and man page; the SPEC lists both.
Installed-RPM smoke checks version and deterministic prefix/suffix results.
Only exact target CI can establish RPM build and installation success; PR
artifacts are not evidence of public RPM repository publication.
