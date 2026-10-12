<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-pushd-perl

This package maps the frozen inventory's exact `libfile-pushd-perl` key to
official stable CPAN [File-pushd 1.016](https://metacpan.org/dist/File-pushd).
The HTTPS source SHA-256
`d73a7f09442983b098260df3df7a832a5f660773a313ca273fa8b56665f97cdc`
matches the official CPAN `CHECKSUMS` index. Its 37 archive entries occupy one
top-level tree and contain no traversal paths, links, or special files. The
archive includes the Apache-2.0 license. Target CI verifies the pinned digest
before building on openEuler 24.03 LTS SP3 `riscv64`/RVA23.

`%check` runs all four upstream default `t/*.t` files, including directory
restoration, temporary-directory cleanup, subprocess behavior, exception
preservation, and void-context handling. The separate `xt/` author and release
tests are not registered in the upstream default MakeMaker target and require
additional development-only dependencies. The installed-RPM smoke verifies the
Perl auto-Provide and a scoped directory change followed by restoration.

Successful PR CI artifacts alone do not prove public RPM repository publication.
