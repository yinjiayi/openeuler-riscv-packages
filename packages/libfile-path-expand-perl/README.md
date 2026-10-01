<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-path-expand-perl

This package maps the frozen inventory's exact `libfile-path-expand-perl` key
to official stable CPAN [File-Path-Expand 1.02](https://metacpan.org/dist/File-Path-Expand).
The HTTPS source SHA-256
`7fb616a5d5904400a9e355ca540049a08605c60ce4f94297f2f8bd95dee9b495`
matches the official CPAN `CHECKSUMS` index. Its 12 archive entries occupy one
top-level tree without traversal paths, links, or special files. The module's
copyright section explicitly permits redistribution and modification under
Perl's GPL/Artistic terms. Target CI verifies the digest before building on
openEuler 24.03 LTS SP3 `riscv64`/RVA23.

`%check` runs the entire upstream default one-file suite. The upstream file
declares eight assertions, but five self-skip unless the hostname is exactly
the author's `penfold.unixbeard.net`; they are not evidence of passed target
behavior. The installed-RPM smoke separately checks the Perl auto-Provide and
HOME-based expansion. No tests are deleted, suppressed, or patched.

Successful PR CI artifacts alone do not prove public RPM repository publication.
