<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-parity-perl

The frozen inventory's exact `libstring-parity-perl` key maps to Ubuntu
source version 1.34-3. This package uses the official stable
[String-Parity 1.34](https://metacpan.org/dist/String-Parity) CPAN release.
The HTTPS tarball SHA-256
`c0ae3bd7a2862654ca6bc7b30c882687e9812c185fd944dfeea54a57d2a29694`
matches the publisher's `CHECKSUMS` entry. Its single-root archive has no
traversal paths, symlinks or special files. The included LICENSE expressly
contains GPL-1-or-later and Artistic-1.0 terms, resolving the frozen
unknown-license metadata for this release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-Parity` nor a `perl(String::Parity)` provider.
The module only needs Perl core facilities. This is a snapshot check, not a
guarantee about future repository contents.

Unmodified upstream `make test` locally ran its sole default
`t/String-Parity.t` suite: all 33 byte-parity checks passed. No tests were
disabled. A source-level staging install yielded one module and one manual
page, both listed in the SPEC. Installed-RPM smoke checks version, generated
Provides, and even/odd byte parity. Target RPM build, the complete default
suite and installed smoke remain for CI to verify; successful PR artifacts
alone do not prove public repository publication.
