<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-elide-parts-perl

The frozen inventory's exact `libstring-elide-parts-perl` key maps to Ubuntu
source version 0.07-3. This package uses the official stable
[String-Elide-Parts 0.07](https://metacpan.org/dist/String-Elide-Parts) CPAN
release. The HTTPS tarball SHA-256
`342e3b149170002a3a840987c37f717653b930de6e3371b3a957b2a64a17257e`
matches the publisher's `CHECKSUMS` entry. Its single-root archive has no
traversal paths, symlinks or special files. The included LICENSE expressly
contains GPL-1-or-later and Artistic-1.0 terms, resolving the frozen
automated unknown-license marker for this release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-Elide-Parts` nor a
`perl(String::Elide::Parts)` provider, and supplies Test::More 1.302198.
This is a snapshot check, not a guarantee about future repository contents.

Unmodified upstream `make test` locally ran two operational default files:
8 top-level TAP items passed, including nested behavior assertions. Two
additional `t/author-*` files explicitly skipped without upstream
`AUTHOR_TESTING`; they are not counted as functional passes. The SPEC retains
this default contract. A source-level staging install yielded one module and
one manual page, both listed in the SPEC. Installed-RPM smoke checks version,
generated Provides and several supported elision modes. Target RPM build,
the complete default suite and installed smoke remain for CI to verify;
successful PR artifacts alone do not prove public repository publication.
