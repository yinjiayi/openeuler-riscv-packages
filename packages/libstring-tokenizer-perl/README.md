<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-tokenizer-perl

The frozen inventory's exact `libstring-tokenizer-perl` key maps to Ubuntu
source version 0.06-3. This package uses the official stable
[String-Tokenizer 0.06](https://metacpan.org/dist/String-Tokenizer) CPAN
release. The HTTPS tarball SHA-256
`a921507044b7db43a06abb96bc0aeedafdc68657dd21d3f5a8cfd37d2478e697`
matches the publisher's `CHECKSUMS` entry. Its single-root archive has no
traversal paths, symlinks or special files. The included LICENSE expressly
contains GPL-1-or-later and Artistic-1.0 terms, resolving the frozen
unknown-license metadata for this release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-Tokenizer` nor a
`perl(String::Tokenizer)` provider, and supplies Test::More through
perl-Test-Simple. This is a snapshot check, not a guarantee about future
repository contents.

Unmodified upstream `make test` locally ran two operational default files:
117 assertions passed, covering tokenization and iterator behavior. Two
additional `t/release-*` files explicitly skipped under upstream's
release-candidate conditions; they are not counted as passing tests. The
SPEC retains this default contract. A source-level staging install yielded
one module and one manual page, both listed in the SPEC. Installed-RPM smoke
checks version, generated Provides, tokenization and iterator behavior.
Target RPM build, the complete default suite and installed smoke remain for
CI to verify; successful PR artifacts alone do not prove public repository
publication.
