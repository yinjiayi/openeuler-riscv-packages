<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdate-simple-perl

This directory packages upstream `https://metacpan.org/dist/Date-Simple` version `3.03` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The official CPAN archive is pinned in `sources.yaml`; the archive
SHA-256 agrees with the publisher index and MetaCPAN release metadata.
The original README, COPYING and module retain the GPL-2.0-or-later
or Perl Artistic terms and the Kasei, John Tobey and Yves Orton notices.
Debian stable's 3.0300-3 is naming lineage only.

The architecture-specific package builds the original XS and runs all
three original test files (233 assertions). Installed smoke checks
leap-day rollover with native XS loaded rather than the Perl fallback.
Host preflight does not replace target CI.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
