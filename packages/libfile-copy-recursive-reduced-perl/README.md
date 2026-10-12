<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-copy-recursive-reduced-perl

This package maps the frozen inventory's exact
`libfile-copy-recursive-reduced-perl` key to official stable CPAN
[File-Copy-Recursive-Reduced 0.008](https://metacpan.org/dist/File-Copy-Recursive-Reduced).
The HTTPS source SHA-256
`462bd66bf55e74b78f29ebdc9626af622d4f0115b5191b03167e82164db98f5a`
matches the official CPAN `CHECKSUMS` index. Its 22 archive entries form one
top-level tree without traversal paths, links or special files. The bundled
LICENSE and module copyright grant Perl GPL/Artistic terms. Target CI checks
the digest before building for openEuler 24.03 LTS SP3 `riscv64`/RVA23.

The official target `primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`
has no RPM named `perl-File-Copy-Recursive-Reduced` and no
`perl(File::Copy::Recursive::Reduced)` Provide. This is a snapshot check,
not a guarantee about future repository state.

`%check` retains all three upstream default suites. It sets
`PERL_AUTHOR_TESTING=1` and declares `File::Copy::Recursive` as a test
dependency so the author-only comparison cases are also exercised. The
upstream tests create and clean isolated temporary directories; they may
conditionally skip hardlink or symlink cases if the target environment lacks
those features. Exact target pass and skip counts await CI. The installed-RPM
smoke checks the Perl auto-Provide and copies a temporary file with `fcopy`.

Successful PR CI artifacts alone do not prove public RPM repository publication.
