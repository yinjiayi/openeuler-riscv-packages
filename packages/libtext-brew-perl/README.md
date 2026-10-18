<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-brew-perl

The frozen inventory's exact `libtext-brew-perl` key maps to Ubuntu source
version 0.02-3. This package uses the official stable
[Text-Brew 0.02](https://metacpan.org/dist/Text-Brew) CPAN release. Its HTTPS
tarball SHA-256
`aa1b85841cf9fc6fe338366bbc870a4e9304a27641e63f92a1fd96bee8ebf64c`
matches the publisher's `CHECKSUMS` entry. The single-root archive contains
only regular files and directories, with no traversal, links or special
files. The included README and module POD both expressly grant the same
terms as Perl itself despite the release metadata reporting an unknown
license. No separate license-text file is included, so the README is
installed as `%license`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Text-Brew` nor a `perl(Text::Brew)` provider, while
`perl-Test-Pod` 1.52 is available. This is a snapshot check, not a guarantee
about future repository contents. Upstream's `Makefile.PL` declares
`Test::More` as a prerequisite; the SPEC retains it.

All three default upstream `t/*.t` files ran locally with the unmodified
release: 18 assertions passed, including the POD check. The SPEC requires
`perl-Test-Pod` so that the POD file is exercised, not silently skipped, in
target CI. The compile test prints a hard-coded historical Perl version in
its diagnostic; that string is not evidence of the interpreter running the
test. A source-level staging install yielded the module and manual page,
both listed in the SPEC. Installed-RPM smoke checks distance and edit
sequence. Target RPM build, the complete default suite and installed smoke
remain for CI to verify; successful PR artifacts alone do not prove public
repository publication.
