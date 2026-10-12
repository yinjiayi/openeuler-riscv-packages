<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-levenshtein-perl

The frozen inventory's exact `libtext-levenshtein-perl` key maps to Ubuntu
source 0.15-1 and the official [Text-Levenshtein
0.15](https://metacpan.org/dist/Text-Levenshtein) CPAN release. The CPAN
`CHECKSUMS` entry and downloaded HTTPS archive both have SHA-256
`6d2e92232caf7550bd6fa8034b8ebbacccd81a8dcefa7a605a8ca539a15d2f22`.
Ubuntu repacks the archive: its original tarball MD5
`ecda29d5a78c74e8821498fd8936900d` differs from the CPAN tarball MD5
`8d20308d078a3c01638b964e3d5008cb`. After extraction, the complete file
trees compare equal with `diff -qr`; compressed-byte identity is not claimed.
The official archive has one root without traversal, links or special files.
Included LICENSE, module POD and metadata grant Perl dual GPL/Artistic terms.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-Levenshtein` nor a `perl(Text::Levenshtein)`
provider. It does contain `perl(Unicode::Collate)` 1.31, satisfying the
upstream declared minimum 1.04. This is a snapshot check, not a guarantee
about future repository contents.

`%check` retains all nine default upstream test files, including Swedish,
Russian, Japanese, Greek and diacritic cases. All 252 assertions passed with
local Perl 5.34.1. A source-level staging install yielded the module and man
page, both listed in the SPEC. Installed-RPM smoke checks version and a
deterministic edit distance; target CI must prove RPM build and installation.

Successful PR CI artifacts alone do not prove public RPM repository publication.
