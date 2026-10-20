<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-truncate-perl

The frozen inventory's exact `libstring-truncate-perl` key maps to Ubuntu
source version 1.100603-1. This package uses the official stable
[String-Truncate 1.100603](https://metacpan.org/dist/String-Truncate) CPAN
release. The HTTPS tarball SHA-256
`ab45602cce2dd9515edfbb2e6e5cde19cdd5498d61a23afd8c46c1f11f8eec62`
matches the publisher's `CHECKSUMS` entry. Its single-root archive has no
traversal paths, symlinks or special files. The included LICENSE expressly
contains GPL-1-or-later and Artistic-1.0 terms, resolving frozen
unknown-license metadata for this release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-Truncate` nor a `perl(String::Truncate)`
provider. It supplies ExtUtils::MakeMaker 7.70, Sub::Exporter 0.990 and
Sub::Install 0.929, satisfying upstream's minimum versions. This is a
snapshot check, not a guarantee about future repository contents.

All four unmodified default upstream `t/*.t` files ran locally: 65 checks
passed, including left, right, middle, ends and export behavior. The report
prerequisites file is retained in the default suite. No tests were disabled.
A source-level staging install yielded one module and one manual page, both
listed in the SPEC. Installed-RPM smoke checks version, generated Provides
and three shortening modes. Target RPM build, the complete default suite
and installed smoke remain for CI to verify; successful PR artifacts alone
do not prove public repository publication.
