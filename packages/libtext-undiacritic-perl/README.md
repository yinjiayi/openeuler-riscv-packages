<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-undiacritic-perl

The frozen inventory's exact `libtext-undiacritic-perl` key maps to official
[Text-Undiacritic 0.07](https://metacpan.org/dist/Text-Undiacritic). The
CPAN HTTPS archive and its official `CHECKSUMS` entry both have SHA-256
`6ba5bfac2a57462aa7a06d7254fefe08511ba36f7e4590fdc54573d821e261a9`.
All archive entries stay under one top-level tree without traversal paths,
links or special files. The bundled `LICENSE` explicitly grants GPL version
1 or later or Perl Artistic License terms. The README retains an outdated
0.01 documentation version, while release metadata and module VERSION are
0.07; the SPEC uses the latter.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-Undiacritic` nor a `perl(Text::Undiacritic)`
provider. It provides Module::Build::Tiny, Unicode::Normalize and Test::Pod.
This snapshot check does not guarantee future repository contents.

`%check` retains all three default upstream `t` files and sets
`RELEASE_TESTING=1` to activate the conditional POD syntax test. Local Perl
5.34.1 ran all 14 assertions with no skips. Separate `xt` author checks
are not part of default `Build test` and are not claimed as run. Installed
smoke checks both precomposed and combining Unicode diacritics, plus the
module provider. Target CI must prove RPM build and smoke; PR artifacts
alone do not establish public RPM repository publication.
