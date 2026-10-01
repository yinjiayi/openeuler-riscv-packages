<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-worddiff-perl

The frozen inventory's exact `libtext-worddiff-perl` key maps to official
[Text-WordDiff 0.09](https://metacpan.org/dist/Text-WordDiff). The CPAN
HTTPS archive and its official `CHECKSUMS` entry both have SHA-256
`fee699ca763adca2f4e18f4a8a836fd2102bc2820af708f8eb43356d5ae0d50e`.
All archive entries stay under one top-level tree without traversal paths,
links or special files. The bundled `LICENSE` grants GPL version 1 or
later or Perl Artistic terms. The differently authored HTMLTwoLines
module also explicitly grants the same Perl terms.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-WordDiff` nor a `perl(Text::WordDiff)` provider.
It provides Algorithm::Diff version 1.201, HTML::Entities, Term::ANSIColor,
Module::Build, Encode and Test::Pod for the complete default test suite.
This snapshot check does not guarantee future repository contents.

`%check` retains all five default upstream tests. Local Perl 5.34.1 ran
59 assertions with no skips, including HTML, ANSI and POD syntax. A
source-level vendor install produced four modules and four man pages;
the SPEC lists those files. Installed-RPM smoke checks every module loads,
the provider exists, and HTML contains the expected word-level deletion
and insertion. Exact target CI must prove RPM build and smoke; PR artifacts
alone do not establish public RPM repository publication.
