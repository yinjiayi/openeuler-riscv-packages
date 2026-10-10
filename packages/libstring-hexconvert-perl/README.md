<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-hexconvert-perl

The frozen inventory's exact `libstring-hexconvert-perl` key maps to the
official stable CPAN String::HexConvert 0.02 release. Its HTTPS tarball
SHA-256 `10105a512be930961c1f5d95d64aa9e5e0d321b7ca4f594eae17f91369d1282b`
matches publisher `CHECKSUMS`. The inspected archive has one root and only
regular files and directories, with no traversal, links or special files.
The archived `LICENSE`, `README` and `dist.ini` specify LGPL version 3;
the module's shorter "LGPL" wording is read alongside those explicit
release documents. This resolves the frozen `license-blocked` historical
marker for this exact release, mapped to `LGPL-3.0-only`. The full license
text is installed in the RPM.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-HexConvert` nor a
`perl(String::HexConvert)` provider. Exporter is its only runtime module
dependency. This snapshot check does not guarantee future repository
contents.

Unmodified upstream `make test` ran all five default `t/*.t` files locally:
the two ordinary files passed three assertions total. The other three are
author-only suites and each emitted its upstream `AUTHOR_TESTING` skip;
they are not counted as passing. The `%check` command retains all files
without setting that author-only flag. A source-level staged install
produced the module and manual page listed in the SPEC. Installed-RPM smoke
checks version, generated Provides, both conversion directions and a
binary round trip. Target RPM build, default test outcome and installed
smoke remain for CI to verify; PR artifacts alone do not prove public
repository publication.
