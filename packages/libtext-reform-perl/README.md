<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-reform-perl

The frozen inventory's exact `libtext-reform-perl` key maps to official
[Text-Reform 1.20](https://metacpan.org/dist/Text-Reform). The CPAN HTTPS
archive and its official `CHECKSUMS` entry both have SHA-256
`a8792dd8c1aac97001032337b36a356be96e2d74c4f039ef9a363b641db4ae61`.
All archive entries stay under one top-level tree, without traversal paths,
links or special files. The release README and module POD grant the same
license terms as Perl, and Build.PL/META state `perl`. No independent VCS
URL is supplied by the release, so the upstream source repository field
links to the canonical CPAN release page rather than an invented Git URL.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-Reform` nor a `perl(Text::Reform)` provider.
It provides Test::Pod, which the SPEC requires so the default POD test
cannot skip in target CI. This snapshot check does not guarantee future
repository contents.

`%check` retains all three default upstream test files. Local Perl 5.34.1
ran 68 assertions, including POD syntax, with no skips. Installed-RPM
smoke checks a deterministic field format and the module provider. Exact
target CI must prove RPM build and smoke; PR artifacts alone do not
establish public RPM repository publication.
