<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-slurp-tiny-perl

The frozen inventory's exact `libfile-slurp-tiny-perl` key maps to official
[File-Slurp-Tiny 0.004](https://metacpan.org/dist/File-Slurp-Tiny).
The CPAN `CHECKSUMS` entry and downloaded HTTPS archive both have SHA-256
`452995beeabf0e923e65fdc627a725dbb12c9e10c00d8018c16d10ba62757f1e`.
All 26 archive entries are under one top-level tree, with no traversal paths,
links or special files. The full `LICENSE` explicitly grants Perl's
GPL-1-or-later OR Artistic dual-license terms.

Upstream labels the distribution `DISCOURAGED` in `Makefile.PL`. This package
preserves compatibility for consumers of its API; it is not a recommendation
for new projects.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-Slurp-Tiny` nor `perl(File::Slurp::Tiny)`. This is
a snapshot check, not a guarantee about future state.

`%check` keeps the sole default upstream test file and all 10 assertions;
it passed on local Perl 5.34.1. The optional `xt/author` and `xt/release`
tests are not part of the default distribution suite and were not run.
Target CI must still prove the complete QEMU result. The installed-RPM
smoke checks reading, writing, line parsing, and directory listing in an
automatically cleaned temporary directory.

Successful PR CI artifacts alone do not prove public RPM repository publication.
