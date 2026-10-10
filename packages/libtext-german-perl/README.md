<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-german-perl

The frozen inventory's exact `libtext-german-perl` key records Ubuntu source
0.06-5. Its original tarball MD5
`9e968525f7385c80d636a4ba68d27bf4` matches the official CPAN
[Text-German 0.06](https://metacpan.org/dist/Text-German) archive byte for
byte, establishing the inventory-to-upstream mapping. The CPAN HTTPS archive
and publisher `CHECKSUMS` both record SHA-256
`922d4f19012d9773b11f4a6f642105e9f913f5866f4461b6059ca674d5bb07dd`.
The archive stays under one root and has no traversal, links or special files.
README and German.pod grant the same license terms as Perl. Upstream declares
no source-repository URL, so metadata uses the canonical CPAN page.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary snapshot,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither `perl-Text-German` nor a `perl(Text::German)` provider. This
snapshot check does not guarantee future repository contents.

Text::German reduces German words to approximate base forms; upstream's README
calls its method incomplete, not a linguistic guarantee. `%check` retains both
default upstream functional test files, which ran 34 assertions locally with
Perl 5.34.1. A local source-level install produced the module, eight helper
modules, a POD file and a man page; the SPEC lists all of them. Installed-RPM
smoke checks deterministic reduction and cache behavior. Exact target CI must
prove RPM build and installation; a PR artifact is not public publication.
