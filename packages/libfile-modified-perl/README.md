<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-modified-perl

This package maps the frozen inventory's exact `libfile-modified-perl` key to
official stable CPAN [File-Modified 0.10](https://metacpan.org/dist/File-Modified).
The HTTPS source SHA-256
`6b50b1aab6ec6998a017f6403c2735b3bc1e1cf46187bd134d7eb6df3fc45144`
matches the official CPAN `CHECKSUMS` index. Its 18 archive entries occupy one
top-level tree without traversal paths, links, or special files. The archive
includes the Perl GPL/Artistic license choice. Target CI verifies the digest
before building on openEuler 24.03 LTS SP3 `riscv64`/RVA23.

`%check` runs the complete upstream default one-file suite. It tests unchanged
signatures, changed temporary files, digest methods when their optional Perl
modules are installed, and the upstream-declared TODO for deep structure
comparison. The installed-RPM smoke checks the Perl auto-Provide and an
unchanged file signature. Any target skips or failures must be reported from
the exact-head CI, not inferred from local inspection.

Successful PR CI artifacts alone do not prove public RPM repository publication.
