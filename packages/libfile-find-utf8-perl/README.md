<!-- SPDX-License-Identifier: Apache-2.0 -->
# file-find-utf8

This directory packages upstream `https://metacpan.org/dist/File-Find-utf8` version `0.016` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed CPAN archive is checked against both official MetaCPAN metadata and
the publisher CHECKSUMS entry. The included LICENSE contains Hayo Baan’s
copyright and the full Perl dual-license terms (Artistic-1.0-Perl or
GPL-1.0-or-later). Fedora is discovery lineage only; no downstream recipe is used.

The pure-Perl module is packaged as `perl-file-find-utf8`. The recipe preserves
the original MakeMaker test suite, including the filesystem encoding and warning
tests. The installed smoke discovers a real UTF-8 filename. Target results must
come from exact-head hosted CI; local source and host checks do not establish them.
