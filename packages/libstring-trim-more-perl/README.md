<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-trim-more-perl

The frozen inventory's exact `libstring-trim-more-perl` key maps to Ubuntu
source version 0.03-2. This package uses the official stable
[String-Trim-More 0.03](https://metacpan.org/dist/String-Trim-More) CPAN
release; it is distinct from String::Trim. Its HTTPS tarball SHA-256
`739cfbd73e0a92897c6f31f0ad8d72a56302f8805e9707d4edca5e5086c14e7f`
matches the publisher's `CHECKSUMS` entry. The single-root archive contains
only regular files and directories, with no traversal, links or special
files. The included LICENSE expressly grants the same terms as Perl itself
despite frozen metadata reporting an unknown license.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-Trim-More` nor a
`perl(String::Trim::More)` provider. This is a snapshot check, not a
guarantee about future repository contents. The runtime module has no
non-core dependencies.

Unmodified upstream `make test` locally ran two operational default files:
15 top-level TAP items passed, with nested trim behavior assertions. Two
additional `t/author-*` files were explicitly skipped by upstream without
`AUTHOR_TESTING`; they are not counted as functional passes. The SPEC retains
this default contract. A source-level staging install yielded the module and
manual page, both listed in the SPEC. Installed-RPM smoke checks version,
generated Provides, whole-string/per-line trimming and ellipsis. Target RPM
build, default suite and installed smoke remain for CI to verify;
successful PR artifacts alone do not prove public repository publication.
