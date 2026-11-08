<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-findindent-perl

The frozen inventory's exact `libtext-findindent-perl` key maps to Ubuntu
source version 0.12-1. This package uses the official stable
[Text-FindIndent 0.12](https://metacpan.org/dist/Text-FindIndent) CPAN release.
Its HTTPS tarball SHA-256
`93cf7c74b313ac842108f272cd00cd6f705aa711a997d8a6345e3b4cae9242ca`
matches the publisher's `CHECKSUMS` entry. The single-root archive contains
only regular files and directories, with no traversal, links or special
files. The included LICENSE and module POD expressly grant the same terms as
Perl itself despite the release metadata reporting an unknown license.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Text-FindIndent` nor a `perl(Text::FindIndent)`
provider. This is a snapshot check, not a guarantee about future repository
contents. The runtime code has no non-core module dependency; upstream's
build metadata lists Test::More for testing.

Both default upstream `t/*.t` files ran locally with the unmodified release:
65 assertions passed, including 20 fixture-based indentation cases. A
source-level staging install yielded the module and manual page, both listed
in the SPEC. Installed-RPM smoke checks the version, auto-generated Provides
and space-indentation detection. Target RPM build, complete default suite and
installed smoke remain for CI to verify; successful PR artifacts alone do not
prove public repository publication.
