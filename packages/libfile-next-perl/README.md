<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-next-perl

This package maps the frozen inventory's exact `libfile-next-perl` key to
official stable CPAN [File-Next 1.18](https://metacpan.org/dist/File-Next).
The HTTPS source SHA-256
`f900cb39505eb6e168a9ca51a10b73f1bbde1914b923a09ecd72d9c02e6ec2ef`
matches the official CPAN `CHECKSUMS` index. Its 53 archive entries have one
top-level tree without path traversal, links, or special files. Target CI
verifies the digest before building on openEuler 24.03 LTS SP3
`riscv64`/RVA23.

`%check` retains all 16 top-level default upstream test files, including the
FIFO/fork test and both optional POD suites. POD dependencies are declared so
those suites run rather than silently skip. The nested `t/swamp/perl-test.t`
is a test fixture in the source tree, not part of upstream's default `t/*.t`
suite. The installed-RPM smoke checks the Perl auto-Provide and iterates an
isolated temporary directory. Upstream declares Artistic License 2.0 in its
module and release metadata but provides no standalone license file.

Successful PR CI artifacts alone do not prove public RPM repository
publication.
