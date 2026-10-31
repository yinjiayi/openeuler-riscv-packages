<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-rewriteprefix-perl

The frozen inventory's exact `libstring-rewriteprefix-perl` key maps to
Ubuntu source version 0.009. This package uses the official stable
[String-RewritePrefix 0.009](https://metacpan.org/dist/String-RewritePrefix)
CPAN release. Its HTTPS tarball SHA-256
`44918bec96a54af8ca37ca897e436709ec284a07b28516ef3cce4666869646d5`
matches the publisher's `CHECKSUMS` entry. The single-root archive contains
only regular files and directories, with no traversal, links or special
files. The included `LICENSE`, README and module POD grant Perl's
GPL-1.0-or-later or Artistic-1.0-Perl terms.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-RewritePrefix` nor a
`perl(String::RewritePrefix)` provider. It supplies `perl-Sub-Exporter`
0.990, above the upstream minimum 0.972. This is a snapshot check, not a
guarantee about future repository contents.

All three unmodified default upstream `t/*.t` files ran locally: 39 tests
passed. The two functional suites cover mappings, longest-prefix selection,
callbacks, import and scalar/list context. The third reports prerequisite
versions. Two `xt/` author/release files are not part of upstream's default
`make test` target and are not counted as passed. The SPEC retains the full
default suite in `%check`; the installed-RPM smoke tests module identity and
three prefix behaviors. Target RPM build, default suite and installed smoke
remain for CI to verify. Successful PR artifacts alone do not prove public
repository publication.
