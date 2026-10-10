<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-greeking-perl

The frozen inventory's exact key `libtext-greeking-perl` maps to the official
[Text-Greeking 0.15](https://metacpan.org/dist/Text-Greeking) CPAN release.
Its HTTPS archive and official `CHECKSUMS` entry both have SHA-256
`b4657a0044bf0db6b79957bcb13b63653fa070bc23a725ab5b0aca649a75b540`.
The archive contains one top-level tree, with no traversal path, link or
special file.

The frozen inventory marked this release `license-blocked` and
`unverified-upstream`. Review of the actual release `LICENSE`, `README`,
`Makefile.PL` and module POD establishes Artistic License 1.0 only. The
SPEC does not assume the usual Perl GPL alternative.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-Greeking` nor a `perl(Text::Greeking)` provider.
It provides target Test::Pod and Test::Pod::Coverage modules. This snapshot
does not guarantee future repository contents.

`%check` retains all three default upstream tests and sets `RELEASE_TESTING`
to activate the two conditional POD checks. Local Perl 5.34.1 ran compile
and POD syntax checks, while POD coverage skipped for a missing local module.
That skip is not counted as a pass; exact-head target CI must prove it.
Installed-RPM smoke exercises text generation from a fixed three-word source
without asserting a particular random sequence. PR artifacts alone do not
establish public RPM repository publication.
