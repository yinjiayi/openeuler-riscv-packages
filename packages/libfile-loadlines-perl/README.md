<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-loadlines-perl

This package maps the frozen inventory's exact `libfile-loadlines-perl` key to
official stable CPAN [File-LoadLines 1.047](https://metacpan.org/dist/File-LoadLines).
The HTTPS source SHA-256
`26efd9682e4ecf91c1efe3e3e27bd8bcfaeea9c3c5e2eb432ed4f96968f84707`
matches the official CPAN `CHECKSUMS` index. Its 37 archive entries occupy one
top-level tree without traversal paths, links, or special files. The module
explicitly grants redistribution and modification under Perl's GPL/Artistic
terms. Target CI verifies the digest before building on openEuler 24.03 LTS
SP3 `riscv64`/RVA23.

The official target repository's `primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`
has no `perl-File-LoadLines` RPM. A recent locked-image baseline also has no
such RPM; these are existence checks, not proof of future repository state.

`%check` runs all 14 upstream default test files with their bundled Unicode
fixtures. Those tests cover files, scalar references, encoding, blobs and
soft failures. Upstream does not test data URLs or optional HTTP fetching via
LWP in the default suite; this package does not claim to validate HTTP. The
installed-RPM smoke independently checks the Perl auto-Provide and base64
data-URL loading.

Successful PR CI artifacts alone do not prove public RPM repository publication.
