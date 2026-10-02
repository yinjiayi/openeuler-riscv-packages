<!-- SPDX-License-Identifier: Apache-2.0 -->
# libnet-dns-resolver-mock-perl

The frozen inventory's exact `libnet-dns-resolver-mock-perl` key maps to
Ubuntu resolute/universe and Debian stable source version `1.20230216-1`.
This package uses the official
[Net-DNS-Resolver-Mock 1.20230216](https://metacpan.org/dist/Net-DNS-Resolver-Mock)
CPAN archive, pinned to SHA-256
`ed4930577fd1a29d6435b5875533d3b28f5c1258a35833fe6ca2cb6a2685a49b`
as published in MBRADSHAW's `CHECKSUMS`. The archive contains one top-level
tree and only ordinary files and directories.

The top-level `LICENSE` and module POD grant the Perl 5 dual GPL/Artistic
choice. The test zonefile uses synthetic `example.net` names and documentation
IP addresses; it is not a copied production DNS dataset. Two generated
author-only test files come from Perl-5-licensed Dist::Zilla plugins and are
retained unchanged in the source archive.

`%check` runs all five original `t/*.t` files: three functional files with
41 assertions, and two upstream author-only files that self-skip without
`AUTHOR_TESTING`. A fresh local macOS Perl run passed all 41 functional
assertions with those two upstream skips. The target openEuler 24.03 LTS SP3
`riscv64`/RVA23 result and installed-RPM smoke remain subject to exact-head
CI; local Perl results are not target evidence. The installed smoke exercises
positive and negative answers from an in-memory zone without external DNS.
PR CI artifacts alone do not prove public RPM/SRPM publication.
