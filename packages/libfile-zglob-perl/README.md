<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-zglob-perl

The frozen inventory's exact `libfile-zglob-perl` key maps to the latest
official [File-Zglob 0.11](https://metacpan.org/dist/File-Zglob) release.
The CPAN HTTPS archive and its official `CHECKSUMS` entry both have SHA-256
`1cb1edde20ac094ef003794bafef2c7624169cf8402c7367d9b7460f6c0e669b`.
All archive entries remain under one top-level tree, with no traversal paths
or special file types. The module POD expressly grants redistribution and
modification under Perl's terms.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither a `perl-File-Zglob` RPM nor a `perl(File::Zglob)` provider.
This snapshot check does not guarantee future repository contents.

`%check` retains all four default upstream `t` files. Local Perl 5.34.1
passed all four files and 21 assertions. The upstream author-only `xt` files
are not part of the default test target and are preserved in the source,
not represented as default-suite results. The installed-RPM smoke verifies
the module, generated provider, and recursive globbing against a private
temporary fixture. QEMU target build and smoke remain unverified until
exact-head CI; PR artifacts alone do not establish public RPM publication.
