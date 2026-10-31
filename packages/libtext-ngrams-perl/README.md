<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-ngrams-perl

The frozen inventory's exact `libtext-ngrams-perl` key recorded Ubuntu
source 2.006-2. Official CPAN now lists
[Text-Ngrams 2.007](https://metacpan.org/dist/Text-Ngrams). Its HTTPS
archive and official `CHECKSUMS` entry both have SHA-256
`0d64bd8b72b31bfeaf06212a8878a8000432a091f8c2bf2d9dc9e7ecbd5f6995`.
All archive paths stay under one top-level tree without traversal paths,
links or special files; the root directory is restrictive mode 0700,
which remains to be exercised by target CI. README, module and CLI POD
credit contributors and grant the same license terms as Perl. The
checked-in large text fixture excerpts are from the 1843 novel
*A Christmas Carol*. The release does not declare an HTTPS
VCS URL, so source_repository links to its canonical CPAN page.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-Ngrams` nor a `perl(Text::Ngrams)` provider.
This snapshot check does not guarantee future repository contents.

`%check` retains all fifteen default upstream tests and their expected
output fixtures. Local Perl 5.34.1 ran 32 assertions with no skips. A
source-level vendor install produced the module, companion script,
command and two man pages; the SPEC lists all of them. Installed-RPM
smoke checks deterministic byte n-gram counts, the command and provider.
The CLI imports `Getopt::Long`, which the official target primary snapshot
provides and the SPEC declares as both a build and runtime dependency.
Exact target CI must prove the RPM build and smoke; PR artifacts alone
do not establish public RPM repository publication.
