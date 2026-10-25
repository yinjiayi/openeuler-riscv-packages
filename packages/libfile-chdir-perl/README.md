<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-chdir-perl

This package maps the frozen inventory's exact `libfile-chdir-perl` key to
the official [File-chdir 0.1011](https://metacpan.org/dist/File-chdir) CPAN
release. The frozen inventory records an older 0.1008 version; 0.1011 is the
latest stable CPAN release and is also present in current Ubuntu source
metadata. Its HTTPS archive was independently downloaded and pinned to
SHA-256 `31ebf912df48d5d681def74b9880d78b1f3aca4351a0ed1fe3570b8e03af6c79`,
matching the official CPAN `CHECKSUMS` index. The 40-entry archive has one
top-level directory and contains no traversal paths, links, or special
files. CI verifies the digest before building on openEuler 24.03 LTS SP3
`riscv64`/RVA23.

`%check` runs all seven default upstream `t/*.t` files. Upstream release and
author-only `xt/` quality checks remain outside that default suite; an
environment-dependent newline-directory test may skip under upstream rules
and is not counted as passed when it does. The installed-RPM smoke checks
the module provider and scoped working-directory restoration. The included
`LICENSE` gives the Perl GPL/Artistic choice. CI artifacts do not prove
public RPM repository publication.
