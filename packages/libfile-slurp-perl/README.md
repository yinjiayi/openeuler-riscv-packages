<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-slurp-perl

This package maps the frozen inventory's exact `libfile-slurp-perl` key to
the official [File-Slurp 9999.32](https://metacpan.org/dist/File-Slurp)
CPAN release. Its HTTPS archive was independently downloaded and pinned to
SHA-256 `4c3c21992a9d42be3a79dd74a3c83d27d38057269d65509a2f555ea0fb2bc5b0`,
matching the official CPAN `CHECKSUMS` index. The 55-entry archive has one
top-level tree with no traversal paths, links, or special files. CI verifies
the digest before building for openEuler 24.03 LTS SP3 `riscv64`/RVA23.

`%check` runs all 30 default upstream `t/*.t` files. Platform-specific
SKIP/TODO branches and the intentionally skipped taint test are not counted
as passes; author-only `xt/author` quality checks remain outside the default
suite. The installed-RPM smoke verifies the module provider and an isolated
write/read round-trip. The source module's copyright POD declares the same
GPL/Artistic choice as Perl, although the archive has no standalone license
file. CI artifacts do not prove public RPM repository publication.

File::Slurp is used by Convert-BinHex's upstream tests in PR
[#2162](https://github.com/yinjiayi/openeuler-riscv-packages/pull/2162).
