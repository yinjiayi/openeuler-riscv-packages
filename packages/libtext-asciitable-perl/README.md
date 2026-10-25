<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-asciitable-perl

The frozen inventory's exact `libtext-asciitable-perl` key records Ubuntu
source 0.22-3. Its original tarball MD5
`6c34e6ed4575d59e8a51cbd4341e85f2` matches the official CPAN
[Text-ASCIITable 0.22](https://metacpan.org/dist/Text-ASCIITable) archive
byte for byte. The publisher's `CHECKSUMS` entry and the HTTPS archive both
have SHA-256
`e4d39537db35d75eb88032d2d26a707733fe33b6baeb212f9c733fc4bff07e43`.
All archive entries stay under one root without traversal, links or special
files. Build.PL, README and module POD grant the same GPL/Artistic terms as
Perl. The release declares no source-repository URL, so metadata links to
its canonical CPAN page rather than inventing one.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary snapshot,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-ASCIITable` nor a `perl(Text::ASCIITable)`
provider, and does provide the declared Perl build/runtime modules. This
snapshot check does not guarantee future repository contents.

`%check` retains all thirteen default upstream tests. Local Perl 5.34.1 ran
111 assertions with no skips. A source-level install produced the main and
wrapping modules plus two man pages; the SPEC lists all of them. The upstream
ANSI example is retained as RPM documentation. Installed-RPM smoke renders a
small deterministic table. Exact target CI must prove RPM build and install;
PR artifacts alone are not public RPM repository publication.
