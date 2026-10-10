<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-ansi-util-perl

The frozen inventory's exact `libtext-ansi-util-perl` key maps to Ubuntu
source version 0.234-1. This package uses the official stable
[Text-ANSI-Util 0.234](https://metacpan.org/dist/Text-ANSI-Util) CPAN release.
Its HTTPS tarball SHA-256
`17eb1f7bb270b1cb2a827262587a66c0e04abfa535a80bb0800ec44317035240`
matches the publisher's `CHECKSUMS` entry. The single-root archive contains
only regular files and directories, with no traversal, links or special
files. The included LICENSE expressly grants the same terms as Perl itself;
the frozen discovery's historical `license-blocked` marker is therefore
resolved by direct review of the release archive, not treated as a waiver.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Text-ANSI-Util` nor a `perl(Text::ANSI::Util)`
provider; it does provide the test dependency `perl(Data::Dump)`. This is a
snapshot check, not a guarantee about future repository contents. The
upstream runtime requirement is List::Util 1.54 or newer.

Unmodified upstream `make test` locally passed its two operational default
files with 16 top-level TAP checks (including nested ANSI behavior checks).
Three additional `t/author-*` files were explicitly skipped by upstream
because `AUTHOR_TESTING` was not set; these are not counted as passing
functional tests. The SPEC retains the same default contract. A source-level
staging install yielded two modules and two manual pages, all listed in the
SPEC. Installed-RPM smoke checks both Provides, version, escape stripping
and visible text length. Target RPM build, default suite and installed smoke
remain for CI to verify; successful PR artifacts alone do not prove public
repository publication.
