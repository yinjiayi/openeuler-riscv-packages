<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-wikicreole-perl

The frozen inventory's exact `libtext-wikicreole-perl` key maps to Ubuntu and
Debian source version 0.07-3. This package uses the official stable
[Text-WikiCreole 0.07](https://metacpan.org/dist/Text-WikiCreole) CPAN release.
Its HTTPS tarball SHA-256
`34d1e4eb65351d5a303a50daf463a9edf854e396680444e80c0a8fb6944b1e90`
matches the publisher's `CHECKSUMS` entry. The single-root archive contains
only regular files and directories, with no traversal, links or special
files. The included README and module POD both explicitly grant the same
terms as Perl itself, resolving the frozen automated `license-blocked`
decision for this release. No separate license-text file is included, so the
README is installed as `%license`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Text-WikiCreole` nor a `perl(Text::WikiCreole)`
provider. This is a snapshot check, not a guarantee about future repository
contents. The implementation imports only core modules, while upstream
`Makefile.PL` declares `Test::More` as a prerequisite; the SPEC retains that
declared dependency.

All eight default upstream `t/*.t` files passed their eight fixture-based
assertions locally with the release unmodified. Each case compares generated
XHTML with a shipped expected output or checks a callback behavior. There
are no upstream test exclusions or expected failures in this default suite.
A source-level staging install yielded the module and manual page, both
listed in the SPEC. Installed-RPM smoke checks simple paragraph conversion.
Target RPM build, the same default tests and installed smoke remain for CI
to verify; successful PR artifacts alone do not prove public publication.
