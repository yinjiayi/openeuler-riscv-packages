<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-escape-perl

The frozen inventory's exact `libstring-escape-perl` key maps to Ubuntu
source version 2010.002-3. This package uses the official stable
[String-Escape 2010.002](https://metacpan.org/dist/String-Escape) CPAN
release. Its HTTPS tarball SHA-256
`fd645f8b336224d20a85ae7fb1a384576eac329f7adc3923c3241e828e3b9a8a`
matches the publisher's `CHECKSUMS` entry. The single-root archive has no
traversal paths, symlinks or special files. Module POD grants the same terms
as Perl; README expressly grants GPL or Artistic, and Makefile.PL and
META.yml identify Perl dual terms. This resolves frozen unknown-license
metadata for this release. README is included as the license notice.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-Escape` nor a `perl(String::Escape)` provider.
It supplies Test::Pod 1.52, Test::Pod::Coverage 1.10 and Pod::Coverage 0.23.
This is a snapshot check, not a guarantee about future repository contents.

Unmodified upstream `make test` locally ran eight default files: seven suites
passed with 46 assertions, while `t/92-pod-coverage.t` explicitly skipped
because local Test::Pod::Coverage was absent. The SPEC requires the target
modules so that this suite executes in CI; it is not counted as passing
before target evidence. No tests were disabled. Source-level staging yielded
one module and one manual page, both listed in the SPEC. Installed-RPM smoke
checks version, generated Provides and backslash round-trip behavior. Target
RPM build, full suite and installed smoke remain for CI to verify; PR
artifacts alone do not prove public repository publication.
