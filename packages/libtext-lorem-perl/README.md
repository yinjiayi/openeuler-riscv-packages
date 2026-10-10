<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-lorem-perl

The frozen inventory's exact `libtext-lorem-perl` key maps to official
[Text-Lorem 0.34](https://metacpan.org/dist/Text-Lorem). The CPAN HTTPS
archive and its official `CHECKSUMS` entry both have SHA-256
`0ce6a3c19917b2323424a1aa742d988b063c39440427a3101a4cec6dbd847157`.
All archive entries stay under one top-level tree; none is a traversal path,
link or special file. The README and module POD say the software has the
same license as Perl; Makefile.PL and META confirm `perl_5`, mapped to
`GPL-1.0-or-later OR Artistic-1.0-Perl`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-Lorem` nor a `perl(Text::Lorem)` provider. This
snapshot check does not guarantee future repository contents.

`%check` retains all five default upstream tests. Local Perl 5.34.1 ran all
23 assertions with no skip. The release also contains `bin/lorem`, but
MakeMaker does not install it and its archive mode is not executable; this
SPEC installs it explicitly as a command. Installed-RPM smoke checks word,
sentence and paragraph counts, the command, and the module provider. Exact
target CI must prove the RPM build and smoke. PR artifacts alone do not
establish public RPM repository publication.
