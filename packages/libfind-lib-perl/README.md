<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfind-lib-perl

This directory packages upstream `https://metacpan.org/dist/Find-Lib` version `1.04` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The signed CPAN release matches Debian stable's original archive. Its README
and module retain the author's Perl dual grant; both full texts are shipped.

All 17 original tests remain unchanged, including the symlink cases. Only
the test command adds the verified source root to `PERL5LIB` so current Perl
can resolve `t/testutils.pl`. The Linux recipe checks for the canonical
module and a single canonical manpage; the case-insensitive macOS host can
generate a duplicate from the same source inode and is not target evidence.
Installed smoke verifies that an application loads an explicit private
library relative to its script from a different working directory.
