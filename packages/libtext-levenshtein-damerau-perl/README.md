<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-levenshtein-damerau-perl

The frozen inventory's exact `libtext-levenshtein-damerau-perl` key records
Ubuntu source version 0.41-3. This package uses the official
[Text-Levenshtein-Damerau 0.41](https://metacpan.org/dist/Text-Levenshtein-Damerau)
CPAN release. Its HTTPS tarball SHA-256
`3e7d14fa97f31f4862eaf24fa5fa24892aaeb7b363e15222dcdcc82a7caf5e50`
matches the publisher's `CHECKSUMS` entry. The archive contains one root,
regular files and directories only, with no path traversal or links. Its
included `LICENSE` explicitly offers GPL-1.0-or-later OR
Artistic-1.0-Perl, resolving the frozen unverified-upstream marker.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Text-Levenshtein-Damerau` nor the
`perl(Text::Levenshtein::Damerau)` and
`perl(Text::Levenshtein::Damerau::PP)` providers. This is a snapshot check,
not a guarantee about future repository contents. The only declared runtime
dependency is Perl's `List::Util`; optional separately distributed XS
acceleration is not bundled or required.

All six default upstream `t/*.t` files passed 45 assertions locally on Perl
5.34.1 using the unmodified release. Two `xt/*.t` POD checks are not part of
upstream's default `make test` and are not counted as passing. A source-level
staging install yielded both modules and both manual pages, all listed in
the SPEC. The installed-RPM smoke checks both the exported distance function
and object interface. Target RPM build, default tests and installed smoke
remain to be verified by CI; successful PR artifacts alone do not prove
public repository publication.
